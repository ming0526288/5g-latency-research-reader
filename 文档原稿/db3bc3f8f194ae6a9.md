# 实施步骤与修改、测试、Git 规范

## 当前已做和下一步

本轮仅P0：从原HEAD建立副本、建立新GitHub原始基线、编写仿真规划和参考清单、验证原件与分支、提交。
下一轮P1：检查依赖/作者代码commit，最小复现；新工作区单独构建RFsim；配独立配置/UE与核心网运行环境，先原样单UE接入。之后P2打点与分层验证。实际命令在检查依赖和相对路径后冻结，不把其他分支的指令照抄成已执行结果。

## 后续RFsim构建候选（尚未执行）

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-latency-analysis/cmake_targets
./build_oai -w SIMU --ninja --gNB --nrUE
```

`--enable-latseq` 只在LatSeq迁移且构建开关被验证后加入。当前原HEAD没有完整LatSeq能力，不能假定命令可用。参考 `latseq-probes-only-120k` 的纯探针改动，与原始代码逐文件比对；不整分支合并RFsim的sl_ahead/线程等变更。

RFsim运行须新配置明确radio backend、频率、PRACH/SSB/BWP、serveraddr；不能把DPDK实机配置直接当作可运行的RFsim配置。需要5GC但不需要实体射频；采用隔离的核心网/命名空间方案，先确认现有进程不受影响。

## 每次修改说明

`records/changes/CHG-编号_主题.md` 至少包含：用户要求；parent commit；修改文件/关键位置；为什么修改、对应时延环节；行为前后；实际运行命令；测试编号/结果；失败/限制；提交信息。每个独立完成部分提交一次。

## 每次测试说明

`records/tests/TEST-编号_主题.md` 至少包含：环境/commit/config、输入、完整命令、预期、退出码、实际输出、原始日志、是否通过、未覆盖内容。失败重试另记编号，并连接原因；不把编译成功等同接入/时延测试成功。

## Git 与身份

基线 `main`/`baseline-120khz` 保留原始代码；开发 `latency-analysis-plan`；已有origin/personal不改写。新remote为`latency-analysis`。提交用命令级身份，不改变原库共享用户配置：

```bash
git -c user.name=ming0526288 -c user.email=1971678626@qq.com commit -m 'docs(latency): describe one completed step'
```

先审查实际diff、明确暂存路径、运行必要校验和写记录，再提交、推送并核对远程SHA。不使用git add .混入构建/数据；不force push基线，不改原文件，不推送敏感认证内容。

本轮验证命令计划：`python3 research/latency-analysis/scripts/validate_plan.py`、`git diff --check`、`git status --short`。脚本只读原目录并核对原件hash/原状态/新源文件差异/文档链接；结果写到records/tests。
