---
name: gpt-image2-ppt
description: Generate visually striking PPT slides via OpenAI's gpt-image-2 -- use any style in styles/<id>.md or mimic a user-supplied .pptx template; outputs high-res slide PNGs and a 16:9 .pptx. Use when the user asks to make a presentation, slides, deck, pitch deck, investor PPT, magazine-style PPT, or 做一份 PPT / 生成幻灯片 / 用 gpt-image 生成 PPT / 按这个模板生成 PPT.
---

# gpt-image2-ppt -- 用 gpt-image-2 生成 PPT

把一份 markdown 大纲（或 `slides_plan.json`）+ 一种视觉风格，直接喂给 OpenAI 官方 Images API（`gpt-image-2`），逐页出图，最后打包成 16:9 .pptx。

## 可用风格

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
| `abstract-art-showcase` | 黑白极简、艺术展览感、超大字体和抽象画面并置 | 艺术策展、作品集、品牌调性展示 |
| `coal-industry-business-company-profile` | 工业棕黑、粗重标题、结构线和硬朗图标 | 能源、制造业、重资产公司介绍 |
| `college-candy-aesthetics-infographics` | 糖果色、校园感、圆润信息图和轻快装饰 | 教育、校园活动、轻量数据科普 |
| `creative-agency` | 创意机构气质、强视觉拼贴、鲜明版式节奏 | Agency 提案、品牌方案、创意汇报 |
| `culinary-innovation` | 餐饮创新感、食材摄影、暖色块和杂志式排版 | 餐饮品牌、食品创新、菜单/新品发布 |
| `data-science-consulting` | 数据咨询蓝灰、模块化布局、图表和技术感信息层级 | 数据分析、AI 咨询、企业数字化 |
| `mindfulness-in-the-classroom-breathing-techniques` | 柔和心理健康配色、留白、圆角块和安静插画感 | 心理健康、课堂活动、呼吸训练课程 |
| `mind-maps-workshop-professional` | 专业工作坊风、思维导图节点、清晰流程结构 | 培训工作坊、方法论、团队共创 |
| `meeting-agenda` | 会议议程感、干净网格、强信息分组和商务标题 | 例会、项目同步、管理层汇报 |
| `investment-company-business-plan` | 投资机构质感、深浅对比、稳重商务版式 | 投资计划、基金介绍、商业计划书 |
| `indigenous-cultures` | 文化纹样、自然色、手工质感和叙事型构图 | 文化课程、历史主题、公益教育 |
| `health-disparities-and-social-determinants-of-health-doctor-of-philosophy-phd-in-health-behavior-and-health-education` | 公共健康学术风、理性网格、柔和医疗色和论文感层级 | 医学论文答辩、公共健康报告、教育研究 |
| `geometric-duotone-thesis` | 双色几何、论文答辩感、斜切图形和强标题 | 学术答辩、研究报告、章节型内容 |
| `geometric-clinical-case` | 几何医疗风、冷静配色、病例卡片和清晰分栏 | 临床病例、医疗培训、诊疗汇报 |
| `geometric-business` | 商务几何块、稳健蓝绿调、简洁图表语言 | 商业计划、团队汇报、产品策略 |
| `formal-lavender-portfolio` | 淡紫正式感、作品集留白、优雅细线和柔和版式 | 个人作品集、设计简历、专业展示 |
| `flowery` | 花卉装饰、柔和色块、浪漫但有秩序的排版 | 生活方式、女性品牌、活动介绍 |
| `first-impressions` | 第一印象主题、强封面视觉、人物/标题的戏剧化关系 | 面试培训、个人品牌、沟通课程 |
| `final-year-project-thesis-defense` | 毕业设计答辩、学院派网格、清晰章节与数据页 | 毕业答辩、项目结题、研究展示 |
| `fashion-business-consulting-toolkit-aesthetic` | 时尚咨询感、高级拼贴、杂志排版和中性色 | 时尚商业、品牌咨询、趋势报告 |
| `economic-impact-of-coronavirus` | 经济影响报告风、严肃信息图、冷静色彩和数据叙事 | 宏观经济、政策分析、风险报告 |
| `eco-green-business-plan` | 鼠尾草绿、自然材质摄影、环保商务与极简分屏 | 可持续商业、环保品牌、健康生活方式 |

所有可用风格都统一放在 `styles/` 下，使用方式完全相同。需要查看风格封面展示时，读取 `docs/distilled-styles.md`。

> 风格选择原则：先根据内容场景在 `styles/` 里选择最贴近的一套。技术类可优先看 `dark-aurora` / `gradient-glass` / `data-science-consulting`，商务类可优先看 `clean-tech-blue` / `editorial-mono` / `eco-green-business-plan` / `investment-company-business-plan`，文化生活类可优先看 `japanese-wabi` / `vector-illustration` / `culinary-innovation` / `flowery`，学术类可优先看 `swiss-grid` / `geometric-duotone-thesis` / `final-year-project-thesis-defense`，工作坊与培训类可优先看 `hand-sketch` / `mind-maps-workshop-professional` / `mindfulness-in-the-classroom-breathing-techniques`。

## 场景 recipes（可选起步模板）

`examples/` 不是新的 skill，也不是运行时必须输入；它是当前 skill 的场景起步模板库，用来在用户只给出模糊需求时，帮助 agent 更快写出第一版 `slides_plan.md`。

触发规则：

- 用户已经提供完整大纲 / 完整 `slides_plan.md` / 完整 `slides_plan.json` 时，不要套 recipe，直接按用户内容走生成流程。
- 用户只说“做一份产品发布 PPT / 融资路演 / 周报 / 课程课件 / 论文答辩 / 读书分享”等常见场景，且没有给清晰页结构时，先查看 `examples/` 是否有匹配 recipe。
- recipe 只作为结构参考：读取 `examples/<id>/recipe.md` 了解场景、推荐风格和注意事项，再参考 `examples/<id>/slides_plan.md` 的页序结构，改写成用户自己的主题与内容。
- 不要把示例里的虚构产品、公司、项目、数据直接当成用户成品；必须替换为用户提供的信息，或明确标注为占位内容并等待用户确认。
- 如果用户给了真实图片、logo、截图、论文图表或产品 UI，仍按“外部真实图片贴入”规则处理；recipe 只负责内容结构，不替代素材保真流程。

当前内置 recipes：

| 用户场景 | recipe 目录 | 推荐风格 |
| --- | --- | --- |
| 产品发布、新功能发布、AI 产品介绍 | `examples/product-launch/` | `gradient-glass` |
| 融资路演、商业计划书、投资人汇报 | `examples/investor-pitch/` | `clean-tech-blue` |
| 项目周报、月报、例会同步 | `examples/weekly-report/` | `meeting-agenda` |
| 课程课件、培训、知识科普 | `examples/courseware/` | `vector-illustration` |
| 论文答辩、毕设答辩、结题展示 | `examples/thesis-defense/` | `final-year-project-thesis-defense` |
| 读书分享、文化访谈、观点分享 | `examples/book-sharing/` | `editorial-mono` |

使用方式：

1. 判断用户需求是否命中某个 recipe。
2. 读取对应 `recipe.md` 和 `slides_plan.md`。
3. 基于用户主题改写一份新的 `slides_plan.md`，不要直接改 recipe 源文件。
4. 与用户确认页数、每页标题和关键内容。
5. 用户确认后再执行 `md_to_plan.py` 转 json，并继续下面的指定风格或模板克隆流程。
### 内置风格的 layout bank sidecar（推荐新格式）

内置风格采用“MD 给人看，JSON 给机器用”的双文件结构：

```text
styles/<style-id>.md            # 风格说明、设计令牌、基础提示词
styles/<style-id>.layouts.json  # 可选；每页 layout bank，供自动分配页面形态
```

当 `--style styles/<style-id>.md` 存在同名 `.layouts.json` 时，`generate_ppt.py` 会自动把它作为无 reference image 的 TemplateProfile 使用：优先通过 `assign_layouts()` 分配不同 layout，把 `visual_signature` / `content_capacity` / `best_for` / `avoid_for` / `variation_tags` 写入 prompt，并把命中的 layout 精简信息写入 `metadata.json`。

当前所有内置 `styles/*.md` 都应配套同名 `.layouts.json`。以后蒸馏公开模板或内置风格时，优先补这个 JSON sidecar；不要把多页 layout 只压缩进单个 MD 的“布局系统”文字段落。

## 模板克隆模式

直接给 skill 一个 .pptx 模板，后续所有页都仿这个模板。

```bash
# 一行：自动渲染 + 模板分析 + 出图。需本机有可用 PPTX 渲染后端
python3 scripts/generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-strict
```

`--template-strict` 表示每页都把模板对应页作为 image reference 喂给 gpt-image-2，仿真度最高。

### 模板渲染：本机不需要操作 PowerPoint

skill 自带 `render_template.py`，把 .pptx 自动渲染成每页 PNG，存到 `<cwd>/template_renders/<stem>/page-NN.png`。

### Agent 前置检查（模板克隆时必须做）

**在跑任何 --template-pptx 命令之前，你必须先检查本机是否有可用 PPTX 渲染后端。**

检查方式：

- 首选：在 skill 目录运行 `python3 scripts/render_template.py --check`。它会验证后端是否真的可执行，而不是只看路径是否存在。
- macOS：优先检查 `/Applications/Keynote.app` 且 AppleScript 可执行；否则检查 `libreoffice --version || soffice --version`
- Windows：优先检查本机 PowerPoint COM 可启动；否则检查 `libreoffice --version` / `soffice --version`
- Linux / 兼容层：检查 `libreoffice --version || soffice --version`，不要只用 `which`

注意：鸿蒙 / Termux / 容器 / 特殊架构环境可能看起来像 Linux，但不能假设 Linux aarch64 的 LibreOffice 二进制可运行；必须以 `render_template.py --check` 或 `soffice --version` 的实际执行结果为准。不要把 `aspose-slides` 当默认兜底，它在很多移动/特殊 Python 环境没有可安装 wheel。

如果都没有可用后端，先告知用户模板渲染需要安装可执行的 LibreOffice，或让用户在桌面端手动把模板每页导出为 `page-01.png`、`page-02.png` 后通过 `--template-images` 传入。可选安装命令：

| 平台 | 安装命令 |
| --- | --- |
| Windows | `winget install LibreOffice.LibreOffice` |
| macOS | `brew install --cask libreoffice` |
| Linux (Debian/Ubuntu) | `sudo apt-get install -y libreoffice` |
| Linux (Fedora/RHEL) | `sudo dnf install -y libreoffice` |
| Linux (Arch) | `sudo pacman -S --noconfirm libreoffice-fresh` |

装完再次检查，确认存在可用渲染后端再继续后续流程。

> 注意：Windows 上 `winget` 是 Win10/11 自带，会弹 UAC 确认框，需要用户点确认；macOS 上 `brew` 需要先安装 Homebrew。

`render_template.py` 的渲染后端按优先级自动挑：
1. **Windows**：PowerPoint COM（本机有 Office 时优先，直出 PNG，跳过 PDF 步骤）> LibreOffice
2. **macOS**：Keynote AppleScript（本机有 Keynote 时优先，直出 PNG）> LibreOffice
3. **Linux / 兼容层**：通过 `--version` 探测确认可运行的 LibreOffice / soffice 命令
4. PDF -> PNG 走 `pymupdf`（已在 requirements）；没装就用 `pdf2image` + poppler

跑 `generate_ppt.py --template-pptx ...` 时如果省略 `--template-images` 会自动调一次渲染；也可以手动先跑一次：

```bash
python3 scripts/render_template.py company-template.pptx
# -> <cwd>/template_renders/company_template/page-01.png ... page-NN.png
```

### 仿模板的两层缓存

| 资料 | 路径 | 用途 |
| --- | --- | --- |
| 模板每页 PNG | `<cwd>/template_renders/<stem>/page-NN.png` | 本机渲染后端一次渲染长期复用 |
| 模板风格分析 | `<cwd>/template_cache/<sha256>.json` 或手写 `template_profile.json` | 多模态 agent 自己看图生成；纯文本 agent 才需要外挂 vision |
| 生成产物 | `<cwd>/outputs/<timestamp>/` | 每次新跑都新目录 |

三者都在调用者 cwd 下，与项目自然同进退；建议把 `template_renders/`、`template_cache/`、`outputs/` 加进项目的 `.gitignore`。

**模板看图分析（让 agent 自己判断要不要配 `VISION_*`）**：

- **当前 code agent 本身是多模态模型**（例如 Claude Code 的多模态 Claude、Codex 的多模态 GPT）：不需要额外配置 `VISION_*`。agent 直接读取 `template_renders/<stem>/page-*.png`，按 `template_analyzer.py` 的 `TemplateProfile` 结构生成 `template_profile.json`，再用 `--template-profile template_profile.json` 传给 `generate_ppt.py`。如果要配合 `--template-strict`，每个 layout 里要写 `reference_image`（模板 PNG 的绝对路径或可访问路径）。
- **当前 code agent 是纯文本模型**（例如只接入 DeepSeek 文本模型）：它看不了模板截图，需要额外配置 `VISION_BASE_URL` / `VISION_API_KEY` / `VISION_MODEL_NAME`，让 `template_analyzer.py` 调一个独立的 OpenAI 兼容多模态端点做模板分析。

vision 分析与图片生成的 `gpt-image-2` 永远解耦——换 vision provider 不影响出图路径。

## 安装

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh --target claude   # Claude Code
# 或
bash install_as_skill.sh --target codex    # Codex
# API 直连所需密钥优先通过 agent 配置 / 系统环境变量注入
```

## 环境变量注入（API 直连时）

不要把本 skill 的密钥写进调用者业务项目根目录的 `.env`，也不要为了出图去读取用户项目里的通用 `.env`。环境变量建议按 agent 框架的标准方式注入：

- **通用 / CI / 服务器**：用系统环境变量、Docker Compose `environment` / `env_file`、Kubernetes Secret、CI Secret 等注入。
- **Claude Code**：用用户级 `~/.claude/settings.json` 或项目级 `.claude/settings.local.json` 注入环境变量；命令行环境变量优先级最高。
- **OpenClaw / 自定义 Agent**：用框架配置里的 `apiKey` / env reference 引用系统环境变量，避免把 key 明文写进项目配置。
- **本地 standalone CLI fallback**：可以设置 `GPT_IMAGE2_PPT_ENV=/path/to/private.env`，或使用 skill 安装目录下的 `.env`；这只是备用方式，不是业务项目 `.env`。

API 直连需要这些变量：

```bash
OPENAI_BASE_URL=https://api.openai.com    # 或任意 OpenAI 兼容中转站
OPENAI_API_KEY=sk-...
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                     # low / medium / high / auto

# 可选：模板克隆模式的 vision 分析 backend。
# 多模态 agent / 原生 Codex 可自己看图生成 --template-profile，不需要下面这组。
# 只有纯文本 agent（如 DeepSeek 文本模型）才需要外挂下面这组。
# 不内置默认 endpoint，请填你自己信任的服务，否则就别填。
# VISION_BASE_URL=https://your-openai-compatible-relay.example.com/v1
# VISION_API_KEY=sk-...
# VISION_MODEL_NAME=gemini-3.1-pro-preview   # 或 gpt-4o / claude-3.5-sonnet 等任意多模态 SKU
```

> **安全提示**：脚本只读取当前进程环境、平台注入的 `gpt-image2-ppt_*` 变量、显式 `GPT_IMAGE2_PPT_ENV`，以及 skill 安装目录下的 `.env` fallback。脚本**不会**向上递归读取调用者项目目录里的 `.env`，避免误吃业务项目密钥。

## 如果你就是 Codex agent（原生 image_generation 出图 — 推荐）

**如果你自己就是 Codex**（正在运行本 skill 的 agent 就是 Codex CLI / Codex TUI），并且当前环境提供 `image_generation` tool 和 ChatGPT 登录态，此时**不要用 `generate_ppt.py` 或 `--backend codex` 负责出图**，直接用原生工具生成图片，最后只复用本仓库的 md 转换 / PPTX 打包逻辑即可。

关键边界：Python 脚本运行在子进程里，拿不到当前 agent 会话里的原生 tool。`generate_ppt.py --backend codex` 能做的只有再启动一个 `codex exec` 子进程，让另一个 Codex 去出图；它不是“复用当前 Codex 的 image_generation tool”。所以当前 agent 已经能原生出图时，出图动作必须由 agent 本身完成，而不是交给 `generate_ppt.py`。

### 如何判断

你能访问 `image_generation` tool，并且不需要手动配 `OPENAI_API_KEY` 就能出图——满足这两个条件就走原生路径。若当前 Codex 会话没有这个 tool，就按普通 agent 处理：走 API 直连、`--backend codex` 备用后端，或让用户补齐环境。

### 出图流程（Codex 原生路径）

**1. 准备 slides 数据**

如果还没有 `slides_plan.json`，先按下面「生成流程」第 2-3 步写 `slides_plan.md` → `python3 scripts/md_to_plan.py ...` 转 json。

**2. 读风格模板**

读 `styles/<id>.md`，取 `## 基础提示词模板` section 作为 base prompt。

**3. 构造每页 prompt**

参考 `generate_ppt.py` 的 `generate_prompt()` 逻辑，核心规则：

- 封面（cover/slide 1）：标题/副标题为视觉焦点
- 数据页（data/最后一页）：突出关键数字、对比或结论
- 内容页（content/其余页）：按层级、对齐、留白结构化呈现
- **所有文字必须简体中文**，字体用思源黑体/苹方，严禁草书/艺术字
- **16:9 横版宽屏**（landscape, widescreen），prompt 里明确说"宽度明显大于高度、绝对不要方图"

```text
{style 基础提示词模板}

---

现在请生成本组中的【{封面页/内容页/数据页}】，{对应 hint}
本页要呈现的内容如下（请按本风格美学重新设计版式）：

{slide content}

【强制语言与字体要求】
1. 所有文字必须使用简体中文，严禁英文（专有名词除外）
2. 中文字体使用思源黑体或苹方，严禁草书、艺术字
3. 标题粗体，正文常规，字号对比清晰

【画面比例 — 强制】16:9 横版宽屏 (landscape, widescreen)，宽度明显大于高度，绝对不要方图或竖图。
```

**4. 调 image_generation tool 出图**

对每页调你的 `image_generation` tool：

- `prompt`: 上面拼好的完整 prompt
- `output_format`: `png`
- 将返回的图片保存到 `outputs/<timestamp>/images/slide-NN.png`（NN 为两位页码）

可以并发（建议 ≤4 并发，避免限流）。

**5. 打包 PPTX**

如果本 deck 没有外部真实图片对象，可以用下面的简易整页 PNG 打包。**如果任一页有 `external_image` / `image_overlay` / `external_image_placeholder` 且指向真实图片，不能用这个简易打包片段**，否则真实图片会被合进整页背景 PNG，用户无法在 PowerPoint 里单独选中拖动。此时必须走 `generate_ppt.py` 的标准打包逻辑，或在已有 session 中调用 `generate_pptx(..., metadata=metadata)`，让真实图片作为独立 picture object 叠在背景上。

```bash
python3 -c "
from pptx import Presentation
from pptx.util import Inches
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
import os, glob
for p in sorted(glob.glob('outputs/<timestamp>/images/slide-*.png')):
    slide = prs.slides.add_slide(blank)
    slide.shapes.add_picture(p, 0, 0, width=prs.slide_width, height=prs.slide_height)
prs.save('outputs/<timestamp>/<title>.pptx')
print('done')
"
```

外部真实图片页的正确 PPTX 结构应是：

- 第 1 层：`images/slide-XX.png` 作为整页背景图（包含模型生成的背景和文字）。
- 第 2 层：`source` 指向的真实图片作为独立 PPT picture object，按 `slide_spec` 坐标贴在背景上，可在 PowerPoint 里选中、拖动、缩放。

### 模板克隆模式（Codex 原生路径）

你自己就是多模态 agent——直接 `Read` 模板每页 PNG 抽取视觉风格，写成 `template_profile.json`（schema 见 `template_analyzer.py` 里的 `TemplateProfile`，每个 layout 写上 `reference_image`），然后按上面流程出图时把对应模板页作为 reference image 传给 `image_generation` tool。

**不需要配 `VISION_*`**——你就是 vision。

### 与下面「--backend codex」的区别

| | 原生路径（本节） | --backend codex |
|---|---|---|
| 适用场景 | **你就是** Codex agent | 你是 Claude Code / 其他 agent，借用本机 codex CLI |
| 调用方式 | 直接调 `image_generation` tool | spawn `codex exec --full-auto` 子进程 |
| 出图层数 | 1 层 | 2 层（agent → python → codex exec） |
| 速度 | 几秒/张 | 30-60s/张 |
| 可靠性 | tool 参数精确 | 自然语言 relay，偶发失败 |
| 需要 API Key | 不需要 | 不需要 |

---

## 可选：走 codex CLI 出图（--backend codex，非 Codex caller 用）

> **如果你就是 Codex agent，不要走这条路——用上一节的「原生路径」代替。**

当你用 Claude Code / OpenClaw / 其他 agent 运行本 skill，但本机装了 codex CLI 且已登录（`codex login`），可以借用它的凭据出图，省掉配 `OPENAI_API_KEY`：

```bash
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/editorial-mono.md --backend codex
```

默认后端仍是 `openai`（直调 API，快、并发稳、每页 3-10s）。`--backend codex` 是逃生口，适合"只跑 1-2 张图试水、不想配 key"的场景。

**Tradeoffs**：
- ✅ 不需要在本 skill 配 `OPENAI_API_KEY`
- ⚠️ 慢：每页多一层 agent loop，单页 30-60s+，10 页可能 5-10 分钟
- ⚠️ 计费不变：gpt-image-2 是按图计费，不在 ChatGPT 订阅内，codex 只是代你刷额度
- ⚠️ 可控性差：aspect_ratio / quality / reference_image 靠自然语言指令让 codex 转发，偶发失败

相关 env（都可选）：

```bash
CODEX_CMD="codex exec --full-auto"   # 覆盖 codex 调用方式（默认这串）
CODEX_IMAGE_MODEL=gpt-image-2        # 传给 codex 的目标模型
CODEX_TIMEOUT_SECS=900               # 单页超时
GPT_IMAGE_BACKEND=codex              # 不想每次敲 --backend 就设这个
```

模板克隆的 vision 分析同理——当 caller agent 自己是多模态时（Claude Code / 多模态 codex），可以直接 `Read` 模板 PNG 抽取风格，不用配 `VISION_*`；只有 caller agent 是纯文本模型时才需要外挂 vision provider。

## 生成流程（指定风格）

**先 md 后 json**：md 给人看、方便 diff / review / 改文案；json 由 md 派生，喂给 `generate_ppt.py`，标为 generated，不手改。

1. 用户给一份大纲 / 已有的 slides_plan.json；如果用户只给常见场景和主题，先按上方“场景 recipes”选择一个 `examples/<id>/` 作为结构参考
2. Agent 按下面 md 规范写一份新的 `slides_plan.md`，与用户确认文案：
   ````markdown
   ---
   title: MediWise Health Suite 商业计划书
   ---

   ## 1. [cover] MediWise Health Suite
   副标题：家庭健康管理智能平台
   年份：2026

   ## 2. [content] 市场痛点：健康管理的两类割裂
   痛点一：高频无深度
   ...

   ## 6. [data] 效率对比：使用 MediWise 前后
   ...
   ````
   - h2 格式：`## N. [page_type, layout=layout-05] 本页标题行`
   - `N.` 可省（按出现顺序自动编号）；`[page_type]` 可省（默认 `content`）；`layout=` 只在模板克隆模式需要
   - `page_type`: `cover` / `agenda` / `section` / `content` / `data` / `quote` / `closing` / `other`
   - h2 标题行 → json 里 `content` 的第一行；下面的正文 → 正文
3. 用户 OK 后，转 json：
   ```bash
   python3 scripts/md_to_plan.py slides_plan.md -o slides_plan.json
   ```
4. 选风格：从 `styles/` 里挑一个，对应 `styles/<id>.md`；如果使用了 recipe，优先采用 `recipe.md` / frontmatter 里的 `recommended_style`，需要视觉预览时先看 `docs/distilled-styles.md`
5. **构造 slide_spec**（Agent 步骤）：读 `styles/<id>.md` 的视觉规范，为 `slides_plan.json` 每页构造 `slide_spec`（每个元素的 type、content、position、style），写入每页的 `slide_spec` 字段。格式见下方"指哪改哪"章节
6. 调脚本：
   ```bash
   python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/editorial-mono.md
   ```
7. 产物在 `<cwd>/outputs/<timestamp>/`：
   - `images/slide-XX.png` -- 每页 PNG（16:9，1536x864）
   - `prompts.json` -- 每页用到的完整 prompt（便于复盘 / 二次微调）
   - `metadata.json` -- slide_spec 版本历史（支持精确编辑和回滚）
   - `<title>.pptx` -- 16:9 PPTX；默认背景与文字是整页图片，通过 `external_image` 放入的真实图片会作为独立 PPT 图片对象叠加

## 外部真实图片贴入（推荐精确流程）

默认规则：用户提供真实图时，优先按原图保真后贴，不要让 `gpt-image-2` 重画这张图。使用 `slide_spec` 声明外部图片槽位：

这套流程只在元素声明了 `type: "external_image"` / `image_overlay` / `external_image_placeholder` 且 `source` 能解析到真实本地图片文件时启用。没有真实图片 source 的普通生成、模板克隆、纯占位布局和老的自由风格生成不受影响。

如果用户明确说“更重视画面融合效果，不需要一定贴原图 / 可以重绘 / 可以图生图”，可以走参考图模式：把图片作为 generation reference 输入给模型，而不是最终独立后贴。此时版面通常更融合，但不保证像素级保真，PPT 里也不会有可单独选中的原图对象。

参考图模式可用 `type: "image_reference"`，或在 `external_image` 上显式写 `render_mode: "reference"` / `preserve_original: false`：

```json
{
  "elements": {
    "mood_reference": {
      "type": "image_reference",
      "source": "/absolute/path/to/photo.png",
      "purpose": "只作为视觉参考，允许模型融合重绘，不作为独立 PPT 图片对象后贴"
    }
  }
}
```

不要对高精度素材使用参考图重绘：医疗影像、病理图、诊断依据、实验/工程读数、财务表格、论文图表、法律证据截图、产品 UI 精确截图等都应默认走 `external_image` 保真后贴，并在交付前提示用户核对。

```json
{
  "elements": {
    "hero_photo": {
      "type": "external_image",
      "source": "/absolute/path/to/photo.png",
      "layout_intent": "auto",
      "tailor_to_asset": true,
      "slot_strategy": "fit-within",
      "fit": "contain",
      "slot": {
        "padding": 0.012,
        "bleed": 0,
        "fill": "#F7F7F5",
        "mask_placeholder": false,
        "sanitize_background": false,
        "draw_frame": false,
        "outline_width": 0,
        "skeleton_canvas_fill": "transparent",
        "skeleton_fill": "transparent",
        "skeleton_shape": "corners",
        "skeleton_outline": "#000000",
        "skeleton_outline_width": 2,
        "skeleton_ticks": false
      }
    }
  }
}
```

生成时脚本会自动做四件事：

1. **先规划槽位，再生成 skeleton**。脚本会优先读取模板 profile 里的 `external_image_slots`，或根据模板摘要推断“左图右文 / 右图左文 / 底部图表 / 中央主视觉”等候选区域；然后结合本页文字量、标题长度、真实图片数量、真实图片宽高比和素材分类（照片 / 图表 / 文档 / 架构图等）打分选位，先产出 `position` / `computed_bbox` / `auto_layout_reason` / `layout_planning_profile`。skeleton 只是把这个规划结果画给模型看，不负责临时想位置。
2. 读取 `source` 真实图片尺寸。如果声明了 `tailor_to_asset: true` 或 `slot_strategy: "fit-within"`，脚本会把 `position` 当作“可用区域”，按真实图片宽高比在其中计算 `computed_bbox`；这个 bbox 会同时用于 prompt、骨架参考图和最终 PPTX 贴图。这样不是生成后再临时缩放，而是在 `gpt-image-2` 出图前就量体裁衣。
3. 在 `outputs/<timestamp>/references/slide-XX-asset-skeleton.png` 生成一张透明画布的角标骨架参考图，把最终真实图会覆盖的 `final_image_rect_px` 标出来，并作为 reference image 传给 `gpt-image-2`。这只用于引导模型不要把关键信息放进该区域；**每页只调用一次 `gpt-image-2`，不是先生成一张再用骨架二次重生。**
4. 打包 PPTX 时，按同一个 bbox 用 `python-pptx` 把 `source` 指向的真实图片作为独立图片对象贴入。默认不画额外框，也不铺遮罩；也不会默认清理 `gpt-image-2` 生成图。真实图片不应被合成进 `images/slide-XX.png`，否则用户无法在 PPT 里单独拖动。

如果生成后发现真实图片槽位压到大面积文字或图形，优先按下面两种方式处理：

1. **预生成前微调槽位**：改 `slide_spec.elements.<id>.position`（或 `anchor` / `padding`），让真实素材移动到更干净的区域，再重新生成该页。只要槽位位置变了，就必须重新生成背景；不要只在 PPTX 里移动最终图片，否则背景内容仍可能压住新位置。
2. **二次版式修复**：当第一页整体风格已经满意，只是局部内容压入槽位时，用 `--edit SLIDE --external-slot-repair`。该模式会同时把当前页和新的 `asset-skeleton` 作为 reference image 传入，要求模型保持原风格但重排文字/图形，让槽位空出来。

示例：把真实图区域右移并重排当前页：

```bash
python3 scripts/generate_ppt.py \
  --session outputs/20260529_120000 \
  --edit 3 \
  --external-slot-repair \
  --element-updates '{"hero_photo":{"position":[0.60,0.16,0.32,0.60],"anchor":"center"}}'
```

同时，每个包含外部真实图片的页面都会在 `outputs/<timestamp>/external_image_trace/slide-XX/` 记录完整中间链路：

- `step1-real-on-blank.png`：把真实图片按最终坐标和大小先贴到空白页上，用来确认“真实图最终应该出现在这里”。
- `step2-reference-outline-blank.png`：去掉真实图片，只保留给 `gpt-image-2` 的角标定位参考图；默认透明画布，不铺白底。定位区域使用 `final_image_rect_px`，也就是最终真实图实际会覆盖的像素矩形，而不是外层 slot。这张图同时会复制到 `references/slide-XX-asset-skeleton.png` 并作为 image reference 输入。
- `step3-generated-background.png`：`gpt-image-2` 根据 step2 reference 生成的背景图，尚未贴入真实图片。
- `step3-image2-raw.png` / `step3-sanitized-background.png`：只有显式设置 `sanitize_background: true` 时才会出现，用于兜底清理模型已经画出的占位块；默认不启用。
- `step4-final-overlay-preview.png`：在 step3 上按 step1 同一坐标贴回真实图片的预览图，用来和 PPTX 最终效果对照。
- `manifest.json`：记录每个外部图片的 `source`、`slot_bbox_norm`、`inner_rect_norm`、`reference_rect_px`、`final_image_rect_px`、padding、bleed、素材尺寸和比例。

关键原则：

- reference skeleton 负责“告诉模型哪里不要放关键信息”，不是要求模型画白色空框。
- 模板克隆 / `--template-strict` 与外部真实图片槽位同时存在时，生成阶段会同时传入两张 reference：模板页用于学习风格，`asset-skeleton` 用于标记后贴图片覆盖区；不要二选一，否则模型只看模板页时不会知道最终图片位置。
- 外部真实图片页不能简单堆叠“模板照片/图片区 prompt”和“留空 prompt”。构造 prompt 前必须先消解冲突：模板只提供配色、字体、网格、节奏和装饰语言；模板里的照片区、图片框、全幅图、裁切图等都视为已被真实图片槽位替代。
- 构造 `slide_spec` 时，`position` 不能随便选，也不要默认固定右侧。模板克隆模式下，优先让模板 profile 提供 `external_image_slots`，或从模板布局摘要推断候选图片区，再根据本页文字量、真实图片数量、真实图片比例和页面类型打分：文字多时优先保证标题/正文阅读区；图片多或比例极端时优先用模板原有分栏/上下布局；无法共存时减少装饰和假视觉主体，而不是让真实图压内容。
- 推荐先写 `layout_intent: "auto"`，不手写 `position`。脚本会读取模板候选槽位、真实图尺寸、文字量、图片数量和比例来选择位置，写入 `position` / `computed_bbox` / `auto_layout_reason`；只有自动规划不理想时才用人工 `position` 覆盖。
- 使用 `layout_intent: "auto"` 时，`slide_spec.layout` 尽量写清图片区方向和结构，例如"左文右图 / right image / right landscape photo / 底部图片 / portrait rail"。自动规划会优先从这些方向性描述和模板候选槽位推断真实图区域；描述过泛时，重文本页可能退化到保守的小图槽位。
- `position` 默认可作为“允许使用的区域”；`computed_bbox` 才是脚本算出的最终真实图片槽位。
- 如果你想完全固定坐标，不要量体裁衣，直接写 `bbox`，或设置 `slot_strategy: "exact"` / `tailor_to_asset: false`。
- 最终精度由 `python-pptx` 坐标保证，不由模型画框保证。
- `skeleton_outline_width` 只控制给模型看的骨架参考图；`outline_width` / `draw_frame` 才控制最终 PPT 里是否出现可见框。
- prompt 中不写归一化坐标；位置通过透明角标 reference 图控制，避免模型错误解释数值坐标，也避免闭合框被理解成真实图片框。
- `skeleton_canvas_fill` / `skeleton_fill` / `skeleton_outline` / `skeleton_outline_width` / `skeleton_shape` 只影响参考骨架图。默认 `skeleton_canvas_fill: "transparent"` 且 `skeleton_shape: "corners"`，只在 `final_image_rect_px` 四角画短角标，不画闭合矩形、不铺白底，避免模型把 reference 理解成真实图片框或白色占位块。需要旧行为时显式设 `skeleton_shape: "outline"`。
- `sanitize_background` / `mask_placeholder` 不是推荐路径；它们只适合清掉极轻微的占位痕迹，不适合解决文字或图形大面积压住槽位的问题。遇到压内容，按“微调槽位并重生”或“二次版式修复”处理。
- 默认最终不画外框、不插入任何底色矩形，只贴真实图片；`mask_placeholder` 会被忽略，避免在真实图下方产生可拖动白底。只有显式设置 `draw_frame: true` 且 `outline_width > 0` 时，才会额外画无填充边框。
- 推荐默认：`tailor_to_asset: true` + `slot_strategy: "fit-within"` + `fit: "contain"` + 少量 `padding`。这会完整保留原图，并让骨架图从一开始就是按素材比例预留的。
- `fit: "contain"` 保留完整图片；`fit: "cover"` 会居中裁剪图片来铺满槽位。
- 如果要“严丝合缝”无白边，使用 `fit: "cover"`、`padding: 0`、`outline_width: 0`，并设置很小的 `bleed`（例如 `0.0015`-`0.003`）让图片比槽位多铺出约 1-3px，抵消 PowerPoint / Quick Look 渲染取整和抗锯齿缝隙。
- 如果想“预留一点但不要莫名空隙”，不要靠后期 `contain` 硬塞进一个比例不匹配的大框；应使用 `fit-within` 先算好比例匹配的槽位，再用很小的 `padding` 做设计留白。
- 交付前必须抽查 `external_image_trace/slide-XX/manifest.json`：重点看 `final_image_rect_px` 是否符合视觉预期，`auto_layout_reason` 是否选中了正确的左右/上下区域。若横图被算成小缩略图、竖图过窄或位置压内容，先补清楚 `slide_spec.layout` 的方向意图，或显式设置 `position`，再重新生成该页背景并重新打包 PPTX。

整体原理图保存于 `docs/external_image_overlay_logic.txt`；修改外部真实图片链路时，先对照这张图确认顺序仍是“模板/页面/素材画像 -> 候选槽位打分 -> 透明 skeleton -> 背景生成 -> 后贴真实图 -> 质检/有限修复”。

## 生成流程（模板克隆）

1. **拿到模板 .pptx**（用户提供 / 内部模板库 / 网络下载）
2. **（可选）先单独渲染并人工挑选**----大模板（>15 页）建议先 `python3 scripts/render_template.py xxx.pptx`，再从 `template_renders/<stem>/` 里挑 8-12 张代表页复制到 `template_renders/<stem>_curated/`，供 vision 分析。页数越精，layout 命中越准
3. **生成 slides_plan.md → 转 slides_plan.json**（见指定风格流程第 2-3 步）。每页 `slide_number` / `page_type` (`cover` / `agenda` / `section` / `content` / `data` / `quote` / `closing` / `other`) / `content`；想精准对位时在 h2 里加 `layout=layout-NN`（NN = 模板第 N 页 / 你期望对应的模板页编号）
4. **出图冒烟**。API 直连 / 非 Codex 原生路径跑 `generate_ppt.py`：
   ```bash
   python3 scripts/generate_ppt.py \
     --plan slides_plan.json \
     --template-pptx xxx.pptx \
     --template-images template_renders/xxx_curated \
     --template-strict --slides 1
   ```
   如果当前 agent 自己是多模态模型，也可以先看模板 PNG 写出 `template_profile.json`，再这样跑，完全不需要 `VISION_*`：
   ```bash
   python3 scripts/generate_ppt.py \
     --plan slides_plan.json \
     --template-profile template_profile.json \
     --template-strict --slides 1
   ```
   先 `--slides 1` 出封面冒烟，效果 OK 再跑全量。

   如果当前 agent 就是带原生出图能力的 Codex，不要用上面的 `generate_ppt.py` 命令负责出图；先生成 / 读取 `template_profile.json`，再按“Codex 原生路径”直接调当前会话的图片生成 tool 输出第 1 页 PNG，用户确认后再生成全量页面并打包。
5. **告知用户产物路径**

### 模板页面挑选 / 复用原则

**核心原则：尽量做到 1 page : 1 layout**----同一份 deck 里每个 slide 用不同的模板页作 reference，观众会觉得每页都是新内容；如果同一个独特 layout 出现 2-3 次，观众下意识会想"为什么又是这页"。

vision 分析时会给每个 layout 标 `reuse_friendly`：

TemplateProfile 每个 layout 除了 `id` / `page_type` / `summary` / `json_schema` / `reference_image`，还会尽量保存：

- `visual_signature`：这页最明显的视觉差异点，例如"右图左文"、"编号时间线"、"三卡片网格"。
- `content_capacity`：适合承载的信息密度，避免把长文塞进强视觉页。
- `best_for` / `avoid_for`：适合或不适合的内容结构。
- `variation_tags`：英文短标签，用来帮助比较和错开 layout 形态。

生成时会用 `assign_layouts()` 优先分配未使用 layout；即使 plan 没有手写 `slide_spec`，命中的模板 layout 也会以精简版 `template_layout_profile` 写进 `metadata.json`，便于后续编辑、贴图槽位规划和复盘。

| reuse_friendly | 典型 layout | 多次使用的代价 |
| --- | --- | --- |
| `false`（不可复用，(!) 强警告） | 封面、3 个具名角色插画页、独特场景图（雪山/广播塔/复古收音机）、5 步骤 zigzag 各步独有图标、novelty 数据中央装置 | 视觉重复非常明显，观众会困惑 |
| `true`（可复用，但仍建议错开，(i) 弱提示） | 纯文字、卡片网格、通用列表、章节小节标题 | 不致命，但平白浪费模板里的其它好版式 |

Agent 在搭 plan 时的执行策略：
1. **优先把模板里 N 个不同 layout 分配给 N 页 slide**（N 不够就在 SKILL 里看 reuse_friendly=true 的部分挑能复用的）
2. **如果 plan 里某页内容结构非常相似（比如多个"5 步骤流程"），先尝试改写内容用不同 layout 表达**（4 步骤 + 5 步骤分别用不同流程页），而不是同一个 zigzag 用两次
3. **冒烟跑完后，看 `Layout 复用检测` 那段输出**：(!) 必须改，(i) 看情况改；改 plan 里相应 slide 的 `layout_id` 即可
4. **看完 profile JSON 选 layout**：`cat <cwd>/template_cache/<sha256>.json | jq '.layouts[] | {id, page_type, reuse_friendly, visual_signature, content_capacity, summary}'`；如果是多模态 agent 自己生成的 `template_profile.json`，就读取那个文件。

`generate_ppt.py` 在派发任务前会自动跑一次复用检测，把警告打到终端，不阻塞执行。

## Skill 调用规范

当用户说"做一份 PPT" / "生成幻灯片"时：

1. **先问三件事**（不要直接动手）：
   - 内容 / 页数 / 观众是谁？
   - 风格偏好？按 `styles/` 和 `docs/distilled-styles.md` 的场景类目映射推荐 1-2 个；**或者用户上传自己的 .pptx 模板**（走 `--template-pptx`，自动渲染）
   - 是否需要单页测试一张图先看效果（API 直连用 `--slides 1`；Codex 原生路径直接生成第 1 页 PNG）
2. **先写 slides_plan.md** 给用户确认文案（md 是 source of truth，人审阅友好）
3. **转 slides_plan.json**：`python3 scripts/md_to_plan.py slides_plan.md -o slides_plan.json`（json 标为 generated，不手改；要改文案回到 md 改再转）
4. **构造 slide_spec**（Agent 步骤）：读 `styles/<id>.md` 了解视觉规范，然后为 `slides_plan.json` 每页构造 `slide_spec`，写入每页的 `slide_spec` 字段（格式见"指哪改哪"章节）。这一步让后续修改能精确到每个元素
5. **出图冒烟**：
   - API 直连 / 非 Codex 原生路径：跑 `generate_ppt.py --slides 1` 出封面冒烟，效果 OK 再跑全量
   - 当前 agent 就是带原生出图能力的 Codex：按上方“Codex 原生路径”直接调当前会话的 `image_generation` tool 生成 `outputs/<timestamp>/images/slide-01.png`；不要用 `generate_ppt.py --backend codex`
6. **告知用户产物路径**，产物在 `outputs/<timestamp>/`，`<title>.pptx` 可直接打开

### 面向用户的表达规范

对普通用户汇报时，默认不要解释 `slide_spec`、`metadata.json`、`element-updates`、JSON Schema、pytest 命令等内部实现，除非用户明确问技术细节。

用户最关心的是：

1. 做出来的 PPT 是否好看、能不能直接用。
2. 哪些场景稳定，哪些场景需要人工验收。
3. 是否只改了指定页 / 指定内容。
4. 最终输出目录和 PPTX 文件在哪里。
5. 当前不足是什么，例如背景/文字仍是整页图片、数字小字需复核；真实 logo/产品图需提供素材，才能作为独立图片对象放入。

如果需要介绍修改能力，优先引用 `docs/edit_guide.md` 的场景分级、before / after 案例和当前不足，不要把实现链路放在用户前面。

当用户说"改第 X 页的 XX"时：

1. **找到 session**：先用 `--list-sessions` 列出现有 session，确定要编辑的是哪个
2. **读 metadata.json**：查看对应 slide 的 slide_spec，找到目标元素
3. **确认修改内容**：告知用户当前内容，询问新内容
4. **构造编辑指令**：用 `--element-updates` 指定要改的元素和新内容
5. **执行 --edit**：`python3 scripts/generate_ppt.py --edit X --session <ts> --element-updates '{"elem_id": {"content": "new"}}'`
6. **告知结果**：新版本已生成，PPTX 已更新

## 仅生成部分页

```bash
python3 scripts/generate_ppt.py --plan my_plan.json --style styles/dark-aurora.md --slides 1,3,5
```

跑过的页有同名 PNG 时会自动跳过，方便逐页迭代。

## "指哪改哪" PPT 编辑工作流

本节只保留 agent 执行所需信息；完整结构、版本链和数据安全细节见 `docs/workflow.md`。向普通用户解释能力时看 `docs/edit_guide.md`。

### 生成时的结构化要求

生成新 PPT 时，agent 应为每页写入简洁的 `slide_spec`，方便后续按标题、副标题、卡片、指标等元素精确修改。最低要求：

- `layout`: 一句话描述版式
- `elements`: 语义化元素字典
- 常用元素 ID：`title`、`subtitle`、`card_1`、`card_2`、`metric_1`、`date_line`、`footer`
- 元素字段优先写 `type`、`content` 或 `heading/body`、`position`、`style`、`color`

不要为了追求完整而写很长的 spec；能让后续定位和编辑即可。

### 修改已有幻灯片

1. 用 `--list-sessions` 找到目标 session。
2. 读目标 session 的 `metadata.json`，定位页号和元素 ID。
3. 如果用户没给新内容，先问一句“当前是 X，要改成什么？”
4. 用 `--element-updates` 描述修改；需要更强约束时加 `--edit-instruction`，明确“其他内容、布局、配色不要动”。
5. 执行 `--edit` 后检查目标页图片，重建后的 PPTX 会同步更新。

常用命令：

```bash
python3 scripts/generate_ppt.py \
  --edit 3 \
  --session 20240523_143052 \
  --element-updates '{"subtitle": {"content": "医疗数据碎片化"}}' \
  --edit-instruction "将副标题从'健康管理的两类割裂'改为'医疗数据碎片化'"

python3 scripts/generate_ppt.py \
  --edit 3 \
  --session 20240523_143052 \
  --edit-prompt "在参考图基础上，只修改标题下方副标题的文字，从'健康管理的两类割裂'改为'医疗数据碎片化'，保持位置、字体、颜色、大小完全不变。" \
  --element-updates '{"subtitle": {"content": "医疗数据碎片化"}}'
```

### 外部 PPTX 摄取后修改

外部 PPTX 可先摄取为图片 session，再由多模态 agent 看图补齐每页的 `slide_spec`。没有补 spec 前，不要承诺“精确改某个对象”。

```bash
python3 scripts/generate_ppt.py --ingest-pptx path/to/deck.pptx
python3 scripts/generate_ppt.py --ingest-pptx path/to/deck.pptx --session my_deck_2024
```

### 回滚和 session 列表

```bash
python3 scripts/generate_ppt.py \
  --rollback 3 \
  --to-version 1 \
  --session 20240523_143052

python3 scripts/generate_ppt.py --list-sessions
```

## 文件结构

```
gpt-image2-ppt-skills/
|---- SKILL.md                # 本文件（Claude Code skill 入口）
|---- AGENTS.md               # codex / aider / cursor 等 agent 的薄索引，指向本文件
|---- README.md               # 项目说明
|---- scripts/                # 所有 Python 脚本
|   |---- generate_ppt.py         # 主入口（CLI）
|   |---- md_to_plan.py           # slides_plan.md -> slides_plan.json 转换器（CLI）
|   |---- render_template.py      # PPTX -> 每页 PNG 的辅助脚本（CLI + library）
|   |---- image_generator.py      # gpt-image-2 wrapper（支持 reference image，openai backend）
|   |---- codex_backend.py        # 可选：走 codex CLI 出图（--backend codex）
|   \---- template_analyzer.py    # PPT 模板剖析器（vision + 缓存）
|---- styles/                 # 所有可用风格，每个 .md 对应一个 style id
|   |---- gradient-glass.md           dark-aurora.md
|   |---- clean-tech-blue.md          risograph.md
|   |---- vector-illustration.md      japanese-wabi.md
|   |---- editorial-mono.md           swiss-grid.md
|   |---- hand-sketch.md              y2k-chrome.md
|---- examples/               # 场景 recipes：常见 PPT 的 slides_plan.md 起步模板
|   |---- product-launch/             investor-pitch/
|   |---- weekly-report/              courseware/
|   |---- thesis-defense/             book-sharing/
|---- docs/README.en.md       # 英文 README
|---- install_as_skill.sh     # 一键安装到 agent skills 目录
|---- requirements.txt        # requests + python-dotenv + python-pptx + jsonschema + pymupdf
\---- .env.example
```

调用时产生的运行时目录都在 `<cwd>` 下：
```
<your-project>/
|---- template_renders/<stem>/page-NN.png   # PPTX 渲染（render_template.py）
|---- template_cache/<sha256>.json          # 外挂 vision 风格分析缓存（纯文本 agent 路径）
|---- template_profile.json                 # 多模态 agent 可手写/生成的模板 profile（可选）
\---- outputs/<timestamp>/                  # 每次生成产物
```

## License

Apache License 2.0.
