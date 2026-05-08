---
name: gpt-image2-ppt
description: Generate image-based presentation decks from a topic, outline, or PPTX template using OpenAI-compatible image models, then package PNG slides into an HTML viewer and 16:9 PPTX.
---

# GPT Image2 PPT

## Description

Use this skill to create visually designed slide decks. It turns a reviewed Markdown slide plan into JSON, generates one 16:9 PNG per slide through an OpenAI-compatible image model, builds a keyboard-friendly HTML viewer, and packages the images into a PowerPoint file. It also supports template clone mode when the user provides a `.pptx` template or rendered template images.

## When to Use

- The user asks to make a PPT, presentation, slide deck, pitch deck, report deck, or visual courseware.
- The user provides a topic or outline and wants a polished visual deck.
- The user provides a `.pptx` template and wants new content in a similar style.
- The user wants HTML preview plus `.pptx` output from generated slide images.

## Prerequisites

- Runtime environment variables:
  - `OPENAI_API_KEY`: required for direct API generation.
  - `OPENAI_BASE_URL`: optional; defaults to `https://api.openai.com`. May include `/v1`.
  - `GPT_IMAGE_MODEL_NAME`: optional; defaults to `gpt-image-2`.
  - `GPT_IMAGE_ENDPOINT`: optional; `auto`, `images`, or `chat`.
  - `GPT_IMAGE_QUALITY`: optional; `low`, `medium`, `high`, or `auto`.
- Python packages: `requests`, `python-dotenv`, `python-pptx`, `jsonschema`, `pymupdf`.
- Template rendering requires LibreOffice or pre-rendered PNG images.
- Never place a real API key in this skill file, source files, or published marketplace content.

## Workflow

1. Ask the user for topic/content, page count, audience, style preference or template file, and whether to run `--slides 1` first.
2. Create `slides_plan.md` as the source of truth. Use this heading format:

   ```markdown
   ---
   title: Deck Title
   ---

   ## 1. [cover] Cover title
   Subtitle: ...

   ## 2. [content] Slide title
   - Point one
   - Point two

   ## 6. [data] Key result
   Metric: ...
   ```

3. Let the user review the Markdown plan before converting it.
4. Convert the plan:

   ```bash
   python {baseDir}/scripts/md_to_plan.py slides_plan.md -o slides_plan.json
   ```

5. For a built-in style deck, choose one style file from `{baseDir}/references/`:

   - `gradient-glass.md`
   - `clean-tech-blue.md`
   - `vector-illustration.md`
   - `editorial-mono.md`
   - `dark-aurora.md`
   - `risograph.md`
   - `japanese-wabi.md`
   - `swiss-grid.md`
   - `hand-sketch.md`
   - `y2k-chrome.md`

6. Run a one-slide smoke test when appropriate:

   ```bash
   python {baseDir}/scripts/generate_ppt.py \
     --plan slides_plan.json \
     --style {baseDir}/references/clean-tech-blue.md \
     --slides 1 \
     --concurrency 1
   ```

7. Run the full deck:

   ```bash
   python {baseDir}/scripts/generate_ppt.py \
     --plan slides_plan.json \
     --style {baseDir}/references/clean-tech-blue.md
   ```

8. For template clone mode, add template flags:

   ```bash
   python {baseDir}/scripts/generate_ppt.py \
     --plan slides_plan.json \
     --template-pptx ./template.pptx \
     --template-strict \
     --slides 1
   ```

9. Report the generated output directory, `index.html`, `.pptx`, and any failed slides.

## Output Format

After generation, respond with:

```text
Style/template: <style id or template filename>
Slides: <generated>/<requested>
Output directory: <path>
HTML viewer: <path>/index.html
PPTX: <path>/<deck>.pptx
Warnings: <API fallback, text-legibility note, layout-reuse note, or none>
```

## Examples

### Built-in Style

User: "帮我做一份 6 页 AI 客服产品发布 PPT，偏科技蓝。"

Action:

1. Draft `slides_plan.md`.
2. Convert with `md_to_plan.py`.
3. Use `{baseDir}/references/clean-tech-blue.md`.
4. Run `--slides 1`, then full generation after approval.

### Template Clone

User: "按这个公司模板，做一份 8 页投融资路演。"

Action:

1. Render or locate template PNGs.
2. Draft a plan with suitable `layout=` hints when needed.
3. Run `generate_ppt.py --template-pptx ./company-template.pptx --template-strict --slides 1`.
4. Inspect layout reuse warnings before full generation.
