# Courseware / 课程课件

适合培训课、公开课、企业内训和知识科普。这个 recipe 用 `AI 写作入门课` 展示 7 页课程结构：目标、概念、方法、案例、练习和总结。

推荐风格：`vector-illustration`

推荐命令：

```bash
python3 scripts/md_to_plan.py examples/courseware/slides_plan.md -o slides_plan.json
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/vector-illustration.md --slides 1
```

适合替换的内容：

- 课程主题和受众
- 三个核心概念
- 练习题和案例
- 课后任务

注意事项：

- 课程页要保留停顿和互动，不要把讲稿全文放进幻灯片。
- 每页最好只承载一个学习目标。
