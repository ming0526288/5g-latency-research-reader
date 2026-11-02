# TEST-170 SSB修复完整编译与新输入冻结

2026-10-21，CHG101。已核无活动RAN后，实际ninja -C cmake_targets/ran_build/build nr-softmodem nr-uesoftmodem，escalated宿主ccache权限；session66656最终exit0、6项工作完成，NR_L2_UE对象/静态库及UE链接成功。gNB二进制949993a69c7c0bf3968c0ea8b6c8bb04438e17f0757e1deaf7a9ab9645bcf718仍原值；UE新d0e91df329b3bc3d42500951dab86b448af7280fca78cc20fa1df60d8c5ea5fa。共同UL源150f8ed6efa8b5d2ee8b774b9c3b1e133a10124b3271562c73fe38d62cacc678不变。安全ssb_build_identity.json；不覆盖历史after_build_identity。

实际/usr/bin/python3 -B .../common-policy-rerun/prepare.py --identity .../common-policy-rerun/evidence/ssb_build_identity.json --output .../results/common-policy-rerun-01/plan-03，session11045最终exit0。再次核23ZIP CRC/31 DOCX XML及有关协议/构建SHA，复制22配置，新79短计划+4长流另2条件sanity，187文件冻结，manifest SHA7e248bc5c5796db604b2ae9ad2badd6392a32c4f648fd0359382a6e61cde591f。没有复用旧测量或改负载/样本/超时/CPU/TDD。

准备脚本的--identity和计划/运行目录显式参数仅防止新旧混用，3GPP无此参数要求；业务语义和数学CHG097/101及README。sanity-plan.json仅N1/N8 UL两已失败条件；实际启动命令同README，输出ssb-sanity-runs-01，session56802开始，完整结果另记TEST171。此TEST不把仍进行的RFsim记为已通过。完整五阶段随后另新short-runs-02/tail-runs-02，未运行不得说完成。后续文档整理的一次functions.exec因JavaScript字符串内含Markdown反引号而在执行shell前SyntaxError，未改任何数据或C；改用apply_patch/无反引号脚本。

## 依据与适用边界 2026-10-20补注

本条2026-10-21新增。通信改动依据38.212 V19.4.0 §7.1.1、38.213 V19.5.0 §4.1、38.331 V19.4.0 §6.3.2，P01 III/IV PDF2–4、教材5.5.4 PDF139–140仅辅助，精确范围CHG101。编译/复制/哈希属工程核验，不等同无线/全栈认证。
