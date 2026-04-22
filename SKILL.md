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
   - 风格偏好？默认推荐：技术分享 → `gradient-glass`，路演 → `clean-tech-blue`，教育 → `vector-illustration`
   - 是否需要单页测试一张图先看效果（`--slides 1`）
2. **生成 slides_plan.json**：每页 `slide_number` / `page_type` (`cover` / `content` / `data`) / `content`
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
├── image_generator.py      # gpt-image-2 wrapper（POST /v1/images/generations）
├── slides_plan.json        # 示例 plan（10 页商业计划书）
├── styles/
│   ├── gradient-glass.md
│   ├── clean-tech-blue.md
│   └── vector-illustration.md
├── templates/
│   └── viewer.html         # HTML viewer 模板
├── install_as_skill.sh     # 一键安装到 ~/.claude/skills/
├── requirements.txt        # requests + python-dotenv
└── .env.example
```

## License

Apache License 2.0.
