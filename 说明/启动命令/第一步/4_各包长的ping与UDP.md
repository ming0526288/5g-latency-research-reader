# 4. 各包长的 ping 与 UDP 对比

[规划](../../文献导读/第一步/4_各包长的ping与UDP.md) · [知识点](../../算法知识点说明/十二步知识点/第一步/4_各包长的ping与UDP.md) · [结果与分析](../../研究结果与分析/第一步/4_各包长的ping与UDP.md) · [返回第一步命令](../第一步启动命令.md)

## 固定 16 B 测量部分，改变填充量

|数据区总长|测量部分|填充|ping 参数|UDP 参数|
|---:|---:|---:|---|---|
|56 B|16 B|40 B|`-s 56`|`--size 56 --header-bytes 16`|
|256 B|16 B|240 B|`-s 256`|`--size 256 --header-bytes 16`|
|1200 B|16 B|1184 B|`-s 1200`|`--size 1200 --header-bytes 16`|

包数、预热和目标间隔沿第 1 项，ping 两种大包只改 `-s`。56 B 直接复用第 2 项，256 B 精简 UDP 也供第 3 项复用。目标都是 50 包/秒，实际间隔另外测；不把不同字节负载称为完全孤立的包长效应。

## 业务工具只负责发包、回复、抓包和统计

先按[第 1 项](1_源码与当前代码.md)完成分终端启动、接入、实际 QoS 和路由核验。`business.py` 不启动、重启或停止核心网、gNB、UE；它复用原有的业务/捕获实现，按新冻结计划选择条件。RAN 的启动命令没有改成脚本。

本轮实际命令如下。`192.169.0.6` 是本轮读取到的业务地址；输出根已存在后不能覆盖，重跑须换新根。

```bash
cd ~/oiwireless/oi-wireless-ran-latency-analysis
sudo -n /usr/bin/python3 -B research/latency-analysis/step1-shared56-v1/business.py --source current --root /home/lbh/oiwireless/analysis-source-audit/step1-shared56-20261118/formal-current-01 --ue-ip 192.169.0.6
```

这是当前代码的完整 21 次独立业务运行：56/256/1200 B 的 ping 与 16 B 字段 UDP 各三轮，再加总数据区 256 B、80 B 字段 UDP 三轮。第 1—5 项按用途复用其中数据，不再分别重复运行。

每次核请求/回复数量、包长、重复与缺失、真实发送间隔、TUN/N3 关联、QFI 和捕获丢弃。UDP 另核两端日志、同一时钟域和四时刻因果顺序。所有慢包保留；失败写最后推进位置，不改阈值强行通过。
