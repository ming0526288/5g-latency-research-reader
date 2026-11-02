# v2：修正真实授权锚点，保留v1失败

本版仅修正状态后处理的跨周期锚点选择，C/ELF/配置/无线消息不变。v1的plan-01首项QUEST已交付13500完整/12000统计UL包、既有分层/服务图/QFI/真实QoS/公式核验通过，但新状态分析对齐失败，原根仍FAIL、PF未运行。禁止改v1目录或失败输出。

错误为把RRC/no_data等未授权决策与原始元数据相同的另周期grant当作锚点。v2只用reason4/11/15的真实授权，确认唯一整1024-SFN-cycle偏移后再应用全部记录；所有未授权事件、极端慢包仍保留。不是选择性删除失败事件，也不使用最近墙钟强配。实际反例和变更见CHG284/TEST419/420。

完整字段、160B布局、未知哨兵、默认关闭/容量、协议/论文/教材逐条定位、原120kHz/TDD/QoS与测量数学见[v1方法](../ul-state-observation/README.md)。本步原文可读，没有新增所需协议；版本仍为本地已授权封面版本，不冒称独立官网最高。锚点与采样为工程定义，不是标准算法。

先在新的analysis-v2-01离线输出重放已交付QUEST原始数据，不覆盖plan-01；通过后再仅补尚未运行PF到新plan-02，同一两个ELF和8模块SHA、同种子/反序/流量与所有门禁。两次来源和原失败状态分别报告，不称原根2/2 PASS、不重发已成功QUEST业务。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-ul-state-observation
/usr/bin/python3 -B research/latency-analysis/ul-state-observation-v2/analyze_state.py /home/lbh/oiwireless/analysis-source-audit/ul-state-observation-20261028/plan-01/obs-s3-reverse-quest --output /home/lbh/oiwireless/analysis-source-audit/ul-state-observation-20261028/analysis-v2-01
/usr/bin/python3 -B research/latency-analysis/ul-state-observation-v2/prepare.py --output /home/lbh/oiwireless/analysis-source-audit/ul-state-observation-20261028/plan-02
sudo -n /usr/bin/python3 -B research/latency-analysis/ul-state-observation-v2/run.py /home/lbh/oiwireless/analysis-source-audit/ul-state-observation-20261028/plan-02
```

命令不代表已执行通过，当前状态看CURRENT及TEST。无新算法、无优化获益承诺，Git取消、Office未改。
