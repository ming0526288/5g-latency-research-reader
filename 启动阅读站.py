#!/usr/bin/env python3
"""Start this folder's static reader and ask the appropriate browser to open it."""
import argparse
import hashlib
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
    args = parser.parse_args()
    if not 1024 <= args.port <= 65515:
        parser.error('端口必须在1024到65515之间。')
    for relative in ('index.html', '网页/app.js', '网页/catalog.js'):
        if not (ROOT / relative).is_file():
            parser.error('缺少 {}，请完整复制或克隆阅读站目录。'.format(relative))
    server = None
    for port in range(args.port, args.port + (1 if args.service else 21)):
        if not args.service and existing_reader(port):
            url = 'http://127.0.0.1:{}/index.html'.format(port)
            print('阅读站已在运行：\n' + url, flush=True)
            if not args.no_open:
                open_reader(url)
            return 0
        try:
            server = ThreadingHTTPServer(('127.0.0.1', port), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
            server.daemon_threads = True
            break
        except PermissionError:
            print('当前环境不允许监听本机端口，请在普通终端运行此命令。', file=sys.stderr)
            return 1
        except OSError as error:
            import errno
            if args.service:
                print('固定端口 {} 无法监听：{}'.format(port,error),file=sys.stderr)
                return 1
            if error.errno not in (errno.EADDRINUSE, 10048):
                print('无法启动阅读站：' + str(error), file=sys.stderr)
                return 1
    if server is None:
        print('这些端口均已占用，请使用 --port 指定其他端口。', file=sys.stderr)
        return 1
    url = 'http://127.0.0.1:{}/index.html'.format(port)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print('阅读站已启动：\n' + url + '\n保持此终端开启；按 Ctrl+C 停止。', flush=True)
    if not args.no_open and not args.service:
        open_reader(url)
    try:
        while thread.is_alive():
            thread.join(timeout=1)
    except KeyboardInterrupt:
        print('\n正在停止阅读站…', flush=True)
    finally:
        server.shutdown()
        server.server_close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
