#!/usr/bin/env python3
"""Rebuild all paper drafts with reviewed math guards, after a known old job.

Uses the established local translation environment. No RAN/core activity.
Snapshots every pre-repair PDF and its index; never edits an English original.
"""
import argparse
import importlib
import hashlib
import json
from pathlib import Path
import shutil
import os
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
import translate_papers as engine

AUDIT = engine.ROOT.parent/'analysis-source-audit/math-translation-audit-20261110'


def wait_old_job(pid):
    if not pid:
        return
    expected='tools/translate_papers.py --all --repair-math --engine babel'
    while True:
        result=subprocess.run(['ps','-p',str(pid),'-o','stat=,args='],capture_output=True,text=True)
        value=result.stdout.strip()
        if not value or value.startswith('Z'):
            return
        if expected not in value:
            raise RuntimeError('PID no longer identifies the expected old translation job')
        time.sleep(5)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wait-pid',type=int)
    parser.add_argument('--candidate',help='Generate one isolated candidate without changing live paper state')
    parser.add_argument('--timeout',type=int,default=600,help='Per-paper generation timeout; not a network latency threshold')
    args=parser.parse_args()
    print('WAITING for old job '+str(args.wait_pid),flush=True)
    wait_old_job(args.wait_pid)
    importlib.reload(engine)
    if args.candidate:
        engine.OUTPUT=engine.ROOT/'阅读转换件/公式核查候选'
        engine.MANIFEST=AUDIT/(args.candidate+'-final-candidate-manifest.json')
        engine.RUNTIME=AUDIT/(args.candidate+'-final-candidate-runtime.js')
        engine.run(SimpleNamespace(only=args.candidate,force=True,repair_math=True,all=False,
            warmup=False,pilot=False,verify=False,publish_existing=False,engine='babel'))
        return
    before=json.loads(engine.MANIFEST.read_text())
    backup=AUDIT/'before-final-repair';backup.mkdir(exist_ok=True)
    (backup/'manifest.json').write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
    for ident,entry in before['papers'].items():
        if entry.get('status') not in ('generated','ready'):
            continue
        source=engine.ROOT/entry['file'];digest=hashlib.sha256(source.read_bytes()).hexdigest()
        if digest!=entry['sha256']:
            raise RuntimeError('Existing translation SHA mismatch before repair: '+ident)
        target=backup/(ident+'-'+digest+'.pdf')
        if not target.exists():shutil.copy2(source,target)
    from babel_math_guard import GUARD_VERSION
    print('FINAL REPAIR START '+GUARD_VERSION,flush=True)
    papers=[p for p in engine.catalog()['papers'] if p['id']!='book']
    priority={'P39':0,'P05':1,'P01':2,'P31':3,'P24':4}
    papers.sort(key=lambda p:(priority.get(p['id'],5),p['id']))
    runs=[]
    for paper in papers:
        command=[sys.executable,'tools/translate_papers.py','--only',paper['id'],'--repair-math','--engine','babel']
        started=time.monotonic()
        process=subprocess.Popen(command,cwd=engine.ROOT,start_new_session=True)
        timed_out=False
        try:
            code=process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out=True;os.killpg(process.pid,signal.SIGTERM)
            try:code=process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL);code=process.wait()
        run={'id':paper['id'],'exit':code,'seconds':time.monotonic()-started,
             'timedOut':timed_out,'command':command}
        runs.append(run);print('PAPER_EXIT '+json.dumps(run),flush=True)
        (AUDIT/'final-repair-run.json').write_text(json.dumps({'status':'RUNNING',
            'guard':GUARD_VERSION,'expected':len(papers),'runs':runs},ensure_ascii=False,indent=2)+'\n')
    current=json.loads(engine.MANIFEST.read_text())['papers']
    papers=[p for p in engine.catalog()['papers'] if p['id']!='book']
    incomplete=[p['id'] for p in papers if current.get(p['id'],{}).get('mathGuard')!=GUARD_VERSION
                or current[p['id']].get('status') not in ('generated','ready')]
    result={'status':'FAIL' if incomplete else 'PASS','guard':GUARD_VERSION,
            'expected':len(papers),'incomplete':incomplete,'pages':sum(p['pages'] for p in papers),'runs':runs}
    (AUDIT/'final-repair-run.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    if incomplete:raise RuntimeError('Some math repairs remain incomplete')


if __name__=='__main__':
    main()
