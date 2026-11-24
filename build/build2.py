"""Lecture video builder v2.
python build2.py [--only L01,L02] [--frames] [--out file.mp4] [--lessons-out DIR]
  --frames : render slide images only (no audio/video) for visual review
"""
import os, sys, re, json, glob, hashlib, subprocess, importlib.util, wave, argparse, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.pdfbase.ttfonts import TTFont

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ap = argparse.ArgumentParser()
ap.add_argument('--only'); ap.add_argument('--frames', action='store_true'); ap.add_argument('--out')
ap.add_argument('--lessons-out'); ap.add_argument('--course-root', help='write Lecture/Slides files into <root>/<lesson folder>/')
ap.add_argument('--credits', action='store_true', help='append image-credit pages to the combined video + write Image_Credits.txt')
ap.add_argument('--voice', default='af_heart'); ap.add_argument('--speed', type=float, default=1.0)
ARGS = ap.parse_args()

D = lambda *p: os.path.join(HERE, *p)
for sub in ('frames', 'figs', 'cache', 'segs', 'out'): os.makedirs(D(sub), exist_ok=True)
CRED = json.load(open(D('assets', 'credits.json'), encoding='utf-8')) if os.path.exists(D('assets', 'credits.json')) else {}
USED = {}   # asset key -> set of lesson tags that showed it

# ---------------- fonts & text ----------------
W, H = 1920, 1080
FD = 'C:\\Windows\\Fonts\\'
_fc = {}
def F(name, size):
    k = (name, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + name, size, index=1 if name == 'cambria.ttc' else 0)
    return _fc[k]
def cm(name, idx=0): return set(TTFont('x' + name + str(idx), FD + name, subfontIndex=idx).face.charToGlyph.keys())
CM = {n: cm(n, 1 if n == 'cambria.ttc' else 0) for n in ('segoeui.ttf', 'segoeuib.ttf', 'seguisb.ttf', 'consola.ttf', 'consolab.ttf', 'cambria.ttc', 'seguisym.ttf', 'malgun.ttf')}

FIGSCALE = 0.8   # figures are drawn smaller then scaled up -> larger, more readable text
BG = (247, 249, 252); INK = (27, 35, 51); ACC = (43, 92, 171); MUT = (93, 103, 120); CODEBG = (236, 240, 247); WHITE = (255, 255, 255)
ORANGE = (224, 123, 57); PALE = (220, 230, 248)

def runs(text, fname):
    out = []
    for ch in text:
        f = fname
        if ord(ch) >= 128 and ord(ch) not in CM[fname]:
            f = next((c for c in ('cambria.ttc', 'seguisym.ttf', 'malgun.ttf') if ord(ch) in CM[c]), 'seguisym.ttf')
        if out and out[-1][1] == f: out[-1][0] += ch
        else: out.append([ch, f])
    return out
def tlen(text, fname, size): return sum(F(f, size).getlength(s) for s, f in runs(text, fname))
def draw_text(d, xy, text, fname, size, fill):
    """draw runs on a shared baseline (fallback fonts have different ascents)"""
    x, y = xy
    base = y + F(fname, size).getmetrics()[0]
    for s, f in runs(text, fname):
        fo = F(f, size); d.text((x, base), s, font=fo, fill=fill, anchor='ls'); x += fo.getlength(s)
    return x

def rich_lines(text, size, maxw, base='segoeui.ttf', bold='segoeuib.ttf'):
    """**bold** spans; returns list of lines, each a list of (word, isbold)"""
    toks = []   # (word, bold, glued-to-previous)
    prev_space = True
    for i, part in enumerate(re.split(r'\*\*', text)):
        if not part: continue
        ws = part.split(' ')
        for j, w in enumerate(ws):
            if w: toks.append((w, i % 2 == 1, j == 0 and bool(toks) and not prev_space))
        prev_space = part.endswith(' ')
    # merge glued tokens into the previous token as a list of runs
    words = []
    for w, b, g in toks:
        if g and words: words[-1].append((w, b))
        else: words.append([(w, b)])
    lines, cur, curw = [], [], 0
    sp = F(base, size).getlength(' ')
    for wd in words:
        ww = sum(tlen(w, bold if b else base, size) for w, b in wd)
        if cur and curw + sp + ww > maxw:
            lines.append(cur); cur, curw = [], 0
        curw += (sp if cur else 0) + ww; cur.append(wd)
    if cur: lines.append(cur)
    return lines

REC = None   # when a list, slide drawing records where each text line / code line / figure landed (pen marks on ordinary slides)
def _rec_line(chars, y, size, kind):
    if REC is not None and chars:
        REC.append({'kind': kind, 't': ''.join(c for c, _, _ in chars), 'xs': [(a, b) for _, a, b in chars],
                    'y0': y + size * 0.14, 'y1': y + size * 1.2})

def draw_rich(d, x, y, lines, size, fill, lh, base='segoeui.ttf', bold='segoeuib.ttf', bcol=None):
    sp = F(base, size).getlength(' ')
    for ln in lines:
        xx = x; chars = []
        for wd in ln:
            for w, b in wd:
                f = bold if b else base
                if REC is not None:
                    for k, ch in enumerate(w): chars.append((ch, xx + tlen(w[:k], f, size), xx + tlen(w[:k + 1], f, size)))
                xx = draw_text(d, (xx, y), w, f, size, (bcol or ACC) if b else fill)
            if REC is not None: chars.append((' ', xx, xx + sp))
            xx += sp
        _rec_line(chars[:-1], y, size, 'text')
        y += lh
    return y

def plain(ln): return ' '.join(''.join(w for w, _ in wd) for wd in ln)

# ---------------- images ----------------
def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], radius=r, fill=255)
    return m

def place(canvas, src, box, card=False, shadow=True):
    """fit image into box (x0,y0,x1,y1) keeping aspect; returns placed rect"""
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    im = Image.open(src).convert('RGB')
    pad = 22 if card else 0
    s = min((bw - 2 * pad) / im.width, (bh - 2 * pad) / im.height)
    nw, nh = max(1, int(im.width * s)), max(1, int(im.height * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    cw, ch = nw + 2 * pad, nh + 2 * pad
    cx, cy = x0 + (bw - cw) // 2, y0 + (bh - ch) // 2
    if shadow:
        sh = Image.new('RGBA', (cw + 60, ch + 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([30, 36, cw + 30, ch + 36], radius=22, fill=(20, 30, 60, 55))
        sh = sh.filter(ImageFilter.GaussianBlur(14)); canvas.paste(sh, (cx - 30, cy - 30), sh)
    if card:
        cardim = Image.new('RGB', (cw, ch), WHITE)
        canvas.paste(cardim, (cx, cy), rounded(cardim, 22))
        ImageDraw.Draw(canvas).rounded_rectangle([cx, cy, cx + cw - 1, cy + ch - 1], radius=22, outline=(214, 223, 238), width=2)
        canvas.paste(im, (cx + pad, cy + pad))
    else:
        canvas.paste(im, (cx, cy), rounded(im, 18))
    return (cx, cy, cx + cw, cy + ch)

def credit_line(key):
    parts = []
    for k in key.split('+'):
        c = CRED.get(k)
        if not c: continue
        a = re.sub(r'\s+', ' ', c['artist'] or 'Unknown').strip()
        a = re.sub(r'^(Photo|Image)\s*(by|:)\s*', '', a, flags=re.I)
        if len(a) > 40: a = a[:38] + '…'
        parts.append(f'{a} · {c["license"]}')
    if not parts: return ''
    return ('Images: ' if len(parts) > 1 else 'Image: ') + ' | '.join(parts) + ' · Wikimedia Commons'

def resolve(mod, ref, box, tag):
    """ref: 'fig:name' | 'a:assetkey' | path -> (png path, is_figure, asset key)"""
    if ref.startswith('fig:'):
        name = ref[4:]; fn = getattr(mod, 'fig_' + name)
        fw, fh = int(box[2] - box[0] - 44), int(box[3] - box[1] - 44)
        out = D('figs', f'{tag}_{name}_{fw}x{fh}.png')
        fn(out, fw, fh)
        return out, True, None
    if ref.startswith('a:') and '+' in ref:
        keys = ref[2:].split('+'); ims = []
        for k in keys:
            p, _, _ = resolve(mod, 'a:' + k, box, tag); ims.append(Image.open(p).convert('RGB'))
        hh = min(im.height for im in ims); ims = [im.resize((int(im.width * hh / im.height), hh), Image.LANCZOS) for im in ims]
        gap = int(hh * 0.04); cw = sum(im.width for im in ims) + gap * (len(ims) - 1)
        comp = Image.new('RGB', (cw, hh), BG); x = 0
        for im in ims: comp.paste(im, (x, 0)); x += im.width + gap
        out = D('figs', f'comp_{h(ref)}.png'); comp.save(out)
        return out, False, '+'.join(k.split('|')[0] for k in keys)
    if ref.startswith('a:'):
        key, crop = (ref[2:].split('|') + [None])[:2]
        USED.setdefault(key, set()).add(tag)
        fs = glob.glob(D('assets', key + '.*')); fs = [f for f in fs if not f.endswith('.json')]
        if not fs: raise FileNotFoundError('asset ' + key)
        if crop:
            x0, y0, x1, y1 = map(float, crop.split(','))
            im = Image.open(fs[0]).convert('RGB'); w0, h0 = im.size
            out = D('figs', f'crop_{key}_{h(crop)}.png')
            im.crop((int(x0 * w0), int(y0 * h0), int(x1 * w0), int(y1 * h0))).save(out)
            return out, False, key
        return fs[0], False, key
    return ref, False, None

# ---------------- slide rendering ----------------
def chrome(d, L, idx, total, light=False):
    d.rectangle([0, 0, W, 84], fill=ACC)
    draw_text(d, (64, 18), L['code'], 'segoeuib.ttf', 36, WHITE)
    x = 64 + tlen(L['code'], 'segoeuib.ttf', 36) + 22
    draw_text(d, (x, 24), L.get('title', ''), 'segoeui.ttf', 30, (205, 218, 242))
    right = L.get('tag', '')
    if right:
        sw = tlen(right, 'segoeui.ttf', 28); draw_text(d, (W - 64 - sw, 26), right, 'segoeui.ttf', 28, (205, 218, 242))
    d.rectangle([0, H - 8, W, H], fill=(220, 227, 240)); d.rectangle([0, H - 8, int(W * idx / total), H], fill=ACC)

def heading(d, text, y=118, size=58, maxw=W - 200):
    lines = rich_lines(text, size, maxw, 'segoeuib.ttf', 'segoeuib.ttf')
    y = draw_rich(d, 100, y, lines, size, INK, int(size * 1.22), 'segoeuib.ttf', 'segoeuib.ttf')
    d.rectangle([100, y + 10, 210, y + 16], fill=ORANGE)
    return y + 44

def bullets(d, pts, x, y, maxw, nshow, size=42, cur=None, bottom=1000):
    lh = int(size * 1.32)
    # shrink to fit
    while size > 28:
        tot = sum(len(rich_lines(p, size, maxw - 60)) * lh + 26 for p in pts)
        if y + tot <= bottom: break
        size -= 2; lh = int(size * 1.32)
    for i, p in enumerate(pts):
        lines = rich_lines(p, size, maxw - 60)
        if i >= nshow:
            y += len(lines) * lh + 26; continue
        active = (cur is not None and i == cur)
        col = INK if (cur is None or active) else (110, 118, 134)
        r = 9 if active else 7
        cy = y + size * 0.62
        d.ellipse([x + 8 - r, cy - r, x + 8 + r, cy + r], fill=ORANGE if active else ACC)
        y = draw_rich(d, x + 44, y, lines, size, col, lh) + 26
    return y

def code_box(d, code, x0, y0, x1, y1, nshow=None):
    lines = code.split('\n'); size = 34
    while size > 20 and (max(tlen(l, 'consola.ttf', size) for l in lines) > (x1 - x0) - 80 or len(lines) * size * 1.42 > (y1 - y0) - 50):
        size -= 1
    lh = int(size * 1.42); hgt = lh * len(lines) + 56
    d.rounded_rectangle([x0, y0, x1, y0 + hgt], radius=18, fill=CODEBG, outline=(201, 213, 234), width=2)
    yy = y0 + 28
    for i, l in enumerate(lines):
        if nshow is not None and i >= nshow: break
        s = l.strip()
        col = (110, 120, 140) if s.startswith(('--', '//', '#')) else (ACC if s.startswith(('=>', '→')) else INK)
        if REC is not None:
            _rec_line([(ch, x0 + 40 + tlen(l[:k], 'consola.ttf', size), x0 + 40 + tlen(l[:k + 1], 'consola.ttf', size)) for k, ch in enumerate(l)],
                      yy, size, 'code')
        draw_text(d, (x0 + 40, yy), l, 'consola.ttf', size, col); yy += lh
    return y0 + hgt

WB_BOX = (64, None, W - 64, 1046)
def wb_frame(mod, L, s, beat, idx, total, upto):
    """whiteboard slide with the first `upto` board events revealed"""
    import board
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    chrome(d, L, idx, total)
    y = heading(d, s['h'], size=50) - 14
    x0, x1, y1 = WB_BOX[0], WB_BOX[2], WB_BOX[3]
    sh = Image.new('RGBA', (x1 - x0 + 60, y1 - y + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30, 34, x1 - x0 + 30, y1 - y + 34], radius=20, fill=(20, 30, 60, 40))
    sh = sh.filter(ImageFilter.GaussianBlur(12)); im.paste(sh, (x0 - 30, y - 30), sh)
    d.rounded_rectangle([x0, y, x1, y1], radius=20, fill=WHITE, outline=(206, 216, 232), width=2)
    bim = board.render(s, mod, beat, upto, x1 - x0 - 24, y1 - y - 24)
    im.paste(bim, (x0 + 12, y + 12)); board.LAST_OFF = (x0 + 12, y + 12)
    return im

def clip_box(y):
    return (760, y + 20, W - 90, 1030)

def clip_src(s):
    return D('assets', 'clips', s['clip'])

def clip_vf(s, bw_, bh_):
    c = s.get('crop')                                  # (w, h, x, y) region of the recording to show
    return (f"crop={c[0]}:{c[1]}:{c[2]}:{c[3]}," if c else '') + f"scale={bw_}:{bh_}:force_original_aspect_ratio=decrease"

def clip_still(s):
    p = D('frames', 'clipstill_' + h(s['clip'], json.dumps(s.get('crop')), s.get('still', 3)) + '.png')
    if not os.path.exists(p):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(s.get('ss', 0) + s.get('still', 3)), '-i', clip_src(s), '-frames:v', '1',
                        '-vf', clip_vf(s, 4000, 4000).split(',scale')[0] if s.get('crop') else 'null', p], check=True)
    return Image.open(p).convert('RGB')

def seg_clip(s, png, wav, dur):
    """slide frame + the recording playing (muted, looped if the narration is longer) inside the panel"""
    src = clip_src(s)
    sig = h(open(png, 'rb').read(), open(wav, 'rb').read(), f'{dur:.3f}', s['clip'], os.path.getsize(src), json.dumps(s.get('crop')), s.get('ss', 0), 'clip1')
    out = D('segs', sig + '.mp4')
    if os.path.exists(out): return out
    y = s['_y']; box = clip_box(y); bw_, bh_ = box[2] - box[0] - 16, box[3] - box[1] - 16
    fc = (f"[1:v]{clip_vf(s, bw_, bh_)},fps={FPS},setpts=PTS-STARTPTS[c];"
          f"[0:v][c]overlay=x={box[0] + 8}+({bw_}-overlay_w)/2:y={box[1] + 8}+({bh_}-overlay_h)/2[v]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', str(FPS), '-i', png,
                    '-stream_loop', '-1', '-ss', str(s.get('ss', 0)), '-i', src, '-i', wav,
                    '-filter_complex', fc, '-map', '[v]', '-map', '2:a', '-af', f'apad', '-t', f'{dur:.3f}',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                    '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-ac', '1', out], check=True)
    return out

def render(mod, L, s, beat, nbeats, path, idx, total, tag):
    if s['t'] == 'wb':
        import board
        wb_frame(mod, L, s, beat, idx, total, board.n_through(s, beat)).save(path); return
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    t = s['t']
    imgs = s.get('img'); img = None
    if imgs:
        img = imgs[min(beat, len(imgs) - 1)] if isinstance(imgs, list) else imgs
    pts = s.get('pts', [])
    off = nbeats - len(pts) if pts else 0
    nshow = len(pts) if (not s.get('reveal', True) or nbeats == 1) else max(0, beat - off + 1)
    cur = (nshow - 1) if (nbeats > 1 and s.get('reveal', True) and pts and nshow > 0) else None
    if s.get('rv') and pts:                       # explicit reveal schedule (fixes.py): bullets shown no later than narrated
        nshow = s['rv'][min(beat, len(s['rv']) - 1)]; cur = nshow - 1 if nshow > 0 else None
    if t == 'title':
        d.rectangle([0, 0, W, H], fill=ACC)
        tx_w = W - 280
        if img:
            path_i, isfig, key = resolve(mod, img, (1000, 170, 1820, 880), tag)
            r = place(im, path_i, (1000, 170, 1820, 880), card=isfig, shadow=True)
            if key:
                cl = credit_line(key); cw = tlen(cl, 'segoeui.ttf', 20)
                draw_text(d, (r[2] - cw, r[3] + 12), cl, 'segoeui.ttf', 20, (190, 205, 235))
            tx_w = 820
        draw_text(d, (130, 250), L['code'] + ('  ·  ' + L['tag'] if L.get('tag') else ''), 'segoeuib.ttf', 36, (200, 215, 245))
        y = 316
        for ln in rich_lines(s.get('h', L.get('title', '')), 88, tx_w, 'segoeuib.ttf', 'segoeuib.ttf'):
            draw_text(d, (130, y), plain(ln), 'segoeuib.ttf', 88, WHITE); y += 106
        d.rectangle([130, y + 26, 330, y + 34], fill=ORANGE)
        y += 70
        for ln in rich_lines(s.get('sub', ''), 38, tx_w):
            draw_text(d, (130, y), plain(ln), 'segoeui.ttf', 38, (220, 230, 248)); y += 52
        d.rectangle([0, H - 8, int(W * idx / total), H], fill=WHITE)
        im.save(path); return
    if t == 'section':
        d.rectangle([0, 0, W, H], fill=(31, 64, 122))
        draw_text(d, (130, 380), s.get('kicker', 'Part'), 'segoeuib.ttf', 38, (200, 215, 245))
        y = 440
        for ln in rich_lines(s['h'], 80, W - 260, 'segoeuib.ttf', 'segoeuib.ttf'):
            draw_text(d, (130, y), plain(ln), 'segoeuib.ttf', 80, WHITE); y += 98
        d.rectangle([130, y + 24, 330, y + 32], fill=ORANGE)
        if s.get('sub'):
            draw_text(d, (130, y + 64), s['sub'], 'segoeui.ttf', 38, (220, 230, 248))
        d.rectangle([0, H - 8, int(W * idx / total), H], fill=WHITE)
        im.save(path); return
    chrome(d, L, idx, total)
    y = heading(d, s['h'])
    bottom = 1030
    if t == 'clip':   # real footage: text on the left, the video plays in the panel on the right (still frame here)
        box = clip_box(y); s['_y'] = y
        d.rounded_rectangle(box, radius=16, fill=(16, 19, 26))
        st = clip_still(s); bw_, bh_ = box[2] - box[0] - 16, box[3] - box[1] - 16
        sc = min(bw_ / st.width, bh_ / st.height); st = st.resize((int(st.width * sc), int(st.height * sc)))
        im.paste(st, (box[0] + 8 + (bw_ - st.width) // 2, box[1] + 8 + (bh_ - st.height) // 2))
        yy = y + 40
        for p in s.get('pts', []):
            for k_, ln in enumerate(rich_lines(p, 34, box[0] - 190)):
                if k_ == 0: d.ellipse([110, yy + 16, 124, yy + 30], fill=ORANGE)
                draw_rich(d, 140, yy, [ln], 34, INK, 46); yy += 46
            yy += 18
        if s.get('cap'):
            cl = rich_lines(s['cap'], 24, box[0] - 160); yy = bottom - 34 * len(cl)
            for ln in cl: draw_rich(d, 110, yy, [ln], 24, MUT, 34); yy += 34
        im.save(path); return
    if t == 'q':   # big statement
        lines = rich_lines(s['big'], 64, W - 360, 'seguisb.ttf', 'segoeuib.ttf')
        hh = len(lines) * 84
        yy = max(y + 30, (y + bottom) // 2 - hh // 2 - 40)
        d.rectangle([150, yy - 10, 162, yy + hh], fill=ORANGE)
        draw_rich(d, 200, yy, lines, 64, INK, 84, 'seguisb.ttf', 'segoeuib.ttf')
        if s.get('cap'):
            draw_rich(d, 200, yy + hh + 40, rich_lines(s['cap'], 36, W - 360), 36, MUT, 48)
        im.save(path); return
    cap = s.get('cap')
    capH = 50 if cap else 0
    split = s.get('split', 0.42)
    if t == 'ex':
        nshow = None
        if s.get('cl'):  # code lines visible per beat
            cl = s['cl']; nshow = cl[min(beat, len(cl) - 1)]
        if img:
            xm = int(W * split)
            code_box(d, s['code'], 100, y, xm - 20, bottom - capH, nshow)
            box = (xm + 20, y, W - 100, bottom - capH - 30)
        else:
            yb = code_box(d, s['code'], 100, y, W - 100, bottom - capH - (len(pts) * 52 + 24 if pts else 0), nshow)
            box = None
        if pts and not img:
            bullets(d, pts, 120, yb + 30, W - 240, nshow if nshow is not None else len(pts), 36)
    elif pts and img:
        xm = int(W * split)
        bullets(d, pts, 100, y + 6, xm - 120, nshow, s.get('fs', 40), cur)
        box = (xm + 10, y - 10, W - 90, bottom - capH - 30)
    elif pts:
        bullets(d, pts, 110, y + 10, W - 240, nshow, s.get('fs', 44), cur)
        box = None
    else:
        box = (100, y - 10, W - 100, bottom - capH - 30) if img else None
    if img and box:
        path_i, isfig, key = resolve(mod, img, box, tag)
        r = place(im, path_i, box, card=isfig, shadow=not isfig)
        if REC is not None: REC.append({'kind': 'fig', 'r': (r[0] + 22, r[1] + 22, r[2] - 22, r[3] - 22) if isfig else r})
        cl = credit_line(key) if key else ''
        if cl:
            cw = tlen(cl, 'segoeui.ttf', 20); draw_text(d, (r[2] - cw, r[3] + 8), cl, 'segoeui.ttf', 20, MUT)
        if cap:
            capx = r[0] if box[0] > 200 else 100
            lines = rich_lines(cap, 32, box[2] - capx)
            draw_rich(d, capx, r[3] + (36 if cl else 14), lines[:2], 32, MUT, 40)
    elif cap:
        draw_text(d, (100, bottom - 40), cap, 'segoeui.ttf', 32, MUT)
    im.save(path)

# ---------------- audio / video ----------------
def wav_dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()

def h(*parts):
    m = hashlib.sha1()
    for p in parts: m.update(p if isinstance(p, bytes) else str(p).encode('utf-8'))
    return m.hexdigest()[:16]

def say_fix(text):
    """pronunciation tweaks applied only to the spoken text"""
    reps = [('—', ', '), ('–', ' to '), ('≈', ' about '), ('%', ' percent'), ('&', ' and ')]
    for a, b in reps: text = text.replace(a, b)
    return text

def audio_for(text, silence=None):
    if silence:
        p = D('cache', f'sil_{silence:.2f}.wav')
        if not os.path.exists(p):
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', f'{silence:.2f}',
                            '-c:a', 'pcm_s16le', p], check=True)
        return p, []
    import tts
    sig = tts.lex_sig(say_fix(text))                # pronunciation-dictionary words re-synthesize only the sentences that use them
    key = h(ARGS.voice, ARGS.speed, 'v5', text) if not sig else h(ARGS.voice, ARGS.speed, 'v5', text, 'lex', sig)
    p = D('cache', key + '.wav'); mp = D('cache', key + '.json')
    if not os.path.exists(p) or not os.path.exists(mp):
        import tts
        marks = tts.make(say_fix(text), p, ARGS.voice, ARGS.speed)
        json.dump(marks, open(mp, 'w', encoding='utf-8'))
    return p, json.load(open(mp, encoding='utf-8'))

def seg_for(png, wav, dur):
    key = h(open(png, 'rb').read(), open(wav, 'rb').read(), f'{dur:.3f}', 'seg2')
    out = D('segs', key + '.mp4')
    if not os.path.exists(out):
        pad = dur - wav_dur(wav)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', '24', '-i', png, '-i', wav,
                        '-af', f'apad=pad_dur={max(pad, 0):.3f}', '-t', f'{dur:.3f}',
                        '-c:v', 'libx264', '-preset', 'medium', '-tune', 'stillimage', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '24',
                        '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-ac', '1', out], check=True)
    return out

FPS = 24
def seg_wb(mod, L, s, beat, idx, total, n, wav, marks, dur):
    """whiteboard beat: each board item is 'written' (wiped on left-to-right) when its sentence starts"""
    import board, numpy as np
    evs = [(i, e) for i, e in enumerate(board.events(s)) if e['beat'] == beat]
    n0 = board.n_through(s, beat - 1) if beat > 0 else 0
    states, paths = [], []
    for k in range(len(evs) + 1):
        states.append(wb_frame(mod, L, s, beat, idx, total, n0 + k)); paths.append(dict(board.LAST_PATHS))
    off = board.LAST_OFF
    sig = h(*[st.tobytes() for st in states], open(wav, 'rb').read(), json.dumps(marks), f'{dur:.3f}',
            json.dumps([e['j'] for _, e in evs]), 'wb2')
    out = D('segs', sig + '.mp4')
    if os.path.exists(out): return out
    # schedule: item j appears at the start of sentence e['j'] (never overlapping the previous stroke)
    plan, tprev = [], 0.0
    for k, (i, e) in enumerate(evs):
        j = min(e['j'], len(marks) - 1); t0 = (marks[j][1] if marks else 0.3) + 0.12   # past the end -> last sentence
        if 'p' in e['it'] and paths[k + 1].get(i):          # pen: drawn along the stroke at marker speed
            strokes = paths[k + 1][i]
            ln_ = sum(float(np.hypot(*np.diff(st, axis=0).T).sum()) for st, *_ in strokes)
            wd = min(1.8, max(0.45, 0.25 + ln_ / 1100))
            t0 = max(t0 + 0.15, tprev + 0.08); t0 = min(t0, max(0.0, dur - wd - 0.2))
            base = states[k]
            if e['it'].get('solo'):                         # wipe the earlier marks first, then draw the new one
                board.EXCLUDE = {i}
                try: base = wb_frame(mod, L, s, beat, idx, total, n0 + k + 1)
                finally: board.EXCLUDE = set()
            plan.append((t0, wd, ('pen', strokes, ln_, base))); tprev = t0 + wd; continue
        a, b = np.asarray(states[k], dtype=np.int16), np.asarray(states[k + 1], dtype=np.int16)
        ys, xs = np.where(np.abs(a - b).sum(2) > 24)
        if len(xs) == 0: plan.append((max(t0, tprev), 0, None)); continue
        bb = (max(xs.min() - 4, 0), max(ys.min() - 4, 0), min(xs.max() + 5, W), min(ys.max() + 5, H))
        wdt = bb[2] - bb[0]
        wd = min(2.6, max(0.5, (0.6 + wdt / 700) if 'd' in e['it'] else (0.3 + wdt / 950)))
        t0 = max(t0, tprev + 0.08); t0 = min(t0, max(0.0, dur - wd - 0.2))
        plan.append((t0, wd, bb)); tprev = t0 + wd
    return anim_encode(states, plan, off, wav, dur, sig, out)

def anim_encode(states, plan, off, wav, dur, sig, out):
    """states[k] -> states[k+1] transitions at plan times: ('pen', strokes, length, base) drawn along the stroke, or a bbox wiped
    left to right; then encoded with the narration. off = where stroke coordinates sit inside the frame."""
    import numpy as np
    tmp = D('segs', 'wb_' + sig); os.makedirs(tmp, exist_ok=True)
    seq = []   # (png, seconds)
    def put(img, name):
        p = os.path.join(tmp, name + '.png'); img.save(p, compress_level=1); return p
    cur = put(states[0], 's0'); tcur = 0.0
    for k, (t0, wd, bb) in enumerate(plan):
        if t0 > tcur: seq.append((cur, t0 - tcur)); tcur = t0
        if bb and bb[0] == 'pen':
            _, strokes, total_len, base = bb; nf = max(2, int(round(wd * FPS)))
            for f in range(1, nf):
                left = total_len * f / nf; mask = Image.new('L', (W, H), 0); md = ImageDraw.Draw(mask)
                for st, wpx, *_ in strokes:
                    if left <= 0: break
                    seglen = np.hypot(*np.diff(st, axis=0).T); cum = np.concatenate([[0], np.cumsum(seglen)])
                    m = int(np.searchsorted(cum, left)); pts = st[:max(1, m)]
                    if m < len(st) and m > 0:
                        fr_ = (left - cum[m - 1]) / (seglen[m - 1] or 1); pts = np.vstack([pts, st[m - 1] + (st[m] - st[m - 1]) * fr_])
                    xy = [(float(x) + off[0], float(y) + off[1]) for x, y in pts]; ww = int(wpx + 8)
                    if len(xy) > 1: md.line(xy, fill=255, width=ww, joint='curve')
                    for (px_, py_) in (xy[0], xy[-1]): md.ellipse([px_ - ww / 2, py_ - ww / 2, px_ + ww / 2, py_ + ww / 2], fill=255)
                    left -= cum[-1]
                fr = Image.composite(states[k + 1], base, mask)
                seq.append((put(fr, f'p{k}_{f:03d}'), 1 / FPS)); tcur += 1 / FPS
        elif bb:
            nf = max(2, int(round(wd * FPS)))
            for f in range(1, nf):
                fr = states[k].copy(); xr = bb[0] + int((bb[2] - bb[0]) * f / nf)
                fr.paste(states[k + 1].crop((bb[0], bb[1], xr, bb[3])), (bb[0], bb[1]))
                seq.append((put(fr, f'w{k}_{f:03d}'), 1 / FPS)); tcur += 1 / FPS
        cur = put(states[k + 1], f's{k + 1}')
    seq.append((cur, max(dur - tcur, 1 / FPS)))
    lst = os.path.join(tmp, 'list.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for p, d_ in seq: f.write(f"file '{p}'\nduration {d_:.4f}\n")
        f.write(f"file '{seq[-1][0]}'\n")
    pad = dur - wav_dur(wav)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', wav,
                    '-af', f'apad=pad_dur={max(pad, 0):.3f}', '-t', f'{dur:.3f}', '-vf', f'fps={FPS}',
                    '-c:v', 'libx264', '-preset', 'medium', '-tune', 'stillimage', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                    '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-ac', '1', out], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return out

# ---------------- the pen on ordinary slides ----------------
# slide['pen'] = [{'b': beat, 'at': sentence, 'p': kind | [kinds], 'on': 'text on the slide' | 'fig': [(kind, fractions...)],
#                  'c': colour, 'n': which occurrence, 'dt': extra seconds into the sentence, 'keep': stays for later beats (default True),
#                  'solo': wipe earlier marks first}]
# text kinds: circle box underline highlight strike check cross arrow;  figure marks use fractions of the figure (0..1, y down):
# ('circle', fx, fy, frx, fry) ('box'|'highlight', fx0, fy0, fx1, fy1) ('arrow', fx0, fy0, fx1, fy1) ('underline', fx0, fx1, fy) ('check'|'cross', fx, fy)
def find_on(rec, want, n=0):
    """boxes (one per wrapped line) of the n-th place `want` appears among the recorded text lines"""
    lines = [r for r in rec if r['kind'] != 'fig']
    chars = []
    for li, r in enumerate(lines):
        if chars: chars.append((' ', None))
        chars += [(c, (li, k)) for k, c in enumerate(r['t'])]
    text = ''.join(c for c, _ in chars)
    for fold in (False, True):
        hay, nd = (text.lower(), want.lower()) if fold else (text, want)
        pos, idx = -1, -1
        for _ in range(n + 1):
            idx = hay.find(nd, pos + 1); pos = idx
            if idx < 0: break
        if idx >= 0: break
    if idx < 0:
        raise KeyError(f"pen: {want!r} is not on the slide. Lines: " + ' | '.join(r['t'][:70] for r in lines))
    by = {}
    for c, ref in chars[idx:idx + len(want)]:
        if ref is None: continue
        li, k = ref; r = lines[li]; a, b = r['xs'][k]
        x0, x1 = by.get(li, (a, b)); by[li] = (min(x0, a), max(x1, b))
    return [(x0, lines[li]['y0'], x1, lines[li]['y1'], lines[li]['kind']) for li, (x0, x1) in sorted(by.items())]

def spen_strokes(mark, rec, seed):
    import board, numpy as np
    rng = np.random.default_rng(int(hashlib.md5(seed.encode()).hexdigest()[:8], 16))
    col = board.c_(mark.get('c', 'red')); kinds = mark['p'] if isinstance(mark.get('p'), list) else [mark.get('p', 'underline')]
    out = []
    if 'on' in mark:
        boxes = find_on(rec, mark['on'], mark.get('n', 0))
        X0, Y0 = min(b[0] for b in boxes), min(b[1] for b in boxes); X1, Y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        my = (Y0 + Y1) / 2
        for k in kinds:
            if k in ('underline', 'highlight', 'strike'):
                for x0, y0, x1, y1, _ in boxes:
                    g = {'underline': (x0, y1 + 4, x1, y1 + 4), 'highlight': (x0 - 4, y0 + 1, x1 + 4, y1 - 1),
                         'strike': (x0 - 4, (y0 + y1) / 2, x1 + 4, (y0 + y1) / 2)}[k]
                    out += board._shape(k, g, rng, col)
                continue
            if k == 'circle' and (X1 - X0 > 300 or len(boxes) > 1): k = 'box'      # an ellipse round a long line cuts its ends
            g = {'circle': ((X0 + X1) / 2, my, (X1 - X0) / 2 + 14, (Y1 - Y0) / 2 + 10), 'box': (X0 - 10, Y0 - 6, X1 + 10, Y1 + 6),
                 'check': (X1 + 34, my, 18), 'cross': (X1 + 34, my, 15), 'arrow': (X0 - 120, my, X0 - 16, my)}[k]
            out += board._shape(k, g, rng, col)
        return out
    fr = next((r['r'] for r in rec if r['kind'] == 'fig'), None)
    if fr is None: raise KeyError('pen: this slide has no figure to mark')
    fx = lambda v: fr[0] + v * (fr[2] - fr[0]); fy = lambda v: fr[1] + v * (fr[3] - fr[1])
    for m in mark['fig']:
        k, a = m[0], m[1:]
        if k == 'circle': g = (fx(a[0]), fy(a[1]), a[2] * (fr[2] - fr[0]), a[3] * (fr[3] - fr[1]))
        elif k in ('box', 'highlight'): g = (fx(a[0]), fy(a[1]), fx(a[2]), fy(a[3]))
        elif k == 'arrow': g = (fx(a[0]), fy(a[1]), fx(a[2]), fy(a[3]))
        elif k == 'underline': g = (fx(a[0]), fy(a[2]), fx(a[1]), fy(a[2]))
        elif k in ('check', 'cross'): g = (fx(a[0]), fy(a[1]), a[2] if len(a) > 2 else 18)
        else: raise ValueError('pen: unknown figure mark ' + str(k))
        out += board._shape(k, g, rng, col)
    return out

def draw_strokes(im, strokes):
    """paint marker strokes (frame pixels) onto a copy of im, antialiased"""
    import numpy as np
    im = im.convert('RGBA'); S = 3
    for pts, w, alpha, col in strokes:
        pts = np.asarray(pts, float); pad = w / 2 + 3
        x0, y0 = int(max(0, pts[:, 0].min() - pad)), int(max(0, pts[:, 1].min() - pad))
        x1, y1 = int(min(W, pts[:, 0].max() + pad + 1)), int(min(H, pts[:, 1].max() + pad + 1))
        if x1 <= x0 or y1 <= y0: continue
        lay = Image.new('L', ((x1 - x0) * S, (y1 - y0) * S), 0); dd = ImageDraw.Draw(lay)
        xy = [((x - x0) * S, (y - y0) * S) for x, y in pts]; ww = max(1, int(w * S))
        if len(xy) > 1: dd.line(xy, fill=255, width=ww, joint='curve')
        for px, py in (xy[0], xy[-1]): dd.ellipse([px - ww / 2, py - ww / 2, px + ww / 2, py + ww / 2], fill=255)
        lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS).point(lambda v: int(v * alpha))
        rgb = tuple(int(col.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        c = Image.new('RGBA', lay.size, rgb + (0,)); c.putalpha(lay); im.alpha_composite(c, (x0, y0))
    return im.convert('RGB')

def spen_plan(s, beat):
    """(marks visible when the beat starts, marks drawn during the beat in order)"""
    P = sorted([m for m in s.get('pen', [])], key=lambda m: (m['b'], m.get('at', 0), m.get('dt', 0)))
    vis = []
    for m in P:
        if m['b'] >= beat: break
        vis = [m] if m.get('solo') else vis + [m]
    imgs = s.get('img'); img_at = lambda b: imgs[min(b, len(imgs) - 1)] if isinstance(imgs, list) else imgs
    vis = [m for m in vis if m.get('keep', True) and not ('fig' in m and img_at(m['b']) != img_at(beat))]   # figure marks leave with their figure
    return vis, [m for m in P if m['b'] == beat]

def seg_spen(s, png, rec, beat, wav, marks, dur):
    """an ordinary slide with the teacher's pen: each mark is drawn along its stroke when its sentence starts"""
    import numpy as np
    vis, now = spen_plan(s, beat)
    seed = lambda m: f"{s.get('h', '')}|{json.dumps(m, sort_keys=True, default=str)}"
    sig = h(open(png, 'rb').read(), os.path.basename(wav), json.dumps([vis, now], sort_keys=True, default=str), f'{dur:.3f}', 'sp1')
    out = D('segs', 'sp_' + sig + '.mp4')
    clean = Image.open(png).convert('RGB')
    strokes = {id(m): spen_strokes(m, rec, seed(m)) for m in vis + now}
    paint = lambda ms: draw_strokes(clean, [st for m in ms for st in strokes[id(m)]]) if ms else clean.copy()
    cur = list(vis); states = [paint(cur)]; plan = []; tprev = 0.0
    for m in now:
        base_ms = [] if m.get('solo') else cur
        cur = [m] if m.get('solo') else cur + [m]
        st = strokes[id(m)]; ln_ = sum(float(np.hypot(*np.diff(np.asarray(p, float), axis=0).T).sum()) for p, *_ in st)
        wd = min(1.8, max(0.45, 0.25 + ln_ / 1100))
        j = min(m.get('at', 0), len(marks) - 1); t0 = (marks[j][1] if marks else 0.3) + 0.27 + m.get('dt', 0)
        t0 = max(t0, tprev + 0.08); t0 = min(t0, max(0.0, dur - wd - 0.2))
        plan.append((t0, wd, ('pen', st, ln_, paint(base_ms)))); tprev = t0 + wd
        states.append(paint(cur))
    states[-1].save(png)                                  # the slide PDF shows the finished marks
    if os.path.exists(out): return out
    return anim_encode(states, plan, (0, 0), wav, dur, sig, out)

WB_VER = 'w3'   # bump to force every whiteboard beat to re-render
_WB_CODE = None
def wb_key(n, si, bi, idx, total, wav, marks, dur):
    """Cache key for a whiteboard beat built from its *inputs* (code + content + audio), so a cache hit costs
    no drawing at all. The old key hashed the drawn frames, which meant redrawing every board state just to look it up."""
    global _WB_CODE
    if _WB_CODE is None:
        import inspect
        src = open(os.path.abspath(__file__), 'rb').read()
        cut = src.find(b'# ---------------- audio / video ----------------')
        _WB_CODE = h(WB_VER, src[:cut], inspect.getsource(seg_wb),
                     *[open(D(f), 'rb').read() for f in ('board.py', 'figlib.py')])
    les = open(D('lessons', n + '.py'), 'rb').read()
    if b'L00_welcome' in les: les += open(D('lessons', 'L00_welcome.py'), 'rb').read()
    return h(_WB_CODE, les, si, bi, idx, total, os.path.basename(wav), json.dumps(marks), f'{dur:.3f}')

def ts(t):
    hh = int(t // 3600); mm = int(t % 3600 // 60); ss = t % 60
    return f'{hh:02d}:{mm:02d}:{int(ss):02d},{int(round((ss % 1) * 1000)) % 1000:03d}'

def cues(marks, t0):
    out = []
    for sent, a, b in marks:
        parts = []; x = sent
        while len(x) > 84:
            cut = x.rfind(', ', 0, 80)
            if cut < 25: cut = x.rfind(' ', 0, 80)
            parts.append(x[:cut + 1].strip()); x = x[cut + 1:].strip()
        parts.append(x)
        tot = sum(len(p) for p in parts); tt = a
        for p in parts:
            dd = (b - a) * len(p) / tot
            out.append((t0 + tt, t0 + tt + dd, p)); tt += dd
    return out

# ---------------- main ----------------
def load_lessons():
    mods = []
    for f in sorted(glob.glob(D('lessons', 'L*.py'))):
        name = os.path.splitext(os.path.basename(f))[0]
        spec = importlib.util.spec_from_file_location(name, f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        import fixes; fixes.apply(name, m.LESSON)
        mods.append((name, m))
    return mods

mods = load_lessons()
if ARGS.only:
    want = ARGS.only.split(',')
    mods = [(n, m) for n, m in mods if any(n.startswith(w) for w in want)]
flat = []
for n, m in mods:
    L = m.LESSON
    for si, s in enumerate(L['slides']):
        if s['t'] == 'wb': s['say'] = [st['say'] for st in s['steps']]
        says = s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')]
        for bi in range(len(says)): flat.append((n, m, si, bi, len(says), says[bi]))
total = len(flat)
print('beats:', total, ' lessons:', len(mods), flush=True)

_RD_P = D('cache', 'segdur.json')
_RD = json.load(open(_RD_P, encoding='utf-8')) if os.path.exists(_RD_P) else {}
def real_dur(seg):
    k = os.path.basename(seg)            # segment files are content-addressed, so the name identifies the encoding
    if k not in _RD:
        r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', seg], capture_output=True, text=True, check=True)
        _RD[k] = float(r.stdout.strip())
        if len(_RD) % 50 == 0: json.dump(_RD, open(_RD_P, 'w', encoding='utf-8'))
    return _RD[k]

segs, srt, chapters, per_lesson, beats = [], [], [], {}, []
t = 0.0; last_lesson = None
for k, (n, m, si, bi, nb, say) in enumerate(flat):
    L = m.LESSON; s = L['slides'][si]
    png = D('frames', f'{n}_{si:02d}_{bi}.png')
    if s['t'] != 'wb' or ARGS.frames:
        REC = []; render(m, L, s, bi, nb, png, k + 1, total, n); rec = REC; REC = None
    if ARGS.frames:
        if s['t'] != 'wb':
            fr_ = next((r['r'] for r in rec if r['kind'] == 'fig'), None)
            if fr_: json.dump(fr_, open(png[:-4] + '.fig.json', 'w'))
        vis, now = spen_plan(s, bi) if s['t'] != 'wb' else ([], [])
        if vis or now:            # preview: the beat's finished pen marks
            sd = lambda mk: f"{s.get('h', '')}|{json.dumps(mk, sort_keys=True, default=str)}"
            cur = []
            for mk in vis + now: cur = [mk] if mk.get('solo') and mk in now else cur + [mk]
            draw_strokes(Image.open(png), [st for mk in cur for st in spen_strokes(mk, rec, sd(mk))]).save(png)
        continue
    if s.get('silent'):
        wav, marks = audio_for(None, silence=float(s['silent']))
    else:
        wav, marks = audio_for(say)
    dur = wav_dur(wav) + (0.55 if bi == nb - 1 else 0.05)
    if n != last_lesson:
        chapters.append((t, L.get('chapter', L['code'] + (' – ' + L['title'] if L.get('title') else '')))); last_lesson = n
    srt += cues(marks, t)
    if s['t'] == 'wb':
        wk = wb_key(n, si, bi, k + 1, total, wav, marks, dur)
        seg = D('segs', WB_VER + '_' + wk + '.mp4'); pc = D('frames', WB_VER + '_' + wk + '.png')
        if os.path.exists(seg) and os.path.exists(pc):
            shutil.copyfile(pc, png)                                   # cache hit: nothing drawn
        else:
            render(m, L, s, bi, nb, png, k + 1, total, n)
            old = seg_wb(m, L, s, bi, k + 1, total, n, wav, marks, dur)   # reuses a segment cached under the old pixel key
            shutil.copyfile(old, seg); shutil.copyfile(png, pc)
    elif s['t'] == 'clip':
        seg = seg_clip(s, png, wav, dur)
    elif any(spen_plan(s, bi)):
        seg = seg_spen(s, png, rec, bi, wav, marks, dur)
    else:
        seg = seg_for(png, wav, dur)
    dur = real_dur(seg)          # encoded length (a few ms longer than planned); summing planned lengths drifted subtitles ~5 s by hour 4
    segs.append(seg); per_lesson.setdefault(n, []).append((seg, marks, dur))
    beats.append([round(t, 3), round(t + dur, 3), n, si, bi])
    t += dur
    print(f'[{k+1}/{total}] {n} s{si} b{bi}  {dur:5.1f}s  total {t/60:5.1f} min', flush=True)

if ARGS.frames:
    print('frames rendered:', total); sys.exit()

def mux(seglist, subs, chaps, total_t, out, title):
    lst = D('out', 'list_' + h(out) + '.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for sg in seglist: f.write(f"file '{sg}'\n")
    joined = D('out', 'joined_' + h(out) + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', joined], check=True)
    srtp = os.path.splitext(out)[0] + '.srt'
    with open(srtp, 'w', encoding='utf-8') as f:
        for i, (a, b, x) in enumerate(subs, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{x}\n\n')
    meta = D('out', 'meta_' + h(out) + '.txt')
    with open(meta, 'w', encoding='utf-8') as f:
        f.write(f';FFMETADATA1\ntitle={title}\n\n')
        for i, (st, name) in enumerate(chaps):
            en = chaps[i + 1][0] if i + 1 < len(chaps) else total_t
            f.write(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(st*1000)}\nEND={int(en*1000)}\ntitle={name}\n\n')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', joined, '-i', srtp, '-i', meta,
                    '-map', '0', '-map', '1', '-map_metadata', '2', '-map_chapters', '2', '-c', 'copy', '-c:s', 'mov_text',
                    '-metadata:s:s:0', 'language=eng', '-movflags', '+faststart', out], check=True)
    os.remove(joined)

out = ARGS.out or D('out', 'lectures.mp4')
CODE = {n: m.LESSON['code'] for n, m in mods}
def credit_entries():
    ents = []
    for key, tags in USED.items():
        c = CRED.get(key)
        if not c: continue
        order = min(tags); codes = ', '.join(CODE[t] for t in sorted(tags))
        a = re.sub(r'\s+', ' ', c.get('artist') or 'Unknown').strip()
        ents.append((order, c['title'].replace('File:', ''), a, c['license'], c.get('page', ''), codes))
    return sorted(ents)

def credit_pages(ents, per=30):
    pages = []
    for p0 in range(0, len(ents), per):
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, W, 8), fill=ACC)
        draw_text(d, (90, 50), 'Image credits', 'segoeuib.ttf', 46, INK)
        draw_text(d, (90, 112), f'Photographs from Wikimedia Commons, used under their free licenses · page {p0 // per + 1} of {(len(ents) + per - 1) // per}', 'segoeui.ttf', 24, MUT)
        for i, (_, title, a, lic, _, codes) in enumerate(ents[p0:p0 + per]):
            col, row = i // 15, i % 15; x = 90 + col * 880; y = 180 + row * 56
            tt = title if len(title) <= 52 else title[:50] + '…'; aa = a if len(a) <= 46 else a[:44] + '…'
            draw_text(d, (x, y), tt, 'segoeuib.ttf', 20, INK)
            draw_text(d, (x, y + 25), f'{aa} · {lic} · {codes}', 'segoeui.ttf', 18, MUT)
        pth = D('frames', f'credits_{p0 // per}.png'); im.save(pth); pages.append(pth)
    return pages

if ARGS.credits:
    ents = credit_entries()
    with open(os.path.splitext(out)[0] + '_Image_Credits.txt', 'w', encoding='utf-8') as f:
        f.write('Image credits — Computer Engineering, Course by Course\n')
        f.write('All photographs are from Wikimedia Commons and used under the licenses shown.\n')
        f.write('Diagrams, charts and schematics were generated for this series.\n\n')
        for _, title, a, lic, page, codes in ents:
            f.write(f'{title}\n  Author: {a}\n  License: {lic}\n  Source: {page}\n  Used in: {codes}\n\n')
    chapters.append((t, 'Image credits'))
    for pth in credit_pages(ents):
        wav, _ = audio_for(None, silence=10.0); seg = seg_for(pth, wav, 10.0); segs.append(seg); t += real_dur(seg)
    print('credits:', len(ents), 'images', flush=True)

json.dump(_RD, open(_RD_P, 'w', encoding='utf-8'))
mux(segs, srt, chapters, t, out, 'Computer Engineering, Course by Course')
# youtube chapter list
with open(os.path.splitext(out)[0] + '_chapters.txt', 'w', encoding='utf-8') as f:
    for st, name in chapters:
        f.write(f'{int(st//3600)}:{int(st%3600//60):02d}:{int(st%60):02d} {name}\n' if st >= 3600 else f'{int(st//60)}:{int(st%60):02d} {name}\n')
print('DONE', out, f'{t/60:.1f} min', flush=True)

if ARGS.lessons_out:
    os.makedirs(ARGS.lessons_out, exist_ok=True)
    for n, m in mods:
        items = per_lesson[n]; tt = 0.0; subs = []
        for sg, marks, dur in items: subs += cues(marks, tt); tt += dur
        L = m.LESSON
        name = re.sub(r'[^A-Za-z0-9]+', '_', f"{n[1:3]} {L['code']} {L.get('title','')}").strip('_')
        mux([x[0] for x in items], subs, [(0.0, L['code'])], tt, os.path.join(ARGS.lessons_out, name + '.mp4'), f"{L['code']} – {L.get('title','')}")
        print('lesson file', name, f'{tt/60:.1f} min', flush=True)

def lesson_chapters(n, L):
    """one chapter per slide, from the per-beat durations"""
    chs = []; tt = 0.0; k = 0
    for si, s in enumerate(L['slides']):
        nb = len(s['say']) if isinstance(s.get('say'), list) else 1
        chs.append((tt, s.get('h', L['title']).replace('**', '')))
        for _ in range(nb): tt += per_lesson[n][k][2]; k += 1
    return chs, tt

def slide_pdf(n, L, path):
    pages = []
    for si, s in enumerate(L['slides']):
        nb = len(s['say']) if isinstance(s.get('say'), list) else 1
        pages.append(Image.open(D('frames', f'{n}_{si:02d}_{nb - 1}.png')).convert('RGB'))
    pages[0].save(path, save_all=True, append_images=pages[1:], resolution=150.0, quality=88)

def write_timeline(path, files):
    """what is on screen / being said at every moment: used by the Ask-the-Narrator player"""
    les = {}
    for n, m in mods:
        L = m.LESSON
        les[n] = {'code': L['code'], 'title': L.get('title', ''), 'tag': L.get('tag', ''), 'file': files.get(n),
                  'start': next(b[0] for b in beats if b[2] == n),
                  'slides': [{'h': s.get('h', '').replace('**', ''),
                              'pts': [p.replace('**', '') for p in s.get('pts', [])] if s['t'] != 'wb' else
                                     [('(written on the whiteboard) ' + __import__('board').plain(it if isinstance(it, str) else it['m'])) if isinstance(it, str) or 'm' in it
                                      else ('(code on the board) ' + it['k']) if 'k' in it else ('(program output) ' + it['o'])
                                      for st in s['steps'] for it in st.get('w', []) if isinstance(it, str) or any(k in it for k in ('m', 'k', 'o'))],
                              'big': s.get('big', '').replace('**', ''), 'code': s.get('code', '') if isinstance(s.get('code'), str) else '',
                              'say': s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')]} for s in L['slides']]}
    json.dump({'video': os.path.basename(out), 'duration': round(t, 3), 'lessons': les, 'beats': beats,
               'chapters': [[round(a, 3), b] for a, b in chapters]}, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    print('timeline ->', path, flush=True)

lesson_files = {}
if ARGS.course_root:
    for n, m in mods:
        L = m.LESSON; folder = L.get('folder')
        dst = os.path.join(ARGS.course_root, folder) if folder else ARGS.course_root
        os.makedirs(dst, exist_ok=True)
        title = re.sub(r'[\\/:*?"<>|]', '-', f"{L['code']} {L.get('title', '')}" if folder else f"{n[1:3]} {L['code']} - {L.get('title', '')}").strip()
        items = per_lesson[n]; subs = []; tt = 0.0
        for sg, marks, dur in items: subs += cues(marks, tt); tt += dur
        chs, _ = lesson_chapters(n, L)
        mux([x[0] for x in items], subs, chs, tt, os.path.join(dst, f'Lecture - {title}.mp4'), f"{L['code']} – {L.get('title','')}")
        slide_pdf(n, L, os.path.join(dst, f'Slides - {title}.pdf'))
        lesson_files[n] = os.path.relpath(os.path.join(dst, f'Lecture - {title}.mp4'), ARGS.course_root).replace('\\', '/')
        print('course files ->', dst, f'{tt/60:.1f} min', flush=True)
write_timeline(os.path.splitext(out)[0] + '_timeline.json', lesson_files)
