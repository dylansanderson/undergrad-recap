import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board
from matplotlib.patches import FancyArrowPatch, Polygon

class M: pass
mod = M()
def draw_incline(ax, n, w, h):
    th = np.radians(30); L = w * 0.85; x0, y0 = w * 0.06, h * 0.18
    if n >= 1:
        ax.add_patch(Polygon([(x0, y0), (x0 + L, y0), (x0 + L, y0 + L * np.tan(th))], closed=True, fill=False, ec=board.INK, lw=3))
        ax.text(x0 + 95, y0 + 18, r'$30°$', fontsize=30 * board.PT)
    cx, cy = x0 + L * 0.55, y0 + L * 0.55 * np.tan(th)
    if n >= 2:
        bw = 90; c, s_ = np.cos(th), np.sin(th)
        pts = [(cx, cy), (cx + bw * c, cy + bw * s_), (cx + bw * c - bw * s_, cy + bw * s_ + bw * c), (cx - bw * s_, cy + bw * c)]
        ax.add_patch(Polygon(pts, closed=True, fc='#dfe8f7', ec=board.INK, lw=3))
        mx, my = np.mean([p[0] for p in pts]), np.mean([p[1] for p in pts])
        mod.m = (mx, my)
    mx, my = mod.m if n >= 2 else (0, 0)
    if n >= 3:
        ax.annotate('', (mx, my - 170), (mx, my), arrowprops=dict(arrowstyle='-|>', lw=3.5, color=board.COL['red'], mutation_scale=30))
        ax.text(mx + 12, my - 160, r'$mg$', fontsize=34 * board.PT, color=board.COL['red'])
    if n >= 4:
        ax.annotate('', (mx - 150 * np.sin(th), my + 150 * np.cos(th)), (mx, my), arrowprops=dict(arrowstyle='-|>', lw=3.5, color=board.COL['blue'], mutation_scale=30))
        ax.text(mx - 150 * np.sin(th) - 40, my + 150 * np.cos(th) + 10, r'$N$', fontsize=34 * board.PT, color=board.COL['blue'])
mod.draw_incline = draw_incline

s = {'t': 'wb', 'h': 'Worked example', 'draw': 'incline', 'split': 0.55, 'steps': [
    {'say': 'a. b. c.', 'w': ['Block on a 30° ramp, no friction: find $a$', {'d': 1}, {'d': 2}]},
    {'say': 'a. b. c. d. e.', 'w': [{'d': 3}, {'d': 4}, r'$\sum F_{\parallel} = mg\,\sin\theta = ma$', r'$a = g\,\sin 30° = 9.8 \times 0.5$',
                                   {'m': r'$a = 4.9\ \mathrm{m/s^2}$', 'c': 'red', 'box': True, 'gap': 8}]},
    {'say': 'a. b.', 'w': [r'Check: $\theta \to 90°$ gives $a \to g$ (free fall) ✓', r'$\frac{d}{dx}\sin(x^2) = 2x\cos(x^2)$,  $\int_0^1 x^2\,dx = \frac{1}{3}$,  $\sqrt{2}\approx 1.414$']},
]}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review')
ims = [board.render(s, mod, 2, k, 1740, 760) for k in (board.n_through(s, 2) - 1, board.n_through(s, 2))]
ims[1].save(os.path.join(out, 'wb_test.png'))
a, b = np.asarray(ims[0]).astype(int), np.asarray(ims[1]).astype(int)
d = np.abs(a - b).sum(2) > 24; ys, xs = np.where(d)
print('diff bbox between last two states:', xs.min(), ys.min(), xs.max(), ys.max(), 'pixels changed', d.sum())
