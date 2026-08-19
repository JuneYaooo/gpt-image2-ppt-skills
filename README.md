<div align="center">

# gpt-image2-ppt-skills

**用 OpenAI `gpt-image-2` 一键生成高审美、高完成度的 PPT。**

Claude Code / Codex / OpenClaw / Hermes 等支持 Skills 的 agent 均可原生使用。装进 agent 后，用一句自然语言生成 16:9 高清图片 + 打包好的 `.pptx`，也可以仿任意 `.pptx` 模板出全新内容。

它不走传统“模板填字”的路线，而是充分发挥 `gpt-image-2` 的审美、构图和排版能力，把每一页都当成完整视觉稿生成，力求让输出从封面到内页都足够精美、统一、可直接展示。

同时，项目对图片型 PPT 的后续编辑做了专门优化：默认模式仍以整页视觉稿保证 gpt-image-2 的构图与审美；如果用户明确要求文字、图形和素材可单独编辑，可以启用**默认关闭的可编辑模式**，把完整视觉稿重建为 PowerPoint 原生文本、基础图形、连接线和独立图片层。

[![GitHub stars](https://img.shields.io/github/stars/JuneYaooo/gpt-image2-ppt-skills?style=flat)](https://github.com/JuneYaooo/gpt-image2-ppt-skills/stargazers)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://www.anthropic.com/claude-code)
[![gpt-image-2](https://img.shields.io/badge/OpenAI-gpt--image--2-black.svg)](https://platform.openai.com/docs/guides/images)

🌐 **English** → [docs/README.en.md](./docs/README.en.md)

</div>

---

## 🎬 效果演示：喂一张模板，仿出一套新内容

<table>
<tr>
<th width="50%">输入：任意一页参考模板（.pptx / 图片）</th>
<th width="50%">输出：本 skill 仿制 + 换内容</th>
</tr>
<tr>
<td><img src="docs/assets/template-demo-input.jpg" width="100%" alt="input template"></td>
<td><img src="docs/assets/template-demo-output.jpg" width="100%" alt="generated output"></td>
</tr>
<tr>
<td align="center"><sub>英文信息图模板（Mass Media Infographics）</sub></td>
<td align="center"><sub>同一版式 / 同一配色 / 同一插画语汇，内容换成「普通人怎么用 AI 做自媒体」</sub></td>
</tr>
</table>

---

## 🧩 可编辑模式示例（默认关闭）

可编辑模式不会限制 gpt-image-2 的初始设计：模型仍先生成包含完整文字与主视觉的成品页，再把已知文字、基础图形和复杂素材重建成 PowerPoint 对象。

<table>
<tr>
<th width="50%">原始完整视觉稿</th>
<th width="50%">可编辑 PPTX 的 Office 回渲染</th>
</tr>
<tr>
<td><img src="examples/editable-pptx/case05-summer-poster/original.png" width="100%" alt="editable mode original poster"></td>
<td><img src="examples/editable-pptx/case05-summer-poster/rendered.png" width="100%" alt="editable PPTX rendered result"></td>
</tr>
</table>

这个示例的 PPTX 实测包含 **13 个可选对象**：5 个原生文本、6 个原生 shape、1 个 clean plate，以及 1 个可移动、可缩放的毛绒角色与粽子冰淇淋独立图片层。文字和基础图形可以直接在 PowerPoint 中修改，复杂主视觉仍保留 gpt-image-2 的完整质感。

- [下载 Case 05 可编辑 PPTX](examples/editable-pptx/case05-summer-poster/editable.pptx)
- [查看完整 Case 05：原图、拆层素材、边缘检查和质量报告](examples/editable-pptx/case05-summer-poster/)

需要可编辑交付时，可以直接这样说：

> 帮我生成一份可编辑模式的 PPT。文字和基础图形要能在 PowerPoint 里直接修改，复杂主视觉要能单独移动，同时尽量保留 gpt-image-2 的完整设计感。

只有明确提出“可编辑模式”“文字可以改”“元素可以拆开”或类似要求时，Skill 才会执行对象级重建。如果不特别说明，默认仍走视觉效果优先的整页图片模式。

> ⚠️ **可编辑模式需要本机具备 PPTX 回渲染能力。** 与模板克隆模式相同，运行前必须有可执行的 Windows PowerPoint、macOS Keynote 或 LibreOffice。用户无需执行检查命令，只要像上面那样用自然语言说明需要可编辑交付；Skill 会自动检查环境，生成后把 `-editable.pptx` 回渲染到 `editable_renders/page-XX.png`，再由多模态 AI 逐页看图验收。没有可用渲染后端时，不会把未经回渲染检查的可编辑文件标记为成功。

可编辑重建采用**效果优先、生成轮次受控**的策略：允许多轮本地预检和回渲染；优先用字体、坐标、裁切等确定性修复，其次进行原像素提取与遮挡补全，只对失败的复杂图层进行 AI 重绘，只有整体构图失败时才重新生成整页。这样不会为了追求单轮而牺牲效果，也不会因为局部问题反复重做整页。

---

## 🚀 快速开始

### 1. 让 AI 安装 Skill

把下面这段话发给 Claude Code、Codex、OpenClaw、Cursor、Trae、Hermes Agent，或其他支持 Skills 的 AI 助手：

> 帮我安装 gpt-image2-ppt-skills：<br>
> https://github.com/JuneYaooo/gpt-image2-ppt-skills

AI 会根据当前环境完成安装并提示你重启。

### 2. 安装后直接说需求

**普通生成**

> 帮我做一份关于「AI 如何改变内容创作」的 6 页 PPT，先生成一页封面给我确认，整体风格要有高级科技感。

**仿模板**

> 我上传了 `company-template.pptx`，请参考它的版式、配色和视觉语言，做一份关于「年度产品战略」的 8 页 PPT。

如果手头没有现成模板，也可以打开 [SlideCraft Template Gallery](https://slidecraft-template-gallery.vercel.app)，在网页中浏览并复制喜欢的模板，再把复制的模板内容直接发给 AI 使用。

**可编辑交付**

> 帮我生成一份可编辑模式的 PPT。文字和基础图形要能直接修改，复杂主视觉要能单独移动，同时尽量保留 gpt-image-2 的完整设计感。

AI 会整理内容、先做单页视觉确认、再生成完整 PPT，并把图片、PPTX 和输出目录交给你。

---

## ✨ 能做什么

- 🎨 **在线模板画廊** — 集中展示目前收录的模板，可按场景和风格搜索、筛选，复制喜欢的模板 Prompt 后直接交给 AI 使用
- 🧬 **模板质量验证** — 候选模板会实际生成封面、章节、内容和数据页，检查整套一致性、可读性和布局效果后再入库
- 🧭 **Prompt Recipes 示例库** — `examples/` 提供产品发布、融资路演、周报、课程课件、论文答辩、读书分享等常见场景的 `slides_plan.md` 起步模板
- 🪄 **模板克隆模式** — 丢一个 `.pptx` 进去，AI 会参考原模板的版式、配色和插画语汇，像上面那张图一样换成新内容
- 🎯 **自然语言精准编辑** — 直接说“改第 3 页副标题”“删掉页脚”“把三个数据换成新数字”，AI 会通过图生图只重生成目标页，尽量保持原风格和版式不变
- 🎮 **双产出** — 每页 PNG 高清原图 + 16:9 `.pptx` 直接用
- ⚡ **默认 10 路并发出图** — 10 页 ~30 秒出完
- 🧪 **先看一页再跑全量** — 默认建议先出封面给你确认，满意后再生成整套
- 🧾 **可追踪、可回滚** — 修改过哪些页、生成过哪些版本都能追踪，方便继续改
- 🖼️ **真实素材双模式** — 用户给的真实图默认保真嵌入；用户明确允许时，也可以作为参考图融合重绘
- 🧩 **可编辑模式（默认关闭）** — 用户明确要求时，把文字、基础图形、连接线和复杂主视觉拆成可单独编辑的 PowerPoint 对象

## ✅ 适合哪些用户场景

| 场景 | 适合程度 | 说明 |
| --- | --- | --- |
| 从主题生成一套新 PPT | 很适合 | 适合汇报、路演、培训、课程、产品介绍。 |
| 按公司模板仿一套新内容 | 很适合 | 上传 `.pptx` 模板，先出封面确认，再跑全量。 |
| 改标题、副标题、日期、页脚 | 很适合 | 当前最稳定的编辑场景。 |
| 更新数据卡片和关键数字 | 适合 | 可批量改，但交付前要逐项核对数字。 |
| 只改复杂多页 PPT 的某一页 | 适合 | 只更新目标页，其他页不重新生成。 |
| 密集表格、财报、法务长文 | 不建议直接承诺 | 小字和数字需要更严格人工验收。 |

## 🎨 在线模板画廊

目前收录的模板统一通过 [SlideCraft Template Gallery](https://slidecraft-template-gallery.vercel.app) 展示。你可以按场景和风格搜索、筛选，查看模板的真实生成效果；选中喜欢的模板后，复制 Prompt 并直接交给 Codex、Claude Code 或其他 AI 助手使用。

[![SlideCraft Template Gallery：浏览并复制喜欢的 PPT 模板](docs/assets/template-gallery.jpg)](https://slidecraft-template-gallery.vercel.app)

点进任意模板后，可以逐页预览整套版式，并复制模板 ID 或完整 Prompt：

[![SlideCraft Template Gallery 模板详情页：逐页预览并复制 Prompt](docs/assets/template-gallery-detail.jpg)](https://slidecraft-template-gallery.vercel.app/templates/abstract-art-showcase)

> 点击图片进入对应页面。模板会持续补充，README 不再维护容易过时的完整模板清单。

模板库不只看单张封面：新模板会用封面、章节、内容和数据等多类页面验证整套效果，并与现有版本对照。只有整体质量更好且关键页面没有明显退步时才会更新正式模板。

使用画廊风格时，复制喜欢的 Prompt 交给 AI 即可；需要沿用自己的品牌模板时，直接上传 `.pptx`，建议先生成一页确认效果，再生成整套 PPT。

---

## 🧪 修改能力测评

如果你关心“到底能不能稳定改 PPT”，先看这份面向用户的图文测评：

- **[`docs/edit_guide.md`](./docs/edit_guide.md)** — 标题替换、日期修改、删除页脚、数据更新、新增 logo、复杂多页只改一页，以及当前不足和交付前检查清单

核心结论：

| 能力 | 当前表现 |
| --- | --- |
| 改短文本 | 稳定，适合日常交付。 |
| 改多个明确元素 | 可用，建议一次说清楚“其他不要动”。 |
| 改数据页 | 可用，但必须核对数字。 |
| 加小图标 / logo | 可用；真实品牌 logo 需要提供素材。 |
| 原生 PPT 对象级编辑 | 默认模式仍是整页图片；明确启用可编辑模式后，可输出原生文本、shape、connector 和独立图片层。 |

<details>
<summary>开发者：查看内部编辑机制示意图</summary>

<img src="docs/assets/architecture_cn.jpg" width="100%" alt="system architecture">

</details>

---

## 🛠 手动安装与高级配置

普通用户优先使用上面的自然语言安装方式。需要自己管理仓库和环境时，可以手动安装：

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh --target claude   # Claude Code
# 或
bash install_as_skill.sh --target codex    # Codex
```

脚本会把 skill 装到对应 agent 的目录：

- Claude Code: `~/.claude/skills/gpt-image2-ppt-skills/`
- Codex: `~/.codex/skills/gpt-image2-ppt-skills/`

<details>
<summary><strong>API 直连与密钥配置</strong></summary>

如果你走 API 直连模式，需要给 agent 注入环境变量。推荐使用当前 agent 框架的标准配置，而不是把密钥写进业务项目根目录 `.env`：

- Claude Code：用户级 `~/.claude/settings.json`，或项目级 `.claude/settings.local.json`
- OpenClaw / 自定义 Agent：用 `apiKey` / env reference 引用系统环境变量
- CI / 服务器：用系统环境变量、Docker Compose、Kubernetes Secret 或 CI Secret
- standalone CLI：可设置 `GPT_IMAGE2_PPT_ENV=/path/to/private.env`，或使用 skill 安装目录下的 `.env` fallback

```bash
# 变量名如下：
OPENAI_BASE_URL=https://api.openai.com    # 或任意 OpenAI 兼容中转
OPENAI_API_KEY=sk-...                     # 必需
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto
```

> 在 **Codex** 里如果当前 agent 自带原生图片生成能力，可以直接走 `SKILL.md` 里的原生路径，**不必配置 `OPENAI_API_KEY`**。
>
> 🔒 **不会误吃密钥**：脚本只读取当前进程环境、平台注入变量、显式 `GPT_IMAGE2_PPT_ENV` 和 skill 安装目录 `.env` fallback，**不会**向上递归读调用者项目目录的 `.env`。
>
> 🪄 模板克隆模式和可编辑模式都需要本机可执行的 PPTX 渲染后端（Windows PowerPoint / macOS Keynote / LibreOffice）。模板克隆需要先把模板转成图片供 AI 看版式；可编辑模式需要把交付文件重新转成图片供 AI 验收。Skill 会先自动检查本机渲染能力；如果当前环境不支持，AI 会提示安装可用后端。模板克隆还可以改用手动导出的模板页面图片。

</details>

<details>
<summary><strong>模板克隆的 Vision 分析</strong></summary>

模板克隆模式下，skill 需要先"看懂"你的 `.pptx` 模板的视觉风格。**如果你的 AI 助手本身就是多模态的**（Claude Code 走 Claude Opus/Sonnet，Codex 走 GPT 多模态等），agent 会直接自己看图抽取风格，生成带 `reference_image` 的 `template_profile.json` 后通过 `--template-profile` 传给 CLI，**不需要额外配置**。

只有当你用的 agent 是纯文本模型时（例如只接入 DeepSeek 文本模型），才需要配下面这组环境变量，走一个独立的多模态模型来分析模板：

```bash
# 可选：模板克隆的 vision 分析（仅纯文本 agent 需要，多模态 agent 不用配）
VISION_BASE_URL=https://your-openai-compatible-relay.example.com/v1
VISION_API_KEY=sk-...
VISION_MODEL_NAME=gemini-3.1-pro-preview   # 或 gpt-4o / claude-3.5-sonnet 等任意多模态 SKU
```

> 支持任意兼容 OpenAI `/v1/chat/completions` 格式的多模态模型（Gemini / GPT-4o / Claude 等），与图片生成的 `gpt-image-2` 完全解耦——换 vision provider 不影响出图。

</details>

---

## 🆕 更新记录

- **2026-08-02 · 新增 233 套 PPT 模板**：在 `styles/xiamulingzi/` 新增 197 套莫兰迪风格、26 套朋克风格和 10 套科技风格模板，模板库由 32 套扩充至 265 套。
- **2026-08-01 · 模板克隆、蒸馏与在线画廊升级**：统一模板复用流程，增加多页面效果验证、新旧版对照和失败保护。同时通过 SlideCraft Template Gallery 集中展示目前收录的模板，支持搜索、筛选、查看真实效果和复制 Prompt 给 AI 使用。
- **2026-07-13 · 可编辑回渲染与轮次策略**：`--editable` 现在像模板克隆一样强制检查 PowerPoint / Keynote / LibreOffice，完成后自动输出 `editable_renders/page-XX.png` 供多模态验收；工作流改为效果优先、低成本检查可多轮、生成修复逐级升级并优先局部处理。
- **2026-07-11 · 可编辑模式**：用户明确要求可编辑交付时，完整视觉稿生成后可重建为原生文本、shape、connector 和独立图片层；重叠素材按 A1 原像素提取 → A2 遮挡补全 → B AI 分离/重生成路由处理。默认模式不受影响。
- **2026-05-31 · 真实素材双模式**：产品截图、logo、图表、表格、医学影像、证据截图等真实素材默认保真嵌入为独立图片对象；用户明确允许时，也可以作为参考图融合重绘。
- **2026-05-26 · 扩展风格库**：从公开渠道 500+ 个 PPT 模板中筛选补充 22 个优质风格，覆盖商务、学术、教育、餐饮、时尚、医疗、环保等场景。

---

## 🙏 致谢

- 感谢设计师 **@夏目玲子** 提供 233 套 PPT 模板。
- [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) — 风格 prompts 与早期 Skill 结构的上游参考。本项目最初把图片后端从 Nano Banana Pro 换成 OpenAI gpt-image-2，重写 3 套继承风格并新增 7 套，后续再扩展模板克隆、md-first 编排、PPTX 打包和结构化风格库。
- [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) — Claude Code skill SKILL.md frontmatter 写法参考。
- [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) — 模板复用与可编辑幻灯片思路参考。
- [ningzimu/image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill) — 图片转可编辑 PPT 与效果检查思路参考。
- [kdnsna/ultimate-ppt-master-skill](https://github.com/kdnsna/ultimate-ppt-master-skill) — PPT 内容组织、交付与审阅流程参考。
- [gnuhpc/ppt-master-plus](https://github.com/gnuhpc/ppt-master-plus) — 模板保留与分阶段质量检查思路参考。

除 NanoBanana-PPT-Skills 的早期上游关系和 html-ppt-skill 的格式参考外，上述项目主要用于公开方案对比。本项目没有复制其代码、模板或视觉素材。

## 💬 Community

[**LINUX DO — 中文开发者社区**](https://linux.do/)

### 微信交流群

欢迎大家有问题一起交流讨论。

<img src="docs/assets/wechat.jpg" width="300" alt="微信交流群">

## ⭐ Star History

[![Star History Chart](https://star-history.dera.page/svg?repos=JuneYaooo/gpt-image2-ppt-skills&type=Date)](https://star-history.dera.page/#JuneYaooo/gpt-image2-ppt-skills&Date)

---

## License

Apache License 2.0，详见 [LICENSE](./LICENSE)。
