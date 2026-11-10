#!/usr/bin/env python3
"""Check final PDF bytes, pages and physically emitted math font/glyph positions.

Not an algebraic proof or a certification of every translated sentence.
"""
import argparse
import base64
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import fitz
from babel_math_guard import GUARD_VERSION

ROOT=Path(__file__).resolve().parents[1]
AUX=ROOT.parent/'analysis-source-audit/paper-zh-20261109'
OUTPUT=ROOT.parent/'analysis-source-audit/math-translation-audit-20261110'


def font_key(name):
    if name.startswith('BASE64:'):
        name=base64.b64decode(name[7:]).decode(errors='replace')
    return re.sub('[^a-z0-9]','',name.split('+')[-1].lower())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def traced_font_keys(page, spans):
    """Resolve observed Type1 name truncation against unique PDF resources.

    P09/P10 text traces report exactly the first 31 ASCII bytes of several
    embedded STIX BaseFont names, including the subset prefix. Do not blindly
    shorten all names or merge ambiguous resources to make a check pass.
    """
    resources={f[3] for f in page.get_fonts(full=True)}
    result={};proof=[]
    for raw in {span['font'] for span in spans}:
        matches={name for name in resources if name==raw}
        if not matches and len(raw.encode('utf-8'))==31 and raw.isascii():
            matches={name for name in resources if name.isascii() and len(name)>31 and name[:31]==raw}
            if len(matches)>1:
                raise ValueError('Ambiguous truncated PDF font resource: '+raw)
            if matches:
                proof.append({'trace':raw,'resource':next(iter(matches))})
        result[raw]=font_key(next(iter(matches)) if matches else raw)
    return result,proof


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=ROOT/'说明/paper-translations.json')
    parser.add_argument('--only')
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'校验/论文数学排版逐篇核验.json')
    args=parser.parse_args()
    cat=json.loads((ROOT/'网页/catalog.js').read_text().split('window.READER_CATALOG=',1)[1].rstrip(';'))
    papers=[p for p in cat['papers'] if p['id']!='book' and (not args.only or p['id'] in args.only.split(','))]
    manifest=json.loads(args.manifest.read_text())['papers'];reports=[];errors=[]
    fitz.TOOLS.set_subset_fontnames(True)
    for paper in papers:
        ident=paper['id'];entry=manifest.get(ident,{})
        try:
            if entry.get('status') not in ('generated','ready') or entry.get('mathGuard')!=GUARD_VERSION:
                raise ValueError('Current math-guard draft is not available')
            path=ROOT/entry['file'];source=ROOT/paper['file']
            assert digest(path)==entry['sha256'] and digest(source)==paper['sha256']==entry['sourceSHA']
            audit=json.loads((AUX/'math-guards'/(ident+'.json')).read_text())
            assert audit['guard']==GUARD_VERSION and audit['status']=='PASS' and not audit['unresolvedFontScopes']
            assert audit['translationSHA']==entry['sha256'] and audit['sourceSHA']==entry['sourceSHA']
            expected=json.loads((AUX/'math-guards'/(ident+'.glyphs.json')).read_text())
            with fitz.open(source) as original,fitz.open(path) as translated:
                assert len(original)==len(translated)==entry['pages']
                actual=defaultdict(list);font_aliases=[]
                for i,page in enumerate(translated):
                    assert list(page.rect)==list(original[i].rect)
                    spans=page.get_texttrace()
                    keys,aliases=traced_font_keys(page,spans)
                    font_aliases.extend({'page':i+1,**alias} for alias in aliases)
                    for span in spans:
                        name=keys[span['font']]
                        for char in span['chars']:
                            x,y=char[2]
                            actual[(i,name,round(x*10),round(y*10))].append((x,y,span['size']))
                    if args.render:
                        folder=OUTPUT/'final-pages'/ident;folder.mkdir(parents=True,exist_ok=True)
                        page.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(folder/f'{i+1:03}.png')
                missing=[]
                for glyph in expected:
                    i=glyph['page'];x=glyph['x'];y=translated[i].rect.height-glyph['y'];name=font_key(glyph['font'])
                    found=any(abs(a-x)<.08 and abs(b-y)<.08 and abs(size-glyph['fontSize'])<.08
                        for dx in [-1,0,1] for dy in [-1,0,1]
                        for a,b,size in actual.get((i,name,round(x*10)+dx,round(y*10)+dy),[]))
                    if not found:missing.append(glyph)
                if ident=='P39':
                    note=re.sub(r'\s+','',translated[1].get_text())
                    assert 'E[·]' in note and 'E[·|·]' in note
                report={'id':ident,'status':'PASS' if not missing else 'REVIEW','pages':len(translated),
                    'sourceSHA':paper['sha256'],'translationSHA':entry['sha256'],
                    'expectedMathGlyphs':len(expected),'matchedMathGlyphs':len(expected)-len(missing),
                    'unmatchedMathGlyphs':len(missing),'renderedPages':len(translated) if args.render else 0,
                    'mathGuard':audit,'resolvedTraceFontAliases':font_aliases,'visualQA':'pending',
                    'mathCoverage':'Recorded protected mathematical fragments only' if expected else
                        'No instrumented mathematical font glyphs; zero is not a mathematical fidelity certificate'}
                if missing:
                    folder=OUTPUT/'unmatched';folder.mkdir(exist_ok=True)
                    (folder/(ident+'.json')).write_text(json.dumps(missing,ensure_ascii=False,indent=2))
                    errors.append(ident+': unmatched physical math glyph positions require review')
                reports.append(report);print(ident,report['status'],report['matchedMathGlyphs'],'/',len(expected),flush=True)
        except Exception as exc:
            errors.append(ident+': '+type(exc).__name__+': '+str(exc))
            reports.append({'id':ident,'status':'FAIL','error':str(exc)})
            print(ident,'FAIL',type(exc).__name__,str(exc),flush=True)
    data={'status':'FAIL' if errors else 'PASS','guard':GUARD_VERSION,'papers':reports,'errors':errors,
        'scope':'Final PDF identity/geometry/physical math glyph positions, plus optional rendering; not full semantic or algebraic certification.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    if errors:raise SystemExit(1)


if __name__=='__main__':
    main()
