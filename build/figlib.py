"""Shared figure helpers. Every figure function in a lesson has signature f(path, w, h) and writes a PNG."""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Polygon, Arc
import numpy as np
from matplotlib.path import Path

C = dict(blue='#2B5CAB', orange='#E07B39', green='#2E9E6A', red='#C8443B', purple='#7A4FB5', gray='#8A93A3',
         ink='#1B2333', light='#E8EEF8', yellow='#E8B931', teal='#1F8A9E', pale='#F4F7FC', mut='#5D6778',
         lblue='#D6E2F5', lorange='#FBE3D2', lgreen='#D5F0E3', lred='#F6D9D6', lpurple='#E6DDF3', lyellow='#FBF0CF')

plt.rcParams.update({
    'font.family': ['Segoe UI', 'DejaVu Sans'], 'font.size': 22, 'mathtext.fontset': 'stix',
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.linewidth': 1.6,
    'axes.edgecolor': C['ink'], 'axes.labelcolor': C['ink'], 'xtick.color': C['ink'], 'ytick.color': C['ink'],
    'axes.titleweight': 'bold', 'axes.titlesize': 26, 'axes.titlepad': 14, 'axes.labelsize': 24,
    'lines.linewidth': 3.2, 'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white',
    'axes.grid': False, 'grid.color': '#DCE2EC', 'grid.linewidth': 1.2, 'legend.frameon': False, 'legend.fontsize': 21,
    'xtick.labelsize': 20, 'ytick.labelsize': 20,
})

# ---------- canvases ----------
def canvas(w, h, units=100, need=None, exact=False):
    """blank diagram canvas; x in [0, units], y in [0, H] (equal aspect), H = units*h/w but at least `need`.
    returns fig, ax, H"""
    ref = 1400 if w > 1250 else 900          # fixed reference width -> layout independent of box size
    h = ref * h / w; w = ref
    H = units * h / w
    if need and (H < need or exact):
        H = need; h = w * need / units
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, units); ax.set_ylim(0, H); ax.set_aspect('equal'); ax.axis('off')
    fig._is_canvas = True
    return fig, ax, H

def plot(w, h, grid=True, **kw):
    s = 0.8   # draw smaller, engine scales up -> bigger text
    fig, ax = plt.subplots(figsize=(w * s / 100, h * s / 100), dpi=100, **kw)
    if grid:
        for a in np.atleast_1d(ax).ravel(): a.grid(True)
    return fig, ax

def save(fig, path, tight=None):
    if tight is None: tight = not getattr(fig, '_is_canvas', False)
    if tight: fig.savefig(path, dpi=100, bbox_inches='tight', pad_inches=0.25)
    else: fig.savefig(path, dpi=100)
    plt.close(fig)

def axes0(ax, xlabel=None, ylabel=None):
    """math-style axes through the origin"""
    ax.axhline(0, color=C['ink'], lw=1.6, zorder=1); ax.axvline(0, color=C['ink'], lw=1.6, zorder=1)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)

def hole(ax, x, y, c=None, s=11):
    ax.plot([x], [y], 'o', ms=s, mfc='white', mec=c or C['blue'], mew=2.6, zorder=6)

def soliddot(ax, x, y, c=None, s=11):
    ax.plot([x], [y], 'o', ms=s, color=c or C['blue'], zorder=6)

def note(ax, x, y, s, c=None, fs=20, **kw):
    ax.text(x, y, s, fontsize=fs, color=c or C['ink'], zorder=7, bbox=dict(fc='white', ec='none', alpha=0.85, pad=2), **kw)

# ---------- primitives ----------
def box(ax, x, y, w, h, text='', fc=None, ec=None, fs=22, tc=None, r=1.2, bold=False, lw=2.5, ha='center', alpha=1, z=2, ls='-'):
    fc = fc or C['lblue']; ec = ec or C['blue']; tc = tc or C['ink']
    p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z, ls=ls)
    ax.add_patch(p)
    if text:
        tx = x + w / 2 if ha == 'center' else x + 1.2
        ax.text(tx, y + h / 2, text, ha=ha, va='center', fontsize=fs, color=tc, fontweight='bold' if bold else 'normal', zorder=z + 1, linespacing=1.25)
    return (x + w / 2, y + h / 2)

def arrow(ax, p1, p2, text=None, color=None, rad=0.0, lw=3, style='-|>', fs=19, tc=None, off=(0, 1.2), ms=22, z=1, ls='-', shrink=0):
    color = color or C['ink']
    a = FancyArrowPatch(p1, p2, connectionstyle=f'arc3,rad={rad}', arrowstyle=style, mutation_scale=ms, lw=lw, color=color,
                        zorder=z, linestyle=ls, shrinkA=shrink, shrinkB=shrink)
    ax.add_patch(a)
    if text:
        mx, my = (p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1]
        ax.text(mx, my, text, ha='center', va='bottom', fontsize=fs, color=tc or color, zorder=z + 2,
                bbox=dict(fc='white', ec='none', pad=1.5, alpha=0.9))
    return a

def line(ax, pts, color=None, lw=3, ls='-', z=1):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=color or C['ink'], lw=lw, ls=ls, zorder=z, solid_capstyle='round')

def txt(ax, x, y, s, fs=22, c=None, ha='center', va='center', bold=False, z=5, **kw):
    return ax.text(x, y, s, fontsize=fs, color=c or C['ink'], ha=ha, va=va, fontweight='bold' if bold else 'normal', zorder=z, **kw)

def dot(ax, x, y, r=0.6, c=None, z=4):
    ax.add_patch(Circle((x, y), r, color=c or C['ink'], zorder=z))

# ---------- composite diagrams ----------
def fsm(ax, states, edges, r=5.0, fs=21, efs=18):
    """states: {name: (x, y, label, color?, double?)}; edges: [(a, b, label, rad)]  (a==b -> self loop; rad = loop angle deg)"""
    for n, s in states.items():
        x, y, lab = s[:3]; col = s[3] if len(s) > 3 and s[3] else C['lblue']; dbl = len(s) > 4 and s[4]
        ax.add_patch(Circle((x, y), r, fc=col, ec=C['blue'], lw=3, zorder=3))
        if dbl: ax.add_patch(Circle((x, y), r * 0.82, fc='none', ec=C['blue'], lw=2, zorder=4))
        ax.text(x, y, lab, ha='center', va='center', fontsize=fs, zorder=5, color=C['ink'], linespacing=1.15)
    for e in edges:
        a, b, lab = e[:3]; rad = e[3] if len(e) > 3 else 0.0
        col = e[4] if len(e) > 4 else C['ink']
        xa, ya = states[a][:2]; xb, yb = states[b][:2]
        if a == b:
            ang = math.radians(rad if rad else 90)
            p1 = (xa + r * math.cos(ang + 0.5), ya + r * math.sin(ang + 0.5)); p2 = (xa + r * math.cos(ang - 0.5), ya + r * math.sin(ang - 0.5))
            c1 = (xa + r * 2.3 * math.cos(ang + 0.6), ya + r * 2.3 * math.sin(ang + 0.6)); c2 = (xa + r * 2.3 * math.cos(ang - 0.6), ya + r * 2.3 * math.sin(ang - 0.6))
            pth = Path([p1, c1, c2, p2], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
            ax.add_patch(FancyArrowPatch(path=pth, arrowstyle='-|>', mutation_scale=20, lw=2.6, color=col, zorder=2))
            lx, ly = xa + r * 2.2 * math.cos(ang), ya + r * 2.2 * math.sin(ang)
            ax.text(lx, ly, lab, ha='center', va='center', fontsize=efs, color=col, zorder=6, bbox=dict(fc='white', ec='none', pad=1))
            continue
        d = math.hypot(xb - xa, yb - ya); ux, uy = (xb - xa) / d, (yb - ya) / d
        p1 = (xa + ux * r, ya + uy * r); p2 = (xb - ux * r, yb - uy * r)
        ax.add_patch(FancyArrowPatch(p1, p2, connectionstyle=f'arc3,rad={rad}', arrowstyle='-|>', mutation_scale=22, lw=2.8, color=col, zorder=2))
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        nx, ny = uy, -ux  # arc3 control point = mid + rad*(dy, -dx); curve midpoint is half of that
        k = rad * d * 0.5
        ax.text(mx + nx * k, my + ny * k, lab, ha='center', va='center', fontsize=efs, color=col, zorder=6, bbox=dict(fc='white', ec='none', pad=1.2))

def timing(ax, x0, y0, signals, cw=6, rh=7, hi=4, fs=20, names_w=12, colors=None, ncyc=None):
    """signals: list of (name, values) values: 0/1 ints or strings (bus) or 'clk' ; drawn top to bottom from y0"""
    n = ncyc or max(len(v) if not isinstance(v, str) else 0 for _, v in signals)
    for i, (name, vals) in enumerate(signals):
        y = y0 - i * rh; col = (colors or {}).get(name, C['blue'])
        ax.text(x0 - 1.5, y + hi / 2, name, ha='right', va='center', fontsize=fs, color=C['ink'], fontweight='bold')
        if vals == 'clk':
            pts = []
            for k in range(n):
                xa = x0 + k * cw
                pts += [(xa, y), (xa, y + hi), (xa + cw / 2, y + hi), (xa + cw / 2, y), (xa + cw, y)]
            line(ax, pts, col, 2.6); continue
        if all(isinstance(v, int) for v in vals):
            pts = [(x0, y + hi * vals[0])]
            for k, v in enumerate(vals):
                xa = x0 + k * cw
                pts += [(xa, y + hi * v), (xa + cw, y + hi * v)]
            line(ax, pts, col, 2.8)
        else:
            for k, v in enumerate(vals):
                xa = x0 + k * cw; e = 0.6
                if v in ('', None):
                    continue
                ax.add_patch(Polygon([(xa + e, y), (xa + cw - e, y), (xa + cw, y + hi / 2), (xa + cw - e, y + hi), (xa + e, y + hi), (xa, y + hi / 2)],
                                     closed=True, fc=C['lblue'] if v != 'X' else '#EEEEEE', ec=col, lw=2.2))
                ax.text(xa + cw / 2, y + hi / 2, v, ha='center', va='center', fontsize=fs - 3)
    return n

def table(ax, x, y, cols, rows, colw, rowh=5, fs=21, hl=None, hlc=None, header_fc=None):
    """draw a table with top-left at (x, y). hl: set of row indices to highlight"""
    hl = hl or set(); cw = colw if isinstance(colw, (list, tuple)) else [colw] * len(cols)
    xs = [x + sum(cw[:i]) for i in range(len(cols))]
    for j, c in enumerate(cols):
        ax.add_patch(Rectangle((xs[j], y - rowh), cw[j], rowh, fc=header_fc or C['blue'], ec='white', lw=2))
        ax.text(xs[j] + cw[j] / 2, y - rowh / 2, c, ha='center', va='center', fontsize=fs, color='white', fontweight='bold')
    for i, r in enumerate(rows):
        yy = y - rowh * (i + 2)
        fc = (hlc or C['lyellow']) if i in hl else (C['pale'] if i % 2 == 0 else 'white')
        for j, v in enumerate(r):
            ax.add_patch(Rectangle((xs[j], yy), cw[j], rowh, fc=fc, ec='#D5DCE8', lw=1.2))
            ax.text(xs[j] + cw[j] / 2, yy + rowh / 2, str(v), ha='center', va='center', fontsize=fs, color=C['ink'])

def bars(ax, labels, values, colors=None, fmt='{:.0f}', horizontal=False, fs=20):
    cols = colors or [C['blue']] * len(values)
    if horizontal:
        b = ax.barh(labels, values, color=cols)
        for r, v in zip(b, values): ax.text(r.get_width(), r.get_y() + r.get_height() / 2, ' ' + fmt.format(v), va='center', fontsize=fs)
    else:
        b = ax.bar(labels, values, color=cols)
        for r, v in zip(b, values): ax.text(r.get_x() + r.get_width() / 2, r.get_height(), fmt.format(v), ha='center', va='bottom', fontsize=fs)
    return b

def chip(ax, x, y, w, h, name, left=(), right=(), fs=20, pin=3.5, fc=None):
    """IC / entity block with labelled pins"""
    box(ax, x, y, w, h, '', fc=fc or C['lblue'], ec=C['blue'], r=0.8)
    ax.text(x + w / 2, y + h + 1.5, name, ha='center', va='bottom', fontsize=fs + 2, fontweight='bold', color=C['blue'])
    for i, p in enumerate(left):
        yy = y + h - (i + 1) * h / (len(left) + 1)
        line(ax, [(x - pin, yy), (x, yy)], C['ink'], 2.6)
        ax.text(x - pin - 0.8, yy, p, ha='right', va='center', fontsize=fs)
    for i, p in enumerate(right):
        yy = y + h - (i + 1) * h / (len(right) + 1)
        line(ax, [(x + w, yy), (x + w + pin, yy)], C['ink'], 2.6)
        ax.text(x + w + pin + 0.8, yy, p, ha='left', va='center', fontsize=fs)

def uml(ax, x, ytop, w, name, attrs=(), methods=(), fs=18, lh=4.2, fc=None, italic=False):
    """UML class box with top-left at (x, ytop). returns dict(top, bottom, left, right, cx)"""
    hh = lh * 1.5 + lh * max(1, len(attrs)) + lh * max(1, len(methods)) + 1.5
    y0 = ytop - hh
    ax.add_patch(Rectangle((x, y0), w, hh, fc=fc or C['lblue'], ec=C['blue'], lw=2.4, zorder=2))
    ax.text(x + w / 2, ytop - lh * 0.75, name, ha='center', va='center', fontsize=fs + 2, fontweight='bold', style='italic' if italic else 'normal', zorder=3)
    ya = ytop - lh * 1.5; ax.plot([x, x + w], [ya, ya], color=C['blue'], lw=2, zorder=3)
    for i, a in enumerate(attrs): ax.text(x + 1, ya - lh * (i + 0.6), a, va='center', fontsize=fs, family='Consolas', zorder=3)
    ym = ya - lh * max(1, len(attrs)) - 0.5; ax.plot([x, x + w], [ym, ym], color=C['blue'], lw=2, zorder=3)
    for i, m in enumerate(methods): ax.text(x + 1, ym - lh * (i + 0.6), m, va='center', fontsize=fs, family='Consolas', zorder=3)
    return dict(top=(x + w / 2, ytop), bottom=(x + w / 2, y0), left=(x, ytop - hh / 2), right=(x + w, ytop - hh / 2), cx=x + w / 2)

def inherit(ax, child_top, parent_bottom):
    ax.add_patch(FancyArrowPatch(child_top, parent_bottom, arrowstyle='-|>,head_length=1.2,head_width=0.8', mutation_scale=14, lw=2.4,
                                 color=C['ink'], fc='white', zorder=4))

# ---------- logic gates (x,y = left-center of body; s = body width) ----------
from matplotlib.path import Path
from matplotlib.patches import PathPatch

def _gate_patch(ax, verts, codes, fc, ec, lw=2.6):
    ax.add_patch(PathPatch(Path(verts, codes), fc=fc, ec=ec, lw=lw, zorder=3))

def gate(ax, kind, x, y, s=8, fc=None, ec=None, label=None, fs=18, n_in=2):
    """returns dict with 'in': [(x,y),...], 'out': (x,y)"""
    fc = fc or 'white'; ec = ec or C['ink']; h = s * 0.8
    M, L4, C4, CL = Path.MOVETO, Path.LINETO, Path.CURVE4, Path.CLOSEPOLY
    ins = [(x, y + h / 2 - h * (i + 1) / (n_in + 1)) for i in range(n_in)]
    if kind in ('and', 'nand'):
        k = 0.5523
        verts = [(x, y - h / 2), (x + s * 0.45, y - h / 2), (x + s * 0.45 + h / 2 * k * 1.1, y - h / 2), (x + s, y - h / 2 * k), (x + s, y),
                 (x + s, y + h / 2 * k), (x + s * 0.45 + h / 2 * k * 1.1, y + h / 2), (x + s * 0.45, y + h / 2), (x, y + h / 2), (x, y - h / 2)]
        codes = [M, L4, C4, C4, C4, C4, C4, L4, L4, CL]
        _gate_patch(ax, verts, codes, fc, ec); out = (x + s, y)
    elif kind in ('or', 'nor', 'xor', 'xnor'):
        verts = [(x, y - h / 2), (x + s * 0.45, y - h / 2),
                 (x + s * 0.78, y - h / 2), (x + s * 0.95, y - h * 0.2), (x + s, y),
                 (x + s * 0.95, y + h * 0.2), (x + s * 0.78, y + h / 2), (x + s * 0.45, y + h / 2),
                 (x, y + h / 2),
                 (x + s * 0.24, y + h * 0.2), (x + s * 0.24, y - h * 0.2), (x, y - h / 2), (x, y - h / 2)]
        codes = [M, L4, C4, C4, C4, C4, C4, C4, L4, C4, C4, C4, CL]
        _gate_patch(ax, verts, codes, fc, ec); out = (x + s, y)
        if kind in ('xor', 'xnor'):
            xv = [(x - s * 0.12, y - h / 2), (x + s * 0.1, y - h * 0.2), (x + s * 0.1, y + h * 0.2), (x - s * 0.12, y + h / 2)]
            ax.add_patch(PathPatch(Path(xv, [M, C4, C4, C4]), fc='none', ec=ec, lw=2.6, zorder=3))
        ins = [(xx + (s * 0.12 if kind in ('or', 'nor') else 0), yy) for xx, yy in ins]
        if kind in ('xor', 'xnor'): ins = [(xx - s * 0.1, yy) for xx, yy in ins]
    elif kind in ('not', 'buf'):
        _gate_patch(ax, [(x, y - h / 2), (x + s * 0.8, y), (x, y + h / 2), (x, y - h / 2)], [M, L4, L4, CL], fc, ec)
        out = (x + s * 0.8, y); ins = [(x, y)]
    if kind in ('nand', 'nor', 'xnor', 'not'):
        r = s * 0.07; ax.add_patch(Circle((out[0] + r, out[1]), r, fc='white', ec=ec, lw=2.4, zorder=4)); out = (out[0] + 2 * r, out[1])
    if label: ax.text(x + s * 0.42, y, label, ha='center', va='center', fontsize=fs, color=C['mut'], zorder=5)
    return {'in': ins, 'out': out}

def wire(ax, pts, color=None, lw=2.6, z=2):
    line(ax, pts, color or C['ink'], lw, z=z)

def schem(path, build, unit=3.0, fontsize=22, lw=2.6, dpi=260):
    """build(d) adds schemdraw elements to Drawing d; saved to PNG"""
    import schemdraw
    schemdraw.config(unit=unit, fontsize=fontsize, lw=lw, font='Segoe UI')
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(path, dpi=dpi)
