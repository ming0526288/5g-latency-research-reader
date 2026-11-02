# TEST-335 修正后首项RFsim路径检查失败及完成位置

日期2026-10-25。实际sudo taskset启动已声明service-process/run.py，root15024 exit1关闭；UTC08:11:11.794692至08:11:39.180948，elapsed26.932139s。首N1完成核心关联/UE接入/TUN/route/capture/receiver和UL预检3ping exit0；业务尚未开始，traffic_start_mono_ns不存在，未启动编号UDP；before_traffic的RFsim真实映射路径gate报Different RF simulator library loaded，停止后五项。不是业务超时/丢包/协议缺件。children_stopped true、宿主ps仅表头exit1，无RAN。private results/header-service-01/runs-01完整保留，原795复核不变。

实际readelf -d旧gNB显示DT_RUNPATH原研究build；源码loader default空路径，用dlopen同名so。原失败当次maps实际字符串未落盘，不能虚构逐行maps证据；明确直接原因路径不匹配，接续显式LD_LIBRARY_PATH及不变实际map gate再核根因。外层原runner有END exit0但status未完成，最终严格gate仍使root失败，不按中间0误称PASS。

## 依据与适用边界 2026-10-20补注

本条2026-10-25新增。本次为动态库加载/实验进程安全工程纠正，3GPP/新数学推导不适用；MAC修正及无线字段依据仍CHG214–215列明原文，不改变协议参数；实际读common/utils/load_module_shlib.c及gnb ELF DT_RUNPATH。具体标准定义与工程选择按正文区分；不把未执行步骤写为通过，不构成全部NR一致性、稳态或真实射频认证。
