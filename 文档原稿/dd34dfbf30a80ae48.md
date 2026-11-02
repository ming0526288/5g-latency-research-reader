# TEST-481 负载七十二正式准备与计划核验

四先导及独立核验全部通过后，实际执行：

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-probe-residual
/usr/bin/python3 -B research/latency-analysis/probe-load-v3/prepare.py --matrix main --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/main-01
sudo -n /usr/bin/python3 -B research/latency-analysis/probe-load-v3/run.py /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/main-01
```

prepare79696实际exit0，72条件/19034冻结输入。独立main-plan-check-01.json命令exit0：完整Cartesian覆盖3负载×6seed×两接入×两策略，共36匹配上下文；每个负载24条件，69在六seed每UE位置恰两次；十运行文件逐SHA与旧ALG005完全相同。最大目标seed发送时长67.380054682秒，未放宽110/120s业务期限。源码C未改。

正式root已由session56949启动，当前仍运行，最终exit及是否72完成未知，不在本记录冒写通过。实际进度aux main-01/execution.json/runtime.json；所有输入/当前方法已冻，禁止重启root或编辑其源。计划完成972000完整/864000统计包仅是计划，不是现有成果。

新collect_load.py和独立verify_delivery_load.py AST实际通过，尚未运行正式汇总；该核验是工程静态语法，不替代数值独立复算。通信/数学来源v3/README及CHG330/331/333，协议本地授权版不称官网最高；新必要缺件立即全停，不下载。Office未改，原核心不停止/替换，后续实际失败/清理另TEST。
