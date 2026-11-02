# CHG-257 运行器使用冻结RAN目录作为工作目录

2026-10-27。TEST383证实独立核心可启动/N4可关联；RAN创建前因cwd不存在失败。prepare_trial.py只将生成运行器的BUILD（子进程工作目录）指向既有冻结runtime，仍用原冻结ELF/模块和显式LD_LIBRARY_PATH，不新编译、不改C/空口/调度/样本。路径工程修正，3GPP/数学推导不适用；通信依据见CHG254及变更依据与验证路径.md，16原文可读无缺件。

另建trial-08，不覆盖trial-07；实际命令和结果TEST384。Git取消。
