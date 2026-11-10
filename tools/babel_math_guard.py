"""Compatibility guards for the locally installed BabelDOC 0.2.33.

Original math characters inside PDF Form XObjects must keep their font resource
scope when moved. Resolve math fonts in that same scope. No formula is rewritten.
The installed package is left untouched; these scoped hooks live in this repo.
"""
from copy import copy
from decimal import Decimal
import importlib.metadata
import json
from pathlib import Path
import re

GUARD_VERSION = 'xobject-font-scope-math-strokes-ligatures-v6'
CURRENT = {}
AUDIT_PATH = None
OVERLAYS = []
CURRENT_PAGE = None
CURRENT_MATH_FONTS = {}
LIGATURE_MAP = {}
CURRENT_FONT_NAMES = {}
EXPECTED_GLYPHS = []


def read_ligatures(source_path):
    """Use the actual embedded CFF Encoding, not guesses about a CID number."""
    if source_path is None:
        return {}
    import fitz
    from io import BytesIO
    from fontTools.cffLib import CFFFontSet
    known={'ff':'\ufb00','fi':'\ufb01','fl':'\ufb02','ffi':'\ufb03','ffl':'\ufb04'}
    source=fitz.open(source_path);result={}
    for xref in {font[0] for page in source for font in page.get_fonts(full=True)}:
        if not xref or source.xref_get_key(xref,'Encoding')[0]!='null':
            continue
        name,extension,kind,data=source.extract_font(xref)
        if extension!='cff' or not data:
            continue
        font=CFFFontSet();font.decompile(BytesIO(data),None)
        encoding=font.topDictIndex[0].Encoding
        if isinstance(encoding,list):
            mapping={i:known[n] for i,n in enumerate(encoding) if n in known}
            if mapping:result[xref]=mapping
    source.close()
    return result


def normalize_matrices(operations):
    """Serialize generated cm operands as decimal PDF numbers, with no rounding."""
    number = r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'
    pattern = re.compile(r'(?<!\S)(' + r'\s+'.join([number]*6) + r')\s+cm(?=\s|$)')
    def replace(match):
        values = match[1].split()
        if not any('e' in value.lower() for value in values):
            return match[0]
        CURRENT['normalizedMatrices'] = CURRENT.get('normalizedMatrices',0)+1
        return ' '.join(format(Decimal(value),'f') for value in values)+' cm'
    return pattern.sub(replace, operations)


def install(audit_path=None, source_path=None):
    global CURRENT, AUDIT_PATH, OVERLAYS, LIGATURE_MAP, EXPECTED_GLYPHS
    CURRENT = {'guard':GUARD_VERSION,'relocatedScopedCharacters':0,
               'scopedFormulaParagraphs':0,'validatedGlyphs':0,'normalizedMatrices':0}
    AUDIT_PATH = Path(audit_path) if audit_path else None
    OVERLAYS = []
    EXPECTED_GLYPHS = []
    LIGATURE_MAP = read_ligatures(source_path)
    CURRENT['decodedProseLigatures']=0
    if importlib.metadata.version('babeldoc') != '0.2.33':
        raise RuntimeError('Math compatibility guard requires reviewed BabelDOC 0.2.33')
    from babeldoc.document_il.midend.styles_and_formulas import StylesAndFormulas
    from babeldoc.document_il.midend.typesetting import TypesettingUnit, Typesetting
    if getattr(TypesettingUnit.relocate, '_reader_math_guard', False):
        return
    original_relocate = TypesettingUnit.relocate

    def relocate(self, x, y, scale):
        result = original_relocate(self, x, y, scale)
        if self.char is not None and result.char is not None:
            result.char.xobj_id = self.char.xobj_id
            if self.char.xobj_id is not None:
                CURRENT['relocatedScopedCharacters'] += 1
        elif self.formular is not None and result.formular is not None:
            result.formular._reader_source = getattr(self.formular,'_reader_source',self.formular)
            if len(self.formular.pdf_character) != len(result.formular.pdf_character):
                raise ValueError('Formula character count changed during relocation')
            for before, after in zip(self.formular.pdf_character, result.formular.pdf_character):
                after.xobj_id = before.xobj_id
                if before.xobj_id is not None:
                    CURRENT['relocatedScopedCharacters'] += 1
        return result

    relocate._reader_math_guard = True
    TypesettingUnit.relocate = relocate
    original_formulas = StylesAndFormulas.process_page_formulas

    def scoped_formulas(self, page):
        # Font IDs are local to each Form. Combining all Forms' fonts globally
        # would confuse identically named F1/F2 resources from different Forms.
        forms = {form.xobj_id: form for form in page.pdf_xobject}
        for paragraph in page.pdf_paragraph:
            scoped = copy(page)
            scoped.pdf_paragraph = [paragraph]
            form = forms.get(paragraph.xobj_id)
            scoped.pdf_font = list(page.pdf_font) + (list(form.pdf_font) if form else [])
            fonts={f.font_id:f for f in scoped.pdf_font};changed=False
            for composition in paragraph.pdf_paragraph_composition:
                line=composition.pdf_line
                if line:
                    for char in line.pdf_character:
                        font=fonts.get(char.pdf_style.font_id)
                        mapping=LIGATURE_MAP.get(font.xref_id,{}) if font else {}
                        if char.char_unicode and char.char_unicode.startswith('(cid:') and char.pdf_character_id in mapping:
                            char.char_unicode=mapping[char.pdf_character_id]
                            CURRENT['decodedProseLigatures']+=1;changed=True
            if changed:
                paragraph.unicode=''.join(char.char_unicode or '' for composition in paragraph.pdf_paragraph_composition
                    if composition.pdf_line for char in composition.pdf_line.pdf_character)
            if form:
                CURRENT['scopedFormulaParagraphs'] += 1
            original_formulas(self, scoped)

    StylesAndFormulas.process_page_formulas = scoped_formulas
    original_start=StylesAndFormulas.is_formulas_start_char
    def formula_start(self,char):
        if char in ('\ufb00','\ufb01','\ufb02','\ufb03','\ufb04'):
            return False
        return original_start(self,char)
    StylesAndFormulas.is_formulas_start_char=formula_start
    # Numerators and denominators can be separate neighboring runs. Their x
    # intervals overlap without either enclosing the other (P39 Q^(1/2)_k).
    # Keep connected mathematical geometry in one untranslatable unit.
    StylesAndFormulas.is_x_axis_contained = lambda self,a,b: min(a.x2,b.x2)>max(a.x,b.x)
    original_page = Typesetting.render_page
    def render_page(self,page):
        global CURRENT_PAGE, CURRENT_MATH_FONTS, CURRENT_FONT_NAMES
        CURRENT_PAGE=page.page_number
        classifier=StylesAndFormulas.__new__(StylesAndFormulas)
        classifier.translation_config=self.translation_config
        root={f.font_id:classifier.is_formulas_font(f.name) for f in page.pdf_font}
        CURRENT_MATH_FONTS={None:root}
        root_names={f.font_id:f.name for f in page.pdf_font}
        CURRENT_FONT_NAMES={None:root_names}
        for form in page.pdf_xobject:
            fonts=dict(root)
            fonts.update({f.font_id:classifier.is_formulas_font(f.name) for f in form.pdf_font})
            CURRENT_MATH_FONTS[form.xobj_id]=fonts
            names=dict(root_names);names.update({f.font_id:f.name for f in form.pdf_font})
            CURRENT_FONT_NAMES[form.xobj_id]=names
        return original_page(self,page)
    Typesetting.render_page=render_page
    original_passthrough = TypesettingUnit.passthrough
    def passthrough(self):
        result=original_passthrough(self)
        if self.formular:
            source=getattr(self.formular,'_reader_source',self.formular)
            pairs=[(a,b) for a,b in zip(source.pdf_character,self.formular.pdf_character)
                   if a.pdf_character_id is not None]
            # The parser also calls an unencoded prose ligature a "formula".
            # Its faulty visual bbox may cover neighboring English prose.
            # Only collect original rule geometry for real math-font content or
            # vertically stacked digits, not ordinary prose-font ligatures.
            has_math_font=any(CURRENT_MATH_FONTS.get(a.xobj_id,CURRENT_MATH_FONTS.get(None,{})).get(a.pdf_style.font_id,False) for a,b in pairs)
            stacked_digits=any(not a.vertical and not c.vertical and a.char_unicode.isdigit() and c.char_unicode.isdigit()
                and min(a.box.x2,c.box.x2)>max(a.box.x,c.box.x)
                and abs(a.box.y-c.box.y)>1 for i,(a,b) in enumerate(pairs)
                for c,d in pairs[i+1:])
            if not has_math_font and not stacked_digits:
                return result
            if pairs:
                first,last=pairs[0]
                scale=last.pdf_style.font_size/first.pdf_style.font_size
                dx=last.box.x-first.box.x*scale;dy=last.box.y-first.box.y*scale
                for a,b in pairs:
                    if abs(b.box.x-(a.box.x*scale+dx))>1e-3 or abs(b.box.y-(a.box.y*scale+dy))>1e-3:
                        raise ValueError('Formula geometry changed non-affinely; retain original instead')
                boxes=[a.visual_bbox.box if a.visual_bbox else a.box for a,b in pairs]
                bbox=[min(b.x for b in boxes),min(b.y for b in boxes),
                      max(b.x2 for b in boxes),max(b.y2 for b in boxes)]
                OVERLAYS.append({'page':CURRENT_PAGE,'sourceBox':bbox,'scale':scale,
                                 'dx':dx,'dy':dy,'glyphs':len(pairs)})
                for before,after in pairs:
                    if (before.char_unicode or '').isspace():
                        continue
                    names=CURRENT_FONT_NAMES.get(before.xobj_id,CURRENT_FONT_NAMES.get(None,{}))
                    EXPECTED_GLYPHS.append({'page':CURRENT_PAGE,'font':names.get(before.pdf_style.font_id),
                        'fontSize':after.pdf_style.font_size,'vertical':bool(after.vertical),
                        'x':after.box.x2 if after.vertical else after.box.x,'y':after.box.y})
        return result
    TypesettingUnit.passthrough=passthrough
    from babeldoc.document_il.backend.pdf_creater import PDFCreater
    original_write = PDFCreater.write

    def write(self, translation_config, *args, **kwargs):
        # A missing scope previously caused a silent `continue` in PDFCreater,
        # dropping the actual glyph. Reject that condition before output.
        errors = []
        for page in self.docs.page:
            base = {f.font_id for f in page.pdf_font} | set(self.font_mapper.fontid2font)
            forms = {f.xobj_id: base | {font.font_id for font in f.pdf_font}
                     for f in page.pdf_xobject}
            characters = list(page.pdf_character)
            for paragraph in page.pdf_paragraph:
                characters.extend(self.render_paragraph_to_char(paragraph))
            for char in characters:
                if char.pdf_character_id is None or char.char_unicode == '\n':
                    continue
                if char.pdf_style.font_id not in forms.get(char.xobj_id, base):
                    errors.append({'page':page.page_number+1,'font':char.pdf_style.font_id,
                                   'scope':char.xobj_id})
                CURRENT['validatedGlyphs'] += 1
            for item in [page, *page.pdf_xobject]:
                if item.base_operations:
                    item.base_operations.value = normalize_matrices(item.base_operations.value)
        CURRENT['unresolvedFontScopes'] = errors
        CURRENT['positionedMathFragments'] = len(OVERLAYS)
        CURRENT['status'] = 'FAIL' if errors else 'PASS'
        if AUDIT_PATH:
            AUDIT_PATH.parent.mkdir(parents=True,exist_ok=True)
            AUDIT_PATH.write_text(json.dumps(CURRENT,ensure_ascii=False,indent=2)+'\n')
            AUDIT_PATH.with_suffix('.overlays.json').write_text(json.dumps(OVERLAYS,ensure_ascii=False)+'\n')
            AUDIT_PATH.with_suffix('.glyphs.json').write_text(json.dumps(EXPECTED_GLYPHS,ensure_ascii=False)+'\n')
        if errors:
            raise ValueError('Unresolved original font scope; output blocked; see math audit')
        return original_write(self,translation_config,*args,**kwargs)

    PDFCreater.write = write


def restore_strokes(mono, source_path):
    """Move original mathematical rule strokes with the protected glyph unit.

    Copy only observed black horizontal strokes, not rectangular text clips:
    tall glyph metric boxes can also contain neighboring ordinary prose.
    Glyphs themselves are preserved by the font-scope and geometry guards.
    """
    import fitz
    source=fitz.open(source_path);dest=fitz.open(stream=mono,filetype='pdf')
    drawings={i:page.get_drawings() for i,page in enumerate(source)}
    count=0;seen=set();proof=[]
    for item in OVERLAYS:
        page=item['page'];height=source[page].rect.height
        x0,y0,x1,y1=item['sourceBox'];s=item['scale'];dx=item['dx'];dy=item['dy']
        original=fitz.Rect(x0-.15,height-y1-.15,x1+.15,height-y0+.15)
        for drawing_id,drawing in enumerate(drawings[page]):
            color=drawing.get('color')
            for segment_id,segment in enumerate(drawing['items']):
                if segment[0]=='re' and drawing.get('fill') is not None and max(drawing['fill'])<=.2:
                    rect=segment[1]
                    if not (0<rect.height<=.8 and rect.width>max(.1,rect.height)) or not original.contains(rect):
                        continue
                    target=fitz.Rect(rect.x0*s+dx,height-((height-rect.y0)*s+dy),
                                     rect.x1*s+dx,height-((height-rect.y1)*s+dy))
                    key=(page,drawing_id,segment_id,*[round(v,4) for v in target])
                    if key not in seen:
                        if not dest[page].rect.contains(target):
                            raise ValueError('Math rule outside page; do not silently clip it')
                        seen.add(key);dest[page].draw_rect(target,color=None,fill=drawing['fill'],overlay=True)
                        proof.append({'page':page,'kind':'filled-rule','source':list(rect),'target':list(target),'scale':s});count+=1
                    continue
                if color is None or max(color)>.2:
                    continue
                if segment[0]!='l':
                    continue
                a,b=segment[1:]
                if abs(a.y-b.y)>.01 or abs(a.x-b.x)<.1:
                    continue
                if not original.contains(a) or not original.contains(b):
                    continue
                aa=fitz.Point(a.x*s+dx,height-((height-a.y)*s+dy))
                bb=fitz.Point(b.x*s+dx,height-((height-b.y)*s+dy))
                key=(page,drawing_id,segment_id,round(aa.x,4),round(aa.y,4),round(bb.x,4),round(bb.y,4))
                if key in seen:
                    continue
                if not dest[page].rect.contains(aa) or not dest[page].rect.contains(bb):
                    raise ValueError('Math stroke outside page; do not silently clip it')
                seen.add(key)
                dest[page].draw_line(aa,bb,color=color,width=drawing['width']*s,
                    stroke_opacity=drawing.get('stroke_opacity',1),overlay=True)
                proof.append({'page':page,'source':[list(a),list(b)],'target':[list(aa),list(bb)],
                              'sourceWidth':drawing['width'],'scale':s})
                count+=1
    data=dest.tobytes(garbage=3,deflate=True);source.close();dest.close()
    CURRENT['originalMathStrokesRestored']=count
    if AUDIT_PATH:
        AUDIT_PATH.write_text(json.dumps(CURRENT,ensure_ascii=False,indent=2)+'\n')
        AUDIT_PATH.with_suffix('.strokes.json').write_text(json.dumps(proof,ensure_ascii=False)+'\n')
    return data
