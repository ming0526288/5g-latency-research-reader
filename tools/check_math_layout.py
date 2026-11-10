#!/usr/bin/env python3
"""Check text/formula border selection without changing a paper or using a network."""
import json
import os
from pathlib import Path
from types import SimpleNamespace as S
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('BABELDOC_CACHE_DIR',str(ROOT.parent/'analysis-source-audit/paper-zh-20261109/cache/babeldoc'))
from babeldoc.document_il.midend.paragraph_finder import ParagraphFinder
from babel_layout_guard import install


def box(x, y, x2, y2):
    return S(x=x, y=y, x2=x2, y2=y2)


def main():
    finder = ParagraphFinder(None)
    page = S(page_layout=[S(id=1,class_name='isolate_formula',box=box(0,0,20,10)),
                          S(id=2,class_name='plain text',box=box(0,9,60,30))])
    prose = S(visual_bbox=S(box=box(4,9.8,8,18)))
    math = S(visual_bbox=S(box=box(4,2,8,8)))
    assert finder.get_layout(prose,page).name=='isolate_formula'
    install()
    assert finder.get_layout(prose,page).name=='plain text'
    assert finder.get_layout(math,page).name=='isolate_formula'
    # Without a text region containing the center, preserve the old decision.
    isolated = S(page_layout=[page.page_layout[0]])
    assert finder.get_layout(prose,isolated).name=='isolate_formula'
    report={'status':'PASS','checks':['Reproduced original formula-priority grazing error',
        'Body character center selects its actual text region',
        'Character centered in formula remains in formula',
        'No containing text region keeps original behavior'],
        'scope':'Geometric document layout regression; not a full-page visual certification'}
    root=Path(__file__).resolve().parents[1]
    (root/'校验/公式正文边界回归核验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: formula/prose border regression and preservation controls')


if __name__=='__main__':
    main()
