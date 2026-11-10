#!/usr/bin/env python3
"""Translate reader PDFs with fixed page geometry; originals are never written.

Use the isolated, pinned pdf2zh environment recorded in the task's CHG/TEST.
PDFs/cache/complete extracted text stay local; only provenance enters Git.
"""
from __future__ import annotations
import argparse, ast, datetime, hashlib, importlib.metadata, json, os, re, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUX = ROOT.parent / 'analysis-source-audit/paper-zh-20261109'
OUTPUT = ROOT / '阅读转换件/论文中文'
MANIFEST = ROOT / '说明/paper-translations.json'
RUNTIME = ROOT / '网页/paper-translations.js'
JS_GLOBAL = 'READER_PAPER_TRANSLATIONS'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    import uuid
    temporary = path.with_suffix(path.suffix + '.tmp-' + uuid.uuid4().hex)
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def prepare():
    AUX.mkdir(parents=True, exist_ok=True)
    for key, path in {
        'PDF2ZH_CACHE_DIR': AUX/'cache/pdf2zh',
        'PDF2ZH_CONFIG_PATH': AUX/'cache/config.json',
        'BABELDOC_CACHE_DIR': AUX/'cache/babeldoc',
        'HF_HOME': AUX/'cache/huggingface',
    }.items():
        os.environ[key] = str(path)
    os.environ.setdefault('OMP_NUM_THREADS', '2')
    (AUX/'cache').mkdir(exist_ok=True)
    import requests
    original_request = requests.sessions.Session.request
    def bounded(self, method, url, **kwargs):
        kwargs.setdefault('timeout', (12, 40))
        return original_request(self, method, url, **kwargs)
    requests.sessions.Session.request = bounded
    import pdf2zh.high_level as high
    import pdf2zh.converter as converter
    import tenacity
    converter.retry = lambda **kw: tenacity.retry(
        stop=tenacity.stop_after_attempt(2), reraise=True,
        retry=tenacity.retry_if_exception_type((requests.Timeout, requests.ConnectionError)), **kw)
    from pdf2zh.config import ConfigManager
    # Extract the installed SC face; no font/model data is committed.
    font_path = AUX/'cache/NotoSerifCJKsc-Regular.otf'
    if not font_path.exists():
        from fontTools.ttLib import TTCollection
        collection = TTCollection('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc')
        font = next(f for f in collection.fonts if 'SC' in (f['name'].getDebugName(1) or ''))
        font.save(font_path)
    ConfigManager.set('NOTO_FONT_PATH', str(font_path))
    from pdf2zh.translator import BingTranslator
    original_init = BingTranslator.__init__
    def initialize(self, *args, **kw):
        original_init(self, *args, **kw)
        self.add_cache_impact_parameters('protection', 'opaque-v1-prose-italic')
    BingTranslator.__init__ = initialize
    original_find = BingTranslator.find_sid
    local = threading.local()
    def find_sid(self):
        # Reuse the session token obtained by the library's normal public page
        # request. Never store or print it. No CAPTCHA or rate-limit bypass.
        current = getattr(local, 'sid', None)
        if current is None or time.monotonic() - local.sid_time > 300:
            local.sid = original_find(self)
            local.sid_time = time.monotonic()
        return local.sid
    BingTranslator.find_sid = find_sid
    def chunks(text, limit=850):
        remaining = text
        while len(remaining) > limit:
            # Prefer a sentence boundary, then a space; do not cut formula tokens.
            matches = list(re.finditer(r'[.!?;:]\s+|\s+', remaining[:limit]))
            pos = matches[-1].end() if matches else limit
            opening = remaining.rfind('{', 0, pos)
            if opening > remaining.rfind('}', 0, pos):
                pos = opening
            if pos == 0:
                raise ValueError('Unsplittable translation token')
            yield remaining[:pos]
            remaining = remaining[pos:]
        if remaining:
            yield remaining
    def translate_bounded(self, text):
        result = []
        encoded = re.sub(r'\{v(\d+)\}', lambda m: 'ZXQPM'+m[1].zfill(4)+'QXZ', text)
        for chunk in chunks(encoded):
            url, ig, iid, key, token = self.find_sid()
            response = self.session.post(
                f'{url}ttranslatev3?IG={ig}&IID={iid}',
                data={'fromLang': self.lang_in, 'to': self.lang_out, 'text': chunk,
                      'token': token, 'key': key}, headers=self.headers)
            response.raise_for_status()
            translated = response.json()[0]['translations'][0]['text']
            # A placeholder loss would silently remove mathematics. Fail instead.
            original_tokens = sorted(re.findall(r'ZXQPM\d+QXZ', chunk))
            actual_tokens = sorted(re.findall(r'ZXQPM\d+QXZ', translated))
            if original_tokens != actual_tokens:
                write_json(AUX/('placeholder-failure-'+str(threading.get_ident())+'.json'), {'source':chunk,'translation':translated,'expected':original_tokens,'actual':actual_tokens})
                # The service may omit a leading superscript marker or a math
                # delimiter. Translate the prose on either side separately and
                # splice the untouched tokens back in; never invent a formula.
                pieces = re.split(r'(ZXQPM\d+QXZ)', chunk)
                protected = []
                for piece in pieces:
                    if re.fullmatch(r'ZXQPM\d+QXZ', piece) or not re.search(r'[A-Za-z]{2}', piece):
                        protected.append(piece)
                        continue
                    response = self.session.post(
                        f'{url}ttranslatev3?IG={ig}&IID={iid}',
                        data={'fromLang':self.lang_in,'to':self.lang_out,'text':piece,
                              'token':token,'key':key},headers=self.headers)
                    response.raise_for_status()
                    protected.append(response.json()[0]['translations'][0]['text'])
                translated = ' '.join(protected)
                if sorted(re.findall(r'ZXQPM\d+QXZ', translated)) != original_tokens:
                    raise ValueError('Formula protection fallback failed')
            if re.search(r'[A-Za-z]{4}', chunk) and not re.search(r'[\u4e00-\u9fff]', translated):
                prose_words = re.findall(r'\b(?:the|is|are|with|that|this|we|our|to|for)\b', chunk.lower())
                if translated.strip() == chunk.strip() and len(chunk) > 90 and len(prose_words) >= 3:
                    write_json(AUX/('untranslated-'+str(threading.get_ident())+'.json'), {'source':chunk,'translation':translated})
                    raise ValueError('Long untranslated passage returned by service')
            result.append(translated.replace('延迟', '时延'))
        joined = ' '.join(result)
        return re.sub(r'ZXQPM(\d+)QXZ', lambda m: '{v'+str(int(m[1]))+'}', joined)
    BingTranslator.do_translate = translate_bounded
    # Long ordinary italic words are prose, not mathematical variables. Keep
    # equations/figures (layout class 0) and mathematical fonts untouched.
    from pdfminer.layout import LTChar
    receive = converter.TranslateConverter.receive_layout
    def receive_prose(self, page):
        word = []
        def flush():
            if len(word) >= 4 and all('Ital' in str(c.fontname) for c in word):
                layout = self.layout[page.pageid]
                h, w = layout.shape
                c = word[0]
                ix, iy = min(w-1,max(0,int(c.x0))), min(h-1,max(0,int(c.y0)))
                if layout[iy,ix] != 0:
                    for item in word:
                        item.fontname = str(item.fontname).replace('Italic','Roman').replace('Ital','Roman')
            word.clear()
        previous = None
        for item in page:
            if isinstance(item, LTChar) and re.fullmatch('[A-Za-z]', item.get_text()):
                if previous is not None and (abs(item.y0-previous.y0)>1 or item.x0-previous.x1>max(1,item.size*.35)):
                    flush()
                word.append(item)
                previous = item
            else:
                flush()
                previous = None
        flush()
        return receive(self,page)
    converter.TranslateConverter.receive_layout = receive_prose
    from babeldoc.assets.assets import get_doclayout_onnx_model_path
    import onnx, onnxruntime
    from pdf2zh.doclayout import OnnxModel
    model_path = get_doclayout_onnx_model_path()
    parsed = onnx.load(str(model_path))
    metadata = {d.key: d.value for d in parsed.metadata_props}
    model = OnnxModel.__new__(OnnxModel)
    model.model_path = str(model_path)
    model._stride = ast.literal_eval(metadata['stride'])
    model._names = ast.literal_eval(metadata['names'])
    options = onnxruntime.SessionOptions()
    options.intra_op_num_threads = 2
    options.inter_op_num_threads = 1
    model.model = onnxruntime.InferenceSession(str(model_path), sess_options=options,
                                              providers=['CPUExecutionProvider'])
    predict = model.predict
    model.paper_layouts = []
    def record_layout(image, **kw):
        values = predict(image, **kw)
        boxes = []
        for item in values[0].boxes:
            name = values[0].names[int(item.cls)]
            if name in ('figure','table','isolate_formula'):
                boxes.append({'kind':name,'bbox':[float(v) for v in item.xyxy],
                              'imageSize':[image.shape[1],image.shape[0]]})
        model.paper_layouts.append(boxes)
        return values
    model.predict = record_layout
    versions = {k: importlib.metadata.version(k) for k in
                ['pdf2zh', 'babeldoc', 'pymupdf', 'onnxruntime', 'tencentcloud-sdk-python-tmt']}
    write_json(AUX/'environment.json', {'versions': versions, 'font': str(font_path),
               'fontSHA': hashlib.sha256(font_path.read_bytes()).hexdigest(),
               'modelSHA': hashlib.sha256(Path(model_path).read_bytes()).hexdigest()})
    return high, model


def catalog():
    text = (ROOT/'网页/catalog.js').read_text()
    return json.loads(text.split('window.READER_CATALOG=', 1)[1].rstrip(';'))


def image_signatures(document):
    output = []
    for page in document:
        values = []
        for item in page.get_image_info(hashes=True):
            # MuPDF can enumerate an empty image left by a clipped PDF form.
            # It has neither pixels nor visible area and is not a changed figure.
            if item['width'] <= 0 or item['height'] <= 0:
                continue
            values.append({'bbox': [round(v, 3) for v in item['bbox']],
                           'width': item['width'], 'height': item['height'],
                           'digest': item['digest'].hex()})
        unique = {json.dumps(v,sort_keys=True):v for v in values}
        output.append([unique[k] for k in sorted(unique)])
    return output


def verify(paper, path):
    import fitz
    original = ROOT/paper['file']
    with fitz.open(original) as src, fitz.open(path) as dst:
        if len(src) != len(dst):
            raise ValueError('Page count changed')
        sizes = [list(p.rect) for p in src]
        if sizes != [list(p.rect) for p in dst]:
            raise ValueError('Page dimensions changed')
        images_unchanged = image_signatures(src) == image_signatures(dst)
        cjk = [len(re.findall(r'[\u4e00-\u9fff]', p.get_text())) for p in dst]
        if sum(cjk) < 200:
            raise ValueError('Translation has too little Chinese text')
        text = ''.join(p.get_text() for p in dst)
        if re.search(r'IRREPARABLE TRANSLATION ERROR|\{v\d+\}|\ufffd', text):
            raise ValueError('Unresolved translation/formula placeholder')
        return {'pages': len(dst), 'pageSizes': sizes, 'chineseCharsPerPage': cjk,
                'rasterImagesAndPlacementUnchanged': images_unchanged,
                'warnings': [] if images_unchanged else [
                    'Raster image content or placement differs; draft preview allowed by user; not visually certified.'],
                'sourceSHA': hashlib.sha256(original.read_bytes()).hexdigest(),
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'bytes': path.stat().st_size,
                'scope': 'Readable draft checks; image differences are warnings. Visual and semantic review remains separate.'}


def publish(manifest):
    # Preserve a review completed while the next paper was being generated.
    current = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for key, value in current.get('papers', {}).items():
        candidate = manifest['papers'].get(key, {})
        if (value.get('status') == 'ready' and value.get('visualQA') == 'passed'
            and candidate.get('status') != 'processing'
            and value.get('sourceSHA') == candidate.get('sourceSHA')
            and (ROOT/value.get('file','')).is_file()
            and hashlib.sha256((ROOT/value['file']).read_bytes()).hexdigest() == value.get('sha256')):
            manifest['papers'][key] = value
    write_json(MANIFEST, manifest)
    target = RUNTIME
    text = 'window.' + JS_GLOBAL + '=' + json.dumps(
        manifest, ensure_ascii=False, separators=(',', ':')) + ';\n'
    tmp = target.with_suffix('.js.tmp')
    tmp.write_text(text)
    tmp.replace(target)




def restore_original_figures(paper, mono, layouts):
    import fitz, math
    original = fitz.open(ROOT/paper['file'])
    translated = fitz.open(stream=mono,filetype='pdf')
    proof=[]
    for index, boxes in enumerate(layouts):
        for entry in boxes:
            if entry['kind'] not in ('figure','isolate_formula'):
                continue
            x0,y0,x1,y1=entry['bbox']
            rect=fitz.Rect(math.floor(x0)-1,math.floor(y0)-1,math.ceil(x1)+1,math.ceil(y1)+1)
            rect=rect & original[index].rect
            # Layout boxes may touch the first row of a caption. Keep both
            # source and translated captions outside the restored figure band.
            if entry['kind']=='figure':
                for document in (original,translated):
                    for block in document[index].get_text('dict')['blocks']:
                        if block['type']!=0:continue
                        for line in block['lines']:
                            text=''.join(v['text'] for v in line['spans']).strip()
                            box=fitz.Rect(line['bbox'])
                            if (re.match(r'^(?:Fig\.?|Figure|图)\s*\d',text) and
                                rect.y1-12 < box.y0 < rect.y1+3 and
                                box.x0 < rect.x1 and box.x1 > rect.x0):
                                rect.y1=min(rect.y1,math.floor(box.y0-.7))
            translated[index].draw_rect(rect,color=None,fill=(1,1,1),overlay=True)
            translated[index].show_pdf_page(rect,original,index,clip=rect,keep_proportion=False,overlay=True)
            proof.append({'page':index+1,'kind':entry['kind'],'bbox':list(rect)})
    if paper['id']=='P05':
        # Proper names remain original. The parser merged the VI heading with
        # Fig.9's caption; the corrected caption and separate original position
        # are restored explicitly, without moving the surrounding figure.
        author=fitz.Rect(90,84,540,109)
        translated[0].draw_rect(author,color=None,fill=(1,1,1),overlay=True)
        translated[0].show_pdf_page(author,original,0,clip=author,keep_proportion=False,overlay=True)
        page=translated[5]
        font=AUX/'cache/NotoSerifCJKsc-Regular.otf'
        page.insert_font(fontname='zhHeading',fontfile=str(font))
        page.insert_text((151,629.677),'VI. 结论',fontname='zhHeading',fontsize=9.5)
        # Detector's Fig.6 region touches the caption. Reinsert the complete
        # Chinese caption below the unchanged plot, inside its caption band.
        caption_page=translated[4]
        caption_page.draw_rect(fitz.Rect(314,164,566,180),color=None,fill=(1,1,1),overlay=True)
        caption_page.insert_font(fontname='zhCaption',fontfile=str(font))
        caption='图 6：请求—响应场景的往返时间（RTT）。'
        face=fitz.Font(fontfile=str(font))
        size=7.9701
        xpos=438.856-face.text_length(caption,fontsize=size)/2
        caption_page.insert_text((xpos,165.5456+face.ascender*size),caption,fontname='zhCaption',fontsize=size)

    translated.subset_fonts(fallback=True)
    data=translated.tobytes(garbage=3,deflate=True)
    write_json(AUX/'restored-regions'/(paper['id']+'.json'),proof)
    return data


def translate_with_babel(paper, model):
    from babel_math_guard import install
    install(AUX/'math-guards'/(paper['id']+'.json'),ROOT/paper['file'])
    from babeldoc.translation_config import TranslationConfig, WatermarkOutputMode
    from babeldoc.document_il.translator.translator import BaseTranslator
    from babeldoc.document_il.translator.cache import init_db
    from pdf2zh.translator import BingTranslator
    from babeldoc import high_level
    init_db()
    class Adapter(BaseTranslator):
        name = 'reader-bing-guard'
        def __init__(self):
            super().__init__('en','zh',False)
            self.model = 'bounded-bing'
            self.inner = BingTranslator('en','zh','')
        def translate(self, text, ignore_cache=False):
            # Normalize only proven ordinary typographic ligatures. Mathematical
            # placeholders and mathematical Unicode symbols remain untouched.
            for old,new in [('\ufb00','ff'),('\ufb01','fi'),('\ufb02','fl'),('\ufb03','ffi'),('\ufb04','ffl')]:
                text=text.replace(old,new)
            corrections = AUX/'corrections'/(paper['id']+'.json')
            custom = json.loads(corrections.read_text()) if corrections.exists() else {}
            output = custom.get(hashlib.sha256(text.encode()).hexdigest())
            if output is None:
                output = super().translate(text, ignore_cache)
            for old,new in [('中介接入控制','媒体接入控制'),('授予','授权'),('信心阶段','置信阶段'),('自信学习','置信学习'),('自信状态','置信状态'),('可信状态','置信状态')]:
                output = output.replace(old,new)
            return output
        def do_translate(self, text):
            return self.inner.translate(text)
        def do_llm_translate(self, text):
            raise NotImplementedError('No LLM/API credentials are used')
        def get_formular_placeholder(self, ident):
            return '{v'+str(ident)+'}'
    folder = AUX/'babel-output'/paper['id']
    folder.mkdir(parents=True,exist_ok=True)
    import numpy as np
    def handle_document(pages, document, config, save_debug_image):
        for page in pages:
            config.raise_if_cancelled()
            pix = document[page.page_number].get_pixmap(dpi=72)
            image = np.frombuffer(pix.samples, np.uint8).reshape(pix.height,pix.width,3)[:,:,::-1]
            result = model.predict(image)[0]
            save_debug_image(image,result,page.page_number+1)
            yield page,result
    model.handle_document = handle_document
    class NativeTableText:
        def handle_document(self, pages, document, config, save_debug_image):
            from babeldoc.docvision.doclayout import YoloBox, YoloResult
            import fitz
            for page in pages:
                index=page.page_number
                tables=[fitz.Rect(v['bbox']) for v in model.paper_layouts[index] if v['kind']=='table']
                boxes=[]
                for block in document[index].get_text('dict')['blocks']:
                    if block['type']!=0:continue
                    for line in block['lines']:
                        rect=fitz.Rect(line['bbox'])
                        center=fitz.Point((rect.x0+rect.x1)/2,(rect.y0+rect.y1)/2)
                        if any(center in table for table in tables):
                            boxes.append(YoloBox(xyxy=np.asarray(list(rect),dtype=np.float32),
                                                conf=np.float32(.99),cls=0))
                result=YoloResult(names={0:'table_text'},boxes=boxes)
                yield page,result
    config = TranslationConfig(translator=Adapter(),input_file=ROOT/paper['file'],
                lang_in='en',lang_out='zh',doc_layout_model=model,
                output_dir=folder,working_dir=AUX/'babel-working'/paper['id'],
                no_dual=True,disable_rich_text_translate=True,qps=3,table_model=NativeTableText(),
                watermark_output_mode=WatermarkOutputMode.NoWatermark,
                use_rich_pbar=False,skip_scanned_detection=True)
    config._is_temp_dir = False  # retain explicit working directory as failure evidence
    result = high_level.translate(config)
    from babel_math_guard import restore_strokes
    return restore_strokes(Path(result.mono_pdf_path).read_bytes(),ROOT/paper['file'])


def run(args):
    papers = [p for p in catalog()['papers'] if p['id'] != 'book']
    priority = {'P05':0,'P01':1,'P31':2,'P24':3}
    papers.sort(key=lambda p: (priority.get(p['id'],4), p['id']))
    language = {v['id']: v for v in json.loads((AUX/'language-audit.json').read_text())}
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    manifest = {'version': 1, 'updated': datetime.date.today().isoformat(), 'papers': old.get('papers', {}),
                'excluded': ['book'], 'translationType': 'machine',
                'layoutScope': 'Original page size; translated text reflows. User accepts figure-placement differences for draft preview.'}
    if args.publish_existing:
        selected = set(args.only.split(',')) if args.only else None
        if not selected:
            raise ValueError('--publish-existing requires explicit --only paper IDs')
        if selected - {p['id'] for p in papers}:
            raise ValueError('Unknown paper ID in --only')
        for paper in papers:
            ident = paper['id']
            if ident not in selected:
                continue
            candidate = AUX/(ident + '.unverified.pdf')
            source_sha = hashlib.sha256((ROOT/paper['file']).read_bytes()).hexdigest()
            if manifest['papers'].get(ident, {}).get('sourceSHA') != source_sha:
                raise ValueError('Candidate source identity is not recorded: ' + ident)
            proof = verify(paper, candidate)
            target = OUTPUT/(ident + '.zh.pdf')
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix('.pdf.tmp')
            temporary.write_bytes(candidate.read_bytes())
            temporary.replace(target)
            write_json(AUX/'checks'/(ident+'.json'), proof)
            manifest['papers'][ident] = {**proof, 'status': 'generated',
                'file': str(target.relative_to(ROOT)), 'visualQA': 'pending',
                'publicationNote': 'Existing candidate published on user request; image placement does not block preview.'}
            publish(manifest)
            print('PUBLISHED ' + ident + ' ' + str(proof['pages']) + ' pages', flush=True)
        return
    if args.verify:
        proof = {}
        for paper in papers:
            entry = manifest['papers'].get(paper['id'], {})
            if entry.get('status') in ('generated', 'ready'):
                proof[paper['id']] = verify(paper, ROOT/entry['file'])
        write_json(AUX/'verification.json', proof)
        print(json.dumps({'verified': len(proof), 'expected': len(papers)}), flush=True)
        return
    high, model = prepare()
    if args.warmup:
        print('Layout model, Chinese font and bounded translator ready.', flush=True)
        return
    chosen = [p for p in papers if p['id'] == 'P05'] if args.pilot else papers
    if args.only:
        selected = set(args.only.split(','))
        chosen = [p for p in papers if p['id'] in selected]
        if len(chosen) != len(selected):raise ValueError('Unknown paper ID in --only')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    failures = []
    for paper in chosen:
        ident = paper['id']
        if ident not in language:
            # Newly registered local materials are not in the historical audit.
            # Inspect their actual first pages instead of assuming a language.
            import fitz
            with fitz.open(ROOT/paper['file']) as document:
                sample = '\n'.join(p.get_text() for p in list(document)[:3])
            language[ident] = {'chinese_original': len(re.findall(r'[\u4e00-\u9fff]', sample)) > max(200, len(sample)*.25)}
        if language[ident]['chinese_original']:
            manifest['papers'][ident] = {'status': 'original-chinese'}
            publish(manifest)
            continue
        target = OUTPUT/(ident + '.zh.pdf')
        sourceSHA = hashlib.sha256((ROOT/paper['file']).read_bytes()).hexdigest()
        entry = manifest['papers'].get(ident, {})
        if not args.force and target.exists() and entry.get('sourceSHA') == sourceSHA:
            from babel_math_guard import GUARD_VERSION
            if not getattr(args,'repair_math',False) or entry.get('mathGuard') == GUARD_VERSION:
                verify(paper, target)
                print(ident + ' already generated and structurally verified.', flush=True)
                continue
        print('START ' + ident + ' ' + str(paper['pages']) + ' pages', flush=True)
        started = time.monotonic()
        manifest['papers'][ident] = {'status': 'processing', 'sourceSHA': sourceSHA}
        publish(manifest)
        stage = 'Source read'
        try:
            source = (ROOT/paper['file']).read_bytes()
            model.paper_layouts.clear()
            # Use the stream API: no library path cleanup, no mutation of originals.
            if args.engine == 'babel':
                mono = translate_with_babel(paper, model)
            else:
                mono, _ = high.translate_stream(source, lang_in='en', lang_out='zh',
                           service='bing', thread=3, model=model)
            stage = 'Translation PDF generated'
            mono = restore_original_figures(paper, mono, model.paper_layouts)
            stage = 'Original figure/formula regions restored'
            temporary = AUX/(ident + '.unverified.pdf')
            temporary.write_bytes(mono)
            write_json(AUX/'layouts'/(ident+'.json'), model.paper_layouts)
            proof = verify(paper, temporary)
            stage = 'Readable draft checks completed'
            output_tmp = target.with_suffix('.pdf.tmp')
            output_tmp.write_bytes(temporary.read_bytes())
            output_tmp.replace(target)
            # The temporary is retained as generation evidence until final QA.
            proof['seconds'] = time.monotonic() - started
            proof['engine'] = args.engine
            if args.engine == 'babel':
                from babel_math_guard import GUARD_VERSION
                audit = json.loads((AUX/'math-guards'/(ident+'.json')).read_text())
                if audit['status'] != 'PASS':
                    raise ValueError('Math font scope audit failed')
                proof['mathGuard'] = GUARD_VERSION
                audit.update(sourceSHA=sourceSHA,translationSHA=proof['sha256'])
                write_json(AUX/'math-guards'/(ident+'.json'),audit)
            write_json(AUX/'checks'/(ident+'.json'), proof)
            manifest['papers'][ident] = {**proof, 'status': 'generated',
                    'file': str(target.relative_to(ROOT)), 'visualQA': 'pending'}
            publish(manifest)
            print('DONE ' + ident + ' ' + json.dumps({'seconds': round(proof['seconds'], 2),
                  'Chinese': sum(proof['chineseCharsPerPage'])}), flush=True)
        except Exception as exc:
            manifest['papers'][ident] = {'status': 'failed', 'sourceSHA': sourceSHA,
                'error': type(exc).__name__ + ': ' + str(exc)[:500]}
            publish(manifest)
            write_json(AUX/'failure.json', {'paper': ident, 'error': repr(exc),
                    'lastSuccessful': stage})
            write_json(AUX/'failures'/(ident+'.json'), {'paper': ident,
                'error': repr(exc), 'lastSuccessful': stage})
            failures.append(ident)
            if not args.all:
                raise
            print('FAILED ' + ident + ' at ' + stage + ': ' + type(exc).__name__, flush=True)
    if failures:
        raise RuntimeError('Batch completed with unpublished failures: ' + ','.join(failures))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--warmup', action='store_true')
    parser.add_argument('--pilot', action='store_true')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--publish-existing', action='store_true',
                        help='Publish existing local candidate PDFs selected by --only, without retranslating')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--repair-math', action='store_true',
                        help='Regenerate existing drafts missing the reviewed math font scope guard')
    parser.add_argument('--only', help='Comma-separated local paper IDs, e.g. P01,P24')
    parser.add_argument('--engine', choices=['pdf2zh','babel'], default='babel')
    options = parser.parse_args()
    if not any([options.warmup, options.pilot, options.all, options.verify, options.only, options.publish_existing]):
        parser.error('Choose --warmup, --pilot, --all or --verify')
    run(options)
