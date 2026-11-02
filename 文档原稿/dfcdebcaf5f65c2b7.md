# 协议原文下载未完成

协议：TS 38.211 V17.2.0。核验日期：2026-10-20。

ETSI原始PDF：https://www.etsi.org/deliver/etsi_ts/138200_138299/138211/17.02.00_60/ts_138211v170200p.pdf
3GPP官方归档：https://www.3gpp.org/ftp/Specs/archive/38_series/38.211/38211-h20.zip

用途与条款：§4.2/4.3.2 时隙与SCS。

当前原始PDF未在本地取得。38.213的相关条款曾通过官方PDF浏览接口读取；其余文件不能据此声称全文已阅读。

失败记录仅说明当前请求结果，不代表站点非公开或协议禁止下载。缺失原文未解决前，涉及尚未核实内容的修改标待核实。

## 2026-10-20 ETSI 请求

命令：`curl --fail --location --max-time 30 https://www.etsi.org/deliver/etsi_ts/138200_138299/138211/17.02.00_60/ts_138211v170200p.pdf -o /home/lbh/oiwireless/3GPP协议原文/TS_38.211_V17.2.0.pdf.download`
退出码：22。

```text
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
curl: (22) The requested URL returned error: 403
```

## 2026-10-20 3GPP 请求

命令：`curl --fail --location --max-time 30 https://www.3gpp.org/ftp/Specs/archive/38_series/38.211/38211-h20.zip -o /home/lbh/oiwireless/3GPP协议原文/38211-h20.zip`
退出码：22。

```text
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
curl: (22) The requested URL returned error: 403
```

后续处理：使用官方源重试，或由用户放入原始PDF/ZIP/Word；检查文件内容与版本，再更新本目录索引。官方Word转PDF必须标注本地转换。
