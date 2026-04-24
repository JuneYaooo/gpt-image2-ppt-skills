<div align="center">

# gpt-image2-ppt-skills

**Generate visually striking PPT decks with OpenAI `gpt-image-2` in one shot.**

A Claude Code / OpenClaw Skill. Once installed in your agent, a single natural-language prompt yields 16:9 high-res images + a keyboard-navigable HTML viewer + a ready-to-send `.pptx` — or clones any reference `.pptx` template and reskins it with new content.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](../LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://www.anthropic.com/claude-code)
[![gpt-image-2](https://img.shields.io/badge/OpenAI-gpt--image--2-black.svg)](https://platform.openai.com/docs/guides/images)

🌐 **中文** → [../README.md](../README.md)

</div>

---

## 🎬 Demo: feed one template, get a fresh deck in that style

<table>
<tr>
<th width="50%">Input: any reference template (.pptx / image)</th>
<th width="50%">Output: cloned layout + new content</th>
</tr>
<tr>
<td><img src="assets/template-demo-input.jpg" width="100%" alt="input template"></td>
<td><img src="assets/template-demo-output.jpg" width="100%" alt="generated output"></td>
</tr>
<tr>
<td align="center"><sub>English infographic template (Mass Media Infographics)</sub></td>
<td align="center"><sub>Same layout / palette / illustration vocabulary, content swapped to "how normal people make AI-powered social content"</sub></td>
</tr>
</table>

---

## ✨ What it does

- 🎨 **10 curated styles** — Spatial Glass / Tech Blue / Editorial Mono / Dark Aurora / Risograph / Wabi / Swiss Grid / Hand Sketch / Y2K Chrome / Vector Illustration, each with `cover` / `content` / `data` composition rules
- 🪄 **Template-clone mode** — drop in any `.pptx` and the skill auto-renders it, asks a vision model to extract style + JSON Schema, then reproduces the layout with your new content (like the demo above)
- 🎮 **HTML viewer + `.pptx`, both shipped** — arrow-key navigation / space to autoplay / ESC fullscreen / swipe on touch, plus a 16:9 `.pptx` you can send as-is
- ⚡ **10-way concurrency by default** — a 10-page deck finishes in ~30s
- 🔁 **Two backends** — `openai` direct (needs key) or `codex` CLI (reuses your codex login, no key configured in this skill)
- 🤖 **Official OpenAI Images API** — model `gpt-image-2`; `base_url` can point at any OpenAI-compatible relay

## 🎨 The 10 built-in styles

> Below: the 10 styles each generating one cover under the same topic — "**How to make a PPT with gpt-image-2**". All covers are raw `gpt-image-2` output, no PS.

![10 styles · same topic, raw gpt-image-2 output](assets/style-gallery.jpg)

| Style ID | One-liner | Use cases |
| --- | --- | --- |
| `gradient-glass` | Apple Vision OS / Spatial Glass | AI product launches, technical talks, creative pitches |
| `clean-tech-blue` | Stripe / Linear-grade blue & white | Investor decks, business plans, corporate strategy |
| `vector-illustration` | Retro vector + black outlines | Education, brand storytelling, community sharing |
| `editorial-mono` | Kinfolk / Monocle editorial | Brand reveals, cultural interviews, book talks |
| `dark-aurora` | Linear / Vercel dark neon | AI products, dev tools, technical talks |
| `risograph` | Riso 2-spot-color print + halftone | Creative studios, indie zines, design agencies |
| `japanese-wabi` | Muji / Hara Kenya wabi-sabi | Tea ceremony, lifestyle, luxury, cultural lectures |
| `swiss-grid` | Bauhaus / Vignelli international grid | Academic reports, museum exhibits, serious dashboards |
| `hand-sketch` | Sketchnote / whiteboard | Workshops, product brainstorming, training |
| `y2k-chrome` | Y2K liquid chrome + butterfly stickers | Streetwear, entertainment, brand collabs, Gen-Z marketing |

---

## 🚀 Install

### Option 1: let your AI install it (recommended)

Paste this prompt into your AI assistant (Claude Code / OpenClaw / Codex / Cursor / Trae / Hermes Agent — all work) and it will handle the install:

```
Please install gpt-image2-ppt-skills for me:
https://raw.githubusercontent.com/JuneYaooo/gpt-image2-ppt-skills/main/docs/install.md
```

The agent will clone the repo, run the install script, ask you for an API key, and tell you to restart.

### Option 2: manual install

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh
```

The script installs the skill to `~/.claude/skills/gpt-image2-ppt-skills/`; Claude Code picks it up after restart.

Then drop in one key and you're ready:

```bash
# ~/.claude/skills/gpt-image2-ppt-skills/.env
OPENAI_BASE_URL=https://api.openai.com    # or any OpenAI-compatible relay
OPENAI_API_KEY=sk-...                     # required
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto
```

> 🔒 **Won't accidentally eat your secrets**: only loads `.env` from the skill's own directory or an explicit `GPT_IMAGE2_PPT_ENV` path. It does **not** walk up into project directories.
>
> 🪄 Template-clone mode additionally needs native `libreoffice` or the docker `linuxserver/libreoffice` image (to render `.pptx` → PNG).

---

## 🛠 How to use inside Claude Code

Once installed, just say it in plain English:

> Use **gpt-image2-ppt** to make a 5-slide deck about **[your topic]**, style = `dark-aurora`.

Template clone, same shape:

> I have a `company-template.pptx` — make a 5-slide deck about **[your topic]** using that template.

Claude will write the `slides_plan`, generate a cover first for you to approve, then run the full deck and hand back the HTML viewer + `.pptx` paths.

> 🧑‍💻 Prefer to call the CLI yourself instead of going through an agent? See [`SKILL.md`](../SKILL.md) — CLI flags and file layout live there.

---

## 🙏 Acknowledgements

- [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) — original author of the style prompts and viewer template. This project swaps the image backend from Nano Banana Pro to OpenAI gpt-image-2, rewrites the 3 inherited styles and adds 7 new ones (10 total), and layers on template-clone mode (vision-based style extraction from any user `.pptx`), an md-first authoring flow, automatic `.pptx` packaging, and a codex CLI fallback backend.
- [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) — reference for the Claude Code skill `SKILL.md` frontmatter.

## License

Apache License 2.0 — see [LICENSE](../LICENSE).
