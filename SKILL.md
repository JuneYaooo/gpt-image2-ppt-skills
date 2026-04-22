---
name: gpt-image2-ppt
description: Generate visually striking PPT slides via OpenAI's gpt-image-2 -- 10 curated styles (Spatial Glass / Tech Blue / Editorial Mono / Dark Aurora / Risograph / Wabi / Swiss Grid / Hand Sketch / Y2K Chrome / Retro Vector) plus a template-clone mode that mimics any user-supplied .pptx; ships an HTML viewer and a 16:9 .pptx. Use when the user asks to make a presentation, slides, deck, pitch deck, investor PPT, magazine-style PPT, or 做一份 PPT / 生成幻灯片 / 用 gpt-image 生成 PPT / 按这个模板生成 PPT.
---

# gpt-image2-ppt -- 用 gpt-image-2 生成 PPT

把一份 markdown 大纲（或 `slides_plan.json`）+ 一种视觉风格，直接喂给 OpenAI 官方 Images API（`gpt-image-2`），逐页出图，最后拼成一个键盘可翻页的 HTML viewer + 16:9 .pptx。

## 十种内置风格

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

> 风格选择原则：技术类首选 `dark-aurora` / `gradient-glass`，商务类首选 `clean-tech-blue` / `editorial-mono`，文化生活类首选 `japanese-wabi` / `vector-illustration`，潮文娱类首选 `risograph` / `y2k-chrome`，学术类首选 `swiss-grid`，工作坊与早期创意类首选 `hand-sketch`。

## 模板克隆模式

直接给 skill 一个 .pptx 模板，后续所有页都仿这个模板。

```bash
# 一行：自动渲染 + vision 抽风格 + 出图。本机有 LibreOffice 或 docker 镜像即可
python3 generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-strict
```

`--template-strict` 表示每页都把模板对应页作为 image reference 喂给 gpt-image-2，仿真度最高。

### 模板渲染：本机不需要操作 PowerPoint

skill 自带 `render_template.py`，把 .pptx 自动渲染成每页 PNG，存到 `<cwd>/template_renders/<stem>/page-NN.png`。

后端按优先级自动挑：
1. 本机 `libreoffice` / `soffice` 命令（最快）
2. 本机 docker + `linuxserver/libreoffice` 镜像（首次拉 ~2.5GB）
3. PDF -> PNG 走 `pymupdf`（已在 requirements）；没装就用 `pdf2image` + poppler

如果两种 LibreOffice 都没有，会让用户手动从 PowerPoint/Keynote/WPS 导出每页 PNG，命名 `page-01.png` 起按字典序对应页码。

跑 `generate_ppt.py --template-pptx ...` 时如果省略 `--template-images` 会自动调一次渲染；也可以手动先跑一次：

```bash
python3 render_template.py company-template.pptx
# -> <cwd>/template_renders/company_template/page-01.png ... page-NN.png
```

### 仿模板的两层缓存

| 资料 | 路径 | 用途 |
| --- | --- | --- |
| 模板每页 PNG | `<cwd>/template_renders/<stem>/page-NN.png` | LibreOffice 一次渲染长期复用 |
| Vision 风格分析 | `<cwd>/template_cache/<sha256>.json` | gemini-3.1-pro-preview 一次分析长期复用 |
| 生成产物 | `<cwd>/outputs/<timestamp>/` | 每次新跑都新目录 |

三者都在调用者 cwd 下，与项目自然同进退；建议把 `template_renders/`、`template_cache/`、`outputs/` 加进项目的 `.gitignore`。

**vision 模型**：模板分析走单独的 OpenAI 兼容多模态 chat completions（默认 `gemini-3.1-pro-preview`，配在 `.env` 的 `VISION_*` 里），与图片生成的 `gpt-image-2` 解耦。

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

# 可选：模板克隆模式才需要（vision 分析独立 provider）。
# 不内置默认 endpoint，请填你自己信任的服务，否则就别填这一组。
# VISION_BASE_URL=https://your-openai-compatible-relay.example.com/v1
# VISION_API_KEY=sk-...
# VISION_MODEL_NAME=gemini-3.1-pro-preview
```

> **安全提示**：脚本只从 `<script_dir>/.env`、`~/.claude/skills/.../env`、`~/skills/.../env` 与显式 `GPT_IMAGE2_PPT_ENV` 加载凭据，**不会**向上递归读取项目目录里的 `.env`，避免误吃无关密钥。

## 生成流程（内置风格）

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
3. 选风格：从上面 10 套里挑一个，对应 `styles/<id>.md`
4. 调脚本：
   ```bash
   python3 generate_ppt.py --plan slides_plan.json --style styles/editorial-mono.md
   ```
5. 产物在 `<cwd>/outputs/<timestamp>/`：
   - `images/slide-XX.png` -- 每页 PNG（16:9，1536x1024）
   - `index.html` -- HTML viewer，方向键翻页、空格自动播放、ESC 全屏
   - `prompts.json` -- 每页用到的完整 prompt（便于复盘 / 二次微调）
   - `<title>.pptx` -- 16:9 整页填充图片的 .pptx，分享 / 投影直接用

## 生成流程（模板克隆）

1. **拿到模板 .pptx**（用户提供 / 内部模板库 / 网络下载）
2. **（可选）先单独渲染并人工挑选**----大模板（>15 页）建议先 `python3 render_template.py xxx.pptx`，再从 `template_renders/<stem>/` 里挑 8-12 张代表页复制到 `template_renders/<stem>_curated/`，供 vision 分析。页数越精，layout 命中越准
3. **生成 slides_plan.json**：每页 `slide_number` / `page_type` (`cover` / `content` / `data` / 等) / `content`；想精准对位时加 `layout_id`，命名按 `layout-NN`（NN = 模板第 N 页 / 你期望对应的模板页编号）
4. **跑 generate_ppt.py**：
   ```bash
   python3 generate_ppt.py \
     --plan slides_plan.json \
     --template-pptx xxx.pptx \
     --template-images template_renders/xxx_curated \
     --template-strict --slides 1
   ```
   先 `--slides 1` 出封面冒烟，效果 OK 再跑全量
5. **告知用户产物路径**

### 模板页面挑选 / 复用原则

**核心原则：尽量做到 1 page : 1 layout**----同一份 deck 里每个 slide 用不同的模板页作 reference，观众会觉得每页都是新内容；如果同一个独特 layout 出现 2-3 次，观众下意识会想"为什么又是这页"。

vision 分析时会给每个 layout 标 `reuse_friendly`：

| reuse_friendly | 典型 layout | 多次使用的代价 |
| --- | --- | --- |
| `false`（不可复用，(!) 强警告） | 封面、3 个具名角色插画页、独特场景图（雪山/广播塔/复古收音机）、5 步骤 zigzag 各步独有图标、novelty 数据中央装置 | 视觉重复非常明显，观众会困惑 |
| `true`（可复用，但仍建议错开，(i) 弱提示） | 纯文字、卡片网格、通用列表、章节小节标题 | 不致命，但平白浪费模板里的其它好版式 |

Claude 在搭 plan 时的执行策略：
1. **优先把模板里 N 个不同 layout 分配给 N 页 slide**（N 不够就在 SKILL 里看 reuse_friendly=true 的部分挑能复用的）
2. **如果 plan 里某页内容结构非常相似（比如多个"5 步骤流程"），先尝试改写内容用不同 layout 表达**（4 步骤 + 5 步骤分别用不同流程页），而不是同一个 zigzag 用两次
3. **冒烟跑完后，看 `Layout 复用检测` 那段输出**：(!) 必须改，(i) 看情况改；改 plan 里相应 slide 的 `layout_id` 即可
4. **看完 cache JSON 选 layout**：`cat <cwd>/template_cache/<sha256>.json | jq '.layouts[] | {id, page_type, reuse_friendly, summary}'` 一眼看清模板有哪些版式可挑

`generate_ppt.py` 在派发任务前会自动跑一次复用检测，把警告打到终端，不阻塞执行。

## Skill 调用规范

当用户说"做一份 PPT" / "生成幻灯片"时：

1. **先问三件事**（不要直接动手）：
   - 内容 / 页数 / 观众是谁？
   - 风格偏好？按"十种内置风格"表的场景类目映射推荐 1-2 个；**或者用户上传自己的 .pptx 模板**（走 `--template-pptx`，自动渲染）
   - 是否需要单页测试一张图先看效果（`--slides 1`）
2. **生成 slides_plan.json**
3. **跑 generate_ppt.py**，先 `--slides 1` 出封面冒烟，效果 OK 再跑全量
4. **告知用户产物路径**，让他在浏览器打开 `outputs/<timestamp>/index.html` 或者 `<title>.pptx`

## 仅生成部分页

```bash
python3 generate_ppt.py --plan my_plan.json --style styles/dark-aurora.md --slides 1,3,5
```

跑过的页有同名 PNG 时会自动跳过，方便逐页迭代。

## 文件结构

```
gpt-image2-ppt-skills/
|---- SKILL.md                # 本文件
|---- README.md               # 项目说明
|---- generate_ppt.py         # 主入口（CLI）
|---- render_template.py      # PPTX -> 每页 PNG 的辅助脚本（CLI + library）
|---- image_generator.py      # gpt-image-2 wrapper（支持 reference image）
|---- template_analyzer.py    # PPT 模板剖析器（vision + 缓存）
|---- slides_plan.json        # 示例 plan（10 页商业计划书）
|---- styles/                 # 10 套内置风格
|   |---- gradient-glass.md           dark-aurora.md
|   |---- clean-tech-blue.md          risograph.md
|   |---- vector-illustration.md      japanese-wabi.md
|   |---- editorial-mono.md           swiss-grid.md
|   |---- hand-sketch.md              y2k-chrome.md
|---- templates/viewer.html   # HTML viewer 模板
|---- install_as_skill.sh     # 一键安装到 ~/.claude/skills/
|---- requirements.txt        # requests + python-dotenv + python-pptx + jsonschema + pymupdf
\---- .env.example
```

调用时产生的运行时目录都在 `<cwd>` 下：
```
<your-project>/
|---- template_renders/<stem>/page-NN.png   # PPTX 渲染（render_template.py）
|---- template_cache/<sha256>.json          # vision 风格分析缓存
\---- outputs/<timestamp>/                  # 每次生成产物
```

## License

Apache License 2.0.
