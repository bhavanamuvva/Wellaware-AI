import unittest

from PIL import Image

import config
from modules.image_utils import _readable_text_color, create_campaign_poster
from modules.prompt_processor import PosterCopy, build_prompt


class CampaignQualityTests(unittest.TestCase):
    def test_human_prompt_preserves_selected_art_style(self):
        prompt = build_prompt(
            "A friendly dentist smiling in a clinic",
            "Dental Hygiene & Oral Health Camp",
            "Flat Vector Graphic",
        )

        self.assertEqual(prompt.style, "Flat Vector Graphic")
        self.assertIn("modern flat vector art", prompt.positive)
        self.assertNotIn("photography", prompt.positive)
        self.assertIn("no more than three people", prompt.positive)
        self.assertIn("hands out of frame", prompt.positive)
        self.assertIn("no visible text", prompt.positive)
        self.assertNotIn("Dental Hygiene & Oral Health Camp subject:", prompt.positive)
        self.assertLess(len(prompt.positive.split()), 70)
        self.assertIn("signage", prompt.negative)

    def test_quality_model_is_the_default_with_full_step_count(self):
        self.assertEqual(config.DEFAULT_MODEL, "Stable Diffusion v1.5 (classic, higher detail)")
        self.assertEqual(config.MODELS[config.DEFAULT_MODEL]["default_steps"], 25)

    def test_photographic_human_prompt_avoids_duplicated_category_scene(self):
        category = "Dental Hygiene & Oral Health Camp"
        prompt = build_prompt(
            config.CAMPAIGN_PRESETS[category]["artwork_prompt"],
            category,
            "Photographic & Realistic",
        )

        self.assertIn("photorealistic editorial portrait", prompt.positive)
        self.assertIn("one to three people", prompt.positive)
        self.assertIn("hands out of frame", prompt.positive)
        self.assertIn("no visible text", prompt.positive)
        self.assertNotIn("campaign:", prompt.positive)
        self.assertLess(len(prompt.positive.split()), 70)

    def test_light_custom_background_uses_dark_text(self):
        self.assertEqual(_readable_text_color("#BFE8F3", "#FFFFFF"), "#0B1D30")

    def test_all_poster_layouts_render_campaign_copy(self):
        copy = PosterCopy(
            headline="HEALTHY SMILES",
            slogan="A brighter smile starts with care.",
            body="Protect your teeth with regular checkups and daily care.",
            bullet_points=["Brush twice daily", "Floss every day", "Choose water over sugary drinks"],
            quote="Small daily habits make a lasting difference.",
            org_name="Community Dental Alliance",
            helpline="Call your local clinic",
        )
        artwork = Image.new("RGB", (64, 64), "#5AAABB")

        for layout in config.POSTER_LAYOUTS:
            with self.subTest(layout=layout):
                poster = create_campaign_poster(
                    artwork,
                    copy,
                    category="Dental Hygiene & Oral Health Camp",
                    layout_name=layout,
                )
                self.assertEqual(poster.size, (config.POSTER_WIDTH, config.POSTER_HEIGHT))


if __name__ == "__main__":
    unittest.main()
