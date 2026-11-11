#!/usr/bin/env python3
"""Check source table transcriptions, teaching arithmetic and generated lessons."""
from fractions import Fraction
import hashlib
import html
import json
from pathlib import Path
import re
import urllib.parse as U
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def main():
    catalog = json.loads((ROOT/'网页/catalog.js').read_text().split('window.READER_CATALOG=',1)[1].rstrip(';'))
    sources = json.loads((ROOT/'校验/知识点协议与文献核验.json').read_text())
    metadata = {doc['id']: doc for doc in catalog['docs']}
    core_topics = {'basics','tdd','scs','multi-ue','layers','tail','algorithms'}
    registered = json.loads((ROOT/'说明/knowledge.json').read_text())['documents']
    assert set(catalog['knowledgeTopics']) == {d['topic'] for d in registered}
    assert core_topics <= set(catalog['knowledgeTopics'])
    originals = {}
    for record in sources['protocols']:
        protocol = next(p for p in catalog['protocols'] if p['spec']==record['spec'])
        path = ROOT/protocol['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'], record['spec']
        assert protocol['version']==record['version'], record['spec']
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            originals[record['spec']] = ET.fromstring(archive.read('word/document.xml')).find(W+'body')
    def plain(node):
        return ''.join(t.text or '' for t in node.iter(W+'t'))
    def table(spec, caption):
        body = list(originals[spec]);index = next(i for i,n in enumerate(body) if caption in plain(n))
        node = next(n for n in body[index+1:] if n.tag==W+'tbl')
        return [[plain(cell) for cell in row.findall(W+'tc')] for row in node.findall(W+'tr')]
    normal = table('38.211','Table 4.3.2-1:')
    assert [row[:4] for row in normal[1:8]] == [[str(mu),'14',str(10*2**mu),str(2**mu)] for mu in range(7)]
    formats = table('38.213','Table 11.1.1-1:')
    for index, direction in [(0,'D'),(1,'U'),(2,'F')]:
        assert next(row[1:] for row in formats if row[0]==str(index)) == [direction]*14
    bandwidth = table('38.104','Table 5.3.2-2:')
    assert next(row for row in bandwidth if row[0]=='60')[2]=='132'
    assert next(row for row in bandwidth if row[0]=='120')[2]=='66'
    patterns = plain(originals['38.331'])
    assert 'maxNrofSlots' in patterns and 'maximum value for this field is 320' in patterns

    svg = ET.parse(ROOT/'说明/插图/TDD实验配置.svg').getroot()
    directions=[node.attrib['data-direction'] for node in svg.iter() if 'data-direction' in node.attrib]
    assert directions == list('D'*6+'F'*4+'U'*4)
    fmt = ET.parse(ROOT/'说明/插图/3GPP时隙格式摘录.svg').getroot()
    for group in fmt.iter():
        if 'data-format' in group.attrib:
            assert len(group.findall('{http://www.w3.org/2000/svg}rect'))==14
    scs = ET.parse(ROOT/'说明/插图/SCS与标称时隙.svg').getroot()
    for group in scs.iter():
        if 'data-scs' in group.attrib:
            assert len(group.findall('{http://www.w3.org/2000/svg}rect'))==int(group.attrib['data-scs'])//15

    slots=Fraction('0.625')*2**3
    assert slots==5
    assert (3*14+6,1*14+4,(slots-3-1)*14-6-4)==(48,18,4)
    assert Fraction(8_000_000,8*1200)==Fraction(2500,3)
    assert Fraction(8*1200,8_000_000)*1000==Fraction(6,5)
    def quantile(values,p):
        ordered=sorted(values);h=(len(ordered)-1)*p;j=h.numerator//h.denominator
        if j==len(ordered)-1:return ordered[j]
        return ordered[j]+(h-j)*(ordered[j+1]-ordered[j])
    assert quantile([1,2,3,4,10],Fraction(99,100))==Fraction(244,25)
    assert quantile([0,10],Fraction(99,100))+quantile([10,0],Fraction(99,100))!=quantile([10,10],Fraction(99,100))
    lessons=[]
    for topic,did in catalog['knowledgeTopics'].items():
        # This original suite verifies the seven illustrated prerequisite lessons;
        # additional algorithm intros have separate DOM/example checks.
        if topic not in core_topics:
            continue
        doc=metadata[did];source=ROOT/doc['source']
        assert source.is_relative_to(ROOT/'说明/算法知识点说明')
        assert source==ROOT/doc['snapshot'] and source.is_file()
        assert hashlib.sha256(source.read_bytes()).hexdigest()==doc['sha256']
        raw=(ROOT/'网页/data'/f'{did}.js').read_text()
        payload=json.loads(raw[raw.index('=')+1:].rstrip(';'))
        assert '<table>' in payload['html'] and 'class="katex' in payload['html']
        assert '<figure class="source-figure">' in payload['html'] and '放大查看' in payload['html']
        assert 'FORMULAHOLDER' not in payload['html'] and '未包含可展示图片' not in payload['html']
        assert '#/protocol/' in payload['html'] and '#/paper/' in payload['html']
        for target in re.findall(r'href="([^"]+)"',payload['html']):
            target=html.unescape(target)
            if not target.startswith('#/protocol/'):
                continue
            spec,_,query=target[len('#/protocol/'):].partition('?');params=U.parse_qs(query)
            parts=[p for p in catalog['protocols'] if p['spec']==spec]
            assert parts, target
            if params.get('clause'):
                assert any(h['clause']==params['clause'][0] for part in parts for h in part['toc']), target
            if params.get('q'):
                found=False
                for part in parts:
                    raw_protocol=(ROOT/'网页/data'/f'{part["id"]}.js').read_text()
                    body=json.loads(raw_protocol[raw_protocol.index('=')+1:].rstrip(';'))['html']
                    words=' '.join(html.unescape(re.sub('<[^>]+>','',body)).split())
                    found |= ' '.join(params['q'][0].split()).casefold() in words.casefold()
                assert found,target
        lessons.append({'topic':topic,'id':did,'source':doc['source']})
    report={'status':'PASS','protocolOriginals':len(originals),'knowledgePages':lessons,
            'checks':['38.211 normal-CP table','38.213 formats0/1/2','38.104 PRB counts','RRC320 field limit',
                      'SVG symbol/slot counts','fraction arithmetic and quantile counterexample','source hash and source-as-download',
                      'seven page tables/math/figures/citations','all new protocol clause/query targets exist'],
            'scope':'Local source/teaching checks; no new communication experiment or performance certification.'}
    (ROOT/'校验/知识点内容核对.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
