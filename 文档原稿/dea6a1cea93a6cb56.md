# ALG-005 剩余资源约束的预算探测授权：首轮正式完成

真实C/完整新gNB与UE/8动态模块、实际C头资源检查、v2三条件先导、18正式及全部原始/预算/资源/统计独立复核完成。不是AUGUSTE预测器/学习算法或所有QoS最优。

首读[结果、代价与边界](../docs/21_ALG005剩余资源探测结果与边界.md)，[正式报告和CSV](/home/lbh/oiwireless/oi-wireless-ran-probe-residual/research/latency-analysis/probe-residual-results/evidence/main-01/ALG005_剩余资源预算探测_正式结果.md)，[全部命令](/home/lbh/oiwireless/oi-wireless-ran-probe-residual/research/latency-analysis/probe-residual-results/README.md)，[知识点](../算法知识点说明/剩余资源预算探测_知识点说明.md)。

实现：gNB pf_ul把B0/无SR纯probe延后到原PF数据分配之后，allocate_minimum_ul_probe共用原构造，残余分支检查每个RB的完整符号mask。SR/重传/原PF_data/eligibility与UE/RRC保持；默认legacy，可选residual，实际raw detail0/1和原因16，104/160字节记录不变、无新空口IE。保留旧strict边界是保守工程选择，非协议必须。

预算：当前F1门限80槽，以lastUL帧+槽4算，非精确10ms定时器；有限窗纯probe间隔≥F帧，3UE长期≤300/F次/无线秒，SR/data/HARQ另计。每轮只用剩余quota/PRB/CCE。已知积压是gNB估计E−S，不能当真实RLC队列/未来信息；无虚构BSR。标准不强制本顺序，未证明最大等待或普遍最优。

同一新10文件/120kHz/66PRB/TDD0.625ms/SR40/K2=4/69-9-9/1200B总UL4Mbps/原CPU，三seed正反18完整243000/216000统计UL。主比较同F1：整体最差P99配对降3.42%（6/6），最差9降5.63%，但69略恶化0.69%（3/6）；总grant RB符号成本配对增0.20%。新最差P99 10.382ms/UL均值5.142ms。对默认F10降10.26%但成本增4.36%且含F变化，不能全归新顺序。每seed先均正反再中位，不能相除两中位或当六独立seed。

3782同轮probe/已知数据quota拒绝→0，新22600延期含所有阶段；独立615620 grant、103817资源对核过。首等候均值仅降0.27%、初传跨度降2.75%，不是已消除SR。所有臂仍保留既有私有HOL-BSR配对环境，PF不使用5QI/HOL权重；本次gNB-only增量不等于已测试标准商用UE。

来源38.300 V19.4.0 §10.1/10.3、38.321 V19.4.0 §5.4.1、§5.4.4、§5.4.5及§5.4.3.1.3、38.214 V19.5.0 §6.1.2.2及§6.1.2.2.2与固定TDA/K2 §6.1.2.1，其他固定IE/表及32本地身份见docs21/方法。P05 v1 §III-B/C PDF3–4与P31另一篇v3 §V-C PDF9；教材§13.1.1.2 PDF530/532、§13.1.1.4/5 PDF537–539辅助，不把工程排序说成协议或论文强制。缺新必要原文全停并告知，不下载。

v1/pilot-01旧UPF名导致RAN前失败，保留；v2/pilot-02完整独立3/3，先导略差未丢弃，C/10 ELF与正式同SHA。main-01/42554已退出0，不重启/覆盖任何已有root或改冻结源。CHG324–329、TEST470–475，最终Git/入口TEST476；源分支latency-probe-residual，代码9f8346072e，正式交付看最后HEAD/remote。原核心/原RAN/旧失败/Office保持。

后续扩负载/UE/TDD/SCS和新同程序强对照、预测可学习业务均未做，不拿旧跨程序结果排序或计划冒成果。
