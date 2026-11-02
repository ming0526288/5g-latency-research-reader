# CHG-042 第一阶段恢复与八周期完整RFsim对照

## 目的、范围与来源

用户明确恢复实验，继续第一阶段TDD分析。新增period_rfsim_matrix.py，分别准备并顺序启动8个基础周期的UL、DL完整RFsim。现有OAI通信源码、UL/DL runner、原始仓库及5GC配置不改；不同SCS、多UE与优化算法不混入本轮。

标准依据为本地官方解压Word：TS38.213 V19.5.0 §11.1（周期P、参考μ、起始D/末尾U/中间F）；TS38.331 V19.4.0 §6.3.2 TDD-UL-DL-Pattern（8基础周期的枚举与字段）；TS38.211 V19.5.0 §4.3.2（正常CP及μ=3网格）。TS38.214 V19.5.0 §5.1.2.1/6.1.2.1与TS38.213 §9.2.3支持区分K0/K2和HARQ反馈时序；仅方向字段合法不保证现有OAI可接入。TS38.300 V19.4.0 §4.3.1.1/4.4.1/6支持用户面路径边界。

教材B01 §4.3.1 PDF79/80、B03 §6.4.3 PDF211至213；P17 §III/IV PDF3/4及P19 §II/III PDF2/3支持方向分布、双向评价的研究设置；P01 §III/IV PDF2至4支持按包关联和边界测量。本轮实际重读这些本地提取页；不复制其算法或性能。具体来源文件、哈希见docs/10与source_audit/current_protocol_review.json；官网最高版未独立确认，不把用户提供版本或当前fork宣称为Release全面认证。

## 配置变更与数学

仅生成忽略目录的gnb.conf：dl_UL_TransmissionPeriodicity依次0..7，对应P=0.5/0.625/1/1.25/2/2.5/5/10ms；nrofDownlinkSlots/nrofUplinkSlots依次2:1、3:1、5:2、7:2、11:4、14:5、29:10、59:20。保持部分符号6D4F4U、120kHz、66PRB、单UE和两方向MCS上限9。

μ=3时Ts=0.125ms，N=P/Ts=8P，D+U+1=N。上述为完整槽配比接近3:1的一族，并非相同D/U符号占比；总D符号=14D+6，总U符号=14U+4，F=4。不能把该实验解释为严格单变量因果比较。每个候选逐符号调用原始set_tdd_config_nr核验。

均匀到达至下一方向机会的E[W]=Σg_i²/(2P)，F_W(w)=Σmin(w,g_i)/P；m个连续槽机会时m-1个间隔Ts，最后一个P-(m-1)Ts。应用时延还含排队、授权/反馈、跨TB、处理和主机/RFsim传输，不能要求等待闭式等于完整业务单向时延。

业务与旧对照一致：UDP载荷1200B、目标2Mbps、4500包、前500预热、4000测量包、固定Poisson种子20261014。UL和DL单独顺序运行，不是同时双向。UL绑定UE TUN；DL核对UPF tun0路由；两方向四边界按序号全关联。保留失败与尾包，不调整阈值，不用RTT替代单向。

## 命令与归档

```bash
python3 research/latency-analysis/tdd-standard/period_rfsim_matrix.py prepare --output research/latency-analysis/results/tdd-standard/period-configs-current-01
sudo -n /usr/bin/python3 research/latency-analysis/tdd-standard/period_rfsim_matrix.py run --configs research/latency-analysis/results/tdd-standard/period-configs-current-01 --output research/latency-analysis/results/tdd-standard/period-rfsim-current-01
```

完整日志、UE配置及pcap仅本地忽略results。执行结果逐项写TEST-067/068及后续报告，运行前不预填成功。原文不上传Git，Word整合另按documents技能完成。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.214 V19.5.0 §5.1.2.1/6.1.2.1、§5.1.3.2/6.1.4.2；TS38.321 V19.4.0 §5.4.1/5.4.4/5.4.5；TS38.300 V19.4.0 §4.3.1.1/4.4.1/6。

依据编号：S03、S04、S05；B02、B03、B04、B05；P01 §III/§IV、P06 §III；C02、C03、E02、E03、M01。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：应用序号、包关联与分层边界参考P01，当前仅四个外部边界；TUN绑定和时钟语义依据Linux。MCS上限、2 Mbps、1200字节和4500/500/4000包为受控选择。单UE主动调度是已有fork行为，不臆测每包SR等待。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
