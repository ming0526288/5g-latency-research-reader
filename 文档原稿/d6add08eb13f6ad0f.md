# TEST-232 修正基线七项通过后PFCP预检停止及定位

2026-10-23，session20634最终exit1。实际通过7项（不是6项）：首块6项与次块N8 ON都完整全gate通过；第8项N8 OFF核心网恢复预检停止，new_smf_request_observed=false/new_upf_response_observed=true、40次轮询，experiment.json空，无RAN/业务/pcap/包时延。后4项未尝试。7项34流153000完整关联/136000统计，具体execution SHA及安全证据pfcp-preflight-stop.json；328前后通过，sudo核无RAN/netns。上一进度口头把失败点说成第二组N8 ON，已据完整日志纠正为其后一项N8 OFF。

实际执行只读/tmp/service_baseline_pfcp_audit.py（sudo），分别收集SMF/UPF两个流。stderr均空，排除该次是stdout漏读stderr。SMF当前日志最早06:40:39.261，UPF响应06:40:38.982；docker inspect SMF为json-file/max-size1m。当前SMF日志缺启动窗口，轮转为有证据候选；尚未直接核PFCP包事务，不断言关联一定失败或一定成功，也不放宽原硬gate。私有原日志/完整audit在analysis-source-audit/service-baseline-pfcp-20261023-01不Git。

本地递归找到29.244-k10.docx，封面TS29.244V20.1.0(2026-09)、CRC/XML可读，SHA2f0fe3a9cf744ffb5a7f3e170f29238ddbca9a2ea5419da815def531db163ed1；已读§6.2.6.1/.2/.3与§7.4.4.2表的Cause定义。不是缺协议，无下载。协议允许UP发起但不强制该实现的两个日志字符串；日志检查仅本项目工程前提，不冒充完整PFCP成功Cause/事务验证。

原始失败目录保留，只授权一次有明确记录的该业务前环境重试及原顺序后缀，重试仍失败即停止；不挑选业务快轮、不重做已通过7项。需新严格接续控制器/自身冻结和全尝试收集账本，随后CHG/TEST登记。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。TS29.244 V20.1.0 §6.2.6.1/.2/.3，§7.4.4.2 Table7.4.4.2-1，Word递归3587–3642/5467–5495；不改PFCP/NR；CHG143持久日志与既有328身份；P01 III/IV PDF2–4完整关联/不删失败，教材13.1.1.2 PDF530–532不用于规定核心网重启。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
