#!/usr/bin/env python3
"""Manage this user's persistent reader and optional protected VPN listener."""
import argparse
import getpass
import hashlib
import importlib.util
import ipaddress
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parent
NAME='5g-latency-reader.service'
MARKER='# Managed by 5g-latency-research-reader/常驻阅读站.py'
CONFIG=Path.home()/'.config/5g-latency-reader'

def private_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True);path.parent.chmod(0o700)
    fd,name=tempfile.mkstemp(dir=path.parent,prefix='.reader-')
    try:
        with os.fdopen(fd,'w') as stream:
            json.dump(data,stream,ensure_ascii=False,indent=2)
        os.chmod(name,0o600);os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)

def login_users(data):
    if not isinstance(data,dict):raise ValueError('login.json最外层需要JSON对象。')
    rows=data.get('users') if 'users' in data else [data]
    if not isinstance(rows,list) or not rows:raise ValueError('users需要至少一个账号。')
    result=[];names=set()
    for row in rows:
        if not isinstance(row,dict):raise ValueError('每个账号需要username和password。')
        username=row.get('username');password=row.get('password')
        if not isinstance(username,str) or not username or ':' in username or not isinstance(password,str) or not password:
            raise ValueError('账号需要非空字符串username/password，用户名不能含冒号。')
        if username in names:raise ValueError('用户名不能重复：'+username)
        names.add(username);result.append({'username':username,'password':password})
    return result

def ensure_access(directory):
    auth=directory/'access.json';login=directory/'login.json'
    if login.exists():
        users=login_users(json.loads(login.read_text()))
    else:
        users=[{'username':'reader','password':secrets.token_urlsafe(12)}]
        private_json(login,users[0])
    current=json.loads(auth.read_text()) if auth.exists() else {}
    old_rows=current.get('users',[]) if 'users' in current else ([current] if current else [])
    old={row['username']:row for row in old_rows};rows=[]
    for user in users:
        username=user['username'];password=user['password'];previous=old.get(username)
        if previous:
            digest=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(previous['salt']),previous['iterations']).hex()
            if secrets.compare_digest(previous['password_hash'],digest):rows.append(previous);continue
        salt=secrets.token_hex(16);iterations=200000
        digest=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),iterations).hex()
        rows.append({'username':username,'salt':salt,'iterations':iterations,'password_hash':digest})
    desired={'version':2,'users':rows}
    if desired!=current:private_json(auth,desired)
    auth.chmod(0o600)
    login.chmod(0o600)
    return auth

def run(args,check=True):
    return subprocess.run(args,text=True,capture_output=True,check=check,timeout=25)
def unit_quote(value):
    value=str(value)
    if '\n' in value or '\r' in value:raise ValueError('服务路径不能包含换行符。')
    return '"'+value.replace('\\','\\\\').replace('"','\\"').replace('%','%%')+'"'
def unit_text(port,hosts=None,auth_file=None):
    python=Path('/usr/bin/python3') if Path('/usr/bin/python3').exists() else Path(sys.executable)
    extra=''.join(' --bind '+unit_quote(h) for h in (hosts or ['127.0.0.1']))
    if auth_file:extra+=' --auth-file '+unit_quote(auth_file)
    return '\n'.join([MARKER,'[Unit]','Description=5G latency research reader','StartLimitIntervalSec=0','',
        '[Service]','Type=simple','WorkingDirectory='+str(ROOT).replace('%','%%'),
        'ExecStart='+unit_quote(python)+' -u '+unit_quote(ROOT/'启动阅读站.py')+' --service --no-open --port '+str(port)+extra,
        'Restart=always','RestartSec=3','KillSignal=SIGINT','TimeoutStopSec=10','',
        '[Install]','WantedBy=default.target',''])

def main():
    parser=argparse.ArgumentParser(description='安装/启动/查看/停止当前用户的阅读站常驻服务。')
    parser.add_argument('action',nargs='?',default='start',choices=['start','status','stop','credentials'])
    parser.add_argument('--port',type=int)
    parser.add_argument('--vpn-address',help='增加已确认可达的内网IPv4监听，并生成独立访问口令')
    parser.add_argument('--local-only',action='store_true',help='恢复仅127.0.0.1访问')
    parser.add_argument('--no-open',action='store_true')
    parser.add_argument('--dry-run',action='store_true',help='只显示服务配置，不写入或启动')
    args=parser.parse_args()
    settings_file=CONFIG/'service.json'
    settings=json.loads(settings_file.read_text()) if settings_file.exists() else {'port':8765,'hosts':['127.0.0.1']}
    port=args.port or settings['port'];hosts=settings['hosts']
    if args.local_only:hosts=['127.0.0.1']
    if args.vpn_address:
        try:
            ip=ipaddress.IPv4Address(args.vpn_address)
            if not ip.is_private or ip.is_loopback or ip.is_unspecified or ip.is_multicast:raise ValueError()
        except ValueError:parser.error('--vpn-address必须是明确的内网IPv4地址。')
        hosts=['127.0.0.1',str(ip)]
    if not 1024<=port<=65535:parser.error('端口应在1024到65535之间。')
    auth_file=CONFIG/'access.json' if any(h!='127.0.0.1' for h in hosts) else None
    if args.action=='credentials':
        login=CONFIG/'login.json'
        if not login.exists():print('尚未设置VPN访问口令。');return 1
        for user in login_users(json.loads(login.read_text())):
            print('阅读站独立账号：'+user['username']+'\n阅读站独立口令：'+user['password']+'\n')
        return 0
    if args.dry_run:
        print(unit_text(port,hosts,auth_file));return 0
    if not sys.platform.startswith('linux') or not shutil.which('systemctl'):
        print('常驻管理用于Linux/systemd。其他电脑可直接双击打开阅读站.html。',file=sys.stderr);return 1
    if args.action=='status':
        result=run(['systemctl','--user','show',NAME,'--property=ActiveState,SubState,MainPID,UnitFileState'],False)
        print(result.stdout or result.stderr,end='')
        for h in reversed(hosts):print('阅读地址：http://{}:{}/index.html'.format(h,port))
        return result.returncode
    if args.action=='stop':
        run(['systemctl','--user','stop',NAME]);print('阅读站常驻服务已停止。');return 0
    target=Path.home()/'.config/systemd/user'/NAME
    if target.exists() and not target.read_text().startswith(MARKER):
        print('发现同名非本站服务文件，未覆盖：'+str(target),file=sys.stderr);return 1
    access_before=auth_file.read_bytes() if auth_file and auth_file.exists() else None
    if auth_file:ensure_access(CONFIG)
    access_changed=bool(auth_file and access_before!=auth_file.read_bytes())
    text=unit_text(port,hosts,auth_file);changed=not target.exists() or target.read_text()!=text
    active=run(['systemctl','--user','is-active',NAME],False).returncode==0
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    run(['systemctl','--user','daemon-reload'])
    run(['systemctl','--user','enable','--now',NAME])
    if active and (changed or access_changed):run(['systemctl','--user','restart',NAME])
    private_json(settings_file,{'port':port,'hosts':hosts})
    spec=importlib.util.spec_from_file_location('reader_launcher',ROOT/'启动阅读站.py')
    launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)
    for _ in range(30):
        if run(['systemctl','--user','is-active',NAME],False).returncode==0 and launcher.existing_reader(port):break
        time.sleep(.2)
    else:
        print('服务暂未就绪。查看原因：journalctl --user -u '+NAME+' -n 30 --no-pager',file=sys.stderr);return 1
    linger=run(['loginctl','show-user',getpass.getuser(),'-p','Linger','--value'],False)
    if linger.stdout.strip()!='yes':
        print('提示：尚未启用linger，退出所有登录后服务可能停止。可执行：loginctl enable-linger '+getpass.getuser())
    url='http://{}:{}/index.html'.format(hosts[-1],port)
    print('阅读站已在后台常驻运行：\n'+url+'\n关闭终端不会停止服务；服务退出后自动重启。')
    print('停止命令：python3 '+str(ROOT/'常驻阅读站.py')+' stop')
    if auth_file:print('查看阅读站独立口令：python3 '+str(ROOT/'常驻阅读站.py')+' credentials\n口令仅保存在本机用户配置目录，不写入Git。')
    if not args.no_open:launcher.open_reader(url)
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,subprocess.SubprocessError,ValueError) as error:
        detail=getattr(error,'stderr','') or str(error)
        print('常驻服务配置失败：'+detail.strip(),file=sys.stderr);sys.exit(1)
