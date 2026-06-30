# Prompt Recipes / 示例库

这个目录提供一组可直接复用的 `slides_plan.md` 示例，用来帮助新用户从常见 PPT 场景快速开始。

它不是一个新的 Skill；它是根目录 `SKILL.md` 的辅助资源。agent 在用户没有提供完整大纲时，可以把这里的 recipe 当作“内容结构参考”，先生成一份新的 `slides_plan.md` 给用户确认，再进入正常的 `md_to_plan.py` 和 `generate_ppt.py` 流程。

每个 recipe 都遵循本 skill 的内容源稿格式：

```markdown
---
title: 示例标题
---

## 1. [cover] 封面标题
页面内容

## 2. [content] 内容页标题
页面内容

## 3. [data] 数据页标题
页面内容
```

使用方式：

### 1. 作为 agent 起步模板

当用户只给出场景和主题时，例如：

```text
帮我做一份 AI 产品发布 PPT
```

agent 应该：

1. 判断场景命中 `product-launch/`。
2. 读取 `product-launch/recipe.md`，确认推荐风格、页数和注意事项。
3. 参考 `product-launch/slides_plan.md` 的页序结构。
4. 改写成用户自己的主题、产品、受众和内容。
5. 把新写的 `slides_plan.md` 给用户确认。
6. 用户确认后再转 `slides_plan.json` 并生成封面冒烟。

不要直接把示例里的虚构产品、公司、数据原样当成用户成品。

### 2. 作为本地 smoke test

新用户也可以直接用示例跑通链路：

```bash
python3 scripts/md_to_plan.py examples/product-launch/slides_plan.md -o slides_plan.json
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 1
```

建议先用 `--slides 1` 生成封面冒烟，确认风格和方向后再全量生成。`slides_plan.json` 是派生文件，不需要提交。

### 3. 在 skill 流程中的位置

```text
用户需求
-> 若内容结构不完整，选择 examples/<recipe>
-> 参考 recipe 写新的 slides_plan.md
-> 用户确认文案和页数
-> scripts/md_to_plan.py 转 slides_plan.json
-> 读取 styles/<id>.md
-> scripts/generate_ppt.py 生成封面冒烟
-> 用户确认后全量生成 PPTX
```

## Recipes

| 场景 | 推荐风格 | 页数 | 目录 |
| --- | --- | ---: | --- |
| 产品发布 | `gradient-glass` | 6 | `product-launch/` |
| 融资路演 | `clean-tech-blue` | 8 | `investor-pitch/` |
| 周报 / 月报 | `meeting-agenda` | 6 | `weekly-report/` |
| 课程课件 | `vector-illustration` | 7 | `courseware/` |
| 论文答辩 | `final-year-project-thesis-defense` | 8 | `thesis-defense/` |
| 读书分享 | `editorial-mono` | 6 | `book-sharing/` |

## 维护原则

- `slides_plan.md` 是 source of truth；不要手写或手改派生出的 `slides_plan.json`。
- 每个 recipe 保持一个清晰场景，不追求覆盖所有变体。
- 页面文字应短而可展示，避免把长文整段塞进一页。
- 如果某页包含密集数字或事实，请在交付前人工核对。
