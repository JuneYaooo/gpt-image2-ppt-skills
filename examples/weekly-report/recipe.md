# Weekly Report / 周报与月报

适合项目例会、团队周报、经营月报和阶段复盘。这个 recipe 使用虚构的 `CityOps` 项目，展示如何把进度、风险、数据和下周计划组织成 6 页。

推荐风格：`meeting-agenda`

推荐命令：

```bash
python3 scripts/md_to_plan.py examples/weekly-report/slides_plan.md -o slides_plan.json
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/meeting-agenda.md --slides 1
```

适合替换的内容：

- 周期时间
- 项目指标
- 本周完成事项
- 风险和需要决策的问题

注意事项：

- 周报不适合做成营销页，信息密度可以略高，但每页仍需有一个中心结论。
- 数字和负责人信息要在生成后人工核对。
