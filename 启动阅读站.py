#!/usr/bin/env python3
"""Start this folder's static reader and ask the appropriate browser to open it."""
import argparse
import base64
import hashlib
import hmac
import ipaddress
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def load_access(path):
    data=json.loads(Path(path).read_text())
    rows=data.get('users') if 'users' in data else [data]
    if not isinstance(rows,list) or not rows:raise ValueError('访问口令文件需要至少一个账号。')
    names=set()
    for row in rows:
        if not all(k in row for k in ('username','salt','password_hash','iterations')):raise ValueError('访问口令文件不完整。')
        if row['username'] in names:raise ValueError('访问口令文件有重复用户名。')
        names.add(row['username'])
    return {'users':rows}

def reader_handler(access=None):
    class ReaderHandler(SimpleHTTPRequestHandler):
        def permitted(self):
            decoded=urllib.parse.unquote(urllib.parse.urlsplit(self.path).path).replace('\\','/')
            if any(p.startswith('.') for p in decoded.split('/') if p):
                self.send_error(404);return False
            try:
                Path(self.translate_path(self.path)).resolve().relative_to(ROOT)
            except ValueError:
                self.send_error(404);return False
            if self.server.server_address[0]=='127.0.0.1':return True
            try:
                scheme,encoded=self.headers.get('Authorization','').split(' ',1)
                if scheme.lower()!='basic':raise ValueError()
                username,password=base64.b64decode(encoded,validate=True).decode('utf-8').split(':',1)
                account=next((row for row in access['users'] if hmac.compare_digest(username.encode('utf-8'),row['username'].encode('utf-8'))),None)
                if account:
                    digest=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(account['salt']),account['iterations']).hex()
                    if hmac.compare_digest(digest,account['password_hash']):return True
            except (ValueError,UnicodeError,TypeError,KeyError):pass
            self.send_response(401)
            self.send_header('WWW-Authenticate','Basic realm="5G Research Reader", charset="UTF-8"')
            self.send_header('Cache-Control','no-store');self.end_headers()
            if self.command!='HEAD':self.wfile.write('请使用阅读站独立账号和口令登录。'.encode())
            return False
        def do_GET(self):
            if self.permitted():super().do_GET()
        def do_HEAD(self):
            if self.permitted():super().do_HEAD()
        def list_directory(self,path):
            self.send_error(404,'Directory listing is disabled');return None
    return ReaderHandler

def existing_reader(port):
    """Reuse only a server whose entry and application match this checkout."""
    for relative in ('index.html', '网页/app.js'):
        url = 'http://127.0.0.1:{}/{}'.format(port, urllib.parse.quote(relative))
        try:
            with OPENER.open(url, timeout=0.8) as response:
                actual = response.read(2 * 1024 * 1024)
            if hashlib.sha256(actual).digest() != hashlib.sha256((ROOT / relative).read_bytes()).digest():
                return False
        except (OSError, urllib.error.URLError):
            return False
    return True

def open_reader(url):
    code = shutil.which('code')
    if code and os.environ.get('VSCODE_IPC_HOOK_CLI'):
        try:
            # The installed VS Code Remote CLI supports --openExternal. It asks
            # the local VS Code client to open the URL and resolve its tunnel.
            result = subprocess.run([code, '--openExternal', url], capture_output=True,
                                    text=True, timeout=15)
            if result.returncode == 0:
                print('已向 VS Code 发送打开浏览器请求。', flush=True)
                return
        except (OSError, subprocess.TimeoutExpired):
            pass
    if not os.environ.get('SSH_CONNECTION') and (
            sys.platform in ('win32', 'darwin') or os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY')):
        try:
            if webbrowser.open(url):
                print('已向本机浏览器发送打开请求。', flush=True)
                return
        except webbrowser.Error:
            pass
    print('请在浏览器打开上面的地址。远程 VS Code 可在“端口”面板转发此端口后打开。', flush=True)

def main():
    parser = argparse.ArgumentParser(description='一键启动5G通信时延研究阅读站（仅监听127.0.0.1）。')
    parser.add_argument('--port', type=int, default=8765, help='首选端口，默认8765；占用时尝试后续端口')
    parser.add_argument('--no-open', action='store_true', help='只启动/显示地址，不请求打开浏览器')
    parser.add_argument('--service', action='store_true', help='供常驻服务使用：固定端口，不复用或自动换端口')
    parser.add_argument('--bind',action='append',help='监听指定IPv4地址，可重复；默认127.0.0.1')
    parser.add_argument('--auth-file',type=Path,help='非127.0.0.1监听需要的本地口令配置文件')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65515:
        parser.error('端口必须在1024到65515之间。')
    for relative in ('index.html', '网页/app.js', '网页/catalog.js'):
        if not (ROOT / relative).is_file():
            parser.error('缺少 {}，请完整复制或克隆阅读站目录。'.format(relative))
    hosts=list(dict.fromkeys(args.bind or ['127.0.0.1']))
    for host in hosts:
        try:
            address=ipaddress.IPv4Address(host)
            if address.is_unspecified or address.is_multicast or not (address.is_private or address.is_loopback):raise ValueError()
        except ValueError:parser.error('只能指定明确的内网或回环IPv4地址，不监听全部网卡。')
    protected=any(h!='127.0.0.1' for h in hosts)
    if protected and not args.auth_file:parser.error('内网监听需要--auth-file独立访问口令。')
    try:access=load_access(args.auth_file) if protected else None
    except (OSError,ValueError) as error:parser.error(str(error))
    servers=[]
    for port in range(args.port, args.port + (1 if args.service else 21)):
        if not args.service and hosts==['127.0.0.1'] and existing_reader(port):
            url = 'http://127.0.0.1:{}/index.html'.format(port)
            print('阅读站已在运行：\n' + url, flush=True)
            if not args.no_open:
                open_reader(url)
            return 0
        try:
            for host in hosts:
                server=ThreadingHTTPServer((host,port),partial(reader_handler(access),directory=str(ROOT)))
                server.daemon_threads=True;servers.append(server)
            break
        except PermissionError:
            for server in servers:server.server_close()
            print('当前环境不允许监听本机端口，请在普通终端运行此命令。', file=sys.stderr)
            return 1
        except OSError as error:
            for server in servers:server.server_close()
            servers=[]
            import errno
            if args.service:
                print('固定端口 {} 无法监听：{}'.format(port,error),file=sys.stderr)
                return 1
            if error.errno not in (errno.EADDRINUSE, 10048):
                print('无法启动阅读站：' + str(error), file=sys.stderr)
                return 1
    if not servers:
        print('这些端口均已占用，请使用 --port 指定其他端口。', file=sys.stderr)
        return 1
    url = 'http://127.0.0.1:{}/index.html'.format(port)
    threads=[]
    for server in servers:
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();threads.append(thread)
    print('阅读站已启动：\n'+'\n'.join('http://{}:{}/index.html'.format(h,port) for h in hosts)+'\n'+('由常驻服务管理。' if args.service else '保持此终端开启；按 Ctrl+C 停止。'),flush=True)
    if not args.no_open and not args.service:
        open_reader(url)
    try:
        while all(t.is_alive() for t in threads):
            threads[0].join(timeout=1)
    except KeyboardInterrupt:
        print('\n正在停止阅读站…', flush=True)
    finally:
        for server in servers:server.shutdown();server.server_close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
