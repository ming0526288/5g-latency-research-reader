# TEST-490 磁盘清理与内容一致性核验

2026-10-30，本机/home分区，所有运行命令均在oi-wireless-ran-probe-residual；3GPP/数学推导不适用，属于用户授权的工程清理。安全证明maintenance/evidence，完整本地根 `/home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/`。未新增无线业务实验。

## 实际命令与结果

首次相同暂停命令因只认绝对argv而assert []/exit1，未发信号；修复相对路径解析后运行成功。失败源码副本aux pause-relative-path-failed.py，仅作真实失败证据，不覆盖现方法。

```bash
sudo -n /usr/bin/python3 -B research/latency-analysis/maintenance/pause_for_cleanup.py --record /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/matrix-pause-01.json
```

修正后在24个已运行条件全部PASS且无RAN时记录PAUSED_AT_COMPLETED_BLOCK；UTC03:38:20.327698，仅控制器暂停，未停止原核心。暂停调用的工具退出码未在接续上下文中保留，记为未核定，不按状态文件推造退出码；实际暂停身份/状态与后续恢复已另行核验。已实际读取ccache --help与fallocate --help，分别核对--clear保留配置和--dig-holes检测零块语义。四个新Python文件AST核查通过（非运行性能测试）。

```bash
sudo -n /usr/bin/python3 -B research/latency-analysis/maintenance/clear_disposable.py --record /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/matrix-pause-01.json --output /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/disposable-01.json
```

session20217 exit0。27冻结清单/328714引用及4697进程链接前置核验，通过后顺序执行三个ccache官方清空命令，再对确切Trash根内容使用不跟随symlink的unlink/rmtree。回收16541507584字节；Trash余0文件/3结构目录。三个缓存分别余21610496/1343488/1441792物理字节，保留配置等官方命令剩余内容；不声称缓存目录字面空无一物。仅合计计数/体积写证明，无回收站私人文件名。

```bash
sudo -n /usr/bin/python3 -B research/latency-analysis/maintenance/sparsify_closed_traces.py --record /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/matrix-pause-01.json --output /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/sparse-closed-01.json
```

session34715 exit0，PASS_BYTE_IDENTICAL；1650候选中处理939文件，逐文件fallocate --dig-holes退出0、完整哈希/长度/inode相同，逻辑共78701980352字节。回收68759064576字节达到事先64 GiB限额即停，不强制处理剩余候选。27清单22472唯一冻结路径及所有打开文件排除。三旧root runtime均complete_plan=true、原核心保持、已结束；当前main-02整个排除。

```bash
sudo -n /usr/bin/python3 -B research/latency-analysis/maintenance/verify_cleanup.py --record /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/matrix-pause-01.json --output /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/identities-after-01.json
```

session14898 exit0，PASS；19050当前冻结文件完整SHA256保持，manifest SHA256=9349dc03e3eaeaabfaf801459c172b362ab166c86d37fbf925a91669016c2f82。原四核心身份/镜像/启动/运行状态保持、无RAN、控制器仍暂停且24条件PASS。此时可用220152217600字节。

```bash
sudo -n /usr/bin/python3 -B research/latency-analysis/maintenance/pause_for_cleanup.py --record /home/lbh/oiwireless/analysis-source-audit/disk-cleanup-20261030/matrix-pause-01.json --resume
```

exit0，RESUMED，UTC03:46:00.318477；PID1569899/启动tick32854461相同，暂停459.990602s。原root62812输出STATE_START l8-s3-forward-residual-f1，execution已第25条件gNB_UE_UL，证明恢复推进；尚未72结束，无本轮最终独立或性能结论。

## 结果与边界

合计物理空间回收85300572160字节=79.442348 GiB，约15.405479 GiB删除缓存/回收站＋64.036869 GiB已有零块回收。939原轨迹全部逻辑数据保留；当前源/无线/业务/超时/完整性门禁未变。文件系统free前后差会有后台写入，不用其微差替代逐范围回收数；此数字不含之前CHG338的回收。

没有删除原始代码、研究分支、标准/教材/英文论文、Office/备份、失败日志或慢包。普通用户初盘点读root-owned状态目录失败，不宣称全盘所有文件都判明用途。维护期间无业务，主机热状态/页缓存影响未单独测量；原四小时预算未停止。维护记录需随正式main-02报告保留，不能叫时延优化收益。后续正式72及独立全量核验仍未完成。

交付工程核验exit0：4个新Python AST通过，4原证明与aux逐字节/哈希一致，独立复加回收85300572160字节，939完整哈希证明相同，CHG/TEST两树一致，docs23链接存在，START/CURRENT旧暂停首段已替换为已恢复。证明maintenance/evidence/delivery-check-01.json。本次未在业务期间重新读全部大轨迹，不把工程交付称为72正式通过。

Git前置检查实际exit0：两树git diff --cached --check通过；active白名单15文件约562350字节，主树白名单6文件，均仅MD/Python/安全JSON，无原始数据/协议/Office/凭据。仅提交本次清理相关路径，保留既有无关工作区改动。实际commit/push和远程一致性以本地aux git-sync-cleanup-01.json为准。
