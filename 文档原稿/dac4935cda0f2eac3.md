# TEST-201 受控RU运行一致性数学解释科学图与交付核验

2026-10-22，全部RAN清理后执行诊断README所列audit_runtime、report（最终带--interpretation）、plot与verify_delivery实际命令，均exit0。report先生成全数据稿，再加入按实际数据审核结论、澄清测点主体范围及成本推导，最终重写同一当前报告，不只追加冲突说明。十个gNB运行日志均HARQ feedback enabled、SIB1 TDA13；同配置SHA及除RU核心外同gnb命令；QFI9/时限/模块/实际mask通过。零调度重传只覆盖实际ON记录窗，不直接推为完整PHY无差错。

两张科学图实际生成并逐张查看。图2首稿视觉标题/图例相互覆盖，未验收；保存私有首稿后改三面板、底部图例、共享y轴再生成通过，图1 PNG字节完全相同。最终ru_controls 1876×697，rf_read_phases 2640×684；全部可见SVG text/tspan Arial声明核通过，PNG为宿主缺Arial后的Liberation Sans回退。没有独立SVG栅格化或原生Office认证，本轮未改Word/PPT。

verify_delivery最终PASS：10条件、66逐UE行、297000/264000、5个ON、全部程序/共享库身份、人口代数和/样本单位/阶段份额和/TBS归一化恒等式、人工结论与本组SHA绑定、图像文件及字体/链接、明显敏感标签扫描。ON/OFF和反向块逐项保留；2块不是总体置信。手工数值复核将“通常毫秒以内”改为实测N8单调用最大值1.01–3.10ms，避免凭均值臆测分布；预算说明明确N8，避免与N1混用。

观测影响已明示：RU9 ON P99较同块OFF高约1.92/2.03秒，RU6 ON较OFF低，不能将差异全部解释为纯观测开销或称零扰动。C成本/帧推进只定位当前主要机制；残余约200ms未解，CPU4竞争与NR资源仍需独立干预/逐包关联。

最终交付校验JSON内容：
```json
{
  "result": "PASS",
  "conditions": 10,
  "flows": 66,
  "matched": 297000,
  "measured": 264000,
  "on_conditions": 5,
  "matrix_sha256": "aaa3220a61d9720a566122cec8ddd04f5d0ca500278b9b6775544289925361ff",
  "summary_sha256": "f12c4111c7c342ad0815fa9b51f4361607fc34929a451d6e577a6a938d41cd38",
  "report_sha256": "043e8c75f06a106b232f79d220aed426607bce0896c370e695d51b4c878cc9a7",
  "interpretation_sha256": "25e06630fa07ccbfd5889934726c336139ccc9f0b519ed82c3c99626e9f396a1",
  "runtime_audit_sha256": "aee4e283a0c994fa4d65e678b1be04000ddd3e0725afb298e0ebca4f23663109",
  "figures_pixels": {
    "ru_controls": [
      1876,
      697
    ],
    "rf_read_phases": [
      2640,
      684
    ]
  },
  "scope": "Identity, all-flow numbers, aggregate algebra and artifact checks; not unique universal causality, pure-air or steady-state proof."
}
```

加入本条后再实际执行source_audit/validate_reference_audit.py和git暂存diff检查；输出与同步以实际工具结果为准，不预写push成功。所有所需原文可读，没有新增协议下载/缺件；原始证据与失败均本地保留。

## 依据与适用边界 2026-10-20补注

本条2026-10-22新增。首选38.300 V19.4.0 §10.2/10.3，38.321 V19.4.0 §5.4.1/5.4.2.1/5.4.2.2/5.4.5/6.1.3.1，38.214 V19.5.0 §6.1.2.1/6.1.4.1，38.211 V19.5.0 §4.3.2；原文SHA/段落causal-diagnosis/source_provenance.json。P01 III/IV本地PDF2–4、P24 VI PDF7–8、教材13.1.1.2 PDF530–532辅助；CPU位置、C时钟、负载和统计是工程研究方法，非协议指定时延。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
