"""
modules/image_generator.py
--------------------------
AI image generation via Hugging Face Diffusers + Fast Vector Engine fallback.

Key points:
- Detects the best compute device: CUDA GPU -> Apple MPS -> CPU.
- Loads pretrained text-to-image pipeline with DPM-Solver scheduler for crisp, fast results.
- Includes Instant Vector Engine for real-time reference artwork generation.
- Generates reproducible images per seed.
"""

from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass
from typing import Callable, List, Optional

import config


class GenerationError(Exception):
    """Raised with a user-friendly message when generation fails."""


@dataclass
class DeviceInfo:
    device: str          # "cuda", "mps" or "cpu"
    name: str            # e.g. "Tesla T4"
    dtype_name: str      # "float16" or "float32"
    vram_gb: Optional[float] = None

    @property
    def is_gpu(self) -> bool:
        return self.device in ("cuda", "mps")


@dataclass
class GeneratedImage:
    image: "object"      # PIL.Image.Image
    seed: int
    seconds: float


# ------------------------------------------------------------------
# Environment checks
# ------------------------------------------------------------------
def check_dependencies() -> Optional[str]:
    missing = []
    for pkg in ("torch", "diffusers", "transformers", "accelerate"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        return ("Missing Python packages: " + ", ".join(missing) +
                ". Install them with `pip install -r requirements.txt`.")
    return None


def get_device_info() -> DeviceInfo:
    import torch

    if torch.cuda.is_available():
        props = torch.cuda.get_device_properties(0)
        return DeviceInfo("cuda", props.name, "float16", round(props.total_memory / 1024 ** 3, 1))
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return DeviceInfo("mps", "Apple Silicon GPU (MPS)", "float32")
    return DeviceInfo("cpu", "CPU", "float32")


def _get_hf_token() -> Optional[str]:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        try:
            import streamlit as st
            token = st.secrets.get("HF_TOKEN") or st.secrets.get("HUGGINGFACE_TOKEN")
        except Exception:
            pass
    return token or None


# ------------------------------------------------------------------
# Generator class
# ------------------------------------------------------------------
class WellnessImageGenerator:
    """Wraps Diffusers pipeline + Fast Vector Graphic Engine."""

    def __init__(self, model_label: str = config.DEFAULT_MODEL):
        if model_label not in config.MODELS:
            model_label = config.DEFAULT_MODEL
        self.model_label = model_label
        self.model_cfg = config.MODELS[model_label]
        self.device_info: Optional[DeviceInfo] = None
        self.pipe = None

    # ---------------- loading ----------------
    def load(self) -> "WellnessImageGenerator":
        dep_error = check_dependencies()
        if dep_error:
            raise GenerationError(dep_error)

        import torch
        from diffusers import AutoPipelineForText2Image

        self.device_info = get_device_info()
        dtype = torch.float16 if self.device_info.dtype_name == "float16" else torch.float32
        repo_id = self.model_cfg["repo_id"]

        load_kwargs = {"torch_dtype": dtype, "use_safetensors": True}
        token = _get_hf_token()
        if token:
            load_kwargs["token"] = token
        if dtype == torch.float16:
            load_kwargs["variant"] = "fp16"

        try:
            try:
                pipe = AutoPipelineForText2Image.from_pretrained(repo_id, **load_kwargs)
            except (OSError, ValueError):
                load_kwargs.pop("variant", None)
                pipe = AutoPipelineForText2Image.from_pretrained(repo_id, **load_kwargs)
        except Exception as exc:
            raise GenerationError(
                f"Could not load AI model '{repo_id}'. Check internet connection and disk space. "
                f"Details: {str(exc)[:250]}"
            ) from exc

        try:
            pipe = pipe.to(self.device_info.device)
        except Exception as exc:
            raise GenerationError(f"Could not move model to {self.device_info.device}: {exc}") from exc

        # Optimize scheduler for SD 1.5 (DPM-Solver is much faster and crisper)
        if "stable-diffusion-v1-5" in repo_id:
            try:
                from diffusers import DPMSolverMultistepScheduler
                pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            except Exception:
                pass

        try:
            pipe.enable_attention_slicing()
        except Exception:
            pass

        pipe.set_progress_bar_config(disable=True)
        self.pipe = pipe
        return self

    # ---------------- generation ----------------
    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        width: int = 512,
        height: int = 512,
        num_images: int = 1,
        steps: Optional[int] = None,
        guidance: Optional[float] = None,
        seed: Optional[int] = None,
        category: str = "General Wellness",
        progress_callback: Optional[Callable[[int, int, int], None]] = None,
        use_instant_engine: bool = False,
        theme_choice: Optional[str] = None,
    ) -> List[GeneratedImage]:
        """
        Generate `num_images` variations.
        If use_instant_engine is True, generates rich, themed vector art in 0.1s.
        """
        base_seed = seed if seed is not None else random.randint(0, 2 ** 31 - 1)
        num_images = max(1, min(int(num_images), config.MAX_VARIATIONS))

        if use_instant_engine:
            # Fast Layout Preview Synthesizer
            from modules.image_utils import generate_procedural_vector_art
            results = []
            for i in range(num_images):
                img_seed = base_seed + i
                start = time.time()
                img = generate_procedural_vector_art(category, prompt, width, height, theme_choice=theme_choice)
                results.append(GeneratedImage(image=img.convert("RGB"), seed=img_seed, seconds=round(time.time() - start, 2)))
            return results

        # Ensure AI pipeline is loaded
        if self.pipe is None:
            self.load()

        import torch

        steps = int(steps or self.model_cfg["default_steps"])
        guidance = float(self.model_cfg["default_guidance"] if guidance is None else guidance)
        width, height = (int(width) // 8) * 8, (int(height) // 8) * 8

        results: List[GeneratedImage] = []
        for i in range(num_images):
            img_seed = base_seed + i
            gen_device = "cpu" if self.device_info.device == "mps" else self.device_info.device
            generator = torch.Generator(device=gen_device).manual_seed(img_seed)

            kwargs = dict(
                prompt=prompt,
                width=width,
                height=height,
                num_inference_steps=steps,
                guidance_scale=guidance,
                generator=generator,
            )
            if self.model_cfg["uses_negative"] and guidance > 1.0:
                kwargs["negative_prompt"] = negative_prompt

            if progress_callback is not None:
                def _on_step(pipe, step, timestep, callback_kwargs, _i=i):
                    try:
                        progress_callback(_i, step + 1, steps)
                    except Exception:
                        pass
                    return callback_kwargs
                kwargs["callback_on_step_end"] = _on_step

            start = time.time()
            try:
                with torch.inference_mode():
                    output = self.pipe(**kwargs)
                image = output.images[0]
            except Exception as exc:
                raise GenerationError(f"AI image generation failed: {exc}") from exc

            results.append(GeneratedImage(image=image, seed=img_seed, seconds=round(time.time() - start, 1)))

        return results


def unload_cuda_memory() -> None:
    try:
        import gc
        import torch
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass
