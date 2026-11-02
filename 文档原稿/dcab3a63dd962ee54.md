# CHG-234 QUEST原公式与五基线及十微秒HOL生产函数

2026-10-26。新增生产头nr_quest_metric.h：QUEST按P24 §V-B式(10) PDF7、MT/PF/PB/EDF/M-LWDF按§VI-C式(12)–(16) PDF8–9实现，统一HOL/PDB为ms，epsilon0.001ms来自固定作者patch269行。输入TBS沿用OAI近似表的字节口径，已实际核nr_init_fr1_ulsch_preprocessor末尾>>3；不是把近似1PRB TBS当整个实际grant大小，也不加入上一轮8轮/2倍补偿。

仅显式提供本轮核对的5QI2/9/69/82/83/84标准属性，未知返回无效，不能默认猜PDB或把QFI当5QI。来源TS23.501 V20.3.0 §5.7.4表5.7.4-1；9的300ms/PER1e-6按表中共享单元及相邻连续边界核对，不把空白当0。GBR实际信令条件仍需运行前核验，提供表项不代表已建立该QoS流。

新增NR_MAC_COMMON/nr_quest_hol.h：私有16bit大端/10µs HOL编码，容量不足不写，超过655.35ms饱和而非回绕；该字节序是明确的工程约定，不把论文未列的端序说成标准规定。本步只有可测试函数，尚未接入MAC报文或gNB排序，也未改变UE/gNB运行行为。

新增test_metric_hol.c，生产函数ASan/UBSan直接核手算、临界期限、优先级/速率关系、全部65536编码与短缓冲，实际结果TEST361。论文/教材/协议原文范围见README和source-audit，无新增缺件。继续保持独立工作树，完整作者补丁和示例凭据不Git。
