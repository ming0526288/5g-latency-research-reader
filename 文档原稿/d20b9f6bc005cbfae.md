# TEST-178 PFCP门槛停止及同程序接续第一项

2026-10-22。session30456 root exit1，最后已完成SCS mu3-d14u5-ul；下一multi n1-ul-fixed_per_ue仅恢复核心网并轮询，assert New PFCP association not confirmed; no RAN launch。association_readiness.json：SMF started01:30:25.618Z，UPF01:30:27.382Z，new_smf_request_observed=false、new_upf_response_observed=true、poll_attempts40。experiment.json为空，无RAN/status/UDP/capture文件，无该项单向时延。

实际sudo只读诊断：docker inspect初次假定.State.Health.Status字段存在，两个模板各返回错误（容器未定义Health）；没有当成容器故障。docker logs --since各StartedAt保留到该预检目录；过滤关联/心跳信息。UPF01:30:27.718收到Response，SMF反复Failed to receive PFCP Association Response，后来心跳双向；根因未唯一定位。/proc只读核两类RAN均无。未改核心网程序或超时，未虚构抓包。

实际接续：sudo -n /usr/bin/python3 -B research/latency-analysis/standards-review/run_all_sdap.py --plan research/latency-analysis/results/common-policy-rerun-01/plan-04/short-plan.json --output research/latency-analysis/results/common-policy-rerun-01/short-runs-04 --phases multi order multi_tdd layered --isolate-cases --frozen-inputs research/latency-analysis/results/common-policy-rerun-01/plan-04/frozen-inputs.json。session84312当前运行，首n1-ul-fixed_per_ue完整4500关联/4000统计，runner/analyze/QFI0，前后189冻结及实际控制TDA通过，不能记整批exit0。

实际collect.py显式plan-04、ssb_build_identity，重复--runs-dir分别03/04，--cohort short --partial，exit0。已收快照TDD22/18/4、SCS12/12/0、multi1/1/0，共139500关联/124000统计31流；独立environment_preflight_failures1，business_attempts0。原始失败未覆盖，不改变已有业务分布。

## 依据与适用边界 2026-10-20补注

本条2026-10-22新增。29.244 V20.1.0 §6.2.6.3给PFCP关联维护语义；日志字符串、40次0.5秒轮询和容器恢复属于工程检查，协议未指定这些判据；P01 III/IV PDF2–4及教材2.3.2 PDF49–55仅支持完整路径与测量边界。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
