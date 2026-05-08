# GPT Image2 PPT

## Overview

GPT Image2 PPT is an expert for turning a topic, outline, or existing deck template into a visually strong presentation. It plans slide copy first, then uses OpenAI-compatible image generation models such as `gpt-image-2` to render each slide as a 16:9 image, assemble a keyboard-friendly HTML viewer, and package the images into a `.pptx` file.

## Core Capabilities

### Presentation Planning
- Converts rough ideas into slide-by-slide Markdown plans with clear page types such as cover, content, and data.
- Keeps `slides_plan.md` as the human-editable source of truth and derives `slides_plan.json` only after the content is approved.
- Adapts structure for pitch decks, product explainers, education decks, strategy reports, and visual storytelling.

### Visual Slide Generation
- Uses curated styles including Spatial Glass, Clean Tech Blue, Editorial Mono, Dark Aurora, Risograph, Wabi, Swiss Grid, Hand Sketch, Y2K Chrome, and Retro Vector.
- Generates full-slide 16:9 PNG images, then creates an HTML viewer and `.pptx` deck.
- Supports OpenAI-compatible relays through configurable `OPENAI_BASE_URL`, model name, quality, and endpoint mode.

### Template Clone Mode
- Renders user-provided `.pptx` templates into PNG references when LibreOffice or a compatible renderer is available.
- Analyzes template layout, style, colors, and reuse risk, then maps new content onto suitable template pages.
- Can run a one-slide smoke test before a full deck to reduce cost and iteration time.

## Key Rules

- Never store, publish, or reveal API keys. Use session-scoped environment variables or a local `.env` file that is not committed.
- Ask for content, audience, style/template preference, and smoke-test preference before starting an expensive generation run.
- Prefer a one-slide smoke test before full generation unless the user explicitly asks to run all slides immediately.
- Preserve editable source copy in Markdown and treat generated JSON, images, HTML, and PPTX as derived outputs.
- Clearly report generated artifact paths and any failed slide numbers.

## Limitations

- Image models may render small text imperfectly; important numbers and labels should be reviewed by the user.
- API cost, latency, available models, and endpoint behavior depend on the configured provider or relay.
- Template clone mode requires either rendered template images or a local renderer such as LibreOffice.
- The expert creates image-based slides, so the final `.pptx` is presentation-ready but not fully text-editable.
