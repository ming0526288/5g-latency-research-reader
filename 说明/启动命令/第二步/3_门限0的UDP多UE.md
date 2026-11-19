# 3. 门限 0 的 UDP 多 UE启动命令

[规划](../../文献导读/第二步/3_门限0的UDP多UE.md) · [知识点](../../算法知识点说明/十二步知识点/第二步/3_门限0的UDP多UE.md) · [结果与分析](../../研究结果与分析/第二步/3_门限0的UDP多UE.md) · [返回第二步启动命令](../第二步启动命令.md)

## 对应条件与完成范围

先按[共同启动表](../第二步启动命令.md)直接启动门限 0 基站和本轮所需 UE，核对 TUN、路由和实际 5QI9/QFI9。下面的业务工具只负责 UDP 发包、UPF 回复、抓包与统计，不管理核心网、gNB 或 UE。

|UE 数|本项完成范围|每 UE 固定负载|总量固定负载|
|---|---|---|---|
|1|复用第一步正式三轮|50 包／秒|同一个条件，不重复计数|
|2|两种负载各三轮，每轮每 UE 2200/200|各 50 包／秒|各 25 包／秒，总 50|
|3|共同接入问题后置，UDP 未开始|不执行业务|不执行业务|

## 本次正式命令

在研究仓库另开业务终端；以下为本轮第一次的实际命令。证据目录已经存在，不要覆盖。将来重新运行必须改为未存在的新 `--root`，并更换本轮标识 `--nonce`。

```bash
cd ~/oiwireless/oi-wireless-ran-latency-analysis
sudo -n /usr/bin/python3 -B research/latency-analysis/step2-multiue56-v1/business.py --environment /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/environment --root /home/lbh/oiwireless/analysis-source-audit/step2-four-formal-20261118/g0-udp-n2/r1-per-ue --ues 2 --regime per-ue --packets 2200 --warmup 200 --nonce 2026112900 --rate 50
```

|执行顺序|新输出子目录|regime|nonce|每 UE 目标包／秒|
|---|---|---|---:|---:|
|1|r1-per-ue|per-ue|2026112900|50|
|2|r1-fixed-total|fixed-total|2026112910|25|
|3|r2-fixed-total|fixed-total|2026112920|25|
|4|r2-per-ue|per-ue|2026112930|50|
|5|r3-per-ue|per-ue|2026112940|50|
|6|r3-fixed-total|fixed-total|2026112950|25|

其余参数相同；本工具的 `--rate 50` 在 `per-ue` 中表示每 UE 50，在 `fixed-total` 中表示全部 UE 合计 50。每个 UDP 数据区固定 56 B，即 16 B 事务字段＋40 B 填充。单 UE 和门限 1 的 UDP 原有正式数据按原条件引用，没有重新发包。

每轮检查应用四时刻、TUN/N3 关联、QFI 和捕获丢弃计数；全部完成后用独立端点 CSV 复算。每次进程结束并核验成功，再进入下一次；不能与 ping 叠加。门限 0 三 UE 未开始业务，不能用双 UE 结果填补。已完成后按要求暂停。

## 依据与测量边界

TS 38.211 V19.5.0 §4.3.2、§7.3.2.2；TS 38.213 V19.5.0 §9.2.4、§11.1；TS 38.321 V19.4.0 §5.4.1、§5.4.4、§5.4.5；TS 38.331 V19.4.0 §6.3.2；TS 38.300 V19.4.0 §10.2/10.3。门限 0/1、56 B、50 包/秒、样本/预热和本配置均为实现或实验选择，不是协议规定的最优值。

P01《Dissecting 5G New-Radio Latency》，IFIP Networking 2025，§III–IV、本地 PDF 第 2–4 页；P24 QUEST，本地 IEEE TNSM 2026 版，§V–VI、PDF 第 6–10 页；教材 §13.1.1.2、PDF 第 530–532 页。使用用户提供且本次核读的本地版本，不冒称官网最高。17 份相关原文可读，缺件立即停止。
