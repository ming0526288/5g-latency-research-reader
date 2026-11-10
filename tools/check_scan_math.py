#!/usr/bin/env python3
"""Compare the original retained P29 proof scans below the explicit note."""
import hashlib
import json
import re
import unicodedata
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]


def main():
    catalog=json.loads((ROOT/'网页/catalog.js').read_text().split('window.READER_CATALOG=',1)[1].rstrip(';'))
    paper=next(p for p in catalog['papers'] if p['id']=='P29')
    source=ROOT/paper['file'];target=ROOT/'阅读转换件/论文中文/P29.zh.pdf';rows=[]
    with fitz.open(source) as original,fitz.open(target) as translated:
        for index in (5,6):
            note=unicodedata.normalize('NFKC',translated[index].get_text())
            assert '扫描公式不作自动认证' in re.sub(r'\s+','',note)
            clip=fitz.Rect(0,40,original[index].rect.width,original[index].rect.height)
            a=original[index].get_pixmap(clip=clip);b=translated[index].get_pixmap(clip=clip)
            assert a.width==b.width and a.height==b.height and a.samples==b.samples
            rows.append({'page':index+1,'identicalPixels':True,'sampleBytes':len(a.samples)})
    result={'status':'PASS','paper':'P29','pages':rows,
        'sourceSHA':hashlib.sha256(source.read_bytes()).hexdigest(),
        'translationSHA':hashlib.sha256(target.read_bytes()).hexdigest(),
        'scope':'Original algorithm/proof scans below the explicit note; no certification of OCR inline mathematics elsewhere'}
    (ROOT/'校验/扫描论文原推导区像素核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS: P29 PDF6/7 retained proof scans pixel-identical below the note')


if __name__=='__main__':
    main()
