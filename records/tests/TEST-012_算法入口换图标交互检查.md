# TEST-012 算法入口换图标交互检查

2026-11-03，CHG-011，仅更换导航装饰图标。

实际在阅读站根目录执行既有 `tools/check_interactions.cjs`，使用 VS Code Server 已安装的现代 Node，`NODE_PATH=/usr/share/nodejs`。检查实际 `file://` 入口、两组研究导航、五类结果页及知识锚点、全文搜索、公式、书签、PDF和协议定位。结果见 `校验/交互逻辑校验.json`；未新增测试脚本，未执行通信实验或此次真实浏览器截图。

实际退出码0，PASS，无DOM脚本错误；仅有既有Node punycode弃用提示。`git diff --check`通过。
