# 3. 门限 0 的 UDP 多 UE启动命令

[规划](../../文献导读/第二步/3_门限0的UDP多UE.md) · [知识点](../../算法知识点说明/十二步知识点/第二步/3_门限0的UDP多UE.md) · [结果与分析](../../研究结果与分析/第二步/3_门限0的UDP多UE.md) · [返回第二步启动命令](../第二步启动命令.md)

## 本项命令与条件对应

|项|本项实际选择|核验要求|
|---|---|---|
|门限|0|gNB 配置必须对应，不靠文件名猜内容|
|工具|UDP|与另一工具分开运行，不叠加负载|
|UE 数|1、2、3|业务前确认实际活动数，不是三 UE 都挂着只给其中一个发包|
|包长|56 B 数据区|三种 UE 数口径一致|
|参考基线|第一步现在代码56 B既有结果，先不重测单UE|旧网络隔离差异写明|

共同的核心网、gNB、逐 UE 启动和停止命令见[第二步共同启动表](../第二步启动命令.md)。选择该表的门限 0 配置。每个 UE 分终端直接启动，不能用旧 RAN 启动器代替。

## 1、2、3 UE 命令参数对应

|UE数|本轮状态|工具参数|输出根|
|---|---|---|---|
|1|复用第一步门限0 UDP三轮，未新增业务|不重新执行|第一步step1-shared56-20261118|
|2|200/20先导与CPU诊断通过，正式三轮待补|`--ues 2 --regime per-ue --packets 200 --warmup 20 --rate 50 --pilot`|pilot-n2-01；CPU对照另列|
|3|共同接入失败，不运行UDP业务|不执行业务|three-ue-failure.json|

## 业务命令

UDP、回复、抓包、统计是独立业务工具；它不启动/重启/停止核心网、gNB 或 UE。以下为一个新的输出目录的先导形式：

```bash
cd ~/oiwireless/oi-wireless-ran-latency-analysis
sudo -n /usr/bin/python3 -B research/latency-analysis/step2-multiue56-v1/business.py --environment /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/environment --root /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/new-output --ues 2 --regime per-ue --packets 200 --warmup 20 --nonce 2026113000 --rate 50 --pilot
```

|需要改变的量|参数|用途|
|---|---|---|
|UE数|`--ues 1/2/3`|必须与实际已启动UE数一致|
|每UE速率固定|`--regime per-ue --rate 50`|每UE目标50包/秒|
|总速率固定|`--regime fixed-total --rate 50`|全部UE总目标50包/秒|
|正式样本|`--packets 2200 --warmup 200`，去掉 `--pilot`|每UE后2000个统计|
|新轮次|更换 `--root` 与 `--nonce`|不覆盖、不混入其他轮次|

本项当前状态：门限 0 单 UE 已有数据复用；双 UE UDP短测已通过；三 UE共同接入失败，不能启动正式业务。

## 依据与测量边界

TS 38.211 V19.5.0 §4.3.2、§7.3.2.2；TS 38.213 V19.5.0 §9.2.4、§11.1；TS 38.321 V19.4.0 §5.4.1、§5.4.4、§5.4.5；TS 38.331 V19.4.0 §6.3.2；TS 38.300 V19.4.0 §10.2/10.3。门限 0/1、56 B、50 包/秒、样本/预热和本配置均为实现或实验选择，不是协议规定的最优值。

P01《Dissecting 5G New-Radio Latency》，IFIP Networking 2025，§III–IV、本地 PDF 第 2–4 页；P24 QUEST，本地 IEEE TNSM 2026 版，§V–VI、PDF 第 6–10 页；教材 §13.1.1.2、PDF 第 530–532 页。使用用户提供且本次核读的本地版本，不冒称官网最高。17 份相关原文可读，缺件立即停止。
