# SR周期机制对照：40/20/10槽，同一新程序

用户2026-10-28授权继续下一步。本目录检验固定SR周期能否改变候选前等待，不是自适应算法、AUGUSTE复现或新的PF/QUEST权重。当前实测状态看CURRENT.md与CHG286起/TEST425起，入口命令不代表通过。旧状态观察、失败/原始数据不覆盖。

## 问题与变量

前一轮新增状态表明：确认编号积压的no_data中99.06%实际E0，SR实际40槽/5ms，本批正SR均能对应gNB接受。现在固定其他因素，只改变标准RRC SR周期，验证请求机会等待与控制代价；不能先把周期缩短量当成端到端收益。

PF固定，三UE反序接入、120kHz/n261/66PRB、原P0.625ms D3/S/U1（S6D4F4U）、MCS上限9、1200B、UL总4Mbps、每UE4500完整/前500热身后4000统计、原CPU布局与私有HOL/所有观察器不变。每种子三种周期共9条件，121500完整/108000统计UL；不是RTT、闭环或P99.9可靠性验证。

|业务种子|周期执行顺序/槽|profile|
|---|---|---|
|20301027|40→20→10|[69,9,9]|
|20302027|20→10→40|[9,69,9]|
|20303027|10→40→20|[9,9,69]|

每种子内相同随机到达计划、包长/负载/profile，周期轮换减少执行顺序影响；3个配对种子，不是9个独立种子。主要逐种子比较最差UE UL P99，另列每UE、首次序列化等待、全部交付/失败和控制/处理成本。正式结果不只报最优周期或最好一轮。

## 实际3GPP与文献依据

开始核25 DOCX SHA/CRC/XML及P24/教材可读；递归本地原文/ZIP，不自行下载。本次全部所需原文可读，没有缺件；后续若缺必要协议立即全研究停止，用户补齐并明确恢复后继续。本地已授权封面版本不冒称独立官网最高。

|用途|实际原文定位|如何应用|
|---|---|---|
|标准周期/offset字段|TS38.331 V19.4.0 §6.3.2 SchedulingRequestResourceConfig，递归39057–39077|sl10 offset0–9、sl20 offset0–19、sl40 offset0–39；本实验各offset3合法。标准列可配置字段，不强制这三种周期用于本场景。|
|机会与有效资源|TS38.213 V19.5.0 §9.2.4，2999–3009含OMML|按配置周期/偏移判断SR机会，资源符号须可用；不能每槽都算SR发送。|
|UCI复用|38.213 V19.5.0 §9.2.5，3020起|保留原HARQ/CSI/PUCCH/PUSCH复用实现，统计资源不可用及正负SR，不认证已审全所有复用场景。|
|TDD符号|38.213 V19.5.0 §11.1，4619–4647|原mu3/P0.625ms有效；按D/S/U符号判断PUCCH位置，不修改原TDD。|
|SR/BSR状态|TS38.321 V19.4.0 §5.4.4/5.4.5，2499/2602起|pending、禁止计时、次数/取消及BSR报告保持；不是每包强制先完成独立SR握手。|
|时隙/帧|38.211 V19.5.0 §4.3.1/4.3.2表4.3.2-1|mu3每10ms帧80槽，0.125ms；原文帧长对象已有独立读取记录。|
|SR等待/资源动机|P05 AUGUSTE本地6页，arXiv:2606.03664v1，2026-06-02，§I/II-A/B PDF1–2|只借鉴请求等待/控制资源权衡；未实施论文学习或预测授权。未核读后续全文，不冒称该v1是最新版。论文“best case至少完整SR周期”不能代替实际相位残余下界，作者RTT数值不套到本机UL。|
|教材解释|指定5G教材§13.1.1.4/5，本地PDF537–539|SR请求资源、BSR报告数据量；原文优先，教材不强制本地周期或算法。|

段号是本地辅助位置，不是官方PDF页码。P01 Dissecting本地6页IFIP Networking2025只核封面/分层动机，不假称采用其SR公式。P24 QUEST的既有私有HOL保持，未更新论文身份或冒称标准BSR/DSR。辅助文本/身份与失败放analysis-source-audit/sr-period-mechanism-20261028，协议目录只保留原件。

## 数学与资源检查

`Tslot=10/80=0.125ms`，SR机会满足`(80*SFN+slot−3) mod P=0`。原TDD周期5槽，P为10/20/40，均有`(3+mP) mod5=3`，机会落原S槽；S最后4符号10–13为UL，原PUCCH0使用symbol13、1符号。PRB为8+uid，各UE不同；原CSI PUCCH2用PRB0–7/symbol13，频域分开。原同PUCCH资源的HARQ复用路径保留，动态处理限制及失败仍须实际观察。

|P/槽|周期/无线ms|理想连续均匀相位残余均值/ms|每UE机会/无线秒|
|---:|---:|---:|---:|
|40|5|2.5|200|
|20|2.5|1.25|400|
|10|1.25|0.625|800|

理想模型假设pending已触发、资源有效、无禁止/冲突且到达连续相位均匀，R服从[0,P*Tslot]均匀分布，E[R]=P*Tslot/2；不是实测墙钟下界/上界。pending若在本槽机会处理后才成立可错过本机会。实际UL还含主机/RFsim推进、轮询、授权、初传、重组等；P99不能把分段相加。机会增多不等于正SR数量同比增加，也不等于实际占用RE或功耗的直接测量。

## C改了哪里、为什么

新树oi-wireless-ran-sr-period-mechanism/latency-sr-period-mechanism，base4ca5b42a67。复制上一轮冻结的4个只读观测C+ul_state_trace.h作为固定基础；原程序不改。唯一新增无线配置控制在nr_rrc_config.c::set_SR_periodandoffset：

`OAI_RESEARCH_SR_PERIOD_SLOTS=40/20/10`选择原SchedulingRequestResourceConfig的标准choice；未设/空值走原逻辑。显式40必须与旧default逐字节UPER一致。研究开关仅限mu3、无pattern2、P0.625ms/D3/S6D4F4U/U1/offset3；非法值和其他工作点拒绝。这是本研究的保护范围，不是标准禁止其他SCS/周期组合。

UE不设置旁路周期，仍真实解析RRC；共享find_period_offset_SR与两端机会判断不改。只改周期，不改SR资源、offset、禁止计时/次数、BSR字节、排序权重、UE名额或MCS。实际gNB日志[SR-PERIOD]与每个UE观察到的period/offset必须吻合。

本fork生成的RRC ASN.1仍是原有17.3.0 schema；所用基本sl10/20/40 choice与本地V19.4.0原文逐项一致，不涉及新增扩展。没有把整个OAI升级成Release19或宣称全栈Release19一致性认证。

固定使用同一两个新ELF和8个原样共享模块。旧ASN静态库仅用于独立构造/UPER夹具；新gNB/UE须本树完整编译，不能用旧ELF性能当新结果。

## 成功/失败与开销口径

自有latency-sr-*、latsr0/latsr-gnb和172.30.207.0/24，原数据库只读快照启动副本；原核心不停止/替换。每UE业务110秒/接收120秒、原TUN等待、根3600秒/清理400秒预声明，失败停止剩余条件，不改阈值或删包重试到成功。

完整gNB+3UE/真实NAS/5QI/QFI、路由、APP与外部/层内/完整初传服务图、抓包0drop、观察0overflow、线程/模块身份等门禁不变。因本轮研究不是候选排序对比，预先取消旧mixed中的“必须同时正积压并出现资源落选”前提；仍统计其次数，不以它过滤有效周期条件，变更见CHG287。

额外核实际SR周期/offset、TDD机会/原PUCCH资源范围；记录UE机会/正负返回、gNB正负指示、SR接收/配置对应、资源错误日志。pf_ul局部墙钟耗时按每轮去重，**不包含整个PUCCH解码CPU成本**；不把事件数当RE/功耗实测。单UE4000样本不认证P99.9或普遍无饿死/死锁。

## 命令入口

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-sr-period-mechanism
/usr/bin/python3 -B research/latency-analysis/sr-period-mechanism/selftest.py --output /home/lbh/oiwireless/analysis-source-audit/sr-period-mechanism-20261028/tests-01
cmake --build cmake_targets/ran_build/build --target nr-softmodem nr-uesoftmodem -j 6
/usr/bin/python3 -B research/latency-analysis/sr-period-mechanism/prepare.py --output /home/lbh/oiwireless/analysis-source-audit/sr-period-mechanism-20261028/plan-01
sudo -n /usr/bin/python3 -B research/latency-analysis/sr-period-mechanism/run.py /home/lbh/oiwireless/analysis-source-audit/sr-period-mechanism-20261028/plan-01
```

路径已存在或execution已开始时禁止覆盖/重启；运行后读完整CHG/TEST和CURRENT，不把命令列表当通过。Git沿用户取消要求不commit/push，Word/PPT本轮未改，原始日志/pcap/凭据/协议全文不上Git。
