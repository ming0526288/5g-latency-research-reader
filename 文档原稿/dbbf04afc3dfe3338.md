# CHG-307 QUEST五模式同程序先导与正式矩阵冻结方法

独立quest-closure目录从sr-per-ue方法复制，prepare改为新3条件先导/正式30，原研究脚本和冻结输入不动。run改独立qclose副本/209网段；固定SR40、显式去掉QoS-SR policy；仍每条件真实核心/gNB/三UE/UL/路径/QFI/控制面/完整字节/状态关联门禁，保留原期限和首失败停止。mode映射显式0/3/4/5/6；analyze_decisions新增mode6重算但真实HOL上报/缓存/匹配照验，要求每模式业务中正HOL报告存在。verify_case和study_gate核实际模式与UE标准SR40字段，没有把UE序号当QoS或把关闭报告当消融。

具体代码/配置/公式/依据与全部命令见quest-closure/README与docs18、ALG003。依据TS38.300 V19.4.0 §10.1/10.3，TS38.321 V19.4.0 §5.4.1/4/5，TS38.213 V19.5.0 §9.2.4、TS38.214 V19.5.0 §6.1.2.1，38.331 V19.4.0 §6.3.2相关SR IE，23.501 V20.3.0 Table5.7.4-1；P24 §V-B/VI-C本地PDF7–9、教材§13.1.1.2/4/5 PDF530–532/537–539。原文身份31件TEST449，旧SR40构造TEST439等。具体网络/次序/重复/包数为工程实验控制，不是3GPP强制方案。

主对照PF/QUEST/EDF/M-LWDF/QUEST-noHOL，全保持真实HOL报告、实际69/9/9、同ELF和相同SR/TDD/MCS/业务/CPU。三seed两接入反序模式顺序镜像轮转，非完美位置平衡。优先用旧数据授权链定位（CHG306/TEST450），不是先换算法盲试；未实际运行的实验不写收益。环境只读检查已pass4原核心/0RAN/0netns；准备/先导实际结果另TEST。Git沿此前取消，Office/原核心/原RAN保持。
