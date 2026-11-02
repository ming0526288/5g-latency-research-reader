# TEST-458 QUEST五模式30条件正式同程序对照

状态：正式root已完整退出0，30/30通过，统计汇总/独立验证另TEST460/461。根analysis-source-audit/quest-closure-20261029/main-01，禁止重启/覆盖或改冻结源。实际prepare session62511 exit0，13237输入/30条件；实际run session65987 exit0；UTC04:34:23.888298–05:16:23.563578，2519.675664秒，405000完整/360000统计UL、90流，30/30全部业务/分层/完整初传/真实QoS/N4/报告/模式/SR与冻结输入门禁通过。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-quest-closure
/usr/bin/python3 -B research/latency-analysis/quest-closure-v3/prepare.py --matrix main --output /home/lbh/oiwireless/analysis-source-audit/quest-closure-20261029/main-01
sudo -n /usr/bin/python3 -B research/latency-analysis/quest-closure-v3/run.py /home/lbh/oiwireless/analysis-source-audit/quest-closure-20261029/main-01
```

前置先导完整及独立全量通过TEST456/457，失败TEST453/455保留。配比/周期/实际QoS/SR/报告/CPU/包数/期限与同程序设计CHG313/v3 README。仅用独立核心网副本，原核心不改，结束须核原身份及全部自有资源清理。协议优先/精确条款CHG313与方法README，本步没有新必要缺件。每条件进度及最后成功位置以execution.json/stage为准，未开始业务不填时延0，firstfailure保留。

最终runtime complete_plan=true、original_core_unchanged=true、13237冻结输入一致。after环境实际exit0，原4受检核心身份相同，RAN0/netns0；自有qclose容器/路由/bridge回收。全部原始root/失败样本保留，正式没有条件失败或补跑。尚须独立原始及统计表复核，未据此预写算法赢家。
