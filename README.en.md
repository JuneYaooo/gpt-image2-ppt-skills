# gpt-image2-ppt-skills

> Generate visually striking PPT slides with OpenAI's official `gpt-image-2` Images API; ships an instant keyboard-navigable HTML viewer + a 16:9 .pptx file. Works as a Claude Code Skill or an OpenClaw Skill.

🌐 **中文** > [README.md](./README.md)

## ✨ Highlights

- 🎨 **10 curated styles**: Spatial Glass / Tech Blue / Retro Vector / Editorial Mono / Dark Aurora / Risograph / Japanese Wabi / Swiss Grid / Hand Sketch / Y2K Chrome -- each with cover/content/data composition rules
- 🪄 **Template-clone mode**: feed any `.pptx`, the skill auto-renders + asks vision to extract style + JSON Schema, then produces new content in that template's look
- 🤖 **Official OpenAI Images API**: model `gpt-image-2`
- 🔄 **OpenAI-compatible**: point `base_url` at any compatible relay
- 🖼 **16:9 high-res**: 1536x1024 default, `quality=high`
- 🎮 **HTML viewer**: arrow-key navigation, space to autoplay, ESC fullscreen, swipe on touch
- 🧩 **Per-slide iteration**: `--slides 1,3,5` regenerates only those pages, completed PNGs are skipped automatically

## 🚀 One-line install

### As a Claude Code skill

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh
```

After installation the skill lives at `~/.claude/skills/gpt-image2-ppt-skills/` and Claude Code picks it up after restart.

### As an OpenClaw skill (via ClawHub)

```bash
clawhub install gpt-image2-ppt
# installed to <cwd>/skills/gpt-image2-ppt/
```

## ⚙ Configuration

Edit `~/.claude/skills/gpt-image2-ppt-skills/.env` (or `skills/gpt-image2-ppt/.env` for OpenClaw):

```bash
OPENAI_BASE_URL=https://api.openai.com    # or any OpenAI-compatible relay
OPENAI_API_KEY=sk-...                     # required
GPT_IMAGE_MODEL_NAME=gpt-image-2          # default
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto

# Optional: only required for template-clone mode (independent vision provider).
# No default endpoint is shipped -- supply your own trusted endpoint, or leave
# VISION_* unset to disable template-clone mode entirely.
# VISION_BASE_URL=https://your-openai-compatible-relay.example.com/v1
# VISION_API_KEY=sk-...
# VISION_MODEL_NAME=gemini-3.1-pro-preview
```

> Security: the script only loads `.env` from `<script_dir>/.env`, `~/.claude/skills/.../env`, `~/skills/.../env`, or an explicit `GPT_IMAGE2_PPT_ENV` path. It does **not** walk parent directories, so it cannot accidentally pick up unrelated project secrets.

## 📝 Usage

### 1. Author a `slides_plan.json`

```json
{
  "title": "My deck",
  "slides": [
    {"slide_number": 1, "page_type": "cover",   "content": "Title: xxx\nSubtitle: yyy"},
    {"slide_number": 2, "page_type": "content", "content": "Three bullet points..."},
    {"slide_number": 3, "page_type": "data",    "content": "Comparison numbers..."}
  ]
}
```

`page_type` is one of `cover` / `content` / `data` -- drives the per-page composition.

### 2. Pick a style and generate

```bash
# Full deck
python3 generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md

# Smoke test slide 1 only (cheap API check)
python3 generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 1

# Re-render only slides 3 and 5
python3 generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 3,5
```

### 2.5 Clone the user's own .pptx template

```bash
# One-liner: auto-render + vision-analyse + image generation.
# Needs LibreOffice locally OR docker with linuxserver/libreoffice
python3 generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-strict

# Explicit images dir (when you ran render_template.py manually or curated PNGs yourself)
python3 generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-images ./template_renders/company-template \
  --template-strict

# Force vision re-analysis (default reads template_cache/<sha256>.json)
python3 generate_ppt.py ... --rebuild-template-cache
```

`--template-strict` passes the matching template page as an image reference to gpt-image-2 -> highest fidelity.

If `--template-images` is omitted the skill auto-invokes `render_template.py` with this priority: native `libreoffice` -> `docker run linuxserver/libreoffice` -> instructive error asking the user to export PNGs manually. PDF->PNG goes through `pymupdf` (already in requirements).

The first vision pass calls `gemini-3.1-pro-preview` (configured in `.env` `VISION_*`), produces per-page `summary` + `json_schema`, caches to `template_cache/`. Subsequent runs against the same template are a cache hit.

#### Where intermediates land

| Path | Content |
| --- | --- |
| `<cwd>/template_renders/<stem>/page-NN.png` | LibreOffice-rendered PNGs |
| `<cwd>/template_renders/<stem>/_source.pdf` | LibreOffice intermediate (kept for inspection) |
| `<cwd>/template_cache/<sha256>.json` | vision style profile cache |
| `<cwd>/outputs/<timestamp>/` | per-run outputs |

Add these three directories to your project's `.gitignore`.

#### Layout reuse policy

The principle: **1 page : 1 layout, by default.** Vision tags every layout with `reuse_friendly`:

| `reuse_friendly` | Typical layouts | Cost of repeating |
| --- | --- | --- |
| `false` ((!) strong warning) | Cover / character illustrations / unique scene art / multi-step flows with per-step icons / novelty data centerpieces | Visually obvious repetition, audience confusion |
| `true` ((i) soft hint) | Plain text / card grids / generic lists / section headers | Tolerable, but wastes the template's other distinctive layouts |

`generate_ppt.py` runs a reuse check before dispatching image generation jobs and prints suggested alternatives. The check never blocks execution.

### 3. Inspect the output

```
outputs/20260422_153012/
|---- images/
|   |---- slide-01.png
|   |---- slide-02.png
|   \---- ...
|---- index.html       # open in browser -> arrow-key navigation
|---- prompts.json     # full prompts used for each slide (for replay & tuning)
\---- <title>.pptx     # 16:9 deck with images filling each slide
```

## 🎨 The 10 built-in styles

| Style ID | One-liner | Use cases |
| --- | --- | --- |
| `gradient-glass` | Apple Vision OS / Spatial Glass | AI product launches, technical talks, creative pitches |
| `clean-tech-blue` | Stripe / Linear-grade blue & white | Investor decks, business plans, corporate strategy |
| `vector-illustration` | Retro vector + black outline | Education, brand storytelling, community sharing |
| `editorial-mono` | Kinfolk / Monocle editorial design | Brand reveals, cultural interviews, book talks |
| `dark-aurora` | Linear / Vercel dark neon | AI products, dev tools, technical talks |
| `risograph` | Riso 2-spot-color print + halftone | Creative studios, indie zines, design agencies |
| `japanese-wabi` | Muji / Hara Kenya wabi-sabi | Tea ceremony, lifestyle brands, luxury, cultural lectures |
| `swiss-grid` | Bauhaus / Vignelli international style grid | Academic reports, museum exhibits, serious dashboards |
| `hand-sketch` | Sketchnote / whiteboard | Workshops, product brainstorming, training |
| `y2k-chrome` | Y2K liquid chrome + butterfly stickers | Streetwear, entertainment, brand collabs, Gen-Z marketing |

Each style file is at `styles/<id>.md` and includes cover / content / data composition rules.

## 🛠 Use it inside Claude Code (or OpenClaw)

Just say:

> Make me a 5-slide deck about [topic] using gpt-image2-ppt, style = clean-tech-blue.

The agent will:
1. Ask clarifying questions about content, audience, page count
2. Author `slides_plan.json`
3. Run `generate_ppt.py --slides 1` for a cover smoke test
4. After approval, generate the full deck and hand back the viewer + .pptx paths

## 📦 Dependencies

- Python 3.8+
- `pip install -r requirements.txt` covers everything (`requests` / `python-dotenv` / `python-pptx` / `jsonschema` / `pymupdf`)
- Template-clone mode additionally needs: native `libreoffice` OR docker with `linuxserver/libreoffice`

## 🙏 Acknowledgements

- [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) -- original style prompts + viewer; this project swaps the image backend from Nano Banana Pro to OpenAI gpt-image-2 and rewrites all 3 inherited styles + adds 7 new ones.
- [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) -- reference for Claude Code skill SKILL.md frontmatter.

## License

Apache License 2.0.
