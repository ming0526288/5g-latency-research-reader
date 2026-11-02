# TEST-361 QUEST手算与全十六位HOL编码核验

2026-10-26，实际cc命令保存在本地analysis-source-audit/quest-reproduction-20261026/unit-01/result.json：-std=c11 -Wall -Wextra -Werror -O1 -g -fsanitize=address,undefined -I新工作树 test_metric_hol.c -lm，编译exit0；ASAN_OPTIONS=detect_leaks=0执行exit0。未测试LSan。

手算P=24/TBS=1200/PDB30ms/HOL10ms，QUEST=225；HOL达到/超过PDB时epsilon给4500000。五个基线、优先级减半/速率加倍、队首等待增加、未知QoS、零HOL、65536合法编码、边界哨兵、1字节/NULL输入拒绝均通过。生产函数直接调用，不从当前脚本另写近似公式充当C验证。

这只是数值和编码复现，不是HOL来源、报文互通、接入、业务或论文性能复现。未启动RAN/抓包/编号UDP，没有算法降幅。C接线后必须重新完整栈验证。实际依据及工程端序、epsilon选择见CHG234/README。
