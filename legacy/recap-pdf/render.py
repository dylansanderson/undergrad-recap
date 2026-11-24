import re, sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Preformatted, Table, TableStyle, KeepTogether, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents

SRC, OUT = sys.argv[1], sys.argv[2]
F = r'C:\Windows\Fonts\\'
pdfmetrics.registerFont(TTFont('Body', F + 'segoeui.ttf'))
pdfmetrics.registerFont(TTFont('Body-B', F + 'segoeuib.ttf'))
pdfmetrics.registerFont(TTFont('Body-I', F + 'segoeuii.ttf'))
pdfmetrics.registerFont(TTFont('Body-SB', F + 'seguisb.ttf'))
pdfmetrics.registerFont(TTFont('Mono', F + 'consola.ttf'))
pdfmetrics.registerFont(TTFont('Sym', F + 'seguisym.ttf'))
pdfmetrics.registerFont(TTFont('Math', F + 'cambria.ttc', subfontIndex=1))
from reportlab.lib.fonts import addMapping
addMapping('Body', 0, 0, 'Body'); addMapping('Body', 1, 0, 'Body-B')
addMapping('Body', 0, 1, 'Body-I'); addMapping('Body', 1, 1, 'Body-B')

def cmap(name):
    return set(pdfmetrics.getFont(name).face.charToGlyph.keys())
BODY_CM, MONO_CM, SYM_CM, MATH_CM = cmap('Body'), cmap('Mono'), cmap('Sym'), cmap('Math')

def fallback(text, primary_cm):
    out, i = [], 0
    for ch in text:
        o = ord(ch)
        if o < 128 or o in primary_cm:
            out.append(ch)
        elif o in MATH_CM:
            out.append(f'<font name="Math">{ch}</font>')
        elif o in SYM_CM:
            out.append(f'<font name="Sym">{ch}</font>')
        else:
            out.append(ch)
    return ''.join(out)

INK = colors.HexColor('#1b2333'); ACCENT = colors.HexColor('#2b5cab'); SOFT = colors.HexColor('#eef3fb')
MUTED = colors.HexColor('#5d6778'); CODEBG = colors.HexColor('#f4f5f7'); RULE = colors.HexColor('#c9d5ea')

ss = dict(
    body=ParagraphStyle('body', fontName='Body', fontSize=9.6, leading=13.6, textColor=INK, spaceBefore=3, spaceAfter=5),
    bullet=ParagraphStyle('bullet', fontName='Body', fontSize=9.6, leading=13.4, textColor=INK, leftIndent=14, bulletIndent=3, spaceAfter=2.5),
    h1=ParagraphStyle('h1', fontName='Body-B', fontSize=20, leading=24, textColor=INK, spaceAfter=10),
    h2=ParagraphStyle('h2', fontName='Body-SB', fontSize=12.5, leading=16, textColor=ACCENT, spaceBefore=9, spaceAfter=4),
    sem=ParagraphStyle('sem', fontName='Body-B', fontSize=30, leading=36, textColor=colors.white),
    code=ParagraphStyle('code', fontName='Mono', fontSize=8.2, leading=10.6, textColor=INK),
    toc0=ParagraphStyle('toc0', fontName='Body-B', fontSize=11, leading=15, textColor=ACCENT, spaceBefore=8),
    toc1=ParagraphStyle('toc1', fontName='Body', fontSize=10, leading=14, leftIndent=14, textColor=INK),
)

def inline(t, cm=BODY_CM):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`', lambda m: f'<font name="Mono" size="8.6" color="#8a2b52">{m.group(1)}</font>', t)
    return fallback(t, cm)

class SemesterBand(Flowable):
    def __init__(self, text): super().__init__(); self.text = text
    def wrap(self, aw, ah): self.aw = aw; return aw, 1.6 * inch
    def draw(self):
        c = self.canv
        c.setFillColor(ACCENT); c.roundRect(0, 0, self.aw, 1.5 * inch, 8, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont('Body-B', 34); c.drawString(24, 0.62 * inch, self.text.title())
        c.setFont('Body', 11); c.drawString(26, 0.35 * inch, 'Semester')

class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='f')
        self.addPageTemplates([PageTemplate('cover', [frame], onPage=lambda c, d: None),
                               PageTemplate('main', [frame], onPageEnd=self.deco)])
        self.current = ''
    def beforeDocument(self):
        self.current = ''
    def deco(self, c, d):
        c.saveState()
        c.setStrokeColor(RULE); c.setLineWidth(0.6)
        c.line(self.leftMargin, letter[1] - 0.55 * inch, letter[0] - self.rightMargin, letter[1] - 0.55 * inch)
        c.setFont('Body', 8); c.setFillColor(MUTED)
        c.drawString(self.leftMargin, letter[1] - 0.48 * inch, 'Undergrad Recap · Computer Engineering, CSUF')
        c.drawRightString(letter[0] - self.rightMargin, letter[1] - 0.48 * inch, self.current)
        c.drawCentredString(letter[0] / 2, 0.45 * inch, str(d.page))
        c.restoreState()
    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ('h1', 'semp'):
            txt = f.getPlainText()
            key = 'k%d' % id(f)
            self.canv.bookmarkPage(key)
            lvl = 0 if (f.style.name == 'semp' or txt.startswith('How to') or txt.startswith('The big')) else 1
            self.canv.addOutlineEntry(txt, key, level=lvl)
            if f.style.name == 'h1': self.current = txt
            self.notify('TOCEntry', (lvl, txt, self.page, key))

lines = open(SRC, encoding='utf-8').read().splitlines()
story = []
title = sub = ''
i = 0
para = []
def flush():
    global para
    if para:
        story.append(Paragraph(inline(' '.join(para)), ss['body'])); para = []

semp = ParagraphStyle('semp', parent=ss['body'], fontSize=1, leading=1, textColor=colors.white)
first_h1 = True
while i < len(lines):
    ln = lines[i]
    if ln.startswith('%% '): sub = ln[3:]; i += 1; continue
    if ln.startswith('% '): title = ln[2:]; i += 1; continue
    if ln.startswith('```'):
        flush(); i += 1; code = []
        while not lines[i].startswith('```'): code.append(lines[i]); i += 1
        i += 1
        txt = '<br/>'.join(fallback(c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), MONO_CM).replace(' ', '&nbsp;') for c in code)
        t = Table([[Paragraph(txt, ss['code'])]], colWidths=['100%'])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), CODEBG), ('BOX', (0, 0), (-1, -1), 0.5, RULE),
                               ('LEFTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
        story += [t, Spacer(1, 6)]
        continue
    if ln.startswith('# '):
        flush(); h = ln[2:].strip()
        if re.fullmatch(r'(SPRING|FALL) \d{4}', h):
            story += [PageBreak(), Spacer(1, 2.6 * inch), Paragraph(h.title(), semp), SemesterBand(h)]
        else:
            if first_h1:
                # cover + TOC before first content heading
                first_h1 = False
            story += [PageBreak(), Paragraph(inline(h), ss['h1']),
                      Table([['']], colWidths=['100%'], rowHeights=[2], style=[('BACKGROUND', (0, 0), (-1, -1), ACCENT)]), Spacer(1, 8)]
        i += 1; continue
    if ln.startswith('## '):
        flush(); story.append(Paragraph(inline(ln[3:]), ss['h2'])); i += 1; continue
    if ln.startswith('- '):
        flush(); story.append(Paragraph(inline(ln[2:]), ss['bullet'], bulletText='•')); i += 1; continue
    if not ln.strip():
        flush(); i += 1; continue
    para.append(ln.strip()); i += 1
flush()

# cover
cover = [Spacer(1, 2.3 * inch),
         Paragraph('COURSEWORK RETROSPECTIVE', ParagraphStyle('k', fontName='Body-SB', fontSize=11, textColor=ACCENT, leading=14)),
         Spacer(1, 8),
         Paragraph(title, ParagraphStyle('t', fontName='Body-B', fontSize=44, leading=50, textColor=INK)),
         Spacer(1, 10),
         Paragraph(inline(sub), ParagraphStyle('s', fontName='Body', fontSize=13, leading=18, textColor=MUTED)),
         Spacer(1, 26),
         Table([['']], colWidths=[1.4 * inch], rowHeights=[4], style=[('BACKGROUND', (0, 0), (-1, -1), ACCENT)], hAlign='LEFT'),
         Spacer(1, 18),
         Paragraph('A course-by-course review of everything in the Coursework folder: what you did in each class, '
                   'the core material re-taught (including what your notes don\'t cover), and how it all connects.',
                   ParagraphStyle('d', fontName='Body', fontSize=11, leading=16, textColor=INK)),
         Spacer(1, 1.6 * inch),
         Paragraph('Prepared November 2026 from 21 course folders, ~400 documents and project files.',
                   ParagraphStyle('f', fontName='Body-I', fontSize=9, textColor=MUTED))]
from reportlab.platypus.doctemplate import NextPageTemplate
toc = TableOfContents(); toc.levelStyles = [ss['toc0'], ss['toc1']]; toc.dotsMinLevel = 0
front = cover + [NextPageTemplate('main'), PageBreak(), Paragraph('Contents', ParagraphStyle('h1toc', parent=ss['h1'])), Spacer(1, 6), toc]
# drop leading PageBreak of first content item (we already broke after TOC)
doc = Doc(OUT, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch, bottomMargin=0.75 * inch,
          title='Undergrad Recap', author='Dylan Sanderson', subject='Computer Engineering coursework recap')
doc.multiBuild(front + story)
print('pages:', doc.page)
