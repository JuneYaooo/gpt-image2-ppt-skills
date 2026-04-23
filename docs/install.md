# gpt-image2-ppt-skills 安装指南（给 AI agent 读）

> 本文档是**让 AI 助手自动完成安装**的可执行指引。Claude Code / OpenClaw / Codex / Cursor / Trae / Hermes Agent 等任一 agent 按以下步骤执行即可。
>
> 人类用户请**不要**手动照抄下面的步骤，直接把这份 URL 扔给你的 AI 助手，它自己会跑通。

## 项目一句话介绍

`gpt-image2-ppt-skills` 是一个 Claude Code / OpenClaw Skill，用 OpenAI `gpt-image-2` 生成视觉强烈的 PPT（10 套内置风格 + 支持仿任意 `.pptx` 模板），产出 HTML viewer + 16:9 `.pptx`。

仓库：https://github.com/JuneYaooo/gpt-image2-ppt-skills

## 前置依赖（agent 请先检查）

- **必需**：`git`、`python3`（3.8+）、`pip`
- **可选**：`libreoffice` 本机命令，或 `docker` + `linuxserver/libreoffice` 镜像（仅模板克隆模式需要，用来把 `.pptx` 渲染成 PNG）

如果缺 `git` / `python3`，先用系统包管理器装好；`libreoffice` 可以留到用户要用模板克隆模式时再装。

## 安装步骤

### 1. 克隆仓库到临时目录

```bash
git clone https://github.com/JuneYaooo/gpt-image2-ppt-skills.git /tmp/gpt-image2-ppt-skills
cd /tmp/gpt-image2-ppt-skills
```

### 2. 跑安装脚本

```bash
bash install_as_skill.sh
```

这一步会：
- 把项目文件拷贝到 `~/.claude/skills/gpt-image2-ppt-skills/`
- `pip install -r requirements.txt` 装齐 Python 依赖
- 从 `.env.example` 生成 `~/.claude/skills/gpt-image2-ppt-skills/.env` 骨架

安装脚本是**交互式**的，如果目标目录已存在会问是否覆盖；agent 可以用 `yes | bash install_as_skill.sh` 自动选"是"，或先检查目录是否存在再决定。

### 3. 问用户要 API key 并写进 .env

agent 需要主动问用户：

> 请提供你的 OpenAI API key（或任意 OpenAI 兼容中转的 base_url + key）。

然后把以下内容写进 `~/.claude/skills/gpt-image2-ppt-skills/.env`（保留已有注释，只填值）：

```bash
OPENAI_BASE_URL=https://api.openai.com    # 或用户提供的兼容中转 URL
OPENAI_API_KEY=sk-...                     # 用户提供的 key（必需）
GPT_IMAGE_MODEL_NAME=gpt-image-2
GPT_IMAGE_QUALITY=high                    # low / medium / high / auto
```

> 如果用户没有 OpenAI 官方 key，agent 可以告诉用户：本 skill 也支持 `--backend codex` 复用本地 codex CLI 登录，不需要在本 skill 配 key；或者用任意 OpenAI 兼容中转站（把 `OPENAI_BASE_URL` 改成中转站地址即可）。

### 4. 提示用户重启 agent

装完之后，告诉用户：

> 已装到 `~/.claude/skills/gpt-image2-ppt-skills/`。请**重启 Claude Code**（或你正在用的 agent）让 skill 生效。

### 5.（可选）清理临时目录

```bash
rm -rf /tmp/gpt-image2-ppt-skills
```

## 冒烟测试（用户重启 agent 后）

告诉用户直接跟 agent 说：

> 帮我用 **gpt-image2-ppt** 生成一份关于「猫为什么是液体」的 3 页 PPT，风格用 `gradient-glass`。

正常的话 agent 会自己写 `slides_plan.json`、跑 `scripts/generate_ppt.py --slides 1` 先出封面、再跑全量，最后给出 HTML viewer 和 `.pptx` 的路径。

## 常见问题（给 agent 参考）

- **`ModuleNotFoundError: pymupdf`** → 重跑 `pip install -r ~/.claude/skills/gpt-image2-ppt-skills/requirements.txt`
- **`libreoffice: command not found`**（仅模板克隆模式）→ Linux: `apt install libreoffice`；macOS: `brew install --cask libreoffice`；或让用户切换到内置 10 套风格之一，不走模板克隆
- **`OPENAI_API_KEY 未设置`** → 回到步骤 3，检查 `.env` 文件路径和内容
- **Claude Code 识别不到 skill** → 确认目录是 `~/.claude/skills/gpt-image2-ppt-skills/`（不是其它路径），并且完全重启过 Claude Code

## 完成标志

以下三条都满足即视为安装成功：

1. `~/.claude/skills/gpt-image2-ppt-skills/SKILL.md` 存在
2. `~/.claude/skills/gpt-image2-ppt-skills/.env` 存在且包含 `OPENAI_API_KEY=sk-...`（非占位符）
3. agent 重启后，用户用自然语言要求生成 PPT 时能触发本 skill

装完不用逐字读 `SKILL.md`，但需要告诉用户："你可以直接用自然语言要 PPT，也可以把任意 `.pptx` 模板丢给我做克隆。"
