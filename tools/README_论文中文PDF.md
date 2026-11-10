# 论文中文 PDF 生成与接续

这是阅读站工程，不启动通信研究/核心网/RAN/UE。3GPP/新增数学推导不适用；忠实翻译本地论文，不把作者旧标准陈述改标为新版认证。最初 35 篇论文共 407 页；本次补入 P36～P39 后为 39 篇论文、446 页。book 为中文 5G 教材，不处理。已生成初稿按现有网页功能立即可预览，人工页面核对状态另记，不把generated/pending改称通过。

原文在文献/论文/，从网页/catalog.js读取真实身份。译文在阅读转换件/论文中文/Pxx.zh.pdf；说明/paper-translations.json和网页/paper-translations.js为本机运行索引。PDF、运行索引、模型、字体、完整缓存、渲染及被拒稿均不上传Git。其他电脑需要原始论文与阅读转换件目录；只克隆代码不等于附带中文PDF。

```bash
cd /home/lbh/oiwireless/5g-latency-research-reader
python3 tools/setup_paper_translation.py --python /home/lbh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --warmup
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --all --engine babel
# 仅重做指定论文时，先核对当前没有另一个生成器正在写同一文件。
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --only P01 --engine babel --force
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --verify
```

已完成文件不会重复覆盖，--force仅用于明确的单篇修正。实际进度和失败在工作区analysis-source-audit/paper-zh-20261109/CURRENT.md、checks/、failure.json及运行清单，不能仅凭输出目录有文件判断校对完成。P05有局部译文校订映射，属于本地全文辅助资料；复现当前精校稿时同时保留aux/corrections/P05.json，否则只是重新机器翻译。

用户已明确允许图片位置差异，要求全部初稿显示。图片内容/位置比较只记录告警，不再阻止上架；MuPDF枚举的零像素空图片不作为可见图片。仍检查可打开、原页数/页面尺寸、中文正文及未解决公式占位符。已生成的候选可用以下命令直接发布，避免重复翻译；该命令要求已有来源SHA记录匹配，不等于人工校对通过：

```bash
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --publish-existing --only P04
```

`--all`遇单篇文件处理错误会记录实际阶段并继续其他论文，结束时若仍有未发布失败返回非0。文件缺失或损坏时不伪造可阅读入口；继续生成或修复该篇。图片位置偏差可接受，不等于数学符号缺失也可接受。

图片与独立公式按原坐标保留，正文在原文字区域重新换行；不能承诺中英文每行字形完全一致。图内嵌英文与数学变量保留，中文正文为辅助译本。原PDF只读、SHA可核；基于原生文字行识别表格文本区域，表格数字/公式仍需对照原文。科学语义与尾分位数据不得只凭机译当作论文事实。

网页版：文献与材料→选论文，英文原文下方显示中文PDF。上下阅读器独立翻页，中文可一键对齐原文页序，也可独立打开。还未生成的只显示状态，不制造空PDF链接；已有初稿允许先看，不将其冒称人工校对完成。字体沿用现有网页设置，不新增标题字号覆盖。

页面工程检查（需要已有 Node 24 和系统 jsdom，不安装新浏览器）：

```bash
NODE_PATH=/usr/share/nodejs:/home/lbh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules /home/lbh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node tools/check_paper_translations.cjs
python3 -B tools/validate_reader.py
```

DOM检查不等于原生浏览器内嵌PDF渲染。所有内容/公式/版式修正记录CHG/TEST并保留拒绝稿。源码依据为PDFMathTranslate与BabelDOC的相应安装版本和官方代码，不以最新版README冒称当前引擎接口；实际版本见aux/environment.json。


## 新增本地论文、旧格式协议及中文协议

新文件先放工作区 `pdf-英文原版/`，编号不复用。协议原包由用户提供，先核 CRC、原文编号/封面/可读性，再把原件安全解压到 `3GPP协议原文/官方解压原文/`；不下载协议。当前 TS 22.104 的原件是二进制 DOC，不是 DOCX。辅助 DOCX 在目录外 `analysis-source-audit/protocol-word-conversion/<原件SHA>/`，不伪称官方原文。网站仍提供原 DOC 与原 ZIP。

在阅读站根目录依次运行：

```bash
python3 -B tools/update_materials.py
python3 -B tools/build_protocol_pdfs.py --spec 22.104 --jobs 1
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/reflow_22104_cover.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --only P36,P37,P38,P39 --engine babel
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_protocols.py --spec 22.104 --engine babel
```

增量登记不重新导出历史研究正文。可维护的标题/版本定位在 `说明/materials.json`，完整构建和增量登记均读取它。新材料原文/中文默认 95% 显示，其他网页字号不变。中文标题可在资料列表和全站搜索找到。

TS 22.104 的 DOC 转换封面曾发生浮动文字重叠；专用脚本只重排本地 PDF 的第一页，原 DOC/ZIP 不改，其余 104 页渲染像素逐页一致。原问题件保留在目录外辅助目录，PDF 内明确标本地重排；本机缺 Arial，重排封面使用 Liberation Sans 替代，不声称嵌入 Arial。`--force` 重做转换后需再次运行封面脚本，再重新生成相应中文稿。

中文协议输出在 `阅读转换件/协议中文/`，运行索引为本机 `说明/protocol-translations.json` 与 `网页/protocol-translations.js`，与论文索引分开。协议原文转换 PDF 的 SHA 是译稿的输入身份；如果原文转换件更新，旧译稿不再显示成匹配稿。协议正文精确解释仍查原 Word，机译不构成官方中文版或标准合规结论。原件、PDF、完整原文检索载荷与运行索引不新增上传 Git；源码、安全元数据、核验与 CHG/TEST 提交。


## 公式缺字/行内分式检查

用户报告P39的E[·]方括号丢失后，定位了实际安装BabelDOC0.2.33的Form字体作用域、数学片段拆分、原水平线和CFF普通连字问题。原英文不改，兼容层在 tools/babel_math_guard.py；当前受保护公式的scope不可解时阻止发布。数学字体按原件保留，不用普通文字字体猜造数学符号。新稿仍pending，字体/字形检查不等于逐句语义审定或重新证明作者定理。

```bash
cd /home/lbh/oiwireless/5g-latency-research-reader
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/check_math_guard.py
# 独立候选，不同时写网站运行索引：
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/repair_paper_math.py --candidate P39
# 先确认没有另一个论文生成器，再按篇生成/备份/限时：
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/repair_paper_math.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/audit_math_pdfs.py --render
```

最终逐篇方法既核源/译SHA与页尺寸，也核最终PDF实际的数学字形字体/位置，而非仅数全文括号。生成器源/译SHA绑定、坐标和原笔画证据在本地aux/paper-zh-20261109/math-guards，原PDF和候选/被拒稿不Git；安全逐篇汇总在校验/论文数学排版逐篇核验.json。600秒是单篇文档生成超时，不是无线时延阈值；超时/失败不能删掉冒充检查通过。数学知识说明已补“通信与时延基础”的E[·]章节，链接P39原文PDF第2页。

先读 records/接续_论文公式核查.md、CHG-019/TEST-020 确定是否已有批次在运行，勿重复启动。39篇完成必须同时有最终生成PASS和逐篇物理核验PASS，不以原先14篇/中间scope批次替代。

本轮最终39篇核查说明在 `说明/文献导读/论文译稿公式核查与修复说明.md`（文献导读可达、搜索“公式核查”）。P10重做用 `--only P10 --force --repair-math --repair-layouts`；P29扫描版重影与原推导页处理随正式生成流程执行。P14/P17/P18/P28/P30/P37仍有已列局部版式问题，不能标全文ready。检查入口另有check_math_trace_fonts.py、check_math_layout.py、check_scan_math.py、check_math_live.py、check_math_report.cjs。后两者分别核最终HTTP字节与网页导航/搜索。
