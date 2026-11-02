# TEST-023 配置准备

```bash
python3 research/latency-analysis/scs2/rfsim_scs_check.py --prepare-only --configs research/latency-analysis/results/scs2/rfsim-configs-01 > research/latency-analysis/results/scs2/preflight/config_prepare.txt 2>&1
```

退出0。生成30/120kHz两个2.5ms隔离副本，source_sha256及overrides.json保留；原配置未改。


历史副本来源：latency-scs-analysis@3ec3548a70f447ff7f988cd3c1b031c807c1bc69，原路径research/latency-analysis/records/tests/TEST-023_第二项隔离RFsim配置生成.md，原文SHA256=e331c62f1362f468b33b767f98ab15f0ed7bf94930111973bd566dd31be49fa3。原分支未改写。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.211 V19.5.0 §4.2/4.3.2；TS38.213 V19.5.0 §11.1；TS38.331 V19.4.0 §6.3.2；TS38.104 V20.1.0 §5.3.2/5.3.5。

依据编号：S01 §4.2/§4.3.2；S02 §11.1；S03；S06 TDD IE；B01、B02、B03；P02、P06；C01、M01。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：SCS和时间网格可做数学敏感性对照，采样率/初始化边界来自本fork实验。240 kHz数学模型不证明FR2-1数据/参考SCS支持；SCS阶段已暂停，不扩写为新实测。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。尚无已核实差异证明本记录固定μ=3非SBFD数据必须重测，不能把旧数据冒称新实验。若进一步确认实质错误，必须修正、重做受影响研究/实验并重写逐步CHG/TEST。
