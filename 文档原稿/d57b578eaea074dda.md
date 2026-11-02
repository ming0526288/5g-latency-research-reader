# TEST-018 K1及模型回归

```bash
python3 -m unittest discover -s research/latency-analysis/tdd1 -p 'test_*.py' -v > research/latency-analysis/results/tdd1/preflight/final_model_tests.txt 2>&1
python3 research/latency-analysis/tdd1/control_analysis.py --output research/latency-analysis/results/tdd1/control-01 > research/latency-analysis/results/tdd1/preflight/control_run.txt 2>&1
```

两项分别退出0；九项单元测试通过，反馈表输出193个时隙记录。手算.625ms D3/U1 slot0 的K1候选为4/8/9；10ms D59/U20 的slot0无4..11窗口内候选。表是方向可达性，不是ACK成功实测。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.213 V19.5.0 §9.2.3/11.1；TS38.214 V19.5.0 §5.1.2.1/6.1.2.1。

依据编号：S02 §9.2.3/§11.1；S03 §5.1.2.1/§6.1.2.1；B03；P06、P17；C02、M01。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：K1/K2定义来自标准和教材，4..11/4取值来自本fork实现。方向候选不代表实际PUCCH资源、ACK成功或完整HARQ性能。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
