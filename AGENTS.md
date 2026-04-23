# AGENTS.md -- 给 codex / aider / cursor 等 agent 的入口说明

本仓库是一个用 OpenAI `gpt-image-2` 生成 PPT 幻灯片的工具包，**权威文档在 [`SKILL.md`](./SKILL.md)**。任何涉及"做一份 PPT / 生成幻灯片 / 出图 / 改风格 / 按模板仿作"的请求，都先完整读 `SKILL.md` 再动手，不要凭本文件的摘要就开跑 -- 下面只是索引。

## 一分钟索引

- **主入口 CLI**：`python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/<id>.md`
- **内容源稿**：先写 `slides_plan.md`（人审阅），再 `python3 scripts/md_to_plan.py slides_plan.md -o slides_plan.json`；json 标为 derived，不手改
- **十种内置风格**：见 `styles/` 目录 + `SKILL.md` 顶部表格
- **模板克隆**：`--template-pptx path/to/xxx.pptx --template-strict`，vision 分析 + 缓存细节在 `SKILL.md` 的"模板克隆模式"一节；**如果你自己就是多模态 agent**(多模态 Claude / GPT / 等)，可以直接 `Read` `template_renders/<stem>/page-*.png` 自己抽风格写 `template_cache/<sha256>.json`，不用外挂 `VISION_*`
- **冒烟策略**：先 `--slides 1` 出封面，确认后再跑全量
- **产物**：`<cwd>/outputs/<timestamp>/{images/, index.html, prompts.json, <title>.pptx}`

## 调用规范（对 agent 的硬约束）

1. **先问三件事**：内容 / 观众、风格偏好（或是否带 .pptx 模板）、是否先 `--slides 1` 冒烟
2. **永远先 md 后 json**：用户改文案改 md，不手改 json
3. **先冒烟再全量**：`--slides 1` 的封面效果用户认可后再跑余下页
4. **告知产物路径**：跑完把 `outputs/<timestamp>/index.html` 和 `.pptx` 路径明确告诉用户

## 凭据 / backend

- 默认后端 `openai`，需在 scoped 位置（`<script_dir>/.env` 或 `$GPT_IMAGE2_PPT_ENV`）配 `OPENAI_API_KEY`
- **如果你就是 codex**：codex 自己就是多模态 + 自带出图能力,可以直接加 `--backend codex` 复用自己的登录,无需在本 skill 配 key(慢一点,见 `SKILL.md` "可选：走 codex 自带的多模态 + 出图能力" 一节的 tradeoff)
- 脚本**不会**向上递归读取项目目录的 `.env`，避免误吃无关密钥

## 不要做的事

- 不要手改 `slides_plan.json`（改 md 再转）
- 不要跳过 `SKILL.md`"模板页面挑选 / 复用原则"直接用同一个 layout 给多页 slide 当 reference
- 不要在没有 `OPENAI_API_KEY` 且没有本地 codex CLI 的情况下强跑 -- 先检查环境

## 同步提醒

本文件是薄索引。如果 `SKILL.md` 有新增章节或流程变更，只在 `SKILL.md` 里维护，本文件的锚点列表按需补；**正文描述不要复制到这里**，避免两边漂移。
