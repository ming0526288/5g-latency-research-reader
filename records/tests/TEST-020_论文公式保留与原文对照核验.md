# TEST-020 论文公式忠实性工程检查

2026-11-10。当前记录已实际做到的位置，未把正在运行写成通过。没有核心网/RAN/UE/业务/抓包。

已实际完成：39篇/446页英文源PDF与工作区、目录SHA/页数相同，全部页可读、rotation=0；原14份已发布中文与运行索引已先备份。P39原文6页与旧译稿6页渲染，确认第2页E算子括号/变量/下标缺失；第3页矩阵条件的上标分数拆散。辅助全文和逐字符原结构只放本地aux。

命令均在阅读站根目录：

```bash
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/check_math_guard.py
python3 -B tools/update_knowledge.py
# 首轮scope修复，当时内存代码为v1：
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --all --repair-math --engine babel > ../analysis-source-audit/math-translation-audit-20261110/repair-all.log 2>&1
# 等旧批次退出后，最终v6再跑，不同时写索引：
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/repair_paper_math.py --wait-pid 203049 > ../analysis-source-audit/math-translation-audit-20261110/final-repair.log 2>&1
```

回归脚本exit0，先验证未修复方法会丢Form scope 9，再验证修复；真实glyph ID [91,1,93]保留。覆盖同名F8页/Form冲突、单字符、0.8缩放、指数数字Decimal等值、分子/分母重叠、水平线/细填充线与不夹带附近英文、原P39嵌入Encoding实际有fi。update_knowledge exit0；最后实跑统计7篇/106排版公式/11图，构建统计涵盖既有各知识页，不冒称均为本次新增；新E知识在源稿/网页/搜索中，非新无线公式。

P39修复候选实际：v1+作用域检查exit0、12269字符、无未解作用域，E[·]/E[·|·]文本及真实图片恢复；v2整块原图clip失败，夹带英文；v3只数学字体片段仍因大括号度量框包含邻行而夹带，均未发布正式网站。v4只原笔画方案exit0/5原线条，分式图恢复；v5候选exit0/44实际连字解码，原矩阵条件段“Q半正定/R正定”与1/2结构已实际查看；v6候选实际通过P39全部795/795受保护数学字形物理位置检查，第2页期望括号、第3页上标分数/矩阵条件及全部6页已实际查看，已复制到网站正式路径并更新索引。旧scope批次与等待队列后按已核PID主动TERM，均exit143；最后P27成功/P28未完成。最终正式批次63071已运行，逐篇PDF审计/渲染67783同步进行，尚不记全39已通过。

首次解析探针因先import Babel再配置工作区缓存，尝试写只读~/.cache而exit1；改正确初始化顺序并按工具要求提升后实际捕获99段原结构，主动在翻译前结束（日志Parsed为故意停止，不是论文/协议缺件）。字体子集缺post警告保留，不能把它当原文缺协议或证明公式全部正确。

最终原/译39篇页数/字节/数学作用域、全部页渲染、逐篇数学样本、浏览器/在线资源、Git记录待实际补齐。渲染成功和作用域可用不等于逐句语义认证或重新证明作者定理；公开状态保留pending。

本地证据 `/home/lbh/oiwireless/analysis-source-audit/math-translation-audit-20261110/`，生成器审计 `.../paper-zh-20261109/math-guards/`。源码依据为实际安装BabelDOC0.2.33相关函数及原嵌入CFF，不声称整个工具最新版已经修复这些问题。
