# TEST-429 SR三周期原始包与状态独立复算

2026-10-28，CHG289；生产RAN已停止，原始9条件保留。

```bash
cd /home/lbh/oiwireless/oi-wireless-ran-sr-period-mechanism
/usr/bin/python3 -B research/latency-analysis/sr-period-results/verify.py --output /home/lbh/oiwireless/analysis-source-audit/sr-period-mechanism-20261028/independent-check-01.json
```

独立原始sent/received复算APP UL，独立struct读取PDCP/RLC/初传/新状态，核actual period/offset和TDD位置、SR成员一一性、完整队列、E/S/B、逐包W及冻结/前缀身份。不import新graph/Queue作为oracle。实际退出/计数执行后填写；未通过不生成正式收益结论。

实际session60065退出0，independent-check-01.json PASS：27编号队列、121500完整/108000统计UL、1889902新旧决策对、11533999新状态记录、138919个SR链原始成员与一一性；351已填充原始前缀和8331唯一冻结输入一致，九项同ELF/模块。原始收发均值/P99/最大值逐流与27个已测结果吻合，actual period/offset及TDD位置通过。验证器SHA587e54a48cdb239a40b310d164613ebe19ec19b827dd8f665d11a74892286d16。
