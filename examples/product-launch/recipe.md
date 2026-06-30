# Product Launch / 产品发布

适合发布新功能、新应用、新硬件概念或 AI 产品。这个 recipe 用虚构产品 `Aurora Notes` 展示一个 6 页发布会结构：从痛点、产品主张、核心能力、使用场景到上线计划。

推荐风格：`gradient-glass`

推荐命令：

```bash
python3 scripts/md_to_plan.py examples/product-launch/slides_plan.md -o slides_plan.json
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 1
```

适合替换的内容：

- 产品名称和一句话定位
- 三个核心能力
- 发布节奏和试用入口
- 目标用户或行业场景

注意事项：

- 产品发布页适合强视觉封面和少量关键词。
- 如果要放真实产品截图，建议走 `external_image` 工作流，而不是让模型重画截图。
