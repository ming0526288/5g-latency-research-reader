# TEST-177 正式配置SCS十二条件完整复测

2026-10-22，session30456已结束1；在停止前SCS12全部runner/analyze/QFI 0，完整54000关联/48000统计。TDD22与SCS12共34业务尝试30完整4 K2失败；核心网停止没有新增业务尝试。

|条件|单向P99/ms|
|---|---:|
|mu1-d1u3-dl|1.36556918|
|mu1-d1u3-ul|5.71172298|
|mu1-d2u2-dl|1.21499507|
|mu1-d2u2-ul|5.69249988|
|mu1-d3u1-dl|1.04110807|
|mu1-d3u1-ul|6.37100945|
|mu3-d10u9-dl|0.97002688|
|mu3-d10u9-ul|4.13227192|
|mu3-d5u14-dl|1.10986604|
|mu3-d5u14-ul|4.11906463|
|mu3-d14u5-dl|1.08906231|
|mu3-d14u5-ul|5.72112679|

实际运行命令TEST176的同一完整79入口。实际收集先单--runs-dir short-runs-03、随后加--runs-dir short-runs-04 --partial，两次exit0；具体完整字段README/docs11。实际report.py --matrix .../evidence/short/current_matrix.json --output .../reports --phases tdd scs --replace-active，exit0。后次安全快照含multi首项，未冒充SCS数据；SCS只取phase=scs。

SCS全部4500/UE去500，1200B/2Mbps，实际SIB1 TDA：FR1为1、FR2为13，完整包N3/TUN/QFI、程序/配置SHA、189冻结前后及回收均通过。每条件单轮不证明长期稳定或显著性。无RAN期间并行绘图/渲染。

## 依据与适用边界 2026-10-20补注

本条2026-10-22新增。38.211 V19.5.0 §4.2/4.3.2；38.213 V19.5.0 §11.1/13表13-8/13-12；38.214 V19.5.0表5.1.2.1.1-2；38.331 V19.4.0 §6.3.2；38.104 V20.1.0 §5.3.2及表5.3.5-2；P01 III/IV PDF2–4、P02 II/III PDF2及IV PDF3；教材4.2/4.3.1 PDF77–80、5.4.5 PDF122、6.4.3 PDF211–213。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
