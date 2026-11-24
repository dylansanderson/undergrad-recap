import os, sys, re, hashlib, json
from pypdf import PdfReader
import docx, pptx

ROOT = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

SKIP_DIRS = re.compile(r'(\.gradle|\.idea|\\build\\|\.metadata|\.Xil|\.cache|\.runs|\.sim|\.hw|ip_user_files|\\Debug|\\Release|intermediates|generated|\.settings|_Software|_Cleanup|\\Licenses)', re.I)
DOC_EXT = {'.pdf', '.docx', '.pptx', '.pptm', '.txt', '.md'}
CODE_EXT = {'.c', '.h', '.cpp', '.java', '.v', '.vhd', '.asm', '.s', '.sql', '.py', '.r', '.m', '.xdc', '.tcl', '.sh', '.ps1'}
PER_DOC = 2500
PER_CODE = 900
MAX_PDF_PAGES = 25

def pdf_text(p):
    r = PdfReader(p)
    n = len(r.pages)
    out = []
    for pg in r.pages[:MAX_PDF_PAGES]:
        try: out.append(pg.extract_text() or '')
        except Exception: pass
    return f'[{n} pages] ' + '\n'.join(out)

def docx_text(p):
    d = docx.Document(p)
    t = [x.text for x in d.paragraphs if x.text.strip()]
    for tb in d.tables:
        for row in tb.rows:
            t.append(' | '.join(c.text.strip() for c in row.cells))
    return '\n'.join(t)

def pptx_text(p):
    pr = pptx.Presentation(p)
    out = []
    for i, s in enumerate(pr.slides, 1):
        parts = []
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                parts.append(sh.text_frame.text.strip())
        out.append(f'--slide {i}: ' + ' / '.join(parts))
    return '\n'.join(out)

seen = set()
stats = {}
for top in sorted(os.listdir(ROOT)):
    tp = os.path.join(ROOT, top)
    if not os.path.isdir(tp) or top.startswith('_Software') or top.startswith('_Cleanup'):
        continue
    buf = []
    nfiles = 0
    for dp, dns, fns in os.walk(tp):
        if SKIP_DIRS.search(dp + '\\'):
            dns[:] = []
            continue
        for fn in sorted(fns):
            fp = os.path.join(dp, fn)
            ext = os.path.splitext(fn)[1].lower()
            if fn.endswith('_summary.pdf'):
                continue
            if ext not in DOC_EXT and ext not in CODE_EXT:
                continue
            size = os.path.getsize(fp)
            rel = os.path.relpath(fp, tp)
            if size > 8_000_000:
                buf.append(f'\n=== {rel} (SKIPPED large file {size//1_000_000}MB, likely textbook)\n')
                continue
            try:
                with open(fp, 'rb') as f: h = hashlib.md5(f.read()).hexdigest()
                if h in seen: continue
                seen.add(h)
                if ext == '.pdf': t = pdf_text(fp)
                elif ext == '.docx': t = docx_text(fp)
                elif ext in ('.pptx', '.pptm'): t = pptx_text(fp)
                else:
                    with open(fp, 'r', encoding='utf-8', errors='replace') as f: t = f.read()
            except Exception as e:
                t = f'(extract failed: {e})'
            t = re.sub(r'[ \t]+', ' ', t)
            t = re.sub(r'\n\s*\n+', '\n', t).strip()
            if 'targetConfigs' in rel or fn in ('Compile_Options.txt', 'TempBreakPointFile.txt', 'htr.txt'):
                continue
            lim = PER_CODE if ext in CODE_EXT else PER_DOC
            buf.append(f'\n=== {rel} ({len(t)} chars)\n{t[:lim]}')
            nfiles += 1
    with open(os.path.join(OUT, top + '.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(buf))
    stats[top] = (nfiles, sum(len(b) for b in buf))
for k, v in stats.items():
    print(f'{k}: {v[0]} files, {v[1]} chars')
