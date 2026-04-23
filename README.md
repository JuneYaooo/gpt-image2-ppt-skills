# gpt-image2-ppt-skills

> 用 OpenAI 官方 `gpt-image-2` Images API 生成视觉风格强烈的 PPT 图片，自动产出可键盘翻页的 HTML viewer。Claude Code Skill / OpenClaw Skill。

🌐 **English** > [docs/README.en.md](./docs/README.en.md)

## ✨ 特性

- 🎨 **十套精选风格**：渐变玻璃 / 蓝白科技 / 矢量插画 / 黑白杂志 / 深色霓虹 / Riso 印刷 / 日式侘寂 / 瑞士网格 / 手绘草稿 / Y2K 金属，每套都有 cover/content/data 三种构图规范
- 🪄 **模板克隆模式**：传一个 .pptx，自动渲染 + vision 抽风格 + JSON Schema，新内容仿这个模板出图
- 🤖 **官方 OpenAI Images API**：模型 `gpt-image-2`
- 🔄 **OpenAI 兼容**：base_url 可换成任何兼容中转站
- 🖼 **16:9 高清 PPT**：默认 1536x1024，`quality=high`
- 🎮 **HTML viewer**：键盘翻页、空格自动播放、ESC 全屏、触摸滑动
- 🧩 **逐页迭代**：`--slides 1,3,5` 只生成指定页，跑过的自动跳过

## 🚀 一键安装

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh
```

安装后 skill 会被装到 `~/.claude/skills/gpt-image2-ppt-skills/`，Claude Code 重启后自动识别。

## ⚙ 配置

编辑 `~/.claude/skills/gpt-image2-ppt-skills/.env`：

```bash
OPENAI_BASE_URL=https://api.openai.com    # 或任意 OpenAI 兼容中转站
OPENAI_API_KEY=sk-...                     # 必需
GPT_IMAGE_MODEL_NAME=gpt-image-2          # 默认 gpt-image-2
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto

# 可选：仅模板克隆模式需要，且仅当调用本 skill 的 agent 不是多模态时才配。
# 多模态 agent (Claude Code / codex 等) 可以直接 Read template_renders 里的 PNG
# 自己抽风格，不用外挂；此时这三项留空即可。
# 不内置默认 endpoint，请填你自己信任的服务，否则就别启用 VISION_*。
# VISION_BASE_URL=https://your-openai-compatible-relay.example.com/v1
# VISION_API_KEY=sk-...
# VISION_MODEL_NAME=gemini-3.1-pro-preview   # 或 gpt-4o / claude-3.5-sonnet 等任意多模态 SKU
```

> 安全：脚本只从 `<script_dir>/.env`、`~/.claude/skills/.../env`、`~/skills/.../env` 或显式 `GPT_IMAGE2_PPT_ENV` 加载，**不会**向上递归读取项目目录的 `.env`，避免误吃无关密钥。

## 📝 用法

### 1. 写一份 slides_plan.json

```json
{
  "title": "我的演示",
  "slides": [
    {"slide_number": 1, "page_type": "cover",   "content": "标题：xxx\n副标题：yyy"},
    {"slide_number": 2, "page_type": "content", "content": "三个要点..."},
    {"slide_number": 3, "page_type": "data",    "content": "对比数据..."}
  ]
}
```

`page_type` 三选一：`cover` / `content` / `data`，影响生图构图。

### 2. 选一种风格生成

```bash
# 全量生成
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md

# 只生成第 1 页（用来先验证 API 通）
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 1

# 只重生第 3 和第 5 页
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 3,5
```

### 2.5 仿用户自己的 PPT 模板

```bash
# 一行：自动渲染 + vision 抽风格 + 出图。本机有 LibreOffice 或 docker 镜像即可
python3 scripts/generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-strict

# 显式指定渲染目录（已经手动跑过 render_template.py 或自己导出过 PNG）
python3 scripts/generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-images ./template_renders/company-template \
  --template-strict

# 强制重跑 vision（默认会读 template_cache/<sha256>.json 缓存）
python3 scripts/generate_ppt.py ... --rebuild-template-cache
```

`--template-strict` 表示每页都把模板对应页作为 image reference 传给 gpt-image-2，仿真度最高。

不传 `--template-images` 时会自动调 `render_template.py`，按优先级：本机 `libreoffice` -> 本机 docker 跑 `linuxserver/libreoffice` -> 报错让用户手工导出 PNG。PDF -> PNG 走 `pymupdf`（已在 requirements）。

第一次跑 vision 分析时,优先让调用本 skill 的 agent 自己看 `template_renders/<stem>/page-*.png` 并把结构化结果写进 `template_cache/<sha256>.json`(Claude Code / codex 这类多模态 agent 开箱即可);只有 agent 本身是纯文本模型时才回落到 `VISION_*` 配置的外部多模态端点(Gemini / GPT / Claude 任选)。后续同一模板秒匹配。

#### 渲染中间产物落盘

| 路径 | 内容 |
| --- | --- |
| `<cwd>/template_renders/<stem>/page-NN.png` | LibreOffice 渲染的每页 PNG |
| `<cwd>/template_renders/<stem>/_source.pdf` | LibreOffice 中间产物（顺手保留以便人工排查） |
| `<cwd>/template_cache/<sha256>.json` | vision 风格分析缓存 |
| `<cwd>/outputs/<timestamp>/` | 每次生成产物 |

把这三个目录加进项目 `.gitignore`。

### 3. 看产物

```
outputs/20260422_153012/
|---- images/
|   |---- slide-01.png
|   |---- slide-02.png
|   \---- ...
|---- index.html       # 浏览器打开就能键盘翻页
\---- prompts.json     # 每页完整 prompt，方便复盘
```

## 🎨 十种内置风格

| 风格 ID | 一句话定位 | 适用场景 |
| --- | --- | --- |
| `gradient-glass` | Apple Vision OS / Spatial Glass | AI 产品发布、技术分享、创意提案 |
| `clean-tech-blue` | Stripe / Linear 级蓝白 | 融资路演、商业计划书、企业战略 |
| `vector-illustration` | 复古矢量插画 + 黑描边 | 教育培训、品牌故事、社区分享 |
| `editorial-mono` | Kinfolk / Monocle 编辑设计 | 品牌发布、文化访谈、读书分享 |
| `dark-aurora` | Linear / Vercel 深色霓虹 | AI 产品、开发者工具、技术分享 |
| `risograph` | Riso 双套色印刷 + 网点纹理 | 创意工作室、文创品牌、独立 zine |
| `japanese-wabi` | 无印 / 原研哉式侘寂 | 茶道、生活方式、奢侈品、文化讲座 |
| `swiss-grid` | Bauhaus / Vignelli 国际主义网格 | 学术报告、博物馆展陈、严肃汇报 |
| `hand-sketch` | Sketchnote / 白板手绘 | 工作坊、产品 brainstorming、培训 |
| `y2k-chrome` | Y2K 千禧液态金属 + 蝴蝶贴纸 | 潮牌、文娱、品牌联名、Z 世代营销 |

每个风格的完整 prompt 见 `styles/<id>.md`，按 cover / content / data 三种构图分别给出版式规范。

## 🛠 在 Claude Code 里调用

直接和 Claude 说：

> 帮我用 gpt-image2-ppt 生成一份关于 [你的主题] 的 5 页 PPT，风格用 clean-tech-blue。

Claude 会：
1. 问你具体内容
2. 写好 `slides_plan.json`
3. 跑 `generate_ppt.py --slides 1` 出封面让你确认
4. 跑全量并把 viewer 路径告诉你

## 📦 依赖

- Python 3.8+
- `pip install -r requirements.txt` 装齐所有依赖（`requests` / `python-dotenv` / `python-pptx` / `jsonschema` / `pymupdf`）
- 模板克隆模式额外需要：本机 `libreoffice` 或本机 docker + `linuxserver/libreoffice` 镜像

## 🙏 致谢

- [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) -- 风格 prompts 与 viewer 模板的原始作者。本项目把图片后端从 Nano Banana Pro 换成了 OpenAI gpt-image-2，重写了继承自上游的 3 套风格并新增 7 套（共 10 套），另加入模板克隆模式（vision 抽风格仿任意 .pptx）、md-first 编排流程、.pptx 自动打包、codex CLI 备用后端等新功能。
- [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) -- Claude Code skill SKILL.md frontmatter 写法参考。

## License

Apache License 2.0.
