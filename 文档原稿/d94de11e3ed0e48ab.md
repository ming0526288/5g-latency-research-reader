# TEST-227 PDCP观察修正单元构建与328正式准备通过

2026-10-23，以下实际exit0：
```bash
/usr/bin/python3 -B research/latency-analysis/service-baseline/verify_layer_capacity.py --output research/latency-analysis/results/service-baseline-02/unit-02
ninja -C cmake_targets/ran_build/build nr-softmodem nr-uesoftmodem rfsimulator
/usr/bin/python3 -B research/latency-analysis/service-baseline/prepare_capacity.py --output research/latency-analysis/results/service-baseline-02/plan-02
```
真实生产头、并发2000写和容量32溢出、原131072对145024事件拒绝、PDCP262144完整保留36000*4+1024事件并由旧reader读取，0600/默认OFF无文件、ASan/UBSan均过。完整ninja15步exit0，两个ELF重建、RFsim库不变，真实SHA在capacity-build.json；未关编译告警/丢记录断言。

本地10原文CRC/XML/SHA及P01/教材仍通过，旧310实际三项声明变化、PDCP C新加入覆盖。正式328冻结SHAe9f92c76e64022e6fd7a757a69f2463bf35c1e783df9189f71d4e4015cf20945，plan SHA07a933a15aea28813c148f8fe1cd3575d72deb5217eb471fd6c581cfeb44e04a，evidence/capacity-preparation.json为安全预声明。无新RAN/业务/捕获，不叫新矩阵已过。

离线collect原组成功（命令同TEST225），source/summary保留6完整/5全gate/6未尝试及原真实观察失败；原组冻结检查在C修正前执行，之后不再说当前仍通过旧310。新数据必须用新328，不混原组量化性能/观察开销。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。capacity_source_provenance_v2.json；38.323 V19.1.0§5.2.2.1/Word递归501–535为接收边界背景，未修改其中PDCP规则；38.300 V19.4.0§10.3、38.321 V19.4.0§5.4.1/2；P01 III/IV本地PDF2–4及教材13.1.1.2 PDF530–532；容量4*N*K与262144预算是工程推导，不是协议门槛。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
