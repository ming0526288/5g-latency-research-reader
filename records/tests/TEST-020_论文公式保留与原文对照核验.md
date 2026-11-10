# TEST-020 39篇论文公式显示核查与修复验证

2026-11-10。仅阅读站辅助译稿工程，无核心网/gNB/UE/业务/抓包；3GPP与新增通信数学推导不适用。原39篇446页可读、rotation均0，站点/工作区/目录SHA一致。

## 最终实际结果

- v6生成器 `tools/repair_paper_math.py`：39/39、446页、exit0；其逐篇600秒为文档生成超时，未把它当无线时延阈值。旧稿与索引先备份，完整日志aux/final-repair-v6.log和final-repair-run.json。
- `tools/audit_math_pdfs.py --render`：39/39、446页渲染、50869项保护片段字体/坐标/字号记录匹配、0未匹配、exit0。P10最后48pt页边修正后单篇再审计/渲染exit0，已合回最终安全汇总。此为明确范围的工程检查，字形位置匹配不能外推为全部代数和专业语义通过。
- 回归 `check_math_guard.py`：未修复丢scope/漏Form字体负对照和7类保护检查exit0。`check_math_trace_fonts.py`：真实P09/P10与同前缀歧义拒绝exit0。`check_math_layout.py`：极小擦边误归公式负例及保留真正公式/无正文回退exit0。
- 原/译各篇数学样页与全446页总览已看，位置见新说明及本地manual-review.json；P39六页逐页查看。P29原/译PDF6、7说明栏以下逐字节像素相同，`check_scan_math.py` exit0，结果绑定原/译SHA；OCR其他行内数学仍未认证。
- P02/P10/P29补修命令exit0，三个实际耗时22.93/45.86/17.33秒，补修日志段落翻译错误计数0；P10最后只扩白底区域上界48pt后再跑exit0。新PDF的旧人工QA不继承，39份仍generated/pending。
- 实际DOM `check_paper_translations.cjs --require-all` exit0：39/39有真实上下阅读器、SHA/页数相符，独立翻页/边界/同步通过，ready=[]。`check_math_report.cjs` exit0：核查说明39行表、文献导引链接、全站搜索均可用。
- `check_math_live.py`：最终实际HTTP GET39份译稿与2个运行资源，200、字节SHA与磁盘一致，exit0；非VPN/远端客户端认证。Firefox独立测试配置实际打开P39中文PDF页2，截图已看，E[·]与条件期望括号可见。
- `update_knowledge.py`、`update_reading_notes.py`、`check_prerequisites.py`、`validate_reader.py`均实际exit0。知识统计涵盖其他既有页；最终网站校验文档1198、PDF原件40、协议分件35/原包27，非本次新协议或实验。E知识表条件竖线已转义、每行3格。

## 重现命令

在阅读站根目录，Python为已记录的隔离环境（下文命令用完整路径），Node为已有Node24，未安装新服务：

```bash
cd /home/lbh/oiwireless/5g-latency-research-reader
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/check_math_guard.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/repair_paper_math.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --only P02,P10,P29 --force --repair-math --repair-layouts --engine babel
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/audit_math_pdfs.py --render
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/check_math_trace_fonts.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/check_math_layout.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/check_scan_math.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/build_math_review_sheets.py --samples P04:8,P09:14,P13:2,P15:3,P20:7,P29:7,P36:10
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_paper_translations.cjs --require-all
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_math_report.cjs
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/check_math_live.py
python3 -B tools/update_reading_notes.py
python3 -B tools/validate_reader.py
```

全部重建前须先核没有另一个生成器写同一索引。独立候选命令为 `venv/bin/python tools/probe_math_layout.py --only P10 --page 8` 和 `--only P14 --page 2`；它们不改网站运行索引。首次wrapper漏layout文件的失败后，实际后处理另用已保存原P10检测框完成；当前脚本已保存本轮检测框。最终网站P10按正式命令重做。

Firefox实际命令使用 `firefox --headless --no-remote --profile /home/lbh/oiwireless/analysis-source-audit/robotics-reader-20261110/firefox-profile --screenshot /home/lbh/oiwireless/analysis-source-audit/math-translation-audit-20261110/firefox-P39-page2.png --window-size 1200,1500` 加本机P39中文PDF地址与#page=2，exit0。不改用户浏览器配置，不重启阅读站。

## 失败、拒绝稿与局限

首轮v1在P27后/P28过程中主动TERM143，等待队列同为143；最终完整批次已取代，非最终P28失败。v2/v3数学矩形clip夹带英文，不发布；v4笔画、v5连字、最终v6保护分别实际候选核对。P02正式首批有一次SSLEOF段落错误被Babel吞掉，后重做且增加发布拦截。P09/P10初次41/155个未匹配是长STIX轨迹名截短，唯一资源映射重核3277/3277和3180/3180，不放宽几何容差。

P10首个边界候选沙箱网络拒绝，未发布；按工具要求提升后生成，wrapper漏layout文件exit1，最后成功到隔离PDF、后处理未完，后来修复并正式重做。解析探针和边界测试缓存初始化失败已先配置工作区路径；HTTP首轮socket被拒已提升重跑。审图器遇processing条目曾KeyError，已跳过并按新SHA重新审图。网页测试首轮用错误标题查入口失败，改已登记source后通过。扫描证明测试说明字串两次断言失败，真实字形“不”为兼容汉字；只对说明查找NFKC/空白规范化后通过，像素比较仍严格相同。字体子集post警告保留，不把警告或exit0代替科学语义判断。

仍有P14/P17/P18/P28/P30/P37局部版式问题，逐篇说明已直接列出；P14候选未解决其标题/正文重叠，未发布该候选。中文稿按照用户“未校对也展示”指令可读，visualQA均pending，不声称全文零缺陷。P29扫描OCR数学不自动认证，原推导页保留并像素核对。未改英文原件、协议、C代码、无线参数或历史研究数值，也未做新无线/控制实验。

本地完整证据：`/home/lbh/oiwireless/analysis-source-audit/math-translation-audit-20261110/`，字符/笔画几何证据在 `.../paper-zh-20261109/math-guards/`。安全代码/统计/记录Git，PDF全文/日志/候选/渲染不Git。
