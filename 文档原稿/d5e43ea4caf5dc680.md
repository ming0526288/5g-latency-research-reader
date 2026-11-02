# TEST-036：默认传输双端启动，未完成同步

工作目录：`/home/lbh/oiwireless/oi-wireless-ran-latency-analysis`。

```bash
python3 research/latency-analysis/tdd1/sa_rfsim_check.py --prepare-only --configs research/latency-analysis/results/tdd1/sa-configs-20261014-01
sudo -n python3 research/latency-analysis/tdd1/sa_rfsim_check.py --configs research/latency-analysis/results/tdd1/sa-configs-20261014-01 --output research/latency-analysis/results/tdd1/sa-run-20261014-01 --seconds 45
```

gNB关联AMF，软件UE建立RFsim TCP连接。45秒窗口内没有初始同步成功、注册完成、UE地址，未发送ping。两端测试前清理时均仍存活，最终停止完成，elapsed51.629秒（包含等待与清理）。判定：接入不通过。

初版runner整体退出0只表示脚本和清理运行完成，不能代表接入通过。后续CHG-021增加成功判据，归档verdict将此轮标为false。记录原日志中的“connect() failed, errno(0)”是该函数在成功分支后仍打印的字符串，不能仅凭该行判定TCP失败；实际也有Connection established。out-of-order一采样提示同样不能独立作根因结论。

完整日志保留于上述结果目录；归档安全摘录、commands/status/verdict及源哈希位于`tdd1/evidence/sa-20261014/sa-run-20261014-01`。没有删除失败记录。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.211 V19.5.0 §4.3.2；TS38.213 V19.5.0 §11.1；TS38.331 V19.4.0 §6.3.2 TDD IEs；TS38.300 V19.4.0 §4.3.1.1/4.4.1。

依据编号：S01、S02、S05、S06；B01、B03、B04；C01、C03、E03。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：TDD字段与协议路径有规范依据；RFsim参数、线程、启动标志和超时属于本地实现。初始化、同步、接入和业务分别判定，不把失败自动解释为违反协议。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
