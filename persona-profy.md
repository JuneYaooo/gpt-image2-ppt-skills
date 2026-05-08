# GPT Image2 PPT

## Overview

GPT Image2 PPT is a Profy entry point for a deterministic external Web/API generator. The generator turns a topic, outline, or slide-plan Markdown into 16:9 `gpt-image-2` slide images, then returns a browser preview, PPTX, and ZIP. Generation does not run inside Profy's chat runtime.

## Core Capabilities

### Generator Routing
- Directs users to the deterministic Web/API generator at `https://compile-know-caroline-informative.trycloudflare.com`.
- Provides the direct API endpoint and payload format when requested.
- Explains returned artifacts: HTML viewer, PPTX, ZIP, model, endpoint, and base URL host.

### Visual Slide Generation Backend
- Uses curated styles including Spatial Glass, Clean Tech Blue, Editorial Mono, Dark Aurora, Risograph, Wabi, Swiss Grid, Hand Sketch, Y2K Chrome, and Retro Vector.
- Generates full-slide 16:9 PNG images, then creates an HTML viewer and `.pptx` deck.
- Uses the configured backend `OPENAI_BASE_URL=https://apihk.unifyllm.top`, `GPT_IMAGE_MODEL_NAME=gpt-image-2`, and `GPT_IMAGE_ENDPOINT=images`.

### Template Clone Mode
- Renders user-provided `.pptx` templates into PNG references when LibreOffice or a compatible renderer is available.
- Analyzes template layout, style, colors, and reuse risk, then maps new content onto suitable template pages.
- Can run a one-slide smoke test before a full deck to reduce cost and iteration time.

## Key Rules

- Never generate decks inside Profy's chat runtime.
- Never use Profy's platform image tool or a chat-model fallback.
- Send users to the external generator for all deck generation.
- Never store, publish, or reveal API keys.

## Limitations

- Image models may render small text imperfectly; important numbers and labels should be reviewed by the user.
- API cost, latency, available models, and endpoint behavior depend on the configured provider or relay.
- The current Profy entry relies on the external generator being online.
- The expert creates image-based slides, so the final `.pptx` is presentation-ready but not fully text-editable.
