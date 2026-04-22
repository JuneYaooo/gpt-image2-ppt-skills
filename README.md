# gpt-image2-ppt-skills

> 用 OpenAI 官方 `gpt-image-2` Images API 生成视觉风格强烈的 PPT 图片，自动产出可键盘翻页的 HTML viewer。Claude ​Code Skill。

## ✨ 特性

- 🎨 **三种内置风格**：渐变玻璃（gradient-glass）/ 清爽科技蓝（clean-tech-blue）/ 矢量插画（vector-illustration）
- 🪄 **模板克隆模式**：传一个 .pptx + 每页 PNG，vision 抽风格 + JSON Schema，新内容仿这个模板出图
- 🤖 **官方 OpenAI Images API**：`POST /v1/chat/completions`，模型 `gpt-image-2`
- 🔄 **OpenAI 兼容**：base_url 可换成任何兼容中转站
- 🖼️ **16:9 高清 PPT**：默认 1536×1024，`quality=high`
- 🎮 **HTML viewer**：键盘翻页、空格自动播放、ESC 全屏、触摸滑动
- 🧩 **逐页迭代**：`--slides 1,3,5` 只生成指定页，跑过的自动跳过

## 🚀 一键安装

```bash
git clone git@github.com:JuneYaooo/gpt-image2-ppt-skills.git
cd gpt-image2-ppt-skills
bash install_as_skill.sh
```

安装后 skill 会被装到 `~/.claude/skills/gpt-image2-ppt-skills/`，Claude ​Code 重启后自动识别。

## ⚙️ 配置

编辑 `~/.claude/skills/gpt-image2-ppt-skills/.env`：

```bash
OPENAI_BASE_URL=https://api.openai.com    # 或任意 OpenAI 兼容中转站
OPENAI_API_KEY=sk-...                     # 必需
GPT_IMAGE_MODEL_NAME=gpt-image-2          # 默认 gpt-image-2
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto

# 可选：仅模板克隆模式需要
VISION_BASE_URL=https://daydream88.fun/v1
VISION_API_KEY=sk-...
VISION_MODEL_NAME=gemini-3.1-pro-preview
```

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
python3 generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md

# 只生成第 1 页（用来先验证 API 通）
python3 generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 1

# 只重生第 3 和第 5 页
python3 generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 3,5
```

### 2.5 仿用户自己的 PPT 模板（v2）

```bash
# 默认模板克隆：vision 抽风格 + 每页 schema，按 schema 拼图片 prompt
python3 generate_ppt.py \
  --plan slides_plan.json \
  --template-pptx ./company-template.pptx \
  --template-images ./template_renders/   # 用户在 PowerPoint 里导出每页 PNG

# 高保真：把模板对应页作为 image reference 传给 gpt-image-2
python3 generate_ppt.py \
  --plan slides_plan.json \
  --template-images ./template_renders/ \
  --template-strict

# 强制重跑 vision（默认会读 template_cache/<sha256>.json 缓存）
python3 generate_ppt.py ... --rebuild-template-cache
```

第一次跑 vision 会调 `gemini-3.1-pro-preview`（在 `.env` 的 `VISION_*` 里配），输出每页的 `summary` + `json_schema` 缓存到 `template_cache/`。后续同一模板秒匹配。

### 3. 看产物

```
outputs/20260422_153012/
├── images/
│   ├── slide-01.png
│   ├── slide-02.png
│   └── ...
├── index.html       # 浏览器打开就能键盘翻页
└── prompts.json     # 每页完整 prompt，方便复盘
```

## 🎨 风格对比

| 风格 ID | 适用 | 关键词 |
| --- | --- | --- |
| `gradient-glass` | 科技产品、技术分享 | 渐变 / 极光 / 玻璃拟态 / Bento 网格 / 3D 物体 |
| `clean-tech-blue` | 融资路演、投资人演示 | 蓝白 / 克制 / McKinsey / 网格对齐 |
| `vector-illustration` | 教育培训、儿童内容 | 扁平矢量 / 黑色描边 / 复古配色 / 米色纸张 |

## 🛠️ 在 Claude ​Code 里调用

直接和 Claude 说：

> 帮我用 gpt-image2-ppt 生成一份关于 [你的主题] 的 5 页 PPT，风格用 clean-tech-blue。

Claude 会：
1. 问你具体内容
2. 写好 `slides_plan.json`
3. 跑 `generate_ppt.py --slides 1` 出封面让你确认
4. 跑全量并把 viewer 路径告诉你

## 📦 依赖

- Python 3.8+
- `requests`、`python-dotenv`（`pip install -r requirements.txt`）

## 🙏 致谢

- [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills) — 风格 prompts 与 viewer 模板的原始作者，本项目把图片后端从 Nano Banana Pro 换成了 OpenAI gpt-image-2。
- [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) — Claude ​Code skill SKILL.md frontmatter 写法参考。

## License

Apache License 2.0.
