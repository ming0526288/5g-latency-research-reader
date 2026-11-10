#!/usr/bin/env python3
"""Reproduce observed STIX text-trace aliases and reject ambiguous prefixes."""
import json
from pathlib import Path
import fitz
from audit_math_pdfs import traced_font_keys, font_key

ROOT = Path(__file__).resolve().parents[1]


def main():
    fitz.TOOLS.set_subset_fontnames(True)
    rows = []
    for ident, index in [('P09', 4), ('P10', 0)]:
        with fitz.open(ROOT / '阅读转换件/论文中文' / (ident + '.zh.pdf')) as document:
            page = document[index]
            spans = page.get_texttrace()
            keys, aliases = traced_font_keys(page, spans)
            assert aliases, 'Expected observed long STIX name alias'
            for alias in aliases:
                assert alias['trace'] == alias['resource'][:31]
                assert keys[alias['trace']] == font_key(alias['resource'])
            rows.append({'id': ident, 'page': index + 1, 'aliases': aliases})
    class AmbiguousPage:
        def get_fonts(self, full=True):
            prefix = 'A' * 31
            return [(1, '', '', prefix + '-one'), (2, '', '', prefix + '-two')]
    try:
        traced_font_keys(AmbiguousPage(), [{'font': 'A' * 31}])
    except ValueError:
        pass
    else:
        raise AssertionError('Ambiguous resource names must not be accepted')
    report = {'status': 'PASS', 'actualPDFCases': rows,
              'negativeControl': 'Two full PDF resource names with the same observed prefix are rejected',
              'scope': 'Font-name reporting only; coordinate tolerance and PDF bytes unchanged'}
    (ROOT / '校验/数学字形字体别名核验.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('PASS: actual P09/P10 resource aliases and ambiguous-prefix rejection')


if __name__ == '__main__':
    main()
