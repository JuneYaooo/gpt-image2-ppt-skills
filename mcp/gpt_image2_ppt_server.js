#!/usr/bin/env node

const DEFAULT_API_BASE_URL = "https://compile-know-caroline-informative.trycloudflare.com";
const configuredUrl = process.env.GPT_IMAGE2_PPT_API_URL || process.env.GPT_IMAGE2_PPT_API_BASE_URL || DEFAULT_API_BASE_URL;
const API_BASE_URL = configuredUrl.replace(/\/api\/run\/?$/, "").replace(/\/+$/, "");

let buffer = Buffer.alloc(0);

function send(message) {
  const body = Buffer.from(JSON.stringify(message), "utf8");
  process.stdout.write(`Content-Length: ${body.length}\r\n\r\n`);
  process.stdout.write(body);
}

function result(id, value) {
  send({ jsonrpc: "2.0", id, result: value });
}

function error(id, code, message) {
  send({ jsonrpc: "2.0", id, error: { code, message } });
}

function readMessages() {
  while (true) {
    const headerEnd = buffer.indexOf("\r\n\r\n");
    if (headerEnd < 0) return;
    const header = buffer.slice(0, headerEnd).toString("utf8");
    const match = header.match(/Content-Length:\s*(\d+)/i);
    if (!match) {
      buffer = buffer.slice(headerEnd + 4);
      continue;
    }
    const length = Number(match[1]);
    const bodyStart = headerEnd + 4;
    const bodyEnd = bodyStart + length;
    if (buffer.length < bodyEnd) return;
    const raw = buffer.slice(bodyStart, bodyEnd).toString("utf8");
    buffer = buffer.slice(bodyEnd);
    handle(JSON.parse(raw)).catch((err) => {
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          if (parsed.id !== undefined) error(parsed.id, -32603, err.message || String(err));
        } catch {}
      }
    });
  }
}

function toolSchema() {
  return {
    name: "generate_image2_ppt",
    description:
      "Generate a complete PPT deck using the deterministic gpt-image-2 backend. Use this for every user request to create, regenerate, or export a PPT deck.",
    inputSchema: {
      type: "object",
      properties: {
        topic: {
          type: "string",
          description: "Deck topic or brief. Required unless slidesMarkdown is provided.",
        },
        slideCount: {
          type: "number",
          description: "Number of slides, 1-12. Default 5.",
          minimum: 1,
          maximum: 12,
        },
        style: {
          type: "string",
          description: "Visual style id.",
          enum: [
            "clean-tech-blue",
            "gradient-glass",
            "dark-aurora",
            "editorial-mono",
            "vector-illustration",
            "risograph",
            "japanese-wabi",
            "swiss-grid",
            "hand-sketch",
            "y2k-chrome",
          ],
        },
        quality: {
          type: "string",
          description: "Image quality. Use high unless the user requests a cheap/fast test.",
          enum: ["high", "medium", "low"],
        },
        slidesMarkdown: {
          type: "string",
          description: "Optional full slides_plan.md. Leave empty to auto-generate from topic.",
        },
      },
      required: [],
    },
  };
}

async function callGenerate(args) {
  const payload = {
    topic: args.topic || "AI 产品发布演示",
    slideCount: Number(args.slideCount || 5),
    style: args.style || "clean-tech-blue",
    quality: args.quality || "high",
    slidesMarkdown: args.slidesMarkdown || "",
  };

  const createResponse = await fetch(`${API_BASE_URL}/api/jobs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Profy-Tool": "gpt-image2-ppt",
    },
    body: JSON.stringify(payload),
  });

  const createText = await createResponse.text();
  let createData;
  try {
    createData = JSON.parse(createText);
  } catch {
    throw new Error(`Backend create returned non-JSON status=${createResponse.status}: ${createText.slice(0, 500)}`);
  }
  if (!createResponse.ok || !createData.jobId) {
    throw new Error(`Job create failed status=${createResponse.status}: ${JSON.stringify(createData).slice(0, 1200)}`);
  }

  const deadline = Date.now() + 45 * 60 * 1000;
  let data = null;
  while (Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, 5000));
    const statusResponse = await fetch(`${API_BASE_URL}/api/jobs/${createData.jobId}`, {
      headers: { "X-Profy-Tool": "gpt-image2-ppt" },
    });
    const statusText = await statusResponse.text();
    try {
      data = JSON.parse(statusText);
    } catch {
      throw new Error(`Backend status returned non-JSON status=${statusResponse.status}: ${statusText.slice(0, 500)}`);
    }
    if (data.status === "failed") {
      throw new Error(`Generation failed: ${JSON.stringify(data).slice(0, 1200)}`);
    }
    if (data.status === "done") {
      break;
    }
  }

  if (!data || data.status !== "done") {
    throw new Error(`Generation timed out for job ${createData.jobId}`);
  }

  data.links = {
    html: `${API_BASE_URL}/api/jobs/${createData.jobId}/file?kind=html`,
    pptx: `${API_BASE_URL}/api/jobs/${createData.jobId}/file?kind=pptx`,
    zip: `${API_BASE_URL}/api/jobs/${createData.jobId}/file?kind=zip`,
  };
  data.jobId = createData.jobId;
  return data;
}

async function handle(message) {
  if (message.method === "initialize") {
    result(message.id, {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      serverInfo: { name: "gpt-image2-ppt", version: "1.0.0" },
    });
    return;
  }

  if (message.method === "notifications/initialized") return;

  if (message.method === "tools/list") {
    result(message.id, { tools: [toolSchema()] });
    return;
  }

  if (message.method === "tools/call") {
    const params = message.params || {};
    if (params.name !== "generate_image2_ppt") {
      error(message.id, -32602, `Unknown tool: ${params.name}`);
      return;
    }
    const data = await callGenerate(params.arguments || {});
    const links = data.links || {};
    const summary = [
      "GPT Image2 PPT generation complete.",
      `model: ${data.model}`,
      `endpoint: ${data.endpoint}`,
      `baseUrlHost: ${data.baseUrlHost}`,
      `HTML viewer: ${links.html || ""}`,
      `PPTX: ${links.pptx || ""}`,
      `ZIP: ${links.zip || ""}`,
    ].join("\n");
    result(message.id, {
      content: [{ type: "text", text: summary }],
      structuredContent: data,
      isError: false,
    });
    return;
  }

  if (message.id !== undefined) error(message.id, -32601, `Unknown method: ${message.method}`);
}

process.stdin.on("data", (chunk) => {
  buffer = Buffer.concat([buffer, chunk]);
  readMessages();
});

process.stdin.on("end", () => process.exit(0));
