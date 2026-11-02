# TEST-049 UL 脚本与核心网前置检查

日期：2026-10-20。

1. git status --short 为空，从 latency-tdd-packet-delay 建新分支 latency-tdd-ul-comparison。
2. 缓存 Python 执行 `-m py_compile`，三个新增 UL 脚本通过。
3. 初始 docker ps 只有 mysql 和 phpmyadmin。首次误用 oai-amf 服务名，Compose 返回 no such service，没有修改配置。读取实际 Compose 后，用 oiwireless-amf / smf / upf 的实际服务名执行 up -d --no-recreate，三个容器启动。
4. 只读查询 UPF 既有 tun0，地址为 192.169.0.1/16，因此接收应用可使用该现有地址，不需加路由或 IP。
5. 原代码 MACRLC_nr_paramdef.h 确认支持 ul_max_mcs 参数，默认上限 28。本轮主动 UL 设上限 9，与原下行测量的业务方向上限策略对齐。其余方向参数保留。

首个 3:1 测量命令：

```bash
sudo -n python3 research/latency-analysis/tdd1/run_ul_packet_check.py --configs research/latency-analysis/results/tdd1/sa-configs-20261014-01 --output research/latency-analysis/results/tdd1/ul-d3u1-20261020-01 --ratio 3:1
```

运行时路由证据：192.169.0.1 from 192.169.0.3 dev oaitun_ue1 table 10000。实际命令、pcap 和日志保存在忽略的输出目录，测量是否完成以之后状态与四边界核验为准，不能仅依据进程启动判定通过。

复现需要 root/TUN、Docker 和本地 socket 权限。只提交安全脚本与说明，不提交 UE 凭据和完整 UE 日志。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.214 V19.5.0 §5.1.2.1/6.1.2.1、§5.1.3.2/6.1.4.2；TS38.321 V19.4.0 §5.4.1/5.4.4/5.4.5；TS38.300 V19.4.0 §4.3.1.1/4.4.1/6。

依据编号：S03、S04、S05；B02、B03、B04、B05；P01 §III/§IV、P06 §III；C02、C03、E02、E03、M01。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：应用序号、包关联与分层边界参考P01，当前仅四个外部边界；TUN绑定和时钟语义依据Linux。MCS上限、2 Mbps、1200字节和4500/500/4000包为受控选择。单UE主动调度是已有fork行为，不臆测每包SR等待。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
