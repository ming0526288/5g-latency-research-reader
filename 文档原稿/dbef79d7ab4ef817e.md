# TEST-356 首轮八条件完整栈全部结束与回收

2026-10-26，TEST355命令的工具session26992最终exit0，UTC03:36:13.604970至03:53:04.130816，单调耗时1010.525866513秒（约16分51秒），不是4200秒全程占满。root runtime-budget complete_plan=true，execution八项全部PASS，8次新RAN尝试，无全栈失败或重试/复用。共42条UE流、189000完整关联/168000统计包。

每UE4500包/500热身/1200字节，1/4/8UE同一新gNB程序在PF/WAIT切换，8UE两个反序块。各case保留runner命令、QFI/路由/抓包、实际RF模块路径/SHA、线程亲和性、external/layered/RLC/QFI/service分析和原gate。每项均完整gNB+UE+UL业务，不是仅gNB或ping；N3与TUN全编号关联，无丢包和删慢包。初始110/120s业务期限没有延长。

原始目录results/queue-service-pilot-01/runs-01，冻结计划plan-01。新增原因观测容量均无溢出，严格模式/权重门槛均通过。算法效果B1正面/B2负面，见CHG231，不把运行通过写成优化通过。全部RAN结束后开始独立核验见TEST357；宿主回收见TEST358。
