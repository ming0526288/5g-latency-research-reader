# TEST-425 SR字段构造与真实ASN编码核验

2026-10-28，CHG286。本步协议预检25DOCX SHA/CRC/XML、论文/教材可读，无所需缺件；实际条款/教材页序和本地论文版别见CHG286。最初在工作树相对搜索pdf-英文原版路径不存在退出2，改为用户工作区绝对目录找到35篇，非资料缺失；没有下载。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-sr-period-mechanism
/usr/bin/python3 -B research/latency-analysis/sr-period-mechanism/selftest.py --output /home/lbh/oiwireless/analysis-source-audit/sr-period-mechanism-20261028/tests-01
```

抽取生产新/旧set_SR_periodandoffset、真实get_first_ul_slot/get_nb_periods_per_frame和共享find_period_offset_SR，使用既有实际ASN.1头/静态库做编码、约束与UE侧解码同类型回环。180组默认输出等价仅验证代码保持，不认证任意组合物理可用；实际点显式40编码须与旧default完全相同，20/10编码后能恢复period/offset及不变resource/ID。

非法值/错误工作点必须拒绝，不放宽到其他SCS/TDD；结果按实际执行后记录。此时尚未运行核心/gNB/UE业务，不能用字段存在冒称完整链路可行或性能收益。

实际tests-01退出0：180组新旧默认输出一致，3个实际UPER回环通过、显式40与原默认逐字节一致，5个非法值与1个错误SCS工作点拒绝；UBSan无错误。使用原构建的真实ASN库仅作序列化夹具，新运行ELF仍须本树完整构建，不混作旧程序性能。
