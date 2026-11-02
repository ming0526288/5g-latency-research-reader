# TEST-003 启动常驻与自动恢复

2026-11-02。只核阅读站静态HTTP/用户服务，3GPP/新增数学推导不适用，没有无线业务或抓包。

实际执行`python3 -m py_compile 启动阅读站.py`及`python3 tools/check_launcher.py`。后者核入口HTTP200且字节等于index、重复执行复用、SIGINT正常exit0、不相关端口占用时换后续端口且不影响原测试服务，最终exit0。首次测试程序以select配合TextIO.readline读取多行就绪输出，因文本预读缓冲而误报未打印地址，exit1；改为读取原始pipe后按行解析，重新完整执行通过，测试进程均回收。没有改业务阈值。

实际用`/usr/bin/python3 常驻阅读站.py --no-open`安装服务。首轮exit1，systemd将带引号的WorkingDirectory值当作非绝对路径并拒绝加载；纠正该指令为原始绝对路径，ExecStart继续使用自身支持的参数引号，重跑exit0。实际`loginctl enable-linger lbh`exit0。临时HTTP进程2132136是本会话启动，已用SIGINT停止并回收，原有研究进程未动。

`/usr/bin/python3 tools/check_persistent.py`实际exit0：active、enabled、linger=yes；在确认MainPID命令行为本站启动脚本且含--service后，对该PID2143778发送一次SIGTERM，systemd自动恢复为2146320，8765重新HTTP200且入口字节保持。摘要为`校验/常驻与自动恢复校验.json`。`常驻阅读站.py status`随后实际显示active/running/enabled。未强制终止其他程序。

启动绑定、读取bus和curl在工具沙箱内曾分别报EPERM/不可连接，按要求提升执行权限后成功，不绕过环境权限。所有实际服务只监听127.0.0.1，不暴露到局域网或互联网。

没有调用自动打开浏览器分支；已核实本地CLI接受openExternal，但Windows浏览器/隧道打开的实际UI结果由用户在VS Code终端运行命令后确认。Windows批处理未在Windows实机测试。此前全站资源/DOM通过结果沿用，没有为此次启动器修改重复无线或全站内容测试。
