# TEST-430 SR配对结果与控制RF成本汇总

2026-10-28，CHG289，完整根与独立复核均已停止。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-sr-period-mechanism
/usr/bin/python3 -B research/latency-analysis/sr-period-results/collect.py --output research/latency-analysis/sr-period-results/evidence/current-01
sudo -n /usr/bin/python3 -B /home/lbh/oiwireless/oi-wireless-ran-sr-period-mechanism/research/latency-analysis/sr-period-mechanism/environment_check.py --output /home/lbh/oiwireless/analysis-source-audit/sr-period-mechanism-20261028/environment-after.json
```

环境after实际退出0：原核心4受检容器、RAN0/netns0；collect进一步比较原核心身份、自己容器名及172.30.207.0/24路由不残留。完整RF分箱仅使用业务窗内部、连接数稳定的既有记录；不是单包时延部件，不混加进UL。

配对先逐种子40→20/10求最差UE P99降幅，再取3次中位；不拿两个中位数直接相除冒充同一统计量。生成9行条件、27行UE、6行配对与36行RF过程安全CSV/JSON/中文MD。实际退出/数值及限制以执行后结果填写；Git取消、Office未改。

实际collect退出0 PASS；40/20/10槽的最差UE UL P99三种子中位11.705915/9.183985/7.955793ms，UL均值中位5.821440/4.642218/4.302051ms，first-wait均值中位3.769125/2.666536/2.190501ms。20/10相对各自同种子40的最差P99降幅中位21.977726%/32.471822%；6个种子-周期比较均改善、18个逐UE配对也均改善，但不是18个独立种子或普遍收益证明。

控制代价：名义机会率1/2/4倍，正SR请求数每条件三种子中位7196/14987/24166；gNB SR指示记录中位19950/39960/79653。PF局部墙钟均值中位0.648/1.044/1.048µs，RF样本推进比中位1.017/1.019/1.016；这些局部计时/事件数不代表整机CPU、RE或能耗实测，不把RF比率用作单包缩放。九项监测的三类资源错误字符串均0，其他协议/物理条件仍限本工作点。

环境after与before四个受检原核心身份相同，RAN0/netns0，自己latency-sr-*容器名和172.30.207.0/24路由均不残留。最终报告/链接/源码/导航交付核验见TEST431及中央TEST432，原先成功或失败的旧根均未重写。
