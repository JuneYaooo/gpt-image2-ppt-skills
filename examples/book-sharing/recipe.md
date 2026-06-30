# Book Sharing / 读书分享

适合读书会、团队学习、个人知识输出和文化类分享。这个 recipe 以《深度工作》为例，展示 6 页结构：书籍定位、核心观点、关键框架、个人启发和行动建议。

推荐风格：`editorial-mono`

推荐命令：

```bash
python3 scripts/md_to_plan.py examples/book-sharing/slides_plan.md -o slides_plan.json
python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/editorial-mono.md --slides 1
```

适合替换的内容：

- 书名和作者
- 你最认同的 3 个观点
- 个人案例或团队实践
- 讨论问题

注意事项：

- 读书分享不需要复述整本书，重点是观点选择和自己的理解。
- 如果使用书封图片，请确认版权和使用场景。
