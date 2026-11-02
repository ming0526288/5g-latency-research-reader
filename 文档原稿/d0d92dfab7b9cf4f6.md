# TEST-137 搜索空间发布与维持语义C检查

2026-10-21，CHG-088。实际运行check_publication.py，C编译使用已构建的NR_SearchSpace/NR_PDCCH_Config类型和libasn1_nr_rrc.a，真实提取modlist_ss/configure_ss_coreset函数体，不把Python模型当OAI C执行。观察边界是ASN_SEQUENCE_ADD完成之时，尚未代表实际RFsim线程频率或历史现场的唯一根因。

## 实际命令与失败

以下均在研究仓库执行，脚本前缀`python3 research/latency-analysis/stability/check_publication.py --output`：

- `research/latency-analysis/results/stability-01/publication-before`：编译0，执行1。LSan报告任务宿主ptrace环境不支持线程枚举，未得到发布检查结果。
- `.../publication-before-unrestricted`：按权限要求沙箱外重试，编译0、执行1，同一LSan环境限制。
- 诊断脚本显式保留ASan/UBSan，设置子进程`ASAN_OPTIONS=detect_leaks=0`并在receipt注明不提供泄漏认证。
- `.../publication-before-address`：编译0、执行3（预期检测到旧缺陷）；published=2、unready_at_publication=2，更新保留与释放语义通过。
- 修改后`.../publication-after-address`：编译0、执行0；published=2、unready_at_publication=0，更新省略周期时保留原指针和sl5偏移2，添加后原条目保持，释放指定ID通过；没有ASan/UBSan错误。

每个子目录保存receipt.json、生成C、build.log、run.log；不上传原始生成/二进制。stability/check_publication.py及安全汇总可Git。harness没有模拟无线链路，不提供应用业务时延，不使用消息内容或凭据。链路完整性另见TEST-139。

## 依据与适用边界 2026-10-20补注

本条2026-10-21新增。TS38.331 V19.4.0 §6.1.2表6.1.2-1及§6.3.2 SearchSpace Cond Setup/Setup4，TS38.213 V19.5.0 §10.1；实际原文锚点和SHA见stability/protocol_provenance.json。P01 §III/IV PDF2–4与教材§2.3.2 PDF49–52仅辅助层界。发布边界检查、sanitizer和互斥锁是工程验证，不是标准规定测试；不新增时延公式。
