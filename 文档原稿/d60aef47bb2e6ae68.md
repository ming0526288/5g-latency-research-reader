# TEST-488 v4四定点先导完整与独立复核

root实际命令CHG340/TEST487，session2782 exit0/386.048746605s，4条件54000完整48000统计UL，12流。前16旧成功子集/旧失败和此前其他先导不混本先导，更不混后续正式。

以下实际命令在active树执行，均exit0（root统一/home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot-04，输出统一同aux父目录）：

```bash
taskset -c 2 /usr/bin/python3 -B research/latency-analysis/probe-load-results/verify.py --root /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot-04 --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot04-independent-01.json
taskset -c 3 /usr/bin/python3 -B research/latency-analysis/probe-load-results/cost.py --root /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot-04 --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot04-cost-01
taskset -c 5 /usr/bin/python3 -B research/latency-analysis/probe-load-results/verify_policy.py --root /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot-04 --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot04-policy-independent-01.json
taskset -c 2 /usr/bin/python3 -B research/latency-analysis/probe-load-results/verify_cost.py --root /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot-04 --cost /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot04-cost-01 --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot04-cost-independent-01.json
taskset -c 2 /usr/bin/python3 -B research/latency-analysis/probe-load-results/arrival_integrity.py --root /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot-04 --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/pilot04-arrival-01
sudo -n /usr/bin/python3 -B research/latency-analysis/probe-load-v4/environment_check.py --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/environment-after-pilot-04.json
```

独立四项session38345/68820/31891/94181；计数/18995保持/实际采集24pcap/原核心保持见CHG341及安全JSON，arrival4/12/6匹配，实际env0残留。新增TUN-s2048和严格采集门禁原方法实际条款与工程源码CHG339；未变C/十运行文件/无线或业务。APP为MONOTONIC单向非RTT；P99不加，不把先导单seed正负结论当多seed验证。原失败业务APP慢包与19缺观测保留，不能删异常强过。后续main-02完整72及独立检查尚未运行完成，另记录；Office未改。
