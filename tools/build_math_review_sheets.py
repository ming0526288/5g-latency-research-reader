#!/usr/bin/env python3
"""Build local-only page overviews and original/translation math-page pairs.

Creating these sheets is not evidence that a person has viewed them.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
AUX = ROOT.parent / 'analysis-source-audit/math-translation-audit-20261110'
GUARDS = ROOT.parent / 'analysis-source-audit/paper-zh-20261109/math-guards'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', default='', help='Explicit local PDF pages, e.g. P04:8,P09:14')
    args = parser.parse_args()
    samples = {ident: int(page) - 1 for ident, page in (item.split(':') for item in args.samples.split(',') if item)}
    catalog = json.loads((ROOT / '网页/catalog.js').read_text().split('window.READER_CATALOG=', 1)[1].rstrip(';'))
    papers = {p['id']: p for p in catalog['papers']}
    manifest = json.loads((ROOT / '说明/paper-translations.json').read_text())['papers']
    folder = AUX / 'review-sheets'
    folder.mkdir(exist_ok=True)
    index_path = AUX / 'review-sheet-index.json'
    previous = {row['id']: row['translationSHA'] for row in json.loads(index_path.read_text())} if index_path.exists() else {}
    rows = []
    for file in sorted((AUX / 'per-paper-audits').glob('P*.json')):
        proof = json.loads(file.read_text())['papers'][0]
        ident = proof['id']
        if proof['status'] != 'PASS':
            continue
        entry = manifest[ident]
        if entry.get('status') not in ('generated', 'ready'):
            continue
        if proof['translationSHA'] != entry['sha256']:
            continue  # A rebuilt draft needs its new physical audit first.
        assert proof['translationSHA'] == entry['sha256']
        changed = previous.get(ident) != entry['sha256']
        glyphs = json.loads((GUARDS / (ident + '.glyphs.json')).read_text())
        counts = Counter(g['page'] for g in glyphs)
        selected = counts.most_common(1)[0][0] if counts else 0
        selected = samples.get(ident, selected)
        assert 0 <= selected < proof['pages']
        contact_paths = []
        pages = sorted((AUX / 'final-pages' / ident).glob('*.png'))
        assert len(pages) == proof['pages']
        for start in range(0, len(pages), 12):
            target = folder / f'{ident}-overview-{start // 12 + 1}.png'
            if changed or not target.exists():
                sheet = Image.new('RGB', (1400, 1500), 'white')
                draw = ImageDraw.Draw(sheet)
                for offset, path in enumerate(pages[start:start + 12]):
                    image = Image.open(path).convert('RGB')
                    image.thumbnail((340, 470))
                    x, y = (offset % 4) * 350, (offset // 4) * 500
                    draw.text((x + 8, y + 4), f'{ident} PDF page {start + offset + 1}', fill='black')
                    sheet.paste(image, (x + (350 - image.width) // 2, y + 24))
                sheet.save(target)
            contact_paths.append(str(target))
        paired = folder / f'{ident}-math-page-{selected + 1}.png'
        if changed or not paired.exists():
            with fitz.open(ROOT / papers[ident]['file']) as source, fitz.open(ROOT / entry['file']) as translated:
                images = []
                for document in (source, translated):
                    pix = document[selected].get_pixmap(matrix=fitz.Matrix(1.1, 1.1))
                    images.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
                width = max(im.width for im in images)
                sheet = Image.new('RGB', (2 * width, max(im.height for im in images) + 30), 'white')
                draw = ImageDraw.Draw(sheet)
                for column, image in enumerate(images):
                    draw.text((column * width + 8, 4), f'{ident} PDF page {selected + 1} ' + ('ORIGINAL' if not column else 'TRANSLATION'), fill='black')
                    sheet.paste(image, (column * width, 30))
                sheet.save(paired)
        rows.append({'id': ident, 'pages': proof['pages'], 'translationSHA': entry['sha256'],
                     'overviewSheets': contact_paths, 'selectedMathPage': selected + 1,
                     'pairedSheet': str(paired), 'manualReview': 'not implied by sheet generation'})
    (AUX / 'review-sheet-index.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    print('Prepared', len(rows), 'paper review sheets; manual viewing is separate.')


if __name__ == '__main__':
    main()
