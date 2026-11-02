# TEST-216 PHY观察修正编译与294输入核验

2026-10-23，实际命令：
```bash
ninja -C cmake_targets/ran_build/build nr-softmodem nr-uesoftmodem rfsimulator
/usr/bin/python3 -B research/latency-analysis/ul-service/prepare_corrective.py --output research/latency-analysis/results/ul-service-01/pilot-plan-02
```
第一条沙箱外6步骤exit0，重建PHY对象/库/UE；gNB及RFsim库SHA与前组相同，UE新SHA在evidence/build_identity_v2.json。第二条exit0：10协议XML/CRC、3论文/教材和程序身份、旧278仅三项声明变化；新294清单SHA47c6553d45898a6451754576f3306525521f7f8bbe81f4d2f4caeb5f2f807bb2，plan SHAb19d38394846fd8bd070440227bb9c30ef40ca5e9fcc5bc7d22407b21d06b8ea。所有当前ul-service Python AST通过。

私人诊断v2（库外源diagnostic_v2_ignore_bad_phy_mu.py）修正列表条件后，旧4500/4000、9186初传段边及9186按包计的编码尝试边可闭合，未再遇到其他断言；明确忽略旧PHY mu，不能当正式成功或修改旧业务结论。完整新图与新PHY字段仍必须在新纠正先导核；准备并未启动RAN。无必要协议缺件/下载，未调超时。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。38.211 V19.5.0§4.3.2/表4.3.2-1、38.321 V19.4.0§5.4.1/5.4.2/5.4.3、38.322 V19.3.0§5.2.3.1/6.2.2.4/6.2.3.3至5；ul-service/source_provenance_v2.json记录原文/读段/新旧源身份，P01 III/IV PDF2–4/P30v3 PDF4–6/22–23/P31v3 PDF3/9–11及教材13.1.1.2 PDF530–532为已声明参考范围。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
