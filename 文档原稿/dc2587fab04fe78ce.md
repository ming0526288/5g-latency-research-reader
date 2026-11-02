# TEST-377 停止前隔离SMF构建与帮助加载记录

此文是2026-10-26停止前已经执行的历史记录；用户暂停后未继续测试。完整实际命令、路径、失败见quest-qos-identity/构建命令与停止位置.md，安全SHA见evidence/smf-build-01.json。

- `docker build --progress=plain ...` exit125；builder-01/02两次APT依赖失败exit100，原因为继承失效代理、可用源缺Pistache包。未在宿主安装新库。builder-03按准确原构建脚本Pistache源码，exit0，新镜像SHA708a7a73aeef...。
- `prepare_build.py .../OAI-SMF-v1.5.1 .../smf-build-01` exit0，2108输入。`docker run --rm --network none --user1000:1000 ... build_smf.sh` exit0，1012/1012链接SMF，Release；完整源码输入事后SHA核对exit0/2108一致。完整SMF不冒称ASan构建，NAS独立ASan/UBSan/LSan见TEST375。
- 第一次`smf --help`只挂ELF，exit1。只读ldd/readelf定位运行时错误加载原镜像旧libNAS.so，引入ASan。第二次同挂新build/nas，`--help` exit0，Usage可读，未启动任何网络服务。
- 只读原容器inspect确认当时原SMF仍原镜像、AMF running、网络及挂载未改；不等同新功能通过。用户停止后复查命令中断，不虚构新的健康检查。

测到哪里：仅新SMF构建/依赖/帮助。新SMF配置加载、N4、N1/N2实际信令、UE接入/DRB映射、业务/抓包均未测；没有新增UL/DL时延或P99。未操作原核心网重启/替换、数据库、配置。此时按用户要求暂停测试，只做既有资料分析。
