#!/usr/bin/env python3
"""Render reader-owned lessons or experiment pages without re-exporting history."""
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


def build(kind='knowledge'):
    if kind not in ('knowledge', 'experiments', 'algorithm-notes', 'reading-notes'):
        raise ValueError('Unknown reader-owned document kind: ' + kind)
    experiments = kind == 'experiments'
    algorithm_notes = kind == 'algorithm-notes'
    reading_notes = kind == 'reading-notes'
    prefix = 'r' if reading_notes else 'a' if algorithm_notes else 'e' if experiments else 'k'
    source_root = ROOT / ('说明' if reading_notes or algorithm_notes or experiments else '说明/算法知识点说明')
    report_path = ROOT / ('校验/文献导读构建校验.json' if reading_notes else '校验/算法自有稿构建校验.json' if algorithm_notes else '校验/实验分析构建校验.json' if experiments else '校验/知识点构建校验.json')
    stat_prefix = 'readingNote' if reading_notes else 'algorithmNote' if algorithm_notes else 'experiment' if experiments else 'knowledge'
    catalog = read_catalog()
    manifest = json.loads((ROOT / '说明' / (kind + '.json')).read_text(encoding='utf-8'))
    previous_sources = set()
    previous_report = report_path
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
        if algorithm_notes:
            if item.get('kind') not in ('knowledge', 'results') or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item.get('algorithm', '')):
                raise ValueError('Algorithm notes require kind (knowledge/results) and an algorithm slug: ' + source)
            folder = '说明/算法知识点说明' if item['kind'] == 'knowledge' else '说明/算法文档'
            if not path.is_relative_to(ROOT / folder):
                raise ValueError('Algorithm note must be below ' + folder)
        if experiments and not any(path.is_relative_to(ROOT / folder) for folder in ('说明/五类时延分析', '说明/研究结果与分析')):
            raise ValueError('Experiment page must be below an approved results folder')
        if reading_notes and not (any(path.is_relative_to(ROOT / folder) for folder in ('说明/文献导读', '说明/启动命令')) or path == ROOT / '说明/研究结果与分析/研究结果与分析总目录.md'):
            raise ValueError('Reading note must be below an approved guide/command folder or the results hub')
        if item.get('commandStep') and (not reading_notes or not re.fullmatch(r'step-[1-9][0-9]*', item['commandStep']) or item.get('commandStatus') not in ('pending-validation', 'partial', 'validated')):
            raise ValueError('Command page requires a valid step and explicit validation status')
        if not path.is_relative_to(source_root) or path.suffix != '.md':
            raise ValueError('Reader source must be Markdown below ' + str(source_root) + ': ' + source)
        if source in sources:
            raise ValueError('Duplicate reader-owned source: ' + source)
        sources.add(source)
        text = path.read_text(encoding='utf-8')
        _, redactions = clean(text)
        if redactions:
            raise ValueError('Source requires credential review: ' + source)
        did = item.get('id') or prefix + hashlib.sha256(source.encode()).hexdigest()[:16]
        if not re.fullmatch(prefix + r'[a-f0-9]{16}', did) or did in builder.docs:
            raise ValueError('Invalid or duplicate reader-owned ID: ' + did)
        builder.paths[path] = did
        builder.docs[did] = {
            'id': did, 'title': re.search(r'^#\s+(.+)', text, re.M)[1],
            'source': source, 'aliases': [source],
            'group': 'guides' if reading_notes else ('knowledge' if item['kind'] == 'knowledge' else 'algorithms') if algorithm_notes else 'research' if experiments else 'knowledge',
            'topic': 'algorithms' if algorithm_notes else item['topic'],
            'prerequisite': not (experiments or algorithm_notes or reading_notes),
            **({'algorithm': item['algorithm']} if algorithm_notes else {}),
            **({'experimentStage': item['topic']} if experiments else {}),
            **({'researchStep': item['researchStep']} if item.get('researchStep') else {}),
            **({'knowledgeStep': item['knowledgeStep']} if item.get('knowledgeStep') else {}),
            **({key:item[key] for key in ('documentRole','parentTopic','stepExperiment')} if item.get('documentRole') else {}),
            **({'commandStatus': item['commandStatus']} if item.get('documentRole') == 'commands' else {}),
            **({'status': item.get('status','not-started')} if item.get('documentRole') == 'results' else {}),
            **({'subexperiments': item['subexperiments']} if item.get('subexperiments') else {}),
            **({key: item[key] for key in ('commandStep', 'planTopic', 'resultTopic', 'commandStatus')} if item.get('commandStep') else {}),
            **({'planTopic': item['planTopic'], 'status': item.get('status', 'not-started')} if experiments and item.get('planTopic') else {}),
            **({'independentExperiment': item['independentExperiment'], 'status': item.get('status', 'partial')} if experiments and item.get('independentExperiment') else {}),
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
    old_formulas = catalog['stats'].get(stat_prefix + 'Formulas', 0)
    old_images = catalog['stats'].get(stat_prefix + 'Images', 0)
    catalog['docs'] = [d for d in catalog['docs'] if d['source'] not in managed_sources] + metadata
    if len({doc['id'] for doc in catalog['docs']}) != len(catalog['docs']):
        raise ValueError('Duplicate IDs after knowledge merge')
    catalog['stats']['documents'] = len(catalog['docs'])
    catalog['stats']['sourceLocations'] += len(metadata) - len(old_owned)
    catalog['stats']['formulas'] += len(builder.math) - old_formulas
    catalog['stats']['images'] += len(builder.assets) - old_images
    catalog['stats'][stat_prefix + 'Documents'] = len(metadata)
    catalog['stats'][stat_prefix + 'Formulas'] = len(builder.math)
    catalog['stats'][stat_prefix + 'Images'] = len(builder.assets)
    catalog[stat_prefix + 'UpdatedAt'] = manifest['updated']
    if kind == 'knowledge':
        catalog['movedKnowledgeRoutes'] = manifest.get('redirects', {})
    elif experiments:
        catalog['movedExperimentRoutes'] = manifest.get('redirects', {})
    if reading_notes:
        catalog['readingNotes'] = [d['id'] for d in metadata]
    elif not algorithm_notes:
        catalog['experimentStages' if experiments else 'knowledgeTopics'] = {d['topic']: d['id'] for d in metadata}
    for feature in catalog['featured']:
        if experiments and feature['title'] in ('五类研究主线', '做过的五类时延分析', '第一步结果与分析'):
            first_step = next((d for d in metadata if d.get('researchStep') == 'step-1'), None)
            if first_step:
                feature.update(title=first_step['title'], id=first_step['id'])
            else:
                feature.update(title='做过的五类时延分析', id=catalog['experimentStages']['tdd'])
        elif kind == 'knowledge' and feature['title'] == '通信与时延基础':
            feature['id'] = catalog['knowledgeTopics']['basics']
        elif kind == 'knowledge' and feature['title'] == '算法知识地图':
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
              'scope': 'Reader-owned ' + kind + ' only; historical documents and source originals retained.'}
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'documents': len(metadata),
                      'formulas': len(builder.math), 'images': len(builder.assets)}, ensure_ascii=False))


if __name__ == '__main__':
    build()
