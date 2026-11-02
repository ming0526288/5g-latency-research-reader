# TEST-413 连续服务独立事件复算与调度空档核验

2026-10-28，CHG279。只读旧数据，未启动RAN。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-quest-qos-identity
/usr/bin/python3 -B research/latency-analysis/service-gap-analysis/verify.py /home/lbh/oiwireless/analysis-source-audit/service-gap-20261028/analysis-01
/usr/bin/python3 -B research/latency-analysis/service-gap-analysis/windows.py /home/lbh/oiwireless/analysis-source-audit/service-gap-20261028/analysis-01 --output /home/lbh/oiwireless/analysis-source-audit/service-gap-20261028/windows-01
```

verify实际session64445退出0，15条件全部PASS：45流202500完整/180000统计请求、45个独立事件队列、2328378条独立决策；162000旧混合包W/分段数一致，465个已填充原始记录前缀SHA与文件尺寸一致。结果analysis-01/independent-check.json。前缀SHA不冒称整个预分配文件全SHA。

windows实际退出0，45流窗口诊断通过。s1-reverse-quest UE0最长进展间隔45.421359ms中，相关pf_ul调用空档41.720823ms、与本UE区间重叠41.097361ms，相邻目标UL标签仅5槽/0.625ms；同轮UE2相关42.370628ms间隔也含该空档。s3-reverse-quest UE0的连续17次候选被拒，跨度12.065742ms，关联最大调用空档约0.892411ms，是另一类证据。不能将无调用墙钟空档唯一归CPU或死锁。

按原local38.211 V19.5.0 §4.3.2、表4.3.2-1及既有mu3配置解释5槽；38.214 V19.5.0 §6.1.2.1实际基础段已核。各源原件在25预检范围，新增缺件0。没有过滤极端慢样本。最终报告数值/链接/身份核验见TEST414。
