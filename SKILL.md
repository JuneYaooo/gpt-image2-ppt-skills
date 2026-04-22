---
name: gpt-image2-ppt
description: 用 OpenAI gpt-image-2 生成视觉风格强烈的 PPT 图片（渐变玻璃 / 矢量插画 / 清爽科技蓝），自动产出可键盘翻页的 HTML viewer。Use when 用户说 "做一份 PPT"、"用 gpt-image 生成 PPT"、"生成幻灯片"、"PPT 封面"、"商业计划书 PPT"、"投资人演示"、"presentation"、"slides"、"deck"、"pitch deck"、"路演"、"科技蓝 PPT"、"玻璃拟态 PPT"、"矢量插画 PPT" 时调用。
---

# gpt-image2-ppt — 用 gpt-image-2 生成 PPT

把一份 markdown 大纲（或 `slides_plan.json`）+ 一种视觉风格，直接喂给 OpenAI 官方 Images API（`gpt-image-2`），逐页出图，最后拼成一个键盘可翻页的 HTML viewer。

## 三种内置风格

| 风格 | 适用场景 |
| --- | --- |
| `gradient-glass` | 科技产品、技术分享、创意提案 — 渐变玻璃 / 极光 / Bento 网格 |
| `clean-tech-blue` | 融资路演、投资人演示、商业计划书 — 蓝白克制、McKinsey 感 |
| `vector-illustration` | 教育培训、儿童内容、品牌故事 — 扁平矢量、复古配色 |

## 模板克隆模式（v2 新增）

不想用预设风格？直接给 skill 一个用户自己的 PPT 模板（.pptx + 每页导出的 PNG），后续生成全部仿这个模板。

```bash
# 默认仿模板（vision 抽风格 + 文本 prompt）
python3 generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-images ./template_renders/

# 高保真仿模板（每页拿模板对应页做 image reference）
python3 generate_ppt.py \
  --plan slides_plan.json \
  --template-images ./template_renders/ \
  --template-strict
```

**怎么导出 PNG**：在 PowerPoint / Keynote / WPS 里 `文件 → 导出 → 图片格式`，选 PNG，每页一张。本机没装 LibreOffice，所以图片得用户自己导出。文件名按字典序对应页码（推荐 `page-01.png`、`page-02.png`...）。

**vision 模型**：模板分析走单独的 OpenAI 兼容多模态 chat completions（默认 `gemini-3.1-pro-preview`，配在 `.env` 的 `VISION_*` 里），与图片生成的 `gpt-image-2` 解耦。同一模板第二次跑直接命中 `template_cache/<sha256>.json`，省钱。

## 安装

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh
# 编辑 ~/.claude/skills/gpt-image2-ppt-skills/.env 填入 API_KEY
```

## 必需的环境变量

```bash
OPENAI_BASE_URL=https://api.openai.com    # 或任意 OpenAI 兼容中转站
OPENAI_API_KEY=sk-...
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                     # low / medium / high / auto

# 可选：模板克隆模式才需要（vision 分析独立 provider）
VISION_BASE_URL=https://daydream88.fun/v1
VISION_API_KEY=sk-...
VISION_MODEL_NAME=gemini-3.1-pro-preview
```

## 生成流程

1. 用户给一份大纲 / 已有的 slides_plan.json
2. Claude 读懂内容，按需要生成 / 校准 `slides_plan.json`：
   ```json
   {
     "title": "...",
     "slides": [
       {"slide_number": 1, "page_type": "cover",   "content": "标题 / 副标题"},
       {"slide_number": 2, "page_type": "content", "content": "正文要点..."},
       {"slide_number": 3, "page_type": "data",    "content": "数据 / 总结..."}
     ]
   }
   ```
3. 选风格：`styles/gradient-glass.md` / `styles/clean-tech-blue.md` / `styles/vector-illustration.md`
4. 调脚本：
   ```bash
   python3 generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md
   ```
5. 产物在 `outputs/<timestamp>/`：
   - `images/slide-XX.png` — 每页 PNG（16:9，1536×1024）
   - `index.html` — HTML viewer，方向键翻页、空格自动播放、ESC 全屏
   - `prompts.json` — 每页用到的完整 prompt（便于复盘 / 二次微调）

## Skill 调用规范

当用户说"做一份 PPT" / "生成幻灯片"时：

1. **先问三件事**（不要直接动手）：
   - 内容 / 页数 / 观众是谁？
   - 风格偏好？默认推荐：技术分享 → `gradient-glass`，路演 → `clean-tech-blue`，教育 → `vector-illustration`；**或者用户上传自己的 .pptx 模板**（走 `--template-pptx` + `--template-images`）
   - 是否需要单页测试一张图先看效果（`--slides 1`）
2. **生成 slides_plan.json**：每页 `slide_number` / `page_type` (`cover` / `content` / `data`) / `content`；如果走模板模式且想精准对位，可以加 `layout_id`（值取自 `template_cache/<hash>.json` 里的 layouts[].id）或 `fields`（直接按 layout 的 json_schema 填字段）。
3. **跑 generate_ppt.py**，先 `--slides 1` 出封面冒烟，效果 OK 再跑全量
4. **告知用户产物路径**，让他在浏览器打开 `outputs/<timestamp>/index.html`

## 仅生成部分页

```bash
python3 generate_ppt.py --plan my_plan.json --style styles/gradient-glass.md --slides 1,3,5
```

跑过的页有同名 PNG 时会自动跳过，方便逐页迭代。

## 文件结构

```
gpt-image2-ppt-skills/
├── SKILL.md                # 本文件
├── README.md               # 项目说明
├── generate_ppt.py         # 主入口（CLI）
├── image_generator.py      # gpt-image-2 wrapper（支持 reference image）
├── template_analyzer.py    # PPT 模板剖析器（vision + 缓存）
├── slides_plan.json        # 示例 plan（10 页商业计划书）
├── styles/
│   ├── gradient-glass.md
│   ├── clean-tech-blue.md
│   └── vector-illustration.md
├── template_cache/         # 模板 vision profile 缓存（按 sha256 命名）
├── templates/
│   └── viewer.html         # HTML viewer 模板
├── install_as_skill.sh     # 一键安装到 ~/.claude/skills/
├── requirements.txt        # requests + python-dotenv + python-pptx + jsonschema
└── .env.example
```

## License

Apache License 2.0.
