# ALG005不同负载：完整结果与全部Markdown入口

最新：[RB来源与双时钟分析](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/27_RB来源还原与授权间隔双时钟分析.md)（193133原原因逐候选回放）及[重传预算修复与旧数据影响](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/28_上行重传RB预算指针修复与旧数据影响.md)（独立C修复/回归，完整栈未跑）。原72为旧ELF，预算证明限纯probe次数/F帧及已分配资源。CHG350/351、TEST497/498。

前一机制：[8Mbps更早授权与载荷分析](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/26_8Mbps更早授权载荷与慢包排队分析.md)；8Mbps24已有条件/288000包独立复核，方法probe-load-earlier-grants/README，字段SCHEMA/命令CURRENT，CHG349/TEST496。

前一切点：[W授权切点分析](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/25_ALG005首段前等待与授权切点分析.md)；864000观察逐包分解/独立复核通过，方法probe-load-wait/README_v2，当前与完整命令CURRENT。CHG348/TEST495。

前一补充：[同业务编号慢包分析](../24_ALG005同业务编号慢包配对分析.md)，432000编号配对与双向选尾/全体对照；主72 P99不变。方法在probe-load-tail/README，实际结果CURRENT，CHG347/TEST494。

72条件和全部独立复核完成；当前首读docs22。旧18、先导和失败不混新结果。

|入口|用途|
|---|---|
|[主结果](../22_ALG005不同负载验证与69代价分析.md)|结果、公式、切点、69/资源代价、失败和局限|
|[原72固定交付：旧ELF数表](/home/lbh/oiwireless/oi-wireless-ran-probe-residual/research/latency-analysis/probe-load-results/evidence/main-02/ALG005_不同负载与69代价_正式结果.md)|72正式及逐UE/seed CSV|
|[SVG图](/home/lbh/oiwireless/oi-wireless-ran-probe-residual/research/latency-analysis/probe-load-results/figures/main-02-v2/ALG005_load_tradeoff.svg)|当前图；SVG声明Arial优先，PNG为替代字体预览|
|[冻结方法](/home/lbh/oiwireless/oi-wireless-ran-probe-residual/research/latency-analysis/probe-load-v4/README.md)|协议条款/论文教材页序、配置和数学|
|[当前状态](/home/lbh/oiwireless/oi-wireless-ran-probe-residual/research/latency-analysis/probe-load-v4/CURRENT.md)|实际完成状态，优先于冻结时点文字|
|[全部完整命令](/home/lbh/oiwireless/oi-wireless-ran-probe-residual/research/latency-analysis/probe-load-results/README.md)|独立核验/汇总/到达审计/成图，既有输出不覆盖|
|[算法](../../算法文档/ALG-005_剩余资源约束的预算探测授权.md)|C实现、首轮历史18与新72|
|[知识](../../算法知识点说明/剩余资源预算探测_知识点说明.md)|负载单位、配对统计、序列化切点、尾分位|

## 逐步修改与测试

- [CHG-330 ALG005负载扩展方法与冻结](../../records/changes/CHG-330_ALG005负载扩展方法与冻结.md)
- [CHG-331 负载先导PFCP地址核验修正](../../records/changes/CHG-331_负载先导PFCP地址核验修正.md)
- [CHG-332 负载扩展中央接续知识与导引](../../records/changes/CHG-332_负载扩展中央接续知识与导引.md)
- [CHG-333 负载扩展汇总与独立复算方法](../../records/changes/CHG-333_负载扩展汇总与独立复算方法.md)
- [CHG-334 负载先导通过与七十二正式启动](../../records/changes/CHG-334_负载先导通过与七十二正式启动.md)
- [CHG-335 目标到达与实际发送偏差审计](../../records/changes/CHG-335_目标到达与实际发送偏差审计.md)
- [CHG-336 负载与69代价对比图程序](../../records/changes/CHG-336_负载与69代价对比图程序.md)
- [CHG-337 负载正式中止与TUN采集丢失诊断](../../records/changes/CHG-337_负载正式中止与TUN采集诊断.md)
- [CHG-338 失败轨迹零块空间回收与字节保全](../../records/changes/CHG-338_失败轨迹零块空间回收与字节保全.md)
- [CHG-339 TUN采集容量验证与v4方法](../../records/changes/CHG-339_TUN采集容量验证与v4方法.md)
- [CHG-340 v4定点先导准备与启动](../../records/changes/CHG-340_v4定点先导准备与启动.md)
- [CHG-341 v4四定点先导及全部独立复核完成](../../records/changes/CHG-341_v4四先导独立复核完成.md)
- [CHG-342 v4完整七十二复测准备与启动](../../records/changes/CHG-342_v4完整七十二准备与启动.md)
- [CHG-343 磁盘清理与实验边界保护](../../records/changes/CHG-343_磁盘清理与实验边界保护.md)
- [CHG-344 完整负载结果报告加入维护暴露](../../records/changes/CHG-344_完整负载结果报告加入维护暴露.md)
- [CHG-345 完整七十二条件与收尾修正](../../records/changes/CHG-345_完整七十二条件与收尾修正.md)
- [CHG-346 ALG005完整负载结果、分段解释与对照图交付](../../records/changes/CHG-346_ALG005完整负载结果与对照图交付.md)
- [TEST-477 ALG005负载扩展资料与准备检查](../../records/tests/TEST-477_ALG005负载扩展资料与准备检查.md)
- [TEST-478 负载先导RAN前失败及抓包重放](../../records/tests/TEST-478_负载先导RAN前失败及抓包重放.md)
- [TEST-479 负载扩展中央导引知识一致性](../../records/tests/TEST-479_负载扩展中央导引知识一致性.md)
- [TEST-480 负载四先导完整与独立核验](../../records/tests/TEST-480_负载四先导完整与独立核验.md)
- [TEST-481 负载七十二正式准备与计划核验](../../records/tests/TEST-481_负载七十二正式准备与计划核验.md)
- [TEST-482 目标间隔与实际发出先导重放](../../records/tests/TEST-482_目标间隔与实际发出先导重放.md)
- [TEST-483 负载对比图程序语法与来源身份](../../records/tests/TEST-483_负载对比图程序语法与来源身份.md)
- [TEST-484 七十二负载正式第十七条件采集失败](../../records/tests/TEST-484_负载正式第十七条件采集失败.md)
- [TEST-485 停止轨迹稀疏化完整字节核验](../../records/tests/TEST-485_停止轨迹稀疏化完整字节核验.md)
- [TEST-486 隔离TUN抓包容量实测](../../records/tests/TEST-486_隔离TUN抓包容量实测.md)
- [TEST-487 v4四先导准备与定点计划核验](../../records/tests/TEST-487_v4四先导准备与定点计划核验.md)
- [TEST-488 v4四定点先导完整与独立复核](../../records/tests/TEST-488_v4定点先导完整与独立复核.md)
- [TEST-489 v4完整七十二计划冻结与启动核验](../../records/tests/TEST-489_v4七十二计划冻结与启动核验.md)
- [TEST-490 磁盘清理与内容一致性核验](../../records/tests/TEST-490_磁盘清理与内容一致性核验.md)
- [TEST-491 报告v5与来源恢复前核验](../../records/tests/TEST-491_报告v5与来源恢复前核验.md)
- [TEST-492 七十二业务完整与外层收尾核验](../../records/tests/TEST-492_七十二业务完整与外层收尾核验.md)
- [TEST-493 七十二独立复核、数表与图形交付](../../records/tests/TEST-493_七十二独立复核数表与图形交付.md)

## 版本与失败位置

v1只准备未运行（README条号笔误）；v2先导RAN前PFCP reader地址迁移错；v3修地址后先导通过，但main-01第17业务后TUN观测内核丢19中止，真实慢包保留；v4只修采集容量、先导独立全过后原72完整重跑。报告v5补维护暴露/方法链接；图v2修标签，统计不变。sudo父收尾遗漏已精确恢复，主实际exit0；不要把这些工程问题混为无线业务失败。

原始根analysis-source-audit/probe-load-20261029只本地，既有root不重启/覆盖，冻结源不编辑。安全证明verification/main-02、成本聚合cost-evidence/main-02。原4核心/原RAN保持；32本地必要原文齐，新必要缺件仍全研究强制停并由用户补，不下载。Office本轮未同步。导引工程整理3GPP/额外数学不适用，通信来源见方法和CHG。

GitHub查看（当前代码/数据在latency-probe-residual分支，主说明在latency-standards-audit）：

- [完整正式报告](https://github.com/ming0526288/oiwireless-latency-analysis/blob/latency-probe-residual/research/latency-analysis/probe-load-results/evidence/main-02/ALG005_%E4%B8%8D%E5%90%8C%E8%B4%9F%E8%BD%BD%E4%B8%8E69%E4%BB%A3%E4%BB%B7_%E6%AD%A3%E5%BC%8F%E7%BB%93%E6%9E%9C.md)
- [当前SVG对照图](https://github.com/ming0526288/oiwireless-latency-analysis/blob/latency-probe-residual/research/latency-analysis/probe-load-results/figures/main-02-v2/ALG005_load_tradeoff.svg)

- [CHG-347 同业务编号慢包配对与负载分段分析](../../records/changes/CHG-347_同编号慢包与负载分段分析.md)

- [TEST-494 同编号慢包分析、统计反例与交叉核验](../../records/tests/TEST-494_同编号慢包统计控制与交叉核验.md)

- [同编号慢包SVG图](https://github.com/ming0526288/oiwireless-latency-analysis/blob/latency-probe-residual/research/latency-analysis/probe-load-tail/figures/result-01/ALG005_matched_tail.svg)

- [CHG-348 W授权切点与清单计数纠正](../../records/changes/CHG-348_W授权切点与清单计数纠正.md)
- [TEST-495 W切点全量重算与独立复核](../../records/tests/TEST-495_W切点全量重算与独立复核.md)

- [CHG-349 8Mbps更早授权载荷与状态机制](../../records/changes/CHG-349_8Mbps更早授权载荷与状态机制.md)
- [TEST-496 更早授权技术先导与全量独立核验](../../records/tests/TEST-496_更早授权技术先导与全量独立核验.md)

- [CHG350 RB来源/双时钟与旧预算异常](../../records/changes/CHG-350_RB来源双时钟与旧预算异常.md)
- [TEST497 RB还原失败后重算与独立回放](../../records/tests/TEST-497_RB还原重算与独立回放.md)
- [CHG351 上行重传指针预算纠错](../../records/changes/CHG-351_上行重传指针预算纠错.md)
- [TEST498 重传预算C回归与真实单元编译](../../records/tests/TEST-498_重传预算C回归与真实单元编译.md)
