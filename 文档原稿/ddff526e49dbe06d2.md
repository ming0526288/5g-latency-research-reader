# TEST-465 授权成本第二实现独立核验与字段错误纠正

实际命令，cwd `oi-wireless-ran-grant-timing`：

```bash
taskset -c 2 /usr/bin/python3 -B research/latency-analysis/grant-timing-results/verify_cost.py --root /home/lbh/oiwireless/analysis-source-audit/grant-timing-20261029/pilot-02 --cost /home/lbh/oiwireless/analysis-source-audit/grant-timing-20261029/pilot-cost-02 --output /home/lbh/oiwireless/analysis-source-audit/grant-timing-20261029/pilot-cost-independent-02.json
```

首次exit1 KeyError:rnti：作者误从flow摘要取不存在字段，原始记录可读、触发关联已到每UE核验环节；没有输出成功文件。根因确定为离线脚本错误，不是协议缺失/接入/业务失败；pilot原业务早已完整，正式runner继续其独立冻结方法，未受改动。

修正为从对应UE的原始ue-proc正SR记录获取真实rnti，非uid算身份，再执行同命令exit0：1条件37499全部原始触发关联；实际F/threshold、目标帧展开、有限窗预算与资源和均通过。本脚本未在main冻结清单中，修改不动正式运行输入；cost.py/已有冻结方法不改。

新增collect.py及grant-timing-results全部py用ast.parse实际通过，尚未运行正式collect。一次读main/runtime.json发生FileNotFoundError（runner结束时才生成），execution.json已有完成项；不是实验停止/数据丢失，不重启root。后续按execution监视，最终才查runtime。缺件无新增，Office未改。
