# TEST-437 每UE SR先导协议缺件与接收核验

2026-10-28，CHG293；资料盘点/接收，不是RAN测试。初始完整盘点使用Python标准输入脚本，递归Path.rglob、ZIP嵌套/CRC、Word document.xml封面内容，而非只看文件名。protocol-inventory-01.json实存：56原始文件、26递归ZIP、64 DOCX原文/包内成员、hits=[]、errors=[]。该长盘点初次调用只取回stdout、未保留session/最终退出码，不能补写exit0；最终JSON已存在并可复核。工作区rg筛选原文无匹配退出1，不是资料损坏/下载失败。

用户补齐后，ZIP预检session75578退出0；CRC通过、唯一成员38473-j40.docx，封面TS38.473 V19.4.0（2026-09）/F1AP/Release19。安全解压session49987退出0，核绝对/父目录路径及符号链接、原始成员字节，不覆盖不同现存文件。读取§8.3.1 Word递归2046–2056、§8.3.4 2248–2257、§9.3.1.26 24325–24345、§9.3.1.45 24926–24941；辅助递归号非官方页码，不宣称全标准/运行时核完。

```bash
cd /home/lbh/oiwireless
/usr/bin/python3 -B analysis-source-audit/sr-per-ue-pilot-20261028/check-receipt.py --output analysis-source-audit/sr-per-ue-pilot-20261028/receipt-check-01.json
```

实际session25690退出0，PASS。ZIP SHA=b3a739825ca588ef8d793032498202a20307751d6109ad603687b8858bd4d60b；Word SHA=cf64dbc0afe72f02a3d2939d78f9c1d0d7658a48166c32e47ae50cfca51ff81a，64702段，CRC/XML/原包成员字节/相关章节可读。未独立认证官网最高版，接收原文不等于F1实现认证。

当前缺件已补齐，按AGENTS“资料齐全不等于自动恢复研究”仍等待用户明确恢复。新分支0、C修改0、构建0、无线实验0，业务/抓包未开始；没有失败业务样本或需要修正的时延数值。原成功/失败数据保留，未触碰原核心，Git取消，Office未改。接续/导航核验receipt-delivery-check-01.json实际PASS：10接续链接、6129源MD SHA、6241导航链接通过，旧C patch身份保持，新C/构建/无线均0，未恢复研究。写入已发生结果后重建导航，并仅补改后来源SHA检查到receipt-delivery-check-02.json，01保留。
