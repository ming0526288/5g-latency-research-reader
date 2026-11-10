#!/usr/bin/env python3
"""Create local PDF previews; never edit originals or upload protocol PDFs.

Run from reader root: python3 -B tools/build_protocol_pdfs.py --jobs 2
Requires local LibreOffice Writer/Math and Poppler. No protocol downloads.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from legacy_protocol import reading_docx

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '阅读转换件/3GPP'
AUDIT = ROOT.parent / 'analysis-source-audit' / ('protocol-pdf-reader-'+datetime.date.today().strftime('%Y%m%d'))
MANIFEST = ROOT / '校验/协议PDF转换清单.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def catalog():
    return json.loads((ROOT / '网页/catalog.js').read_text().split('window.READER_CATALOG=', 1)[1].rstrip(';'))


def page_map(text, toc):
    """Only map headings observed on a PDF page; never infer printed page offsets."""
    normalize = lambda s: re.sub(r'\s+', '', s).casefold()
    expected = {t['clause']: normalize(t['title']) for t in toc if t.get('clause')}
    matches = {}
    for page, body in enumerate(text.split('\f'), 1):
        lines = body.splitlines()
        for i, line in enumerate(lines):
            m = re.match(r'^\s*(\d+(?:\.\d+)*[a-z]?)\s+(\S.*)', line, re.I)
            if not m or m[1] not in expected or re.search(r'\.{3,}', line):
                continue
            title = normalize(' '.join(lines[i:i+3]))
            if title.startswith(expected[m[1]]):
                matches.setdefault(m[1], []).append(page)
    # Contents normally precede the body; preserve the last exact heading match.
    return {clause: max(pages) for clause, pages in matches.items()}


def convert(part, converter, force=False):
    source = ROOT / part['file']
    dest = OUTPUT / (part['part'] + '.pdf')
    old = {}
    if MANIFEST.is_file():
        old = json.loads(MANIFEST.read_text()).get('documents', {}).get(part['id'], {})
    reusable = not force and dest.is_file() and old.get('source_sha256') == part['sha256'] and old.get('sha256') == sha(dest)
    command = None
    if not reusable:
        with tempfile.TemporaryDirectory(prefix=part['id']+'-', dir=AUDIT) as temp:
            temp = Path(temp)
            command = ['soffice', '-env:UserInstallation='+(temp/'profile').as_uri(),
                       '--headless', '--norestore', '--convert-to', 'pdf:writer_pdf_Export',
                       '--outdir', str(temp), str(source)]
            env = dict(os.environ, GSETTINGS_BACKEND='memory', SAL_USE_VCLPLUGIN='svp')
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=900)
            stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
            (AUDIT/(part['id']+'-convert-'+stamp+'.log')).write_text(json.dumps({
                'command':command, 'exit':result.returncode, 'stdout':result.stdout,
                'stderr':result.stderr}, ensure_ascii=False, indent=2))
            generated = temp/(part['part']+'.pdf')
            if result.returncode or not generated.is_file() or generated.stat().st_size < 100:
                raise RuntimeError('Conversion failed: '+part['part']+'; see local conversion log')
            shutil.copyfile(generated, dest)
    info = subprocess.run(['pdfinfo', str(dest)], capture_output=True, text=True, check=True)
    pages = int(re.search(r'^Pages:\s+(\d+)', info.stdout, re.M)[1])
    text_result = subprocess.run(['pdftotext', '-layout', str(dest), '-'], capture_output=True, text=True, check=True)
    text = text_result.stdout
    if len(text.strip()) < 20:
        raise RuntimeError('PDF has no readable text: '+part['part'])
    (AUDIT/(part['part']+'-pdf.txt')).write_text(text)
    if sha(source) != part['sha256']:
        raise RuntimeError('Original changed during conversion: '+part['part'])
    result = {'id':part['id'], 'spec':part['spec'], 'version':part['version'], 'part':part['part'],
              'source':part['file'], 'source_sha256':part['sha256'],
              'file':str(dest.relative_to(ROOT)), 'sha256':sha(dest), 'bytes':dest.stat().st_size,
              'pages':pages, 'clausePages':page_map(text, part['toc']), 'converter':converter,
              'kind':'Local PDF converted from user-provided original Word, not an official downloaded PDF',
              'validation':'Readable text, page count, source/PDF SHA; visual review is recorded separately',
              'reused':reusable}
    print(json.dumps({'part':part['part'], 'pages':pages, 'headings':len(result['clausePages']), 'status':'PASS'}, ensure_ascii=False), flush=True)
    (AUDIT/(part['id']+'-result.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=2, choices=[1,2])
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--spec', help='Convert a single pilot specification; full run is needed for complete coverage')
    args = parser.parse_args()
    for command in ['soffice','pdfinfo','pdftotext']:
        if not shutil.which(command):
            raise SystemExit('Required local tool missing: '+command)
    parts = catalog()['protocols']
    # Check all local originals before any conversion; a missing original stops the batch.
    original_root = ROOT.parent/'3GPP协议原文/官方解压原文'
    for p in parts:
        path = ROOT/p['file']
        original = original_root/Path(p['file']).relative_to('协议/官方解压原文')
        if not path.is_file() or not original.is_file() or sha(path) != p['sha256'] or sha(original) != p['sha256']:
            raise SystemExit('STOP: original missing or SHA mismatch: '+p['part'])
        with zipfile.ZipFile(reading_docx(original, ROOT.parent)) as z:
            if z.testzip():
                raise SystemExit('STOP: unreadable original: '+str(original))
            ET.fromstring(z.read('word/document.xml'))
    selected = [p for p in parts if not args.spec or p['spec'] == args.spec]
    if not selected:
        raise SystemExit('No matching local specification: '+str(args.spec))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    version = subprocess.check_output(['soffice','--version'], text=True, stderr=subprocess.DEVNULL).strip()
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for result in pool.map(lambda p:convert(p, version, args.force), selected):
            results[result['id']] = result
    if args.spec and MANIFEST.is_file():
        existing = json.loads(MANIFEST.read_text()).get('documents', {})
        existing.update(results);results = existing
    data = {'updated':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
            'notice':'本地 Word 转换 PDF，仅供阅读；非 3GPP 官方下载 PDF。精确核对以保留的原 Word 为准。',
            'source_originals_checked':len(parts), 'documents':results,
            'scope':'Read-only format conversion and local viewer; no protocol content/research configuration changed.'}
    temp = MANIFEST.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temp.replace(MANIFEST)
    payload = ROOT/'网页/protocol-pdfs.js'
    payload.write_text('window.READER_PROTOCOL_PDFS='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
    print(json.dumps({'status':'PASS','converted':len(selected),'manifest':len(results),'pages':sum(p['pages'] for p in results.values())},ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
