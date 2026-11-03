# TEST-017 手机再缩小一档显示核验

2026-11-03，CHG-016。实际复用Firefox/Marionette核验逻辑，临时脚本位于 `analysis-source-audit/reader-phone-type-small-20261103/browser_check.py`，仅连接本机2833端口，退出0，8组检查/8张截图。

实际computed style：1440px桌面正文18px、导航/卡片16px、表格16px保持；桌面两倍根文字为正文36px、导航32px，阅读宽度检查通过。500px实际窄内容和同源320px iframe中，正文15px、导航/卡片说明14px、表格14px，无整体横向溢出；菜单和公式排版保持。检查了知识正文窄屏截图。Firefox正常退出。

摘要 `校验/手机字号再收小浏览器核验.json`。外窗请求390px仍实际500px，320px为真实页面iframe媒体查询，不冒称实体手机/VPN或全站WCAG认证；截图和脚本只本地保存。

最终 `python3 tools/validate_reader.py`与`git diff --check`核验；更改限手机样式和维护/校验记录，既有研究源稿、catalog、payload、图及资料未改，不启动通信实验。保留前轮TEST-016证据，不覆盖其旧字号身份。暂不推送。

实际离线校验退出0、PASS，1189文档及全部既有资源/路由保持，无新增错误；diff检查通过。
