# CHG-286 SR周期协议资源核验与独立控制分支

2026-10-28，用户“ok可以继续下一步”，执行docs16的标准SR周期机制对照。新工作树oi-wireless-ran-sr-period-mechanism、分支latency-sr-period-mechanism，从4ca5b42a67创建；复制已冻结的4个只读观测C及ul_state_trace.h作为基础，保留原观察/算法源、结果和失败。Git继续取消提交/推送，原始RAN/核心保持。

开始核25本地DOCX SHA/CRC/XML及P24/教材SHA可读，递归协议目录56原件/原ZIP；本步无必要缺件。实际重读38.331 V19.4.0 §6.3.2 SchedulingRequestResourceConfig（递归39057起）sl10/20/40及各offset范围、SchedulingRequestConfig的禁止计时；38.213 V19.5.0 §9.2.4含OMML机会公式、§9.2.5复用背景及§11.1（4619起）TDD符号；38.321 V19.4.0 §5.4.4 pending/机会/禁止/取消，§5.4.5 BSR背景；38.211 V19.5.0 §4.3.1/4.3.2表4.3.2-1沿本地已核帧/槽定义。版本为已授权本地封面版，不冒称官网最高。

实际读本地AUGUSTE arXiv:2606.03664v1/2026-06-02，PDF1–2的SR等待/资源开销动机；本地6页，不冒称最新版或复现该算法。其PDF2“best case至少完整SR周期”不能作为本实验数学下界，实际机会残余依到达相位为0到一个周期；论文中的10–40ms/RTT降幅不替代本机120kHz的5ms/UL指标。P01 Dissecting本地6页IFIP Networking2025仅核封面/分层动机，不假称有SR周期实测公式；指定教材§13.1.1.4/5 PDF537–539重读SR/BSR。资料身份/检索均放analysis-source-audit/sr-period-mechanism-20261028，协议目录不添辅助文件。

代码核查：nr_rrc_config.c::set_SR_periodandoffset在mu3下选择sl40；共享find_period_offset_SR及UE/gNB机会函数支持10/20/40，非协议要求固定40。原PUCCH0资源PRB=8+uid、symbol13、1符号；三UE为不同PRB，CSI PUCCH2为PRB0–7/symbol13；HARQ可在原同资源路径复用，保持原实现并实测检查冲突/丢失。

原TDD每5槽为D3/S/U1，S最后4符号UL（10–13）。P∈{10,20,40}都为5的倍数，offset3使全部SR机会k=3+mP满足k mod5=3，symbol13在UL区；这只是所选配置下的可行性推理，不声称标准强制这些组合或完整一致性认证。缩周期增加机会/监听次数，需要同时报告正SR、负/空机会、资源/处理与时延代价。

下一修改只允许gNB RRC构造以显式研究开关选原sl10/20/40，默认沿旧逻辑；仅限本已核120kHz/原TDD工作点，非法值/其他配置拒绝。单一新二进制PF、3种子×3周期、反序接入，周期顺序轮换；原QoS/负载/包长/观测/CPU/门禁不改。不实现预测授权、自适应请求或新算法；先验证机制。每步TEST425起记录实际命令/结果，失败停止保留。

实际新增nr_rrc_config.c::set_SR_periodandoffset的OAI_RESEARCH_SR_PERIOD_SLOTS环境开关，未设置/空值走原代码；仅10/20/40且原mu3/P0.625ms/D3/S6D4F4U/U1/无pattern2可用，保留offset3、resource/ID，日志[SR-PERIOD]显示实际选择。已用真实ASN.1构造/UPER核显式40与旧default同编码、20/10可回环；没有绕过UE RRC解析。
