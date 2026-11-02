# 原72数据：首段前等待W的授权切点分析

用户在同编号慢包分析结束后再次要求继续。本步只读既有v4/main-02，复用已验证的完整字节/片段/TB/grant图，不重启核心网、gNB或UE，不改C、配置、期限、包或原主要P99。这是事后补充分析，不声称主实验前预注册。

## 观察点与数学

- A：UE RLC接纳；B：首段初传序列化。W=(B−A)/10^6 ms。
- G：第一**实际承载该包首段**的grant准备观察，gNB `nr_schedule_ulsch` 中UST_GRANT（gNB_scheduler_ulsch.c:2521附近）。它不是实际PDCCH RF发射时刻，也不是首个可用grant。
- U：该grant在UE成功处理UL DCI并配置PUSCH后、释放UL配置锁前的观察（nr_ue_procedures.c:560/664，observe_ul_dci，status=0、stage4）。它不是PHY纯解码起点/终点，也不是整个DCI处理函数已经返回。
- 三者通过首段→MAC TB→PHY参数→DCI/grant的原图关联，所有UST时间由ul_service_trace.h的CLOCK_MONOTONIC采集。配置保持120kHz/K2=4；只检查已测标签，不重新推导任何通用K2/SLIV公式或修改取值。

必须实证A≤B、G≤U≤B，错误顺序拒绝，不排序修复。早grant允许G<A，U也可能<A。定义clip(t)=min(B,max(A,t))，三个非负区间为：

P0=clip(G)−A；P1=clip(U)−clip(G)；P2=B−clip(U)。

逐包P0+P1+P2=B−A。全用整数ns再除10^6为ms。截断是取与等待区间[A,B]的交集，保留原始有符号G−A及早grant计数，不是删异常/负值后强迫通过。P0不是纯gNB排队，P1不是纯PDCCH空口，P2不是纯CPU或K2等待。

继续使用上一步已固定的全部4000、legacy慢40、新策略慢40的同业务seq集合，不能看到新切点后重选尾。匹配业务ID不是同一个物理包的反事实。每seed先平均正反和相同UE组，再六seed取算术均值；主P99口径不变，阶段P99不可相加。

## 等待中的正SR子集

沿已有独立核验的ue*-SR-radio-joins.csv，只使用其中accepted=1的gNB正SR观察，并报告总连接行/接受行数。该字段复用fork实际判据sr_indication非零、confidence=0、ul_cqi≥148（gNB_scheduler_uci.c:1061），是实现判据，不是3GPP规定148。选等待中第一个满足A≤gNB正SR观察<G的记录。仅在这个**有观察的包子集**上报告A→SR、SR→G及两者之和，给出覆盖包数；没有观察写未观测，不填0。SR可同时服务多个排队包，此观察不证明它由当前包单独触发、也不证明它导致当前grant。没有该切点不等于gNB未知积压或未获得资源。

## 来源优先与检索纠正

32本地原文同SHA可读。本步实际读TS38.212 V19.4.0 §7.3.1.1.1/2（DCI0_0/0_1）、TS38.214 V19.5.0 §6.1.2.1（本次非SBFD基础时域配置）、TS38.321 V19.4.0 §5.4.1/5.4.4/5.4.5、TS38.213 V19.5.0 §9.2.4（基础SR过程，非9.2.4A UEIRI）。最初前缀检索误命中6.1.2.1a SBFD旁节，已在新研究代码/运行前纠正到基础条款（原XML段8383）；另9.2.4的拼接文本前缀检索也误命中9.2.4A，已保留XML制表符并按完整编号token定位基础9.2.4（段2999）。两个旁节均未用于本步假设/配置/结论，定位问题本地保留，不把旁节替代适用原文。

38.214基础条款正文标识TDA/K2等概念；纯文本提取有OMML公式缺失，本步不据它重建一般公式或新配置。标准不规定这些Linux时间戳、ns格式、统计cohort或固定处理耗时。沿上一步TS38.322 V19.3.0 §5.2.3.1.1/5.2.3.2.3与P01 IFIP Networking2025 III/IV本地PDF2–4、教材RLC子层PDF52的分段/按包方法；本步不改协议。

用户授权本地版本不冒称独立官网最高；来源在analysis-source-audit/probe-load-wait-20261030/sources-01.json。未来新必要协议缺失立即全研究停并告知，不下载。工程目录/图形/记录维护3GPP/额外数学不适用。

## 运行与保存

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-probe-residual
taskset -c 2 /usr/bin/python3 -B research/latency-analysis/probe-load-wait/analyze.py --self-test
taskset -c 2 /usr/bin/python3 -B research/latency-analysis/probe-load-wait/analyze.py --root /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/main-02 --tail research/latency-analysis/probe-load-tail/evidence/result-01 --cost-identities research/latency-analysis/probe-load-results/cost-evidence/main-02/input-identities.json --sources /home/lbh/oiwireless/analysis-source-audit/probe-load-wait-20261030/sources-01.json --output /home/lbh/oiwireless/analysis-source-audit/probe-load-wait-20261030/result-01
```

原raw图入口/32字节LYR或64字节UST/QST头、记录数/容量/零丢弃与已填充前缀SHA须匹配原成本证明；不把预分配零块当数据。复核原CSV每包W及固定cohort均值，压缩逐包切点只本地，Git只安全聚合/哈希/说明/SVG。原始root、已有输出和冻结代码禁止覆盖/修改。列出命令不代表已执行；实际结果/失败CHG348、TEST495，动态状态CURRENT.md。Office本步不更新。
