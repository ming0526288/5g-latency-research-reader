#!/usr/bin/env python3
"""Build standalone literature guides: python3 -B tools/update_reading_notes.py.

Register user-supplied numbered PDFs if available; never download sources or
replace an existing paper's identity. Full texts remain local, excluded by Git.
"""
import json
import re

from build_reader import Builder, ROOT, WEB, sha
from update_knowledge import build, write_atomic


def main():
    catalog_path = WEB / 'catalog.js'
    catalog = json.loads(catalog_path.read_text().split('window.READER_CATALOG=', 1)[1].rstrip(';'))
    papers = {p['id']: p for p in catalog['papers']}
    builder = Builder(ROOT.parent)
    added = []
    for path in sorted((ROOT.parent / 'pdf-英文原版').glob('*.pdf')):
        match = re.match(r'(\d+)[_\s]', path.name)
        if not match:
            continue
        pid = 'P' + match[1].zfill(2)
        if pid in papers:
            if papers[pid]['sha256'] != sha(path):
                raise ValueError('Paper changed; explicitly review before replacing: ' + pid)
            continue
        builder.add_paper(pid, path, '论文')
        item = builder.papers[pid]
        papers[pid] = {k: sorted(v) if isinstance(v, set) else v
                       for k, v in item.items() if not k.startswith('_')}
        added.append(pid)
    if added:
        catalog['papers'] = sorted(papers.values(), key=lambda p: p['id'])
        catalog['stats']['papers'] = len(papers)
        write_atomic(catalog_path, 'window.READER_CONTENT={};window.READER_CATALOG=' +
                     json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + ';')
        source_path = ROOT / '校验/来源清单.json'
        sources = json.loads(source_path.read_text())
        sources['papers'] = catalog['papers']
        write_atomic(source_path, json.dumps(sources, ensure_ascii=False, separators=(',', ':')))
    build('reading-notes')
    print(json.dumps({'registeredPapers': added}, ensure_ascii=False))


if __name__ == '__main__':
    main()
