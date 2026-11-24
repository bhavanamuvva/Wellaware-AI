"""
modules/prompt_processor.py
---------------------------
Prompt engineering + content safety + poster copy generation for WellAware AI.

Responsibilities:
1. Validate user inputs (blocked terms, claim terms).
2. Clean and engineer AI prompts for clean, isolated vector artwork with no messy backgrounds.
3. Generate relevant, professional healthcare poster copy (Headline, Slogan, Body, Bullet Tips, Quote, Org).
4. Provide category presets and prompt suggestions matching reference posters.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import config


# ------------------------------------------------------------------
# Data containers
# ------------------------------------------------------------------
@dataclass
class ValidationResult:
    """Outcome of validating user input."""
    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class PromptBundle:
    """Everything the image generator needs, plus human-readable summary."""
    positive: str
    negative: str
    category: str
    style: str
    user_text: str
    readable: str


@dataclass
class PosterCopy:
    """Structured, professional content for healthcare campaign posters."""
    headline: str
    slogan: str
    body: str
    bullet_points: List[str]
    quote: str
    org_name: str
    helpline: str


# ------------------------------------------------------------------
# Campaign copy generation & presets
# ------------------------------------------------------------------
def get_campaign_preset(category: str, custom_category: str = "") -> PosterCopy:
    """Return default professional poster copy matching the selected category."""
    cat_key = custom_category.strip() if category == config.CUSTOM_CATEGORY and custom_category.strip() else category
    preset = config.CAMPAIGN_PRESETS.get(cat_key)
    
    if not preset:
        # Fallback for custom or unknown category
        title = cat_key.upper() if cat_key else "HEALTH & WELLNESS"
        preset = {
            "headline": title,
            "slogan": "Empowering Healthy Living, Mind, and Body",
            "body": f"Proactive health awareness is the foundation of a vibrant, thriving community. Take small, mindful steps every day toward lasting wellness and preventative care.",
            "bullet_points": [
                "Prioritize balanced nutrition and daily hydration",
                "Stay active with 30 minutes of daily physical exercise",
                "Care for mental well-being and get restful sleep",
                "Support and encourage your family and community",
            ],
            "quote": "Wellness is not a destination, but a continuous journey of positive daily choices.",
            "org_name": f"{cat_key.title() if cat_key else 'Community'} Health Partnership",
            "helpline": "WellAware Helpline: 1-800-WELLNESS · Visit: www.wellaware.org",
            "artwork_prompt": f"clean modern flat vector illustration representing {cat_key.lower() or 'wellness'}, isolated on white background, no text",
        }

    return PosterCopy(
        headline=preset["headline"],
        slogan=preset["slogan"],
        body=preset["body"],
        bullet_points=list(preset["bullet_points"]),
        quote=preset["quote"],
        org_name=preset["org_name"],
        helpline=preset["helpline"],
    )


HUMAN_KEYWORDS = [
    "woman", "women", "lady", "girl", "female",
    "man", "men", "guy", "boy", "male",
    "person", "people", "human", "face", "portrait",
    "doctor", "nurse", "physician", "optometrist", "dentist", "surgeon",
    "patient", "child", "children", "baby", "infant", "kid", "kids",
    "senior", "elder", "elderly", "grandparent", "mother", "father"
]


def generate_poster_copy(prompt: str, category: str, custom_category: str = "") -> PosterCopy:
    """
    Intelligently generate relevant poster copy based on both the user's prompt
    and the campaign category with 100% accurate spelling and actionable advice.
    """
    base = get_campaign_preset(category, custom_category)
    combined = f"{prompt or ''} {category or ''} {custom_category or ''}".lower()
    cleaned = combined

    # Specialized health campaign topics:
    if any(k in combined for k in ["eye", "vision", "optometr", "sight", "cataract", "glaucoma", "blind"]):
        return PosterCopy(
            headline="CLEAR VISION FOR LIFE",
            slogan="Protect Your Eyesight, Brighten Your World",
            body="Sight is our most precious window to the world. Regular eye screenings detect early vision changes, protect against digital strain, and ensure clear sight for life.",
            bullet_points=[
                "Follow the 20-20-20 rule: rest eyes every 20 minutes from screens",
                "Wear UV-protective sunglasses in bright sunlight",
                "Ensure comfortable lighting when reading or working",
                "Schedule annual comprehensive eye examinations",
            ],
            quote="The eyes are the windows to the soul and the guide to a vibrant life.",
            org_name=f"{custom_category or category or 'Community'} Vision Initiative",
            helpline="Eye Care Helpline: 1-800-EYE-CARE · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["dental", "tooth", "teeth", "oral", "gum", "dentist"]):
        return PosterCopy(
            headline="HEALTHY SMILES, HEALTHY LIFE",
            slogan="Brushing Away Disease, Smiling with Confidence",
            body="Oral wellness is directly connected to overall systemic health. Protecting your teeth and gums prevents infections and keeps your natural smile bright and strong.",
            bullet_points=[
                "Brush thoroughly twice daily with fluoride toothpaste",
                "Floss daily to remove plaque between tight teeth",
                "Limit sugary beverages, candy, and sticky snacks",
                "Visit your dental professional every six months",
            ],
            quote="A genuine smile is the shortest distance between two people.",
            org_name=f"{custom_category or category or 'Community'} Dental Alliance",
            helpline="Dental Helpline: 1-800-SMILE-DOC · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["dengue", "malaria", "mosquito", "vector", "chikungunya"]):
        return PosterCopy(
            headline="PREVENT MOSQUITO ILLNESS",
            slogan="Clean Surroundings, Safe and Healthy Communities",
            body="Vector-borne diseases are preventable through proactive community hygiene. Eliminate standing water, protect your living spaces, and stay alert to early fever symptoms.",
            bullet_points=[
                "Empty and scrub water containers, flower pots, and coolers weekly",
                "Install fine mesh window screens and sleep under bed nets",
                "Apply protective insect repellent when outdoors at dawn and dusk",
                "Seek prompt medical testing at the first onset of high fever",
            ],
            quote="A clean community is the first and strongest barrier against disease.",
            org_name=f"{custom_category or category or 'Public Health'} Taskforce",
            helpline="Vector Control Hotline: 1-800-MOSQUITO · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["fruit", "vegetable", "woman", "salad", "nutrition", "diet", "food", "eat"]):
        return PosterCopy(
            headline="FRESH NOURISHMENT, VIBRANT LIFE",
            slogan="Nourish Your Body from the Inside Out",
            body="Wholesome food is the foundation of energy, immunity, and lifelong wellness. Transform your daily meals with colorful whole fruits, crisp vegetables, and natural hydration.",
            bullet_points=[
                "Fill half your plate with colorful fruits and crisp vegetables",
                "Drink at least 8 glasses of pure fresh water daily",
                "Choose whole, unprocessed foods cooked with natural ingredients",
                "Listen to your natural hunger cues and practice mindful eating",
            ],
            quote="Let your food be your daily medicine and your kitchen be your source of health.",
            org_name=f"{custom_category or category or 'Community'} Nutrition Initiative",
            helpline="Nutrition Helpline: 1-800-EAT-WELL · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["pediatric", "vaccin", "immuniz", "baby", "infant", "child", "children"]):
        return PosterCopy(
            headline="NURTURING CHILD WELLNESS",
            slogan="Healthy Steps for Little Champions",
            body="Every child deserves a strong foundation for lifelong vitality. Wholesome nutrition, active play, timely vaccinations, and loving care shape a bright future.",
            bullet_points=[
                "Ensure age-appropriate immunizations and routine checkups",
                "Provide balanced home meals rich in whole fruits and vegetables",
                "Encourage at least 60 minutes of joyful active play every day",
                "Foster emotional security and screen-free family connection",
            ],
            quote="Children are our greatest treasure and the future of our communities.",
            org_name=f"{custom_category or category or 'Community'} Pediatric Coalition",
            helpline="Child Wellness Line: 1-800-KID-CARE · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["elder", "senior", "grandparent", "aging", "stroke", "mobility", "orthoped", "joint"]):
        return PosterCopy(
            headline="ACTIVE & HEALTHY AGING",
            slogan="Vitality, Wisdom, and Grace at Every Stage of Life",
            body="Aging with vitality begins with daily movement, sharp minds, and strong social bonds. Take proactive care of bone strength, cardiovascular wellness, and joint flexibility.",
            bullet_points=[
                "Engage in daily gentle walking, stretching, or swimming",
                "Stay connected with community, friends, and family",
                "Nourish bone and brain vitality with wholesome foods",
                "Monitor blood pressure and medication schedules regularly",
            ],
            quote="Age is an honor and a testament to a life lived with purpose and care.",
            org_name=f"{custom_category or category or 'Senior'} Health Partnership",
            helpline="Senior Care Line: 1-800-SENIOR-CARE · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["doctor", "nurse", "hospital", "clinic", "scrub", "surgeon"]):
        return PosterCopy(
            headline="HEALTHCARE HEROES IN ACTION",
            slogan="Compassionate Care, Dedicated to Every Patient",
            body=f"Celebrating the dedicated healthcare professionals who protect our well-being every day. {base.body}",
            bullet_points=[
                "Support and appreciate your local healthcare workers",
                "Schedule regular health check-ups and preventative screenings",
                "Communicate openly with your doctors and nurses",
                "Prioritize care and wellness for your entire family",
            ],
            quote="Dedicated hands and caring hearts build the foundation of community wellness.",
            org_name=f"{custom_category or category or 'Community'} Health Partnership",
            helpline=base.helpline,
        )
    elif any(k in combined for k in ["skin", "derma", "sunscreen", "uv"]):
        return PosterCopy(
            headline="RADIANT SKIN, HEALTHY LIVING",
            slogan="Protect Your Skin, Embrace Your Natural Glow",
            body="Skin is your body's first line of defense against the elements. Daily hydration, sun protection, and mindful skincare preserve health, resilience, and vitality.",
            bullet_points=[
                "Apply broad-spectrum sunscreen daily before sun exposure",
                "Stay hydrated by drinking at least 8 glasses of water",
                "Cleanse gently and moisturize with clean, natural products",
                "Examine skin regularly for unusual mole or lesion changes",
            ],
            quote="Healthy skin is a reflection of overall wellness and mindful daily care.",
            org_name=f"{custom_category or category or 'Dermatology'} Awareness Alliance",
            helpline="Skin Care Hotline: 1-800-SKIN-CARE · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["kidney", "renal", "dialysis"]):
        return PosterCopy(
            headline="PROTECT YOUR KIDNEYS, PROTECT LIFE",
            slogan="Early Detection and Daily Care for Kidney Health",
            body="Kidneys filter waste, regulate blood pressure, and maintain fluid balance. Proactive monitoring of blood sugar and blood pressure keeps kidneys functioning at their best.",
            bullet_points=[
                "Drink adequate water daily to flush metabolic toxins",
                "Monitor and maintain healthy blood pressure and blood sugar",
                "Reduce excessive salt intake and avoid unprescribed pain relievers",
                "Get annual urine and blood screenings for kidney function",
            ],
            quote="Gentle daily habits protect the silent organs that sustain your life.",
            org_name=f"{custom_category or category or 'Kidney'} Health Alliance",
            helpline="Renal Care Helpline: 1-800-KIDNEY · Visit: www.wellaware.org",
        )
    elif any(k in combined for k in ["yoga", "meditat", "peace", "calm", "relax", "mindfulness"]):
        return PosterCopy(
            headline="MINDFUL LIVING & INNER PEACE",
            slogan="Breathe Deeply, Move Mindfully, Live Fully",
            body=f"Harmony between body and mind is the essence of true vitality. Take mindful moments each day to reset, reflect, and restore your calm. {base.body}",
            bullet_points=[
                "Practice 15 minutes of mindful breathing or meditation daily",
                "Engage in restorative stretching or mindful yoga flow",
                "Unplug from digital screens and connect with peaceful nature",
                "Cultivate daily gratitude and gentle self-compassion",
            ],
            quote="Peace of mind is not the absence of storms, but calmness within the soul.",
            org_name=f"{custom_category or category or 'Mindfulness'} Alliance",
            helpline=base.helpline,
        )

    # Built-in campaign presets check
    if category != config.CUSTOM_CATEGORY and category in config.CAMPAIGN_PRESETS and category != "General Wellness":
        return PosterCopy(
            headline=base.headline,
            slogan=base.slogan,
            body=base.body,
            bullet_points=list(base.bullet_points),
            quote=base.quote,
            org_name=base.org_name,
            helpline=base.helpline,
        )

    # Inspect prompt keywords to dynamically find best preset
    if any(k in cleaned for k in ["blood", "donor", "donation"]):
        preset = config.CAMPAIGN_PRESETS["Blood Donation Awareness"]
    elif any(k in cleaned for k in ["cancer", "ribbon", "tumor", "oncolog"]):
        preset = config.CAMPAIGN_PRESETS["Cancer Awareness"]
    elif any(k in cleaned for k in ["diabet", "sugar", "glucose", "insulin"]):
        preset = config.CAMPAIGN_PRESETS["Diabetes Awareness"]
    elif any(k in cleaned for k in ["run", "fitness", "exercise", "workout", "gym", "sport", "athletic", "movement"]):
        preset = config.CAMPAIGN_PRESETS["Physical Fitness"]
    elif any(k in cleaned for k in ["women", "female", "maternal", "breast"]):
        preset = config.CAMPAIGN_PRESETS["Women's Health Awareness"]
    elif any(k in cleaned for k in ["mental", "mind", "brain", "stress", "inside"]):
        preset = config.CAMPAIGN_PRESETS["Mental Health"]
    elif any(k in cleaned for k in ["heart", "lung", "respiratory", "cardio", "pulse"]):
        preset = config.CAMPAIGN_PRESETS["Heart Health"]
    elif any(k in cleaned for k in ["world health", "community"]):
        preset = config.CAMPAIGN_PRESETS["World Health Day"]
    else:
        # Dynamic universal health campaign generator for ANY custom topic
        topic_title = custom_category.strip() or category
        if topic_title in ("General Wellness", config.CUSTOM_CATEGORY, ""):
            # Extract main noun phrase from prompt if possible
            words = [w for w in re.findall(r"[a-zA-Z]+", prompt) if len(w) > 3 and w.lower() not in {"poster", "camp", "with", "make", "draw", "generate", "create", "about"}]
            topic_title = " ".join(words[:3]).title() if words else "Health & Wellness"

        return PosterCopy(
            headline=topic_title.upper(),
            slogan="Empowering Healthy Living, Community, and Prevention",
            body=f"Proactive awareness is the foundation of a vibrant, thriving community. Take small, mindful steps every day toward lasting wellness and preventative care.",
            bullet_points=[
                "Prioritize balanced nutrition and daily hydration",
                "Stay active with 30 minutes of daily physical exercise",
                "Care for mental well-being and get restful sleep",
                "Support and encourage your family and community",
            ],
            quote="Wellness is not a destination, but a continuous journey of positive daily choices.",
            org_name=f"{topic_title.title()} Health Partnership",
            helpline="WellAware Helpline: 1-800-WELLNESS · Visit: www.wellaware.org",
        )

    return PosterCopy(
        headline=preset["headline"],
        slogan=preset["slogan"],
        body=preset["body"],
        bullet_points=list(preset["bullet_points"]),
        quote=preset["quote"],
        org_name=preset["org_name"],
        helpline=preset["helpline"],
    )


# ------------------------------------------------------------------
# Prompt Suggestions
# ------------------------------------------------------------------
def get_example_prompt(category: Optional[str] = None) -> str:
    if category and category in config.CAMPAIGN_PRESETS:
        return config.CAMPAIGN_PRESETS[category]["artwork_prompt"]
    return "Silhouette profile of a human head with a vibrant colorful tree of brain leaves growing inside, promoting mental wellness."


def get_random_suggestion(category: Optional[str] = None) -> str:
    suggestions = {
        "Mental Health": "Silhouette profile of a human head with a vibrant colorful tree of brain leaves growing inside, modern vector art.",
        "Heart Health": "Stylized anatomical lungs and heart vector illustration, clean bold red and deep blue tones on white background.",
        "Blood Donation Awareness": "Modern minimalist geometric blood droplet emblem with vibrant red gradient lines, sleek healthcare logo.",
        "World Health Day": "Diverse people exercising and doing yoga around a clean stylized earth globe, flat modern vector illustration.",
        "Diabetes Awareness": "A colorful balanced bowl of fresh vegetables and whole grains with subtle blue circle health motif.",
        "Healthy Eating": "A vibrant fresh salad bowl overflowing with colorful avocado, tomatoes, greens and citrus, clean vector art.",
        "Physical Fitness": "Energetic silhouettes of diverse people running and stretching outdoors at sunrise, athletic energy.",
        "Women's Health Awareness": "Artistic flat vector illustration of diverse women smiling together with floral botanical accents.",
        "Cancer Awareness": "Elegant awareness ribbon intertwined with hopeful blooming botanical flowers, vibrant soft colors.",
        "General Wellness": "Minimalist clean illustration of a healthy human figure stretching peacefully with green leaves and sunlight rays.",
    }
    if category and category in suggestions:
        return suggestions[category]
    return random.choice(list(suggestions.values()))


# ------------------------------------------------------------------
# Input validation
# ------------------------------------------------------------------
def _find_terms(text: str, terms: List[str]) -> List[str]:
    found = []
    lowered = text.lower()
    for term in terms:
        if re.fullmatch(r"[a-z0-9 &\-]+", term):
            pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
            if re.search(pattern, lowered):
                found.append(term)
        elif term in lowered:
            found.append(term)
    return found


def validate_user_input(text: str, custom_category: str = "",
                        poster_text: str = "") -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []
    cleaned = (text or "").strip()

    if not cleaned:
        errors.append("Please enter a short description of the illustration or poster theme.")
        return ValidationResult(False, errors, warnings)

    if len(cleaned) < config.MIN_PROMPT_CHARS:
        errors.append(f"Description should be at least {config.MIN_PROMPT_CHARS} characters.")

    if len(cleaned) > config.MAX_PROMPT_CHARS:
        errors.append(f"Description is too long ({len(cleaned)} chars). Max is {config.MAX_PROMPT_CHARS}.")

    combined = f"{cleaned} {custom_category or ''} {poster_text or ''}"
    blocked = _find_terms(combined, config.BLOCKED_TERMS)
    if blocked:
        errors.append(
            "WellAware AI only creates non-clinical wellness visuals. "
            f"Please remove: **{', '.join(sorted(set(blocked)))}**."
        )

    claims = _find_terms(combined, config.CLAIM_TERMS)
    if claims:
        warnings.append(
            f"Note: Description contains claim-like terms (**{', '.join(sorted(set(claims)))}**). "
            "Images are illustrative only."
        )

    return ValidationResult(ok=not errors, errors=errors, warnings=warnings)


# ------------------------------------------------------------------
# Prompt building for clean vector artwork on white background
# ------------------------------------------------------------------
def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    # Strip text/word instructions from image prompt since text is rendered separately
    text = re.sub(r"(with|showing|saying)?\s*(the\s+)?(text|caption|slogan|words?)\s*[\"'“][^\"'”]*[\"'”]",
                  "", text, flags=re.IGNORECASE)
    text = re.sub(r"^(please\s+)?(create|generate|make|draw|design)\s+(me\s+)?(an?\s+)?",
                  "", text, flags=re.IGNORECASE)
    return text.strip(" ,.")


def _limit_prompt_words(text: str, limit: int) -> str:
    """Keep the prompt's key phrases near the front of the model's text limit."""
    words = text.split()
    return " ".join(words[:limit])


def build_prompt(user_text: str, category: str, style: str,
                 custom_category: str = "") -> PromptBundle:
    """
    Build concise style-aware prompts for text-free campaign artwork.
    """
    description = _clean_text(user_text)

    if category == config.CUSTOM_CATEGORY:
        cat_name = (custom_category or "General Wellness").strip()
        cat_visuals = "healthy balanced lifestyle, clean iconic composition"
        if not description:
            description = f"clean modern healthcare visual representing {cat_name.lower()}"
    else:
        cat_name = category
        info = config.CATEGORIES.get(category, config.CATEGORIES["General Wellness"])
        cat_visuals = info["visuals"]
        if not description:
            preset = config.CAMPAIGN_PRESETS.get(category, {})
            description = preset.get("artwork_prompt", cat_visuals)

    # Detect if prompt requests human subjects (woman, doctor, child, patient, senior, etc.)
    has_human = any(re.search(r"\b" + re.escape(kw) + r"\b", description.lower()) for kw in HUMAN_KEYWORDS)

    effective_style = style if style in config.STYLES else config.DEFAULT_STYLE
    style_info = config.STYLES.get(effective_style, config.STYLES[config.DEFAULT_STYLE])

    parts = [_limit_prompt_words(description, 32)]
    if cat_visuals and not has_human:
        parts.append(f"{cat_name} subject: {_limit_prompt_words(cat_visuals, 8)}")
    if effective_style == "Photographic & Realistic":
        parts.append("photorealistic editorial portrait, sharp focus, natural skin texture, soft daylight")
    elif style_info.get("prompt"):
        parts.append(_limit_prompt_words(style_info["prompt"], 12))
    if has_human:
        if effective_style == "Photographic & Realistic":
            parts.append(
                "one to three people, medium close-up, clear distinct faces, realistic proportions, "
                "hands out of frame, plain uncluttered background"
            )
        else:
            parts.append("no more than three people, clear separated faces, hands out of frame, simple background")
    parts.append(
            "single scene only, no visible text, signage, labels, logos, or watermark"
    )
    positive = ", ".join(part.strip(" ,.") for part in parts if part.strip(" ,."))

    neg_parts = [config.BASE_NEGATIVE_PROMPT]
    if style_info.get("negative"):
        neg_parts.append(_limit_prompt_words(style_info["negative"], 10))
    if has_human:
        neg_parts.append("poorly drawn face, crossed eyes, fused fingers, malformed hands")
    negative = ", ".join(neg_parts)

    readable = (
        f"A clear {cat_name} visual: {description}. "
        f"Rendered in {effective_style.lower()} style on a clean background, ready for campaign posters."
    )

    return PromptBundle(
        positive=positive,
        negative=negative,
        category=cat_name,
        style=effective_style,
        user_text=user_text.strip(),
        readable=readable,
    )
