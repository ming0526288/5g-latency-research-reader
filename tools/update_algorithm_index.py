#!/usr/bin/env python3
"""Resolve algorithm reading families against the portable document catalogue.

This only organizes existing notes; it does not infer algorithm identity from
filename keywords or turn candidate reading material into completed algorithms.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

from update_knowledge import ROOT, WEB, build, read_catalog, write_atomic


def main():
    notes = ROOT / '说明/algorithm-notes.json'
    if notes.is_file() and json.loads(notes.read_text())['documents']:
        build('algorithm-notes')
    catalog = read_catalog()
    manifest = json.loads((ROOT / '说明/algorithms.json').read_text())
    by_source = {}
    for doc in catalog['docs']:
        for source in doc['aliases'] + [doc['source']]:
            if source in by_source and by_source[source]['id'] != doc['id']:
                raise ValueError('Ambiguous source: ' + source)
            by_source[source] = doc
    used = []

    def resolve(entry, allowed=None):
        source = entry['source']
        if source not in by_source:
            raise ValueError('Algorithm document not built: ' + source)
        doc = by_source[source]
        if allowed and doc['group'] not in allowed:
            raise ValueError('Wrong document kind: ' + source)
        used.append({'id': doc['id'], 'source': source, 'sha256': doc['sha256']})
        return doc['id']

    common = resolve(manifest['commonKnowledge'], {'knowledge'})
    families = []
    family_ids = set()
    for item in manifest['families']:
        slug = item['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in family_ids:
            raise ValueError('Invalid or duplicate family ID: ' + slug)
        family_ids.add(slug)
        family = {k: item[k] for k in ['id', 'name', 'code', 'subtitle', 'description', 'keywords']}
        for kind in ['knowledge', 'results']:
            sections = []
            seen = set()
            for section in item[kind]:
                ids = [resolve(entry, {'knowledge'} if kind == 'knowledge' else {'algorithms', 'research', 'guides'})
                       for entry in section['documents']]
                if not ids or seen.intersection(ids) or len(set(ids)) != len(ids):
                    raise ValueError('Empty or duplicate section in ' + slug)
                seen.update(ids)
                sections.append({'title': section['title'], 'documents': ids})
            if not sections:
                raise ValueError('Both reading modes require a section: ' + slug)
            family[kind] = sections
        families.append(family)
    # Require every primary algorithm explanation to remain reachable. General
    # README/index documents can still be opened from the complete catalogue.
    knowledge = {}
    rank = lambda d: (d['source'].startswith('说明/'), d['source'].startswith('oi-wireless-ran-latency-analysis/'))
    for doc in catalog['docs']:
        if doc['group'] == 'knowledge' and (not doc.get('topic') or doc['topic'] == 'algorithms') and not re.search(r'/(?:README|00_通信与时延基础知识)\.md$', doc['source']):
            name = Path(doc['source']).name
            if name not in knowledge or rank(doc) > rank(knowledge[name]): knowledge[name] = doc
    reachable = {common} | {did for f in families for sec in f['knowledge'] for did in sec['documents']}
    missing = {d['id'] for d in knowledge.values()} - reachable
    if missing:
        raise ValueError('Unassigned primary knowledge notes: ' + ', '.join(sorted(missing)))
    result_docs = {did for f in families for sec in f['results'] for did in sec['documents']}
    missing = {d['id'] for d in catalog['docs'] if d['group'] == 'algorithms' and not d['source'].endswith('/README.md')} - result_docs
    if missing:
        raise ValueError('Unassigned implementation notes: ' + ', '.join(sorted(missing)))
    data = {'updated': manifest['updated'], 'commonKnowledge': common, 'families': families}
    write_atomic(WEB / 'algorithms.js', 'window.READER_ALGORITHMS=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';')
    report = {'status': 'PASS', 'families': len(families), 'sources': used,
              'manifestSHA': hashlib.sha256((ROOT / '说明/algorithms.json').read_bytes()).hexdigest(),
              'scope': 'Reading navigation and source identities only; no protocol/model/formula change or new experiment.'}
    (ROOT / '校验/算法分类构建校验.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({'status': 'PASS', 'families': len(families), 'documents': len({d['id'] for d in used})}, ensure_ascii=False))


if __name__ == '__main__':
    main()
