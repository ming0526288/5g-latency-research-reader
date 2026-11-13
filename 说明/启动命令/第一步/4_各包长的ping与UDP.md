# 4. 各包长的 ping 与 UDP 对比

[规划](../../文献导读/第一步/4_各包长的ping与UDP.md) · [知识点](../../算法知识点说明/十二步知识点/第一步/4_各包长的ping与UDP.md) · [启动命令](4_各包长的ping与UDP.md) · [结果与分析](../../研究结果与分析/第一步/4_各包长的ping与UDP.md) · [返回第一步启动命令](../第一步启动命令.md)

#### 新六条件：已执行的准备与短测命令

在研究仓库根执行以下命令，v2 先导 exit 0、六条件全部通过；输出根已经存在，禁止重新 prepare 或覆盖。v1 首次先导失败记录保留在 `pilot-01`，不能与本轮混用。固定周期与抓包关联已实现；正式三轮也已全部执行并通过独立统计复核。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-latency-analysis
/usr/bin/python3 -B research/latency-analysis/step1-ping-udp-v2/selftest.py
/usr/bin/python3 -B research/latency-analysis/step1-ping-udp-v2/prepare.py --kind pilot --output /home/lbh/oiwireless/analysis-source-audit/step1-ping-udp-implementation-20261112/pilot-02
sudo -n /usr/bin/python3 -B research/latency-analysis/step1-ping-udp-v2/run.py /home/lbh/oiwireless/analysis-source-audit/step1-ping-udp-implementation-20261112/pilot-02
```

#### 新六条件：已执行的正式三轮与复核命令

以下命令已实际执行、exit 0；`main-01` 已结束，不能重复运行或覆盖。下次重测需全新根，并重新核对协议、环境与冻结输入。

```bash
/usr/bin/python3 -B research/latency-analysis/step1-ping-udp-v2/prepare.py --kind main --output /home/lbh/oiwireless/analysis-source-audit/step1-ping-udp-implementation-20261112/main-01
sudo -n /usr/bin/python3 -B research/latency-analysis/step1-ping-udp-v2/run.py /home/lbh/oiwireless/analysis-source-audit/step1-ping-udp-implementation-20261112/main-01
/usr/bin/python3 -B research/latency-analysis/step1-ping-udp-results/aggregate.py /home/lbh/oiwireless/analysis-source-audit/step1-ping-udp-implementation-20261112/main-01 --output /home/lbh/oiwireless/analysis-source-audit/step1-ping-udp-implementation-20261112/main-01-checked
```

18 条件、39600 完整 / 36000 统计事务与 2308 冻结输入均核验通过，耗时 1163.408 s（包括全部编排与回收）。结果见[第一步结果与分析](../../研究结果与分析/第一步结果与分析.md)，规则和条件见[第一步规划](../../文献导读/第一步规划_单UE通信RTT基线.md)。图表生成与发布脚本在研究树 `step1-ping-udp-results/`，不得反复覆盖已发布数据根。
