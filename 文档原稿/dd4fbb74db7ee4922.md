# TEST-126 七十九条件终检与追加设计核验

原续跑命令见TEST-122。session34671已正常退出0，但steady-reruns-02早先根退出1仍保留。联合唯一计划79项：TDD22/18完整/4失败；SCS12/12；多UE15/15；顺序6/6；多UE×TDD12/6完整/6失败；分层12/12。总69完整、10失败、666000完整四边界和QFI包、592000预热后样本。8个ON条件99000完整包/1386000事件，逐包求和残差0ns。不能说单根进程79项全成功。

实际汇总命令返回0：

```bash
/usr/bin/python3 research/latency-analysis/standards-review/collect_current.py --plan research/latency-analysis/results/qfi-review-02/steady-plan-01/plan.json --root research/latency-analysis/results/qfi-review-02/steady-reruns-02 --root research/latency-analysis/results/qfi-review-02/steady-reruns-03 --output research/latency-analysis/standards-review/evidence/current --packet-diagnostics
```

pgrep -af 'nr-(ue)?softmodem'退出1且无输出，已无gNB/UE。各成功与失败status均确认自有进程回收，namespace删除0；不是靠隐藏旧进程换“成功”。协议目录核验validate_protocol_storage.py返回0：21原ZIP、31原DOCX及2配套ZIP字节未变，三份规则相同。

失败：5/10ms双向4项，RF前生成Msg3 K2=34/74越0..32，无UE/业务/抓包。多UE交叉5项在每UE25秒等TUN超时，无业务/抓包；均有失败UE PHY同步标志，未有该UE RRC_CONNECTED/TUN标志，不能据此给唯一根因。n4-dl-d2u2四TUN先后就绪，receiver0启动bind返回Errno99，N3抓包已开、发送未开始，无时延样本；绑定地址当时不可用，地址为何不可用未定位。原日志仅按脱敏标志只读检查，未公开完整日志。后续6追加最多一次设计已写在CHG-080/evidence/retry_design.json，未预写成功。

新增CLI语法检查第一次返回1：rerun_sdap.py新QFI调用块多一空格导致IndentationError，未启动RAN；已纠正。随后/usr/bin/python3 AST解析7脚本及multi-ue/run.py、run_all_sdap.py、collect_current.py --help均0。默认110/120秒不变。计划生成tail/prepare.py返回0：4长条件，精确种子时长N1=482.625796秒，N4最大484.014333秒；业务/接收期限595/613和597/639秒。追加计划生成0：6条件，每项一次，不含K2失败4项。两计划原文件只本地，安全设计含SHA已存证。

文档预检查另有一次默认python3读取Word的lxml导入失败1，无写Word；改用匹配缓存bundled Python后只读成功，确认原A4。后续文档工作必须继续用该bundled运行时，不能用默认Python。本记录不宣称Word/PPT已经重写或渲染。来源与工程/统计限制见CHG-080，原79短样本不能代替正式长尾。

## 依据与适用边界 2026-10-20补注

依据：M01项目统计推导及E01/E02/E03；P19 §IV PDF4–5、P01 §III/IV PDF2–4；通信层与字段的原文条款见记录正文和逐项协议映射。样本数、次序统计、分窗和运行期限为研究设计，不是3GPP强制；IID参考不适用于依赖或漂移队列，失败不合池、不伪造成功。 精确原文定位/版本/已验证边界以记录正文、standards-review/逐项协议映射.md和接收SHA为准；用户指定本地原文，不称官网最高版；未完成不填旧数值。
