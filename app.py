"""
app.py
------
WellAware AI – Patient Wellness Campaign Visual Generator (Team 17)

Professional graphic poster generator creating campaign-ready wellness visuals
matching reference designs (Split Editorial, Radiant Sunburst, World Health Day,
and Minimalist Modern Geometry).
"""

from __future__ import annotations

import inspect
import uuid
from datetime import datetime
from typing import Optional

import streamlit as st

import config
from modules import image_utils
from modules.image_generator import (
    GenerationError,
    WellnessImageGenerator,
    check_dependencies,
    get_device_info,
    unload_cuda_memory,
)
from modules.prompt_processor import (
    PosterCopy,
    build_prompt,
    generate_poster_copy,
    get_campaign_preset,
    get_example_prompt,
    get_random_suggestion,
    validate_user_input,
)

# ==================================================================
# Page setup
# ==================================================================
st.set_page_config(
    page_title=f"{config.APP_NAME} · {config.APP_SUBTITLE}",
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO = str(image_utils.ensure_logo())

STRETCH = ({"width": "stretch"} if "width" in inspect.signature(st.button).parameters
           else {"use_container_width": True})
C = config.COLORS
PAGES = ["🏠 Home", "✨ Create Campaign", "🖼️ Gallery", "🛡️ Guidelines & Help"]


# ==================================================================
# Styling
# ==================================================================
def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"], .stMarkdown, button, input, textarea {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .stApp {{ background: #FAFCFD; }}
        .block-container {{ padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1280px; }}
        h1, h2, h3, h4 {{ color: {C['text']}; font-weight: 700; }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {C['bg_soft']} 0%, #FFFFFF 100%);
            border-right: 1px solid {C['border']};
        }}
        .sb-brand {{ font-size: 1.35rem; font-weight: 800; color: {C['primary_dark']}; margin: 0; }}
        .sb-sub {{ font-size: .8rem; color: {C['muted']}; margin-top: -4px; }}

        /* Buttons */
        .stButton > button, .stDownloadButton > button {{
            border-radius: 12px; font-weight: 600; border: 1px solid {C['border']};
            transition: all .15s ease-in-out;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: {C['primary']}; color: {C['primary_dark']};
            transform: translateY(-1px); box-shadow: 0 4px 12px rgba(15,157,154,.15);
        }}
        .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {{
            background: linear-gradient(90deg, {C['primary']} 0%, {C['secondary']} 100%);
            color: white; border: none;
        }}
        .stButton > button[kind="primary"]:hover {{ color: white; filter: brightness(1.05); }}

        /* Inputs */
        textarea, input, [data-baseweb="select"] > div {{ border-radius: 10px !important; }}

        /* Bordered containers */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important; border-color: {C['border']} !important;
            background: #FFFFFF;
        }}

        /* Hero */
        .hero {{
            background: linear-gradient(125deg, #0D253F 0%, #0F9D9A 60%, #3BA4E8 100%);
            border-radius: 22px; padding: 2.6rem 2.4rem; color: white;
            box-shadow: 0 12px 30px rgba(13,37,63,.22); margin-bottom: 1.6rem;
        }}
        .hero h1 {{ color: white; font-size: 2.6rem; margin: 0; font-weight: 800; }}
        .hero h3 {{ color: #E6FAF9; font-weight: 500; margin: .3rem 0 1rem 0; }}
        .hero p  {{ font-size: 1.05rem; max-width: 820px; opacity: .95; }}
        .badge {{
            display: inline-block; background: rgba(255,255,255,.18); color: white;
            padding: .25rem .8rem; border-radius: 999px; font-size: .8rem; margin-right: .4rem;
        }}
        .card {{
            background: #FFFFFF; border: 1px solid {C['border']}; border-radius: 16px;
            padding: 1.2rem 1.2rem; height: 100%;
            box-shadow: 0 2px 10px rgba(31,59,77,.04);
        }}
        .card .icon {{ font-size: 1.8rem; }}
        .card h4 {{ margin: .4rem 0 .3rem 0; font-size: 1.02rem; }}
        .card p  {{ color: {C['muted']}; font-size: .9rem; margin: 0; }}
        .chip {{
            display: inline-block; background: {C['bg_soft']}; color: {C['primary_dark']};
            border: 1px solid {C['border']}; padding: .2rem .7rem; border-radius: 999px;
            font-size: .8rem; font-weight: 600; margin: 0 .3rem .3rem 0;
        }}
        .section-title {{ font-size: 1.25rem; font-weight: 700; color: {C['text']}; margin: 1.4rem 0 .6rem 0; }}
        .label {{ font-weight: 700; color: {C['text']}; margin-bottom: .25rem; font-size: .92rem; }}
        .muted {{ color: {C['muted']}; font-size: .88rem; }}
        .disclaimer {{
            background: #FFF9EC; border: 1px solid #F6E3B4; border-radius: 14px;
            padding: .9rem 1.1rem; color: #6B5414; font-size: .88rem;
        }}
        .empty {{
            border: 2px dashed {C['border']}; border-radius: 18px; padding: 3rem 1.5rem;
            text-align: center; color: {C['muted']}; background: {C['bg_soft']};
        }}
        .empty .big {{ font-size: 3rem; }}
        .footer {{ text-align: center; color: {C['muted']}; font-size: .8rem; margin-top: 2.5rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==================================================================
# Session state & Callbacks
# ==================================================================
def init_state() -> None:
    first_cat = list(config.CATEGORIES)[0]
    preset = get_campaign_preset(first_cat)

    defaults = {
        "nav": PAGES[0],
        "gallery": [],
        "last_results": [],
        "last_request": None,
        "pending_request": None,
        "user_prompt": "A friendly healthcare professional in blue scrubs, smiling in a bright modern clinic, waist-up portrait, hands out of frame.",
        "category": first_cat,
        "custom_category": "",
        "poster_layout": config.DEFAULT_POSTER_LAYOUT,
        "poster_title": preset.headline,
        "poster_slogan": preset.slogan,
        "poster_body": preset.body,
        "poster_tips": "\n".join(preset.bullet_points),
        "poster_quote": preset.quote,
        "poster_org": preset.org_name,
        "style": config.DEFAULT_STYLE,
        "theme_choice": "✨ Auto-Detect from Prompt & Campaign",
        "engine_mode": "🤖 Generative AI Engine (SD-Turbo)",
        "model_label": config.DEFAULT_MODEL,
        "first_visit": True,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    if not st.session_state.get("_quality_defaults_migrated"):
        if st.session_state.get("model_label") == "SD-Turbo (fast, recommended)":
            st.session_state.model_label = config.DEFAULT_MODEL
            if st.session_state.get("style") == "Flat Vector Graphic":
                st.session_state.style = config.DEFAULT_STYLE
        st.session_state["_quality_defaults_migrated"] = True


def go_to(page: str) -> None:
    st.session_state.nav = page


def get_recommended_layout(category: str) -> str:
    """Intelligently recommend the best poster layout style for a category."""
    if "Heart" in category:
        return "Radiant Sunburst (Reference 1)"
    elif "Blood" in category:
        return "Minimalist Modern Geometry (Reference 4)"
    elif "World Health" in category:
        return "World Health Day Card (Reference 2)"
    elif "Fitness" in category:
        return "Radiant Sunburst (Reference 1)"
    elif "Mental" in category:
        return "Split Editorial (Reference 3)"
    else:
        return "Modern Visual Hero (Full-Bleed)"


def cb_category_change() -> None:
    """Triggered automatically when the user selects a new campaign category."""
    cat = st.session_state.category
    if cat != config.CUSTOM_CATEGORY and cat in config.CAMPAIGN_PRESETS:
        preset = config.CAMPAIGN_PRESETS[cat]
        # Only fill prompt if user hasn't typed an expressive custom prompt
        current = st.session_state.get("user_prompt", "").strip()
        is_preset = any(current == p.get("artwork_prompt", "").strip() for p in config.CAMPAIGN_PRESETS.values())
        if not current or is_preset:
            st.session_state.user_prompt = preset.get("artwork_prompt", "")
        st.session_state.poster_title = preset["headline"]
        st.session_state.poster_slogan = preset["slogan"]
        st.session_state.poster_body = preset["body"]
        st.session_state.poster_tips = "\n".join(preset["bullet_points"])
        st.session_state.poster_quote = preset["quote"]
        st.session_state.poster_org = preset["org_name"]
        st.session_state.poster_layout = get_recommended_layout(cat)
    elif cat == config.CUSTOM_CATEGORY:
        st.session_state.poster_layout = config.DEFAULT_POSTER_LAYOUT


def cb_autofill_copy() -> None:
    cat = st.session_state.get("category", "Mental Health")
    cust = st.session_state.get("custom_category", "")
    prompt = st.session_state.get("user_prompt", "")
    copy = generate_poster_copy(prompt, cat, cust)

    st.session_state.poster_title = copy.headline
    st.session_state.poster_slogan = copy.slogan
    st.session_state.poster_body = copy.body
    st.session_state.poster_tips = "\n".join(copy.bullet_points)
    st.session_state.poster_quote = copy.quote
    st.session_state.poster_org = copy.org_name
    st.session_state.poster_layout = get_recommended_layout(cat)


def cb_example_prompt() -> None:
    cat = st.session_state.get("category", "Mental Health")
    st.session_state.user_prompt = get_example_prompt(cat)
    cb_autofill_copy()


def cb_random_prompt() -> None:
    cat = st.session_state.get("category")
    st.session_state.user_prompt = get_random_suggestion(cat if cat in config.CATEGORIES else None)
    cb_autofill_copy()


def cb_quick_prompt(prompt_text: str, category_override: Optional[str] = None, theme_override: Optional[str] = None) -> None:
    st.session_state.user_prompt = prompt_text
    if category_override and category_override in config.CATEGORIES:
        st.session_state.category = category_override
        st.session_state.poster_layout = get_recommended_layout(category_override)
    if theme_override and theme_override in getattr(config, "THEME_PALETTES", {}):
        st.session_state.theme_choice = theme_override
    cb_autofill_copy()


def cb_clear_prompt() -> None:
    st.session_state.user_prompt = ""
    st.session_state.poster_title = ""
    st.session_state.poster_slogan = ""
    st.session_state.poster_body = ""
    st.session_state.poster_tips = ""
    st.session_state.poster_quote = ""


def cb_reset_all() -> None:
    first_cat = list(config.CATEGORIES)[0]
    preset = get_campaign_preset(first_cat)
    st.session_state.category = first_cat
    st.session_state.custom_category = ""
    st.session_state.user_prompt = config.CAMPAIGN_PRESETS[first_cat]["artwork_prompt"]
    st.session_state.poster_title = preset.headline
    st.session_state.poster_slogan = preset.slogan
    st.session_state.poster_body = preset.body
    st.session_state.poster_tips = "\n".join(preset.bullet_points)
    st.session_state.poster_quote = preset.quote
    st.session_state.poster_org = preset.org_name
    st.session_state.theme_choice = "✨ Auto-Detect from Prompt & Campaign"
    st.session_state.poster_layout = get_recommended_layout(first_cat)
    st.session_state.last_results = []
    st.session_state.last_request = None


def cb_regenerate() -> None:
    if st.session_state.last_request:
        req = dict(st.session_state.last_request)
        req["seed"] = None
        st.session_state.pending_request = req


def cb_clear_preview() -> None:
    st.session_state.last_results = []


def cb_delete_item(item_id: str) -> None:
    st.session_state.gallery = [g for g in st.session_state.gallery if g["id"] != item_id]
    st.session_state.last_results = [g for g in st.session_state.last_results if g["id"] != item_id]


def cb_clear_gallery() -> None:
    st.session_state.gallery = []
    st.session_state.last_results = []


# ==================================================================
# Model helpers
# ==================================================================
@st.cache_resource(show_spinner=False)
def cached_device_info():
    if check_dependencies():
        return None
    return get_device_info()


@st.cache_resource(show_spinner=False, max_entries=1)
def load_generator(model_label: str) -> WellnessImageGenerator:
    unload_cuda_memory()
    return WellnessImageGenerator(model_label).load()


def show_image(image, caption: str | None = None) -> None:
    st.image(image, caption=caption)


# ==================================================================
# Sidebar
# ==================================================================
def render_sidebar() -> None:
    with st.sidebar:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.image(LOGO, width=52)
        with c2:
            st.markdown(f"<p class='sb-brand'>{config.APP_NAME}</p>"
                        f"<p class='sb-sub'>Campaign Poster Studio</p>", unsafe_allow_html=True)
        st.write("")

        st.radio("Navigation", PAGES, key="nav", label_visibility="collapsed")
        st.divider()

        st.markdown("<div class='label'>⚡ Active Engine</div>", unsafe_allow_html=True)
        active_mode = st.session_state.get("engine_mode", "🤖 Generative AI Engine (SD-Turbo)")
        is_ai_active = any(k in active_mode for k in ["Generative", "SD-Turbo", "Stable Diffusion"])
        if is_ai_active:
            st.success("🤖 Generative AI Active")
            st.caption("Creates custom neural artwork matching your exact prompt.")
        else:
            st.info("⚡ Fast Draft Engine Active")
            st.caption("Creates instant themed vector artwork in 0.2s.")

        st.divider()

        # Model selection
        if is_ai_active:
            st.markdown("<div class='label'>🤖 AI Model</div>", unsafe_allow_html=True)
            st.selectbox("AI model", list(config.MODELS), key="model_label", label_visibility="collapsed")
            st.caption(config.MODELS[st.session_state.model_label]["description"])

        # Device status
        info = cached_device_info()
        st.markdown("<div class='label'>⚙️ Compute</div>", unsafe_allow_html=True)
        if info is None:
            st.info("CPU Mode active · Instant Graphic Engine recommended.")
        elif info.device == "cuda":
            st.success(f"GPU ready: {info.name} ({info.vram_gb} GB)")
        elif info.device == "mps":
            st.success(f"GPU ready: {info.name}")
        else:
            st.info("Compute: CPU · The quality model is slower here; SD-Turbo is for drafts, not final portraits.")

        st.divider()
        st.metric("Posters Created", len(st.session_state.gallery))
        st.markdown(f"<div class='disclaimer'>⚠️ {config.DISCLAIMER_SHORT}</div>", unsafe_allow_html=True)
        st.caption(f"{config.APP_TEAM} · Generative AI Healthcare Project")


# ==================================================================
# Home Page
# ==================================================================
def render_home() -> None:
    st.markdown(
        f"""
        <div class="hero">
            <span class="badge">🩺 Healthcare Graphic Design</span>
            <span class="badge">🎨 4 Professional Poster Layouts</span>
            <span class="badge">⚡ Instant Engine + SD AI</span>
            <h1>{config.APP_NAME}</h1>
            <h3>Professional Patient Wellness Campaign Visual Generator</h3>
            <p>Create polished, high-resolution healthcare campaign posters matching industry design standards.
            Includes clean vector backgrounds, authentic typography, actionable health tips, and official badges.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    b1, b2, _ = st.columns([1.3, 1, 3])
    b1.button("✨ Create Campaign Poster", type="primary", **STRETCH, on_click=go_to, args=(PAGES[1],))
    b2.button("🖼️ Open Gallery", **STRETCH, on_click=go_to, args=(PAGES[2],))

    st.markdown("<div class='section-title'>4 Reference-Grade Poster Layouts</div>", unsafe_allow_html=True)
    layouts_info = [
        ("📰", "Split Editorial (Ref 3)", "Arched slogan, circular artwork halo, rich dark card with heart bullet health tips, gold quote, and contact info."),
        ("☀️", "Radiant Sunburst (Ref 1)", "High-impact sunburst ray backdrop, soft clouds, white halo centerpiece, bold all-caps headline banner, and educational copy."),
        ("🌍", "World Health Day (Ref 2)", "Clean white card with script title accent, partner header, central illustrated wellness circle, and action tips."),
        ("📐", "Minimalist Geometry (Ref 4)", "Warm pastel canvas, split bold headline ('SAFE BLOOD' / 'SAVES LIVES'), geometric accent line framing, and partner badges."),
    ]
    cols = st.columns(4)
    for col, (icon, title, text) in zip(cols, layouts_info):
        col.markdown(f"<div class='card'><div class='icon'>{icon}</div><h4>{title}</h4><p>{text}</p></div>",
                     unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Key Capabilities</div>", unsafe_allow_html=True)
    features = [
        ("🎯", "10 Healthcare Categories", "Mental Health, Heart Health, Blood Donation, World Health Day, Diabetes, Nutrition, and more."),
        ("✍️", "Smart Copywriter", "Auto-generates relevant headlines, slogans, health tips, and inspirational quotes."),
        ("🎨", "Clean Vector Art", "Eliminates messy backgrounds with isolated centerpiece artwork on white backgrounds."),
        ("🛡️", "Safety & Compliance", "Blocks non-clinical and claim terms; includes required review disclaimers."),
    ]
    cols2 = st.columns(4)
    for col, (icon, title, text) in zip(cols2, features):
        col.markdown(f"<div class='card'><div class='icon'>{icon}</div><h4>{title}</h4><p>{text}</p></div>",
                     unsafe_allow_html=True)


# ==================================================================
# Create Campaign Page
# ==================================================================
def _category_label(name: str) -> str:
    if name == config.CUSTOM_CATEGORY:
        return config.CUSTOM_CATEGORY
    return f"{config.CATEGORIES[name]['icon']} {name}"


def _style_label(name: str) -> str:
    return f"{config.STYLES[name]['icon']} {name}"


def _layout_label(name: str) -> str:
    item = config.POSTER_LAYOUTS[name]
    return f"{item['icon']} {item['name']}"


def render_create() -> None:
    st.markdown("## ✨ Healthcare Campaign Poster Studio")
    st.markdown("<p class='muted'>Design publication-grade patient wellness posters with Pretrained Generative AI models and tailored, spellchecked healthcare typography.</p>",
                unsafe_allow_html=True)

    left, right = st.columns([5, 6], gap="large")

    # ---------------- LEFT: inputs ----------------
    with left:
        with st.container(border=True):
            st.markdown("<div class='label'>1 · Campaign Theme & Health Camp</div>", unsafe_allow_html=True)
            camp_options = list(config.CATEGORIES) + [config.CUSTOM_CATEGORY]
            st.selectbox("Select Health Camp / Theme", camp_options, key="category",
                         on_change=cb_category_change,
                         format_func=_category_label, label_visibility="collapsed")

            st.text_input(
                "Camp Title / Topic (or type ANY custom health camp)",
                key="custom_category",
                placeholder="e.g. Free Eye Screening & Cataract Camp, Dengue Prevention Drive...",
                help="Type ANY custom camp name or health topic here."
            )

            st.markdown("<div class='label'>2 · Generative AI Engine & Prompt</div>", unsafe_allow_html=True)
            engine_choices = [
                "🤖 Generative Diffusion AI (Pretrained Neural Model)",
                "⚡ Fast Layout Preview (Instant Synthesizer)",
            ]
            st.radio("Generation Mode", engine_choices, key="engine_mode", horizontal=True)
            is_ai = "Generative" in st.session_state.engine_mode
            if is_ai:
                st.caption("✨ Choose Stable Diffusion v1.5 in the sidebar for final posters; SD-Turbo is a quick draft model. Review generated faces and hands before publishing.")
            else:
                st.caption("⚡ **Fast Layout Preview Active**: Generates instantaneous graphic layout previews in 0.2s.")

            st.text_area(
                "Artwork Description", key="user_prompt", height=85, label_visibility="collapsed",
                max_chars=config.MAX_PROMPT_CHARS,
                placeholder="Describe your scene (e.g. A smiling healthy woman holding a fresh wooden bowl of ripe fruits and green vegetables, bright natural sunlight, high resolution photography).",
                help="Describe the main subject first. For clearer faces, use 1–3 people, a medium/waist-up view, and avoid complex hand/object interactions.",
            )

            st.caption("💡 **Quick Inspirations (click to load prompt, palette & copy):**")
            qi1, qi2, qi3 = st.columns(3)
            qi1.button("🥑 Woman & Fresh Fruits", on_click=cb_quick_prompt,
                       args=("A healthy smiling woman in a sunlit kitchen holding a wooden bowl of ripe fruits and green vegetables, high resolution photography", "Healthy Eating", "💚 Fresh Botanical Green & Lime"),
                       **STRETCH)
            qi2.button("👁️ Free Eye Checkup", on_click=cb_quick_prompt,
                       args=("An optometrist examining a patient's eye with modern medical equipment in an eye clinic, crisp professional lighting", "Free Eye Checkup & Vision Camp", "💙 Royal Health Blue & Teal"),
                       **STRETCH)
            qi3.button("🦷 Dental Hygiene Camp", on_click=cb_quick_prompt,
                       args=("A friendly dentist beside an adult patient with a healthy smile in a bright dental clinic, waist-up composition, hands out of frame", "Dental Hygiene & Oral Health Camp", "💙 Royal Health Blue & Teal"),
                       **STRETCH)

            qi4, qi5, qi6 = st.columns(3)
            qi4.button("🩺 Healthcare Heroes", on_click=cb_quick_prompt,
                       args=("Two friendly healthcare professionals in blue scrubs standing side by side in a bright clinic, waist-up portrait, natural smiles, hands out of frame", "General Wellness", "💙 Royal Health Blue & Teal"),
                       **STRETCH)
            qi5.button("👶 Pediatric Vaccination", on_click=cb_quick_prompt,
                       args=("A friendly pediatrician smiling beside a happy child and parent in a bright pediatric clinic, clear faces, simple waist-up composition", "Pediatric Care & Vaccination Camp", "🧡 Athletic Sunrise Orange & Cyan"),
                       **STRETCH)
            qi6.button("💜 Cancer Hope Ribbon", on_click=cb_quick_prompt,
                       args=("Elegant purple awareness ribbon intertwined with blooming botanical orchids, golden hope aura", "Cancer Awareness", "💜 Awareness Purple & Golden Hope"),
                       **STRETCH)

            p1, p2, p3, p4 = st.columns(4)
            p1.button("💡 Preset", on_click=cb_example_prompt, **STRETCH)
            p2.button("🎲 Random", on_click=cb_random_prompt, **STRETCH)
            p3.button("✨ Auto-Copy", on_click=cb_autofill_copy, **STRETCH, help="Auto-fills all copy fields based on prompt & theme")
            p4.button("🧹 Clear", on_click=cb_clear_prompt, **STRETCH)

            st.markdown("<div class='label'>3 · Visual Artwork Style</div>", unsafe_allow_html=True)
            st.radio("Artwork Style", list(config.STYLES), key="style", format_func=_style_label,
                     horizontal=True, label_visibility="collapsed")

            st.markdown("<div class='label'>4 · Poster Design Layout</div>", unsafe_allow_html=True)
            st.selectbox("Poster Layout", list(config.POSTER_LAYOUTS), key="poster_layout",
                         format_func=_layout_label, label_visibility="collapsed")
            st.caption(config.POSTER_LAYOUTS[st.session_state.poster_layout]["description"])

            st.markdown("<div class='label'>5 · Color Customization</div>", unsafe_allow_html=True)
            color_mode = st.radio("Color Mode", ["✨ Dynamic Auto Theme", "🎨 Custom Color Pickers", "🎯 Curated Theme Palettes"],
                                  horizontal=True, label_visibility="collapsed")
            custom_pal = None
            if color_mode == "🎨 Custom Color Pickers":
                c_col1, c_col2 = st.columns(2)
                p_accent = c_col1.color_picker("Accent Highlight Color", value="#0D9488")
                p_dark = c_col2.color_picker("Card Background Tone", value="#0F172A")
                custom_pal = {
                    "primary": p_accent,
                    "accent": p_accent,
                    "accent2": "#F59E0B",
                    "bg_light": "#F8FAFC",
                    "bg_dark": p_dark,
                    "text_dark": p_dark,
                    "text_light": "#FFFFFF",
                    "badge_bg": p_accent,
                }
            elif color_mode == "🎯 Curated Theme Palettes":
                st.selectbox("Curated Palette", list(config.THEME_PALETTES), key="theme_choice", label_visibility="collapsed")

            st.markdown("<div class='label'>6 · Poster Headline & Slogan</div>", unsafe_allow_html=True)
            st.text_input("Poster Headline", key="poster_title", max_chars=60,
                          placeholder="e.g. CLEAR VISION FOR LIFE or HEALTHY SMILES, HEALTHY LIFE")
            st.text_input("Slogan / Sub-headline", key="poster_slogan", max_chars=80,
                          placeholder="e.g. Protect Your Eyesight, Brighten Your World")

            st.markdown("<div class='label'>7 · Educational Message & Actionable Health Tips</div>", unsafe_allow_html=True)
            st.text_area("Campaign Educational Message", key="poster_body", height=75, max_chars=220,
                         placeholder="Short, encouraging awareness message for the community.")
            st.text_area("Health Tips (one per line, styled with campaign bullet markers)", key="poster_tips", height=90,
                         placeholder="Point 1\nPoint 2\nPoint 3\nPoint 4")

            c_q1, c_q2 = st.columns(2)
            with c_q1:
                st.text_input("Inspirational Quote", key="poster_quote", max_chars=110,
                              placeholder="e.g. Small consistent daily habits build lifelong health.")
            with c_q2:
                st.text_input("Partner / Org Name", key="poster_org", max_chars=60,
                              placeholder="e.g. Health & Care Partnership")

        with st.expander("⚙️ Advanced Generation Settings", expanded=False):
            res_label = st.selectbox("Artwork Resolution", list(config.RESOLUTIONS), index=0)
            width, height = config.RESOLUTIONS[res_label]
            variations = st.slider("Variations", 1, config.MAX_VARIATIONS, 1)
            steps = config.MODELS[st.session_state.model_label]["default_steps"]
            if is_ai:
                model_cfg = config.MODELS[st.session_state.model_label]
                min_steps = 1 if model_cfg["max_steps"] <= 4 else 10
                steps = st.slider(
                    "Diffusion Steps",
                    min_steps,
                    model_cfg["max_steps"],
                    model_cfg["default_steps"],
                    key=f"steps_{st.session_state.model_label}",
                    help="More steps generally improve detail but take longer. SD-Turbo is intended for quick drafts.",
                )
            fixed_seed = st.toggle("Fixed Seed", value=False)
            seed = int(st.number_input("Seed Value", 0, 2**31 - 1, 42)) if fixed_seed else None
            add_footer = st.toggle("Add Review Disclaimer Bar", value=True)
            save_disk = st.toggle("Save PNGs to generated_images folder", value=True)

        g1, g2 = st.columns([3, 1])
        generate_clicked = g1.button("🚀 Generate Campaign Poster", type="primary", **STRETCH)
        g2.button("↺ Reset", on_click=cb_reset_all, **STRETCH)

        if generate_clicked:
            st.session_state.first_visit = False
            effective_category = st.session_state.custom_category.strip() if st.session_state.custom_category.strip() else st.session_state.category
            result = validate_user_input(
                st.session_state.user_prompt,
                effective_category,
                poster_text=f"{st.session_state.poster_title} {st.session_state.poster_body}",
            )
            for err in result.errors:
                st.error(err)
            for warn in result.warnings:
                st.warning(warn)

            if result.ok:
                st.session_state.pending_request = {
                    "user_prompt": st.session_state.user_prompt,
                    "category": effective_category,
                    "custom_category": st.session_state.custom_category,
                    "poster_layout": st.session_state.poster_layout,
                    "theme_choice": st.session_state.get("theme_choice", "✨ Auto-Detect from Prompt & Campaign"),
                    "custom_palette": custom_pal,
                    "poster_title": st.session_state.poster_title,
                    "poster_slogan": st.session_state.poster_slogan,
                    "poster_body": st.session_state.poster_body,
                    "poster_tips": st.session_state.poster_tips,
                    "poster_quote": st.session_state.poster_quote,
                    "poster_org": st.session_state.poster_org,
                    "style": st.session_state.style,
                    "engine_mode": st.session_state.engine_mode,
                    "model_label": st.session_state.model_label,
                    "width": width, "height": height,
                    "steps": steps,
                    "variations": variations, "seed": seed,
                    "add_footer": add_footer, "save_disk": save_disk,
                }

    # ---------------- RIGHT: generation + preview ----------------
    with right:
        if st.session_state.pending_request:
            request = st.session_state.pending_request
            st.session_state.pending_request = None
            run_generation(request)
        render_preview()


def run_generation(request: dict) -> None:
    bundle = build_prompt(
        request["user_prompt"], request["category"], request["style"],
        request.get("custom_category", ""),
    )

    # Prepare structured poster copy
    bullet_list = [line.strip("-•* ").strip() for line in request.get("poster_tips", "").splitlines() if line.strip()]
    if not bullet_list:
        preset = get_campaign_preset(bundle.category)
        bullet_list = preset.bullet_points

    copy = PosterCopy(
        headline=request.get("poster_title", "").strip() or bundle.category.upper(),
        slogan=request.get("poster_slogan", "").strip(),
        body=request.get("poster_body", "").strip(),
        bullet_points=bullet_list,
        quote=request.get("poster_quote", "").strip(),
        org_name=request.get("poster_org", "").strip() or f"{bundle.category} Health Partnership",
        helpline=get_campaign_preset(bundle.category).helpline,
    )

    use_instant = "Instant" in request.get("engine_mode", "") or "Fast Draft" in request.get("engine_mode", "")
    n = request["variations"]

    with st.container(border=True):
        st.markdown("#### ⏳ Creating your Campaign Poster…")
        generator = None
        if not use_instant:
            try:
                with st.spinner("Initializing Pretrained Generative AI Model…"):
                    generator = load_generator(request["model_label"])
            except GenerationError as exc:
                st.error(f"Generative AI loading error: {exc}")
                return

        bar = st.progress(0.0, text="Synthesizing pixels & generating artwork…")

        def on_progress(i: int, step: int, total: int) -> None:
            done = (i + step / total) / n
            bar.progress(min(done, 1.0), text=f"Poster {i + 1} of {n} · diffusion step {step}/{total}")

        try:
            with st.spinner("Rendering poster elements and high-res typography…"):
                if use_instant:
                    # Instant Graphic Engine
                    generator = WellnessImageGenerator()
                    outputs = generator.generate(
                        prompt=bundle.positive, negative_prompt=bundle.negative,
                        width=request["width"], height=request["height"],
                        num_images=n, seed=request["seed"], category=bundle.category,
                        use_instant_engine=True,
                        theme_choice=request.get("theme_choice"),
                    )
                else:
                    outputs = generator.generate(
                        prompt=bundle.positive, negative_prompt=bundle.negative,
                        width=request["width"], height=request["height"],
                        num_images=n, seed=request["seed"], category=bundle.category,
                        steps=request.get("steps", 2),
                        progress_callback=on_progress,
                        theme_choice=request.get("theme_choice"),
                    )
        except Exception as exc:
            bar.empty()
            st.error(f"Generation error: {exc}")
            return

        bar.empty()

    # --- Composite into reference poster layout ---
    items = []
    for out in outputs:
        poster_img = image_utils.create_campaign_poster(
            out.image, copy, category=bundle.category,
            layout_name=request["poster_layout"],
            user_prompt=request.get("user_prompt", ""),
            theme_choice=request.get("theme_choice"),
            custom_palette=request.get("custom_palette"),
        )
        if request["add_footer"]:
            poster_img = image_utils.add_disclaimer_footer(poster_img)

        filename = image_utils.make_filename(bundle.category, out.seed)
        saved = image_utils.save_image(poster_img, filename) if request["save_disk"] else None

        items.append({
            "id": uuid.uuid4().hex,
            "png_bytes": image_utils.pil_to_png_bytes(poster_img),
            "filename": filename,
            "saved_path": str(saved) if saved else None,
            "category": bundle.category,
            "layout": request["poster_layout"],
            "style": bundle.style,
            "user_prompt": bundle.user_text,
            "poster_title": copy.headline,
            "poster_slogan": copy.slogan,
            "poster_body": copy.body,
            "final_prompt": bundle.positive,
            "negative_prompt": bundle.negative,
            "readable": bundle.readable,
            "seed": out.seed,
            "seconds": out.seconds,
            "size": f"{poster_img.width}×{poster_img.height}",
            "engine": "⚡ Fast Draft Engine" if use_instant else f"🤖 Generative AI ({request['model_label'].split()[0]})",
            "created": datetime.now().strftime("%d %b %Y, %H:%M:%S"),
        })

    st.session_state.last_results = items
    st.session_state.last_request = request
    st.session_state.gallery = items + st.session_state.gallery
    st.toast(f"✅ {len(items)} campaign poster(s) created!", icon="🎉")


def render_preview() -> None:
    results = st.session_state.last_results
    if not results:
        st.markdown(
            "<div class='empty'><div class='big'>🖼️</div>"
            "<h4>Your finished poster will appear here</h4>"
            "<p>Select your theme & layout on the left, then click <b>Generate Campaign Poster</b>.</p></div>",
            unsafe_allow_html=True,
        )
        return

    first = results[0]
    with st.container(border=True):
        st.markdown("#### 🎉 Generated Campaign Poster")
        st.markdown(f"<span class='chip'>🏷️ {first['category']}</span>"
                    f"<span class='chip'>📐 {first.get('layout', 'Editorial')}</span>"
                    f"<span class='chip'>⚡ {first.get('engine', 'Engine')}</span>"
                    f"<span class='chip'>📏 {first['size']} px</span>", unsafe_allow_html=True)

        if len(results) == 1:
            show_image(first["png_bytes"], caption=f"{first['poster_title']} · {first['seconds']}s")
            st.download_button("⬇️ Download High-Res Poster (PNG)", data=first["png_bytes"],
                               file_name=first["filename"], mime="image/png",
                               key=f"dl_prev_{first['id']}", type="primary", **STRETCH)
        else:
            grid = st.columns(len(results))
            for idx, item in enumerate(results):
                with grid[idx]:
                    show_image(item["png_bytes"], caption=f"Variation {idx + 1}")
                    st.download_button("⬇️ Download PNG", data=item["png_bytes"],
                                       file_name=item["filename"], mime="image/png",
                                       key=f"dl_prev_{item['id']}", **STRETCH)

        st.markdown(f"**Headline:** {first.get('poster_title')}")
        if first.get("poster_slogan"):
            st.markdown(f"**Slogan:** {first['poster_slogan']}")
        if first.get("poster_body"):
            st.markdown(f"**Body Copy:** {first['poster_body']}")

        with st.expander("🔍 Engineered Prompt Details"):
            st.markdown(f"**Summary:** {first['readable']}")
            st.markdown("**Positive Prompt:**")
            st.code(first["final_prompt"], language=None)
            st.markdown("**Negative Prompt:**")
            st.code(first["negative_prompt"], language=None)

        r1, r2 = st.columns(2)
        r1.button("🔄 Regenerate", on_click=cb_regenerate, **STRETCH)
        r2.button("🧹 Clear Preview", on_click=cb_clear_preview, **STRETCH)

    st.markdown(f"<div class='disclaimer'>⚠️ {config.DISCLAIMER_FULL.replace('**', '')}</div>",
                unsafe_allow_html=True)


# ==================================================================
# Gallery Page
# ==================================================================
def render_gallery() -> None:
    gallery = st.session_state.gallery
    st.markdown("## 🖼️ Session Gallery")
    st.markdown("<p class='muted'>All posters created in this session. Download individually or export all as a ZIP.</p>",
                unsafe_allow_html=True)

    if not gallery:
        st.markdown("<div class='empty'><div class='big'>📭</div><h4>No posters created yet</h4>"
                    "<p>Generate your first poster to collect them here.</p></div>",
                    unsafe_allow_html=True)
        st.write("")
        st.button("✨ Create your first poster", type="primary", on_click=go_to, args=(PAGES[1],))
        return

    t1, t2, t3 = st.columns([3, 1.3, 1])
    categories = sorted({g["category"] for g in gallery})
    selected = t1.multiselect("Filter by category", categories, placeholder="All categories")
    t2.download_button("📦 Download All (ZIP)", data=image_utils.make_zip(gallery),
                       file_name="wellaware_posters.zip", mime="application/zip",
                       **STRETCH)
    t3.button("🗑️ Clear Gallery", on_click=cb_clear_gallery, **STRETCH)

    items = [g for g in gallery if not selected or g["category"] in selected]
    st.caption(f"Showing {len(items)} of {len(gallery)} poster(s)")

    cols_per_row = 3
    for row_start in range(0, len(items), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, item in zip(cols, items[row_start:row_start + cols_per_row]):
            with col, st.container(border=True):
                show_image(item["png_bytes"])
                st.markdown(f"<span class='chip'>🏷️ {item['category']}</span>"
                            f"<span class='chip'>📐 {item.get('layout', 'Editorial')}</span>", unsafe_allow_html=True)
                st.markdown(f"**{item.get('poster_title', 'Poster')}**")
                d1, d2 = st.columns([3, 1])
                d1.download_button("⬇️ PNG", data=item["png_bytes"], file_name=item["filename"],
                                   mime="image/png", key=f"dl_gal_{item['id']}", **STRETCH)
                d2.button("🗑️", key=f"del_{item['id']}", on_click=cb_delete_item, args=(item["id"],),
                          help="Remove", **STRETCH)


# ==================================================================
# Guidelines & Help Page
# ==================================================================
def render_help() -> None:
    st.markdown("## 🛡️ Guidelines & Reference Styles")
    st.markdown(f"<div class='disclaimer'>⚠️ {config.DISCLAIMER_FULL.replace('**', '')}</div>",
                unsafe_allow_html=True)
    st.write("")

    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("#### ✅ Supported Features")
        st.markdown("- **4 Reference Poster Styles** (Editorial Split, Sunburst, World Health Day, Minimalist Geometry)\n"
                    "- **Relevant Copywriting** (auto-suggests headlines, slogans, health tips, and quotes)\n"
                    "- **Clean Vector Art** with isolated subjects on clean backgrounds\n"
                    "- **Instant Graphic Engine** for immediate real-time results")
    with c2, st.container(border=True):
        st.markdown("#### 🚫 Content Restrictions")
        st.markdown("- No diagnostic scans (X-rays, MRIs, biopsies)\n"
                    "- No pharma brand logos or commercial endorsements\n"
                    "- No medical claim guarantees (\"cures\", \"guaranteed 100%\")\n"
                    "- Non-clinical awareness visuals only")

    st.markdown("<div class='section-title'>Poster Design Tips</div>", unsafe_allow_html=True)
    st.markdown(
        "- Click **✨ Auto-Copy** in the Create form to instantly fill all text fields with tailored healthcare content.\n"
        "- Choose **Instant Graphic Engine** for immediate high-resolution vector posters without model download delays.\n"
        "- Switch between the 4 layout styles to match your campaign medium (social media, clinic flyers, or print banners)."
    )


# ==================================================================
# Main
# ==================================================================
def main() -> None:
    inject_css()
    init_state()
    render_sidebar()

    page = st.session_state.nav
    if page == PAGES[0]:
        render_home()
    elif page == PAGES[1]:
        render_create()
    elif page == PAGES[2]:
        render_gallery()
    else:
        render_help()

    st.markdown(f"<div class='footer'>{config.APP_NAME} · {config.APP_SUBTITLE} · "
                f"{config.APP_TEAM} · Non-clinical illustrative posters.</div>",
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
