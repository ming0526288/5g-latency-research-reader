# TEST-124 TDD已测十八条件与剩余计划核验

实际steady-reruns-02/tdd/experiment.json有18尝试：三配比UL/DL六次，P0.5/1/1.25/2/2.5ms双向十次共16完整，每次4500路径关联/4000统计且逐包QFI检查0；5ms UL/DL两次RF启动前Msg3 K2越界，无业务。根工具session2914退出1，因为调度器将缺SDAP启动日志误判配置；原phase日志/退出码不修改，源配置均enable1。

实际remaining-plan-01生成退出0：原79个唯一(phase,case)，18个有runner_exit的已尝试键，剩余61，交集空/并集79；输出及关联清单见evidence/matrix_continuation.json。本次只过滤已尝试条件，不删除失败、不改变配置。新的源码经AST语法解析通过；实际剩余运行根命令与结果随后TEST-122补记。尚未完成的不得预写成功。

补充实际检查：研究计划22份gnb.conf的有效enable_sdap赋值列表均恰为[1]；AST解析rerun_sdap.py通过。python3 research/latency-analysis/source_audit/validate_reference_audit.py返回0，202条记录及28论文/教材哈希通过。本次后续条件从session34671接续。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：本项为工程操作，3GPP通信参数与新数学推导不适用；依据E01/E03，不硬贴协议条款。

依据编号：E01、E03。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：Git、文件隔离、边界修复、哈希、结果一致性或排版属于工程追溯，不修改通信协议；没有对应3GPP强制条款。相关实验条件仍以对应报告和M01为准。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
