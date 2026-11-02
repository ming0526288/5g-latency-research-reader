# TEST-212 包级观察器ASan及完整编译核验

2026-10-23。修改前mechanism-mapping/verify_delivery.py输出/tmp/mechanism-source-check-before-C-20261023.json：10协议/6论文/教材/11源码及251旧冻结全部PASS。当前所需原文可读。

实际命令：
```bash
ninja -C cmake_targets/ran_build/build nr-softmodem nr-uesoftmodem rfsimulator
/usr/bin/python3 -B research/latency-analysis/ul-service/verify_probe.py --output research/latency-analysis/results/ul-service-01/unit-01
/usr/bin/python3 -B research/latency-analysis/multi-ue/run.py --help
```
编译第一次沙箱exit1：ccache不能在/run/user/1000/ccache-tmp创建临时文件（Read-only file system），最后完成LDPC/VCD生成检查，没有C诊断证据，不是协议或业务故障。按工具要求require_escalated重做同命令，15步骤exit0，六个C源与两个程序链接通过，RFsim库未变；evidence/build_identity.json记录真实三程序SHA。

ASan/UBSan保留完整检查在沙箱外运行exit0：默认OFF无文件；四写者4000预留和对象ID无复用；固定容量32时3968溢出、严格读取器拒绝；0600；独立有效AM12首/中/尾PDU字节与生产C双哈希一致；SN相同实体不同不混；初传/重传区间并集；畸形段和短BSR边界只记错误无越界；9字节原BSR保留；截断header/record拒绝。原输出unit-01及安全evidence/unit_validation.json。此单元不是完整AM状态机、实际SFN/NDI/CRC失败注入或新RAN测试，这些仍待图关联/先导验证。

CLI --help exit0已见新开关；四个Python源AST解析与全部after_code SHA一致。7个旧251冻结输入因本轮声明的C/运行器/主程序变化而改变，新添UE MAC/PHY/NR_IF源码也须进入新冻结；旧清单不覆盖为“通过”，旧业务数据不改。检索曾猜不存在utils、OPT/opt.c、common-policy-rerun/run.py、backlog-diagnosis/run.py和layered-stage4导致rg exit2，经实际目录/rg --files定位；无协议缺件、RAN/业务/抓包均未开始。

Git前完整索引/diff核验另按实际输出记录，不预写远端状态。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。TS38.321 V19.4.0§5.4.1/5.4.2.1/5.4.2.2/5.4.3.1.3/5.4.5/6.1.3.1、38.322 V19.3.0§5.2.3.1/6.2.2.4/6.2.3.3至5、38.212 V19.4.0§7.3.1.1.1/2、38.214 V19.5.0§6.1.2.1/6.1.4.2；P01 III/IV PDF2–4、P30v3 PDF4–6/22–23、P31v3 PDF3/9–11；教材13.1.1.2 PDF530–532；ul-service/source_provenance.json及README逐文件/事件映射。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
