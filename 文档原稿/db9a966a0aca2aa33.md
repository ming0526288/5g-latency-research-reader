# TEST-365 QUEST首轮准备与启动入口

2026-10-26实际运行：

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-quest-reproduction
/usr/bin/python3 -B research/latency-analysis/quest-reproduction/prepare.py --output /home/lbh/oiwireless/oi-wireless-ran-quest-reproduction/research/latency-analysis/results/quest-reproduction-01/plan-01
```

exit0，2514输入/12条件/135000完整包/120000统计包；新UE/gNB、旧共享模块同SHA，实际预期QoS9。ast与import实际通过，QST dtype104字节。sudo只读ip netns list exit0、空；未将其当接入测试。

计划启动入口（下条命令的实际退出与业务位置另记后续TEST）：

```bash
sudo -n /usr/bin/python3 -B /home/lbh/oiwireless/oi-wireless-ran-quest-reproduction/research/latency-analysis/quest-reproduction/run.py --plan /home/lbh/oiwireless/oi-wireless-ran-quest-reproduction/research/latency-analysis/results/quest-reproduction-01/plan-01/plan.json --output /home/lbh/oiwireless/oi-wireless-ran-quest-reproduction/research/latency-analysis/results/quest-reproduction-01/runs-01
```

准备时没有RAN/业务/pcap，不填时延结果。执行中每条件runner.log、status.json、execution.json及五类关联日志保留。与旧算法pilot结果不同组，不混用。
