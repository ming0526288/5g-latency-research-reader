# 每UE真实QoS到标准SR配置：ALG-002首个C实现

本目录来自冻结的sr-period-mechanism方法副本，所有新根与旧根独立，不重启/覆盖旧根。实际控制在openair2/LAYER2/NR_MAC_gNB/mac_rrc_dl_handler.c，不在Python仿真模型里。原始RAN保持不变。

## 修改、依据与限制

research_sr_configure在既有UE Context Setup/Modification生成CellGroupConfig后、UPER编码前运行；apply_research_sr_policy读取当前UE实际DRB的QoS配置，拒绝多DRB、多QoS及未知5QI，绝不以uid/接入顺序推断5QI。初始接入尚无DRB保持40槽，实际QoS到达后经既有标准RRC重配置发送新的SchedulingRequestResourceConfig。只支持本次审计120kHz、P0.625ms D3/S6D4F4U/U1、初始UL BWP、一个SR资源、offset3。原PUCCH/HARQ/CSI资源及SR/BSR触发和PF调度不改。

OAI_RESEARCH_SR_POLICY未设置时不读/改配置；uniform20、qos-pdb、uniform10为三个明确受支持的工程策略。qos-pdb将真实69设10槽、真实9设40槽；不是3GPP强制的5QI映射。OAI_RESEARCH_SR_PERIOD_SLOTS保持40或未设置，避免与旧全局周期实验混用。当前仅静态DRB建立时分配，不是在线学习、业务中动态切换或AUGUSTE复现。

实际查阅：TS38.401 V19.3.0 §6.1.1/8.1/8.9.2；TS38.473 V19.4.0 §8.3.1/8.3.4、§9.3.1.26/45；TS38.331 V19.4.0 §5.3.5.1/5.3.5.3/5.3.5.5.1/5.3.5.5.7与§6.3.2 PUCCH-Config/SchedulingRequestResourceConfig；TS38.213 V19.5.0 §9.2.4/9.2.5/11.1；TS38.321 V19.4.0 §5.4.4/5.4.5；TS38.211 V19.5.0 §4.3.1/2；TS23.501 V20.3.0 §5.7.3.3/4及表5.7.4-1。均为用户本地原文封面版，不冒称独立核定官网最高。来源SHA在source-preflight-resumed-01.json，相关新段实际读取见CHG295。

P05 AUGUSTE本地arXiv2606.03664v1（2026-06-02）§I/II-A/B PDF1–2、教材§13.1.1.4/5 PDF537–539支持SR等待/资源权衡动机，不支持本地周期取值强制性或未经测试的收益；未取得后续版本全文不冒称新版。既有QUEST私有HOL和观察仅作固定背景，不是标准BSR/DSR。

原fork ASN.1为17.3.0基础字段，本步与本地19.4.0原文逐项核基本IE，不是全栈升级。原fork在RRC重配置失败路径已有未实现rollback日志（与38.473 §8.3.4.2失败继续旧配置要求存在限制），本步不宣称修复该路径或认证全部标准符合性；实验门禁遇此日志立即失败，不能继续取性能样本。PREPARED日志仅证明准备配置，必须实际UE字段、机会公式和接收关联通过才称生效。

## 数学、边界与预声明

P槽对应T=.125P ms；名义SR机会率r=8000/P每无线秒。三UE真实69/9/9下，uniform20与qos-pdb均为1200机会/无线秒，uniform10为2400。均匀连续相位且pending成立、无禁止/冲突时，残余E[R]=T/2、Q99=.99T；仅理想等待参考，不是APP UL上界或实际收益。按名义PDB 60/300/300ms归一化的目标与整体最差UL P99分开报告。

单独pilot：seed1、反序、qos-pdb、三UE；只验证真实身份/配置生效/完整链，不混入正式重复。通过后正式main：三种子×正反接入×三策略18条件，轮转策略先后；同一gNB/UE ELF及八模块、同PF、1200B UDP、UL总4Mbps、每UE4500包，丢前500后4000统计。18条件243000完整/216000统计UL；六配对不是六独立种子。分别报告69、两个9、最差UE和控制/主机推进代价，不能只选69收益或拼接旧统一曲线。

新隔离核心副本latency-srp-*，172.30.208.0/24，namespace latsrp-gnb，不停止/替换原核心。pilot上限1800秒、main7200秒、剩余400秒清理预留；业务110秒/接收120秒不延长。首失败停止并保存、同根不能重启，修复另立根。完整NAS/真实QFI/QoS、无同机旁路、外部/层内/编号图、捕获零drop和观察零overflow、实际UE周期offset与TDD机会、RRC失败门禁均保留。名义机会率不等于占用RE/能耗；P99不可分段相加。所有结论限本地RFsim实现/负载，非真实空口普遍保证。

## 命令

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-sr-per-ue
cmake -S . -B cmake_targets/ran_build/build -G Ninja -DOAI_SIMU=ON -DAVX512=OFF -DAVX2=ON -DENABLE_TESTS=OFF -DE2_AGENT=OFF -DCCACHE_ACTIVE=OFF
cmake --build cmake_targets/ran_build/build --target nr-softmodem nr-uesoftmodem -j 6
/usr/bin/python3 -B research/latency-analysis/sr-per-ue/selftest.py --output NEW_SCALAR_TEST_ROOT
/usr/bin/python3 -B research/latency-analysis/sr-per-ue/selftest_policy.py --output NEW_POLICY_TEST_ROOT
sudo -n /usr/bin/python3 -B research/latency-analysis/sr-per-ue/environment_check.py --output NEW_ENV_JSON
/usr/bin/python3 -B research/latency-analysis/sr-per-ue/prepare.py --matrix pilot --output NEW_PILOT_ROOT
sudo -n /usr/bin/python3 -B research/latency-analysis/sr-per-ue/run.py NEW_PILOT_ROOT
# pilot通过后，另立正式根：
/usr/bin/python3 -B research/latency-analysis/sr-per-ue/prepare.py --matrix main --output NEW_MAIN_ROOT
sudo -n /usr/bin/python3 -B research/latency-analysis/sr-per-ue/run.py NEW_MAIN_ROOT
```

NEW为必须新建的路径，禁止替换为已有运行根。实际执行位置/退出码/失败看TEST439及后续TEST；未测不写通过。Git沿用户此前取消，Office未改。目录/运行包装工程本身3GPP额外参数及数学推导不适用。
