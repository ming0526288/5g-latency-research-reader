# TEST-101 内部观测器编译与原始二进制保护

实际用shutil.copy2备份nr-softmodem/nr-uesoftmodem到results/layered/baseline-binaries，逐字节与原文件一致，记录SHA256/字节数manifest。原始仓库不改。改动前ninja -n仅列出2个LDPC生成及VCD检查，没有通信编译错误。

实际首编译命令：ninja -C cmake_targets/ran_build/build -j 4 nr-softmodem nr-uesoftmodem，日志results/layered/build-01.log，退出1。ccache无法创建/run/user/1000/ccache-tmp（沙盒只读），失败在C对象编译之前，无新无线实验、无业务/抓包。按工具规则请求沙盒外执行相同编译，日志build-02.log，build-02实际退出0，15步骤完成，两个可执行文件链接成功，编译日志保留。不是协议/PHY初始化失败，不删除失败日志。

观测器依据已实际读本地38.323 V19.1.0 §5.2、38.322 V19.3.0 §4.2/5.2、37.324 V19.0.0 §5.2，详见CHG-065。新增开销必须对照，不在编译阶段写性能通过。

## 依据与适用边界 2026-10-20补注

依据编号：S05 §6.2–6.6；S08 38.322 V19.3.0 §4.2/5.2；S09 38.323 V19.1.0 §5.2；S10 37.324 V19.0.0 §5.2；S11 29.281 V19.2.0 §4.2.1；P01 III/IV PDF2–4；B04 PDF49–52；E01/E02/E03/M01。第四阶段只读事件观测，指定本地协议版本，软件队列/混合区间与标准层分开，未改协议字节/调度。 用户明确按已下载原文版本继续，不称官网最高版；先查本地，缺件立即停止，禁止自行下载。详细条款/原文哈希和测量假设见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)及layered/source_provenance.json。
