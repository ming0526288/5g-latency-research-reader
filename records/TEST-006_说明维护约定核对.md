# TEST-006 说明维护约定核对

2026-11-02。在阅读站仓库根目录执行以下命令，实际exit0：

```bash
python3 - <<'PY'
from pathlib import Path
root = Path.cwd().parent
paths = [root/'AGENTS.md', root/'oi-wireless-ran-latency-analysis/AGENTS.md']
for path in paths:
    text = path.read_text()
    assert '讲解说明只在' in text and '阅读站`说明/算法知识点说明/`' in text
    assert '阅读站`说明/算法文档/`' in text
    assert '旧说明及既有网页快照保留作历史参考，不删除' in text
    assert '每次交付新说明，必须同时更新阅读站页面、导航与搜索' in text
assert '只写Markdown不算完成' in Path('AGENTS.md').read_text()
assert '尚未接入`说明/`' in Path('AGENTS.md').read_text()
assert '静态网页不会因保存Markdown而自动更新' in Path('README.md').read_text()
print('PASS: canonical reader paths, web delivery requirement and historical retention agree across instructions and README; automatic import is not claimed.')
PY
```

另在阅读站执行`git diff --check`，在研究主仓库执行`git diff --check -- AGENTS.md`，实际均exit0。

结果：工作区/主研究仓库/阅读站规则及README对新说明的保存位置、网页交付要求、历史文件保留一致。人工阅读`tools/build_reader.py`确认现有导出器以原研究工作区为源，本次只约定未来维护位置，未将其误写成已经具备自动导入能力。

只做文档一致性检查，3GPP/新增数学推导不适用。未写入新研究正文、未重新生成网页、未删除旧文件、未启动通信实验或重启服务；没有新增网页或浏览器验收结果。
