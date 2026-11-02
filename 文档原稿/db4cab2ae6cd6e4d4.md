# TEST-150 接续材料数值来源与最终接续检查

2026-10-21，CHG091。新建analysis-documents/records/source_snapshot_v11.json，保留历史report_replacement原文件/旧记录不变，新增本次22篇现行报告SHA（原19篇与3篇接续）。原19备份字节仍核对；不是重新填旧测试哈希冒称旧材料再次通过。

实际命令为缓存Python执行artifacts/validate_current.py --with-followup，word指向原路径当前27页DOCX，ppt指向followup-20261021/output/五阶段时延分析与接续实验_20261021_Arial.pptx，matrix/tail为原冻结矩阵，replacement指向新私有source_snapshot_v11.json，research为research/latency-analysis，output为analysis-documents/records/artifact_validation_v11.json。退出0：28表/11图/20原生公式、32页、原TDD及10个长流行、15区间舍入和、21方向连接端点及接续14项P99与原安全数据一致；22篇现行报告与历史备份SHA通过。

Word最终SHA6bc2c4d28d3afd9bc20b84933237381932a0d724628945d3abe76d88e8093ff6；PPT最终SHA55a16b39a97534fa16286ce08cf3c10d4736d9f8a2c033b3e55c470df5a0df48。完整像素差异清单在本地followup_visual_diff_v11.json，变化页逐张核，未变化页与先前已核页面逐像素一致。新渲染共27+32页，不以接触表替代逐页验证。

sudo只读最后核查14项原始status的44个自有namespace，实际ip netns list中残留0；两种RAN pgrep均退出1，无活动RAN。没有停止其他用户进程/网络。当前所需协议原文可读，未新增下载；三份AGENTS未改，来源索引/28论文/教材SHA检查以最后终端通过为准。

C同步修复、负载对照、主线程ABBA已分别提交并推送53558b7455、bffc0fcb55、0a62721786。本文及材料代码将白名单另提交，最终Git状态以git log/status/远端核验为准；不提交Word/PPT、协议原文、原始日志/pcap、凭据或二进制，不混入旧scs2未跟踪目录。

下一步仍为增加内部MAC/RLC出队、授权/DCI、TB/HARQ及RFsim等待关联，解释上行轮间波动；5/10ms配置、60kHz全链、长尾重复尚未补齐。冷DL仍依赖显式UL预检，需匹配UPF源码与完整初始化核查，不能冒称根治。当前短4000包/UE不支持可靠P99.9，未实施NR调度优化。

## 依据与适用边界 2026-10-20补注

本条2026-10-21新增。包结构/数值显示/来源SHA/Git/进程回收为工程核验，3GPP和新数学推导不适用；通信条款与有限人口公式的独立推导、实际测试及局限见CHG088至090，材料校验不能替代NR一致性、平稳性或真实射频认证。
