"""Whiteboard slides ('t': 'wb'): the narrator writes the worked example line by line and draws diagrams
part by part, each item appearing (wiped on left-to-right like handwriting) when its sentence is spoken.

Slide spec:
  {'t': 'wb', 'h': 'Worked example: ...', 'draw': 'name' (optional: draw_name(ax, n, w, h) in the lesson module
   draws the first n parts of a diagram in pixel coords, y up), 'split': 0.56 (text column fraction when drawing),
   'steps': [ {'say': "sentence. sentence.", 'w': [item, ...], 'clear': False}, ... ]}   # one step = one beat
  item: "text with $math$"                       -> next line of working
        {'m': "...", 'c': 'red', 'box': True, 'x': 40, 'fs': 40, 'gap': 10, 'at': 1, 'col': 2}
        {'d': 3}                                 -> reveal drawing parts up to 3
  'at' = index of the sentence (within the step's narration) at which the item is written (default: its position).
        {'p': mark or [marks], 'at': 1, 'c': 'red', 'keep': False, 'on': 'text'}   -> PEN: the teacher's marker,
           drawn stroke by stroke over the board. Pen marks last until the end of their step (beat), like a teacher
           wiping the marks before the next step, unless 'keep': True (then until the page is cleared).
           'p' may also be a function  lambda A, w, h: [marks]  (A = points named by the draw function with anchor()).
           Drawing marks (coordinates of the draw_* function; x/y may name an anchor set with anchor()):
             ('circle', x, y, rx, ry)  ('box', x0, y0, x1, y1)  ('underline', x0, x1, y)  ('strike', x0, y0, x1, y1)
             ('arrow', x0, y0, x1, y1)  ('cross', x, y)  ('check', x, y)  ('highlight', x0, y0, x1, y1)
           Text marks: 'on': a substring of a written line / code line, and marks without coordinates:
             ('circle',) ('box',) ('underline',) ('highlight',) ('strike',) ('check',) ('cross',) ('arrow',)
             'cols': (c0, c1) limits a code-line mark to characters c0..c1 (e.g. circle just `prev->next`).
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

INK = '#1d2f5e'
COL = dict(ink=INK, red='#c8443b', green='#23895a', blue='#2B5CAB', orange='#d9702c', gray='#7a8496', purple='#7A4FB5')
RC = {'font.family': ['Ink Free', 'Segoe UI Symbol', 'Segoe UI'], 'mathtext.fontset': 'custom', 'mathtext.rm': 'Ink Free', 'mathtext.it': 'Ink Free',
      'mathtext.bf': 'Ink Free', 'mathtext.sf': 'Ink Free', 'mathtext.cal': 'Ink Free', 'mathtext.fallback': 'stixsans',
      'text.color': INK, 'axes.edgecolor': INK, 'lines.color': INK}
DPI = 100
PT = 72 / DPI            # px -> pt
FS = 40                  # default line size (px)

def norm(item):
    it = {'m': item} if isinstance(item, str) else dict(item)
    if 'm' in it: it['m'] = it['m'].replace(r'\frac', r'\dfrac').replace(r'\ddfrac', r'\dfrac').replace(r'\tfrac', r'\frac')
    return it

def fs_of(s, it):
    return it.get('fs', s.get('fs', FS if s.get('draw') else FS + 6))

def events(s):
    """flat list of reveal events: dict(item, beat, j, page)"""
    ev, page = [], 0
    for b, st in enumerate(s['steps']):
        if st.get('clear') and b > 0: page += 1
        for j, it in enumerate(st.get('w', [])):
            it = norm(it); ev.append({'it': it, 'beat': b, 'j': it.get('at', j), 'page': page})
    return ev

def page_of_beat(s, beat):
    return sum(1 for b, st in enumerate(s['steps'][:beat + 1]) if st.get('clear') and b > 0)

def n_through(s, beat):
    return sum(1 for e in events(s) if e['beat'] <= beat)

import re as _re
TEXTKEYS = ('m', 'k', 'o')
KW = {
 'cpp': 'int double float char bool void return if else for while do class struct public private protected const auto new delete include using namespace std true false nullptr virtual override template typename vector string unsigned long size_t this break continue switch case',
 'python': 'def return if elif else for while in import from class True False None and or not range with as lambda',
 'vhdl': 'library use entity is port in out inout std_logic std_logic_vector end architecture of begin signal process if then else elsif case when others rising_edge and or not xor downto to variable constant type all',
 'verilog': 'module endmodule input output reg wire always posedge negedge begin end if else assign case endcase default parameter logic initial',
 'sql': 'select from where join on group by order insert into values create table primary key foreign references and or as count avg sum having int varchar not null update set delete inner left distinct',
 'c': 'int char void return if else for while do struct const volatile unsigned static include define uint8_t uint16_t uint32_t break switch case',
}
KW['c'] += ' ' + 'while'
SYN = dict(kw='#2B5CAB', str='#23895a', com='#66707f', num='#c0562a', ink='#1d2f5e', op='#7A4FB5')
CODE_BG, OUT_BG, OUT_FG = '#eef2f8', '#1f2633', '#e6edf5'

def _toks(line, lang):
    """split a code line into (text, colour) runs"""
    com = {'python': '#', 'vhdl': '--', 'sql': '--', 'asm': ';'}.get(lang, '//')
    ci = line.find(com) if com in line else -1
    body, tail = (line[:ci], line[ci:]) if ci >= 0 else (line, '')
    kws = set(KW.get(lang, '').split())
    out = []
    for m in _re.finditer(r'"[^"]*"|\'[^\']*\'|0x[0-9A-Fa-f]+|\d+(?:\.\d+)?|[A-Za-z_#][\w]*|\s+|.', body):
        t = m.group(0)
        if t[0] in '"\'': c = SYN['str']
        elif t[0].isdigit(): c = SYN['num']
        elif (t.lower() if lang == 'sql' else t) in kws or (t.startswith('#') and lang in ('cpp', 'c')): c = SYN['kw']
        elif lang == 'asm' and not out and t.strip(): c = SYN['kw']          # mnemonic = first word
        else: c = SYN['ink']
        out.append((t, c))
    if tail: out.append((tail, SYN['com']))
    return out

_CW = {}
def _charw(ax, r, px):
    if px not in _CW:
        t = ax.text(0, 0, 'M' * 40, fontsize=px * PT, family='Consolas'); _CW[px] = t.get_window_extent(r).width / 40; t.remove()
    return _CW[px]

def _put(ax, s, it, x, y, r, draw=True, bgw=None):
    """draw (or just measure) one text item at (x, y top); returns (width, height)"""
    px = fs_of(s, it)
    if 'm' in it:
        c = COL.get(it.get('c', 'ink'), it.get('c', INK)); kw = {}
        if it.get('box'): kw['bbox'] = dict(boxstyle='round,pad=0.35', fc='none', ec=c, lw=2.6)
        t = ax.text(x, y, it['m'], fontsize=px * PT, va='top', ha='left', color=c, **kw)
        e = t.get_window_extent(r) if r else None
        if not draw: t.remove()
        return (e.width, e.height) if e else (0, 0)
    raw = it.get('k', it.get('o')); code = raw
    px = it.get('fs', s.get('cfs', 30 if s.get('draw') else 36)); cw = _charw(ax, r, px); hgt = px * 1.38
    wdt = cw * len(code)
    if draw:
        from matplotlib.patches import Rectangle
        is_out = 'o' in it
        ax.add_patch(Rectangle((x - 14, y - 4), (bgw or wdt) + 28, hgt + s.get('clh', 2) + 1, fc=OUT_BG if is_out else (it.get('hl') or CODE_BG), ec='none', zorder=0))
        esc = lambda t_: t_.replace('$', r'\$')     # never let "$" switch on mathtext inside code
        if is_out:
            ax.text(x, y + px * 0.12, esc(code), fontsize=px * PT, family='Consolas', va='top', ha='left', color=OUT_FG)
        elif it.get('plain'):               # monospace scratch work (aligned columns), no syntax colours
            ax.text(x, y + px * 0.12, esc(code), fontsize=px * PT, family='Consolas', va='top', ha='left', color=COL.get(it.get('c', 'ink'), INK))
        else:
            col = 0
            for tok, c in _toks(code, it.get('lang', s.get('lang', 'cpp'))):
                if tok.strip(): ax.text(x + col * cw, y + px * 0.12, esc(tok), fontsize=px * PT, family='Consolas', va='top', ha='left', color=c)
                col += len(tok)
    return wdt, hgt

def _layout(s, mod, page, bw, bh):
    """positions of every text item on a page (measured once with all items present)"""
    key = (id(s), page, bw, bh)
    if key in _LAY: return _LAY[key]
    ev = [(i, e) for i, e in enumerate(events(s)) if e['page'] == page and any(k in e['it'] for k in TEXTKEYS)]
    tw = bw * (s.get('split', 0.56) if s.get('draw') else 1.0)
    with plt.rc_context(RC):
        fig = plt.figure(figsize=(bw / DPI, bh / DPI), dpi=DPI); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, bw); ax.set_ylim(bh, 0); ax.axis('off')
        r = fig.canvas.get_renderer(); pos = {}; wid = {}; size = {}
        cx, right, y = 44, 44, 30          # current column x, right edge of the column, current y
        for i, e in ev:
            it = e['it']; is_code = 'k' in it or 'o' in it
            y += it.get('gap', 0)
            wd, ht = _put(ax, s, it, cx + it.get('x', 0), y, r, draw=False)
            if (y + ht > bh - 12 and y > 60) or it.get('newcol'):   # board full: continue in a new column
                cx, y = right + 70, 30 + it.get('gap', 0)
            pos[i] = (cx + it.get('x', 0), y); wid[i] = (cx, wd, is_code); size[i] = (wd, ht)
            y += ht + it.get('lh', s.get('clh', 2) if is_code else s.get('lh', 22)); right = max(right, cx + it.get('x', 0) + wd)
            if cx + it.get('x', 0) + wd > tw + 8 or y > bh + 5:
                print(f"  [board] warning: '{str(it.get('m', it.get('k', it.get('o'))))[:40]}' overflows ({cx + wd:.0f}/{tw:.0f}px wide, y={y:.0f}/{bh})")
        plt.close(fig)
    # code/output blocks share one panel width per column
    bg = {}
    for i, (c0, wd, is_code) in wid.items():
        if is_code: bg[c0] = max(bg.get(c0, 0), wd + pos[i][0] - c0)
    pos = {i: (p[0], p[1], bg.get(wid[i][0]) if wid[i][2] else None) for i, p in pos.items()}
    _LAY[key] = pos; _SIZE[key] = size
    return pos
_LAY = {}; _SIZE = {}

def render(s, mod, beat, upto, bw, bh):
    """board image (PIL RGB) for the page shown at `beat`, with the first `upto` events (global index) revealed"""
    page = page_of_beat(s, beat)
    ev = [(i, e) for i, e in enumerate(events(s)) if e['page'] == page and i < upto]
    pos = _layout(s, mod, page, bw, bh)
    with plt.rc_context(RC):
        fig = plt.figure(figsize=(bw / DPI, bh / DPI), dpi=DPI, facecolor='white')
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, bw); ax.set_ylim(bh, 0); ax.axis('off')
        r = fig.canvas.get_renderer()
        for i, e in ev:
            it = e['it']
            if not any(k in it for k in TEXTKEYS): continue
            x, y, bgw = pos[i]
            _put(ax, s, it, x, y, r, draw=True, bgw=bgw)
        nd = max([e['it']['d'] for i, e in ev if 'd' in e['it']] + [0])
        dax = None
        if s.get('draw') and nd:
            sx = s.get('split', 0.56)
            dax = fig.add_axes([sx, 0.02, 1 - sx - 0.01, 0.96])
            dw, dh = bw * (1 - sx - 0.01), bh * 0.96
            dax.set_xlim(0, dw); dax.set_ylim(0, dh); dax.set_aspect('equal'); dax.axis('off'); dax._wh = (dw, dh)
            with plt.xkcd(scale=0.7, length=140, randomness=1.6):
                plt.rcParams.update({'font.family': ['Ink Free', 'Segoe UI Symbol', 'Segoe UI'], 'path.effects': []})
                getattr(mod, 'draw_' + s['draw'])(dax, nd, dw, dh)
        # the teacher's pen: marks of this step (and kept ones), drawn on top of everything
        global LAST_PATHS
        LAST_PATHS = {}
        pens = [(i, e) for i, e in ev if 'p' in e['it'] and (e['beat'] == beat or e['it'].get('keep'))]
        solo = [i for i, e in pens if e['it'].get('solo')]   # 'solo': the marker moves here (earlier marks of the step are wiped)
        if solo: pens = [(i, e) for i, e in pens if i >= solo[-1] or e['it'].get('keep')]
        pens = [(i, e) for i, e in pens if i not in EXCLUDE]
        if pens:
            if dax is not None: dax.apply_aspect()
            pax = fig.add_axes([0, 0, 1, 1]); pax.set_xlim(0, bw); pax.set_ylim(bh, 0); pax.axis('off'); pax.patch.set_alpha(0)
            for i, e in pens:
                strokes = pen_strokes(s, e['it'], i, dax, page, bw, bh)
                for st, wpx, alpha, col in strokes:
                    pax.plot(st[:, 0], st[:, 1], color=col, lw=wpx * PT, alpha=alpha, solid_capstyle='round', solid_joinstyle='round')
                LAST_PATHS[i] = strokes
        fig.canvas.draw()
        im = Image.frombuffer('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert('RGB')
        plt.close(fig)
    return im

# ---------- the pen ----------
LAST_PATHS = {}           # event index -> strokes drawn by the last render() (board pixel coords, y down); used to animate
LAST_OFF = (0, 0)         # where build2.wb_frame pasted the board inside the video frame
EXCLUDE = set()           # event indexes to leave out of render() (build2 uses it for the frame just before a solo mark)
PEN_W = 6.0               # marker stroke width (px)
HILITE = '#ffd43b'

def anchor(ax, name, x, y):
    """name a point of a drawing (its own coordinates) so pen marks can refer to it, e.g. ('circle', 'R1', 0.6, 0.4)"""
    ax.__dict__.setdefault('_pen_anchors', {})[name] = (x, y)

def _smooth_noise(n, rng, amp):
    k = max(3, n // 14 + 2)
    knots = rng.normal(0, amp, (k, 2))
    xs = np.linspace(0, k - 1, n)
    return np.c_[np.interp(xs, np.arange(k), knots[:, 0]), np.interp(xs, np.arange(k), knots[:, 1])]

def _dense(pts, step=6.0):
    pts = np.asarray(pts, float); out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(np.hypot(*(b - a)) / step))
        out += [a + (b - a) * f for f in np.linspace(0, 1, n + 1)[1:]]
    return np.array(out)

def _shape(kind, g, rng, col):
    """pixel-space strokes for one mark. g: geometry already in board pixels (y down)"""
    W_ = PEN_W; S = []
    def add(pts, w=W_, alpha=0.92, c=col, jit=1.1):
        p = _dense(pts) if len(pts) < 40 else np.asarray(pts, float)
        S.append((p + _smooth_noise(len(p), rng, jit), w, alpha, c))
    if kind == 'circle':
        cx, cy, rx, ry = g; a0 = rng.uniform(-2.7, -2.1)
        t = a0 + np.linspace(0, 2 * np.pi + 0.55, 150); gr = np.linspace(1.0, 1.0 + min(0.09, 12 / max(rx, ry, 1)), t.size)   # overshoot ~12 px at most
        add(np.c_[cx + rx * gr * np.cos(t), cy + ry * gr * np.sin(t)], jit=1.4)
    elif kind == 'box':
        x0, y0, x1, y1 = g; add([(x0, y0 + 4), (x0, y1), (x1, y1), (x1, y0), (x0 - 6, y0 + 1)])
    elif kind == 'underline':
        x0, y0, x1, y1 = g; add([(x0, y0), (x1, y1)])
    elif kind == 'strike':                           # crossed out, but what's underneath stays readable
        x0, y0, x1, y1 = g; add([(x0, y0), (x1, y1)], w=4.0, alpha=0.6, jit=0.8)
    elif kind == 'highlight':
        x0, y0, x1, y1 = g; add([(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)], w=abs(y1 - y0), alpha=0.38, c=HILITE if col == COL['red'] else col, jit=0.6)
    elif kind == 'arrow':
        x0, y0, x1, y1 = g; p0, p1 = np.array([x0, y0], float), np.array([x1, y1], float)
        add([p0, p1]); d = (p1 - p0) / (np.hypot(*(p1 - p0)) or 1); L = 20
        rot = lambda v, a: np.array([v[0] * np.cos(a) - v[1] * np.sin(a), v[0] * np.sin(a) + v[1] * np.cos(a)])
        add([p1 - L * rot(d, 0.5), p1, p1 - L * rot(d, -0.5)], jit=0.5)
    elif kind == 'cross':
        x, y, s_ = g; add([(x - s_, y - s_), (x + s_, y + s_)], jit=0.6); add([(x + s_, y - s_), (x - s_, y + s_)], jit=0.6)
    elif kind == 'check':
        x, y, s_ = g; add([(x - s_, y), (x - s_ / 3, y + s_ * 0.75), (x + s_, y - s_ * 0.9)], jit=0.6)
    return S

def _text_bbox(s, it_on, page, bw, bh):
    """board-pixel bbox (x0, y0, x1, y1, is_code, x_of_col) of the written line containing it_on['on']"""
    key = (id(s), page, bw, bh); pos = _LAY[key]; size = _SIZE[key]; want = it_on['on']
    want_m = norm({'m': want})['m']                  # written lines get \frac -> \dfrac; match either form
    for i, e in enumerate(events(s)):
        it = e['it']
        if i not in pos: continue
        txt = it.get('m', it.get('k', it.get('o')))
        if txt is None or (want not in txt and not ('m' in it and want_m in txt)): continue
        x, y, _ = pos[i]; wd, ht = size[i]
        if 'm' in it: return (x, y, x + wd, y + ht), None
        px = it.get('fs', s.get('cfs', 30 if s.get('draw') else 36)); cw = _CW.get(px, px * 0.55)
        c0, c1 = it_on.get('cols') or ((0, len(txt.rstrip())) if it_on.get('line') else (txt.index(want), txt.index(want) + len(want)))
        return (x + c0 * cw, y + 1, x + c1 * cw, y + px * 1.38 - 1), True
    raise KeyError(f"pen: no written line contains {want!r}")

def pen_strokes(s, it, i, dax, page, bw, bh):
    marks = it['p']
    if callable(marks):                              # lambda A, w, h: [...]  (A = the drawing's named points)
        marks = marks(dax.__dict__.get('_pen_anchors', {}), *dax._wh) if dax is not None else []
    marks = marks if isinstance(marks, list) else [marks]
    if not marks: return []
    col = c_(it.get('c', 'red'))
    import hashlib   # stable seed (built-in hash() changes per process, which would re-render every build)
    rng = np.random.default_rng(int(hashlib.md5(f"{s.get('h', '')}|{i}|{marks!r}".encode()).hexdigest()[:8], 16))
    out = []
    if 'on' in it:                                   # mark a written line / code
        (x0, y0, x1, y1), is_code = _text_bbox(s, it, page, bw, bh); my = (y0 + y1) / 2
        for m in marks:
            k = m[0] if isinstance(m, (tuple, list)) else m
            if k == 'span':                              # one box from line 'on' down to line 'to' (e.g. a column of a sum)
                (a0, b0, a1, b1), _ = _text_bbox(s, {'on': it['to'], 'cols': it.get('cols'), 'line': it.get('line')}, page, bw, bh)
                X0, Y0, X1, Y1 = min(x0, a0), min(y0, b0), max(x1, a1), max(y1, b1)
                if X1 - X0 < 60:                         # a single column: a highlighter swipe down it (a box would cut the neighbours)
                    xc = (X0 + X1) / 2; c_hl = HILITE if col == COL['red'] else col
                    S = [(np.array([[xc, Y0 - 2], [xc, Y1 + 2]], float), X1 - X0 + 6, 0.38, c_hl)]
                    out += [(_dense(p) + _smooth_noise(len(_dense(p)), rng, 0.5), w_, a_, c__) for p, w_, a_, c__ in S]
                else: out += _shape('box', (X0 - 6, Y0 - 4, X1 + 6, Y1 + 4), rng, col)
                continue
            if k == 'link':                              # arrow down/up the right side, from line 'on' to line 'to'
                (a0, b0, a1, b1), _ = _text_bbox(s, {'on': it['to'], 'line': True}, page, bw, bh)
                X = max(x1, a1) + 28; out += _shape('arrow', (X, my, X, (b0 + b1) / 2), rng, col); continue
            if k == 'circle' and x1 - x0 > 260: k = 'box'          # an ellipse round a long line cuts its ends: box it instead
            g = {'circle': ((x0 + x1) / 2, my, (x1 - x0) / 2 + 12, (y1 - y0) / 2 + 9),
                 'box': (x0 - 8, y0 - 5, x1 + 8, y1 + 5), 'underline': (x0, y1 + 3, x1, y1 + 3), 'strike': (x0 - 4, my, x1 + 4, my),
                 'highlight': (x0 - 4, y0 + 2, x1 + 4, y1 - 2), 'check': (x1 + 30, my, 16), 'cross': (x1 + 30, my, 13),
                 'arrow': (x0 - 110, my, x0 - 14, my)}[k]
            out += _shape(k, g, rng, col)
        return out
    if dax is None: return out
    anchors = dax.__dict__.get('_pen_anchors', {})
    tax = dax
    def P(args, k):          # point (data coords, possibly an anchor name) -> (data xy, pixel xy, next arg index)
        if isinstance(args[k], str):
            if args[k] not in anchors: raise KeyError(f"pen: drawing has no point named {args[k]!r} (has: {sorted(anchors)[:12]}...)")
            x, y = anchors[args[k]]; k += 1
        else: x, y = args[k], args[k + 1]; k += 2
        d = tax.transData.transform((x, y)); return (x, y), np.array([d[0], bh - d[1]]), k
    for m in marks:
        k = m[0]; a = list(m[1:])
        if '@' in k:                                     # 'circle@1': coordinates of the 2nd schematic drawn on this board
            k, ci = k.split('@'); circs = dax.figure.__dict__.get('_circuits', [])
            tax = circs[int(ci)]; tax.apply_aspect()
        else: tax = dax
        if k == 'row':                                   # ('row', table_row_index): box around a whole table row
            x0, x1, y, rh = dax.__dict__['_pen_rows'][a[0]]
            p0 = dax.transData.transform((x0 - 6, y - rh * 0.45)); p1 = dax.transData.transform((x1 + 6, y + rh * 0.45))
            out += _shape('box', (p0[0], bh - p1[1], p1[0], bh - p0[1]), rng, col); continue
        if k == 'circle':
            (x, y), c, j = P(a, 0); rx, ry = a[j], a[j + 1]
            e = tax.transData.transform((x + rx, y + ry)); r = np.abs(np.array([e[0], bh - e[1]]) - c)
            g = (c[0], c[1], r[0], r[1])
        elif k in ('box', 'highlight', 'strike', 'arrow'):
            _, p0, j = P(a, 0); _, p1, _ = P(a, j)
            g = (min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])) if k in ('box', 'highlight') else (*p0, *p1)
        elif k == 'underline':
            _, p0, _ = P([a[0], a[2]], 0); _, p1, _ = P([a[1], a[2]], 0); g = (*p0, *p1)
        elif k in ('cross', 'check'):
            _, p, j = P(a, 0); g = (p[0], p[1], a[j] if len(a) > j else (16 if k == 'check' else 13))
        else: raise ValueError('pen: unknown mark ' + str(k))
        out += _shape(k, g, rng, col)
    return out

# ---------- helpers for lesson draw_* functions (pixel coords, y up) ----------
def c_(c): return COL.get(c, c)
def arr(ax, x0, y0, x1, y1, c='ink', lw=3.5, ms=30, style='-|>', rad=0.0):
    ax.annotate('', (x1, y1), (x0, y0), arrowprops=dict(arrowstyle=style, lw=lw, color=c_(c), mutation_scale=ms, shrinkA=0, shrinkB=0,
                                                        connectionstyle=f'arc3,rad={rad}'))

def circle(ax, x, y, r, fc='#dfe8f7', c='ink', lw=3, text='', fs=30, tc='ink'):
    t = np.linspace(0, 2 * np.pi, 80); poly(ax, list(zip(x + r * np.cos(t), y + r * np.sin(t))), fc=fc, c=c, lw=lw)
    if text: lab(ax, x, y, text, fs, tc)

def selfloop(ax, x, y, r, label='', c='ink', fs=28, up=True):
    """small loop arrow on top (or bottom) of a state circle"""
    s = 1 if up else -1
    arr(ax, x - 0.5 * r, y + s * 0.85 * r, x + 0.5 * r, y + s * 0.85 * r, c, 2.5, 20, rad=-1.6 * s)
    if label: lab(ax, x, y + s * 2.0 * r, label, fs, c)
def lab(ax, x, y, s, fs=34, c='ink', ha='center', va='center', **kw):
    return ax.text(x, y, s, fontsize=fs * PT, color=c_(c), ha=ha, va=va, **kw)
def ln(ax, xs, ys, c='ink', lw=3, **kw):
    return ax.plot(xs, ys, color=c_(c), lw=lw, solid_capstyle='round', **kw)
def dot(ax, x, y, c='ink', s=11, hollow=False):
    ax.plot([x], [y], 'o', ms=s, color=c_(c), mfc='white' if hollow else c_(c), mew=3)
def poly(ax, pts, fc='none', c='ink', lw=3, alpha=1):
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=c_(c), lw=lw, alpha=alpha))
def rect(ax, x, y, w, h, fc='none', c='ink', lw=3):
    poly(ax, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fc, c, lw)
def axes(ax, x0, y0, x1, y1, xl='x', yl='y', c='gray'):
    arr(ax, x0, y0, x1, y0, c, 2.5, 22); arr(ax, x0, y0, x0, y1, c, 2.5, 22)
    lab(ax, x1 + 4, y0 - 26, xl, 30, c, ha='right'); lab(ax, x0 - 14, y1 - 6, yl, 30, c, ha='right')

def node(ax, x, y, w, h, text='', fc='#dfe8f7', c='ink', fs=30, tc='ink', lw=2.5):
    """labelled box with lower-left corner (x, y)"""
    rect(ax, x, y, w, h, fc=fc, c=c, lw=lw)
    if text: lab(ax, x + w / 2, y + h / 2, text, fs, tc)

def table(ax, x, ytop, cols, rows, cw, rh=60, nrows=None, fs=30, hl=None, hc='blue'):
    """grid table: header row + the first `nrows` data rows. hl = {(r, c): colour} highlights cells"""
    import numpy as _np
    xs = _np.cumsum([x] + list(cw)); nr = len(rows) if nrows is None else nrows
    for j, c in enumerate(cols): lab(ax, (xs[j] + xs[j + 1]) / 2, ytop - rh / 2, str(c), fs, hc)
    ln(ax, [x, xs[-1]], [ytop - rh, ytop - rh], lw=2.5)
    for j in range(len(cols)): anchor(ax, f'h{j}', (xs[j] + xs[j + 1]) / 2, ytop - rh / 2)
    for i in range(len(rows)):           # named cells for the pen: 'r<row>c<col>', and 'row<row>' = (left edge, right edge, y)
        y = ytop - rh * (i + 1.5)
        for j in range(len(cols)): anchor(ax, f'r{i}c{j}', (xs[j] + xs[j + 1]) / 2, y)
        ax.__dict__.setdefault('_pen_rows', {})[i] = (xs[0], xs[-1], y, rh)
    for i, r in enumerate(rows[:nr]):
        y = ytop - rh * (i + 1.5)
        for j, v in enumerate(r):
            col = (hl or {}).get((i, j), 'ink')
            lab(ax, (xs[j] + xs[j + 1]) / 2, y, str(v), fs, col)

def wave(ax, x0, y0, levels, cw=60, hgt=60, c='blue', name=None, fs=28, lw=3):
    """digital waveform: levels like [0,1,1,0] or 'X' for unknown; y0 = low level"""
    xs, ys = [], []
    for k, v in enumerate(levels):
        if v == 'X':
            if xs: ln(ax, xs, ys, c=c, lw=lw); xs, ys = [], []
            poly(ax, [(x0 + k * cw, y0 + hgt / 2), (x0 + k * cw + 8, y0 + hgt), (x0 + (k + 1) * cw - 8, y0 + hgt), (x0 + (k + 1) * cw, y0 + hgt / 2),
                      (x0 + (k + 1) * cw - 8, y0), (x0 + k * cw + 8, y0)], fc='#e7e9ee', c='gray', lw=2); continue
        yy = y0 + hgt * v
        xs += [x0 + k * cw, x0 + (k + 1) * cw]; ys += [yy, yy]
    if xs: ln(ax, xs, ys, c=c, lw=lw)
    if name: lab(ax, x0 - 14, y0 + hgt / 2, name, fs, c, ha='right')

def mos(ax, x, y, kind='n', s=1.0, c='ink', lw=3):
    """hand-drawn MOSFET centred at (x, y), gate on the left.
    returns terminals: 'g' gate end, 'top' and 'bot' (NMOS: drain top / source bottom; PMOS: source top / drain bottom)"""
    ln(ax, [x, x], [y - 42 * s, y + 42 * s], c=c, lw=lw + 1)                       # channel
    ln(ax, [x - 16 * s, x - 16 * s], [y - 34 * s, y + 34 * s], c=c, lw=lw)          # gate plate
    gx = x - 16 * s
    if kind == 'p':
        t = np.linspace(0, 2 * np.pi, 40); ln(ax, gx - 10 * s + 9 * s * np.cos(t), y + 9 * s * np.sin(t), c=c, lw=lw - 0.5); gx -= 19 * s
    ln(ax, [gx, x - 85 * s], [y, y], c=c, lw=lw)
    for sgn in (1, -1):
        ln(ax, [x, x + 42 * s, x + 42 * s], [y + sgn * 30 * s, y + sgn * 30 * s, y + sgn * 85 * s], c=c, lw=lw)
    return {'g': (x - 85 * s, y), 'top': (x + 42 * s, y + 85 * s), 'bot': (x + 42 * s, y - 85 * s)}

def circuit(ax, n, build, fs=17, lw=2.6, pad=0.8, unit=3.0):
    """hand-drawn schematic that grows with n.
    build(d, elm, v): add schemdraw elements to d; colour each one with v(k) (or v(k, 'red')), which is
    invisible until reveal step k. Every element is always placed, so the layout never shifts."""
    import schemdraw, schemdraw.elements as elm
    ax.figure.__dict__.setdefault('_circuits', []).append(ax)      # pen marks 'circle@k' use the k-th circuit's coordinates
    schemdraw.config(unit=unit, fontsize=fs, lw=lw, font='Ink Free')
    plt.rcParams['font.family'] = ['Ink Free', 'Segoe UI Symbol', 'Segoe UI']
    HIDE = '#fefefd'                       # sentinel colour for not-yet-drawn parts (schemdraw rejects 'none')
    v = lambda k, c='ink': c_(c) if n >= k else HIDE
    d = schemdraw.Drawing(canvas=ax, show=False)
    build(d, elm, v)
    d.draw(show=False)
    for num in plt.get_fignums():          # schemdraw opens a spare pyplot figure each call: close it (memory leak over a full build)
        f_ = plt.figure(num)
        if f_ is not ax.figure: plt.close(f_)
    import matplotlib.colors as mc
    hid = mc.to_rgba(HIDE)
    for a in list(ax.lines) + list(ax.patches) + list(ax.texts):
        cols = []
        for g in ('get_color', 'get_edgecolor', 'get_facecolor'):
            if hasattr(a, g):
                try: cols.append(tuple(mc.to_rgba(getattr(a, g)())))
                except Exception: pass
        if any(cc[:3] == hid[:3] for cc in cols): a.set_visible(False)
    # real extents: every drawn line vertex + every label anchor (schemdraw's own bbox over-estimates text)
    pts = [xy for l in ax.lines for xy in l.get_xydata()] + [t.get_position() for t in ax.texts]
    xs_ = [p[0] for p in pts]; ys_ = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs_) - pad - 0.6, max(xs_) + pad + 0.6, min(ys_) - pad, max(ys_) + pad
    W_, H_ = ax.get_window_extent().width, ax.get_window_extent().height
    sc = max((x1 - x0) / W_, (y1 - y0) / H_)          # data units per pixel, equal aspect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ax.set_xlim(cx - W_ * sc / 2, cx + W_ * sc / 2); ax.set_ylim(cy - H_ * sc / 2, cy + H_ * sc / 2); ax.set_aspect('equal'); ax.axis('off')
    # second pass: include the real rendered size of every visible label, then refit
    r = ax.figure.canvas.get_renderer(); inv = ax.transData.inverted()
    for t in ax.texts:
        if not t.get_visible() or not t.get_text().strip(): continue
        e = t.get_window_extent(r); (a0, b0), (a1, b1) = inv.transform([[e.x0, e.y0], [e.x1, e.y1]])
        x0, x1, y0, y1 = min(x0, a0 - 0.5), max(x1, a1 + 0.5), min(y0, b0 - 0.3), max(y1, b1 + 0.3)
    sc = max((x1 - x0) / W_, (y1 - y0) / H_); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ax.set_xlim(cx - W_ * sc / 2, cx + W_ * sc / 2); ax.set_ylim(cy - H_ * sc / 2, cy + H_ * sc / 2)
    import os as _os
    if _os.environ.get('BOARD_DEBUG'): print('circuit fit', dict(W=W_, H=H_, bbox=(round(x0, 2), round(x1, 2), round(y0, 2), round(y1, 2)), xl=ax.get_xlim(), pos=ax.get_position().bounds))

def pen(lesson, heading, step, *items):
    """add pen marks to step `step` of the whiteboard slide whose heading starts with `heading`.
    Each item is placed in sentence order (by its 'at'); existing items keep their timing."""
    s = next(x for x in lesson['slides'] if x.get('t') == 'wb' and x.get('h', '').startswith(heading))
    w = s['steps'][step].setdefault('w', [])
    for j, it in enumerate(w):                       # freeze each item's default 'at' (= its position) before inserting
        if isinstance(it, str): w[j] = {'m': it, 'at': j}
        elif 'at' not in it: it['at'] = j
    for it in items:
        it = dict(it); it.setdefault('at', 0)
        k = max([j + 1 for j, x in enumerate(w) if x['at'] <= it['at']] + [0])
        w.insert(k, it)

def spen(lesson, heading, beat, *items):
    """pen marks on an ordinary (non-whiteboard) slide, during narration beat `beat`.
    item: {'on': 'text on the slide', 'p': 'circle'|'box'|'underline'|'highlight'|'strike'|'check'|'cross'|'arrow' (or a list), 'at': sentence}
       or {'fig': [('circle', fx, fy, frx, fry), ('arrow', fx0, fy0, fx1, fy1), ...], 'at': ...}  (fractions of the figure, y down)"""
    s = next(x for x in lesson['slides'] if x.get('t') != 'wb' and x.get('h', '').startswith(heading))
    for it in items: s.setdefault('pen', []).append(dict(it, b=beat))

def insert(lesson, after, slide):
    """insert a whiteboard slide right after the slide whose heading starts with `after`"""
    S = lesson['slides']
    i = next(k for k, s in enumerate(S) if s.get('h', '').startswith(after))
    S.insert(i + 1, slide)

def plain(m):
    """board line -> plain text for the Q&A timeline"""
    import re
    t = re.sub(r'\\(frac|dfrac)\{([^{}]*)\}\{([^{}]*)\}', r'(\2)/(\3)', m)
    t = re.sub(r'\\(left|right|,|;|!|quad|qquad)', ' ', t)
    t = re.sub(r'\\([A-Za-z]+)', r'\1', t)
    return re.sub(r'[${}]', '', t).replace('  ', ' ').strip()
