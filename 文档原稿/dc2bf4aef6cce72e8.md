# TEST-374 核心QoS源码与部署二进制只读审计

2026-10-26。实际内联Python重核14份当前相关本地DOCX的SHA/ZipFile.testzip/XML exit0，读取23.503 §6.1.3.2.4及23.501/24.501相关原文；38.413实际表格QFI基准范围INTEGER(0..63, …)，不能把69/84直接作为当前6bit字段值。尚未新接入/业务/抓包，没有新时延值。

实际docker cp oiwireless-smf:/oiwireless-smf/smf到analysis-source-audit/quest-heterogeneous-20261026/deployed-smf.bin exit0；file/readelf/nm/strings/gdb -batch -nx并关闭auto-load/debuginfod，只读离线ELF，不attach或执行程序。gdb日志static-01/02/03保存本地，确认NAS函数写固定9及单参数；源路径含厂商openxg，banner090579d4和BuildID记录source-audit。原核心镜像/配置未改。

官方GitLab ls-remote v1.5.2 TLS失败exit128；转官方GitHub只读标签查询exit0但无v1.5.2标签，完整标签列表对应v1.5.1=090579d41b6e0950d844b78ff90adf05a11bd4d9。实际git clone --depth1 --branch v1.5.1官方SMF仓库exit0，公共源码依赖从官方镜像clone后checkout原gitlink db83907f0edcfcb4a9b189decedfd00fa01f98aa exit0。nghttp2固定v1.43.0/fb0bd22979711c89d92d98ac5db57ebc6f4fd148用于独立构建依赖，尚未编译。不下载任何3GPP原包。

曾有只读路径探查命中不存在的文件/工具头，按rg实际清单定位；不是代码测试/无线失败。宿主缺JSON/spdlog等开发头，运行SMF容器也没有编译工具，故计划独立构建镜像，尚未宿主安装或替换容器。没有用上游相同banner认证整个厂商程序；未核路径仍需后续实际信令验证。

用户中断后只读/proc相关进程名为空，无遗留git/编译/RAN进程；新工作树创建成功且初始clean。核心镜像只读检查不构成启动实验，旧数据不作废。后续生产修改/测试各自记录。
