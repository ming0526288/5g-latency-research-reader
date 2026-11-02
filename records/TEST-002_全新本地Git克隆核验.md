# TEST-002 全新本地Git克隆核验

2026-11-02。首次完整阅读站已提交为`4c6e9ba4b623ba5bfa68ac9693078676fde724af`，2668个跟踪文件。以该提交执行：

```bash
git clone --no-hardlinks --quiet /home/lbh/oiwireless/5g-latency-research-reader /tmp/5g-reader-portability-20261102-01
```

实际exit0，新目录HEAD与源完全一致。在新目录运行`python3 tools/validate_reader.py`及TEST001列出的Node/jsdom交互命令均exit0，资源/原文SHA/页码/MathML与七项交互继续通过。没有依赖原研究工作区读取正文、公式字体、图片、论文或协议；这里核验的是文件/DOM层面，未做另一台电脑浏览器实机验收。完整摘要见`校验/全新本地克隆核验.json`。

随后只扩大“返回阅读文档”的绑定，使正文中已有PDF链接和自动引用链接都保存返回位置，未改变原文或数据。GitHub仓库可见性确认前不推送全文；本次本地克隆不能写成GitHub远程克隆成功。

工程核验，3GPP/新增数学推导不适用，没有通信实验。
