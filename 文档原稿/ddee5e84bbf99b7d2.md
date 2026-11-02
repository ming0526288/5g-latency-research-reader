# CHG-074 旧UPF冷启动下行与显式预检对照

N4进一步按PDI（IE2）展开，实际UL PDR/PDI明确包含QFI9，不能说整个SMF未向UPF传QFI；新会话无QER是事实，但不能仅据此直接判整个配置非法。更正先前“没有下发QFI标记规则”的过宽表述：未发QER，UL检测规则中已有QFI9。对应29.244 V20.1.0 §7.5.2.2的PDI及§7.5.2.5条件C，§8.2.89；N3仍见0。

查公开OAI SPGWU上游源码93df89971f8bce5595489d8a8a02a4c1fd6a17b2 src/spgwu/simpleswitch/pfcp_switch.cpp L976–978和L1044附近：UL转发时从UL PDR取QFI存session，DL从session取。仅作为部署实现假设，上游源码不冒称与本镜像字节对应；须动态对照确认。原始仓库来源Gitee部署目录在Web工具不可访问，未用不可读页面猜源码。公开primary来源：https://github.com/openairinterface/openair-spgwu-tiny/blob/93df89971f8bce5595489d8a8a02a4c1fd6a17b2/src/spgwu/simpleswitch/pfcp_switch.cpp 。

multi-ue/run.py新增显式可选--ul-qfi-preflight，默认关闭，避免改写历史/冷启动对照。开启时在单向UDP测量前每UE通过其TUN发3个ICMP（-c3 -i.2 -W2），核验成功才启动测量；stdout和返回码保留，status/commands登记。ICMP不计入UDP4500/500/4000统计，不用RTT冒充单向。run_qfi_diagnostic.py透传该选项。未改UPF、C头值、订阅或包；此工程预检不是3GPP强制，也不是根治UPF或优化收益，稳态前提须在报告/Word/PPT标红。

若预检后DL仍失败，保留真实失败继续定位；若QFI9和完整UDP恢复，则只证明本部署的状态前提，不保证从未发UL的首个DL可用。已有冷DL失败不删除，不能用预检对照替换成“全部标准一致性通过”。本轮数学仅包关联/边界计数，不新增协议时延常数。

## 依据与适用边界 2026-10-20补注

依据：38.415 V19.1.0 §5.4.2.1、§5.5.2.2、§5.5.3.3；29.244 V20.1.0 §7.5.2.2表7.5.2.2-2、§7.5.2.5表7.5.2.5-1、§8.2.89；24.501 V20.1.0 §9.11.4.12/13；38.331 V19.4.0 §6.3.2 SDAP-Config；37.324 V19.0.0 §5.2.1 NOTE2；P01 III/IV PDF2–4及教材2.3.2 PDF49–55辅助。N3单QoS流C修正、逐包标记/内部关联及显式UL预检；冷DL仍失败，单流保护/ICMP/进程控制均须写工程边界，不宣称全面认证或优化收益。 精确原文定位/版本/已验证边界以记录正文、standards-review/逐项协议映射.md和接收SHA为准；用户指定本地原文，不称官网最高版；未完成不填旧数值。
