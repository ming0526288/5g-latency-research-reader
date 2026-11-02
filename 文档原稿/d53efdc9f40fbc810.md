# TEST-021 SCS适配单元测试

工作目录 oi-wireless-ran-latency-analysis。

```bash
python3 -m unittest discover -s research/latency-analysis/scs2 -p test_scs.py -v > research/latency-analysis/results/scs2/preflight/unit_first.txt 2>&1
python3 -m unittest discover -s research/latency-analysis/scs2 -p test_scs.py -v > research/latency-analysis/results/scs2/preflight/unit_final.txt 2>&1
```

两次分别退出0，均5项通过。第二次删除冗余自比较断言后复测。核心验证：120kHz机会与第一项逐对象相同；固定图样和66PRB下将时间、到达缩放一半，完整FIFO结果也缩放一半；非整数周期拒绝；不同mu的有效数据RB带宽相同。

日志均保留；这是数学/接口测试，不测完整PHY延迟。


历史副本来源：latency-scs-analysis@3ec3548a70f447ff7f988cd3c1b031c807c1bc69，原路径research/latency-analysis/records/tests/TEST-021_第二项SCS单元测试.md，原文SHA256=dec165d17994d608b3ae1f6844fe62e1295e198252b457a2235c7be056b6c084。原分支未改写。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.211 V19.5.0 §4.2/4.3.2；TS38.213 V19.5.0 §11.1；TS38.331 V19.4.0 §6.3.2；TS38.104 V20.1.0 §5.3.2/5.3.5。

依据编号：S01 §4.2/§4.3.2；S02 §11.1；S03；S06 TDD IE；B01、B02、B03；P02、P06；C01、M01。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：SCS和时间网格可做数学敏感性对照，采样率/初始化边界来自本fork实验。240 kHz数学模型不证明FR2-1数据/参考SCS支持；SCS阶段已暂停，不扩写为新实测。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。尚无已核实差异证明本记录固定μ=3非SBFD数据必须重测，不能把旧数据冒称新实验。若进一步确认实质错误，必须修正、重做受影响研究/实验并重写逐步CHG/TEST。
