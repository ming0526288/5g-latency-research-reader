# 修改记录 CHG-151—CHG-175

以下按原 CHG/TEST 转录，包含原命令、结果、失败与后补依据。**它们是各历史阶段的记录，后续纠错以总入口说明为准；不能把旧阶段的‘当前’当成今天。**

转录只整理标题层级与正文中的链接；源文件 SHA256 绑定原始字节。命令只用于历史追溯，本次没有重跑；文档内失效旧链接保留为文字提示，不能据此继续执行旧脚本。

<a id="chg-151"></a>

## CHG-151 长流对比报告和经验尾图离线源声明

原记录：[打开 CHG-151](../../records/changes/CHG-151_长流对比报告和经验尾图离线源声明.md)；SHA256：`2a56facdaba93dff4af327fa8468bec4f5259e2c3cd0d44172857c1d13eb7651`。

2026-10-23，继续在RAN活动时仅编写未冻结report.py/plot.py/analysis_reference.json，不读取热trace或执行统计/画图。报告分短固定每UE与长固定总量、每UE及最差分位（最大P99/P99.9可以不同UE）、十窗同一选中UE、首4000对全长、完整失败/未尝试；全部明确旧短OFF为独立参考而非新重复/算法收益，旧ON约93%不移植。两科学图计划为短/长分位与经验CCDF/十窗；CCDF选各长条件最大单UEP99.9的同一流、固定网格严格大于比例，不作可靠性置信/稳态声明。字体Arial优先/实际回退单独记录，SVG文本保留并清行尾空格。

analysis_reference固定上一组安全summary SHA，report/plot须核输入identity，防止默默改参考。离线源AST通过且均不在345内；原C/NR/运行输入不改。实际collect/report/plot须全部RAN结束后运行，后续TEST/图视觉QA/文档Git收尾。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。source_provenance.json及CHG149/150；首选协议背景/实际页序沿原声明，不新增NR逻辑；图/参考SHA/经验统计为工程方法，3GPP不规定这些图或阈值；P01 III/IV PDF2–4完整关联、不采用V-A PDF4裁峰，教材13.1.1.2 PDF530–532背景。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-152"></a>

## CHG-152 长流统计独立夹具与交付核验入口

原记录：[打开 CHG-152](../../records/changes/CHG-152_长流统计独立夹具与交付核验入口.md)；SHA256：`21d9e1975a1d7b2eaaa56fd819cd59f788db15f36c7f1735214194d6f6b05dc8`。

2026-10-23，仅新增未冻结离线verify_analysis.py/verify_delivery.py。前者用0..999的有理数线性分位期望、连续掩码和含PID/TID复用的4个合成主机快照独立核流式CPU，避免把合成值当RFsim实测；强制RAN停止后运行。后者核完整12/52流2730000/2704000、每长UE10万统计、逐UEP99/P99.9身份、十窗加权均值、CCDF单调/整数计数、有限在途残差、345当前源/执行/参考SHA、图与报告链接/字体。不是重算原包或独立模型/稳态/可靠性认证。

当前仅AST和345成员边界检查，未执行这些检查程序/新数据统计/图，不修改任何运行源。两入口等全部RAN结束后实际运行并记TEST。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。CHG149–151及source_provenance；工程统计/文件交付核验不新增3GPP要求；有理数线性插值为经验分位算法一致性，不是总体分位证明；论文教材实际页序沿README。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-153"></a>

## CHG-153 长流离线报告保留宿主观测成本

原记录：[打开 CHG-153](../../records/changes/CHG-153_长流离线报告保留宿主观测成本.md)；SHA256：`6728a7e65748dd07bfdc72157ec4dbb546e1fe8af198ca6ff12b242961b17884`。

2026-10-23，仅扩充未冻结collect/report离线源：从每条件既有observer_summary导出采样数、墙钟、observer自身CPU秒、最大采样时长/继承mask及scope；报告单列完整条件窗口的观察成本，明确内部OFF仍有外部捕获和1Hz观测，不能叫零开销或每包成本。CPU计数不用于缩放时延或唯一归因。当前仅AST通过，尚未执行新数据统计，原345/NR/C不变；完整停止后才运行本离线源。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。CHG149/150及source_provenance；宿主资源计数为工程统计，3GPP/新数学推导不适用；不更改协议或运行观测，原1Hz观察方法沿既有声明。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-154"></a>

## CHG-154 兼容本机NumPy线性分位参数

原记录：[打开 CHG-154](../../records/changes/CHG-154_兼容本机NumPy线性分位参数.md)；SHA256：`db3bdc4fbc4c0201521dbe55a581cb560a1d5da210d7ce4626fd4f45f4149425`。

2026-10-23，仅修改未冻结long-baseline/collect.py的quantiles：np.quantile(...,method=linear)改interpolation=linear，兼容实际NumPy1.21.5签名。插值、样本、分位、窗口、尾阈值均不变；完整原始RAN/345未改，不需要因离线关键字错误重测12条件。首次两个失败和最后位置写TEST249，evidence/current及合成证据未创建，修正后重跑既定入口并记录实际结果。非通信工程兼容，不新增3GPP规则或数学假设。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。TEST249实际安装源码/签名；3GPP/新数学推导不适用；科学口径source_provenance/README保持，有理数夹具随后验证。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-155"></a>

## CHG-155 按完整长流结果写研究结论并改善窗口图坐标

原记录：[打开 CHG-155](../../records/changes/CHG-155_按完整长流结果写研究结论并改善窗口图坐标.md)；SHA256：`c8997867d658bee8fe2bbd8c3aa039f0f7ef233897f7eb1930b4a65f23a67f4a`。

2026-10-23，完整collect/合成检查通过后，report生成器直接补本组主要发现：固定每UE及长总量分位范围、N8同UE成串慢包/lag1/阈值比例、十窗波动而非持续单调增长、CPU/粗推进的非唯一归因、旧ON不可移植、下一步PF零回退/独立种子。实际offered/接收率含预热而分位去500的口径写清。记录NumPy离线失败和纠正，不把它改成RAN失败。

图首次两PNG均已实际view_image查看。第二张右轴34–41ms小范围使用log导致科学计数标签费读，改为线性纵轴便于读窗均值，左CCDF/第一图分位仍log；不改任何数据。首报告/两图/首交付proof库外备份analysis-source-audit/long-baseline-delivery-20261023-01，原报告重生成、图v2视觉合格后替换活动图与proof，不只追加过时说明。原C/NR/345/原始测量不变，离线源非运行输入。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。source_provenance/README、TEST248/249及当前安全summary；结论为本组有限数据推论非3GPP强制；协议/论文/教材精确范围沿CHG149，经验相关/窗口不证明因果或稳态；坐标/字体工程呈现不新增数学模型。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-156"></a>

## CHG-156 长流结果接续说明运行命令与协议索引完成改写

原记录：[打开 CHG-156](../../records/changes/CHG-156_长流结果接续说明运行命令与协议索引完成改写.md)；SHA256：`062758ac52655410aa41af685c08c13b393be63b2907357a5af7174e35a6c455`。

2026-10-23，直接将long-baseline README/START的尚未运行、尚未完成、图未生成状态改为12全过和离线核验完成，保留NumPy首次失败及修正、所有原实验数据/历史身份。README集中原实际命令、每UE分位结果、显式0基线性插值公式/全流负载率与去预热分位口径、N8相关/包串与非稳态/非唯一CPU边界；docs10新增第29节逐条实际原文/论文教材范围，docs11加入长流已结束的运行命令及禁止重开说明。AGENTS不写实时状态，不改原始oi仓库、C/NR/345或旧测量值。

所有新科学数据/图/报告来自本组，旧短ON占比不移植；Word/PPT本组未修改，不能声称已同步。文档新增链接后最终交付核验/索引检查另TEST，Git明确白名单不混scs2/raw。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。CHG149–155及long-baseline/source_provenance/README；3GPP条款/Word实际范围和P01/教材页序在docs10第29节；线性经验分位按本机NumPy1.21.5原源码与有理数夹具核，不是标准时延目标；接续/命令工程整理不新增协议要求。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-157"></a>

## CHG-157 交付核验处理自身输出链接并写后复核

原记录：[打开 CHG-157](../../records/changes/CHG-157_交付核验处理自身输出链接并写后复核.md)；SHA256：`44dcb0bc95bb7fd3c59bb74a7c3f349d9b36993574cff377c84f932250f7ea7e`。

2026-10-23，仅改离线verify_delivery.py的本地链接检查：目标已存在或精确等于本次a.output.resolve()时可继续；后者是所有检查通过后才生成的自身proof。其他缺失链接仍拒绝。写出JSON后再读取status PASS并确认文件存在，避免文档合法自指形成检查循环。原始样本、数学、345、参考、C/NR和全部科学检查不变，无需重跑仿真/collect/绘图。TEST252记录实际失败和最后位置，最终重跑后TEST登记，既有旧proof库外保留。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。非通信工程逻辑修正，3GPP/数学推导不适用；仅处理已知自身输出生命周期，不用例外绕过原科学/协议检查。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-158"></a>

## CHG-158 十六小时仅分析授权窗口与工作计划

原记录：[打开 CHG-158](../../records/changes/CHG-158_十六小时仅分析授权窗口与工作计划.md)；SHA256：`9a514b63768a6473e8164659fe5cd41fc5e5f54b961bff5afaf096b867640f5c`。

用户最新明确禁止算法优化，要求自主持续16小时，按此建立analysis-only-16h/authorization-window.json和README。窗口UTC2026-10-23 10:00:06至2026-10-24 02:00:06，北京时间18:00:06至次日10:00:06。先补尾部关联/不同种子重复，再TDD/SCS和方向交叉、数学来源与总结文档；当前仅计划未预写运行成功。所有C调度/优化算法禁止，旧START算法下一步当前覆盖；实时状态不写AGENTS，缺必要协议立即全任务停不下载。

本轮跨北京时间日期，辅助/tmp记录生成器仅对未来新增记录的“本条日期”改为Asia/Shanghai动态日期，保留审计所需旧补注标题；不改历史记录或其hash。原辅助脚本备份库外analysis-only-20261023-01。原仓库/scs2不动，每部分说明测试Git继续，预算留清理，不能把未运行写通过。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。当前用户16小时/仅分析指令与AGENTS；本条授权/文档/日期工程整理，3GPP和数学推导不适用；后续通信/模型步骤仍须实际原文/论文/教材依据。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-159"></a>

## CHG-159 多UE慢包共同时间聚集分析方法与原文映射

原记录：[打开 CHG-159](../../records/changes/CHG-159_多UE慢包共同时间聚集分析方法与原文映射.md)；SHA256：`040476bcdd4720ca4139cc83c95efd35f8465619489078a02160e0b66f54a94f`。

2026-10-23，新增tail-synchrony/analyze.py/verify_math.py/README/source_provenance。只离线读取完整长流组12条件，不改原始数据/全分位/C/NR/调度。按发送时刻分箱，预声明5箱宽2阈值、空箱None和共同曝光、K分布/成对相关/边际积参考；公式/变量/限制在README。参考系数递推不是调度优化算法，不作独立性/显著性/因果或稳态断言。

本步实际重读38.30010.3、38.3215.4.1/5.4.5、38.3225.2.3.1、38.2114.3.2指定Word段落，P01 III/IV PDF2–4及教材13.1.1.2 PDF530–532。原345当前未变，11原文与RF附加原文已盘点可读，未下载。先人工构造数学核验，再真实全数据，实际命令/结果随后TEST；尚未启动新RAN。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。tail-synchrony/source_provenance.json；首选标准版本/条款和Word范围、论文/教材PDF页序在README；分箱/阈值/边际参考均工程描述非3GPP规定，不以统计相关断言唯一资源原因。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-160"></a>

## CHG-160 共同慢包完整报告与科学图交付核验

原记录：[打开 CHG-160](../../records/changes/CHG-160_共同慢包完整报告与科学图交付核验.md)；SHA256：`c3779ea06a1f174a6f4530c8e7db6e2e8c34876cf70999b829e93066c15f5c3d`。

日期2026-10-23。新增tail-synchrony/report.py、plot.py、verify_delivery.py及报告、安全summary/每秒聚合CSV/数学/交付证据、两PNG/SVG。report完整12项/完整K分布/每UE共同箱内外计数/5箱宽2阈值；plot两完整32分钟时间线，缺包灰色，及完整0..8K分布对假设边际积参考。无C/配置/算法变更，不把1秒箱当毫秒同时，不把独立参考当统计检验。英文Arial优先但宿主PNG实际回退Liberation Sans，metadata明示。命令见TEST256，Word/PPT本项未修改。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。首选TS38.300 V19.4.0§10.3、TS38.321 V19.4.0§5.4.1/5.4.5、TS38.322 V19.3.0§5.2.3.1和TS38.211 V19.5.0§4.3.2；实际Word范围/hash见tail-synchrony/source_provenance.json。P01 III/IV本地PDF2–4，教材13.1.1.2 PDF530–532。分箱与描述性参考为本项目数学定义，非标准规定。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-161"></a>

## CHG-161 不同流量种子控制与十八项长流预声明

原记录：[打开 CHG-161](../../records/changes/CHG-161_不同流量种子控制与十八项长流预声明.md)；SHA256：`0c450687025987c03694aee043c7697a405a944b73405276fe8de2f206186245`。

日期2026-10-23。multi-ue/run.py main新增traffic_seed_base状态/flow种子参数，argparse新增--seed-base默认20261014；standards-review/rerun_sdap.py execute仅声明时转发；默认实际流字典与Random序列不变。无C/NR/ELF/RF库/无线配置/算法变更。原两文件私有备份analysis-source-audit/seed-repeats-20261023-01/before。新增seed-repeats design/prepare/gate/run/verify_controls/source_provenance/README：6业务seed×N1/4/8反序交替、全OFF、原长deadline、原legacy gates+实际种子核、绝对授权时间/余时守卫及firstfailure，不自动重试。旧345两项有明确before/after，其他343项不变；新364独立冻结0a7f0912fa0812b5f672a9f82db1b409d692b2d25fb1f25b48cf7cec1934faea，plan 85ce4554231376a787f1bac7c47ec3bad4be39f9976faa023a0347238dbfdf83。用途检验尾部对不同到达序列的敏感性，非优化/独立性保证。真实运行入口/公式/边界见README，当前只准备未新RAN。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。实际读取38.300 V19.4.0§10.3 Word3100–3105、38.321 V19.4.0§5.4.1 Word2150–2155/§5.4.5 Word2602–2607；既有已审38.211/213/214/331配置不变；P01 III/IV本地PDF2–4、教材13.1.1.2 PDF530–532。逐文件SHA/条款/工程选择见seed-repeats/source_provenance.json，3GPP不规定测试种子。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-162"></a>

## CHG-162 六种子长流离线收集源准备

原记录：[打开 CHG-162](../../records/changes/CHG-162_六种子长流离线收集源准备.md)；SHA256：`dad0278ea6d1df54b6a309b87a6a76714cc386e7fcaf00c78021be52d8759587`。

日期2026-10-23。新增seed-repeats/collect.py，复用long-baseline/collect.py的完整匹配/分位/等包数窗/连续慢包/CCDF/在途积分恒等式/流式CPU方法，只用新design/gate，case与CSV显式seedbase、流显式trafficseed，文字改为六不同PRNGbase而非旧短/长混合。analysis_reference锁原collector和旧summarySHA，旧源不改。新增在364运行冻结之后，仅离线作者源，不参与当前RAN身份。活动RAN时只源码语法编译，未实际统计新包或给新分位，不把将来目标写已完成。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。seed-repeats/source_provenance：38.300V19.4§10.3、38.321V19.4§5.4.1/5.4.5、38.322V19.3§5.2.3.1；P01 III/IV本地PDF2–4、教材13.1.1.2 PDF530–532。离线统计不是协议规定。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-163"></a>

## CHG-163 固定CPU的TDD方向与多UE二十四项预声明

原记录：[打开 CHG-163](../../records/changes/CHG-163_固定CPU的TDD方向与多UE二十四项预声明.md)；SHA256：`b777b16b24c1c4f72ffbb732ecd4d495f88a57d5536cd0868764719a36d82076`。

日期2026-10-23。新增tdd-confirmation design/prepare/gate/run/来源/README；24条件目标126流5175000关联/5112000统计，18短N1/4/8双向×三配比与6N8UL长两反序种子。复制当前8UE输入只变完整D/U两个字段，S6D4F4U/SSB1/sib1_tda13/PRACH52/TDRA/CPU/C/NR/binary不变。gate独立复用原long检查，把方向和D/U按已冻结row核对，额外实际seed检查；run在core恢复前拒绝活动RAN/seed18未完成，硬截止/余时/firstfailure。还未新启动TDD业务，不改当前seed364任何输入。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。tdd-confirmation/source_provenance：首选38.213V19.5§11.1/4.1CaseD/§13表13-8及13-12、38.331V19.4§6.3.2 TDD IE、38.214V19.5表5.1.2.1.1-2行14、38.211V19.5表6.3.3.2-4行52/38.213§8.1；原文段落/native表及哈希明确。P17本地IEEE2020 III/IV-A PDF3，P19本地arxiv2012.05507v1 II PDF2–3及选读III，P01 PDF2–4，教材4.3.1 PDF79–80及13.1.1.2 PDF530–532。配比/CPU/种子/统计为项目选择。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-164"></a>

## CHG-164 机会等待推导与六种子报告绘图作者源

原记录：[打开 CHG-164](../../records/changes/CHG-164_机会等待推导与六种子报告绘图作者源.md)；SHA256：`ee4e21e34352403dce894b9da3737aa206eb285573690b9a9e8c9aaae53fc81b`。

日期2026-10-23。新增tdd-confirmation/calendar.py及数学模型与测量边界.md：名义机会间隙积分/CDF/分位、方向与K2控制候选区分、当前C真实图样及TBS和独立相位枚举的待运行核验；明确CP/主动授权/实际grant/CPU边界。新增seed-repeats report.py/plot.py：完整18项78UE表、逐UE独立分位后六轮最差范围/中位、全十窗/CCDF网格/主机代理，拒绝未完整组，英文Arial声明与实际fallback元数据。源仅离线作者，在364/403冻结后新增不参与RAN，不改冻结源/C/NR/算法。当前活动seed RAN，尚未执行新collect/数学compile/图，不写新测量值；手工日历表明确是模型非实测。

### 依据与适用边界 2026-10-20补注

本条2026-10-23新增。tdd-confirmation/source_provenance及数学模型与测量边界：38.213V19.5§11.1，38.211V19.5§4.2/4.3.2，38.331V19.4§6.3.2，实际再读38.214V19.5§6.1.2.1 Word8383–8394；源码nr_rrc_config.c871–907、gnb_config.c953、scheduler_ulsch.c2116–2162/2252–2265、config.c637–655；P01 PDF2–4、P17 III/IV-A PDF3、P19本地arxivv1 II PDF2–3；教材4.3.1 PDF79–80及13.1.1.2 PDF530–532。均匀相位/统计/预算为项目方法。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-165"></a>

## CHG-165 六种子长流完成汇总独立验证与窗口收尾

原记录：[打开 CHG-165](../../records/changes/CHG-165_六种子长流完成汇总独立验证与窗口收尾.md)；SHA256：`bd42d8eeea6dfb87e8134ae0b93f47da3867fec0f2abba8451e33d2855874905`。

日期2026-10-24。18条件完整RAN实际已结束，session17149 exit0；本次新用户要求先收尾再解释Word，之后在无RAN时执行既有collect/report/plot，新增seed-repeats/verify_analysis.py（独立有理数/复用PID夹具）与verify_delivery.py（逐case/计数/CSV/身份/图核）并保存安全summary/逐UE聚合CSV/两PNG/SVG和报告。新增tdd-confirmation/evidence/calendar-verification.json是独立数学，不是24项RAN。直接改README/数学文档中过时“进行中/待执行”，补analysis-only-16h实际完成/未完成与时间观察，不改AGENTS。原16h窗口截止UTC02:00:06，工具等待返回时观察UTC04:03:55；中间没有持续推进交互步骤，原因未定位，不声称连续完成16h研究、不把新指令后收尾回填原窗口。原C/NR/二进制/无线/算法不变；Word/PPT未改。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。seed-repeats/source_provenance：首选38.300V19.4§10.3、38.321V19.4§5.4.1/5.4.5、38.322V19.3§5.2.3.1及既有已审38.211/213/214/331无线字段；P01 III/IV本地PDF2–4，教材13.1.1.2 PDF530–532。随机种子/CPU/统计为项目选择，非标准规定。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-166"></a>

## CHG-166 新增Word通俗阅读说明术语与优化用途

原记录：[打开 CHG-166](../../records/changes/CHG-166_新增Word通俗阅读说明术语与优化用途.md)；SHA256：`bba615c380e190b506a3d1a8bb4d8ffcc00c1120c0366c8471b1059d40cd9f5a`。

日期2026-10-24。按用户要求在docs/12_Word阅读说明_名词解释与时延优化的关系.md回答：实际做过什么、业务路径/边界、D:U/S/14:5、五组术语解释、五类分析如何帮助优化、最新18项范围、旧大数值与新值负载/CPU差别、如何读Word、明确未完成项。旧Word是2026-10-22快照，不把其全部未测项当当前进度；24新TDD只准备、长ON/60/240支持/真实RF等仍待，算法未实施。增加source_audit/word_reading_guide_sources.json及read-only verify_reading_guide.py/版本化核验，START加入新入口。说明不是新通信配置/算法，不修改原Word/PPT；协议全文及Word文本提取仅库外，Git只来源哈希/定位。文字迭代增加业务测量不含注册/视频/机械闭环边界，最后核验final02。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。source_audit/word_reading_guide_sources.json：实际读原Word全部374正文/表文本和原QA页3/5/16/19，SHA1525c42f97ff7fd7028fdb77afe08578b37960137f1a7d870849e43d8a85b5bb未改；新读本地23.501V20.3§6.2.1/2/3 Word11608–11629/11675–11698/11735–11756，38.321V19.4§5.4.2 Word2269–2280，38.212V19.4§6.2.1 Word8984–8988，38.213V19.5§9.2.3 Word2870–2881及表9.2.3-1；其余已读TDD/SCS/层界来源精确引用于正文/既有source_provenance，P01 III/IV PDF2–4、教材4.3.1 PDF79–80和13.1.1.2 PDF530–532。工程术语/Markdown整理的3GPP强制要求和新增数学推导不适用，做一致性检查。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-167"></a>

## CHG-167 当前用户继续TDD对照的新运行预算和独立冻结

原记录：[打开 CHG-167](../../records/changes/CHG-167_当前用户继续TDD对照的新运行预算和独立冻结.md)；SHA256：`5b4812061e194421e2566a3d5bdc38ef234ba0dda1c5930a708241a5312ebb65`。

日期2026-10-24。用户“接着做那就”明确继续24项TDD分析，不做算法优化。旧run.py、prepare.py、source_provenance及旧403/16h授权文件全部原样保留；新增run_current.py/prepare_current.py/current_source_provenance.json/verify_current_controls.py和安全准备证据。正式plan-03复制plan-02三配置全部字节相同，24业务字段除了副本路径完全相同。新增按运行开始MONOTONIC计的工程批次保护上限Σ24(receiver_timeout+600)+600=29862s，绑定planSHA；旧短110/120、长2087/2117不变，不修改NR定时器或延长旧16h。core任何修改前核冻结/无RAN/前18全部PASS，失败即停、保留现场，无自动重试。新441冻结SHA769580cf179574daba576daa951aa09c963d30da7a3f31b65eabdc3dca39dcaf，plan25785169818d7783ff159d64632d77fdb62c65b8322cb30297812fbb5183ed4b、budget57485af4badd44a84f829ef2e49c1b3d986d602252c804e136de17fcf34ff279；旧403全部当前一致。C/NR/ELF/RF库/调度/负载/视频不变。实际入口README，当前仅准备，不能当24项成功。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。tdd-confirmation/current_source_provenance.json：本步12份原文SHA/CRC/XML/封面核，实际重读38.213V19.5§11.1 Word4619–4648、38.331V19.4§6.3.2 Word42485–42530、38.214V19.5§6.1.2.1 Word8383–8385、38.300V19.4§10.3 Word3100–3102、38.321V19.4§5.4.1 Word2150–2151；38.104V20.1表5.3.2-2/5.3.5-2 n261原表，访问控制/PRACH原表沿同字节输入重新核几何。P01 III本地PDF2–3，P17 III/IV-A PDF3、P19本地arxiv2012.05507v1 II PDF2，教材4.3.1 PDF79及13.1.1.2 PDF530。新计时/复制/进程控制为工程选择，3GPP与新增NR数学推导不适用。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-168"></a>

## CHG-168 TDD二十四项离线收集报告与双向尾部图作者源

原记录：[打开 CHG-168](../../records/changes/CHG-168_TDD二十四项离线收集报告与双向尾部图作者源.md)；SHA256：`5e92fcd7ec063dc1998d5d055ba655272065598d460e99a7e4d5716ea4debbc4`。

日期2026-10-24。新增tdd-confirmation/collect_current.py、report_current.py、plot_current.py和current_analysis_reference.json；在441运行冻结之后添加，仅离线作者源。复用seed collector统计函数（四函数AST字节语义一致），主过程增加D/U/direction、完整gate失败不输出成功子集分位、短/长尾样本边界、原measurement三外部REALTIME区间及同包均值和残差，对MONOTONIC总量另列。报告完整24状态、短双向P99、长两反序块P999及同块差、CPU/粗MAC代理和名义日历界限；不说算法收益/唯一原因/全局最优。两图作者源用NaN表示缺测、不将短P999当可靠尾，CCDF阈值不外推，Arial/fallback明示。未修改运行源、NR/二进制/无线/算法，活动时未运行统计/画图。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。current_source_provenance.json的12本地原文与P01 III本地PDF2–3、P17 III/IV-A PDF3、P19本地arxivv1 II PDF2、教材4.3.1 PDF79/13.1.1.2 PDF530；UL/DL层界首选38.300V19.4§4.4.1/§6、38.321V19.4§5.4.1及38.322/323和37.324已读条款。统计/时钟分段为工程测量定义，不能代替独立PHY/空口。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-169"></a>

## CHG-169 TDD结果独立统计与交付验收入口

原记录：[打开 CHG-169](../../records/changes/CHG-169_TDD结果独立统计与交付验收入口.md)；SHA256：`f3d3b0eec871c2d170dca75cff5dd57297fcc32e5fb39bbff0a3cc4f7306b848`。

日期2026-10-24。新增tdd-confirmation/verify_analysis_current.py、verify_delivery_current.py。前者独立有理数分位、连续超时串及PID/TID复用计量夹具；后者逐项核24条件126流、短长计数、方向/配比、原始状态及摘要SHA、三段同包REALTIME均值和、逐UECSV和图SHA，要求实际视觉审核回执。只编写并compile，不在活动RAN时运行统计/绘图；不修改441冻结源或通信实现。正式输出仍待全RAN停止。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。非通信工程验收脚本新增，3GPP/数学模型变更不适用；当前研究依据仍为tdd-confirmation/current_source_provenance.json，原441运行源/NR/配置未改。独立有理数分位期望、PID复用夹具及原始运行状态用于一致性核验，脚本尚未执行实际统计。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-170"></a>

## CHG-170 TDD当前入口直接重写并去除过期未运行表述

原记录：[打开 CHG-170](../../records/changes/CHG-170_TDD当前入口直接重写并去除过期未运行表述.md)；SHA256：`afa1aa68c81b71360a8b9548d5dac3c65081394bb1ec1cd50ee5c04e73f89e2d`。

日期2026-10-24。直接重写tdd-confirmation/README.md：用18短PASS/6长进行中替换旧仅准备/未启动正文；旧403、过期16h入口退为历史，当前441/run_current为正式入口；列已执行和待执行命令、失败留证及短长统计边界。并更新START的TEST273里程碑。没有修改441冻结源、NR参数或模型。验收脚本仅语法通过，统计/图/Word仍待全RAN结束。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。非通信文档整理，3GPP/数学推导不适用；源依据仍current_source_provenance.json，实际进度据execution/TEST273。旧原始记录保留，未把旧数字改标成新实验。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-171"></a>

## CHG-171 当前五类总结Word作者入口与旧文纠偏计划

原记录：[打开 CHG-171](../../records/changes/CHG-171_当前五类总结Word作者入口与旧文纠偏计划.md)；SHA256：`0097892717bfd1e4867979a016945480afa961e740a7670ed0b817aa15a1e529`。

日期2026-10-24。新增artifacts/build_word_tdd_current.py，复用原Report版式/原生OMML/Arial及宋体。新入口要求24项全通过及同SHA交付回执、无RAN、备份原Word后才替换；正文按名词、路径、时间戳、TDD字段/数学、当前ULDL/长尾、SCS边界、六seed、多层与观察成本组织，纠正旧逐DCI未关联及PDCP容量等过期说法。当前仅源码，原Word/PPT未改、无artifact marker、无渲染，不宣称交付。后续还须源页实读、独立数值核验与逐页QA。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。本步仅离线文档作者源码准备，未执行DOCX修改，3GPP/数学结论变更不适用。未来正文首选current_source_provenance已核12原文及docs10逐条定位；将复核P02/P06等实际引用全文后才生成。所有数值读取各原组安全summary，不合池、不改源标签；本代码不是已完成Word证明。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-172"></a>

## CHG-172 Word作者标明P06的FDD背景与论文版本身份

原记录：[打开 CHG-172](../../records/changes/CHG-172_Word作者标明P06的FDD背景与论文版本身份.md)；SHA256：`55074f45e0a0e43897d30b7d11a96c31b553ec736abc662ec7c1fac5b825599d`。

日期2026-10-24。直接修订待执行build_word_tdd_current.py引文：P06仅支持时延分解方法，其原FDD/CG或SPS场景不搬入本TDD动态/主动grant；补期刊封面/上线日期。P02的Rel15概述不替代当前38系列原文，未读更新全文不称新版认证。PDF选页文本在analysis-source-audit/tdd-confirmation-20261024-01/word-background-reread，目录在协议原文之外。未实际生成或修改Word。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。实际重读本地P02 PDF2–3 II/III/IV和P06 PDF3–6 III，另查各PDF1页；P06封面IEEE TVT72(2)Feb2023、上线2022-09-21、期刊current2023-02-13；P02不冒称已核更新全文。协议首选current_source_provenance的12可读本地原文，未改NR/模型。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-173"></a>

## CHG-173 二十二页当前五类分析PPT作者入口

原记录：[打开 CHG-173](../../records/changes/CHG-173_二十二页当前五类分析PPT作者入口.md)；SHA256：`d73fd57f5310679ad7e4ee6278d1585a102a80d8d64f2123eb74317ebd26674f`。

日期2026-10-24。新增artifacts/build_deck_tdd_current.mjs，使用现有artifact-tool及原1280×720/Arial+中文补充字体，22页原生表、线图和用户要求的可编辑包路径/关联图，分别呈现当前24TDD、六seed及旧短ON，改掉旧逐DCI未关联及PDCP预算表述。要求完整24项/同SHA回执才执行导出；源码目前仅语法检查，原PPT不改，无PPT marker，不把源码当交付。真正导出前须按presentations技能marker、最终器、逐页render/看图，原活动PPT先备份新通过后再撤换。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。仅PPT待执行作者源准备，未创建PPTX，3GPP/数学模型变更不适用；内容定位current_source_provenance的12本地原文、P01III/IV PDF2–4、P17本地IEEE2020 PDF3、P19本地arxivv1 PDF2–5、教材4.3.1 PDF79/13.1.1.2 PDF530。实际数据从各原组summary读入且要求当前24项交付回执SHA相同。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-174"></a>

## CHG-174 TDD离线入口增加控制器关闭证据守卫

原记录：[打开 CHG-174](../../records/changes/CHG-174_TDD离线入口增加控制器关闭证据守卫.md)；SHA256：`4c203c44c9b77a17c309fd94d9a4656d263a07612611bdb8869ed6f1dab01ba6`。

日期2026-10-24。新增offline_guard.py、verify_offline_guard.py，并接入当前collect/report/plot/两验收入口。除原进程检查外，要求runtime-budget.json有真实ended_utc、带时区的起止与非负MONOTONIC耗时；即使sandbox进程视图为空也拒绝活动控制器。此门槛只证明本控制器关闭，仍须单独在宿主核无RAN/命名空间清理，不冒称全宿主证明。新源均在441冻结后添加，通信运行源/无线/数据不改。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。非通信离线执行隔离工程，3GPP/数学推导不适用；发现sandbox /proc仅见自身，不能仅凭空进程表判宿主RAN停止。新增控制器结束证据门槛补充宿主ps/清理核验，原441/NR未改。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。

<a id="chg-175"></a>

## CHG-175 通俗阅读说明直接改正TDD未启动旧状态

原记录：[打开 CHG-175](../../records/changes/CHG-175_通俗阅读说明直接改正TDD未启动旧状态.md)；SHA256：`53b75645cb270f3d3fbe634b7d95b7199292f94c6a344fbccd4ed6208a81bc19`。

日期2026-10-24。直接修改docs12，把24项尚未启动改为18短全通过、两长已通过/其余运行的有时间戳截面；六seed18项不再笼统叫最新18项，24项链接更名当前运行说明。保留reading_guide_tdd_runtime_checkpoint安全状态快照及旧Word/六seed身份，不改原历史证明。verify_reading_guide更新进度断言，原Word仍旧快照未改。

### 依据与适用边界 2026-10-20补注

本条2026-10-24新增。非通信说明进度纠偏，3GPP/数学模型未改；当前TDD实际execution快照及旧Word/六seed原summary身份，正文各术语协议依据仍docs10/current_source_provenance。未把运行截面当全部业务完成。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
