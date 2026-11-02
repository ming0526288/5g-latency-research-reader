# TEST-022 原始采样率函数

```bash
python3 research/latency-analysis/scs2/probe_sampling.py --output research/latency-analysis/results/scs2/sampling-01 > research/latency-analysis/results/scs2/preflight/sampling_probe.txt 2>&1
```

脚本退出0，八个输入符合独立源代码预期。30kHz/273PRB与120kHz/66PRB子进程退出0；其余六项退出-6（SIGABRT）。60/240 stderr为“Numerology 2/4 not supported for the moment”；30kHz模型RB数不是支持的载波grid，原函数按“不支持N_RB”拒绝。

逐项记录sampling_support.csv和mu*_prb*.txt，生成C及源码SHA256保留。拒绝是支持边界结果，不伪装成链路成功；无实际射频，无UDP流，无软件UE。


历史副本来源：latency-scs-analysis@3ec3548a70f447ff7f988cd3c1b031c807c1bc69，原路径research/latency-analysis/records/tests/TEST-022_实际采样率函数支持验证.md，原文SHA256=7df6ac00ba4d71d9fe02b4a0cd0718189672b7456960b7b150744397d1e51164。原分支未改写。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.211 V19.5.0 §4.2/4.3.2；TS38.213 V19.5.0 §11.1；TS38.331 V19.4.0 §6.3.2；TS38.104 V20.1.0 §5.3.2/5.3.5。

依据编号：S01 §4.2/§4.3.2；S02 §11.1；S03；S06 TDD IE；B01、B02、B03；P02、P06；C01、M01。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：SCS和时间网格可做数学敏感性对照，采样率/初始化边界来自本fork实验。240 kHz数学模型不证明FR2-1数据/参考SCS支持；SCS阶段已暂停，不扩写为新实测。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。尚无已核实差异证明本记录固定μ=3非SBFD数据必须重测，不能把旧数据冒称新实验。若进一步确认实质错误，必须修正、重做受影响研究/实验并重写逐步CHG/TEST。
