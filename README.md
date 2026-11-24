# 🩺 WellAware AI – Patient Wellness Campaign Visual Generator

**Team 17 · Generative AI Project**

WellAware AI is a Streamlit web app that turns a short text description into a friendly,
patient-ready **wellness and health-awareness campaign image** using **Stable Diffusion**
(through Hugging Face Diffusers + PyTorch). Healthcare and pharmaceutical communication teams can
use it to draft awareness visuals without hand-designing every illustration.

> ⚠️ **Disclaimer:** Images are AI-generated, **illustrative and non-clinical**. They are **not
> medical advice** and **must be reviewed** by qualified people (medical, legal, brand) before
> publication.

---

## 1. Project architecture

```
WellAware-AI/
│
├── app.py                     # Streamlit UI: Home, Create Campaign, Gallery, Guidelines & Help
├── config.py                  # All settings: models, categories, styles, resolutions, safety lists, colours
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── WellAware_AI_Colab.ipynb   # Ready-made Google Colab notebook (GPU + public link)
├── .gitignore
│
├── .streamlit/
│   └── config.toml            # Light theme with teal / light-blue palette
│
├── modules/
│   ├── __init__.py
│   ├── prompt_processor.py    # Input validation, safety checks, prompt engineering, suggestions
│   ├── image_generator.py     # Stable Diffusion loading, GPU/CPU detection, generation, error handling
│   └── image_utils.py         # PNG conversion, disclaimer footer, saving, ZIP export, logo drawing
│
├── scripts/
│   └── quick_test.py          # Command-line test: loads the model and generates one image
│
├── assets/
│   └── logo.png               # App logo (re-drawn automatically if deleted)
│
└── generated_images/          # PNGs saved here when "save to folder" is on
```

### How the pieces fit together

```
User (Streamlit UI)
   │  category + artwork description + poster copy + style + settings
   ▼
prompt_processor.validate_user_input()   → blocks clinical/unsafe/brand terms, warns on claims
   ▼
prompt_processor.build_prompt()          → positive prompt + negative prompt
   ▼
image_generator.WellnessImageGenerator   → Stable Diffusion (Diffusers, PyTorch, GPU/CPU)
   ▼
image_utils                              → poster layout + crisp text, disclaimer footer, PNG bytes, save, ZIP
   ▼
Preview  ──►  Download / Regenerate  ──►  Session Gallery (st.session_state)
```

---

## 2. Features

| Area | What it does |
|---|---|
| **Home page** | Hero banner, feature cards, "how it works", category chips, disclaimer |
| **Categories** | Diabetes Awareness, Heart Health, Mental Health, Healthy Eating, Physical Fitness, Women's Health Awareness, Cancer Awareness, General Wellness + **Custom Category** |
| **Prompt input** | Text area, **💡 Example**, **🎲 Random** (category-aware), **🧹 Clear**, character limit |
| **Styles** | Cartoon, 3D, Flat Vector, Realistic Photography, Minimalist, Watercolor |
| **Generation** | Stable Diffusion via Diffusers, progress bar, 1–4 variations, steps, guidance, seed, poster portrait resolution |
| **Poster layout** | Exact headline and supporting copy are typeset on a designed poster after image generation, keeping key text crisp and readable |
| **Preview** | Large image, category/style chips, user prompt + engineered prompt, **Download PNG**, **Regenerate** |
| **Gallery** | All session images, filter by category, per-image download & delete, **Download all (ZIP)** with a prompt log |
| **Safety** | Blocks clinical imagery, graphic content, pharma brand names; warns on claim words; negative prompt avoids text/logos/pills/needles; optional disclaimer footer on every image |
| **Robustness** | Friendly errors for missing packages, model download failure, GPU out-of-memory, generation failure; CPU fallback |

---

## 3. Model and Hugging Face access

| Model (in sidebar) | Hugging Face repo | Notes |
|---|---|---|
| **Stable Diffusion v1.5 (default)** | `stable-diffusion-v1-5/stable-diffusion-v1-5` | Higher-detail default, supports negative prompts. Slower than Turbo, especially on CPU; several GB download |
| SD-Turbo (fast) | `stabilityai/sd-turbo` | 1–4 steps; fastest option for CPU or quick drafts. Several GB download |

- **No account is required.** Both models are public and download automatically on first use,
  then are cached (`~/.cache/huggingface`).
- **Optional token** (avoids rate limits):
  1. Create a free account at <https://huggingface.co/join>.
  2. Go to **Settings → Access Tokens → New token** (type *Read*), copy it.
  3. Provide it as an environment variable named `HF_TOKEN`:
     - Colab: 🔑 *Secrets* panel → add `HF_TOKEN` → run notebook cell 4.
     - Windows (PowerShell): `$env:HF_TOKEN="hf_xxx"`
     - macOS/Linux: `export HF_TOKEN=hf_xxx`
- **Licences:** each model has its own licence on its Hugging Face page (Stability AI licence for
  SD-Turbo, CreativeML OpenRAIL-M for SD v1.5). Both allow research and educational use, so they are
  fine for a college project — read the licence before any commercial use.

---

## 4. Download the project

1. Download **WellAware-AI.zip** and unzip it. You should see `app.py` at the top level of the
   `WellAware-AI` folder.
2. (Optional) Put it on GitHub: `git init && git add . && git commit -m "WellAware AI"`.

---

## 5. Run on Google Colab (recommended – free GPU)

1. Open <https://colab.research.google.com> → **File → Upload notebook** → choose
   `WellAware_AI_Colab.ipynb` from the project folder.
2. **Runtime → Change runtime type → T4 GPU → Save.**
3. Run the cells in order:
   1. `nvidia-smi` – confirms the GPU.
   2. Upload `WellAware-AI.zip` – it is unzipped to `/content/WellAware-AI`.
   3. `pip install -r requirements.txt`.
   4. (Optional) load `HF_TOKEN`.
   5. `quick_test.py` – downloads the model and shows one test image.
   6. Starts Streamlit in the background.
   7. Starts a **Cloudflare tunnel** and prints a `https://….trycloudflare.com` link → open it.
4. Keep the Colab tab open while you demo. If the link dies, rerun cells 6 and 7.

**Manual Colab commands** (if you prefer a blank notebook):

```python
!unzip -q -o WellAware-AI.zip -d /content
%cd /content/WellAware-AI
!pip install -q -r requirements.txt
!nohup streamlit run app.py --server.port 8501 --server.headless true > /content/streamlit.log 2>&1 &
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared && chmod +x cloudflared
!./cloudflared tunnel --url http://localhost:8501 --no-autoupdate
# Look for the https://xxxx.trycloudflare.com line in the output
```

---

## 6. Run locally in VS Code

**Requirements:** Python 3.9–3.12, about 10 GB free disk, internet for the first model download.
An NVIDIA GPU (4 GB+ VRAM) is recommended; Apple Silicon (M1/M2/M3) uses MPS. CPU works but is
much slower; choose SD-Turbo in the sidebar for quick drafts. The detailed v1.5 model and portrait
poster layout can take several minutes per image on CPU. A GPU or Colab T4 is recommended for
regular poster generation.

1. **Open the folder:** VS Code → *File → Open Folder…* → select `WellAware-AI`.
2. **Open a terminal:** *Terminal → New Terminal*.
3. **Create and activate a virtual environment:**

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Then *Ctrl+Shift+P → Python: Select Interpreter* → choose `.venv`.

4. **Install PyTorch:**
   - **NVIDIA GPU:** go to <https://pytorch.org/get-started/locally/>, pick your OS + *Pip* + a CUDA
     version, and run the command it shows, e.g.
     `pip install torch --index-url https://download.pytorch.org/whl/cu124`
   - **CPU or Mac:** `pip install torch`
5. **Install the rest:** `pip install -r requirements.txt`
6. **(Optional) test from the command line:** `python scripts/quick_test.py`
7. **Run the app:** `streamlit run app.py`
8. Your browser opens <http://localhost:8501>. Stop the app with **Ctrl+C** in the terminal.

---

## 7. Using the app (end to end)

1. Open **WellAware AI** → read the Home page → click **✨ Start creating**.
2. **Select a category** (or *Custom Category* and type a name such as "Hydration Awareness").
3. **Describe the artwork** – or click **💡 Example** / **🎲 Random**.
4. Add an exact **poster headline** and optional supporting copy. This text is typeset on the finished poster rather than drawn by the image model.
5. **Choose a style** (e.g. *Flat Vector Art*).
6. (Optional) **⚙️ Advanced settings:** resolution, variations (1–4), quality steps, guidance,
   fixed seed, disclaimer footer, save to folder.
7. Click **🚀 Generate Image** and watch the progress bar.
   The first run downloads the model (several GB); generation time depends on your hardware.
8. **Preview** the image, open *See the engineered AI prompt*, then **⬇️ Download PNG** or
   **🔄 Regenerate** for a new variation.
9. Open **🖼️ Gallery** to see everything from this session, filter, download, or download all as ZIP.

---

## 8. Prompt engineering

`modules/prompt_processor.py` builds the final prompt in this order (Stable Diffusion's CLIP text
encoder only reads ~77 tokens, so the most important part goes first):

1. **User description** (cleaned and prioritized)
2. **Campaign category** – e.g. `heart health awareness poster illustration`
3. **Style keywords** – e.g. `flat vector illustration, clean geometric shapes…`
4. **Composition and category visual cues** – one focal subject and concise safe scene details
5. **Colour palette** for the cause
6. **Quality tags** – `crisp edges, clean composition, high detail, sharp focus`

A **negative prompt** discourages text, logos, medical equipment, scary/dark content and common
artefacts. Exact poster copy is drawn afterward with fonts, not generated by the diffusion model.
For final artwork, use **Stable Diffusion v1.5** with the default 25 steps; SD-Turbo is a quick
preview model and is more likely to produce soft or inconsistent faces and hands. Keep people
prompts focused on a clear foreground subject and choose **Photographic & Realistic** for photo
style. The image model can still create fake writing or anatomical errors inside the artwork despite
negative prompts. Poster headlines and copy are drawn separately, but generated artwork must still
be reviewed before publication. CPU-only generation is slower and less consistent than a capable GPU.

**Example**

- User: *"Heart health awareness"* · Category: Heart Health · Style: Flat Vector Art
- Readable summary shown in the app: *"A professional and friendly Heart Health awareness campaign
  visual: Heart health awareness. Rendered as flat vector art with warm red, coral and white tones,
  suitable for patient education."*
- Poster headline and supporting copy are placed over the generated illustration as crisp typography.

No medical claims are ever added by the prompt engine.

---

## 9. Safety and content guidelines

- Only **non-clinical** wellness and awareness visuals.
- **Blocked** (generation refused with a clear message): diagnostic imagery (X-ray, MRI, scans),
  treatment/procedure terms (surgery, injection, syringe, dosage, prescription), graphic or unsafe
  content, and major pharmaceutical brand names. Edit the list in `config.BLOCKED_TERMS`.
- **Warned** (generation allowed): claim words such as "cure", "guaranteed", "100%", "miracle".
- The negative prompt discourages text, logos, pills, needles and medical equipment.
- An optional **footer** stamps every image with
  *"AI-generated illustration · Review before publication · Not medical advice"*.
- Disclaimers appear on the Home, Create, Guidelines pages and in the sidebar.

---

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'torch' / 'diffusers'` | Activate your venv, then `pip install -r requirements.txt` (install torch first for GPU). |
| Sidebar says **"Running on CPU"** but you have an NVIDIA GPU | You installed the CPU build of torch. `pip uninstall torch` then reinstall using the CUDA command from pytorch.org. Check with `python -c "import torch; print(torch.cuda.is_available())"`. |
| On Colab, sidebar shows CPU | *Runtime → Change runtime type → T4 GPU*, then rerun all cells. |
| **CUDA out of memory** | Use 512 × 512, 1 variation, SD-Turbo; restart the runtime/app. |
| **Faces or hands look soft/distorted** | Select Stable Diffusion v1.5, set 25 diffusion steps, use 512 × 512, and describe a clear foreground subject. SD-Turbo is intended for drafts. AI images still need review. |
| **Fake words appear inside the artwork** | The poster's typeset copy is separate; fake signs/letters may still come from the image model. Regenerate with a short, text-free scene description and Stable Diffusion v1.5. The model cannot guarantee zero artifacts. |
| **Model download fails / OSError / timeout** | Check internet and disk space (about 10 GB recommended). Retry. Set `HF_TOKEN` if you hit rate limits (HTTP 429). |
| **401 / 403 when downloading** | Set a valid `HF_TOKEN`; if a model page asks you to accept terms, accept them on huggingface.co while logged in. |
| First generation takes several minutes | Normal – the model is downloading. Later runs are fast. |
| Images are black (Mac) | The app already uses float32 on MPS; update `torch` and `diffusers`. |
| Images look repeated/stretched at 768 px | Use the model's native 512 × 512 size; 768 px generation can reduce quality or exceed available memory. |
| Colab link not opening / "502" | Wait 10 s and refresh; check `!tail -n 40 /content/streamlit.log`; rerun cells 6–7. |
| localtunnel asks for a password | Enter the IP printed by `curl ipv4.icanhazip.com` in the same notebook. |
| `streamlit: command not found` | Use `python -m streamlit run app.py`. |
| Port 8501 already in use | `streamlit run app.py --server.port 8502` |
| Form values or gallery disappeared | The gallery lives in the browser session; refreshing the page starts a new session. Saved PNGs remain in `generated_images/`. |
| "Please remove: …" error | Your description contains a blocked clinical/unsafe/brand term – rephrase it as a lifestyle/wellness scene. |

---

## 11. Sample campaign prompts for testing

| Category | Style | Prompt |
|---|---|---|
| General Wellness | Flat Vector Art | Create a colorful and friendly health awareness illustration showing a person practicing yoga, eating healthy food, and maintaining a balanced lifestyle. |
| Heart Health | Cartoon Illustration | A father and daughter jogging together in the park on a bright morning. |
| Diabetes Awareness | Watercolor Illustration | An elderly couple taking a morning walk through a green park with a bowl of fresh fruit on a picnic blanket. |
| Mental Health | Minimalist Design | A calm young adult meditating by a lake at sunrise, surrounded by soft clouds. |
| Healthy Eating | Realistic Photography | A vibrant rainbow of fruits and vegetables arranged in bowls on a wooden table. |
| Physical Fitness | 3D Illustration | A diverse group of adults doing an outdoor yoga session in a park at sunrise. |
| Women's Health Awareness | Watercolor Illustration | A group of confident women of different ages walking together holding flowers. |
| Cancer Awareness | Flat Vector Art | A large pink awareness ribbon made of flowers in a peaceful garden. |
| Custom: Hydration Awareness | Cartoon Illustration | A cheerful student refilling a water bottle at a fountain on a sunny campus. |
| *(Safety demo – should be blocked)* | any | Show an X-ray of a patient's lungs with a syringe. |

More suggestions are in the app under **🛡️ Guidelines & Help → Sample prompts** (click *Use*).

---

## 12. Suggested demo flow for evaluation (≈5 minutes)

1. Show the **Home page** and explain the problem and architecture.
2. **Create Campaign:** Heart Health → 🎲 Random → Cartoon → Generate.
3. Open **"See the engineered AI prompt"** to explain prompt engineering.
4. Set **2 variations** → Generate; then **Regenerate**; download a PNG.
5. Try a **Custom Category** with a different style.
6. Enter the **safety demo prompt** to show the validation message.
7. Open the **Gallery**, filter by category and **Download all (ZIP)**.

---

## 13. Limitations and future work

- Diffusion models can draw odd hands/faces; review the artwork before publication. Poster headline
  and supporting copy are typeset separately to avoid generated-text blur.
- The gallery is per browser session (not a database).
- Future ideas: image-to-image editing, adding campaign logo overlays, multilingual prompts,
  SDXL for higher resolution, user accounts with saved projects.

---

## 14. Tech stack

Python · Streamlit · Stable Diffusion · Hugging Face Diffusers · PyTorch · Transformers ·
Accelerate · Pillow · Google Colab / VS Code
