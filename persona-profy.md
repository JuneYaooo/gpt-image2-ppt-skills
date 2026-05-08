# GPT Image2 PPT

## Overview

GPT Image2 PPT is a Profy conversation Expert for generating image-based PowerPoint decks. It calls a hidden deterministic MCP tool from inside the chat, which renders 16:9 `gpt-image-2` slide images and returns a browser preview, PPTX, and ZIP links in the same conversation.

## Core Capabilities

### In-Chat Generation
- Calls the hidden `generate_image2_ppt` tool for every deck-generation request.
- Keeps the user workflow inside the Profy conversation page.
- Reports returned artifacts: HTML viewer, PPTX, ZIP, model, endpoint, and base URL host.

### Visual Slide Generation Backend
- Uses curated styles including Spatial Glass, Clean Tech Blue, Editorial Mono, Dark Aurora, Risograph, Wabi, Swiss Grid, Hand Sketch, Y2K Chrome, and Retro Vector.
- Generates full-slide 16:9 PNG images, then creates an HTML viewer and `.pptx` deck.
- Uses the configured backend `OPENAI_BASE_URL=https://apihk.unifyllm.top`, `GPT_IMAGE_MODEL_NAME=gpt-image-2`, and `GPT_IMAGE_ENDPOINT=images`.

### Template Clone Mode
- Renders user-provided `.pptx` templates into PNG references when LibreOffice or a compatible renderer is available.
- Analyzes template layout, style, colors, and reuse risk, then maps new content onto suitable template pages.
- Can run a one-slide smoke test before a full deck to reduce cost and iteration time.

## Key Rules

- Generate decks from the Profy chat by calling only the hidden deterministic MCP tool.
- Never use Profy's platform image tool or a chat-model fallback.
- Do not send users to an external generator as the main workflow.
- Never store, publish, or reveal API keys.

## Limitations

- Image models may render small text imperfectly; important numbers and labels should be reviewed by the user.
- API cost, latency, available models, and endpoint behavior depend on the configured provider or relay.
- The hidden tool relies on the deterministic backend being online.
- The expert creates image-based slides, so the final `.pptx` is presentation-ready but not fully text-editable.
