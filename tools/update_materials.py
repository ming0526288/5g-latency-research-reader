#!/usr/bin/env python3
"""Incrementally register local papers/protocols, preserving all document pages.

Run from reader root: python3 -B tools/update_materials.py
No downloads, no full historical research re-export, no experiments.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
from build_reader import Builder, ROOT, WEB, sha


def public(entry):
    return {k: sorted(v) if isinstance(v, set) else v for k, v in entry.items()
            if not k.startswith('_') and k != 'html'}


def main():
    path = WEB/'catalog.js'
    catalog = json.loads(path.read_text().split('window.READER_CATALOG=', 1)[1].rstrip(';'))
    sources_path = ROOT/'校验/来源清单.json'
    sources = json.loads(sources_path.read_text())
    metadata_path = ROOT/'说明/materials.json'
    metadata = json.loads(metadata_path.read_text()) if metadata_path.is_file() else {}
    builder = Builder(ROOT.parent)
    papers = {p['id']: p for p in catalog['papers']}
    protocols = {p['id']: p for p in catalog['protocols']}
    archives = {p['source']: p for p in sources['protocolArchives']}
    added = {'papers': [], 'protocols': []}
    for source in sorted((ROOT.parent/'pdf-英文原版').rglob('*.pdf')):
        match = re.match(r'(\d+)[_\s]', source.name)
        if not match:
            continue
        ident = 'P' + match[1].zfill(2)
        if papers.get(ident, {}).get('sha256') == sha(source):
            continue
        if ident in papers:
            raise RuntimeError('Existing paper content changed; review explicitly before replacing: ' + ident)
        builder.add_paper(ident, source, '论文')
        entry = public(builder.papers[ident])
        entry['title'] = entry['title'].replace('_', ' ')
        papers[ident] = entry
        added['papers'].append(ident)
    original = ROOT.parent/'3GPP协议原文'
    for archive in sorted(original.rglob('*.zip')):
        key = str(archive.relative_to(ROOT.parent))
        if key in archives:
            if archives[key]['sha256'] != sha(archive):
                raise RuntimeError('Existing protocol archive changed: ' + key)
            continue
        import zipfile
        with zipfile.ZipFile(archive) as z:
            if z.testzip():
                raise RuntimeError('Unreadable protocol archive: ' + key)
        dest = ROOT/'协议/原始压缩包'/archive.relative_to(original)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archive, dest)
        archives[key] = {'file': str(dest.relative_to(ROOT)), 'source': key,
                         'sha256': sha(archive), 'bytes': archive.stat().st_size}
    builder.archives = list(archives.values())
    for source in sorted((original/'官方解压原文').rglob('*')):
        if source.suffix.lower() not in ('.doc', '.docx'):
            continue
        ident = 's'+hashlib.sha256(str(source.relative_to(original)).encode()).hexdigest()[:12]
        if protocols.get(ident, {}).get('sha256') == sha(source):
            continue
        if ident in protocols:
            raise RuntimeError('Existing protocol content changed; review first: ' + ident)
        match = re.match(r'(\d{2})(\d{3})(-\d)?', source.name)
        if not match:
            raise RuntimeError('Unrecognized protocol identity: ' + source.name)
        spec = match[1] + '.' + match[2] + (match[3] or '')
        entry = builder.protocol_doc(source, spec, ident)
        protocols[ident] = public(entry)
        (WEB/'data'/(ident+'.js')).write_text('window.READER_CONTENT['+json.dumps(ident)+']='+
            json.dumps({'html':entry['html'],'toc':entry['toc']},ensure_ascii=False)+';')
        added['protocols'].append({'id':ident, 'spec':spec, 'version':entry['version']})
    for ident, entry in papers.items():
        entry.update(metadata.get('papers', {}).get(ident, {}))
    for entry in protocols.values():
        entry.update(metadata.get('protocols', {}).get(entry['spec'], {}))
    catalog['papers'] = sorted(papers.values(), key=lambda p: p['id'])
    catalog['protocols'] = sorted(protocols.values(), key=lambda p: (p['spec'],p['part']))
    catalog['stats'].update(papers=len(papers), protocolParts=len(protocols),
                            protocolSpecs=len({p['spec'] for p in protocols.values()}))
    sources.update(papers=catalog['papers'], protocols=catalog['protocols'],
                   protocolArchives=list(archives.values()))
    sources_path.write_text(json.dumps(sources,ensure_ascii=False,separators=(',',':')))
    path.write_text('window.READER_CONTENT={};window.READER_CATALOG='+
                   json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+';')
    print(json.dumps({'added':added, 'papers':len(papers), 'protocols':len(protocols)},ensure_ascii=False))


if __name__ == '__main__':
    main()
