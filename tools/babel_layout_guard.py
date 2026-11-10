"""Keep prose glyphs grazing a formula box in their actual text region."""
from copy import copy

VERSION = 'text-region-center-v1'
COUNTS = {}


def install():
    from babeldoc.document_il.midend.paragraph_finder import ParagraphFinder
    from babeldoc.document_il.utils.layout_helper import Layout
    global COUNTS
    COUNTS = {'guard': VERSION, 'reassignedBorderCharacters': 0}
    if getattr(ParagraphFinder.get_layout, '_reader_center_guard', False):
        return
    original = ParagraphFinder.get_layout

    def select(self, char, page):
        result = original(self, char, page)
        if result is None or self.is_text_layout(result):
            return result
        box = char.visual_bbox.box
        x, y = (box.x + box.x2) / 2, (box.y + box.y2) / 2
        centered = [layout for layout in page.page_layout
                    if layout.box.x <= x <= layout.box.x2 and layout.box.y <= y <= layout.box.y2]
        if not any(self.is_text_layout(Layout(layout.id, layout.class_name)) for layout in centered):
            return result
        scoped = copy(page)
        scoped.page_layout = centered
        selected = original(self, char, scoped)
        if selected != result:
            COUNTS['reassignedBorderCharacters'] += 1
        return selected

    select._reader_center_guard = True
    ParagraphFinder.get_layout = select
