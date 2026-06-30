# Thesis Defense / 论文答辩

适合本科毕设、硕士论文、博士开题或项目结题。这个 recipe 使用虚构题目 `多模态学习系统的交互设计研究`，展示 8 页答辩结构。

推荐风格：`final-year-project-thesis-defense`

推荐命令：

```bash
python3 scripts/md_to_plan.py examples/thesis-defense/slides_plan.md -o slides_plan.json
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/final-year-project-thesis-defense.md --slides 1
```

适合替换的内容：

- 论文题目、作者、导师和学院
- 研究问题与方法
- 实验数据和结论
- 创新点与不足

注意事项：

- 答辩中的数据、图表和引用必须人工核对。
- 如果有真实实验图或系统截图，建议作为外部真实图片后贴。
