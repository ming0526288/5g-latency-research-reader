#!/usr/bin/env python3
"""Isolated math/prose boundary candidate; never changes live reader manifests."""
import argparse
import dataclasses
import json
from pathlib import Path
import translate_papers as engine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', required=True)
    parser.add_argument('--page', type=int, required=True)
    args = parser.parse_args()
    paper = dict(next(p for p in engine.catalog()['papers'] if p['id'] == args.only))
    high, model = engine.prepare()
    from babel_layout_guard import install
    import babel_layout_guard
    install()
    from babeldoc.document_il.midend.il_translator import ILTranslator
    original = ILTranslator.translate
    folder = engine.ROOT.parent / 'analysis-source-audit/math-translation-audit-20261110'

    def capture(self, docs):
        selected = [dataclasses.asdict(p) for pg in docs.page if pg.page_number == args.page - 1 for p in pg.pdf_paragraph]
        (folder / (args.only + '-layout-candidate-il.json')).write_text(json.dumps(selected, ensure_ascii=False))
        return original(self, docs)

    ILTranslator.translate = capture
    paper['id'] = args.only + '-layout-candidate'
    output = folder / (args.only + '-layout-candidate.pdf')
    output.write_bytes(engine.translate_with_babel(paper, model))
    # Apply the same original figure/display-equation restoration as live drafts.
    engine.write_json(engine.AUX / 'layouts' / (paper['id'] + '.json'), model.paper_layouts)
    output.write_bytes(engine.restore_original_figures(paper, output.read_bytes(), model.paper_layouts))
    import fitz
    with fitz.open(output) as document:
        document[args.page - 1].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(output.with_suffix('.png'))
    print('ISOLATED CANDIDATE', args.only, babel_layout_guard.COUNTS)


if __name__ == '__main__':
    main()
