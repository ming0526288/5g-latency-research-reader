# TEST-001 离线阅读站核验

2026-11-02。非通信工程核验，**3GPP/新增数学推导不适用**，没有启动gNB、UE、业务或抓包。

## 实际命令

在阅读仓库执行：

```bash
python3 tools/build_reader.py --workspace /home/lbh/oiwireless
python3 tools/validate_reader.py
NODE_PATH=/usr/share/nodejs /home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node tools/check_interactions.cjs
/home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node --check 网页/app.js
```

Python为当前环境的3.14，已安装markdown-it-py；PDF页数由本地Poppler读取。数学排版使用本地Node24与KaTeX。以上依赖只用于生成/核验，普通阅读和克隆后使用不需要它们。

## 结果与失败

首轮构建在已完成PDF/Word复制、协议视图、1175篇MD和数学渲染后，写JSON摘要时因PosixPath未转字符串而exit1。修正诊断字段后重跑exit0；失败见`校验/构建失败-01.json`。最初调用通用`node`运行Sites辅助脚本时，系统旧Node不能解析可选链，改用现有Node24；最终按用户要求交付独立Git离线站，未发布Sites，也未向Sites传输研究资料。

资源校验实际通过：检查每篇payload存在、文档路由、PDF页码范围、论文/Word/原ZIP哈希、本地图片和CSS资源、公式无占位符残留、基础示例确为分式、敏感模式扫描、单文件不超过GitHub100MiB。细目以`校验/离线资源与跳转校验.json`为准。旧原文标题锚点和少数历史条款不能精确匹配时有目录/关键词回退，不冒称全部旧引用已独立校正。

交互检查使用实际入口文件、`catalog.js`、应用脚本和按需阅读页，在jsdom DOM中运行：首页六步、基础分式/示意图、书签、全文搜索、P24第7/9页地址控件、从PDF切换至38.321并定位5.4.5、主题切换均通过。首次测试未将Debian模块目录加入NODE_PATH而缺tough-cookie；补充现有模块查找路径后可运行，没有安装新依赖。最初将PDF当作HTML iframe交给jsdom时，后续脚本队列未完成；通过对照定位到测试替身，改为明确不加载PDF iframe，仅检查实际src和页码，再按原顺序通过。失败/跟进保留在`校验/交互失败-01.json`。

## 尚未核验

`cua.getState()`返回无浏览器，`createBrowserTab(iab,...)`返回Browser is not available。因此**没有完成真实浏览器版式、原生PDF显示或另一台电脑实机验收**，不能将DOM测试写成浏览器截图验收。当前仅声称结构、资源、哈希、公式生成和上述DOM交互通过。PDF iframe、`file://`本地存储、复杂Word公式/矢量图等边界在README中说明。

远程推送、全新克隆及文件清单核验在发生后另记Git验证结果；未发生不写通过。
