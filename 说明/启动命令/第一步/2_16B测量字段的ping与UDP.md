# 2. 16 B 数据区的 ping 与 UDP 对比

[规划](../../文献导读/第一步/2_16B测量字段的ping与UDP.md) · [知识点](../../算法知识点说明/十二步知识点/第一步/2_16B测量字段的ping与UDP.md) · [结果与分析](../../研究结果与分析/第一步/2_16B测量字段的ping与UDP.md) · [返回第一步命令](../第一步启动命令.md)

## 本项做什么

这一次 **16 B 指 ping/UDP 数据区总长**。ping 使用 `-s 16`；UDP 使用 `--size 16 --header-bytes 16`，数据区恰好放下事务标记。IPv4 无选项时，两者再加各自 8 B 传输/控制头和 20 B IP 头，IP 总长均为 44 B。

```bash
ping -D -n -I oaitun_ue1 -c 2200 -s 16 -i 0.02 -W 2 172.11.200.25
```

我配对比较 `current-r1-ping-16-h16` 与 `current-r1-udp-16-h16`，第二、三轮同条件。案例名 ping 的 h16 只是计划命名，不表示 ICMP 有 16 B UDP 探针头。旧“16 B 测量字段装入 256 B 数据区”的结果保留历史身份，不当成本轮 16 B 数据包结果。

## 先完成共用启动

核心网、gNB、UE 和接入/路由顺序，见[1. 分终端启动命令](1_源码与当前代码.md)。本页的业务命令不会替我启动无线程序。

## 业务和捕获工具

新版统一工具为 `research/latency-analysis/step1-native-v1/traffic.py`，只发业务、启回复端和抓包，不启动/停止核心网、gNB 或 UE。先导 200 包、正式 2200 包由 `--pilot` 区分；输出根必须不存在。

本轮已实际完成下列先导和正式命令；其中 `192.169.0.4` 是**本轮接入后分配的业务地址**，再次运行须先读网卡，不能照抄成永久值。它不替换 UE 启动命令中的 `--rfsimulator.serveraddr 127.0.0.1`。

```bash
ip -4 addr show dev oaitun_ue1
ip -4 route get 172.11.200.25 from 192.169.0.4 oif oaitun_ue1
cd ~/oiwireless/oi-wireless-ran-latency-analysis
sudo -n /usr/bin/python3 -B research/latency-analysis/step1-native-v1/traffic.py --source current --small-data-contrast --pilot --ue-ip 192.169.0.4 --root /home/lbh/oiwireless/analysis-source-audit/step1-current-dpdk-20261117/pilot-16-01
sudo -n /usr/bin/python3 -B research/latency-analysis/step1-native-v1/traffic.py --source current --small-data-contrast --ue-ip 192.169.0.4 --root /home/lbh/oiwireless/analysis-source-audit/step1-current-dpdk-20261117/main-16-01
/usr/bin/python3 -B research/latency-analysis/step1-native-v1/analyze_small_data.py /home/lbh/oiwireless/analysis-source-audit/step1-current-dpdk-20261117/main-16-01 --output /home/lbh/oiwireless/analysis-source-audit/step1-current-dpdk-20261117/small-data-independent.json
```

这些是已发生的命令，输出根现已存在；复跑须换新的输出根，不能覆盖。先导和正式六轮均通过，独立复算一致；真实顺序为第 1 轮 ping→UDP、第 2 轮 UDP→ping、第 3 轮 ping→UDP。工具内部执行的 ping 就是上面的直接业务命令，gNB/UE 仍由分终端命令启动。
每轮核验 TUN/N3 请求回复、QFI/方向、包长、捕获丢弃和实际到达间隔；UDP 再核验同一时钟域的四时刻。失败保留新根和最后成功步骤，不删慢包。统计按前 200 包预热、后 2000 包；RTT 不除以二冒充单向时延。

## 来源与范围

共同无线与测量来源见[实验 1 的依据](1_源码与当前代码.md)。80/16 B 格式、包长、包数、间隔是本项目测量设计，3GPP 没有指定这些值；新工具的命令行整理不等于新通信算法或性能收益。旧运行命令完整保留在原 CHG/TEST 与本地历史证据，本页用于本轮新基线。
