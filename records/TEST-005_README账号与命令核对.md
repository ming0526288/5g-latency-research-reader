# TEST-005 README账号与命令核对

2026-11-02。在阅读站仓库根目录执行以下命令，实际exit0：

```bash
python3 - <<'PY'
import ast
import json
from pathlib import Path
import re
import subprocess
import sys

readme = Path('README.md').read_text()
examples = re.findall(r'```json\n(.*?)\n```', readme, re.S)
assert len(examples) == 1
example = json.loads(examples[0])
module = ast.parse(Path('常驻阅读站.py').read_text())
parser = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == 'login_users')
namespace = {}
exec(compile(ast.Module(body=[parser], type_ignores=[]), '常驻阅读站.py', 'exec'), namespace)
assert len(namespace['login_users'](example)) == 2
commands = re.findall(r'^python3 (.+)$', readme, re.M)
assert commands
for command in commands:
    script = command.split()[0]
    assert not Path(script).is_absolute(), command
    assert Path(script).is_file(), command
assert '--workspace /' not in readme
assert '/home/lbh/oiwireless/' not in readme
for script in ['常驻阅读站.py', '启动阅读站.py']:
    result = subprocess.run([sys.executable, script, '--help'], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert '--no-open' in result.stdout
print('PASS: README JSON accepted (2 users); Python script paths relative and present; --no-open documented by both launchers.')
print('No live account files read or changed; no service restarted.')
PY
```

结果：README双用户JSON格式合法，并被实际`login_users`函数接受；所有独立Python命令的脚本路径均相对且文件存在；两个启动器的帮助均声明`--no-open`。另执行`git diff --check`，实际exit0，无空白错误。

人工对照`ensure_access`与`main`确认说明中的配置同步、按需重启及保留监听设置行为。本次没有读取实际账号、修改私有配置或重启服务；未进行浏览器、手机或客户端VPN测试。3GPP/新增数学推导不适用，无新通信实验。
