# C 代码、配置、模型和脚本分别改了什么

本文件回答此前“原代码是 C，为什么看到很多 Python”的疑问。真实 OAI 协议栈仍由 C/C++ 运行；Python 分别承担原函数适配、实验准备/进程控制、抓包与 trace 关联、数学/统计、报告生成。不能把 Python 模型说成完整 OAI 业务，也不能把只写 Python 误说成从未改过 C。

以下是历史说明及 Git 差异梳理，不是本轮新修改通信代码或进行标准认证。精确提交/每次改动文件见 04，原条款/论文/教材依据在对应 CHG 和 docs/10。

## 一、真实通信功能或稳定性修正

|修改|真实位置与前后行为|原因及效果|验证与边界|
|---|---|---|---|
|N3 QFI 取控制面配置|`nr_pdcp/cucp_cuup_handler.c::e1_bearer_context_setup`：写死 QFI0 → 使用已配置 QoS 流 QFI，检查 legacy 单流/范围|纠正 N3 与控制面/N4 不一致；不是硬写实验值 9|CHG-075；TEST-119/120 编译、双向与 N3 字段；多 QoS 流限制是实现边界，不是标准禁止|
|SearchSpace 发布/同步|`NR_MAC_UE/config_ue.c` 及 UE 接口：新对象初始化后发布，RRC 更新与正常读者使用既有 MAC 接口锁|防止读到监测配置尚未完整的中间态，针对真实空字段崩溃线索|CHG-088；TEST-137—140 生产函数 C harness、内存检查、全构建和六业务；不全面认证其他同步路径|
|主线程核心可控|`executables/nr-uesoftmodem.h/.c`、`nr-ue.c::init_NR_UE_threads`：固定 core4 → CLI 可选，默认4保留|-1 继承亲和性；使同核/分核对照真正可控，不只依赖初始 taskset|CHG-090；TEST-145—150，运行前后实际 mask/policy/priority 核对；Linux 位置是工程参数|
|首 UE 调度资格/MCS 位置例外移除|`NR_MAC_gNB/gNB_scheduler_ulsch.c::pf_ul`：移除 `cnt==1` 强制资格与固定上限覆盖，所有 UE 用共同现有规则|建立共同资格/上限基准，避免列表位置覆盖配置上限|CHG-095/096；TEST-158 起生产 C、边界、全构建、六业务；未另写 PF/RR 优化，主动授权并非自动违规|
|FR2 SSB 索引幂等构造|`NR_MAC_UE/nr_ue_procedures.c::nr_ue_decode_mib`：对共享值重复 `+=` 高位 → 取低三位，在局部重新按位组合后赋值|修复重复解 MIB 可从合法33累加到65的问题，保留索引校验|CHG-101；真实旧反例、FR2/FR1 枚举、内存检查、全构建及 N1/N8 回归；不是取模或强塞固定索引|
|短 MAC SDU 子头/预算|新 `NR_MAC_COMMON/nr_mac_sdu.h` 与 `NR_MAC_UE/nr_ue_scheduler.c::fill_mac_sdu`：按长度选择 F/L、实际头长和安全剩余预算/搬移|纠正规范问题和字节核算前提；在独立修正 worktree 保留旧程序身份|CHG-213/214/215；TEST-332/333/339/340，长度边界/独立字节解码/全构建/新六业务；不改 PF/HARQ/MCS/TDD/CPU|

最初模型阶段并没有上述 C 改动；后续问题定位需要真实探针/纠错时才陆续实施。也不能把不同 C 版本测到的差值都归因某一次算法。

## 二、真实 C 观察探针：记录发生了什么，不等于改调度

|观察层次|新增头文件与 C 落点|能看到什么|不能自动得出什么|
|---|---|---|---|
|内部层界/软件队列|`common/utils/layer_trace.h`；SDAP、PDCP API/队列、RLC API|同包处理入口/队列/交付和完整 PDU 指纹；14 内部事件、15 区间历史定义|不能把 RLC 跨端混合段拆成纯空口/HARQ/重组各自固定值|
|RLC 初传分段|`common/utils/rlc_tx_trace.h`；`nr_rlc_entity_am.c` 初传/重传生成点|完整 SDU 到 SN/SO/长度/首尾和请求预算，首次/末次交 MAC 时刻|请求预算不等于完整 TB 字节数，W 不能全称 CPU，RLC 重传不等于 HARQ|
|RFsim 执行与调度/BSR|`common/utils/ran_diagnosis.h`；`radio/rfsimulator/simulator.c`、gNB scheduler|采样等待/合成 wall/线程 CPU、时间桶、只读 BSR/调度统计|不是精确 UE 缓冲区，不证明 UE 收到每个 grant，不按推进比校正 UDP|
|包—段—MAC PDU/TB—PHY—gNB 授权/CRC 图|`common/utils/ul_service_trace.h`；UE scheduler、RLC、PHY 编码、gNB scheduler/接口等|父子 ID、双指纹、尝试键、多对多初传边和实际服务切点|首个实际使用的 grant 不一定是首个可用 grant；观察未检出某事件不是标准全面排除|

共同要求是默认 OFF、独立进程/文件、有界记录、溢出可见、完整性/时序/唯一关联检查、原程序与 OFF/ON 对照。OFF 也可能有额外分支/一次性环境检查，不能无测试宣称严格零开销。长流预算不够时关闭探针并声明无法分层，不能截断后继续报完整图。

两次观察本身的实质纠错也应算进工程版本：

1. **PHY μ 观察来源错误。** CHG-134 改读实际 `frame_parms->numerology_index`，不改变工作 numerology；同时修离线候选条件错误，旧业务成功/新图失败分开。旧 trace 的无效 μ 不被强行标成有效。
2. **PDCP 观察容量不足。** CHG-140 发现同一个 producer 每包四事件，N8×4,500 的基础事件量超过旧 131,072。改为该 TU 的 262,144，其他 producer/记录格式/严格 dropped0 不变；重新构建、冻结和全组重测，旧溢出记录无法恢复。

对应原记录范围：CHG-065、092、122、132—141；测试范围见 03 和全量 TEST 索引。

## 三、与原始基线相比，当前修正分支改动的生产源码/头文件

下列 22 个路径来自原始基线到冻结修正分支的实际 Git 差异。它们是累计净变化，不表示每个文件只改过一次；逐次提交查 04。原研究树缺少最后的 MAC helper/预算纠正，不能拿原研究树的 ELF 冒充修正分支程序。

|路径|累计用途|
|---|---|
|`common/utils/layer_trace.h`|内部层界 mmap 记录与按 TU 容量支持|
|`common/utils/ran_diagnosis.h`|RFsim 执行/调度诊断记录|
|`common/utils/rlc_tx_trace.h`|RLC 分段/初传/重传观测|
|`common/utils/ul_service_trace.h`|包级完整服务图 sidecar|
|`executables/nr-ue.c`|软件 UE 主线程位置使用参数|
|`executables/nr-uesoftmodem.c`|CLI 参数定义|
|`executables/nr-uesoftmodem.h`|工程参数字段/默认行为|
|`openair1/PHY/NR_UE_TRANSPORT/nr_ulsch_ue.c`|实际 PHY 编码/μ 等服务图观测|
|`openair2/LAYER2/NR_MAC_COMMON/nr_mac_sdu.h`|短/长 MAC SDU 子头和安全预算 helper|
|`openair2/LAYER2/NR_MAC_UE/config_ue.c`|搜索空间发布/同步修复|
|`openair2/LAYER2/NR_MAC_UE/nr_ue_procedures.c`|SSB 组合、历史诊断及 DCI 观察|
|`openair2/LAYER2/NR_MAC_UE/nr_ue_scheduler.c`|MAC PDU/TB 观察与最近短头/预算修正|
|`openair2/LAYER2/NR_MAC_gNB/gNB_scheduler_ulsch.c`|共同资格/MCS、BSR/grant 观察|
|`openair2/LAYER2/nr_pdcp/cucp_cuup_handler.c`|N3 控制面 QFI 修正|
|`openair2/LAYER2/nr_pdcp/nr_pdcp_oai_api.c`|PDCP 处理/软件队列边界、该 producer 容量|
|`openair2/LAYER2/nr_rlc/nr_rlc_entity_am.c`|RLC 初传/重传/父子字节边|
|`openair2/LAYER2/nr_rlc/nr_rlc_oai_api.c`|RLC 接纳和跨端交付边界|
|`openair2/NR_PHY_INTERFACE/NR_IF_Module.c`|gNB NFAPI/CRC/服务图回调观测|
|`openair2/NR_UE_PHY_INTERFACE/NR_IF_Module.h`|UE 接口同步保护相关声明|
|`openair2/SDAP/nr_sdap/nr_sdap.c`|发送 SDAP 入口观察|
|`openair2/SDAP/nr_sdap/nr_sdap_entity.c`|接收向上交付观察|
|`radio/rfsimulator/simulator.c`|RFsim 等待/合成执行阶段只读观察|

## 四、配置修改：多数是生成研究副本，没有覆盖原始启动配置

|配置/运行前提|如何调整、为什么|怎样核验与不能省略的边界|
|---|---|---|
|TDD D/U 和周期|从原模板生成候选，保留来源/override/哈希；D/U 为完整槽，S/边界符号单列|字段算术、可达授权/反馈、PRACH/SSB/控制及实际业务分别核，不能只靠方向表宣称合法可部署|
|SCS 无线参数|30/120 用本软件可运行模板，UE 的 band/frequency/PRB/μ/SSB 参数化|频段、grid、方向份额等伴随变化须披露；60/240 模型不宣称完整业务支持|
|PRACH 对照|在周期失败里依据实际映射与方向做副本对照，不根据时延结果挑索引|接入通过不证明完整标准认证，一次失败也不能说标准禁此配比|
|SDAP|生成副本启用现有 `enable_sdap=1`|默认 DRB UL 头前提纠正；DL 头联动属于本 fork 选择，不硬改旧模型假设|
|SSB/Type0/SIB1 方向|保留修复后 C，另改副本的 SSB/初始控制设置|具体单 SSB1、默认 A 行14是工程选择，需显示与方向的实际检查，不能写标准唯一方案|
|MCS|受控上限、旧外部状态上限和每 TB 实际值区别记录|不能说上限9等于每 TB 固定9，也不能按摄像头故事改视频内容|
|5GC/网络|复用部署，生成 N2/N3 地址副本、namespace/veth/TUN/UPF 路由，预检 PFCP/QFI|不修改密钥/订阅来强过；维护/冷状态前提单列，不把 AMF/DB 重启当无线优化|
|CPU/RU|真实 C main-core 参数或已有 RU core 字段，运行前后实际 mask/模块身份检查|初始 mask 不代表最终所有线程；性能/能效核不等同，CPU位置不是 NR 标准参数|
|期限/负载/样本|每组事前声明短/长目标、接收和 trace 预算|失败后不扩大时限强过、不丢慢包，未测项不填0|

配置本身、UE 鉴权、完整日志和原始捕获按既有规则留本地；可提交安全字段/哈希/脚本。原始 `oi-wireless-ran` 路径没有被用于这些修改。

## 五、Python/脚本承担的工作及其测试

|类别|主要目录/例子|做什么|怎样证明没有把脚本结果冒充无线实测|
|---|---|---|---|
|原函数适配/模型|`tdd1`、早期 `scs2`、`scs-stage2/model.py`、`multi-ue/model.py`|取原 C 的 TDD/TBS，建立理想队列/方向/授权机会参照|独立公式、原表、边界、均值分解、种子/基线复现；始终标模型假设|
|实验准备/冻结|各组 `prepare.py`/`design.py`/来源文件|生成私有副本、计划、源/配置/ELF/模块/原文身份，检查容量/期限|坏计划/方向/身份/预算负例、冻结前后核对，准备成功不当实验通过|
|进程/网络控制|`multi-ue/run.py`、各组 `run/gate/resume`|真实启动 gNB/UE/探针，隔离网络、预检、关闭自己的进程，记录每次尝试|退出码、阶段、路径、包/抓包、实际 mask/动态库身份、严格接续|
|离线关联/统计|`layered`、`rlc-queue`、`ul-service`、各诊断组 `collect/verify`|解析真实 trace/pcap/应用 CSV，核多对多边、算每 UE 分位和同尾集合|独立原事件复算、整数求和、代码块/人口夹具、拒绝缺失/重叠/溢出；不虚拟重建丢事件|
|文献/来源|`source_audit`、`mechanism-mapping`|标实际条/表/章节/本地页序，核用户原包与论文版本|核实际文件可读/哈希；不把补注变成过去已读或最新全面认证|
|科研图/交付|各 `plot/report`、`artifacts`|把已核数据变图/Markdown/Office|数值与源逐项对、字体与页面检查；图轴/公式显示修改不改实验统计|

## 六、为什么会反复出现“旧结果保留、当前值重写”

改变采样后分析器的路径/NumPy 参数/图例，通常只需重新离线计算或生成材料；不重跑无线。相反，修正真实协议字节、关键配置前提、C 稳定性或观察程序/容量后，需要另记程序身份并重做受影响的必要组；旧 raw 和失败保留。不能用旧程序的数据改标签，不能把漏掉的 trace 补算出来，更不能按推进速度乘一个系数冒充当前实测。

最近短 MAC 纠正后只完成必要六条件，不代表历史所有 TDD/SCS/DL/长尾都在新程序上测完。这个范围差异是当前最重要的接续边界。
