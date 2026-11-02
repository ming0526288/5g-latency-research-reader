# TEST-252 最终文档自引用交付证据链接检查失败

2026-10-23，README新增指向evidence/delivery-verification.json的自引用后，我先按既定方式将旧proof库外备份并删除以重新生成。verify_delivery实际exit1：AssertionError evidence/delivery-verification.json，发生链接存在性检查；该文件正是程序通过后才要写出的输出。其前全12/52流/逐UE分位/十窗/CCDF/有限积分/345/执行/参考SHA检查已过，当前失败不是测量数据或协议失败，未重启RAN。source_audit实际PASS407条、git diff --check exit0。

根因为交付核验器未处理自己的将来输出链接；修正仅允许该精确output路径为尚待创建，其余链接必须存在，写出后重新打开确认status PASS及文件存在。不放宽科学门槛、未知目标链接或包完整性。旧proof在analysis-source-audit/long-baseline-delivery-20261023-01/delivery-verification-v2-before-doclinks.json保留。最后重跑结果另TEST。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。交付文件工程检查，3GPP/数学推导不适用；原12/RAN/345/科学值和CHG155/156不变，所有失败保留。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
