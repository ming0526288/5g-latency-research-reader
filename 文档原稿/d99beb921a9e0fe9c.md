# TEST-090 多UE资源模型与实际轨迹对照

首次模型命令在创建输出目录时PermissionError退出1：前面sudo准备脚本新建了root所有的results/multi-ue父目录。尚未创建模型输出/编译C/仿真数据；不是协议或模型数值失败。申请权限后sudo -n chown lbh:lbh research/latency-analysis/results/multi-ue退出0，只恢复本阶段自己新建父目录；prepare.py同步修复仅对新建父目录设置SUDO_UID所有权。未改任何无线参数或已有样本。

随后实际执行：

    /usr/bin/python3 research/latency-analysis/multi-ue/model.py --output research/latency-analysis/results/multi-ue/model-01 --packets 4000
    /usr/bin/python3 research/latency-analysis/multi-ue/compare_trace.py --data research/latency-analysis/results/multi-ue --output research/latency-analysis/results/multi-ue/trace-01

两脚本在全部RFsim/CPU诊断结束后启动，模型CPU计算不与业务并发。模型/TBS/RR与时钟缩放假设看CHG-057/058；新结果完成后按实际补记。独立MAC帧速率用于额外墙钟服务时间轴敏感性，不拟合业务P99，不给无帧观察的历史运行造r值。

模型与轨迹两命令实际退出0。224条件、2520个UE/种子统计行、10080000预热后UE包实例；168次N1逐包退化核对单FIFO通过，字节守恒/逐包分项求和断言全部通过。N4固定总/每UE输入重合按条件列示，不伪称独立输入。64个实际UE轨迹各16个共同相位比较完成，3个诊断运行另按独立MAC帧速率缩放服务轴，非P99拟合。

N8诊断名义理想RR最大P99≈19.374242ms；观测r≈0.358973后约27312.650575ms，实际最差UE42672.713517ms。只能说帧推进减速解释积压量级，不能凭剩余差额指定协议层/CPU贡献。原始名义和缩放两组都保留，其他无帧观察运行不填r=1。模型容量/ρ仅声明的参考，不把有限运行排空当稳定。

## 依据与适用边界 2026-10-20补注

当前依据优先TS38.300 V19.4.0 §10.2/10.3、TS38.321 V19.4.0 §5.4.1/5.4.4/5.4.5；TDD/授权/TBS按38.211/213/214 V19.5.0及38.331 V19.4.0已读条款。论文/教材辅助设计，不能替代协议；精确定位见正文和[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。

依据编号：S01、S02、S03、S04 §5.4.1/5.4.4/5.4.5、S05 §10.2/10.3、S06；B02/B04/B05；P01/P06/P24 §VI PDF7–8；C02/C03/E01/E02/E03/M01。第三阶段多UE：协议定义优先，模型/软件支持/真实多UE业务分别报告，现有PF和首UE偏置未优化。 本次具体UE数量/负载/测量与数学模型属项目选择，原文版本按用户提供核读、未独立宣称官网最高版；非完整Release认证。缺协议先告诉用户，不猜测、不自行下载。
