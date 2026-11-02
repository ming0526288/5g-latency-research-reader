# TEST-125 分批汇总与二项次序公式核验

2026-10-21。实际运行：

```bash
python3 research/latency-analysis/standards-review/collect_current.py --plan research/latency-analysis/results/qfi-review-02/steady-plan-01/plan.json --root research/latency-analysis/results/qfi-review-02/steady-reruns-02 --root research/latency-analysis/results/qfi-review-02/steady-reruns-03 --output research/latency-analysis/results/qfi-review-02/partial-collection-02 --allow-partial
```

退出0。此固定checkpoint为TDD22尝试/18完整/4失败、SCS12/12完整、多UE7/7完整，其他阶段未尝试，总180000完整关联包。输出complete_plan=false；不能宣称全部完成。每次4500/4000、QFI/回收及配置检查均由汇总器实际断言；4失败均无业务，5ms计算Msg3 K2=34、10ms=74超0..32。原phase退出状态保留，不把两根目录混为同次根进程成功。

尾部计算先调用shell默认python3失败，退出1、ModuleNotFoundError:numpy；尚未读取包或生成统计。未安装依赖，改用现有RAN分析器一直使用的/usr/bin/python3后成功。这是Python环境选择错误，不是协议/业务失败。

实际/usr/bin/python3内联导入tail/analyze.py iid_ranks()，n=5/20/100、p=.5/.99/.999共9组合，与直接math.comb二项概率求和差<1e−10且覆盖≥.95；返回0。预声明n100000时P99秩界98938/99062、覆盖.9512338613；P99.9秩界99880/99920、覆盖.9547890568。没有将这些秩界伪装成已观测时延。相关/非平稳条件下仅IID参考。

本轮已实际阅读P19本地全文§III/IV及表I/图2，采用CCDF与负载观察视角，不移植其CG、功控、多小区干扰或1ms目标；当前1/5/10ms为项目示例。原文协议映射沿用CHG-079，本次未增加必要协议缺件。长时尾部实验未运行，Word/PPT仍待重写；当前自有RAN仅session34671中的原计划，未并发另启。

## 依据与适用边界 2026-10-20补注

依据：M01项目统计推导及E01/E02/E03；P19 §IV PDF4–5、P01 §III/IV PDF2–4；通信层与字段的原文条款见记录正文和逐项协议映射。样本数、次序统计、分窗和运行期限为研究设计，不是3GPP强制；IID参考不适用于依赖或漂移队列，失败不合池、不伪造成功。 精确原文定位/版本/已验证边界以记录正文、standards-review/逐项协议映射.md和接收SHA为准；用户指定本地原文，不称官网最高版；未完成不填旧数值。
