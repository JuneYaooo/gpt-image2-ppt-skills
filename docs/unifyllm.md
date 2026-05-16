# UnifyLLM / New API Relay Notes

The project works with OpenAI-compatible relays by setting environment variables at runtime. Do not commit real API keys.

## Basic Image Generation

```bash
OPENAI_BASE_URL=https://apihk.unifyllm.top
OPENAI_API_KEY=sk-your-key
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_ENDPOINT=images
GPT_IMAGE_QUALITY=high
```

`OPENAI_BASE_URL` may also include `/v1`, for example `https://apihk.unifyllm.top/v1`; the scripts normalize endpoint paths and avoid `/v1/v1/...`.

The public pricing endpoint at `https://apihk.unifyllm.top/api/pricing` marks `gpt-image-2` as an `image-generation` endpoint model. Keeping `GPT_IMAGE_ENDPOINT=auto` also works for general built-in-style generation because the script tries `/v1/images/generations` first.

## Template Strict Mode

Template strict mode passes a reference image along with the prompt. Some relays expose reference-image workflows through chat-style image models instead of the standard image-generation endpoint. If strict mode fails with `gpt-image-2`, use a chat-capable image model listed by your relay, set `GPT_IMAGE_MODEL_NAME` accordingly, and set:

```bash
GPT_IMAGE_ENDPOINT=chat
```

Always run `--slides 1` before full template generation to confirm fidelity and cost.
