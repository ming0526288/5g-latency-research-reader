#!/usr/bin/env python3
"""Reflow only the overlapping local DOC-conversion cover, keeping the original.

Run with the existing PDF translation venv after build_protocol_pdfs.py. The
source DOC is never edited. This is explicitly a local reading conversion.
"""
import hashlib
import json
from pathlib import Path
import shutil
import fitz

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest_path = ROOT/'校验/协议PDF转换清单.json'
    manifest = json.loads(manifest_path.read_text())
    ident, entry = next((k,v) for k,v in manifest['documents'].items()
                        if v['part'] == '22104-j20')
    path = ROOT/entry['file']
    if entry.get('coverLayout') == 'local-reflow' and sha(path) == entry['sha256']:
        print('Cover already reflowed; unchanged')
        return
    if sha(path) != entry['sha256'] or entry['version'] != '19.2.0':
        raise ValueError('Explicitly reviewed source version/PDF required')
    aux = ROOT.parent/'analysis-source-audit/robotics-reader-20261110'
    backup = aux/('22104-j20-before-cover-'+entry['sha256']+'.pdf')
    if not backup.exists():
        shutil.copyfile(path, backup)
    document = fitz.open(path)
    page = document[0]
    original_text = page.get_text()
    assert all(s in original_text for s in ['22.104','19.2.0','2024-06','Release 19'])
    before = [hashlib.sha256(p.get_pixmap().samples).hexdigest() for p in list(document)[1:]]
    page.add_redact_annot(fitz.Rect(35,60,558,295), fill=(1,1,1))
    page.apply_redactions(images=0, graphics=1)
    # Use the locally available Arial-compatible face, recording substitution.
    font = '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf'
    page.insert_font(fontname='CoverSans', fontfile=font)
    lines = [
        (78,18,'3GPP TS 22.104 V19.2.0 (2024-06)'),
        (110,13,'Technical Specification'),
        (144,12,'3rd Generation Partnership Project;'),
        (164,12,'Technical Specification Group Services and System Aspects;'),
        (194,13,'Service requirements for cyber-physical control'),
        (214,13,'applications in vertical domains;'),
        (244,12,'Stage 1 (Release 19)'),
        (282,8,'Local reading conversion: cover layout reflowed; original DOC retained.')]
    for y, size, text in lines:
        page.insert_text((48,y),text,fontname='CoverSans',fontsize=size)
    temporary = path.with_suffix('.reflow.tmp.pdf')
    document.save(temporary, garbage=4, deflate=True)
    document.close()
    with fitz.open(temporary) as checked:
        after = [hashlib.sha256(p.get_pixmap().samples).hexdigest() for p in list(checked)[1:]]
        if after != before:
            raise ValueError('A non-cover page changed')
        if len(checked) != entry['pages']:
            raise ValueError('Page count changed')
    temporary.replace(path)
    entry.update(sha256=sha(path),bytes=path.stat().st_size,coverLayout='local-reflow',
        coverNote='Local conversion cover text reflowed after DOC floating-text overlap; source DOC unchanged; all other pages pixel-identical.',
        coverFont='Arial unavailable locally; Liberation Sans substituted.')
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'网页/protocol-pdfs.js').write_text('window.READER_PROTOCOL_PDFS='+
        json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+';\n')
    (aux/'cover-reflow.json').write_text(json.dumps({'sourceSHA':entry['source_sha256'],
        'beforeSHA':sha(backup),'afterSHA':entry['sha256'],'nonCoverPagesIdentical':len(before),
        'entry':entry},ensure_ascii=False,indent=2))
    print(json.dumps({'coverReflowed':True,'nonCoverPagesIdentical':len(before),'pages':entry['pages']}))


if __name__ == '__main__':
    main()
