# CHG-129 接收五篇前沿PDF与当前版本状态更正

2026-10-23，用户告知已下载文献。本轮只接收核验，不新增RAN/UDP/pcap、算法实现、配置、二进制、测量值或Word/PPT编辑。原始仓库和原始PDF不改。

实际递归rg --files盘点英文PDF目录及工作区PDF/ZIP（排除results/.git）；对/home/lbh/Downloads、/home/lbh/下载相关文件名也检查。收到P30 LatencyScope v3(23页)、P31 MAC-Gyver v3(17页)、P32 vRAN v1(15页)、P34 UL MU-MIMO v2(7页)、P35 IEEE2026/DOI会议文件(6页)。P33 Near-RT xApp在已查位置未找到，明确只是可选论文而非必需协议缺件，不能写成全部六篇已收或推断用户其他路径不存在。

逐份pdfinfo/pdftotext exit0，页段合计68；8页封面/相关页渲染并view_image。新说明新增五篇文献接收与版本核验_20261023.md、元数据received_papers_20261023.json及补充provenance；只读范围明示，不把全文可抽取冒充全文已读。

两个差异保留：P32本地印刷末页15/实际15页，与arXiv Comments12pages不同，未核原因，不篡改本地页码或判文件错误；P34 PDF题名含Testbed、摘要网页不含，同2601.09384v2/日期/作者，分别登记。P35只有本篇DOI/会议印记为版本证据，参考文献里的其他arXiv号不冒充本篇版本。私有首次提取清单保留，修正接收字段名称避免误读这些参考文献号。

当前前沿清单和资源记录直接更正“新文献只有网页/未本地接收”状态，新增接续入口README/START及docs09/10。旧CHG/TEST当时网页核对事实不变；历史28篇清单不改，P29与251实验冻结不动。没有AGENTS实时状态修改。所有PDF/抽取文本/核图只本地，不上传Git。

使用PDF技能只读核验，无PDF创作/编辑marker。实际复核：
```bash
/usr/bin/python3 -B research/latency-analysis/algorithm-options/verify_sources.py
/usr/bin/python3 -B research/latency-analysis/source_audit/validate_reference_audit.py
```
第一条已PASS，第二条及Git随后以真实终端输出为准。下一步仍优先文献精读，不自动开始算法实验。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。本条为文献资料接收、原文身份和页序/版次核验，不涉及3GPP参数修改、新数学推导或调度算法，3GPP/数学推导不适用。当前所需既有7份协议可读性随verify_sources核验通过；本地P30 PDF1/9、P31 PDF1/2、P32 PDF1/15、P34 PDF1、P35 PDF1，确切SHA/版本证据和阅读范围在algorithm-options/source_provenance.json及evidence/received_papers_20261023.json。新文献未替代协议。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
