# CHG-103 FR2控制信道与TDD联合方向修正

2026-10-21，用户继续测试。继SSB65修复后，plan-03两DL超时都锁定SSB33、无SIB1。实际核原文及生产调度发现配置方向冲突，停止整批，不用挑SSB1成功轮替代该错误。保留旧source/config/日志；不改原始仓库。本次不再改C/二进制，继续用70027c6795同gNB/UE身份。

准确首选原文：38.213 V19.5.0 §4.1 CaseD、§11.1、§13正文n0/SFN奇偶/两监测槽规则、表13-8 index2（mux1、48RB、1个CORESET符号）、表13-12 index0（O0/M1/首符号0）；38.214 V19.5.0 §5.1.2.1.1表5.1.2.1.1-2，默认A行2为K0=0/S2/L10，行14为K0=0/S2/L4；38.331 V19.4.0 §6.3.2 ssb-PositionsInBurst字段，位1为实际发SSB。FR1不改，以38.213表13-4/13-11核既有方向。原文实际读取，相关段/表号TEST173/174，不借相邻版本或缺件资料推定。

生产依据：gnb_config.c::fix_scc逐字节反序及ASN.1位序，项目整数bitmap0x0000000200000002对应SSB1/33；nr_mac_common.c::get_type0_PDCCH_CSS_config_parameters据O/M算n0；gNB_scheduler_bch.c::schedule_nr_sib1只在n0排SIB1；gnb_paramdef.h的sib1_tda默认1（零起，标准行2）。不能把“配置启动过/部分UE接入过”写成联合方向正确。

数学：n0=[O2^μ+floor(iM)] mod(10·2^μ)，SFN奇偶=floor([O2^μ+floor(iM)]/(10·2^μ)) mod2。μ3/index0时i1→n01、i33→n033。P0.625ms为5槽，33/34模5=3/4，在2:2和1:3均为U，Type0没有可用DL机会；3:1的n033为S，但原SIB1符号2..11越过S的D0..5，含固定U，仍冲突。即使锁到SSB1时某些轮业务通过，也不能恢复冲突配置的合法性结论。

新FR2统一在研究副本配置选单SSB1（项目bitmap0x2L）及sib1_tda=13（标准默认A行14，S2/L4），searchSpaceZero0/CORESET index2等保持。SSB1在slot0符号8..11全D；SIB1实际n01上的CORESET符号0及PDSCH符号2..5均能放入最短6D段。19份FR2配置统一改两个字段，3份FR1原字节不改；TDD/SCS、负载/CPU/样本/超时/PRACH/NR定时器不改。**单SSB1和第14行是项目选择，协议未强制该组合；Word/PPT须标红。** 移除第二波束/缩短SIB1会改变控制开销，故所有受影响业务新组重测，不能从旧新差值单独归因调度策略优化。

audit_access.py读实际22配置、生产CORESET/O/M/TDA表，对SSB、实际发SIB1首Type0控制和PDSCH的逐符号D方向做静态核验；UE第二监测槽不强制必须有gNB发射。旧11配置被方向门槛拒绝；新22通过。仅联合方向检查，不包办PRACH、频率映射、HARQ、TBS容量或完整一致性。prepare.py新增--normalize-fr2-access，仅改新复制配置并先强制审计，生成plan-04/189冻结；不覆盖plan-02/03。四项独立sanity后才正式79短+4长。collect.py允许sanity按已声明计划长度核数量，不再硬写2，并导出各条件实际SSB/CORESET/SIB1字段和审计SHA，强制其与配置SHA及通过的方向审计一致，并从运行gNB的SIB1 TDA日志核实13/1真实生效，重核生产Type0/TDA表源SHA未变。report.py现行口径同时说明控制开销已改，不能宣称旧新差值是纯调度收益。

论文P01 III/IV PDF2–4用于完整包测量，P17 III/IV PDF3–4用于图样与机制范围；教材§5.4.5本地PDF122直接讲Type0监测，§5.4.1–4 PDF114–121为背景，§6.4.3 PDF211–213讲TDA/偏移。教材旧版本不能覆盖最新原文。每步运行与失败TEST173/174，四完整回归另TEST175；不预先写通过。

## 依据与适用边界 2026-10-20补注

本条2026-10-21新增。所需原文已本地可读，不缺件不下载；选择按协议允许字段约束构造而非标准固定配比/控制配置。保留旧失败，修正活动正文/Word/PPT时直接替换数值和错误解释，不只追加免责声明。
