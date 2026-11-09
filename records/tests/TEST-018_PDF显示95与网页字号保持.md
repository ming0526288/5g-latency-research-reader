# TEST-018 PDF 显示 95 与网页字号保持

实际执行现代 Node v24.22.1：

```bash
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_protocol_pdfs.cjs
```

exit 0，34 分册覆盖、图 4.2.3-2 第 49 页链接 `#page=49&zoom=95`、翻页、页码范围、条款、版本提示和分册切换通过。这是阅读界面交互测试，不是译文内容校验。

Firefox 独立工作区配置截图命令实际 exit 0：

```bash
firefox --headless --no-remote --profile /home/lbh/oiwireless/analysis-source-audit/network-architecture-figure-20261109/firefox-profile --screenshot /home/lbh/oiwireless/analysis-source-audit/font-size-compact-20261109/pdf-zoom95.png --window-size 1440,2300 'file:///home/lbh/oiwireless/5g-latency-research-reader/index.html#/paper/P05?page=1'
```

已查看截图，真实内嵌 PDF 工具栏显示 95%，页面可见。未做新译文校对、手机原生 PDF 实测或远端 VPN 测试，未修改 PDF 文件。

临时网页字号修改已撤销。首次要求 CSS 与任务开始前逐字节相同的断言 exit 1，随后定位到独立提交 33599cb 删除了一条 `.pdf-view h2` 样式；保留其他会话已提交修改，不回退。最终核实 CSS 与当前 HEAD 完全一致、AGENTS 无本项差异。证据为 `校验/PDF默认缩放95与网页字号保持_20261109.json`，完整截图本地保存。
