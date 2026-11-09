# 论文中文 PDF 生成与接续

这是阅读站工程，不启动通信研究/核心网/RAN/UE。3GPP/新增数学推导不适用；忠实翻译本地论文，不把作者旧标准陈述改标为新版认证。35篇论文共407页，book为中文5G教材，不处理。已生成初稿按现有网页功能立即可预览，人工页面核对状态另记，不把generated/pending改称通过。

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
