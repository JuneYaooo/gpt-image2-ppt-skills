# Expert Behavioral Rules

## Core Workflows

### Built-in Style Deck

1. Ask for the deck topic, approximate page count, target audience, preferred style, and whether to run a one-slide smoke test.
2. Draft `slides_plan.md` with page numbers, page types, titles, and concise slide content.
3. Ask the user to confirm or revise the slide copy before converting it.
4. Convert Markdown to JSON with `python {baseDir}/scripts/md_to_plan.py slides_plan.md -o slides_plan.json`.
5. Generate one slide first when smoke testing is requested.
6. Generate the full selected slide set with `python {baseDir}/scripts/generate_ppt.py --plan slides_plan.json --style {baseDir}/references/<style>.md`.
7. Report the output directory, `index.html`, `.pptx`, and any failed slides.

### Template Clone Deck

1. Ask the user for a `.pptx` template and the new deck topic/content.
2. Render or locate template PNG images before analysis.
3. Prefer one unique template layout per new slide and avoid reusing layouts marked not reusable.
4. Add `layout=<layout-id>` in `slides_plan.md` when the user wants precise mapping.
5. Run a one-slide smoke test with `--template-pptx`, `--template-images` if available, and `--template-strict` when high fidelity is desired.
6. Continue to the full deck only after the user accepts the direction or explicitly skips review.

### Credential Handling

1. Check whether `OPENAI_API_KEY` is available in the current runtime environment.
2. If missing, ask the user to provide a key for this session or to set `GPT_IMAGE2_PPT_ENV` to a local env file.
3. Never print, summarize, store in committed files, or include credentials in marketplace content.
4. If the provider base URL includes `/v1`, keep it as-is; the scripts normalize endpoint paths.

## Output Standards

When generation completes, answer with:

- Style or template used.
- Number of slides requested and generated.
- Output directory.
- HTML viewer path.
- PPTX path if created.
- Any warnings about text legibility, layout reuse, API fallback, or failed slides.

## Interaction Rules

- Ask only the minimum questions needed before a run, but do ask before spending image-generation credits.
- Use the user's preferred language for slide copy and status updates.
- Prefer built-in style generation for fast first drafts and template clone mode when the user cares about brand fidelity.
- Do not promise exact visual reproduction; describe template mode as high-fidelity adaptation.

## Skill Routing

| User Intent | Recommended Skill |
|-------------|-------------------|
| Make slides from a topic or outline | `gpt-image2-ppt` |
| Generate a pitch deck or product deck | `gpt-image2-ppt` |
| Turn an existing `.pptx` into a new deck with similar style | `gpt-image2-ppt` |
| Package generated slide images into PowerPoint | `gpt-image2-ppt` |

## Safety & Compliance

- Never publish API keys, bearer tokens, user private files, or template assets without explicit permission.
- Warn before running a large generation job because image-generation calls may consume paid credits.
- Keep generated outputs in the user's working directory and avoid overwriting existing deck artifacts unless asked.
