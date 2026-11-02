# TEST-417 UL只读状态观测完整构建

2026-10-28，CHG281/282，新工作树oi-wireless-ran-ul-state-observation。

```bash
cmake -S . -B cmake_targets/ran_build/build -G Ninja -DOAI_SIMU=ON -DAVX512=OFF -DAVX2=ON -DENABLE_TESTS=OFF -DE2_AGENT=OFF -DCCACHE_ACTIVE=OFF
cmake --build cmake_targets/ran_build/build --target nr-softmodem nr-uesoftmodem -j 6
```

首次配置session96787退出0；首次完整构建session36721退出0，11036步骤，UTC04:47:37.478213至04:50:04.303611，146.825秒。日志analysis-source-audit/ul-state-observation-20261028/build-01.log/json。两个真实ELF均链接完成，没有用编译头夹具冒称完整栈通过。

之后为跨流严格epoch对齐补UE TB对象锚点（CHG282），需同一命令增量构建；最终先导只能用补锚点后身份，不能把首次ELF当最终版本。增量实际结果另记于下方。构建只写新树及辅助日志，旧构建/旧运行根不改，没有启动核心/业务。

增量session47980退出0，UTC04:55:50.453214至04:55:55.038081，4.585秒，build-02.log/json。本次两个最终softmodem均重新链接，先导prepare从新树复制这两个ELF；8个未改共享模块另核旧冻结SHA。源码diff --check退出0。没有用旧运行ELF替换新构建成果。
