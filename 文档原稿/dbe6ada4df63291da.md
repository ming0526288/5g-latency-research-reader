# 本步导出字段：防止把观测误当因果

字段依据冻结README及docs26；本文只精化工程含义，不改变已执行方法、包集合、公式或数据。

- 所有A/G/B/H为同主机MONOTONIC整数ns；G即首段真正使用grant的准备，不是首个可用grant。H_ns缺失为null，没有测得H→G条件时长，不填0ms。
- P0_ns=max(G−A,0)；no_H_P0_ns、A_to_H_ns、H_to_G_ns是加性分量I(无H)P0、I(有H)(H−A)、I(有H)(G−H)。它们为0是分量定义；后两个字段不能无条件当成H条件子集的时长。相应条件均值必须只用H非null或按sum/有H包数算；0个有H包则结果null。
- TB.MAC_header_bytes=原so−CE，指MAC SDU子头；MAC_CE_bytes含CE及它的子头；padding_bytes=TBS−MAC_SDU−原so，含填充子头/填充内容。原so已含CE，不能再叠加CE。numbered_initial_bytes是MAC SDU中的RLC SDU初传字节，差额other_MAC_SDU_bytes仍可能有RLC头，不全部称其他业务/控制。
- earlier_TB窗口[A,B)，earlier_prepared_grants窗口[A,G)，含义不同。TB新构造及进入PHY关联不是天线真实发送时间；HARQ重传可以复用旧TB，不要求新MAC构造。3个无新TB构造的grant在业务窗外另列，不伪造新TB或填充。
- *_count是包与原决策的关联数，*_affected_packets是至少出现一次的包数；同一原决策/TB可重复关联多个排队包，不能拿总和冒充唯一资源成本。reason是该轮最终分类，定位时间是ULS快照ns。
- *_sum是逐包整数分量/次数求和；comparisons中每组流数/包数相同，除packets即先正反/UE再六seed算术均值。它不是主P99配对中位。all4000和双向slow40集合固定，选尾结果不能冒充因果净收益。
- candidate_RB包括连续资源/边缘检查和轮末剩余RB不足的重分类，尚未分离；不是所有PRB已用尽的证明。E/S是gNB估计/预约，不是UE真实队列。3GPP原文及具体实现行号、P01/教材本地页序在docs26和来源JSON。

完整逐包/grant/TB/示例原行仅本地，不Git；Git只聚合、哈希/代码/说明。Office本轮未改。工程schema说明3GPP新参数/额外数学推导不适用，代数定义在方法和docs26。
