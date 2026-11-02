# TEST-489 v4完整七十二计划冻结与启动核验

实际prepare命令（active树，session51970 exit0）：
```bash
taskset -c 2 /usr/bin/python3 -B research/latency-analysis/probe-load-v4/prepare.py --matrix main --output /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/main-02
```
实际输出PREPARED_NOT_RUN/72/19050。独立taskset -c2 Python计划核验exit0，safe main02-plan-check-01.json：全笛卡尔72；每行除corrected_config/binary_directory/build_identity_file三个新root路径外与旧预声明main-01逐字段相同；相同顺序和到达seed；69位置各2seed、同十运行文件、同新先导runner；冻结列表19050路径唯一。没有继承旧成功子集或改门槛。

实际root启动（session62812，写本文时运行中，尚无退出码）：
```bash
sudo -n /usr/bin/python3 -B research/latency-analysis/probe-load-v4/run.py /home/lbh/oiwireless/analysis-source-audit/probe-load-20261029/main-02
```
此时972000/864000/216流是计划，不是已测成果。后续需实际72、独立字节/状态/SR/成本/预算/策略/环境/汇总/交付/附加到达审核；尚未运行完成不填PASS。业务上行单向、非RTT；所有异常和失败保持。具体源与数学/窗口冻结v4/README，工程采集CHG339，原C/原核心不改。磁盘新轮前约175GiB，每新条件20GiB保留检查原样；不删原证据。Office未改。

交付工程核验actual exit0：42个当前README/docs22/11号导引链接存在，CHG341/342与TEST488/489两树字节相同；两树暂存diff --cached --check通过。原始业务目录/pcap/ELF/协议/Office未暂存，旧草稿不混入；这是导航一致性，不是72正式或新时延结论通过。
