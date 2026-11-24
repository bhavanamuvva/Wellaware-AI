"""
config.py
---------
Central configuration for WellAware AI.

Every tunable value (model choices, categories, styles, resolutions,
colours, poster layouts, presets, safety lists) lives here.
"""

from pathlib import Path

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
OUTPUT_DIR = BASE_DIR / "generated_images"

# ------------------------------------------------------------------
# App identity
# ------------------------------------------------------------------
APP_NAME = "WellAware AI"
APP_SUBTITLE = "Patient Wellness Campaign Visual Generator"
APP_TEAM = "Team 17"
APP_ICON = "🩺"

# ------------------------------------------------------------------
# Models (all free, no gated licence click-through required)
# ------------------------------------------------------------------
MODELS = {
    "SD-Turbo (fast, recommended)": {
        "repo_id": "stabilityai/sd-turbo",
        "default_steps": 2,
        "max_steps": 4,
        "default_guidance": 0.0,
        "uses_negative": False,
        "native_size": 512,
        "description": "Fast draft model (1–4 steps). Use for previews; it produces less detail than the quality model.",
    },
    "Stable Diffusion v1.5 (classic, higher detail)": {
        "repo_id": "stable-diffusion-v1-5/stable-diffusion-v1-5",
        "default_steps": 25,
        "max_steps": 25,
        "default_guidance": 7.5,
        "uses_negative": True,
        "native_size": 512,
        "description": "Recommended for final posters: more inference steps, negative prompts, and sharper subject detail. Slower than SD-Turbo.",
    },
}
DEFAULT_MODEL = "Stable Diffusion v1.5 (classic, higher detail)"

# ------------------------------------------------------------------
# Poster Layout Styles (Directly matching professional healthcare reference posters)
# ------------------------------------------------------------------
POSTER_LAYOUTS = {
    "Modern Visual Hero (Full-Bleed)": {
        "id": "modern_hero",
        "name": "Modern Visual Hero (Full-Bleed)",
        "icon": "🖼️",
        "description": "Full-width hero artwork showcasing custom scenes, people, and colors with sleek typography and health tips.",
    },
    "Split Editorial (Reference 3)": {
        "id": "split_editorial",
        "name": "Split Editorial & Health Tips",
        "icon": "📰",
        "description": "Top arched slogan & circular framed artwork; dark contrasting lower card with bullet health tips, gold quote, and contact info (Reference 3).",
    },
    "Radiant Sunburst (Reference 1)": {
        "id": "sunburst",
        "name": "Radiant Sunburst Awareness",
        "icon": "☀️",
        "description": "Dynamic radiating sunburst rays & soft clouds, isolated centerpiece artwork with luminous aura, bold headline banner, and educational copy (Reference 1).",
    },
    "World Health Day Card (Reference 2)": {
        "id": "community_card",
        "name": "World Health Day / Community Card",
        "icon": "🌍",
        "description": "Clean airy white card with script accent title, partner organization header, central illustrated circle with clouds & health crosses (Reference 2).",
    },
    "Minimalist Modern Geometry (Reference 4)": {
        "id": "minimalist_geo",
        "name": "Minimalist Modern Geometry",
        "icon": "📐",
        "description": "Warm pastel canvas, split bold headline ('SAFE BLOOD' / 'SAVES LIVES'), geometric accent line framing the central artwork, and partner badges (Reference 4).",
    },
}
DEFAULT_POSTER_LAYOUT = "Modern Visual Hero (Full-Bleed)"

# ------------------------------------------------------------------
# Resolutions (width, height) – for artwork generation
# ------------------------------------------------------------------
RESOLUTIONS = {
    "Square 512 × 512 (fastest)": (512, 512),
    "Portrait 512 × 768 (posters)": (512, 768),
    "Large Square 768 × 768 (GPU only)": (768, 768),
}
DEFAULT_RESOLUTION = "Square 512 × 512 (fastest)"

POSTER_WIDTH = 1024
POSTER_HEIGHT = 1536
MAX_VARIATIONS = 4

# ------------------------------------------------------------------
# Campaign categories
# ------------------------------------------------------------------
CUSTOM_CATEGORY = "✏️ Custom Category"

CATEGORIES = {
    "General Wellness": {
        "icon": "🌿",
        "visuals": "minimalist clean illustration of a healthy human figure stretching peacefully with green leaves and sunlight rays",
        "palette": "calming health teal, soft aqua, and golden sunlight tones",
    },
    "Free Eye Checkup & Vision Camp": {
        "icon": "👁️",
        "visuals": "professional optometrist examining patient eye with modern vision chart, bright optical clinic, crystal clear focus",
        "palette": "clinical cobalt blue, crisp white, and aqua tones",
    },
    "Dental Hygiene & Oral Health Camp": {
        "icon": "🦷",
        "visuals": "radiant healthy smiling person with clean bright teeth, friendly dentist with dental mirror, modern clinic lighting",
        "palette": "fresh mint teal, clean sky blue, and pure white tones",
    },
    "Pediatric Care & Vaccination Camp": {
        "icon": "👶",
        "visuals": "caring pediatrician doctor smiling with happy healthy child and mother, cheerful warm pediatric clinic",
        "palette": "cheerful sunny yellow, soft sky blue, and gentle coral tones",
    },
    "Senior Mobility & Orthopedic Camp": {
        "icon": "🚶",
        "visuals": "active happy senior elder walking outdoors in sunny park, physical therapist assisting with gentle rehabilitation",
        "palette": "warm amber gold, sage green, and earthy navy tones",
    },
    "Dengue & Infectious Disease Prevention": {
        "icon": "🛡️",
        "visuals": "community health workers protecting clean water tanks, mosquito net protection, clean hygienic home environment",
        "palette": "protective warning orange, deep navy blue, and clean teal tones",
    },
    "Mental Health": {
        "icon": "🧠",
        "visuals": "silhouette profile of a human head with a vibrant colorful tree of brain leaves, calm meditation, peaceful nature, balance and hope",
        "palette": "deep midnight blue, amber gold, and soft teal tones",
    },
    "Heart Health": {
        "icon": "❤️",
        "visuals": "stylized vector anatomical lungs and heart, clean medical illustration, active runners, heart-shaped motifs, vitality",
        "palette": "radiant cyan, coral red, and crisp white tones",
    },
    "Blood Donation Awareness": {
        "icon": "🩸",
        "visuals": "modern geometric blood droplet emblem with vibrant red and coral gradient lines, gift of life, caring community",
        "palette": "deep slate navy, vivid crimson, and warm blush tones",
    },
    "World Health Day": {
        "icon": "🌍",
        "visuals": "diverse people exercising around a clean stylized earth globe, yoga, skipping rope, fresh apple, medical crosses, sunny sky",
        "palette": "royal health blue, teal green, and cheerful sun yellow tones",
    },
    "Diabetes Awareness": {
        "icon": "🥗",
        "visuals": "colorful balanced bowl of fresh vegetables and whole grains, active people walking, blue circle wellness motif",
        "palette": "sky blue, fresh green, and clean white tones",
    },
    "Healthy Eating": {
        "icon": "🥑",
        "visuals": "a healthy happy smiling woman holding a fresh bowl of ripe fruits and green vegetables, bright natural sunlight, kitchen daylight",
        "palette": "fresh leafy green, carrot orange, and warm lime tones",
    },
    "Physical Fitness": {
        "icon": "🏃",
        "visuals": "energetic silhouettes of diverse people running and stretching outdoors at sunrise, athletic energy",
        "palette": "energetic athletic teal, vibrant orange, and white tones",
    },
    "Women's Health Awareness": {
        "icon": "🌸",
        "visuals": "artistic flat vector illustration of diverse women smiling together with floral botanical accents, strength, self-care",
        "palette": "soft rose, blossom pink, and coral tones",
    },
    "Cancer Awareness": {
        "icon": "🎗️",
        "visuals": "elegant awareness ribbon intertwined with hopeful blooming botanical flowers, solidarity, hope, early screening",
        "palette": "awareness purple, hope pink, and gentle lavender tones",
    },
}

# ------------------------------------------------------------------
# Visual styles
# ------------------------------------------------------------------
STYLES = {
    "Flat Vector Graphic": {
        "icon": "📐",
        "prompt": "modern flat vector art, clean Swiss graphic design, expressive shapes, harmonious colors, no messy artifacts",
        "negative": "blurry, grainy, 3d render, noisy texture, photorealistic",
    },
    "Photographic & Realistic": {
        "icon": "📷",
        "prompt": "clean professional editorial lifestyle photography, crisp subject focus, natural soft lighting, high resolution 35mm film aesthetic, clean composition",
        "negative": "cartoon, anime, 3d render, illustration, sketch, blurry, oversaturated, deformed",
    },
    "Modern 3D Digital & Clay": {
        "icon": "🧊",
        "prompt": "3D digital artwork, smooth clay style, soft studio rim lighting, vibrant depth, tactile materials, modern graphic render",
        "negative": "flat 2d, sketch, rough drawing, blurry, grainy",
    },
    "Minimalist Modern Geometry": {
        "icon": "⚪",
        "prompt": "minimalist graphic design, bold iconic silhouettes, elegant negative space, clean geometric composition",
        "negative": "cluttered, messy, noisy, low resolution, blurry",
    },
    "Watercolor & Fine Art": {
        "icon": "🖌️",
        "prompt": "soft expressive watercolor painting, luminous color washes, delicate ink line art, artistic and hopeful, clean paper texture",
        "negative": "harsh plastic 3d render, photo, neon, dark muddy colors",
    },
    "Bold Pop & Screenprint": {
        "icon": "🎨",
        "prompt": "bold contemporary screenprint poster art, high contrast, vibrant graphic color blocking, striking editorial visual",
        "negative": "blurry, dull colors, low resolution, messy artifacts",
    },
}
DEFAULT_STYLE = "Photographic & Realistic"

# ------------------------------------------------------------------
# Rich Campaign Presets (Matching Real Healthcare Campaigns)
# ------------------------------------------------------------------
CAMPAIGN_PRESETS = {
    "Mental Health": {
        "headline": "MENTAL HEALTH MONTH",
        "slogan": "Take Care of What's Inside",
        "body": "This month, let's break the stigma and start the conversation. Mental health is just as important as physical health. Take time to rest, connect, and care for your mind.",
        "bullet_points": [
            "Talk openly about mental health with loved ones",
            "Reach out for support whenever you feel overwhelmed",
            "Practice daily self-care, healthy boundaries & balance",
            "Support and listen to others with kindness & patience",
        ],
        "quote": "Together, we can build a world where mental health is prioritized, understood, and supported.",
        "org_name": "Mental Health & Care Alliance",
        "helpline": "Support Helpline: +1 800 273 8255 · Visit: www.wellaware.org",
        "artwork_prompt": "silhouette profile of a human head with a vibrant colorful tree of brain leaves growing inside, isolated on pure white background, flat vector illustration, dribbble design, high quality, clean lines, no text",
    },
    "Heart Health": {
        "headline": "WORLD HEALTHY DAY",
        "slogan": "Strong Heart, Healthy Lungs, Full Life",
        "body": "Your cardiovascular and respiratory systems work in harmony every second. Nourish your heart and protect your lungs through regular movement, clean air, and nutritious whole foods.",
        "bullet_points": [
            "Engage in at least 30 minutes of aerobic exercise daily",
            "Eat nutrient-dense whole foods rich in omega-3 & fiber",
            "Avoid smoking and protect your lungs from polluted air",
            "Monitor your resting heart rate and blood pressure regularly",
        ],
        "quote": "Every heartbeat is a reminder to cherish your health and move with purpose.",
        "org_name": "Global Cardiovascular Health Partnership",
        "helpline": "Heart Helpline: +1 800 432 7878 · Visit: www.wellaware.org",
        "artwork_prompt": "stylized anatomical lungs and heart vector art illustration, clean bold red and deep blue tones, isolated on white background, modern healthcare graphic, dribbble, crisp vector shapes, no text",
    },
    "Blood Donation Awareness": {
        "headline": "SAFE BLOOD SAVES LIVES",
        "slogan": "Give Blood and Make the World a Healthier Place",
        "body": "Safe blood and blood products are essential for surgeries, emergency trauma care, and chronic conditions. A single voluntary donation can save up to three lives.",
        "bullet_points": [
            "A single blood donation takes under an hour and saves up to 3 lives",
            "Voluntary unpaid blood donors are the foundation of safe blood supplies",
            "Stay well hydrated and eat an iron-rich meal prior to donating",
            "Encourage friends and community members to become regular donors",
        ],
        "quote": "Your blood is a gift of life. Share the pulse of life with those in need.",
        "org_name": "World Blood Donor Organization · WHO Partner",
        "helpline": "Donor Line: +1 800 448 3766 · Find a Center: www.wellaware.org",
        "artwork_prompt": "modern minimalist geometric blood droplet emblem with vibrant red and coral gradient lines, clean icon vector art, isolated on white background, sleek healthcare logo, dribbble, no text",
    },
    "World Health Day": {
        "headline": "WORLD HEALTH DAY",
        "slogan": "My Health, My Right · Wellness for Every Community",
        "body": "Good health begins with active communities and accessible care. Empower yourself through daily movement, balanced nutrition, mental peace, and solidarity with those around you.",
        "bullet_points": [
            "Incorporate daily physical activity like walking, yoga, or jogging",
            "Choose colorful whole foods, fresh vegetables, and adequate water",
            "Prioritize restorative sleep and positive social connections",
            "Schedule regular preventive health check-ups for your family",
        ],
        "quote": "Health is not merely the absence of illness, but a complete state of physical, mental, and social vitality.",
        "org_name": "Humber and North Yorkshire Health and Care Partnership",
        "helpline": "Community Health Hub · Visit: www.wellaware.org",
        "artwork_prompt": "diverse smiling people exercising around a clean stylized earth globe, yoga meditation, dumbbell lifting, skipping rope, fresh apple, flat vector illustration, isolated on white background, dribbble, no text",
    },
    "Diabetes Awareness": {
        "headline": "BEAT DIABETES TOGETHER",
        "slogan": "Empower Your Life Through Balanced Living",
        "body": "Managing and preventing diabetes is within your hands. Smart meal choices, daily active movement, and early screening empower you and your loved ones to live full, vibrant lives.",
        "bullet_points": [
            "Choose fiber-rich whole grains and leafy green vegetables",
            "Stay active with brisk walks after meals to support glucose uptake",
            "Keep hydrated with water and limit sugary beverages and syrups",
            "Check your HbA1c and fasting blood sugar levels annually",
        ],
        "quote": "Small, consistent daily habits build the strongest defense for lifelong vitality.",
        "org_name": "International Diabetes Wellness Alliance",
        "helpline": "Wellness Helpline: +1 800 342 2383 · Visit: www.wellaware.org",
        "artwork_prompt": "colorful balanced bowl of fresh vegetables and whole grains with subtle stylized blue circle motif, isolated on white background, flat vector art, modern editorial illustration, clean, no text",
    },
    "Healthy Eating": {
        "headline": "EAT FRESH, LIVE VIBRANT",
        "slogan": "Nourish Your Body from the Inside Out",
        "body": "Food is the foundation of energy, immunity, and longevity. Transform your plate into a colorful celebration of whole fruits, leafy vegetables, nuts, and natural nutrients.",
        "bullet_points": [
            "Fill half your plate with colorful fruits and vegetables daily",
            "Drink plenty of water and minimize ultra-processed foods",
            "Cook whole-food meals at home together with family",
            "Listen to your hunger cues and practice mindful eating",
        ],
        "quote": "Let your food be your daily medicine and your kitchen be your source of health.",
        "org_name": "Nutrition & Public Health Initiative",
        "helpline": "Healthy Living Line: +1 800 782 5238 · Visit: www.wellaware.org",
        "artwork_prompt": "vibrant fresh salad bowl overflowing with colorful avocado, tomatoes, greens and citrus, clean vector art, isolated on white background, flat modern illustration, dribbble, no text",
    },
    "Physical Fitness": {
        "headline": "MOVE YOUR BODY DAILY",
        "slogan": "Energy, Strength, and Longevity in Every Step",
        "body": "Movement is celebration, not a chore. Whether it's a brisk walk, dancing, yoga, or lifting weights, physical activity sharpens the mind, strengthens the heart, and elevates your mood.",
        "bullet_points": [
            "Aim for 150 minutes of moderate activity or 75 minutes vigorous weekly",
            "Include strength and flexibility training twice a week",
            "Take short walking breaks every hour during sedentary work",
            "Find activities you genuinely enjoy and do them with friends",
        ],
        "quote": "You don't have to be extreme, just consistent. Every step moves you forward.",
        "org_name": "Active Living & Fitness Foundation",
        "helpline": "Fitness Hub: +1 800 555 3488 · Visit: www.wellaware.org",
        "artwork_prompt": "energetic silhouettes of diverse people running and stretching outdoors at sunrise, dynamic flat vector illustration, isolated on white background, modern healthcare design, no text",
    },
    "Women's Health Awareness": {
        "headline": "WOMEN'S WELLNESS FIRST",
        "slogan": "Nurturing Strength, Harmony, and Lifelong Care",
        "body": "Women's health encompasses physical strength, emotional balance, reproductive wellness, and self-care. Prioritize your well-being through proactive check-ups and daily rejuvenation.",
        "bullet_points": [
            "Schedule regular preventive screenings and wellness exams",
            "Maintain bone and heart strength with weight-bearing exercises",
            "Prioritize mental peace, restful sleep, and emotional support networks",
            "Nourish your body with calcium, iron, and antioxidant-rich foods",
        ],
        "quote": "When women thrive in health and spirit, entire families and communities flourish.",
        "org_name": "Women's Health & Wellness Alliance",
        "helpline": "Support Helpline: +1 800 994 9662 · Visit: www.wellaware.org",
        "artwork_prompt": "artistic flat vector illustration of diverse women smiling together with floral botanical accents, soft pastel colors, isolated on white background, dribbble, modern healthcare visual, no text",
    },
    "Cancer Awareness": {
        "headline": "HOPE, STRENGTH & SCREENING",
        "slogan": "United in the Fight · Early Detection Saves Lives",
        "body": "Early detection remains the single most powerful tool in fighting cancer. Learn the signs, participate in recommended screenings, and stand in solidarity with survivors and fighters everywhere.",
        "bullet_points": [
            "Participate in age-appropriate cancer screenings and regular check-ups",
            "Know your family history and discuss risk factors with your clinician",
            "Adopt an active lifestyle, sun protection, and smoke-free living",
            "Support and stand beside loved ones undergoing treatment",
        ],
        "quote": "Hope is the anchor of the soul and the spark that ignites our collective strength.",
        "org_name": "National Cancer Awareness Coalition",
        "helpline": "Care & Guidance Hotline: +1 800 227 2345 · Visit: www.wellaware.org",
        "artwork_prompt": "elegant awareness ribbon intertwined with hopeful blooming botanical flowers, vibrant soft colors, isolated on white background, flat modern vector illustration, clean, no text",
    },
    "General Wellness": {
        "headline": "WELLNESS STARTS TODAY",
        "slogan": "Small Healthy Steps for a Lifetime of Vitality",
        "body": "True wellness is the harmony of body, mind, and spirit. Celebrate each day with wholesome nutrition, refreshing hydration, joyful movement, and calm moments of gratitude.",
        "bullet_points": [
            "Drink at least 8 glasses of fresh water throughout the day",
            "Prioritize 7-8 hours of uninterrupted, restorative sleep",
            "Take 10 minutes daily for deep breathing and mental stillness",
            "Spend time in natural sunlight and green outdoor spaces",
        ],
        "quote": "Wellness is a connection of paths: what we eat, how we move, and how we care for ourselves.",
        "org_name": "WellAware Community Health Foundation",
        "helpline": "WellAware Hotline: 1-800-WELLNESS · Visit: www.wellaware.org",
        "artwork_prompt": "minimalist clean illustration of a healthy human figure stretching peacefully with green leaves and sunlight rays, isolated on white background, modern flat vector, dribbble, no text",
    },
    "Free Eye Checkup & Vision Camp": {
        "headline": "CLEAR VISION FOR LIFE",
        "slogan": "Protect Your Eyesight, Brighten Your World",
        "body": "Sight is our most precious window to the world. Regular eye screenings detect early vision changes, protect against digital strain, and ensure clear sight for life.",
        "bullet_points": [
            "Follow the 20-20-20 rule: rest eyes every 20 minutes from screens",
            "Wear UV-protective sunglasses in bright sunlight",
            "Ensure comfortable lighting when reading or working",
            "Schedule annual comprehensive eye examinations",
        ],
        "quote": "The eyes are the windows to the soul and the guide to a vibrant life.",
        "org_name": "Community Vision Care Alliance",
        "helpline": "Eye Care Helpline: 1-800-EYE-CARE · Visit: www.wellaware.org",
        "artwork_prompt": "A friendly optometrist and one adult patient during a routine eye check, waist-up composition, clear faces, simple bright clinic background without signs or visible text.",
    },
    "Dental Hygiene & Oral Health Camp": {
        "headline": "HEALTHY SMILES, HEALTHY LIFE",
        "slogan": "Brushing Away Disease, Smiling with Confidence",
        "body": "Oral wellness is directly connected to overall systemic health. Protecting your teeth and gums prevents infections and keeps your natural smile bright and strong.",
        "bullet_points": [
            "Brush thoroughly twice daily with fluoride toothpaste",
            "Floss daily to remove plaque between tight teeth",
            "Limit sugary beverages, candy, and sticky snacks",
            "Visit your dental professional every six months",
        ],
        "quote": "A genuine smile is the shortest distance between two people.",
        "org_name": "Community Dental Health Alliance",
        "helpline": "Dental Helpline: 1-800-SMILE-DOC · Visit: www.wellaware.org",
        "artwork_prompt": "A friendly dentist beside one adult patient with a healthy smile in a bright dental clinic, waist-up portrait, simple background, no signs or visible text.",
    },
    "Pediatric Care & Vaccination Camp": {
        "headline": "NURTURING CHILD WELLNESS",
        "slogan": "Healthy Steps for Little Champions",
        "body": "Every child deserves a strong foundation for lifelong vitality. Wholesome nutrition, active play, timely vaccinations, and loving care shape a bright future.",
        "bullet_points": [
            "Ensure age-appropriate immunizations and routine checkups",
            "Provide balanced home meals rich in whole fruits and vegetables",
            "Encourage at least 60 minutes of joyful active play every day",
            "Foster emotional security and screen-free family connection",
        ],
        "quote": "Children are our greatest treasure and the future of our communities.",
        "org_name": "Community Pediatric Coalition",
        "helpline": "Child Wellness Line: 1-800-KID-CARE · Visit: www.wellaware.org",
        "artwork_prompt": "A pediatrician, one child, and one parent smiling together in a bright clinic, waist-up portrait, three clear faces, plain background without signs or text.",
    },
    "Senior Mobility & Orthopedic Camp": {
        "headline": "ACTIVE & HEALTHY AGING",
        "slogan": "Vitality, Wisdom, and Grace at Every Stage of Life",
        "body": "Aging with vitality begins with daily movement, sharp minds, and strong social bonds. Take proactive care of bone strength, cardiovascular wellness, and joint flexibility.",
        "bullet_points": [
            "Engage in daily gentle walking, stretching, or swimming",
            "Stay connected with community, friends, and family",
            "Nourish bone and brain vitality with wholesome foods",
            "Monitor blood pressure and medication schedules regularly",
        ],
        "quote": "Age is an honor and a testament to a life lived with purpose and care.",
        "org_name": "Senior Wellness Partnership",
        "helpline": "Senior Care Line: 1-800-SENIOR-CARE · Visit: www.wellaware.org",
        "artwork_prompt": "An active older adult walking beside a physical therapist on a quiet sunny park path, medium shot, two clear faces, uncluttered background without signs or text.",
    },
    "Dengue & Infectious Disease Prevention": {
        "headline": "PREVENT MOSQUITO ILLNESS",
        "slogan": "Clean Surroundings, Safe and Healthy Communities",
        "body": "Vector-borne diseases are preventable through proactive community hygiene. Eliminate standing water, protect your living spaces, and stay alert to early fever symptoms.",
        "bullet_points": [
            "Empty and scrub water containers, flower pots, and coolers weekly",
            "Install fine mesh window screens and sleep under bed nets",
            "Apply protective insect repellent when outdoors at dawn and dusk",
            "Seek prompt medical testing at the first onset of high fever",
        ],
        "quote": "A clean community is the first and strongest barrier against disease.",
        "org_name": "Public Health Vector Taskforce",
        "helpline": "Vector Control Hotline: 1-800-MOSQUITO · Visit: www.wellaware.org",
        "artwork_prompt": "One community health worker checking a covered water container in a clean sunny yard, medium shot, simple background without signs or visible text.",
    },
}

# ------------------------------------------------------------------
# Poster Color Palettes (Rich Healthcare Palettes)
# ------------------------------------------------------------------
POSTER_PALETTES = {
    "Mental Health": {
        "primary": "#0D253F",       # Deep navy (like Ref 3)
        "accent": "#F5A623",        # Warm gold / amber
        "accent2": "#2EB872",       # Soft teal/green
        "bg_light": "#FFFDF8",      # Warm cream
        "bg_dark": "#0B1D30",       # Dark card
        "text_dark": "#0D253F",
        "text_light": "#FFFFFF",
        "badge_bg": "#F5A623",
    },
    "Heart Health": {
        "primary": "#0B7A8B",       # Cyan/Teal (like Ref 1 sunburst)
        "accent": "#E63946",        # Red / coral
        "accent2": "#457B9D",       # Steel blue
        "bg_light": "#F0F9FB",      # Light cyan tint
        "bg_dark": "#0A3641",
        "text_dark": "#0B3039",
        "text_light": "#FFFFFF",
        "badge_bg": "#E63946",
    },
    "Blood Donation Awareness": {
        "primary": "#1A365D",       # Deep slate navy (like Ref 4)
        "accent": "#E63946",        # Vivid blood red
        "accent2": "#F4A261",       # Coral pink gradient
        "bg_light": "#FFF5F2",      # Warm blush cream
        "bg_dark": "#132338",
        "text_dark": "#1A365D",
        "text_light": "#FFFFFF",
        "badge_bg": "#E63946",
    },
    "World Health Day": {
        "primary": "#1E3A8A",       # Royal health blue (like Ref 2)
        "accent": "#0D9488",        # Teal green
        "accent2": "#F59E0B",       # Sun yellow
        "bg_light": "#FFFFFF",      # Crisp clean white
        "bg_dark": "#111827",
        "text_dark": "#111827",
        "text_light": "#FFFFFF",
        "badge_bg": "#0D9488",
    },
    "Diabetes Awareness": {
        "primary": "#0369A1",       # Blue
        "accent": "#06B6D4",        # Sky cyan
        "accent2": "#10B981",       # Emerald
        "bg_light": "#F0F9FF",
        "bg_dark": "#082F49",
        "text_dark": "#082F49",
        "text_light": "#FFFFFF",
        "badge_bg": "#0284C7",
    },
    "Healthy Eating": {
        "primary": "#166534",       # Deep garden green
        "accent": "#84CC16",        # Fresh lime
        "accent2": "#F97316",       # Vibrant carrot orange
        "bg_light": "#F7FEE7",
        "bg_dark": "#14532D",
        "text_dark": "#14532D",
        "text_light": "#FFFFFF",
        "badge_bg": "#15803D",
    },
    "Physical Fitness": {
        "primary": "#0F766E",       # Deep athletic teal
        "accent": "#F97316",        # High energy orange
        "accent2": "#06B6D4",       # Sky blue
        "bg_light": "#F0FDFA",
        "bg_dark": "#134E4A",
        "text_dark": "#134E4A",
        "text_light": "#FFFFFF",
        "badge_bg": "#F97316",
    },
    "Women's Health Awareness": {
        "primary": "#9D174D",       # Rich rose / berry
        "accent": "#F472B6",        # Blossom pink
        "accent2": "#FB7185",       # Coral
        "bg_light": "#FDF2F8",
        "bg_dark": "#831843",
        "text_dark": "#831843",
        "text_light": "#FFFFFF",
        "badge_bg": "#DB2777",
    },
    "Cancer Awareness": {
        "primary": "#701A75",       # Awareness purple / plum
        "accent": "#F43F5E",        # Hope pink
        "accent2": "#C084FC",       # Lavender
        "bg_light": "#FAF5FF",
        "bg_dark": "#581C87",
        "text_dark": "#581C87",
        "text_light": "#FFFFFF",
        "badge_bg": "#9333EA",
    },
    "General Wellness": {
        "primary": "#0F766E",       # Health teal
        "accent": "#14B8A6",        # Aqua
        "accent2": "#F59E0B",       # Golden sunlight
        "bg_light": "#F0FDFA",
        "bg_dark": "#115E59",
        "text_dark": "#134E4A",
        "text_light": "#FFFFFF",
        "badge_bg": "#0D9488",
    },
    "Free Eye Checkup & Vision Camp": {
        "primary": "#0369A1",
        "accent": "#06B6D4",
        "accent2": "#38BDF8",
        "bg_light": "#F0F9FF",
        "bg_dark": "#082F49",
        "text_dark": "#082F49",
        "text_light": "#FFFFFF",
        "badge_bg": "#0284C7",
    },
    "Dental Hygiene & Oral Health Camp": {
        "primary": "#0D9488",
        "accent": "#14B8A6",
        "accent2": "#2DD4BF",
        "bg_light": "#F0FDFA",
        "bg_dark": "#115E59",
        "text_dark": "#115E59",
        "text_light": "#FFFFFF",
        "badge_bg": "#0D9488",
    },
    "Pediatric Care & Vaccination Camp": {
        "primary": "#D97706",
        "accent": "#F59E0B",
        "accent2": "#FB7185",
        "bg_light": "#FFFBEB",
        "bg_dark": "#78350F",
        "text_dark": "#78350F",
        "text_light": "#FFFFFF",
        "badge_bg": "#D97706",
    },
    "Senior Mobility & Orthopedic Camp": {
        "primary": "#475569",
        "accent": "#F59E0B",
        "accent2": "#10B981",
        "bg_light": "#F8FAFC",
        "bg_dark": "#1E293B",
        "text_dark": "#1E293B",
        "text_light": "#FFFFFF",
        "badge_bg": "#475569",
    },
    "Dengue & Infectious Disease Prevention": {
        "primary": "#EA580C",
        "accent": "#F97316",
        "accent2": "#0D9488",
        "bg_light": "#FFF7ED",
        "bg_dark": "#7C2D12",
        "text_dark": "#7C2D12",
        "text_light": "#FFFFFF",
        "badge_bg": "#EA580C",
    },
}

THEME_PALETTES = {
    "✨ Auto-Detect from Prompt & Campaign": None,
    "💜 Awareness Purple & Golden Hope": {
        "primary": "#701A75", "accent": "#F5A623", "accent2": "#C084FC",
        "bg_light": "#FAF5FF", "bg_dark": "#3B0764", "text_dark": "#3B0764", "text_light": "#FFFFFF", "badge_bg": "#9333EA",
    },
    "💙 Royal Health Blue & Teal": {
        "primary": "#1E3A8A", "accent": "#0D9488", "accent2": "#38BDF8",
        "bg_light": "#F0F9FF", "bg_dark": "#0B1D30", "text_dark": "#0B1D30", "text_light": "#FFFFFF", "badge_bg": "#0D9488",
    },
    "💚 Fresh Botanical Green & Lime": {
        "primary": "#166534", "accent": "#84CC16", "accent2": "#F59E0B",
        "bg_light": "#F7FEE7", "bg_dark": "#14532D", "text_dark": "#14532D", "text_light": "#FFFFFF", "badge_bg": "#15803D",
    },
    "❤️ Crimson Blood Red & Slate Navy": {
        "primary": "#1A365D", "accent": "#E63946", "accent2": "#F4A261",
        "bg_light": "#FFF5F2", "bg_dark": "#132338", "text_dark": "#132338", "text_light": "#FFFFFF", "badge_bg": "#E63946",
    },
    "🧡 Athletic Sunrise Orange & Cyan": {
        "primary": "#0F766E", "accent": "#F97316", "accent2": "#06B6D4",
        "bg_light": "#F0FDFA", "bg_dark": "#134E4A", "text_dark": "#134E4A", "text_light": "#FFFFFF", "badge_bg": "#F97316",
    },
    "🌸 Rose Blossom & Warm Coral": {
        "primary": "#9D174D", "accent": "#F472B6", "accent2": "#FB7185",
        "bg_light": "#FDF2F8", "bg_dark": "#831843", "text_dark": "#831843", "text_light": "#FFFFFF", "badge_bg": "#DB2777",
    },
    "🌙 Modern Midnight Dark & Cyan Glow": {
        "primary": "#0284C7", "accent": "#38BDF8", "accent2": "#22D3EE",
        "bg_light": "#F8FAFC", "bg_dark": "#0F172A", "text_dark": "#0F172A", "text_light": "#FFFFFF", "badge_bg": "#0284C7",
    },
}

# ------------------------------------------------------------------
# Prompt engineering constants
# ------------------------------------------------------------------
QUALITY_TAGS = "high quality professional healthcare campaign visual, clean composition, vivid harmonious colors, sharp focus, award-winning design, no text, no watermark"

BASE_NEGATIVE_PROMPT = (
    "text, words, letters, numbers, writing, signage, signs, banners, labels, captions, typography, "
    "poster graphics, brand names, watermark, logo, blurry, out of focus, low resolution, jpeg artifacts, "
    "deformed face, asymmetrical eyes, unnatural smile, distorted anatomy, malformed hands, "
    "extra fingers, missing fingers, fused fingers, malformed limbs, duplicate people, cluttered composition"
)

# ------------------------------------------------------------------
# Input validation & safety
# ------------------------------------------------------------------
MIN_PROMPT_CHARS = 3
MAX_PROMPT_CHARS = 500

BLOCKED_TERMS = [
    # clinical / diagnostic imagery
    "x-ray", "xray", "mri", "ct scan", "ultrasound", "biopsy", "tumor", "tumour",
    "surgery", "surgical", "operation theatre", "autopsy", "diagnosis", "diagnose",
    "diagnostic", "lab report", "prescription", "dosage",
    # graphic / unsafe content
    "blood and gore", "bloody wound", "violent blood", "excessive bleeding", "blood splatter",
    "gore", "wound", "corpse", "dead body", "suicide", "self-harm", "self harm",
    "nude", "nudity", "naked", "nsfw", "sexual", "weapon", "gun", "violence",
    # pharma branding
    "pfizer", "novartis", "johnson & johnson", "astrazeneca", "moderna", "roche",
    "merck", "sanofi", "gsk", "bayer", "abbott", "eli lilly",
]

CLAIM_TERMS = [
    "cure", "cures", "guaranteed", "guarantee", "100%", "miracle", "heals",
    "treats", "treatment", "reverse diabetes", "prevents cancer", "clinically proven",
]

DISCLAIMER_SHORT = "AI-generated illustration · Review before publication · Not medical advice"

DISCLAIMER_FULL = (
    "WellAware AI creates **illustrative, non-clinical** wellness and awareness visuals "
    "using a pretrained AI model. Generated images are **not medical advice**, may contain "
    "inaccuracies, and **must be reviewed by a qualified person** (medical, legal, brand) "
    "before publication. Do not use these images to imply medical claims or diagnoses."
)

# ------------------------------------------------------------------
# UI colours (healthcare palette)
# ------------------------------------------------------------------
COLORS = {
    "primary": "#0F9D9A",      # teal
    "primary_dark": "#0B7B78",
    "secondary": "#3BA4E8",    # light blue
    "bg_soft": "#F2FAFB",
    "text": "#1F3B4D",
    "muted": "#6B8794",
    "border": "#DCEFF2",
}
