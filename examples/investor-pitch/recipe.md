# Investor Pitch / 融资路演

适合早期项目向投资人说明市场、问题、产品、商业模式和增长计划。这个 recipe 使用虚构公司 `FlowLedger`，展示一个 8 页种子轮路演结构。

推荐风格：`clean-tech-blue`

推荐命令：

```bash
python3 scripts/md_to_plan.py examples/investor-pitch/slides_plan.md -o slides_plan.json
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/clean-tech-blue.md --slides 1
```

适合替换的内容：

- 市场规模、收入和增长数据
- 客户画像和使用场景
- 竞争优势和团队背景
- 融资金额和资金用途

注意事项：

- 数据页中的数字只是示例，占位后必须替换成真实数字。
- 如果涉及真实财务数据，生成后需要人工逐项核对。
