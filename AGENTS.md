# AGENTS.md -- 给 codex / aider / cursor 等 agent 的入口说明

本仓库是一个用 OpenAI `gpt-image-2` 生成 PPT 幻灯片的工具包，**权威文档在 [`SKILL.md`](./SKILL.md)**。任何涉及"做一份 PPT / 生成幻灯片 / 出图 / 改风格 / 按模板仿作"的请求，都先完整读 `SKILL.md` 再动手，不要凭本文件的摘要就开跑 -- 下面只是索引。

## 一分钟索引

- **主入口 CLI（API 直连 / 非 Codex 原生出图路径）**：`python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/<id>.md`
- **内容源稿**：先写 `slides_plan.md`（人审阅），再 `python3 scripts/md_to_plan.py slides_plan.md -o slides_plan.json`；json 标为 derived，不手改
- **场景起步模板**：用户只有模糊主题、没有完整大纲时，先看 `SKILL.md` 的“场景 recipes”规则，并参考 `examples/` 写新的 `slides_plan.md`
- **十种内置风格**：见 `styles/` 目录 + `SKILL.md` 顶部表格
- **模板克隆**：`--template-pptx path/to/xxx.pptx --template-strict`，vision 分析 + 缓存细节在 `SKILL.md` 的"模板克隆模式"一节；**如果你自己就是多模态 agent**(多模态 Claude / GPT / 原生 Codex 等)，可以直接 `Read` `template_renders/<stem>/page-*.png` 自己抽风格写 `template_profile.json`，用 `--template-profile` 传入，不用外挂 `VISION_*`
- **冒烟策略**：API 直连 / 非 Codex 原生路径先 `--slides 1` 出封面；如果你自己就是带原生出图能力的 Codex，则直接用当前会话的 image_generation tool 生成第 1 页 PNG 做冒烟，不要经 `--backend codex`
- **产物**：`<cwd>/outputs/<timestamp>/{images/, prompts.json, metadata.json, <title>.pptx}`

## 调用规范（对 agent 的硬约束）

1. **先问三件事**：内容 / 观众、风格偏好（或是否带 .pptx 模板）、是否先单页冒烟
2. **永远先 md 后 json**：用户改文案改 md，不手改 json
3. **先冒烟再全量**：API 直连用 `--slides 1`；Codex 原生出图用当前会话 image_generation tool 先生成封面 PNG
4. **告知产物路径**：跑完把 `outputs/<timestamp>/` 和 `.pptx` 路径明确告诉用户

## 凭据 / backend

- 默认后端 `openai`，需通过 agent 配置 / 系统环境变量注入 `OPENAI_API_KEY`；standalone CLI 可用 `$GPT_IMAGE2_PPT_ENV` 或 skill 安装目录 `.env` 作为 fallback，**不要**写进调用者业务项目根目录 `.env`
- **如果你就是 codex**：走「原生 image_generation 出图」路径——直接用你自带的 `image_generation` tool 出图，**不要**跑 `generate_ppt.py --backend codex`（那是给 Claude Code 等非 codex caller 用的，会 spawn 一个多余的 codex 子进程）。完整流程见 `SKILL.md` 的「如果你就是 Codex agent」一节
- 脚本**不会**向上递归读取调用者项目目录的 `.env`，避免误吃业务项目密钥

## 不要做的事

- 不要手改 `slides_plan.json`（改 md 再转）
- 不要跳过 `SKILL.md`"模板页面挑选 / 复用原则"直接用同一个 layout 给多页 slide 当 reference
- 不要在没有 `OPENAI_API_KEY`、不能走 Codex 原生出图、且没有本地 codex CLI 的情况下强跑 -- 先检查环境

## 同步提醒

本文件是薄索引。如果 `SKILL.md` 有新增章节或流程变更，只在 `SKILL.md` 里维护，本文件的锚点列表按需补；**正文描述不要复制到这里**，避免两边漂移。
