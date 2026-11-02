# TEST-007 网页间距与原有交互核验

2026-11-02。排版工程检查，3GPP/新增数学推导不适用，没有无线实验或业务抓包。

## 语法与DOM交互

在阅读站仓库根目录实际执行：

```bash
node --check 网页/typography.js
```

exit0。扩充既有`tools/check_interactions.cjs`，使用真实离线入口、catalog及正文脚本，核对实际基础知识中的“两个 Priority = 5 的 UE”，以及动态插入的跨粗体/内联代码文字、`8 Mbps`、`0.5 ms`、`2 Mbit/s`。比对原数据：内联/多行代码文本、公式DOM、链接地址与标题ID一致；URI查询参数、文件名及协议文字保持，重复处理不增加空格。书签、全文搜索、PDF页序控件、38.321条款5.4.5定位与主题切换均通过。

环境实际失败及修复：直接`node tools/check_interactions.cjs`退出1，系统Node无法解析既有测试中的可选链，尚未加载网页；换用VS Code自带Node后退出1，提示缺少`tough-cookie`，测试仍未启动。该Node默认模块搜索路径不含系统包目录，补上`NODE_PATH`后实际运行：

```bash
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_interactions.cjs
```

exit0，`校验/交互逻辑校验.json`为PASS、`jsdomErrors`为空；只出现系统依赖的punycode弃用提示。以上是本机核验命令，不是普通读者的启动依赖。

## 实际Firefox截图

初次`firefox --version`在沙箱内退出46，无法创建只读`/run/user/1000/snap.firefox`；依工具要求申请沙箱外执行后，实际命令：

```bash
firefox --headless --no-remote --profile /home/lbh/oiwireless/analysis-source-audit/reader-typography-20261102/profile --screenshot /home/lbh/oiwireless/analysis-source-audit/reader-typography-20261102/foundation.png --window-size 1440,1100 'file:///home/lbh/oiwireless/5g-latency-research-reader/index.html#/doc/d377c9daec93a3876'
```

exit0，生成截图并实际查看：导航、中文/英文/数字间距、基础知识表格、两条分式正常。Firefox启动有snap挂载命名空间提示，未阻止截图。截图及临时浏览器配置仅留在阅读站仓库外的辅助目录，不提交Git。

本次实际视觉范围为1440×1100的Firefox基础知识页首屏，未声称完成全部文章、手机浏览器或VPN客户端视觉验收。全部交互覆盖由上述DOM测试验证，不把jsdom当成浏览器排版或PDF阅读器验收。

## 离线资源与原件一致性

实际执行`python3 tools/validate_reader.py`，exit0，错误/警告均为空。核对1177篇文档、9722个文档跳转、10033个文献跳转、6944个协议跳转、3467处页序定位及149处本地资源引用；36份PDF、34份协议Word及26个协议ZIP的来源哈希保持。既有571处旧标题链接、21处协议条款仍沿用原有回退机制，不冒称本次全部修复。

新脚本已加入必需资源清单，校验报告中的浏览器说明改为本次实际Firefox首屏检查范围。实际执行`git diff --check`，exit0。查看Git变更清单，未修改Markdown快照、生成的文档/协议正文或原始论文协议文件。
