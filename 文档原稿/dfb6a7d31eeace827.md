# CHG-046 撤回PDF并更新替换PPT

用户更正原“PDF”实际指PPT，因此删除上轮生成的同名总结PDF；Word保留。没有删除任何协议、论文、教材PDF。当前PPT更新到29页，包含历史下行批次、同期UL/DL批次、八周期结果、接入配置对照、失败阶段、固定K2近似与实测差异、新协议范围。所有数字取自已归档安全证据，不增加RFsim实验。

最终本地文件：`/home/lbh/oiwireless/analysis-presentations/tdd-20261020/output/120kHz_TDD时延分析与RFsim核验_最终版.pptx`。可编辑15张原生表、3个原生图表。完成校验和逐页检查后，按用户要求删除两次任务目录中的10份旧版/中间PPTX，只保留这一份最终PPTX。删除路径和前SHA在本地`build/old_ppt_deletion_manifest.json`；PDF删除记录在`analysis-documents/records/pdf_removed_user_correction.json`。

工具：缓存Node的`@oai/artifact-tool`，本地`build/update.mjs`、`revise-body.mjs`、`finalize-labels.mjs`、`render-verified.mjs`。初始作者脚本依赖旧PPT，该旧版已按要求删除，不能再把脚本当作现存模板一键重建入口；今后编辑以唯一最终版为源。真实图表工作簿从旧版本逐字节保留，记录位于本地workbook_restoration与revised_workbook_restoration。没有伪造原工作簿。运行和遇到的失败见TEST-074。

本项为文档输出与文件替换，3GPP/新数学推导不适用；通信内容依据CHG-042至044、TEST-068至070、统一来源表。Word/PPT/QA/生成脚本仅本地，Git提交说明及安全索引。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：本项为工程操作，3GPP通信参数与新数学推导不适用；依据E01/E03，不硬贴协议条款。

依据编号：E01、E03。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：Git、文件隔离、边界修复、哈希、结果一致性或排版属于工程追溯，不修改通信协议；没有对应3GPP强制条款。相关实验条件仍以对应报告和M01为准。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
