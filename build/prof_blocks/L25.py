# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def _L(ax, x0, y0, x1, y1, c='ink', lw=3):
    B.ln(ax, [x0, x1], [y0, y1], c, lw)

def draw_aoi(ax, n, w, h):
    # simple network sketch: pull-down on bottom, pull-up on top, output in middle
    def tr(x, y, name, col):
        B.rect(ax, x - 45, y - 30, 90, 60, fc='white', c=col, lw=3); B.lab(ax, x, y, name, 30, col)
    mid = h * 0.50
    if n >= 1:
        _L(ax, w * 0.05, mid, w * 0.95, mid, 'ink', 3); B.lab(ax, w * 0.95, mid + 28, 'Y', 34, 'ink', ha='right')
        B.lab(ax, w * 0.5, h * 0.06, 'GND', 26, 'gray'); _L(ax, w * 0.15, h * 0.12, w * 0.85, h * 0.12, 'gray', 3)
        # pull-down: (A series B) parallel C
        xa = w * 0.32; xc = w * 0.68
        _L(ax, xa, mid, xa, mid - 25, 'blue', 3); tr(xa, mid - 60, 'A', 'blue'); _L(ax, xa, mid - 90, xa, mid - 115, 'blue', 3)
        tr(xa, mid - 145, 'B', 'blue'); _L(ax, xa, mid - 175, xa, h * 0.12, 'blue', 3)
        _L(ax, xc, mid, xc, mid - 70, 'blue', 3); tr(xc, mid - 100, 'C', 'blue'); _L(ax, xc, mid - 130, xc, h * 0.12, 'blue', 3)
        B.lab(ax, w * 0.5, mid - 220, 'NMOS', 24, 'blue')
    if n >= 2:
        B.lab(ax, w * 0.5, h * 0.94, 'VDD', 26, 'gray'); _L(ax, w * 0.15, h * 0.88, w * 0.85, h * 0.88, 'gray', 3)
        # pull-up: (A parallel B) series C
        xa = w * 0.32; xb = w * 0.68; xm = w * 0.5
        _L(ax, xm, mid, xm, mid + 25, 'red', 3); tr(xm, mid + 55, 'C', 'red'); _L(ax, xm, mid + 85, xm, mid + 110, 'red', 3)
        _L(ax, xa, mid + 110, xb, mid + 110, 'red', 3)
        _L(ax, xa, mid + 110, xa, mid + 125, 'red', 3); tr(xa, mid + 155, 'A', 'red'); _L(ax, xa, mid + 185, xa, h * 0.88, 'red', 3)
        _L(ax, xb, mid + 110, xb, mid + 125, 'red', 3); tr(xb, mid + 155, 'B', 'red'); _L(ax, xb, mid + 185, xb, h * 0.88, 'red', 3)
        B.lab(ax, w * 0.5, mid + 225, 'PMOS', 24, 'red')

B.insert(LESSON, 'Static CMOS gates: NAND and NOR', {'t': 'wb', 'h': 'Worked example: any inverting expression is one gate', 'draw': 'aoi', 'split': 0.52, 'steps': [
    {'say': "Students usually ask: what if the function isn't just NAND or NOR? The same recipe builds any inverting expression as a single gate. Take Y equals not of A and B, or C. This is called an and or invert gate.",
     'w': [{'m': r'$Y = \overline{A\cdot B + C}$', 'fs': 56, 'at': 1}]},
    {'say': "Step one, the pull down network: it must conduct when the expression inside the bar is true. AND means series, OR means parallel. So A in series with B, and that pair in parallel with C.",
     'w': [{'m': 'pull-down conducts when  A·B + C = 1', 'c': 'blue', 'at': 1}, {'m': 'AND → series,   OR → parallel', 'c': 'blue', 'at': 2}, {'d': 1, 'at': 2}]},
    {'say': "Step two, the pull up network is the dual: swap series and parallel. A in parallel with B, and that pair in series with C. Check one case: A equals B equals one, C equals zero. The series A B chain conducts, pulling Y low, and in the pull up, C's PMOS is on but both A and B PMOS are off, so there's no path up. Y is zero. Correct.",
     'w': [{'m': 'pull-up = the dual: swap series ↔ parallel', 'c': 'red', 'at': 1}, {'d': 2, 'at': 1},
           {'m': 'A=B=1, C=0:  down path on, up path off  →  Y = 0', 'at': 3}]},
    {'say': "Six transistors, one gate delay. Built from separate AND, OR and NOT gates, it would take more transistors and three levels of delay. That's why standard cell libraries are full of these compound gates.",
     'w': [{'m': '6 transistors, 1 stage of delay', 'c': 'green', 'box': True, 'at': 0}]},
]})

G = 'Worked example: any inverting expression is one gate'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'AND → series', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'A=B=1, C=0', 'at': 5})
