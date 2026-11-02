# TEST-008 算法单行导航与列表核对

2026-11-02。工程核验，3GPP/新增数学推导不适用。

在阅读站仓库根目录执行：

```bash
/home/lbh/.vscode-server/cli/servers/Stable-2c33b50b16c472efe58357d1d2a8a5414bc23fbf/server/node --check 网页/app.js
```

实际exit0。随后实际执行：

```bash
firefox --headless --no-remote --profile /home/lbh/oiwireless/analysis-source-audit/reader-typography-20261102/profile --screenshot /home/lbh/oiwireless/analysis-source-audit/reader-typography-20261102/algorithms-sidebar.png --window-size 1440,1100 'file:///home/lbh/oiwireless/5g-latency-research-reader/index.html#/browse/algorithms'
```

实际exit0，并查看生成截图。左侧为单行“算法实现与结果”及9的数量徽标，没有展开列表；该分类高亮，右侧正常显示算法说明、筛选框及9篇文档。截图及临时浏览器配置仅本地辅助目录，不提交Git。

另实际执行以下命令核对数量，exit0，输出9：

```bash
python3 - <<'PY'
import json
from pathlib import Path
s=Path('网页/catalog.js').read_text()
c=json.loads(s.split('window.READER_CATALOG=',1)[1].rstrip(';'))
print('算法分类文档数：',sum(d['group']=='algorithms' for d in c['docs']))
PY
```

实际执行`git diff --check`，exit0。此次直接打开算法分类路由并视觉核对，未声称完成手机端或所有文档浏览验收；未新增测试程序或重跑无线实验。
