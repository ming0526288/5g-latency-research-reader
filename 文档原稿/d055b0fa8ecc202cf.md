# SR周期机制对照：结果入口

9/9真实gNB+3UE条件及独立原始数据复算完成；固定PF与原120kHz/TDD等设置，仅改标准RRC SR周期。CHG286/287/289、TEST425–431，中央CHG288/TEST432。

- [中文结果与结论](evidence/current-01/SR周期三UE时延机制对照_结果与结论.md)：三周期/三种子、配对收益、控制与RF成本、数学/协议、局限及下一步。
- [当前接续](CURRENT.md)：工作树/运行根/已做未做，禁止重启与冻结边界。
- [C/协议/参数/命令](../sr-period-mechanism/README.md)：标准字段、工程选择及完整运行方法。

verify.py独立struct/字节队列与原始sent/received复算，不import新graph/Queue；collect.py将已停止数据汇总成9条件/27流/6配对/36 RF过程CSV和安全JSON/中文MD。不是新学习算法或真实射频/RTT测量。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-sr-period-mechanism
/usr/bin/python3 -B research/latency-analysis/sr-period-results/verify.py --output /home/lbh/oiwireless/analysis-source-audit/sr-period-mechanism-20261028/independent-check-01.json
/usr/bin/python3 -B research/latency-analysis/sr-period-results/collect.py --output research/latency-analysis/sr-period-results/evidence/current-01
```

以上路径已使用，不得覆盖；重分析使用新空输出。原始日志/pcap/凭据/协议全文和Office只在本地，Git继续取消提交/推送。
