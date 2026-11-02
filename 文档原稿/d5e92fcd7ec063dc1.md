# CHG-168 TDD二十四项离线收集报告与双向尾部图作者源

日期2026-10-24。新增tdd-confirmation/collect_current.py、report_current.py、plot_current.py和current_analysis_reference.json；在441运行冻结之后添加，仅离线作者源。复用seed collector统计函数（四函数AST字节语义一致），主过程增加D/U/direction、完整gate失败不输出成功子集分位、短/长尾样本边界、原measurement三外部REALTIME区间及同包均值和残差，对MONOTONIC总量另列。报告完整24状态、短双向P99、长两反序块P999及同块差、CPU/粗MAC代理和名义日历界限；不说算法收益/唯一原因/全局最优。两图作者源用NaN表示缺测、不将短P999当可靠尾，CCDF阈值不外推，Arial/fallback明示。未修改运行源、NR/二进制/无线/算法，活动时未运行统计/画图。

## 依据与适用边界 2026-10-20补注

本条2026-10-24新增。current_source_provenance.json的12本地原文与P01 III本地PDF2–3、P17 III/IV-A PDF3、P19本地arxivv1 II PDF2、教材4.3.1 PDF79/13.1.1.2 PDF530；UL/DL层界首选38.300V19.4§4.4.1/§6、38.321V19.4§5.4.1及38.322/323和37.324已读条款。统计/时钟分段为工程测量定义，不能代替独立PHY/空口。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
