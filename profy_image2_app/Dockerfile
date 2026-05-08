# syntax=docker/dockerfile:1.7
FROM alpine:3.21

ENV OPENAI_BASE_URL=https://apihk.unifyllm.top
ENV GPT_IMAGE_MODEL_NAME=gpt-image-2
ENV GPT_IMAGE_ENDPOINT=images
ENV GPT_IMAGE_QUALITY=high
ENV GPT_IMAGE_CONCURRENCY=2
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

WORKDIR /app

RUN apk add --no-cache ca-certificates python3

RUN rm -rf \
  /root/.cache \
  /usr/lib/python*/ensurepip \
  /usr/lib/python*/site-packages/pip* \
  /usr/lib/python*/site-packages/setuptools* \
  /usr/bin/pip* \
  && find /usr/lib/python* -type d -name '__pycache__' -prune -exec rm -rf {} +

RUN --mount=type=secret,id=openai_api_key,required=false \
  sh -c 'if [ -f /run/secrets/openai_api_key ]; then umask 077; printf "OPENAI_API_KEY=%s\n" "$(cat /run/secrets/openai_api_key)" > /app/.runtime.env; fi'

COPY app /app/app
COPY engine /app/engine

EXPOSE 3000
CMD ["sh", "-c", "if [ -z \"$OPENAI_API_KEY\" ] && [ -f /app/.runtime.env ]; then set -a; . /app/.runtime.env; set +a; fi; exec python3 -m app.server_stdlib"]
