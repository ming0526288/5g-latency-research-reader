# CHG-162 六种子长流离线收集源准备

日期2026-10-23。新增seed-repeats/collect.py，复用long-baseline/collect.py的完整匹配/分位/等包数窗/连续慢包/CCDF/在途积分恒等式/流式CPU方法，只用新design/gate，case与CSV显式seedbase、流显式trafficseed，文字改为六不同PRNGbase而非旧短/长混合。analysis_reference锁原collector和旧summarySHA，旧源不改。新增在364运行冻结之后，仅离线作者源，不参与当前RAN身份。活动RAN时只源码语法编译，未实际统计新包或给新分位，不把将来目标写已完成。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。seed-repeats/source_provenance：38.300V19.4§10.3、38.321V19.4§5.4.1/5.4.5、38.322V19.3§5.2.3.1；P01 III/IV本地PDF2–4、教材13.1.1.2 PDF530–532。离线统计不是协议规定。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
