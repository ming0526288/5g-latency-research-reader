# CHG-135 修正版包级先导准备与失败证据保留

2026-10-23，CHG134两项修正完成；新增prepare_corrective.py、source_provenance_v2.json、build_identity_v2和初试字段审计安全表；analyze增加原BSR长度错误拒绝、逐包CRC失败/HARQ重传/早于入队的准备授权计数，仍不把grant前置当负排队，不改成功门槛。旧source_provenance/278清单/初试失败保持，不冒称当前源不变。

修正后PHY日志读frame_parms->numerology_index，原DCI未初始化字段不再读取；完整ninja6步骤exit0。analyze的if筛选已修，私人诊断对旧4500包能闭合其余图边，但故意忽略旧坏PHY mu，结果明确DIAGNOSTIC_ONLY_INVALID_PHY_MU，不是正式观察PASS，未覆盖旧正式failure或新RAN结果。所有原始数据、旧P99与旧W/S/R保持，诊断CSV有独立diagnostic前缀，只库外辅助源/结果。

纠正先导pilot-plan-02新294文件，SH A按predeclaration记录；case n1-ul-total4-service-on-pilot-v2，除新观察程序/关联器身份和输出目录外，业务/NR/CPU/超时与初试相同。最多一次纠正先导，不放宽门槛/删错误或自动无限重试。准备script核旧278仅三项改变（UE程序/PHY C/analyze.py）、10协议CRC/XML与选读源，后续实际启动/结果另TEST。原始仓库与Word/PPT未改。

## 依据与适用边界 2026-10-20补注

本条2026-10-23新增。38.211 V19.5.0§4.3.2/表4.3.2-1、38.321 V19.4.0§5.4.1/5.4.2/5.4.3、38.322 V19.3.0§5.2.3.1/6.2.2.4/6.2.3.3至5；ul-service/source_provenance_v2.json记录原文/读段/新旧源身份，P01 III/IV PDF2–4/P30v3 PDF4–6/22–23/P31v3 PDF3/9–11及教材13.1.1.2 PDF530–532为已声明参考范围。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
