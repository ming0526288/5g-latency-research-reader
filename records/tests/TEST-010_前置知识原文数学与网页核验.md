# TEST-010 前置知识：原文、数学与网页核验

2026-11-03。本轮实际做知识解释与网页工程验证，没有RAN/核心网启动、接入、编号业务或pcap采集，不产生新单向时延性能结果。

## 原文资料

在本地递归定位12份所需协议原始DOCX，使用Python `zipfile.ZipFile.testzip()`及`ElementTree`读取`word/document.xml`，记录SHA256和封面版本/日期。实际exit0，12/12可读。辅助JSON和文本存于`analysis-source-audit/reader-prerequisites-20261103/`；可提交摘要在`校验/知识点协议与文献核验.json`，具体实际已读范围见CHG-009。

5份PDF（P01/P02/P19/P24/指定教材）实际`pdfinfo`均exit0，所选页的`pdftotext -layout -f ... -l ...`均exit0。使用`pdftoppm`生成教材PDF78、P01 PDF2的PNG并实际查看；原件及源页未修改。PDF仅做读取，未创建或编辑PDF。

## 构建、公式与原表复核

在阅读站根目录实际执行：

```bash
python3 tools/draw_prerequisites.py
python3 tools/update_knowledge.py
python3 tools/check_prerequisites.py
```

各项实际exit0。构建结果为7页、75个行内/独立公式、8幅SVG，KaTeX错误列表为空。内容核对直接从随站保存且与本地原文同SHA的DOCX读取表格：38.211正常CP七行槽数、38.213格式0/1/2各14符号、38.104的100MHz/60或120kHz对应132/66 PRB、RRC完整槽字段上限320均相符。图中D/F/U和SCS槽数与声明一致；分数算术验证5槽、48/18/4共70符号、发包速率/间隔、9.76ms教学分位数，以及分位数不具可加性的反例。

逐页检查源稿与下载文件是同一文件、SHA一致，表格/公式/图均已生成，所有新增协议条款或检索目标存在于本地协议页。另一次性调用构建前后比较`网页/catalog.js`与7个`k*.js`内容SHA，实际exit0，重构建逐字节一致，页数和计数不累加。

`node -p 'require("./网页/vendor/katex/katex.min.js").version'`实际输出0.16.47。比较随站KaTeX CSS与该本地分发CSS的SHA，两者相同。新加入的引擎文件来自原站使用的本地MIT许可分发，不自行联网安装依赖。

## 实际交互

```bash
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_interactions.cjs
```

最终实际exit0，`jsdomErrors`为空，见`校验/交互逻辑校验.json`。七类入口连接新知识，图片提供独立放大链接；实际点击TDD原文引用后定位到38.213表11.1.1-1；新正文关键词可被搜索找到；旧分式、间距、代码/URL/标题ID、书签、QUEST检索、PDF页码、38.321条款和主题切换继续通过。jsdom不是浏览器排版或真实手机验收。

## 实际视觉检查

使用Firefox `--headless --no-remote --profile ... --screenshot ... --window-size ...`读取本地网页，均实际exit0，截图后实际查看。原始完整命令位置/目标如下，公共前缀为`firefox --headless --no-remote --profile /home/lbh/oiwireless/analysis-source-audit/reader-navigation-20261103/profile`：

- `--screenshot /home/lbh/oiwireless/analysis-source-audit/reader-prerequisites-20261103/tdd-desktop.png --window-size 1440,1200 'file:///home/lbh/oiwireless/5g-latency-research-reader/index.html#/doc/k7be2718894117a09'`：实际应用TDD入口首屏，表图、目录与正文正常。
- `--screenshot /home/lbh/oiwireless/analysis-source-audit/reader-prerequisites-20261103/tdd-mobile.png --window-size 390,1000 'file:///home/lbh/oiwireless/5g-latency-research-reader/index.html#/doc/k7be2718894117a09'`：窄屏响应式检查，有放大入口，不是实体手机/VPN验证。
- `--screenshot /home/lbh/oiwireless/analysis-source-audit/reader-prerequisites-20261103/tdd-math-preview.png --window-size 1000,1350 'file:///home/lbh/oiwireless/analysis-source-audit/reader-prerequisites-20261103/tdd-math-preview.html'`：从实际生成正文截取、使用同站CSS/字体/图片的静态布局核对，TDD计数公式与展开图正常。
- `--screenshot /home/lbh/oiwireless/analysis-source-audit/reader-prerequisites-20261103/scs-math-preview-final.png --window-size 1000,1350 'file:///home/lbh/oiwireless/analysis-source-audit/reader-prerequisites-20261103/scs-math-preview.html'`：修正强调格式后的SCS表格、竖式公式和图正常。

截图、源页渲染、布局预览HTML和独立浏览器配置只保存在仓库外辅助目录，未纳入Git。不声称完成全部长文每一屏、不同实体电脑或手机端的视觉认证。

## 实际问题及修正

1. 初检新增引用发现`38.321?clause=10.2`错误：同一段混列38.300与38.321后，自动条款上下文串到了后者。分列协议出处，重新构建；新增严格断言要求所有新条款/检索目标确实存在，最终通过。没有修改原协议或科研结论。
2. 原TDD锚点CLI截图虽exit0，截图时未稳定捕获目标公式屏；保留`tdd-formulas.png`，不拿它当公式验收证据。改用同一生成正文的静态截段核对，实际应用入口另有桌面/窄屏截图与DOM路由测试。
3. 视觉发现3处中文强调末尾句号导致CommonMark将`**`保留为字面文本。直接修改三篇源稿，增加构建期未解析强调检查；重新构建，最终SCS截图已确认修正。
4. 增加前置知识搜索测试后，旧QUEST检查曾exit1：新输入的防抖更新前读到了上一查询的结果。改为等待结果确实包含QUEST，不改变网站时延或测试阈值；最终exit0。保留本记录与当次工具输出，不把首次失败记成通过。

最后的离线资源/原件哈希、语法与diff检查结果随`校验/离线资源与跳转校验.json`和本地提交保存。用户明确本轮不用先推送，未执行Git push。

最终离线资源核对实际执行`python3 tools/validate_reader.py`，exit0：1184页、9744个文档跳转、10060个文献跳转、6999个协议跳转、3481处页序定位、173处本地资源，错误/警告为空；36份PDF、34份协议Word、26份协议ZIP保持来源哈希。旧571处标题回退、21处协议条款回退保持，新增知识引用均有准确条款/检索目标。最终用VS Code Node执行`--check 网页/app.js`、执行`git diff --check`，均exit0。

另实际只读检查原`oi-wireless-ran/targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb1.sa.band261.fr2.66PRB.5slot.dpdk.conf`的SCS、带宽与TDD字段，确认参考/数据SCS索引3、PRB66、周期索引1、完整槽3/1、部分符号6/4；配置文件未修改或运行。源SHA和最小数字字段记录在上述来源核验JSON，不提交完整配置。源稿最后统一到`说明/算法知识点说明/`，网页ID保持；本文截图为本轮实际渲染内容，其拍摄时工具栏源稿路径可能早于最终目录归并。
