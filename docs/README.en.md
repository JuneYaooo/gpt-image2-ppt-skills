<div align="center">

# gpt-image2-ppt-skills

**Generate design-forward, highly polished PPT decks with OpenAI `gpt-image-2` in one shot.**

Works natively in Claude Code, Codex, OpenClaw, Hermes, and any other Skill-compatible agent. Once installed in your agent, a single natural-language prompt yields 16:9 high-res images + a ready-to-send `.pptx` — or clones any reference `.pptx` template and reskins it with new content.

**Possibly one of the best-looking AI PPT Skills available today.** Instead of filling text into traditional templates, it uses the visual taste, composition, and layout strengths of `gpt-image-2` to generate each slide as a complete visual composition, aiming for decks that look polished, consistent, and presentation-ready from cover to inner pages.

The project also includes dedicated optimization for editing image-based PPTs. You can describe the target slide and element in natural language, and the system regenerates that slide through image-to-image editing while trying to preserve the original style and layout. One important caveat: the background and text in these PPTs are full-slide images. If your workflow depends on manually editing native PowerPoint text boxes and individual objects, this may not be the right fit.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](../LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://www.anthropic.com/claude-code)
[![gpt-image-2](https://img.shields.io/badge/OpenAI-gpt--image--2-black.svg)](https://platform.openai.com/docs/guides/images)
[![GitHub stars](https://img.shields.io/github/stars/JuneYaooo/gpt-image2-ppt-skills?style=flat)](https://github.com/JuneYaooo/gpt-image2-ppt-skills/stargazers)

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

- 🎨 **10 curated styles + an expanded style library** — built-ins include Spatial Glass / Tech Blue / Editorial Mono / Dark Aurora / Risograph / Wabi / Swiss Grid / Hand Sketch / Y2K Chrome / Vector Illustration; on 2026-05-26, 22 additional high-quality styles were selected from 500+ publicly available PPT templates
- 🧭 **Prompt Recipes** — `examples/` provides starter `slides_plan.md` templates for common scenarios such as product launches, investor pitches, weekly reports, courseware, thesis defenses, and book talks
- 🪄 **Template-clone mode** — drop in any `.pptx`; the agent follows its layout, palette, and illustration language, then swaps in your new content
- 🎯 **Precise natural-language edits** — say "change slide 3's subtitle", "remove the footer", or "replace these three metrics"; the agent regenerates only the target slide through image-to-image editing while trying to preserve the original style and layout
- 🎮 **Dual output** — high-res PNG per slide + 16:9 `.pptx` ready to use
- ⚡ **10-way concurrency by default** — a 10-page deck finishes in ~30s
- 🧪 **Preview one slide first** — approve the cover before generating the full deck
- 🧾 **Trackable edits** — changed slides and generated versions can be traced and rolled back

## ✅ Best-fit use cases

| Use case | Fit | Notes |
| --- | --- | --- |
| Generate a new deck from a topic | Strong | Good for reports, pitches, training, courses, product intros. |
| Create a new deck from a company template | Strong | Provide a `.pptx`, approve one cover first, then run the full deck. |
| Edit titles, subtitles, dates, footers | Strong | The most stable editing scenario. |
| Update metric cards and key numbers | Good | Works, but every number must be checked before delivery. |
| Modify only one slide in a multi-slide deck | Good | The target slide is regenerated; other slides are left alone. |
| Dense tables, financial reports, legal long copy | Weak | Small text and numbers need strict human review. |

If the user only has a rough topic and no complete outline yet, the agent can first consult [`examples/`](../examples/) to draft a scenario-appropriate `slides_plan.md`, ask for confirmation, then convert it to `slides_plan.json` and continue with generation.

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

## 🧬 Expanded style library: 22 new styles added on 2026-05-26

On 2026-05-26, we added 22 high-quality styles selected from 500+ publicly available PPT templates. More styles will continue to be added, and good PPT template or style references are welcome.

See the full style table, thumbnails, style IDs, visual traits, and use cases in [`distilled-styles.md`](./distilled-styles.md).

---

## 🧪 Editing Capability Report

If you care about "how reliable are edits in real scenes", see the user-facing case report:

- **[`docs/edit_guide.md`](./edit_guide.md)** — title replacement, date edits, footer removal, metric updates, logo insertion, single-slide edits in a multi-slide deck, current limitations, and a delivery checklist

Summary:

| Capability | Current behavior |
| --- | --- |
| Short text edits | Stable for everyday delivery. |
| Multiple explicit edits | Works best when the user clearly says what should stay unchanged. |
| Metric slides | Works, but numbers must be checked. |
| Small icon / logo insertion | Works for style-matched icons; real brand logos need source assets. |
| Native PowerPoint object editing | Not supported; output PPTX uses full-slide images. |

<details>
<summary>Developer note: internal editing mechanism diagram</summary>

<img src="assets/architecture_cn.jpg" width="100%" alt="system architecture">

</details>

---

## 🚀 Install

### Option 1: let your AI install it (recommended)

Paste this prompt into your AI assistant (Claude Code / OpenClaw / Codex / Cursor / Trae / Hermes Agent, or any other agent that supports Skills) and it will handle the install:

```
Please install gpt-image2-ppt-skills for me:
https://raw.githubusercontent.com/JuneYaooo/gpt-image2-ppt-skills/main/docs/install.md
```

The agent will clone the repo, run the install script, ask for an API key only when direct API mode is needed, and tell you to restart.

### Option 2: manual install

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh --target claude   # Claude Code
# or
bash install_as_skill.sh --target codex    # Codex
```

The script installs the skill into the selected agent directory:

- Claude Code: `~/.claude/skills/gpt-image2-ppt-skills/`
- Codex: `~/.codex/skills/gpt-image2-ppt-skills/`

If you use direct API mode, inject environment variables through your agent
framework instead of writing secrets into the caller project's root `.env`:

- Claude Code: user-level `~/.claude/settings.json`, or project-level `.claude/settings.local.json`
- OpenClaw / custom agents: reference system env vars from `apiKey` / env config
- CI / servers: system env vars, Docker Compose, Kubernetes Secrets, or CI Secrets
- Standalone CLI: set `GPT_IMAGE2_PPT_ENV=/path/to/private.env`, or use the skill install directory `.env` as a fallback

```bash
# Variable names:
OPENAI_BASE_URL=https://api.openai.com    # or any OpenAI-compatible relay
OPENAI_API_KEY=sk-...                     # required
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto
```

> In **Codex**, if the current agent has native image generation, use the native path in `SKILL.md` and skip `OPENAI_API_KEY`.
>
> 🔒 **Won't accidentally eat your secrets**: the script only reads the current process env, platform-injected variables, an explicit `GPT_IMAGE2_PPT_ENV`, and the skill install directory `.env` fallback. It does **not** walk up into caller project directories.
>
> 🪄 Template-clone mode additionally needs an executable PPTX renderer: Windows PowerPoint, macOS Keynote, or LibreOffice. Run `python3 scripts/render_template.py --check` first; HarmonyOS / Termux / containers / unusual architectures should not assume Linux aarch64 LibreOffice binaries are runnable.

### Vision analysis for template clone (optional)

In template-clone mode, the skill needs to "see" your `.pptx` template's visual style first. **If your AI assistant is already multimodal** (Claude Code with Claude Opus/Sonnet, Codex with GPT multimodal, etc.), the agent will analyze the visual style directly and generate a `template_profile.json` with `reference_image` to pass to the CLI with `--template-profile`. **No extra configuration needed.**

Only when your agent uses a text-only model (e.g., DeepSeek text model), you'll need the following env vars to use a separate multimodal model for template analysis:

```bash
# Optional: vision analysis for template clone (only needed by text-only agents; skip for multimodal agents)
VISION_BASE_URL=https://your-openai-compatible-relay.example.com/v1
VISION_API_KEY=sk-...
VISION_MODEL_NAME=gemini-3.1-pro-preview   # or gpt-4o / claude-3.5-sonnet, any multimodal SKU
```

> Supports any multimodal model compatible with the OpenAI `/v1/chat/completions` format (Gemini / GPT-4o / Claude, etc.). Fully decoupled from `gpt-image-2` — switching the vision provider won't affect image generation.

---

## 🛠 How to use inside Claude Code

Once installed, just say it in plain English:

> Use **gpt-image2-ppt** to make a 5-slide deck about **[your topic]**, style = `dark-aurora`.

Template clone, same shape:

> I have a `company-template.pptx` — make a 5-slide deck about **[your topic]** using that template.

Claude will write the `slides_plan`, generate a cover first for you to approve, then run the full deck and hand back the `.pptx` path.

> Prefer to call the CLI yourself instead of going through an agent? See [`SKILL.md`](../SKILL.md) — CLI flags and file layout live there.

---

## 🙏 Acknowledgements

- [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) — reference for the original style prompts and early skill structure. This project swaps the image backend from Nano Banana Pro to OpenAI gpt-image-2, rewrites the 3 inherited styles and adds 7 new ones (10 total), and layers on template-clone mode (vision-based style extraction from any user `.pptx`), an md-first authoring flow, automatic `.pptx` packaging, and a codex CLI fallback backend.
- [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) — reference for the Claude Code skill `SKILL.md` frontmatter.

## 💬 Community

[**LINUX DO — Chinese Developer Community**](https://linux.do/)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JuneYaooo/gpt-image2-ppt-skills&type=Date)](https://star-history.com/#JuneYaooo/gpt-image2-ppt-skills&Date)

---

## License

Apache License 2.0 — see [LICENSE](../LICENSE).
