# TEST-080 30kHz完整RFsim上下行业务

已有5GC运行。独立完整gNB+UE，两方向顺序分别启动新会话，不并发；同一宿主内核时钟。n78、30kHz、273PRB、100MHz标称、P2.5ms、D3/S/U1（6D4F4U）、MCS双向上限9。原二进制，未重编通信源码。

实际命令（工作目录研究仓库）：

```
sudo -n /usr/bin/python3 research/latency-analysis/scs-stage2/run_ul.py --configs research/latency-analysis/results/scs-stage2/configs-02/mu1-p2p5 --output research/latency-analysis/results/scs-stage2/mu1-ul-01 --ratio 3:1
/usr/bin/python3 research/latency-analysis/tdd1/analyze_ul_packet_capture.py research/latency-analysis/results/scs-stage2/mu1-ul-01
sudo -n /usr/bin/python3 research/latency-analysis/scs-stage2/run_dl.py --configs research/latency-analysis/results/scs-stage2/configs-02/mu1-p2p5 --output research/latency-analysis/results/scs-stage2/mu1-dl-01 --ratio 3:1
/usr/bin/python3 research/latency-analysis/tdd1/analyze_packet_capture.py research/latency-analysis/results/scs-stage2/mu1-dl-01
```

四条退出0。每方向4500发送/接收/四边界匹配，4000预热后样本，零丢包/重复。UL均值2.705616893ms、P99=3.90936132ms、最大4.681879ms；DL均值0.719667060ms、P99=1.04934213ms、最大5.053877ms。最大值没有删除；DL慢包可能来自外部段，不能笼统归因无线。实际payload约2.0371Mbps，目标2Mbps是随机到达期望，单次有限样本实际不强制等于目标。

UL应用→TUN、TUN→N3、N3→UPF应用均值0.007404916/2.673867333/0.024311624ms；DL UPF应用→N3、N3→TUN、TUN→应用0.017641203/0.688700547/0.013235449ms。分段REALTIME总量与MONOTONIC存在非原子读差异，最大分别0.008492/0.036329ms，逐包如实记录，未通过阈值筛包。分段均值和对应REALTIME总量，不直接加P99。路由UL强制oaitun_ue1，DL核验UPF tun0；发送前完成UE接入和TUN配置。

原始status/commands/sent/received/pcap/matched/measurement及日志位于上述results目录，不上传。全部自有子进程已回收。P99.9不报告；每方向仅一个4000样本运行，不支持跨次置信或稳定尾机制结论。30/120跨频段/PRB/方向份额/4槽毫秒数不同，不能单变量归因SCS。依据CHG-050和P01/P02，以及TS38.104/211/213/331相关条款。

## 依据与适用边界 2026-10-20补注

当前依据：TS38.211 V19.5.0 §4.2/4.3.2；TS38.213 V19.5.0 §11.1；TS38.214 V19.5.0 §5.1.3.2/6.1.4.2；TS38.331 V19.4.0 §6.3.2；TS38.104 V20.1.0 §5.3.2/5.3.5。依据编号：S01、S02、S03、S05、S06、S07；B01、B02、B03；P01、P02、P06；C01、C03、E02、E03、M01。精确论文/教材页序见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)和本记录正文。

本记录对应范围：第二阶段新SCS实验：30/120kHz业务对照与30/60/120/240kHz抽象模型分开，240不视为n261数据支持。 本次新测量不继承历史“SCS暂停”的状态；不属于Release19/20全面认证。原文最高版未独立核实；实现限制与标准支持分开，所有具体参数和数学假设为项目选择。
