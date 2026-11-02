#!/usr/bin/env python3
"""Manage the current user's persistent, loopback-only static reader service."""
import argparse
import getpass
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
NAME='5g-latency-reader.service'
MARKER='# Managed by 5g-latency-research-reader/常驻阅读站.py'

def run(args,check=True):
    return subprocess.run(args,text=True,capture_output=True,check=check,timeout=25)
def unit_quote(value):
    value=str(value)
    if '\n' in value or '\r' in value:raise ValueError('服务路径不能包含换行符。')
    return '"'+value.replace('\\','\\\\').replace('"','\\"').replace('%','%%')+'"'
def unit_text(port):
    python=Path('/usr/bin/python3') if Path('/usr/bin/python3').exists() else Path(sys.executable)
    return '\n'.join([MARKER,'[Unit]','Description=5G latency research reader','StartLimitIntervalSec=0','',
        '[Service]','Type=simple','WorkingDirectory='+str(ROOT).replace('%','%%'),
        'ExecStart='+unit_quote(python)+' -u '+unit_quote(ROOT/'启动阅读站.py')+' --service --no-open --port '+str(port),
        'Restart=always','RestartSec=3','KillSignal=SIGINT','TimeoutStopSec=10','',
        '[Install]','WantedBy=default.target',''])

def main():
    parser=argparse.ArgumentParser(description='安装/启动/查看/停止当前用户的阅读站常驻服务。')
    parser.add_argument('action',nargs='?',default='start',choices=['start','status','stop'])
    parser.add_argument('--port',type=int,default=8765)
    parser.add_argument('--no-open',action='store_true')
    parser.add_argument('--dry-run',action='store_true',help='只显示服务配置，不写入或启动')
    args=parser.parse_args()
    if not 1024<=args.port<=65535:parser.error('端口应在1024到65535之间。')
    if args.dry_run:
        print(unit_text(args.port));return 0
    if not sys.platform.startswith('linux') or not shutil.which('systemctl'):
        print('常驻管理用于Linux/systemd。其他电脑可直接双击打开阅读站.html。',file=sys.stderr);return 1
    if args.action=='status':
        result=run(['systemctl','--user','show',NAME,'--property=ActiveState,SubState,MainPID,UnitFileState'],False)
        print(result.stdout or result.stderr,end='');print('阅读地址：http://127.0.0.1:{}/index.html'.format(args.port));return result.returncode
    if args.action=='stop':
        run(['systemctl','--user','stop',NAME]);print('阅读站常驻服务已停止。');return 0
    target=Path.home()/'.config/systemd/user'/NAME
    if target.exists() and not target.read_text().startswith(MARKER):
        print('发现同名非本站服务文件，未覆盖：'+str(target),file=sys.stderr);return 1
    text=unit_text(args.port);changed=not target.exists() or target.read_text()!=text
    active=run(['systemctl','--user','is-active',NAME],False).returncode==0
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    run(['systemctl','--user','daemon-reload'])
    run(['systemctl','--user','enable','--now',NAME])
    if active and changed:run(['systemctl','--user','restart',NAME])
    spec=importlib.util.spec_from_file_location('reader_launcher',ROOT/'启动阅读站.py')
    launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)
    for _ in range(30):
        if run(['systemctl','--user','is-active',NAME],False).returncode==0 and launcher.existing_reader(args.port):break
        time.sleep(.2)
    else:
        print('服务暂未就绪。查看原因：journalctl --user -u '+NAME+' -n 30 --no-pager',file=sys.stderr);return 1
    linger=run(['loginctl','show-user',getpass.getuser(),'-p','Linger','--value'],False)
    if linger.stdout.strip()!='yes':
        print('提示：尚未启用linger，退出所有登录后服务可能停止。可执行：loginctl enable-linger '+getpass.getuser())
    url='http://127.0.0.1:{}/index.html'.format(args.port)
    print('阅读站已在后台常驻运行：\n'+url+'\n关闭终端不会停止服务；服务退出后自动重启。')
    print('停止命令：python3 '+str(ROOT/'常驻阅读站.py')+' stop')
    if not args.no_open:launcher.open_reader(url)
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,subprocess.SubprocessError,ValueError) as error:
        detail=getattr(error,'stderr','') or str(error)
        print('常驻服务配置失败：'+detail.strip(),file=sys.stderr);sys.exit(1)
