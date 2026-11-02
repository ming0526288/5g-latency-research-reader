# CHG-106 核心网预检停止保留与同冻结计划接续收集

2026-10-22，session30456在34业务条件后、multi n1-ul-fixed_per_ue之前结束1。核心网关联门槛未满足，不修改冻结运行器/时限/3GPP字段，不把该次视为无线业务失败。原short-runs-03保留原貌；用同plan-04和同189文件，从multi/order/multi_tdd/layered继续到新short-runs-04，session84312。不是重跑已完成的34项，也不是挑成功样本。先只读确认无活动gNB/UE，未动认证或订阅库。

collect.py --runs-dir变为可重复参数，明确声明两个原始输出根；按每个实际checkpoint反查所属phases.json，仍要求对应外层exit0及前后冻结相同。现有collect_current拒绝任何重复业务key，不能静默覆盖初次失败/挑最好。外层exit非0且experiment严格为空、缺PFCP门槛的环境停止，独立导出environment_preflight_failures和文件SHA、实际布尔值，计business_attempts0，不填业务时延。若非空业务/未知停止，断言拒绝合并；保持所有原始记录。

直接证据：SMF请求标志false，UPF响应标志true，轮询40；后续有双方心跳。只确定规定的新进程日志对未完整满足，不能唯一证明PFCP传输未建立。相应SMF不断提示未收到Response，但与UPF已收Response并存；更深初始化/报文根因未定，不以推测改核心网。日志私有，Git只安全布尔/哈希摘要。

新组用同程序与原超时恢复后首项完整，TEST178。完整命令更新README/docs11/START，长组仍尚未启动。

## 依据与适用边界 2026-10-20补注

本条2026-10-22新增。29.244 V20.1.0 §6.2.6.3给PFCP关联维护语义；日志字符串、40次0.5秒轮询和容器恢复属于工程检查，协议未指定这些判据；P01 III/IV PDF2–4及教材2.3.2 PDF49–55仅支持完整路径与测量边界。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
