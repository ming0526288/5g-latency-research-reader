# TEST-081 120kHz同期完整RFsim上下行业务

实际命令：

```
sudo -n /usr/bin/python3 research/latency-analysis/scs-stage2/run_ul.py --configs research/latency-analysis/results/scs-stage2/configs-02/mu3-p2p5 --output research/latency-analysis/results/scs-stage2/mu3-ul-01 --ratio 14:5
/usr/bin/python3 research/latency-analysis/tdd1/analyze_ul_packet_capture.py research/latency-analysis/results/scs-stage2/mu3-ul-01
sudo -n /usr/bin/python3 research/latency-analysis/scs-stage2/run_dl.py --configs research/latency-analysis/results/scs-stage2/configs-02/mu3-p2p5 --output research/latency-analysis/results/scs-stage2/mu3-dl-01 --ratio 14:5
/usr/bin/python3 research/latency-analysis/tdd1/analyze_packet_capture.py research/latency-analysis/results/scs-stage2/mu3-dl-01
```

四条退出0。每方向4500应用发送/接收及N3/TUN四边界完整关联，4000预热后样本，零丢包、零抓包重复；gNB/UE在流量完成时仍运行，最后仅回收自有进程。完整核心网、gNB、UE业务，非gNB-only。n261/66PRB/120kHz、P2.5ms、D14/S/U5、S6D4F4U、PRACH41，其他控制量同TEST-080。原始日志和pcap忽略保留。

UL均值1.723741168ms，P99=2.60234703ms，最大6.518404ms；DL均值0.513721802ms，P99=1.01646095ms，最大1.8144ms。分段均值UL应用→TUN/TUN→N3/N3→UPF应用为0.007427001/1.693231263/0.02298864ms；DL UPF应用→N3/N3→TUN/TUN→应用为0.016280377/0.486132067/0.011189539ms。REALTIME与MONOTONIC逐包读差最大UL0.007073ms、DL0.003822ms，如实保留。

30kHz/120kHz单次UL P99为3.909/2.602ms，DL为1.049/1.016ms，不是按4倍槽长比同比缩放。不能由此排除PRB、频段、图样符号份额、调度、主机开销；4槽是配置最小收发间隔，不声称每次实际DCI K2都固定4。未获取逐TB/DCI或层内时间戳，不能定量断言CPU瓶颈。不同运行最大值受偶发慢包影响，不宣称120kHz尾部全面更好。没有可靠P99.9结论。

第一阶段历史P2.5ms UL P99=2.77985074ms、DL1.11778018ms属于此前运行，不覆盖成当前2.60234703/1.01646095，也不混为同批。当前4次完整业务共18000四边界包/16000预热后样本。

依据CHG-050，TS38.211/213/214/331/104已列条款；P01/P02及教材B01/B03。统计为同宿主RFsim，不外推真实射频工业时延。

## 依据与适用边界 2026-10-20补注

当前依据：TS38.211 V19.5.0 §4.2/4.3.2；TS38.213 V19.5.0 §11.1；TS38.214 V19.5.0 §5.1.3.2/6.1.4.2；TS38.331 V19.4.0 §6.3.2；TS38.104 V20.1.0 §5.3.2/5.3.5。依据编号：S01、S02、S03、S05、S06、S07；B01、B02、B03；P01、P02、P06；C01、C03、E02、E03、M01。精确论文/教材页序见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)和本记录正文。

本记录对应范围：第二阶段新SCS实验：30/120kHz业务对照与30/60/120/240kHz抽象模型分开，240不视为n261数据支持。 本次新测量不继承历史“SCS暂停”的状态；不属于Release19/20全面认证。原文最高版未独立核实；实现限制与标准支持分开，所有具体参数和数学假设为项目选择。
