# TEST-045：报告、图表、数值和Word核验

研究工作区运行：

```bash
python3 research/latency-analysis/tdd1/build_packet_report.py
python3 research/latency-analysis/tdd1/build_packet_report.py --refresh-figures
python3 research/latency-analysis/tdd1/validate_packet_report.py
```

均退出0；首次matplotlib提示主目录缓存不可写，使用/tmp，图成功生成。五PNG/SVG初次视觉检查发现裁切/重叠，保存初图后调整，refresh只改图与哈希；图的数字保持。修订后逐张视觉检查通过。

验证：12000测量包序号完整、无负分段、四边界匹配、0丢包；独立时间戳和统计重算、源/数据/脚本哈希、N3→tun0路由、MCS9与有限窗口无DL重传日志检查通过；180万数学核对及四TBS预算通过。不给内部处理层或样本时钟映射的虚构数字。

本地Word工作目录`/home/lbh/oiwireless`：

```bash
python3 analysis-documents/append_packet_math_to_word.py
python3 analysis-documents/validate_latency_word_v4.py
```

退出0：13表、6嵌入图、10原生公式、4个官方协议链接，来源全文核对、原始数值表和原图保持、备份及图片哈希通过。没有Word/LibreOffice分页渲染器，实际分页未渲染；图片已视觉核验。Word与备份不Git上传，详见本地CHG-Word-004/TEST-Word-004。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：TS38.214 V19.5.0 §5.1.2.1/6.1.2.1、§5.1.3.2/6.1.4.2；TS38.321 V19.4.0 §5.4.1/5.4.4/5.4.5；TS38.300 V19.4.0 §4.3.1.1/4.4.1/6。

依据编号：S03、S04、S05；B02、B03、B04、B05；P01 §III/§IV、P06 §III；C02、C03、E02、E03、M01。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：应用序号、包关联与分层边界参考P01，当前仅四个外部边界；TUN绑定和时钟语义依据Linux。MCS上限、2 Mbps、1200字节和4500/500/4000包为受控选择。单UE主动调度是已有fork行为，不臆测每包SR等待。本次重新核对的是未配置SBFD、正常CP、固定参考/数据μ=3等原实验范围；不外推为整个新Release的功能或一致性认证。全局D/U字段上限现为320、部分周期的μ适用范围已扩展，不能沿用旧版全局解释。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
