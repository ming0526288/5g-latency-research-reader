#!/usr/bin/env python3
"""Translate a local converted protocol PDF through the existing paper engine.

Run in the established translation venv: tools/translate_protocols.py --spec 22.104
Original Word/ZIP and original converted PDF remain unchanged. Separate state
avoids mixing protocol versions with paper IDs or paper translation reviews.
"""
import argparse
import json
from types import SimpleNamespace
import translate_papers as engine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', required=True)
    parser.add_argument('--engine', choices=['babel','pdf2zh'], default='babel')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    source_catalog = engine.catalog()
    converted = json.loads((engine.ROOT/'校验/协议PDF转换清单.json').read_text())['documents']
    selected = []
    for source in source_catalog['protocols']:
        if source['spec'] != args.spec:
            continue
        pdf = converted.get(source['id'])
        if not pdf or pdf['source_sha256'] != source['sha256']:
            raise RuntimeError('Matching readable original PDF required before translation: '+source['part'])
        selected.append({'id':source['id'], 'file':pdf['file'], 'pages':pdf['pages'],
                         'title':source['title'], 'spec':source['spec'], 'version':source['version']})
    if not selected:
        raise RuntimeError('Protocol missing from local catalog: '+args.spec)
    engine.OUTPUT = engine.ROOT/'阅读转换件/协议中文'
    engine.MANIFEST = engine.ROOT/'说明/protocol-translations.json'
    engine.RUNTIME = engine.ROOT/'网页/protocol-translations.js'
    engine.JS_GLOBAL = 'READER_PROTOCOL_TRANSLATIONS'
    engine.catalog = lambda: {'papers': selected}
    engine.run(SimpleNamespace(only=','.join(p['id'] for p in selected), all=False,
        warmup=False, pilot=False, verify=False, publish_existing=False,
        force=args.force, engine=args.engine))


if __name__ == '__main__':
    main()
