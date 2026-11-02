# TEST-158 上行首UE例外的3GPP原文核查

2026-10-21，CHG095。实际rg --files递归查本地3GPP协议原文，读取38300-j40、38321-j40、38214-j50原始DOCX的ZIP CRC、document.xml、封面版本/SHA和正文/表内递归段落；38331/38213也已找到，但没有虚构为本次改动全部重审。必要原文齐全可读，无下载。

实际定位38.300 V19.4.0 §10.2/10.3，38.321 V19.4.0 §5.4.1/§5.4.4/§5.4.5，38.214 V19.5.0 §6.1.4.1。源SHA/精确段落范围在scheduler-baseline/evidence/protocol_provenance.json。结论：UL需授权不等于每包需先SR，主动动态授权不能仅因标准未点名策略就判违规；标准没有要求首UE固定9或强制首UE每次候选。当前修改属于移除工程位置例外、统一基线，不宣称证明旧所有测试违规。

实际pdftotext提取P01 PDF2–4到/tmp/common-ul-p01.txt；教材530–532与537–539到/tmp/common-ul-book-scheduler.txt及common-ul-book-srbsr.txt，核§13.1.1.2调度/§13.1.1.4/5 SR/BSR。没有用文献替代3GPP，没有采用QUEST/新BSR算法。

实际读pf_ul完整相关路径、nr_UE_is_to_be_scheduled与外部MCS控制，确认旧两项cnt==1和共同inactivity分支；既有comparator等不同时改。原代码备份及旧二进制身份已存，本项未启动业务/抓包、未产生新时延数据；原始oi-wireless-ran不改，旧scs2保留。

## 依据与适用边界 2026-10-20补注

本条2026-10-21新增。准确版本/条款及本地PDF页序如上，CRC/检索/备份为工程核查。共同规则数学和修改函数见CHG095/README；相关原文不是本项目调度算法的逐行实现指南。
