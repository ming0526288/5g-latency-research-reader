# TEST-154 六项RLC分段完整栈上行业务

2026-10-21，CHG092/093，程序提交fb48f38468。实际命令在研究仓库：

```
sudo -n /usr/bin/python3 -B research/latency-analysis/standards-review/run_all_sdap.py --plan research/latency-analysis/results/rlc-queue-01/plan-01/plan.json --output research/latency-analysis/results/rlc-queue-01/runs-01 --phases multi --isolate-cases
```

session88080结束0，六个PHASE_END均0，各runner/外部关联/QFI为0，4ON的旧14边界与新RLC关联均0；没有选择性重试或更换参数。每次独立AMF→SMF→UPF恢复并确认新PFCP关联，使用实际gNB+各UE、TUN、路由、UDP及N3抓包；不拿gNB-only/ping冒充业务。仅显式UL预检的3ICMP不进入UDP单向统计。

|顺序/条件|UE|完整包|统计包|最差UE应用单向P99 ms|最后完成位置|
|---|---:|---:|---:|---:|---|
|1 n1-ul-off-b1|1|4500|4000|1.387624|完整业务/外部关联/QFI/回收|
|2 n1-ul-on-b1|1|4500|4000|1.548708|以上加旧/新内部关联|
|3 n4-ul-off-b1|4|18000|16000|1913.290192|完整业务/外部关联/QFI/回收|
|4 n4-ul-on-b1|4|18000|16000|577.558999|以上加旧/新内部关联|
|5 n1-ul-on-b2|1|4500|4000|1.705372|以上加旧/新内部关联|
|6 n4-ul-on-b2|4|18000|16000|941.615692|以上加旧/新内部关联|

合计67500完整关联/60000统计、15流；4ON45000完整/40000统计。每UE1200B/2Mbps、4500去500，120kHz n26166PRB/P0.625ms/D3-S-U1/S6D4F4U，MCS上限9；原25s接入、110s流量、120s接收期限。6项同一新程序及同配置SHA，实际主线程CPU4、policy2/priority97在流量前后核同，控制核验保存在rlc-queue/evidence/current/control_checks.json。

实际RLC分段只读C探针在整个六项运行未再修改；新汇总/画图在另一个文件，仅结束后运行。OFF两类trace目录均不存在。ON各编号包初传段覆盖完整/无重复、SN/SI一致、顺序与预算通过，45k逐包整数拆分残差0ns，掉事件/溢出0；103762新事件包含信令与预检，不全算UDP。旧14边界共630000关联事件，新文件最大15686/131072，未凭截取数据宣称完整。

本轮六项无业务失败；此前独立桩两次失败仍保留在TEST152，不删失败。原始计划、日志/pcap/trace/status及实际命令在results/rlc-queue-01；安全矩阵含逐条件程序/配置/结果SHA，不Git原始敏感文件。

局限：仅本机RFsim短有限组；N1/N4固定每UE负载导致总负载不同；每种UE数一次OFF两次ON、固定顺序。N4 OFF/ON波动不能作优化收益/纯探针成本；没有独立DCI/TB/HARQ/RFsim等待时刻，不给其份额填0，未重复长100k内部流或实现NR优化算法。

## 依据与适用边界 2026-10-20补注

本条2026-10-21新增。具体首选38.322 V19.3.0 §5.2.3.1/§5.2.3.2.3、§6.2.2.4、§6.2.3.3至5和表6.2.3.4-1；38.321 V19.4.0 §5.4.1、38.214 V19.5.0 §6.1.2.1授权背景。P01 §III/IV PDF2–4及教材§2.3.2 PDF52支持测点/分段方法。W/S/R推导、工程选择及精确函数见CHG092/README；不是协议逐项列出的3:1强制配置、实际TB测量或全面3GPP认证。
