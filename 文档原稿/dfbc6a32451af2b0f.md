# TEST-382 修正快照导入后独立QoS端到端实验

2026-10-27。前一trial-05业务前失败，见TEST381，不复用为成功数据。

本轮执行入口：
```bash
/usr/bin/python3 -B research/latency-analysis/quest-qos-identity/prepare_trial.py /home/lbh/oiwireless/analysis-source-audit/quest-heterogeneous-20261026/trial-06
sudo -n /usr/bin/python3 -B /home/lbh/oiwireless/oi-wireless-ran-quest-qos-identity/research/latency-analysis/quest-qos-identity/run_trial.py /home/lbh/oiwireless/analysis-source-audit/quest-heterogeneous-20261026/trial-06
```

协议/论文/教材依据CHG254/255。只修数据库克隆导入，不改RAN/算法/业务预算。准备/运行结果待实际填入，不预判PASS。原始凭据、SQL、日志、抓包仅本地；Git取消。

## 实际结果：FAIL，TCP root认证未通过

准备exit0，实际运行exit1。UTC05:31:25.826017–05:33:07.953075，102.13秒。数据库本身完成初始化并监听3306；最后客户端错误1045，root@127.0.0.1认证拒绝。移除0600挂载后Permission denied已消除，但新增的TCP就绪检测与原库常用socket维护方式不同；尚未证明TCP拒绝的更深账户匹配原因。原库只读快照成功及SELECT表名成功；未输出密码。

execution=[]，核心其他NF/gNB/UE/抓包/业务均未启动；runtime changed_inputs=[]、original_core_unchanged=true。失败完整保留trial-06，私有容器/网络已回收。不是无线/QoS性能失败，不算时延样本。下一轮需在确认init完成后用原已验证socket维护方式导入，另建trial-07。
