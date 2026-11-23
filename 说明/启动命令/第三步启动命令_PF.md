# 第三步启动命令 · PF

目前先用已保存的第二步记录核对 PF。原双 UE 结果和运行命令可直接复用。 [第二步门限 0 双 UE 的实际命令](第二步/1_门限0的ping多UE.md)

## 先核对实际调度入口

以下是只读检查，在已有运行源码中定位候选排序、PF 得分和排序调用。

```bash
cd ~/oiwireless/oi-wireless-ran-ping-slot-validation
rg -n 'static void pf_ul|base_coeff|qsort\(UE_sched' openair2/LAYER2/NR_MAC_gNB/gNB_scheduler_ulsch.c
```

如果已有业务记录缺少所需的竞争条件，我会先确定缺的是哪个负载或事件，再登记对应的输入与输出。专用竞争场景的命令待验证。无线启动仍按核心网、gNB、各 UE 和业务分终端执行。

[第三步规划](../文献导读/第三步规划_PF基线与调度核验.md) · [第三步知识点](../算法知识点说明/十二步知识点/第三步知识点_PF.md) · [第三步结果与分析](../研究结果与分析/第三步结果与分析_PF.md) · [返回启动命令总目录](启动命令总目录.md)
