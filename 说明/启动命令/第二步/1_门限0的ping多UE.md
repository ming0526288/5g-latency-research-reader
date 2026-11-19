# 1. 门限 0 的 ping 多 UE启动命令

[规划](../../文献导读/第二步/1_门限0的ping多UE.md) · [知识点](../../算法知识点说明/十二步知识点/第二步/1_门限0的ping多UE.md) · [结果与分析](../../研究结果与分析/第二步/1_门限0的ping多UE.md) · [返回第二步启动命令](../第二步启动命令.md)

## 本项命令与实际状态

先按[第二步共同启动表](../第二步启动命令.md)选择门限 0 配置，核心网、gNB、各 UE 分终端直接启动。业务工具不启动无线程序，不加 continuous-tx 或额外线程池。看到所有本轮 UE 的 TUN 地址并核路由、实际 NAS/QFI 后，才开始本页业务。

|UE 数|每种负载的规模|每 UE 固定负载间隔|总量固定间隔|实际完成范围|
|---|---|---|---|---|
|1|三轮各 2200，前 200 预热|0.02 s|与左侧同一条件，不重复测|既有三轮复用|
|2|各三轮，每轮每 UE 2200/200|0.02 s|0.04 s|两种负载均已补齐|
|3|未开始本工具业务|不执行|不执行|共同接入问题后置，RTT 未测|

## 先捕获 再在独立终端运行原生 ping

捕获终端进入研究仓库，以下为正式双 UE、每 UE 50 包／秒的命令形式。`--root` 必须换成未存在的新目录；此命令仅抓包、检查路由和核验，不启动 ping／gNB／UE。

```bash
cd ~/oiwireless/oi-wireless-ran-latency-analysis
sudo -n /usr/bin/python3 -B research/latency-analysis/step2-multiue56-v1/ping_capture.py --environment /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/environment --root /home/lbh/oiwireless/analysis-source-audit/new-ping-output --ues 2 --regime per-ue --packets 2200 --warmup 200
```

看到 `READY` 后，在两个独立业务终端分别执行；用各自新输出目录的 `ping.log` 保存完整原生结果：

```bash
sudo -n ip netns exec s2m56u0 ping -D -n -I oaitun_ue1 -c 2200 -s 56 -i 0.02 -W 2 172.11.200.25 | tee /home/lbh/oiwireless/analysis-source-audit/new-ping-output/ue0/ping.log
```

```bash
sudo -n ip netns exec s2m56u1 ping -D -n -I oaitun_ue1 -c 2200 -s 56 -i 0.02 -W 2 172.11.200.25 | tee /home/lbh/oiwireless/analysis-source-audit/new-ping-output/ue1/ping.log
```

总量固定组将捕获改为 `--regime fixed-total`，两个 UE 的 ping 都改为 `-i 0.04`；三 UE 的对应间隔为 `0.06`。每轮换新输出根。两路／三路发包要在同一测试时段进行；原生终端自然启动，事后核对实际公共统计时段，不要求修改 RFsim 启动相位。

全部 ping 真正结束、确认发收数量后，另一个普通终端执行以下结束标记，捕获工具才会停止自己的 tcpdump 并核验；管道退出 0 不能代替数量与 TUN/N3/QFI 检查：

```bash
touch /home/lbh/oiwireless/analysis-source-audit/new-ping-output/finish.request
```

独立短测使用新的目录，包数／预热对应 200/20；它与正式 2200/200 分开保存。三轮正式合计每 UE 6600 完整、6000 统计。不能只把第一次测试的前 200 次预热当成独立短测。

## 200 MHz 独立短测命令

核心网沿用共同启动方式。本轮复用原核心网。基站在后置策略试验构建目录直接启动，使用新配置 132 PRB、门限 0。这个配置还沿用已有的 RFsim 同步项。

```bash
cd ~/oiwireless/analysis-source-audit/step2-three-ue-admission-20261119/residual-build-v2
sudo -n OAI_RESEARCH_PROBE_POLICY=residual ./nr-softmodem -O /home/lbh/oiwireless/oi-wireless-ran-latency-analysis/research/latency-analysis/step2-multiue56-v1/configs/gnb1.sa.band261.fr2.132PRB.5slot.multiue.mcs9.inactivity0.sync1.dpdk.conf --sa --rfsim --rfsimulator.serveraddr server
```

在独立终端分别启动各 UE。下例用 `ue_index=0`，第二、第三台分别为 1、2。前一台有 TUN IPv4 后再接入下一台。本批先测单 UE，再加入第二台，最后加入第三台。

```bash
cd ~/oiwireless/oi-wireless-ran-ping-slot-validation/cmake_targets/ran_build/build
ue_index=0
sudo -n ip netns exec "s2m56u${ue_index}" ./nr-uesoftmodem --band 261 -C 27612360000 -r 132 --numerology 3 --ssb 301 --sa -O "/home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/environment/private/ue${ue_index}.conf" --ue-txgain 0 --ue-rxgain 20 --ue-fo-compensation --rfsim --rfsimulator.serveraddr "10.203.$((ue_index+1)).1"
```

三个 UE 数分别使用新的捕获目录，`--ues` 为 1、2 或 3。下例为单 UE；实际证据在 `step2-gate0-200mhz-ping-20261119/n1`、`n2`、`n3`。

```bash
cd ~/oiwireless/oi-wireless-ran-latency-analysis
sudo -n /usr/bin/python3 -B research/latency-analysis/step2-multiue56-v1/ping_capture.py --environment /home/lbh/oiwireless/analysis-source-audit/step2-multiue56-20261118/environment --root /home/lbh/oiwireless/analysis-source-audit/new-200mhz-n1 --ues 1 --regime per-ue --packets 200 --warmup 20
```

看到捕获终端显示 `READY` 后，在每个业务终端直接运行 ping。双／三 UE 组让各路业务在同一时段运行。下例为单 UE。每组全部 ping 完成后再创建本组的 `finish.request`，按上文核验收包。

```bash
sudo -n ip netns exec s2m56u0 ping -D -n -I oaitun_ue1 -c 200 -s 56 -i 0.02 -W 2 172.11.200.25 | tee /home/lbh/oiwireless/analysis-source-audit/new-200mhz-n1/ue0/ping.log
```

200 MHz 与 132 PRB 的对应、频率栅格和同步栅格按 TS 38.104 V20.1.0 §5.3.2／§5.3.5／§5.4.2／§5.4.3 及 TS 38.101-2 V20.1.0 对应表核对。实际参数差异和首轮未接入原因见 CHG478／TEST633。

## 本轮证据目录

目录前缀为 `/home/lbh/oiwireless/analysis-source-audit/`；下列是已运行证据，不能原样覆盖重跑。

|条件|目录|用途|
|---|---|---|
|单 UE|step1-shared56-20261118|既有三轮参照，未新增发包|
|双 UE|step2-four-formal-20261118/g0-ping-n2-concurrent|五轮原证据链接＋一轮并发补正；原六次仍在 g0-ping-n2|
|三 UE|step2-multiue56-20261118/three-ue-failure.json|共同接入记录，无 RTT|

本批补测结束后暂停。原生 RTT 不除以 2 冒充单向时延；完整原生输出、pcap 和配置身份保留在本地。

## 依据与测量边界

TS 38.211 V19.5.0 §4.3.2、§7.3.2.2；TS 38.213 V19.5.0 §9.2.4、§11.1；TS 38.321 V19.4.0 §5.4.1、§5.4.4、§5.4.5；TS 38.331 V19.4.0 §6.3.2；TS 38.300 V19.4.0 §10.2/10.3。门限 0/1、56 B、50 包/秒、样本/预热和本配置均为实现或实验选择，不是协议规定的最优值。

P01《Dissecting 5G New-Radio Latency》，IFIP Networking 2025，§III–IV、本地 PDF 第 2–4 页；P24 QUEST，本地 IEEE TNSM 2026 版，§V–VI、PDF 第 6–10 页；教材 §13.1.1.2、PDF 第 530–532 页。使用用户提供且本次核读的本地版本，不冒称官网最高。17 份相关原文可读，缺件立即停止。
