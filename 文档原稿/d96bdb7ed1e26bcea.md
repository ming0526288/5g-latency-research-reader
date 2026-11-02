# TEST-067 八周期准备与实验前检查

2026-10-20，对应CHG-042。用户恢复第一阶段实验。当前分支latency-tdd-standard-patterns，前一提交9755b3a8ea。协议/文献/教材定位及推导见CHG-042，原文实际相关条款可读，暂不缺上述7份资料。

实际检查：ps未发现既有softmodem/tcpdump；普通docker ps遇到socket权限拒绝，未操作容器。依环境权限申请后sudo -n docker ps只读确认现有oiwireless-amf/smf/upf运行；无核心网重建、配置修改或密钥导出。权限失败不属通信实验失败，没有发业务或抓包。

实际执行：

```bash
python3 research/latency-analysis/tdd-standard/period_rfsim_matrix.py prepare --output research/latency-analysis/results/tdd-standard/period-configs-current-01
```

退出0，8个候选逐符号与原OAI C构造一致。完整槽D/U、周期枚举及源/目标gnb.conf SHA在该目录cases.json，适配器来源在adapter/provenance.json。原始配置保留，UE配置权限0600，不输出凭据。本次准备不代表PHY、接入或业务成功。

完整RFsim运行与逐包核验另记TEST-068；所有失败保留最后成功阶段和0样本/部分样本事实。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.211 V19.5.0 §4.3.2；TS38.213 V19.5.0 §11.1；TS38.331 V19.4.0 §6.3.2 TDD IEs；TS38.300 V19.4.0 §4.3.1.1/4.4.1。

依据编号：S01、S02、S05、S06；B01、B03、B04；C01、C03、E03。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：TDD字段与协议路径有规范依据；RFsim参数、线程、启动标志和超时属于本地实现。初始化、同步、接入和业务分别判定，不把失败自动解释为违反协议。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
