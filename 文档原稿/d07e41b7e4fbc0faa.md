# TEST-349 论文原页量化数字、35行来源与口径核验

日期2026-10-25，CHG-226。文献选读/文档检查，无新增通信代码、参数、模型公式或本机算法结果；无新增协议需求。

已用系统pdftotext -layout读取35个本地PDF，35次提取均返回0，缓存仅/tmp/latency-paper-reading-jx0obhe8。原PDF未改。实际以pdftoppm -f/-l/-singlefile/-scale-to 1800 -png渲染P04第18、P05第6、P20第11、P24第14页，四次均exit0；四PNG全部实际查看，核结论/图5/指标分母与场景。

一次生成调用在functions.exec的JavaScript编排层报SyntaxError: missing ) after argument list，Python/shell尚未启动，无shell退出码，也未生成目标MD/JSON。修正调用字符串后实际Python退出0，生成66行精简MD及来源JSON；不是论文数据或实验失败，没有隐去该工具错误。

实际核验入口（研究仓库根）：

```bash
python3 -B research/latency-analysis/source_audit/verify_paper_algorithm_brief.py --sources research/latency-analysis/source_audit/paper_algorithm_brief_sources_20261025.json --output /home/lbh/oiwireless/analysis-source-audit/paper-algorithm-brief-20261025/verification.json
```

上述核验已经实际exit0，PASS：35原PDF字节SHA不变、pdfinfo页数及所有定位在范围内、MD35行编号1—35各一次且35原文链接存在、12组25个数值在指定原页文本中找到。对应指标、分母/基线和场景由人工复核，不能用数字检出替代语义认证。修正P26文字为预测完整回报分布的critic，避免与分布式计算混淆；给分组标题补空行，均无数值变化。

4个已检查PNG副本保存在库外analysis-source-audit/paper-algorithm-brief-20261025/qa；仅清理自己创建的/tmp/latency-paper-reading-jx0obhe8全文提取/临时PNG缓存，未删原论文或协议。核验脚本直接读原PDF，不依赖该临时缓存，可重跑。git diff --check exit0，生产源码/原配置相对HEAD的git diff --exit-code exit0；原未跟踪scs2保持。

作者版本页/arXiv及TUM机构条目实际可读；在线核对不称本地35篇均为官网最高版本或最终出版版。本轮只核选读内容，未复现论文算法/重跑无线，未检查所有图表/样本/完整公式，未核得统一降幅的行明确标注。论文原文、QA和详细验证JSON不Git；最终暂存/提交/推送以实际工具结果核实。
