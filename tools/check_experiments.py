#!/usr/bin/env python3
"""Check portable experiment evidence, chronology, links and graph provenance."""
import hashlib
import html as H
import json
from pathlib import Path
import re
import urllib.parse as U

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '说明/五类时延分析'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload(did):
    return json.loads((ROOT / '网页/data' / (did + '.js')).read_text().split('=', 1)[1].rstrip(';'))


def main():
    cat = json.loads((ROOT / '网页/catalog.js').read_text().split('window.READER_CATALOG=', 1)[1].rstrip(';'))
    docs = {d['id']: d for d in cat['docs']}
    manifest = read(ROOT / '说明/experiments.json')['documents']
    assert {d['topic'] for d in manifest} == {'tdd', 'scs', 'multi-ue', 'layers', 'tail', 'source-changes'}
    provenance = read(BASE / '数据/来源与图片核验.json')
    for item in provenance['aggregateCopies']:
        assert sha(BASE / item['file']) == item['sha256'], item['file']
    for item in provenance['figures']:
        assert sha(BASE / item['file']) == item['sha256'], item['file']
    # The source report hyperlinks must identify the exact reports read for curation.
    research_prefix = 'oi-wireless-ran-latency-analysis/research/latency-analysis/'
    source_reports = [s for s in provenance['sources'] if s['source'].endswith('.md')]
    for item in source_reports:
        matching = [d for d in docs.values() if research_prefix + item['source'] in d['aliases']]
        assert any(d['sha256'] == item['sha256'] for d in matching), item['source']

    short = read(BASE / '数据/共同规则短流汇总.json')['cases']
    assert len(short) == 73
    failures = [c for c in short if not c['completed']]
    assert {c['case'] for c in failures} == {'period-p5-ul', 'period-p5-dl', 'period-p10-ul', 'period-p10-dl'}
    assert all(c.get('worst_ue_p99_ms') is None and not c['flows'] for c in failures)
    for c in short:
        if c['completed']:
            assert abs(c['worst_ue_p99_ms'] - max(f['p99'] for f in c['flows'])) < 1e-9, c['case']
            assert all(f['samples'] == 4000 for f in c['flows'])
        if c.get('internal_flows'):
            assert c['internal_validation']['sum_residual_ns'] == 0
            for f in c['internal_flows']:
                assert len(f['segment_mean_ms']) == 15
                assert abs(sum(f['segment_mean_ms'].values()) - f['mean_total_ms']) < 1e-9
                assert abs(sum(f['same_slowest_40_segment_mean_ms'].values()) - f['slowest_40_mean_total_ms']) < 1e-9
    by_id = {c['case']: c for c in short}
    plots = read(BASE / '数据/重绘图片核验.json')
    assert plots['input_sha256'] == sha(BASE / '数据/共同规则短流汇总.json')
    for item in plots['plots']:
        assert sha(BASE / item['file']) == item['sha256']
        assert all(by_id[c]['completed'] for c in item['cases'])
    # Independent cohorts are deliberately retained separately.
    tdd = read(BASE / '数据/固定CPU_TDD汇总.json')
    long = read(BASE / '数据/固定负载长流汇总.json')
    assert (tdd['passed_conditions'], tdd['total_attempts'], tdd['measured_packets']) == (24, 25, 5112000)
    assert (long['passed_conditions'], long['measured_packets']) == (12, 2704000)
    assert sum(f['samples'] for c in tdd['cases'] for f in c['flows']) == 5112000
    assert sum(f['samples'] for c in long['cases'] for f in c['flows']) == 2704000
    common_tail = read(BASE / '数据/共同规则长流汇总.json')['cases']
    assert len(common_tail) == 4 and all(f['samples'] == 100000 for c in common_tail for f in c['flows'])
    # Rank reversal is an observed result, not a global-optimum statement.
    blocks = [[c for c in tdd['cases'] if c['cohort'] == 'long' and c['block'] == b] for b in [1, 2]]
    assert [min(rows, key=lambda c: c['worst_ue_p999_ms'])['d'] for rows in blocks] == [2, 1]

    page_checks = []
    for item in manifest:
        d = docs[item['id']]
        assert d['sha256'] == sha(ROOT / item['source']) and d['snapshot'] == item['source']
        assert d['experimentStage'] == item['topic'] and cat['experimentStages'][item['topic']] == d['id']
        p = payload(d['id']); html = p['html']
        if item['topic'] == 'source-changes':
            assert html.count('<table') >= 4 and '383aa52a' in html and '61654513d5' in html
            assert '不是全部时延结果都已重测' in html
            assert '原始源码与当前研究版本' in d['search'] and '私有 HOL' in d['search']
            assert 'FORMULAHOLDER' not in html and '#/local' not in html
            page_checks.append({'id': d['id'], 'title': d['title'], 'kind': 'source-review',
                                'canonicalSourceSHA': d['sha256']})
            continue
        assert html.count('<figure') >= 2 and '错误' in html
        assert 'FORMULAHOLDER' not in html and '原文路径未包含可展示图片' not in html
        assert '#/local' not in html, 'Explanations must have portable evidence, not workstation-only links'
        assert any(c in d['search'] for c in ['失败', '报错'])
        links = [H.unescape(url) for url in re.findall(r'href="([^"]+)"', html)]
        knowledge_links = []
        for url in links:
            if not url.startswith('#/doc/'):
                continue
            path, _, query = U.unquote(url).partition('?')
            target = docs[path.removeprefix('#/doc/')]
            anchor = U.parse_qs(query).get('anchor', [''])[0]
            if anchor:
                assert anchor in {h['id'] for h in target['toc']}, (d['title'], target['title'], anchor)
            if target['id'] in cat['knowledgeTopics'].values(): knowledge_links.append(target['id'])
        assert cat['knowledgeTopics'][item['topic']] in knowledge_links
        # Verify actual downloadable/rendered image bytes, not just Markdown paths.
        for url in re.findall(r'<img[^>]+src="([^"]+)"', html):
            path = ROOT / U.unquote(url)
            assert path.is_file(), url
            known = {f['sha256'] for f in provenance['figures'] + plots['plots']}
            assert sha(path) in known, url
            # Dimension attributes reserve space before lazy plot loading.
            header = path.read_bytes()[:24]
            width, height = int.from_bytes(header[16:20], 'big'), int.from_bytes(header[20:24], 'big')
            assert f'width="{width}" height="{height}"' in html
        page_checks.append({'id': d['id'], 'title': d['title'], 'figures': html.count('<figure'),
                            'knowledgeLinks': len(knowledge_links), 'canonicalSourceSHA': d['sha256']})
    report = {'status': 'PASS', 'shortConditions': 73, 'shortFailedBeforeBusiness': 4,
              'originalFigures': len(provenance['figures']), 'replottedFigures': len(plots['plots']),
              'exactSourceReports': len(source_reports), 'documents': page_checks,
              'scope': 'Portable aggregate/hash/link/identity checks; no new experiment or raw packet statistical recomputation.'}
    (ROOT / '校验/五类实验内容核验.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
