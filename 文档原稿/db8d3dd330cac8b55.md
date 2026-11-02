# TEST-017 本地 RFsim 复核

因沙箱 socket 禁止，在授权的沙箱外执行：
```bash
python3 research/latency-analysis/tdd1/smoke_rfsim.py --configs research/latency-analysis/results/tdd1/rfsim-configs-01 --output research/latency-analysis/results/tdd1/rfsim-smoke-02 > research/latency-analysis/results/tdd1/preflight/smoke_matrix_unrestricted.txt 2>&1
```

脚本整体退出1，符合一项失败的汇总状态：

|候选|gNB退出|结果|
|---|---|---|
|D3/U1|124，计划限时终止|RFsim socket/PHY 初始化通过|
|D2/U2|124，计划限时终止|RFsim socket/PHY 初始化通过|
|D1/U3|-6，SIGABRT|nr_schedule_ue_spec() 中 HARQ buffered TB 与 scheduled TBS 不一致|

三份完整日志和 status.json 保留。失败位置 openair2/LAYER2/NR_MAC_gNB/gNB_scheduler_dlsch.c:1273。说明当前 PHY 测试路径存在配置限制，不推断该配比在所有 SA 场景均非法。测试没有接入真实/软件 UE，没有有效 UDP 流，没有真实射频，也没有协议栈端到端时延。

初始化还有缺少 UE Capabilities 文件、无 SYS_NICE 能力提示；不能用这些运行日志测 CPU 处理时延。3:1、2:2 只是这一模式初始化通过，不是完整 SA/PRACH/SSB/UE 接入验收。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.211 V19.5.0 §4.3.2；TS38.213 V19.5.0 §11.1；TS38.331 V19.4.0 §6.3.2 TDD IEs；TS38.300 V19.4.0 §4.3.1.1/4.4.1。

依据编号：S01、S02、S05、S06；B01、B03、B04；C01、C03、E03。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：TDD字段与协议路径有规范依据；RFsim参数、线程、启动标志和超时属于本地实现。初始化、同步、接入和业务分别判定，不把失败自动解释为违反协议。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
