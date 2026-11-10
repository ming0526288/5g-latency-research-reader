#!/usr/bin/env python3
"""Audit each completed final draft while the sequential repair continues."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from babel_math_guard import GUARD_VERSION

ROOT=Path(__file__).resolve().parents[1]
AUX=ROOT.parent/'analysis-source-audit/math-translation-audit-20261110'


def main():
    folder=AUX/'per-paper-audits';folder.mkdir(exist_ok=True)
    checked={}
    while True:
        manifest=json.loads((ROOT/'说明/paper-translations.json').read_text())['papers']
        for ident,entry in sorted(manifest.items()):
            if entry.get('status') not in ('generated','ready') or entry.get('mathGuard')!=GUARD_VERSION:
                continue
            if checked.get(ident)==entry['sha256']:
                continue
            command=[sys.executable,'tools/audit_math_pdfs.py','--only',ident,'--render',
                     '--output',str(folder/(ident+'.json'))]
            result=subprocess.run(command,cwd=ROOT)
            checked[ident]=entry['sha256']
            print('AUDIT_EXIT',ident,result.returncode,flush=True)
        batch=AUX/'final-repair-run.json'
        if batch.exists() and json.loads(batch.read_text()).get('status') in ('PASS','FAIL'):
            break
        time.sleep(5)
    reports=[]
    for file in sorted(folder.glob('P*.json')):
        reports.extend(json.loads(file.read_text())['papers'])
    result={'status':'PASS' if len(reports)==39 and all(x['status']=='PASS' for x in reports) else 'REVIEW',
        'guard':GUARD_VERSION,'expectedPapers':39,'papers':reports,
        'scope':'Final PDF glyph/geometry/render checks; manual page review and translation semantics remain separate.'}
    (ROOT/'校验/论文数学排版逐篇核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('AUDIT COMPLETE',result['status'],len(reports),flush=True)


if __name__=='__main__':
    main()
