# 4. 门限 1 的 UDP 多 UE启动命令

[规划](../../文献导读/第二步/4_门限1的UDP多UE.md) · [知识点](../../算法知识点说明/十二步知识点/第二步/4_门限1的UDP多UE.md) · [结果与分析](../../研究结果与分析/第二步/4_门限1的UDP多UE.md) · [返回第二步启动命令](../第二步启动命令.md)

## 本项命令与条件对应

|项|本项实际选择|核验要求|
|---|---|---|
|门限|1|gNB 配置必须对应，不靠文件名猜内容|
|工具|UDP|与另一工具分开运行，不叠加负载|
|UE 数|1、2、3|业务前确认实际活动数，不是三 UE 都挂着只给其中一个发包|
|包长|56 B 数据区|三种 UE 数口径一致|
|参考基线|本轮补测单UE，不复用门限0的数值|旧网络隔离差异写明|

共同的核心网、gNB、逐 UE 启动和停止命令见[第二步共同启动表](../第二步启动命令.md)。选择该表的门限 1 配置。每个 UE 分终端直接启动，不能用旧 RAN 启动器代替。

## 1、2、3 UE 命令参数对应

|UE数|本轮状态|工具参数|输出根|
|---|---|---|---|
|1|正式三轮完成|`--ues 1`；每轮2200/200，per-ue与fixed-total同点只计一次|formal-n1|
|2|两种负载各三轮完成|`--ues 2`；每轮每UE2200/200|formal-n2|
|3|两种负载各三轮完成|`--ues 3`；每轮每UE2200/200|formal-n3|

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

本项当前状态：门限1 UDP已完成1/2/3 UE共15次正式业务；本工具与抓包/关联核验通过，详结果页。

## 依据与测量边界

TS 38.211 V19.5.0 §4.3.2、§7.3.2.2；TS 38.213 V19.5.0 §9.2.4、§11.1；TS 38.321 V19.4.0 §5.4.1、§5.4.4、§5.4.5；TS 38.331 V19.4.0 §6.3.2；TS 38.300 V19.4.0 §10.2/10.3。门限 0/1、56 B、50 包/秒、样本/预热和本配置均为实现或实验选择，不是协议规定的最优值。

P01《Dissecting 5G New-Radio Latency》，IFIP Networking 2025，§III–IV、本地 PDF 第 2–4 页；P24 QUEST，本地 IEEE TNSM 2026 版，§V–VI、PDF 第 6–10 页；教材 §13.1.1.2、PDF 第 530–532 页。使用用户提供且本次核读的本地版本，不冒称官网最高。17 份相关原文可读，缺件立即停止。

## 本轮正式串行业务命令

下列每条都要求先用原生终端把实际活动UE数调成对应N；工具不会替你停UE或改变gNB。在研究仓库根目录执行，三个不同输出根不能覆盖；本轮这些根已存在，复跑必须另取新根。

|对应UE数|`--ues`|`--root`|实际状态|
|---|---|---|---|
|1|1|formal-n1|3/3业务通过|
|2|2|formal-n2|6/6业务通过|
|3|3|formal-n3|6/6业务通过|

```bash
cd ~/oiwireless/oi-wireless-ran-latency-analysis
sudo -n /usr/bin/python3 -B research/latency-analysis/step2-multiue56-v1/matrix.py --environment /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/environment --root /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/formal-n1 --ues 1 --plan /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/formal-gate1-plan.json
```

N=2/3对应命令只把`--ues`和新输出根分别换成表中两项。正式计划先冻结，per-ue为每UE50包/秒，fixed-total为总50包/秒；N=1相同点不重复运行。以上只管理独立UDP端点/捕获/统计，不启动/停止任何RAN或核心网。
