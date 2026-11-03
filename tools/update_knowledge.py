#!/usr/bin/env python3
"""Render reader-owned knowledge notes without re-exporting historical research."""
from __future__ import annotations
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from build_reader import Builder, ROOT, WEB, clean, slug


def write_atomic(path, text):
    descriptor, name = tempfile.mkstemp(prefix='.knowledge-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            stream.write(text)
        os.chmod(name, 0o644)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def read_catalog():
    text = (WEB / 'catalog.js').read_text(encoding='utf-8')
    return json.loads(text.split('window.READER_CATALOG=', 1)[1].rstrip(';'))


def build():
    catalog = read_catalog()
    manifest = json.loads((ROOT / '说明/knowledge.json').read_text(encoding='utf-8'))
    previous_sources = set()
    previous_report = ROOT / '校验/知识点构建校验.json'
    if previous_report.is_file():
        previous_sources = {doc['source'] for doc in json.loads(previous_report.read_text())['documents']
                            if doc['source'].startswith('说明/')}
    builder = Builder(ROOT.parent)
    for paper in catalog['papers']:
        item = dict(paper, _source=(ROOT / paper['file']).resolve())
        item['citedPages'] = set(item.get('citedPages', []))
        builder.papers[item['id']] = item
    for protocol in catalog['protocols']:
        item = dict(protocol, _source=(ROOT / protocol['file']).resolve())
        builder.protocols[item['id']] = item
        builder.specs[item['spec']].append(item['id'])
    builder.spec_clauses = {
        spec: {entry['clause'] for pid in ids for entry in builder.protocols[pid]['toc']}
        for spec, ids in builder.specs.items()
    }
    for doc in catalog['docs']:
        builder.paths[(ROOT / doc['snapshot']).resolve()] = doc['id']
        builder.paths[(ROOT.parent / doc['source']).resolve()] = doc['id']
        if doc['source'].startswith('说明/'):
            builder.paths[(ROOT / doc['source']).resolve()] = doc['id']
    sources = set()
    for item in manifest['documents']:
        source = item['source']
        path = (ROOT / source).resolve()
        if not path.is_relative_to(ROOT / '说明/算法知识点说明') or path.suffix != '.md':
            raise ValueError('Knowledge source must be Markdown below 说明/算法知识点说明/: ' + source)
        if source in sources:
            raise ValueError('Duplicate knowledge source: ' + source)
        sources.add(source)
        text = path.read_text(encoding='utf-8')
        _, redactions = clean(text)
        if redactions:
            raise ValueError('Source requires credential review: ' + source)
        did = item.get('id') or 'k' + hashlib.sha256(source.encode()).hexdigest()[:16]
        if not re.fullmatch(r'k[a-f0-9]{16}', did) or did in builder.docs:
            raise ValueError('Invalid or duplicate knowledge ID: ' + did)
        builder.paths[path] = did
        builder.docs[did] = {
            'id': did, 'title': re.search(r'^#\s+(.+)', text, re.M)[1],
            'source': source, 'aliases': [source], 'group': 'knowledge',
            'topic': item['topic'], 'prerequisite': True,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'snapshot': source, 'redacted': False, 'toc': [],
            '_path': path, '_text': text,
        }

    def inline_renderer(tokens, options, env):
        result = ''; depth = 0
        for index, token in enumerate(tokens):
            if token.type == 'link_open':
                depth += 1
            env['inside_link'] = depth > 0
            rule = builder.md.renderer.rules.get(token.type)
            result += (rule(tokens, index, options, env) if rule
                       else builder.md.renderer.renderToken(tokens, index, options, env))
            if token.type == 'link_close':
                depth -= 1
        env['inside_link'] = False
        return result

    builder.md.renderer.renderInline = inline_renderer
    for doc in builder.docs.values():
        builder.current = doc['_path']
        builder.default_paper_context = None
        builder.paper_context = None
        text = re.sub(r'^```math\s*\n(.*?)^```\s*$',
                      lambda m: '\n' + builder.math_tag(m[1], True) + '\n',
                      doc['_text'], flags=re.M | re.S)
        tokens = builder.md.parse(builder.equations(text, doc['_path']))
        if any('**' in child.content for token in tokens for child in (token.children or [])
               if child.type == 'text'):
            raise ValueError('Unparsed emphasis delimiters in ' + doc['source'])
        headings = collections.Counter()
        for index, token in enumerate(tokens):
            if token.type == 'heading_open':
                title = tokens[index + 1].content
                base = slug(title); number = headings[base]; headings[base] += 1
                anchor = base + (f'-{number}' if number else '')
                token.attrSet('id', anchor)
                doc['toc'].append({'id': anchor, 'title': re.sub(r'[`*_]', '', title),
                                   'level': int(token.tag[1])})
        doc['html'] = builder.md.renderer.render(tokens, builder.md.options, {})
        doc['words'] = len(re.sub(r'\s', '', doc['_text']))
        doc['minutes'] = max(1, round(doc['words'] / 650))

    node = shutil.which('node') or shutil.which('nodejs')
    if not node:
        raise RuntimeError('Rendering formulas requires Node.js; ordinary reading does not.')
    katex = ROOT / '网页/vendor/katex/katex.min.js'
    if not katex.is_file():
        raise FileNotFoundError(katex)
    with tempfile.TemporaryDirectory(prefix='reader-knowledge-') as temp:
        input_path = Path(temp) / 'input.json'; output_path = Path(temp) / 'output.json'
        input_path.write_text(json.dumps(builder.math, ensure_ascii=False))
        result = subprocess.run([node, str(ROOT / 'tools/render_math.cjs'), str(katex),
                                 str(input_path), str(output_path)],
                                capture_output=True, text=True, check=True)
        math = json.loads(output_path.read_text())
    if math['errors']:
        raise ValueError('KaTeX errors: ' + json.dumps(math['errors'], ensure_ascii=False))

    payloads = {}
    metadata = []
    for doc in builder.docs.values():
        rendered = re.sub(r'FORMULAHOLDER(\d+)END',
                          lambda m: math['html'][int(m[1])], doc['html'])
        if 'FORMULAHOLDER' in rendered or '原文路径未包含可展示图片' in rendered:
            raise ValueError('Incomplete formula or image in ' + doc['source'])
        payloads[doc['id']] = {'html': rendered, 'toc': doc['toc']}
        public = {key: value for key, value in doc.items()
                  if not key.startswith('_') and key != 'html'}
        public['search'] = re.sub(r'[`#*|\[\]<>]', ' ', doc['_text'])
        metadata.append(public)

    managed_sources = sources | previous_sources
    old_owned = [d for d in catalog['docs'] if d['source'] in managed_sources]
    old_formulas = catalog['stats'].get('knowledgeFormulas', 0)
    old_images = catalog['stats'].get('knowledgeImages', 0)
    catalog['docs'] = [d for d in catalog['docs'] if d['source'] not in managed_sources] + metadata
    if len({doc['id'] for doc in catalog['docs']}) != len(catalog['docs']):
        raise ValueError('Duplicate IDs after knowledge merge')
    catalog['stats']['documents'] = len(catalog['docs'])
    catalog['stats']['sourceLocations'] += len(metadata) - len(old_owned)
    catalog['stats']['formulas'] += len(builder.math) - old_formulas
    catalog['stats']['images'] += len(builder.assets) - old_images
    catalog['stats']['knowledgeDocuments'] = len(metadata)
    catalog['stats']['knowledgeFormulas'] = len(builder.math)
    catalog['stats']['knowledgeImages'] = len(builder.assets)
    catalog['knowledgeUpdatedAt'] = manifest['updated']
    catalog['knowledgeTopics'] = {d['topic']: d['id'] for d in metadata}
    for feature in catalog['featured']:
        if feature['title'] == '通信与时延基础':
            feature['id'] = catalog['knowledgeTopics']['basics']
        elif feature['title'] == '算法知识地图':
            feature['id'] = catalog['knowledgeTopics']['algorithms']
    for paper in catalog['papers']:
        paper['citedPages'] = sorted(builder.papers[paper['id']]['citedPages'])
    for did, payload in payloads.items():
        write_atomic(WEB / 'data' / (did + '.js'),
            'window.READER_CONTENT[' + json.dumps(did) + ']=' +
            json.dumps(payload, ensure_ascii=False) + ';')
    write_atomic(WEB / 'catalog.js',
        'window.READER_CONTENT={};window.READER_CATALOG=' +
        json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + ';')
    report = {'status': 'PASS', 'documents': metadata,
              'formulas': len(builder.math), 'mathErrors': math['errors'],
              'imageCount': len(builder.assets), 'warnings': builder.warnings,
              'scope': 'Reader-owned lessons only; historical documents and source originals retained.'}
    (ROOT / '校验/知识点构建校验.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'documents': len(metadata),
                      'formulas': len(builder.math), 'images': len(builder.assets)}, ensure_ascii=False))


if __name__ == '__main__':
    build()
