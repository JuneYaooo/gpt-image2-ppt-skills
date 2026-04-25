<div align="center">

# gpt-image2-ppt-skills

**用 OpenAI `gpt-image-2` 一键生成视觉强烈的 PPT。**

Claude Code / OpenClaw Skill。装进 agent 后，用一句自然语言生成 16:9 高清图片 + 可键盘翻页的 HTML viewer + 打包好的 `.pptx`，也可以仿任意 `.pptx` 模板出全新内容。

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

## ✨ 能做什么

- 🎨 **十套精选风格** — Spatial Glass / Tech Blue / Editorial Mono / Dark Aurora / Riso / Wabi / Swiss Grid / Hand Sketch / Y2K Chrome / Vector Illustration，每套都细分 `cover` / `content` / `data` 三种构图
- 🪄 **模板克隆模式** — 丢一个 `.pptx` 进去，自动渲染 + vision 抽风格 + JSON Schema 复刻，像上面那张图一样仿版式换内容
- 🎮 **HTML viewer + `.pptx` 双产出** — 键盘翻页 / 空格自动播放 / ESC 全屏 / 触摸滑动，同时打包成 16:9 `.pptx` 直接用
- ⚡ **默认 10 路并发出图** — 10 页 ~30 秒出完
- 🔁 **双后端** — `openai` 直调（需 key）或 `codex` CLI（复用 codex 登录，无需在本 skill 配 key）
- 🤖 **官方 OpenAI Images API** — 模型 `gpt-image-2`，`base_url` 可换任意 OpenAI 兼容中转

## 🎨 十种内置风格

> 下图为 10 套风格在同一主题「**如何用 gpt-image-2 做 PPT**」下各生成一张封面的对照。全部由 `gpt-image-2` 直出，未经 PS。

![10 种风格封面对照 · 同一主题直出](docs/assets/style-gallery.jpg)

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

---

## 🚀 安装

### 方式一：让 AI 自己装（推荐）

把下面这段 prompt 丢给你的 AI 助手（Claude Code / OpenClaw / Codex / Cursor / Trae / Hermes Agent 都行），它会自动完成安装：

```
帮我安装 gpt-image2-ppt-skills：
https://raw.githubusercontent.com/JuneYaooo/gpt-image2-ppt-skills/main/docs/install.md
```

agent 会自己 clone 仓库、跑安装脚本、问你要 API key、提示你重启。

### 方式二：手动安装

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh
```

脚本会把 skill 装到 `~/.claude/skills/gpt-image2-ppt-skills/`，Claude Code 重启后自动识别。

然后填一个 key 就能用：

```bash
# ~/.claude/skills/gpt-image2-ppt-skills/.env
OPENAI_BASE_URL=https://api.openai.com    # 或任意 OpenAI 兼容中转
OPENAI_API_KEY=sk-...                     # 必需
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto
```

> 🔒 **不会误吃密钥**：只从 skill 自己目录的 `.env` 或显式 `GPT_IMAGE2_PPT_ENV` 加载，**不会**向上递归读项目目录的 `.env`。
>
> 🪄 模板克隆模式额外需要本机 `libreoffice` 或 docker `linuxserver/libreoffice` 镜像（用来把 `.pptx` 渲染成 PNG）。

---

## 🛠 在 Claude Code 里怎么用

装完直接跟 Claude 说人话就行：

> 帮我用 **gpt-image2-ppt** 生成一份关于 **[你的主题]** 的 5 页 PPT，风格用 `dark-aurora`。

仿模板同理：

> 我这有一个 `company-template.pptx`，帮我按这个模板做一份关于 **[你的主题]** 的 5 页 PPT。

Claude 会自己写 `slides_plan`、先出一页封面让你确认、再跑全量，把 HTML viewer + `.pptx` 路径告诉你。

> 🧑‍💻 想自己写脚本调 CLI 而不走 agent？看 [`SKILL.md`](./SKILL.md)，CLI 参数、文件布局都在那。

---

## 🙏 致谢

- [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) — 风格 prompts 与 viewer 模板的原始作者。本项目把图片后端从 Nano Banana Pro 换成了 OpenAI gpt-image-2，重写了继承自上游的 3 套风格并新增 7 套（共 10 套），另加入模板克隆模式（vision 抽风格仿任意 `.pptx`）、md-first 编排流程、`.pptx` 自动打包、codex CLI 备用后端等新功能。
- [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) — Claude Code skill SKILL.md frontmatter 写法参考。

---

## 💬 Community

[**LINUX DO — 中文开发者社区**](https://linux.do/)

---

## License

Apache License 2.0，详见 [LICENSE](./LICENSE)。
