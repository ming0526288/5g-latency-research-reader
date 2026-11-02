# 算法知识点说明：总入口

本文件夹按用户2026-10-28要求建立，帮助理解实验和算法中的名词、单位、公式及实际含义。通用知识持续写入同一份基础文档；每个算法各有自己的知识点文件，同一算法遇到新问题就更新原文件。目录只解释知识，不代表又做了一轮实验。

固定位置：`/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/算法知识点说明/`。

|先读哪一份|讲什么|
|---|---|
|[00 通信与时延基础知识](00_通信与时延基础知识.md)|B、bit、Mbps、包长、负载、ICMP、UDP、ping、闭环、5QI/QFI、统计口径、死锁/饿死/积压区别及当前证据；持续更新的公共知识库；第11.1节用当前120kHz说明SR周期、与TDD的区别及等待例子，第12节列已测收益/成本，第14节区分3GPP要求和gNB排序算法。|
|[QUEST知识点](QUEST_知识点说明.md)|HOL、BSR、私有HOL上报、标准DSR、PDB、TBS、优先级及QUEST公式。|
|[QUEST无HOL评分消融](QUEST无HOL评分消融_知识点说明.md)|保留真实上报、仅评分去掉HOL；30条件正式/独立复核完成，解释Priority/PDB与HOL作用。|
|[WAIT知识点](WAIT_知识点说明.md)|积压估计、等待轮次、PF升权；为什么等待轮次不等于包时延。|
|[PF知识点](PF_知识点说明.md)|比例公平、历史吞吐量；为什么公平不等于每个UE时延相同。|
|[MT知识点](MT_知识点说明.md)|最大吞吐量；为什么吞吐量目标不同于尾时延目标。|
|[PB知识点](PB_知识点说明.md)|按优先级排序；5QI编号与Priority Level的区别。|
|[EDF知识点](EDF_知识点说明.md)|剩余预算、截止期、HOL及截断；这里说明论文和本地移植的具体版本。|
|[M-LWDF知识点](M-LWDF_知识点说明.md)|等待、吞吐和概率权重；论文概率参数与本地PER输入映射的区别。|
|[SR周期分配知识点](SR周期分配_知识点说明.md)|机会预算、最差与归一化目标、模型最优边界、联合配置干扰；真实C/18条件正式与独立复核完成，69局部收益与整体最差代价并报。|
|[服务欠账/服务间隔控制：候选知识](服务欠账控制_候选知识点说明.md)|待定位后选择的控制方向，未确定公式/参数、未实现、无收益结果。|
|[RR候选对照知识](RR_知识点说明.md)|等机会轮询、与等吞吐/等时延的区别；本项目未实现/未测。|
|[AUGUSTE阅读知识](AUGUSTE_知识点说明.md)|预测授权与PF排序的不同层次、原文基线和隔离评估边界；本项目未复现。|
|[授权时机机制知识](授权时机_知识点说明.md)|F工程门限、纯不活跃预算、grant真实字节用途及RB×符号成本；18正式/全部独立复核完成；首发等待与完整包跨度的取舍，非预测器。|
|[剩余资源预算探测知识](剩余资源预算探测_知识点说明.md)|首轮18与新72全部独立通过；2/4/8Mbps最差P99改善-1.63%/+0.80%/+3.62%，69与资源代价单列，低负载不保证收益。|
|[新算法知识点模板](TEMPLATE_算法知识点说明.md)|新算法各建一份，解释变量/单位、手算例子、代码位置、依据和易错点。|

已实现/对照算法专篇共七份：QUEST、WAIT和五个对照算法。另有已完成真实C/18条件首版验证的SR周期分配知识页，以及明确标记“候选”的服务欠账知识页；后者尚未实现，不算已有收益算法。对照算法各自解释知识，也不因此变成七个新的研究方向。尚未实现的论文算法不冒称已有实现。

## 后续怎么维护

1. 讨论或实施过程中出现需要解释的新名词、单位、公式、统计口径，及时补入对应文件，不能只在聊天中解释。通用知识写00文件，算法专有知识写该算法文件，并链接00避免大段重复。
2. 每篇尽量按“是什么→在本实验里是什么→变量与单位→简单例子→容易误解什么→依据在哪里”来写。实际未测内容注明未测。
3. 同一知识点应直接修正旧解释，不只在尾部追加相互冲突的说法；改动历史、原因和核验放CHG/TEST。新算法新建独立文件并登记本页，同时更新算法文档索引、新会话引导和总导引。
4. 协议要求、论文算法、代码实现和工程选择分别标明，引用到条款/表号、论文/教材本地PDF页序及源代码函数。缺必需3GPP原文按AGENTS立即停止。
5. 本目录不替代[算法实现与结果说明](../算法文档/README.md)、逐步CHG/TEST或原始证据；不搬入协议全文、凭据或完整日志。

通用网络单位不是3GPP专有参数；目录组织本身3GPP/额外通信数学推导不适用。具体通信概念仍见各篇来源。此次只整理已知知识，不修改通信代码/配置或冻结文件、不启动实验；Git沿用户取消指令不提交/推送。

本次建立和核验：[CHG273](../records/changes/CHG-273_算法知识点分算法归档与长期维护规则.md)、[TEST407](../records/tests/TEST-407_知识点文档数值依据链接与规则核验.md)。

按[执行路线](../docs/16_下一步_多UE服务不足定位与算法验证路线.md)推进；步骤1已有数据分析与步骤2状态观测现已完成。路线建立/旧总路线状态纠正见[CHG276](../records/changes/CHG-276_多UE服务不足到算法验证的后续路线.md)、[TEST410](../records/tests/TEST-410_后续路线现有字段与文档入口核验.md)，该记录描述当时规划，后续真实实验见下方当前入口。

2026-10-28补充：基础篇第9节和七算法专篇增加死锁/饿死/服务不足边界，核查记录见[CHG274](../records/changes/CHG-274_多UE死锁饿死与已有证据知识补充.md)、[TEST408](../records/tests/TEST-408_死锁饿死只读源码与有限业务核验.md)。没有新无线实验或无饿死证明。

2026-10-28继续补充：基础篇第9节解释“修复死锁、防止饿死为何可能改善时延及代价”，QUEST/WAIT/PF各补对应知识；[CHG275](../records/changes/CHG-275_防饿死与时延优化收益边界知识说明.md)、[TEST409](../records/tests/TEST-409_防饿死时延关系文档与既有证据核验.md)记录纯说明核验。没有新算法实现、参数修改或新业务实验。

当前步骤1已经完成：[三UE连续未服务与慢包原因](/home/lbh/oiwireless/oi-wireless-ran-quest-qos-identity/research/latency-analysis/service-gap-analysis/evidence/current-01/三UE连续未服务与慢包原因_已有数据分析.md)。公共知识和QUEST/WAIT/PF及候选页已更新；随后[状态链观察](/home/lbh/oiwireless/oi-wireless-ran-ul-state-observation/research/latency-analysis/ul-state-observation-results/evidence/current-01/三UE候选前等待原因_状态链观测结果.md)也已完成，基础知识第11节解释SR/BSR、40槽周期、候选前等待与切点统计。随后[SR周期机制对照结果](/home/lbh/oiwireless/oi-wireless-ran-sr-period-mechanism/research/latency-analysis/sr-period-results/evidence/current-01/SR周期三UE时延机制对照_结果与结论.md)9/9完成，121500完整UL包；基础第12节解释配对P99、SR与TDD周期、控制代价和静态参数/算法的区别。最差UE P99中位11.706/9.184/7.956ms，20/10配对降幅中位21.98%/32.47%，机会率2/4倍。随后[SR分配已有数据与模型设计](../sr-allocation-design/CURRENT.md)及真实C/18条件正式验证已完成，见[每UE SR正式结果](/home/lbh/oiwireless/oi-wireless-ran-sr-per-ue/research/latency-analysis/sr-per-ue-results/evidence/main-01/每UE_SR周期分配_正式对照结果.md)；它仍是静态策略，不是动态自适应或在线学习。CHG288/TEST432记录本次知识和导航收尾。

跨场景的基线选择见[原始资料调研与本项目建议](../docs/17_多UE时延研究基线选择与场景对照.md)；RR/AUGUSTE新增篇均是候选/阅读知识，不算新的已实现算法。


当前收尾30/30与完整独立复核完成，先读[docs19](../docs/19_QUEST收尾结论与下一方向.md)。下一方向优先请求后服务/授权时机；AUGUSTE未实现，不能将旧静态SR或评分消融冒称预测授权。

新增基础知识“慢包选择偏差与同编号配对”及ALG005专篇：解释为什么只跟踪旧慢包会产生假改善，来源/反例/实际72数据详docs24与CHG347/TEST494。

前一步ALG005知识补充：[W授权切点分析](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/25_ALG005首段前等待与授权切点分析.md)；授权提前的clip分解、SR条件子集、软件观察边界在既有ALG005专篇与基础篇持续维护，没有新算法编号。CHG348/TEST495。

前一步ALG005补充：[8Mbps更早授权与载荷分析](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/26_8Mbps更早授权载荷与慢包排队分析.md)，先理解包/授权/TB与事件重复计数，再看已有积压的连续服务问题。CHG349/TEST496；无新算法编号。

最新：[RB来源与双时钟分析](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/27_RB来源还原与授权间隔双时钟分析.md)及[重传预算修复与旧数据影响](/home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/docs/28_上行重传RB预算指针修复与旧数据影响.md)；原因标签与实际分支、名义标签/墙钟、C指针预算分别说明，无新算法编号；新修复版完整栈先导尚未完成。CHG350/351、TEST497/498。
