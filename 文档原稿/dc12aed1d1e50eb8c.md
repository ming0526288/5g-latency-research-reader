# 第一项补充：同机120 kHz gNB＋UE＋5GC接入核验

本页业务数据属于保留首UE位置例外时的原策略组。CHG095已移除该调度资格/MCS例外，当前新组见[共同上行调度基线](../scheduler-baseline/按3GPP边界建立共同上行调度基线.md)。本页原数值及程序身份保留，不能改标签冒充新规则复测或直接推算优化收益。

后续已增加[单向下行UDP时延与数学核验](第一项_数据包流程_数学推导与RFsim时延核验.md)，并更新本地Word。本记录保留初次五包接入探针的历史结果；下文“未更新Word/时延采样待做”描述的是当时状态。

2026-10-14实际启动已有核心网和RFsim两端，完成3:1、2:2、1:3的SA接入与五包ping连通性检查。没有真实射频，没有修改OAI通信源码。本次补足gNB-only预检查，不替代第一项受控负载模型，也尚未完成协议栈时延矩阵。

## 1. 结果

| 图样 | 周期/ms | UE地址 | 同步/RRC/会话 | 经UE TUN的ping | 结论 |
|---|---|---|---|---|---|
| DDDSU，3:1 | .625 | 192.169.0.3；复核.6 | 完成 | 两轮均5发5收 | 本轮SA链路通过 |
| DDSUU，2:2 | .625 | 192.169.0.4 | 完成 | 5发5收 | 本轮SA链路通过 |
| DSUUU，1:3 | .625 | 192.169.0.5 | 完成 | 5发5收 | 本轮SA链路通过 |

每轮均有UE初始同步、随机接入成功、RRC_CONNECTED、RegistrationComplete发送、UE地址配置，以及gNB到UPF的GTP-U隧道记录。用户面检查为`ping -I oaitun_ue1 -c 5 -W 2 172.11.200.25`；gNB LCID4字节计数也增加。地址由已有SMF池分配，不是配置固定地址。完整统计见[evidence/sa-20261014/summary.csv](evidence/sa-20261014/summary.csv)。

首次使用默认样本传输/线程池时，两端进程启动、gNB关联AMF、UE建立RFsim TCP连接，但45秒内未完成初始同步或获取地址。保留这个失败点，不将TCP连接等同于接入成功。

后续两端同时启用`--continuous-tx --thread-pool N`后通过。它们分别影响RFsim样本传输与线程执行方式，未逐项隔离原因；不能断言某一个开关单独解决了全部问题。连续样本传输不改变配置的上下行调度图样。

## 2. 原始配置与修改

- 独立分支`latency-tdd-rfsim-sa`从第一项分支建立，原始目录不变。
- 保留n261、120 kHz、66 PRB、.625 ms、特殊时隙6D+4灵活保护+4U、min_rxtxtime=4；完整D/U数分别为3/1、2/2、1/3。
- gNB N2/N3源地址172.11.200.1，AMF172.11.200.14，UPF172.11.200.25。RFsim使用127.0.0.1:4043，gNB服务端、UE客户端。
- UE采用原始ue.oiwireless.conf，本机已有IMSI的订阅记录；PLMN466/92、TAC100、DNN internet。未修改订阅数据库或鉴权密钥。
- 5GC来自`/home/lbh/oiwireless/oiwireless-5gc-deploy`；启动AMF/SMF/UPF，保留已运行的MySQL/phpMyAdmin。没有使用真实射频设备。
- 本次沿用独立工作区已编译的nr-softmodem/nr-uesoftmodem，无通信源码改动，因此未重复编译。

## 3. 对先前1:3失败的修正认识

先前gNB-only使用`--phy-test`模式，1:3触发MAC调度HARQ/TBS一致性断言。本轮使用`--sa`并连接实际软件UE、核心网，没有启用`--phy-test`，1:3成功接入并通过用户面探针。

因此之前的断言不能用于证明1:3违反协议或无法部署。它仍是PHY测试路径的待定位问题，没有删除断言，也没有在源码中修复其原因。本轮成功只覆盖当前参数及短时单UE业务，不能推广为所有负载、周期或长期运行均稳定。

原第一项报告、图注和Word中的“1:3未通过检查”属于当时gNB-only路径的历史结论，应与本补充并读；不能再把1:3整体归类为不可用。当前Word未在本次更新，避免把接入小样本写成完整时延分析已完成。

## 4. 复现命令

核心网目录：

```bash
cd /home/lbh/oiwireless/oiwireless-5gc-deploy
docker compose -f docker-compose-5gc.yaml up -d --no-recreate oiwireless-amf oiwireless-smf oiwireless-upf
```

分析工作区，输出目录必须不存在：

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-latency-analysis
python3 research/latency-analysis/tdd1/sa_rfsim_check.py --prepare-only --configs research/latency-analysis/results/tdd1/my-sa-config --down 3 --up 1
sudo -n python3 research/latency-analysis/tdd1/sa_rfsim_check.py --configs research/latency-analysis/results/tdd1/my-sa-config --output research/latency-analysis/results/tdd1/my-sa-run --seconds 30 --continuous
```

测试2:2或1:3时，分别指定`--down 2 --up 2`或`--down 1 --up 3`并使用新的配置/结果目录。脚本按实际日志核验接入与连通；不通过返回1，通过返回0，finally停止本次RAN进程组。运行前应确认没有其他gNB/UE占用4043、2152或oaitun_ue1。

实际gNB与UE完整命令保存在各轮`commands.json`，包含载频27547560000 Hz、--numerology 3、--ssb 301等。需要管理员网络/TUN权限及允许本机socket；不能在受限沙箱结果上推断链路故障。

## 5. 数据位置、验证边界及下一步

归档证据：[evidence/sa-20261014](evidence/sa-20261014)。完整本地日志位于忽略目录`research/latency-analysis/results/tdd1/sa-run-20261014-*`，UE配置仅本地保存。归档保留经过筛选的阶段日志、原日志SHA256、配置和命令；不含鉴权密钥。

五包ping的RTT只有连通性意义，不用于配比优劣排序、P99/P99.9或单向时延。它包含双向通信、核心网/主机处理，RFsim的样本推进与主机壁钟也不能直接当成实机无线时间。该探针未固定MCS9，包长/到达/负载亦不同于第一项模型。后续需要相同负载、包长和采样窗口，记录实际MCS/TBS/HARQ、主机CPU和包级时间戳，才可做模型对照。

测试结束后gNB、UE均已停止；本次启动的AMF、SMF、UPF保持运行，既有数据库与phpMyAdmin未停止。接下来优先做第一项受控UL/DL业务时延采样，第二项暂不推进。

修改说明：[CHG-021](../records/changes/CHG-021_第一项软件UE与5GC接入检查.md)。测试记录：TEST-035～039。原始代码和原始文档隔离检查通过。
