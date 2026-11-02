# CHG-321 授权资源独立解码复核与交付汇总方法

新增新树`grant-timing-results/verify_cost.py`，不导入cost/graph/radio模块，直接struct读QST/ULST/UST，以完整rnti/源帧槽/目标帧槽键内时间序一一配对，独立展开目标SFN周期，核实际F/threshold、纯不活跃间隔/有限窗、各触发真实grant/TBS/RB×符号。它不是独立PHY或编号字节图验证，范围明确区分。

新增`collect.py`，要求18完整、原始/成本/切点独立核验和环境清理全部通过才输出；同seed先平均正反接入，再三seed中位，另保留六上下文/逐UE/原始成本，时延正值改善、资源change正值增加。无需新的通信参数/信令/数学模型，测量和预算依据v2/README/CHG319/320；原文缺件规则不变。

这些是main-01冻结完成后新增的离线文件，不修改被冻结cost.py或运行方法，不影响正式18条件输入。AST通过；pilot独立成本修正一次摘要字段读取错误，见TEST465，不把脚本字段错误称无线失败。正式collect尚未运行，不写通过/收益。Word/PPT及原C保持。
