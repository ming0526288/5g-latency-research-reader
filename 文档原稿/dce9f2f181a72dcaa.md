# TEST-175 控制方向修正后四项完整回归

记录日期2026-10-22；实际四项开始时间为2026-10-21 UTC09:54:13、09:55:10、09:56:07、09:57:04，均21日北京时间，不能因记录跨日改写历史时间。CHG103。实际运行命令TEST174，session70098最终exit0。

|独立回归条件|完整关联包|统计样本|最差UE P99/ms|
|---|---:|---:|---:|
|120kHz 2:2 DL|4500|4000|0.75858932|
|120kHz 1:3 DL|4500|4000|0.94089442|
|30kHz 1:3 UL|4500|4000|5.51639185|
|120kHz N8 UL 每UE2Mbps|36000|32000|75381.55333375|

4/4完整，共49500关联/44000统计、11流。所有runner/analyze/QFI为0；新PFCP、189文件前后冻结、实际程序/配置SHA、SDAP日志、各完整包与回收均核验。multi实际主线程CPU4/policy2/priority97保持。N8完整有限流P99仍约75秒，不是纯空口、不证明长期承载或优化收益。

实际collect.py --input .../results/common-policy-rerun-01 --plan-dir .../plan-04 --runs-dir .../access-sanity-runs-01 --identity .../ssb_build_identity.json --output .../evidence/access-sanity --cohort sanity，exit0、complete_plan=true。每项实际控制字段与配置SHA、通过的access-controls审计相符：FR2 SSB1/CORESET2且1符号/sib1_tda13 S2/L4；FR1 SSB0/CORESET12且1符号/原sib1_tda1 S2/L10。再次实际收集exit0，另核运行gNB日志SIB1 TDA：FR2为13、FR1为1，确认参数真实生效；安全current_matrix/current_flows/summary及audit SHA保留；无旧/新合池。

四项通过后，2026-10-22正式启动plan-04/short-plan.json→short-runs-03，共79按阶段；同189冻结、--isolate-cases，session30456。随后才启动四长tail-runs-03（尚未启动）。本TEST不能代替正式83或宣称五阶段完成。原SSB前组与修复后但控制冲突组均保留，不改成通过。

## 依据与适用边界 2026-10-20补注

本条2026-10-22记录，实际测试21日。38.213 V19.5.0 §4.1/11.1/13表13-8/13-12，38.214 V19.5.0 §5.1.2.1.1表5.1.2.1.1-2行14，38.331 V19.4.0 §6.3.2 bitmap；P01 III/IV PDF2–4、P17 III/IV PDF3–4、教材5.4.5 PDF122。n0/方向及局限CHG103，样本/CPU/负载/超时是工程设置，非标准强制值。
