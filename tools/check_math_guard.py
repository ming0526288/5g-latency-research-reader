#!/usr/bin/env python3
"""Regression checks for lost Form-scoped mathematical glyphs in BabelDOC."""
import json
import os
from pathlib import Path
from types import SimpleNamespace
from decimal import Decimal
import tempfile

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('BABELDOC_CACHE_DIR',str(ROOT.parent/'analysis-source-audit/paper-zh-20261109/cache/babeldoc'))
from babeldoc.document_il import il_version_1 as il
from babeldoc.document_il.midend.typesetting import TypesettingUnit
from babeldoc.document_il.midend.styles_and_formulas import StylesAndFormulas
from babel_math_guard import install, normalize_matrices


def character(text, code, x=0):
    return il.PdfCharacter(pdf_character_id=code,char_unicode=text,
        box=il.Box(x=x,y=100,x2=x+4,y2=110),
        visual_bbox=il.VisualBbox(box=il.Box(x=x,y=100,x2=x+4,y2=110)),
        pdf_style=il.PdfStyle(font_id='F8',font_size=10,graphic_state=il.GraphicState()),
        scale=1,vertical=False,xobj_id=9)


def scoped_page():
    # Same font resource name in two different scopes: only the Form font is math.
    chars=[character('j',106)]
    paragraph=il.PdfParagraph(xobj_id=9,pdf_paragraph_composition=[
        il.PdfParagraphComposition(pdf_line=il.PdfLine(pdf_character=chars))])
    return il.Page(pdf_font=[il.PdfFont(font_id='F8',name='Arial')],
        pdf_xobject=[il.PdfXobject(xobj_id=9,pdf_font=[il.PdfFont(font_id='F8',name='CMSY10')])],
        pdf_paragraph=[paragraph])


def main():
    chars=[character(ch,gid,i*4) for i,(ch,gid) in enumerate([('[',91),('·',1),(']',93)])]
    unit=TypesettingUnit(formular=il.PdfFormula(box=il.Box(x=0,y=100,x2=12,y2=110),
        pdf_character=chars,x_offset=0,y_offset=0))
    old=unit.relocate(50,100,.8)
    assert [c.xobj_id for c in old.formular.pdf_character]==[None,None,None]
    parser=StylesAndFormulas.__new__(StylesAndFormulas)
    parser.translation_config=SimpleNamespace(formular_font_pattern=None,formular_char_pattern=None)
    parser.font_mapper=SimpleNamespace(has_char=lambda _:True)
    before=scoped_page();parser.process_page_formulas(before)
    assert not before.pdf_paragraph[0].pdf_paragraph_composition[0].pdf_formula
    install()
    fixed=unit.relocate(50,100,.8)
    assert [c.xobj_id for c in fixed.formular.pdf_character]==[9,9,9]
    assert [c.pdf_character_id for c in fixed.formular.pdf_character]==[91,1,93]
    assert TypesettingUnit(char=chars[0]).relocate(50,100,.8).char.xobj_id==9
    after=scoped_page();parser.process_page_formulas(after)
    assert after.pdf_paragraph[0].pdf_paragraph_composition[0].pdf_formula
    assert after.pdf_font[0].name=='Arial'
    value='5.3611818930660574e-16'
    normalized=normalize_matrices('q 1 0 0 1 '+value+' 2 cm ')
    assert Decimal(normalized.split()[5])==Decimal(value)
    assert 'e-' not in normalized
    assert parser.is_x_axis_contained(il.Box(x=0,y=0,x2=12,y2=10),il.Box(x=8,y=0,x2=14,y2=10))
    # A broad mathematical bounding box must never copy surrounding prose.
    import fitz
    import babel_math_guard as guard
    with tempfile.TemporaryDirectory(dir=ROOT.parent/'analysis-source-audit') as folder:
        source=fitz.open();page=source.new_page(width=150,height=100)
        page.insert_text((5,15),'DO NOT COPY ORIGINAL PROSE',fontsize=7)
        page.draw_line((20,30),(40,30),color=(0,0,0),width=.4)
        page.draw_rect(fitz.Rect(60,30,70,30.4),color=None,fill=(0,0,0))
        path=Path(folder)/'source.pdf';source.save(path)
        dest=fitz.open();dest.new_page(width=150,height=100).insert_text((5,15),'TRANSLATED PROSE',fontsize=7)
        guard.OVERLAYS=[{'page':0,'sourceBox':[0,0,150,100],'scale':.8,'dx':5,'dy':5,'glyphs':2}]
        result=fitz.open(stream=guard.restore_strokes(dest.tobytes(),path),filetype='pdf')
        assert 'TRANSLATED PROSE' in result[0].get_text()
        assert 'DO NOT COPY' not in result[0].get_text()
        assert len(result[0].get_drawings())==2
        assert guard.CURRENT['originalMathStrokesRestored']==2
    from babel_math_guard import read_ligatures
    paper=next((ROOT.parent/'pdf-英文原版').glob('39*'))
    assert any('\ufb01' in m.values() for m in read_ligatures(paper).values())
    report={'status':'PASS','negativeControl':'Unpatched relocation loses scope 9; unpatched parser misses Form-local CMSY font.',
        'checks':['Formula bracket/dot glyph IDs and Form scope preserved at scale 0.8',
                  'Single original glyph scope preserved',
                  'Conflicting F8 in root/Form resolved per paragraph without mutating root',
                  'Generated matrix exponent converted to numerically identical decimal',
                  'Overlapping numerator/denominator fragments remain one mathematical unit',
                  'Both source stroke and filled rule preserved without copying nearby source prose',
                  'P39 actual embedded CFF Encoding resolves fi ligature'],
        'scope':'BabelDOC 0.2.33 engineering regression; no paper theorem/translation semantics certification.'}
    (ROOT/'校验/公式字体作用域回归核验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
