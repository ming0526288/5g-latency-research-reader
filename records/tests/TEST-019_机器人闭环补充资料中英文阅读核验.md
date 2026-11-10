# TEST-019 机器人闭环补充资料中英文阅读核验

2026-11-10。网页/PDF 工程；不是新无线实验或科学语义认证。无核心网/gNB/UE/业务/抓包。

## 已实际执行

```bash
cd /home/lbh/oiwireless/5g-latency-research-reader
python3 -B tools/update_materials.py
python3 -B tools/build_protocol_pdfs.py --spec 22.104 --jobs 1
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/reflow_22104_cover.py
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_papers.py --only P36,P37,P38,P39 --engine babel
/home/lbh/oiwireless/analysis-source-audit/paper-zh-20261109/venv/bin/python tools/translate_protocols.py --spec 22.104 --engine babel
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_protocol_pdfs.cjs
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_paper_translations.cjs
python3 -B tools/validate_reader.py
```

增量登记首次 exit0 新增 P36～P39 和 22.104；再次运行 exit0，无重复条目。目录含 39 论文＋1 教材、35 协议分册/25 编号。PDF 转换 exit0，105 页、观察到 50 个数字条款标题页映射；未找到的条款不猜页。封面重排 exit0，页数保持105，其他104页渲染像素一致。源码 Python AST 与 app.js 的 Node --check 实际通过。

四论文翻译整体命令 exit0：P36 117.21s/13页/14009汉字，P37 56.88s/4页/3476汉字，P38 141.69s/16页/16816汉字，P39 92.14s/6页/4882汉字。共39页。页数/页面尺寸、文件SHA及生成后可读性检查通过；全部39页以0.9倍渲染、四张接触图已实际查看，另细看P36第1、P37第3、P38第9页，未做逐句翻译/公式等价审定，generated/pending 保持。图内英文和作者专名可能保留/音译，不构成官方中文版。

协议中文105页仍生成中，暂不能写完成，后续结果补在下方。真实工具会话62051；进程只读检查确认仍运行，不启动重复生成器。

现有论文上下阅读器回归 exit0：14/39篇实际有中文，其中包含这次4篇；其余旧未完成项不冒称已生成。协议阅读器回归 exit0，35/35来源匹配PDF，49页架构图、翻页/边界、多分册、版本提示、检索返回通过。整站 validator exit0：1191文档、40原PDF、35协议分册、27原包检查，无错误。验证器元数据中旧字体QA描述沿历史，不冒称本轮重做那些截图。

## 失败与限制保留

- 最初 LibreOffice 沙箱文本读取 exit1，dconf 只读文件系统；按工具要求提升重试 exit0。非缺协议，未下载。
- DOC 转 PDF 最初封面浮动文字重叠，已保存问题图及原问题PDF，再重排本地阅读封面；原DOC/ZIP不改。转换DOCX时有PNG zTXt CRC警告，ZIP CRC/XML与原文可读，未据警告捏造原件缺失；图像细节仍应查原Word。
- 字体子集模块报缺post表、P38专名无点i字形警告、P39科学计数内容流警告：引擎最终exit0、实际输出可打开且全部页可渲染。记录不删除，不由此声称语义/公式无误。
- Firefox首次exit1，独立profile目录不存在；创建目录后重试exit0。1440×3800截图实际看见P36网站原文95%与资料/协议数量；中文框在该截图下方，不能把它写成两个原生PDF框均视觉核验。
- 原有101输入（39论文及协议ZIP/已解压原文等）SHA复核保持。新增原DOC与原包成员逐字节一致；辅助文档、译稿、完整日志/缓存/截图和全文检索载荷只在本地，不上传Git。

本地证据根：`/home/lbh/oiwireless/analysis-source-audit/robotics-reader-20261110/`；安全元数据 `校验/机器人闭环补充资料来源.json`。只读测试/准备脚本中曾有两个记账错误（空上下文候选补丁、把pagesRendered误写为pages），均exit1且未触及Git索引；已纠正后实际执行成功，不是研究或翻译失败。

补充：`python3 -B tools/check_protocol_pdf_live.py` 沙箱首次 exit1（socket EPERM），按工具要求提升后同命令 exit0，实际本机 HTTP 38 项资源（3 JS＋35 PDF HEAD）均正常；未验证用户 VPN/手机客户端。

## 最终收尾

待协议译稿实际完成后填写最终功能检查、HTTP资源、Git提交/推送状态。
