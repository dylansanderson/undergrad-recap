import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

# ======================================================================= figures
def fig_scale(path, w, h):
    fig, ax = plot(w, h)
    chips = [('4004\n1971', 2.3e3), ('8086\n1978', 2.9e4), ('Pentium\n1993', 3.1e6),
             ('Pentium 4\n2000', 4.2e7), ('Core 2\n2006', 2.91e8), ('Apple M1\n2020', 1.6e10)]
    labs = [c[0] for c in chips]; vals = [c[1] for c in chips]
    cols = [C['gray']] * 2 + [C['blue']] * 4
    b = ax.bar(labs, vals, color=cols); ax.set_yscale('log'); ax.set_ylim(1e3, 1e11)
    for r, v in zip(b, vals):
        s = f'{v/1e9:.0f} billion' if v >= 1e9 else (f'{v/1e6:.0f} million' if v >= 1e6 else f'{v:,.0f}')
        ax.text(r.get_x() + r.get_width() / 2, v * 1.6, s, ha='center', fontsize=18, fontweight='bold')
    ax.set_ylabel('transistors (log scale)'); ax.tick_params(axis='x', labelsize=16)
    ax.set_title('Transistors per chip')
    ax.annotate('drawn by hand', xy=(0.5, 3e4), xytext=(0.6, 3e7), fontsize=19, color=C['red'], ha='center',
                arrowprops=dict(arrowstyle='->', color=C['red'], lw=2))
    ax.annotate('only possible\nwith HDLs', xy=(4.6, 3e9), xytext=(3.2, 1.5e10), fontsize=19, color=C['blue'], ha='center',
                arrowprops=dict(arrowstyle='->', color=C['blue'], lw=2))
    save(fig, path)

def fig_timeline(path, w, h):
    fig, ax, H = canvas(w, h, need=44)
    y = H * 0.5; line(ax, [(2, y), (98, y)], C['gray'], 4)
    ev = [(1981, 'US DoD starts\nVHSIC program', C['gray']), (1983, 'VHDL design\nbegins', C['blue']),
          (1984, 'Verilog created\n(Gateway Design)', C['orange']), (1987, 'VHDL becomes\nIEEE 1076', C['blue']),
          (1995, 'Verilog becomes\nIEEE 1364', C['orange']), (2005, 'SystemVerilog\nIEEE 1800', C['orange']),
          (2008, 'VHDL-2008\nbig update', C['blue']), (2019, 'VHDL-2019\nlatest', C['blue'])]
    for i, (yr, lab, col) in enumerate(ev):
        x = 7 + i * 12.3; top = i % 2 == 0
        dot(ax, x, y, 1.1, col)
        line(ax, [(x, y), (x, y + (5 if top else -5))], col, 2.5)
        txt(ax, x, y + (8 if top else -8), str(yr), 21, col, bold=True)
        txt(ax, x, y + (15 if top else -15), lab, 16, C['ink'])
    txt(ax, 3, H - 2.5, '● VHDL', 19, C['blue'], ha='left', bold=True); txt(ax, 17, H - 2.5, '● Verilog family', 19, C['orange'], ha='left', bold=True)
    save(fig, path)

def fig_fpga(path, w, h):
    fig, ax, H = canvas(w, h, need=72)
    n, m = 6, 5; x0, y0, cw, ch = 14, 8, 12, 11
    for i in range(n):
        for j in range(m):
            box(ax, x0 + i * cw, y0 + j * ch, cw * 0.6, ch * 0.55, 'LUT\n+FF', fc=C['lblue'], fs=13, r=0.6, lw=1.8)
    for i in range(n + 1):
        line(ax, [(x0 - cw * 0.2 + i * cw, y0 - 2), (x0 - cw * 0.2 + i * cw, y0 + m * ch)], C['orange'], 1.6)
    for j in range(m + 1):
        line(ax, [(x0 - 3, y0 - ch * 0.22 + j * ch), (x0 + n * cw, y0 - ch * 0.22 + j * ch)], C['orange'], 1.6)
    for i in range(n + 1):
        for j in range(m + 1):
            ax.add_patch(Rectangle((x0 - cw * 0.2 + i * cw - 0.7, y0 - ch * 0.22 + j * ch - 0.7), 1.4, 1.4, fc=C['orange'], ec='none', zorder=3))
    for j in range(m):
        box(ax, 3, y0 + j * ch + 1, 6, ch * 0.4, 'I/O', fc=C['lgreen'], ec=C['green'], fs=13, r=0.5, lw=1.5)
        box(ax, x0 + n * cw + 1, y0 + j * ch + 1, 6, ch * 0.4, 'I/O', fc=C['lgreen'], ec=C['green'], fs=13, r=0.5, lw=1.5)
    txt(ax, 50, H - 3, 'Inside an FPGA: a sea of tiny logic blocks + programmable wiring', 21, bold=True)
    txt(ax, 50, 3, 'blue = logic blocks   ·   orange = routing switches   ·   green = pins', 18, C['mut'])
    save(fig, path)

def fig_lut(path, w, h):
    fig, ax, H = canvas(w, h, need=64)
    rows = [(a, b, c, int((a + b + c) >= 2)) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    table(ax, 8, H - 8, ['a', 'b', 'c', 'stored bit'], rows, [7, 7, 7, 16], 5.6, 20, hl={3, 5, 6, 7}, hlc=C['lgreen'])
    box(ax, 60, H / 2 - 14, 22, 28, '3-input\nLUT\n(8 memory\ncells)', fc=C['lblue'], fs=20, bold=True)
    for k, nm in enumerate(['a', 'b', 'c']):
        yy = H / 2 + 8 - k * 8; line(ax, [(52, yy), (60, yy)], C['ink'], 2.6); txt(ax, 50.5, yy, nm, 20, ha='right')
    arrow(ax, (82, H / 2), (92, H / 2), lw=3); txt(ax, 94, H / 2, 'y', 22, ha='left', bold=True)
    txt(ax, 70, H / 2 - 20, 'this one is programmed as\n"majority of a, b, c"', 18, C['green'])
    txt(ax, 50, 4, 'A look-up table is just a tiny memory holding the truth table.', 20, C['mut'])
    save(fig, path)

FLOW = ['Write\nVHDL', 'Simulate\n(testbench)', 'Synthesize\n(→ gates/LUTs)', 'Place &\nRoute', 'Generate\nbitstream', 'Run on\nthe board']
NOTE = ['describe what\nthe hardware does', 'prove it works\nbefore building', 'tool turns code\ninto a netlist', 'pick physical spots\nand wires on chip', 'the configuration\nfile for the FPGA', 'measure, debug,\nrepeat']
def _flow(path, w, h, k):
    fig, ax, H = canvas(w, h, need=40)
    n = len(FLOW); bw = 14.5; gap = (100 - 2 - n * bw) / (n - 1); yb = H / 2 + 1
    for i, s in enumerate(FLOW):
        x = 1 + i * (bw + gap); on = (k < 0) or (i == k); done = k >= 0 and i < k
        fc = C['blue'] if on else (C['lblue'] if done else '#EEF1F6'); tc = 'white' if on else C['ink']
        box(ax, x, yb - 2, bw, 13, s, fc=fc, ec=C['blue'] if (on or done) else '#C9D1DE', tc=tc, fs=19, bold=on)
        if i < n - 1: arrow(ax, (x + bw + 0.2, yb + 4.5), (x + bw + gap - 0.2, yb + 4.5), lw=2.6, ms=16)
        if on or k < 0: txt(ax, x + bw / 2, yb - 8, NOTE[i], 16, C['mut'])
    txt(ax, 50, H - 3, 'Tools: Vivado (AMD/Xilinx) · Quartus (Intel/Altera) · ModelSim/Questa · GHDL (free)', 19, C['mut'])
    x0, x1 = 1 + bw / 2, 1 + (bw + gap) + bw / 2
    line(ax, [(x0, yb - 13), (x0, yb - 15), (x1, yb - 15), (x1, yb - 13)], C['orange'], 2.2, ls='--')
    txt(ax, x0 - 1, yb - 18, 'loop here until it works — bugs are cheap to fix in simulation', 17, C['orange'], ha='left')
    save(fig, path)
for _k in range(-1, 6):
    globals()[f'fig_flow{_k + 1}'] = (lambda kk: (lambda p, w, h: _flow(p, w, h, kk)))(_k)

def fig_seqpar(path, w, h):
    fig, ax, H = canvas(w, h, need=58)
    box(ax, 2, 6, 44, H - 16, '', fc=C['pale'], ec='#C9D1DE')
    box(ax, 54, 6, 44, H - 16, '', fc=C['pale'], ec='#C9D1DE')
    txt(ax, 24, H - 5, 'Software (C)', 24, C['ink'], bold=True); txt(ax, 76, H - 5, 'Hardware (VHDL)', 24, C['blue'], bold=True)
    code = ['x = a & b;', 'y = !c;', 'z = x | y;']
    for i, s in enumerate(code):
        yy = H - 18 - i * 11
        box(ax, 8, yy - 3.5, 22, 7, s, fc='white', ec=C['gray'], fs=19, ha='left')
        txt(ax, 36, yy, f'step {i+1}', 18, C['mut'])
        if i < 2: arrow(ax, (19, yy - 3.8), (19, yy - 7.2), lw=2.4, ms=16)
    txt(ax, 24, 10, 'one line at a time, in order', 18, C['mut'])
    g1 = gate(ax, 'and', 64, H - 20, 8); g2 = gate(ax, 'not', 65, H - 38, 6); g3 = gate(ax, 'or', 82, H - 29, 8)
    for (px, py), nm in zip(g1['in'], 'ab'): wire(ax, [(58, py), (px, py)]); txt(ax, 57, py, nm, 19, ha='right')
    wire(ax, [(58, H - 38), g2['in'][0]]); txt(ax, 57, H - 38, 'c', 19, ha='right')
    wire(ax, [g1['out'], (78, g1['out'][1]), (78, g3['in'][0][1]), g3['in'][0]]); txt(ax, 76, g1['out'][1] + 2, 'x', 17, C['mut'])
    wire(ax, [g2['out'], (78, g2['out'][1]), (78, g3['in'][1][1]), g3['in'][1]]); txt(ax, 75, g2['out'][1] + 2, 'y', 17, C['mut'])
    wire(ax, [g3['out'], (95, g3['out'][1])]); txt(ax, 96, g3['out'][1], 'z', 19, ha='left')
    txt(ax, 76, 10, 'all three gates exist and work at once, forever', 18, C['blue'])
    save(fig, path)

def fig_entity(path, w, h):
    fig, ax, H = canvas(w, h, need=46)
    chip(ax, 34, H / 2 - 16, 32, 32, 'full_adder', left=['a', 'b', 'cin'], right=['s', 'cout'], fs=24, pin=7)
    txt(ax, 50, H / 2, 'architecture\n(what is inside)', 20, C['mut'])
    txt(ax, 50, 7, 'entity = the outside: a name + ports (pins),\neach with a direction (in/out) and a type', 18, C['mut'])
    save(fig, path)

FA_ROWS = [(a, b, c, (a + b + c) % 2, int(a + b + c >= 2)) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
def _fa_table(path, w, h, hl):
    fig, ax, H = canvas(w, h, need=70)
    table(ax, 14, H - 4, ['a', 'b', 'cin', 'cout', 's'], [(r[0], r[1], r[2], r[4], r[3]) for r in FA_ROWS], [14, 14, 14, 16, 16], 7.2, 24, hl=hl)
    save(fig, path)
def fig_fa_table(p, w, h): _fa_table(p, w, h, set())
def fig_fa_table_hl(p, w, h): _fa_table(p, w, h, {6})

def fig_fa_gates(path, w, h):
    fig, ax, H = canvas(w, h, need=72)
    ya, yb, yc = H - 12, H - 20, H - 34
    for nm, yy in (('a', ya), ('b', yb), ('cin', yc)): txt(ax, 5, yy, nm, 22, ha='right', bold=True)
    x1 = gate(ax, 'xor', 30, (ya + yb) / 2, 10); x2 = gate(ax, 'xor', 58, (ya + yb) / 2 - 6, 10)
    a1 = gate(ax, 'and', 58, H - 48, 10); a2 = gate(ax, 'and', 58, H - 64, 10); o1 = gate(ax, 'or', 80, H - 56, 10)
    wire(ax, [(6, ya), x1['in'][0]]); wire(ax, [(6, yb), x1['in'][1]])
    dot(ax, 14, ya, 0.6); dot(ax, 18, yb, 0.6)
    wire(ax, [(14, ya), (14, a2['in'][0][1]), a2['in'][0]]); wire(ax, [(18, yb), (18, a2['in'][1][1]), a2['in'][1]])
    wire(ax, [x1['out'], (48, x1['out'][1]), (48, x2['in'][0][1]), x2['in'][0]]); dot(ax, 48, x2['in'][0][1], 0.6)
    wire(ax, [(48, x2['in'][0][1]), (48, a1['in'][0][1]), a1['in'][0]])
    wire(ax, [(6, yc), (44, yc), (44, x2['in'][1][1]), x2['in'][1]]); dot(ax, 44, yc, 0.6)
    wire(ax, [(44, yc), (44, a1['in'][1][1]), a1['in'][1]])
    wire(ax, [x2['out'], (90, x2['out'][1])]); txt(ax, 91, x2['out'][1], 's', 24, ha='left', bold=True, c=C['blue'])
    wire(ax, [a1['out'], (75, a1['out'][1]), (75, o1['in'][0][1]), o1['in'][0]])
    wire(ax, [a2['out'], (75, a2['out'][1]), (75, o1['in'][1][1]), o1['in'][1]])
    wire(ax, [o1['out'], (90, o1['out'][1])]); txt(ax, 91, o1['out'][1], 'cout', 22, ha='left', bold=True, c=C['blue'])   # label ends before x = 100
    txt(ax, 35, H - 3, 's = a ⊕ b ⊕ cin', 22, C['blue']); txt(ax, 35, 4, 'cout = a·b + cin·(a ⊕ b)', 22, C['blue'])
    save(fig, path)

def fig_glitch(path, w, h):
    fig, ax, H = canvas(w, h, need=56)
    sig = [('a', [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]), ('b', [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]), ('a xor b', [1, 1, 1, 1, 0, 1, 1, 1, 1, 1])]
    timing(ax, 20, H - 14, sig, cw=7.5, rh=13, hi=7, fs=22, colors={'a xor b': C['red']})
    ax.add_patch(Rectangle((20 + 4 * 7.5 - 0.5, H - 14 - 26 - 2), 8.5, 11, fc='none', ec=C['red'], lw=2.5, ls='--'))
    txt(ax, 20 + 4.5 * 7.5, H - 14 - 26 - 6, 'glitch!', 22, C['red'], bold=True)
    txt(ax, 55, 7, 'b changes a moment after a, so for an instant a = b = 1\nand the XOR output briefly drops to 0', 18, C['mut'])
    save(fig, path)

def _rca(path, w, h, k):
    """4-bit ripple add of 0111 + 0011; carries revealed up to stage k"""
    fig, ax, H = canvas(w, h, need=50)
    A = [1, 1, 1, 0]; B = [1, 1, 0, 0]  # LSB first: A=0111, B=0011
    carry = [0]; S = []
    for i in range(4):
        t = A[i] + B[i] + carry[-1]; S.append(t % 2); carry.append(t // 2)
    for i in range(4):
        x = 76 - i * 22; on = i < k
        box(ax, x, H / 2 - 8, 14, 16, f'FA{i}', fc=C['lorange'] if on else C['lblue'], ec=C['orange'] if on else C['blue'], fs=22, bold=True)
        txt(ax, x + 4, H / 2 + 14, f'a{i}={A[i]}', 19); txt(ax, x + 10, H / 2 + 20, f'b{i}={B[i]}', 19)
        line(ax, [(x + 4, H / 2 + 11.5), (x + 4, H / 2 + 8)], C['ink'], 2.2); line(ax, [(x + 10, H / 2 + 17.5), (x + 10, H / 2 + 8)], C['ink'], 2.2)
        arrow(ax, (x + 7, H / 2 - 8), (x + 7, H / 2 - 13), lw=2.4, ms=16)
        txt(ax, x + 7, H / 2 - 16, f's{i} = {S[i]}' if on else f's{i} = ?', 21, C['orange'] if on else C['mut'], bold=on)
        cx0 = x + 22 if i > 0 else 94
        arrow(ax, (x + 14 + 8 if i > 0 else 95, H / 2), (x + 14, H / 2), lw=2.6, ms=16, color=C['orange'] if i <= k and i > 0 and i - 1 < k else C['ink'])
        cin_txt = f'c{i}={carry[i]}' if (i == 0 or i - 1 < k) else f'c{i}=?'
        txt(ax, x + 18 if i > 0 else 96, H / 2 + 3, cin_txt, 17, C['orange'] if i > 0 and i - 1 < k else C['ink'])
    arrow(ax, (10, H / 2), (2, H / 2), lw=2.6, ms=16, color=C['orange'] if k >= 4 else C['ink'])
    txt(ax, 6, H / 2 + 3, f'c4={carry[4]}' if k >= 4 else 'c4=?', 17, C['orange'] if k >= 4 else C['ink'])
    res = ''.join(str(S[i]) if i < k else '?' for i in range(3, -1, -1))
    txt(ax, 50, 3.5, f'0111 (7)  +  0011 (3)  =  {res}' + ('  (10) ✓' if k >= 4 else ''), 24, C['blue'], bold=True)
    txt(ax, 50, H - 3, 'each stage must wait for the carry from the stage to its right', 18, C['mut'])
    save(fig, path)
for _k in range(5):
    globals()[f'fig_rca{_k}'] = (lambda kk: (lambda p, w, h: _rca(p, w, h, kk)))(_k)

def fig_wheel(path, w, h):
    fig, ax, H = canvas(w, h, need=72)
    cx, cy, R = 28.5, H / 2, min(H / 2 - 6, 23.5)
    for v in range(16):
        ang = math.pi / 2 - v * 2 * math.pi / 16
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        sv = v if v < 8 else v - 16
        col = C['blue'] if sv >= 0 else C['red']
        ax.add_patch(Circle((x, y), 4.0, fc=C['lblue'] if sv >= 0 else C['lred'], ec=col, lw=2, zorder=3))
        txt(ax, x, y + 0.9, f'{v:04b}', 13, C['ink']); txt(ax, x, y - 1.5, str(sv), 17, col, bold=True)
    txt(ax, cx, cy + 3, 'add 1 =', 18, C['mut']); txt(ax, cx, cy - 2, 'step clockwise', 18, C['mut'])
    ang7 = math.pi / 2 - 7.5 * 2 * math.pi / 16
    line(ax, [(cx + (R - 6) * math.cos(ang7), cy + (R - 6) * math.sin(ang7)), (cx + (R + 6) * math.cos(ang7), cy + (R + 6) * math.sin(ang7))], C['orange'], 4)
    X = 57      # text column: everything must end before x = 100 (it was clipped at the right edge)
    txt(ax, X, H - 8, 'Negate:  −x = (NOT x) + 1', 20, C['ink'], ha='left', bold=True)
    txt(ax, X, H - 17, '5 = 0101 → 1010 + 1', 18, ha='left'); txt(ax, X, H - 23, '   = 1011 = −5', 18, ha='left')
    txt(ax, X, H - 32, 'Range of 4 bits:  −8 … +7', 18, ha='left')
    txt(ax, X, H - 42, 'Overflow (orange line):', 18, C['orange'], ha='left', bold=True)
    txt(ax, X, H - 49, '0111 + 0001 = 1000', 18, ha='left'); txt(ax, X, H - 55, '7 + 1 → −8  ✗', 18, C['red'], ha='left')
    txt(ax, X, H - 64, 'carry into MSB ≠ carry out\n→ overflow flag', 17, C['mut'], ha='left')
    save(fig, path)

def fig_addsub(path, w, h):
    fig, ax, H = canvas(w, h, need=70)
    box(ax, 16, 14, 62, 13, '4-bit adder', fc=C['lblue'], fs=24, bold=True)
    ysub = 52
    wire(ax, [(4, ysub), (90, ysub)], C['orange'], 3.2); txt(ax, 4, ysub + 3, 'SUB', 22, C['orange'], bold=True, ha='left')
    for i in range(4):
        x = 22 + i * 15
        g = gate(ax, 'xor', x, 38, 9)
        bx = g['in'][0][0] - 4
        wire(ax, [(bx, g['in'][0][1]), g['in'][0]]); txt(ax, bx - 0.5, g['in'][0][1], f'B{3-i}', 18, ha='right', bold=True)
        sx = g['in'][1][0] - 2
        wire(ax, [(sx, ysub), (sx, g['in'][1][1]), g['in'][1]], C['orange'], 2.4); dot(ax, sx, ysub, 0.6, C['orange'])
        ox, oy = g['out']
        wire(ax, [(ox, oy), (ox + 1.5, oy), (ox + 1.5, 27)])
        txt(ax, x + 4.5, 66 - 2, '', 10)
        arrow(ax, (x + 6, 14), (x + 6, 7), lw=2.4, ms=15); txt(ax, x + 6, 4.5, f'S{3-i}', 18, bold=True)
    wire(ax, [(90, ysub), (90, 20.5), (78, 20.5)], C['orange'], 3.2); txt(ax, 91, 24, 'cin', 20, C['orange'], ha='left')
    arrow(ax, (4, 20.5), (16, 20.5), lw=2.8); txt(ax, 4, 23.5, 'A', 22, bold=True, ha='left')
    txt(ax, 50, H - 4, 'SUB = 0:  S = A + B          SUB = 1:  S = A + (NOT B) + 1 = A − B', 20, C['blue'], bold=True)
    txt(ax, 50, H - 10, 'XOR with 1 flips a bit; XOR with 0 passes it unchanged', 18, C['mut'])
    save(fig, path)

def fig_stdlogic(path, w, h):
    fig, ax, H = canvas(w, h, need=62)
    rows = [("'U'", 'uninitialized', 'never assigned — usually a missing reset'), ("'X'", 'forcing unknown', 'two drivers fighting (0 vs 1)'),
            ("'0'", 'forcing 0', 'logic low'), ("'1'", 'forcing 1', 'logic high'), ("'Z'", 'high impedance', 'driver switched off (tri-state bus)'),
            ("'W'", 'weak unknown', 'rare'), ("'L'", 'weak 0', 'pull-down resistor'), ("'H'", 'weak 1', 'pull-up resistor'), ("'-'", "don't care", 'lets synthesis optimize')]
    table(ax, 4, H - 2, ['value', 'meaning', 'when you see it'], rows, [12, 26, 54], 5.8, 21, hl={0, 1, 4})
    save(fig, path)

def fig_mux(path, w, h):
    fig, ax, H = canvas(w, h, need=66)
    ax.add_patch(Polygon([(40, H / 2 - 26), (64, H / 2 - 14), (64, H / 2 + 14), (40, H / 2 + 26)], fc=C['lblue'], ec=C['blue'], lw=3))
    txt(ax, 55, H / 2, '4:1\nMUX', 24, C['blue'], bold=True)
    for i, nm in enumerate(['a', 'b', 'c', 'd']):
        yy = H / 2 + 18 - i * 12; wire(ax, [(26, yy), (40, yy)]); txt(ax, 24, yy, nm, 24, ha='right', bold=True); txt(ax, 33, yy + 2.6, f'"{i:02b}"', 16, C['mut'])
    wire(ax, [(64, H / 2), (78, H / 2)]); txt(ax, 80, H / 2, 'y', 26, ha='left', bold=True)
    wire(ax, [(52, H / 2 - 20), (52, H / 2 - 30)], lw=3); txt(ax, 52, H / 2 - 33, 'sel (2 bits)', 20)
    save(fig, path)

def _seg(path, w, h, digit):
    fig, ax, H = canvas(w, h, need=48)
    on = {'0': 'abcdef', '1': 'bc', '2': 'abdeg', '3': 'abcdg', '4': 'bcfg', '5': 'acdfg', '6': 'acdefg', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg'}[digit]
    cx, cy, L, t = 28, H / 2, 16, 3.2
    segs = {'a': (cx, cy + L, 'h'), 'g': (cx, cy, 'h'), 'd': (cx, cy - L, 'h'), 'f': (cx - L / 2, cy + L / 2, 'v'), 'b': (cx + L / 2, cy + L / 2, 'v'),
            'e': (cx - L / 2, cy - L / 2, 'v'), 'c': (cx + L / 2, cy - L / 2, 'v')}
    for nm, (x, y, o) in segs.items():
        lit = nm in on; col = C['red'] if lit else '#E6E9EF'
        if o == 'h': pts = [(x - L / 2 + t / 2, y), (x - L / 2 + t, y + t / 2), (x + L / 2 - t, y + t / 2), (x + L / 2 - t / 2, y), (x + L / 2 - t, y - t / 2), (x - L / 2 + t, y - t / 2)]
        else: pts = [(x, y - L / 2 + t / 2), (x + t / 2, y - L / 2 + t), (x + t / 2, y + L / 2 - t), (x, y + L / 2 - t / 2), (x - t / 2, y + L / 2 - t), (x - t / 2, y - L / 2 + t)]
        ax.add_patch(Polygon(pts, fc=col, ec='none', zorder=3))
        ox = {'a': (0, 3.5), 'g': (0, 3.5), 'd': (0, -3.5), 'f': (-3.5, 0), 'b': (3.5, 0), 'e': (-3.5, 0), 'c': (3.5, 0)}[nm]
        txt(ax, x + ox[0], y + ox[1], nm, 17, C['ink'] if lit else C['gray'], bold=lit)
    txt(ax, 72, H / 2 + 15, f'digit {digit}', 30, C['ink'], bold=True)
    for k, s in enumerate('abcdefg'):
        xx = 54 + k * 6
        txt(ax, xx, H / 2 + 3, s, 22, C['mut'])
        txt(ax, xx, H / 2 - 5, '1' if s in on else '0', 26, C['red'] if s in on else C['gray'], bold=True)
    txt(ax, 72, H / 2 - 16, '(1 = segment on)', 18, C['mut'])
    save(fig, path)
def fig_seg2(p, w, h): _seg(p, w, h, '2')

def fig_dff(path, w, h):
    fig, ax, H = canvas(w, h, need=58)
    sig = [('clk', 'clk'), ('d', [0, 1, 1, 0, 0, 1, 0, 0]), ('q', [0, 0, 1, 1, 0, 0, 1, 0])]
    timing(ax, 18, H - 15, sig, cw=10, rh=15, hi=8, fs=24, colors={'q': C['orange']})
    for k in range(8):
        line(ax, [(18 + k * 10, 8), (18 + k * 10, H - 5)], C['gray'], 1.2, ls=':')
    txt(ax, 58, 4, 'q copies d only at each rising clock edge, then holds it', 19, C['mut'])
    save(fig, path)

def fig_swap(path, w, h):
    fig, ax, H = canvas(w, h, need=60)
    box(ax, 22, H / 2 + 6, 16, 16, 'reg a', fs=22, bold=True); box(ax, 62, H / 2 + 6, 16, 16, 'reg b', fs=22, bold=True)
    arrow(ax, (38, H / 2 + 14), (62, H / 2 + 14), color=C['blue'], rad=-0.3)
    arrow(ax, (62, H / 2 + 10), (38, H / 2 + 10), color=C['orange'], rad=-0.3)
    txt(ax, 50, H / 2 + 27, 'b <= a', 21, C['blue']); txt(ax, 50, H / 2 - 2, 'a <= b', 21, C['orange'])
    txt(ax, 50, H / 2 - 14, 'Both registers sample at the same clock edge,\nso the values truly swap — no temp variable needed.', 19, C['mut'])
    save(fig, path)

def fig_latch(path, w, h):
    fig, ax, H = canvas(w, h, need=52)
    box(ax, 3, 8, 44, H - 16, '', fc=C['lgreen'], ec=C['green']); box(ax, 53, 8, 44, H - 16, '', fc=C['lred'], ec=C['red'])
    txt(ax, 25, H - 13, 'What you meant', 22, C['green'], bold=True); txt(ax, 75, H - 13, 'What you got', 22, C['red'], bold=True)
    ax.add_patch(Polygon([(18, H / 2 - 10), (28, H / 2 - 5), (28, H / 2 + 5), (18, H / 2 + 10)], fc='white', ec=C['ink'], lw=2.5))
    txt(ax, 23, H / 2, 'MUX', 15)
    wire(ax, [(10, H / 2 + 5), (18, H / 2 + 5)]); wire(ax, [(10, H / 2 - 5), (18, H / 2 - 5)]); wire(ax, [(28, H / 2), (38, H / 2)])
    txt(ax, 9, H / 2 + 5, 'a', 18, ha='right'); txt(ax, 9, H / 2 - 5, '0', 18, ha='right'); txt(ax, 39, H / 2, 'y', 18, ha='left')
    txt(ax, 25, 15, 'pure combinational:\noutput always defined', 17, C['ink'])
    box(ax, 66, H / 2 - 8, 18, 16, 'LATCH\nD    Q\nEN', fc='white', ec=C['red'], fs=16)
    wire(ax, [(58, H / 2 + 3), (66, H / 2 + 3)]); wire(ax, [(84, H / 2), (92, H / 2)]); wire(ax, [(58, H / 2 - 5), (66, H / 2 - 5)])
    txt(ax, 57, H / 2 + 3, 'a', 18, ha='right'); txt(ax, 57, H / 2 - 5, 'en', 18, ha='right'); txt(ax, 93, H / 2, 'y', 18, ha='left')
    txt(ax, 75, 15, 'remembers old value when\nen = 0 → timing bugs', 17, C['ink'])
    save(fig, path)

def fig_timingpath(path, w, h):
    fig, ax, H = canvas(w, h, need=50)
    yb = H - 22
    box(ax, 4, yb - 6, 12, 16, 'FF', fs=22, bold=True)
    ax.add_patch(matplotlib.patches.Ellipse((50, yb + 2), 40, 18, fc=C['lyellow'], ec=C['yellow'], lw=2.5))
    txt(ax, 50, yb + 2, 'combinational logic', 21)
    box(ax, 84, yb - 6, 12, 16, 'FF', fs=22, bold=True)
    arrow(ax, (16, yb + 2), (30, yb + 2)); arrow(ax, (70, yb + 2), (84, yb + 2))
    y2 = 14; segs = [('t clk→q\n0.5 ns', 0.5, C['blue']), ('t logic\n3.0 ns', 3.0, C['yellow']), ('t setup\n0.3 ns', 0.3, C['red'])]
    x = 10; sc = 80 / 3.8
    for lab, v, col in segs:
        ax.add_patch(Rectangle((x, y2), v * sc, 6, fc=col, ec='white', lw=2)); txt(ax, x + v * sc / 2, y2 - 5, lab, 16)
        x += v * sc
    txt(ax, 50, y2 + 11, 'clock period ≥ 3.8 ns   →   f max ≈ 263 MHz', 22, C['ink'], bold=True)
    save(fig, path)

def fig_clkdiv(path, w, h):
    fig, ax, H = canvas(w, h, need=70)
    fast = 'clk'
    timing(ax, 22, H - 14, [('100 MHz', 'clk')], cw=3.2, rh=14, hi=6, fs=20, ncyc=24)
    slow = []
    for k in range(24): slow.append((k // 4) % 2)
    timing(ax, 22, H - 30, [('÷ 8', slow)], cw=3.2, rh=14, hi=6, fs=20, colors={'÷ 8': C['orange']})
    txt(ax, 50, H - 46, 'toggle the output every N = 4 input cycles\nf out = f in / (2N)', 21, C['ink'])
    txt(ax, 50, H - 60, '100 MHz → 1 Hz:  N = 50,000,000\n→ needs a 26-bit counter (2²⁶ ≈ 67 million)', 21, C['blue'], bold=True)
    save(fig, path)

def fig_muxdisp(path, w, h):
    fig, ax, H = canvas(w, h, need=74)
    for i in range(4):
        x = 10 + i * 16; lit = (i == 1)
        box(ax, x, H - 30, 12, 20, '', fc='#2A2F3A', ec='#2A2F3A', r=1)
        txt(ax, x + 6, H - 20, '8', 40, C['red'] if lit else '#4A505C', bold=True, family='Consolas')
        txt(ax, x + 6, H - 34, f'AN{3-i}', 16, C['orange'] if lit else C['mut'])
    txt(ax, 82, H - 18, 'shared segment\nlines a–g', 18, C['mut'])
    sig = [('AN3', [1, 0, 0, 0, 1, 0, 0, 0]), ('AN2', [0, 1, 0, 0, 0, 1, 0, 0]), ('AN1', [0, 0, 1, 0, 0, 0, 1, 0]), ('AN0', [0, 0, 0, 1, 0, 0, 0, 1])]
    timing(ax, 18, H - 48, sig, cw=9, rh=6.2, hi=3.6, fs=16, colors={'AN2': C['orange']})
    txt(ax, 56, 3, 'each digit is lit 1/4 of the time; at ~1 kHz your eye sees all four steadily', 17, C['mut'])
    save(fig, path)

def _fsm101(path, w, h, hl=None):
    fig, ax, H = canvas(w, h, need=46)
    y = H / 2 + 2; hlc = lambda k: C['lorange'] if hl == k else None
    st = {'S0': (12, y, 'IDLE\nout=0', hlc('S0')), 'S1': (38, y, 'got "1"\nout=0', hlc('S1')),
          'S2': (64, y, 'got "10"\nout=0', hlc('S2')), 'S3': (88, y, 'FOUND\nout=1', hlc('S3') or C['lgreen'])}
    ed = [('S0', 'S1', '1', 0.0), ('S1', 'S2', '0', 0.0), ('S2', 'S3', '1', 0.0), ('S0', 'S0', '0', 90), ('S1', 'S1', '1', 90),
          ('S2', 'S0', '0', 0.45), ('S3', 'S2', '0', -0.4), ('S3', 'S1', '1', 0.55)]
    fsm(ax, st, ed, r=7, fs=17, efs=19)
    txt(ax, 50, 3, 'Moore machine detecting the bit pattern 1-0-1 (overlaps allowed)', 19, C['mut'])
    save(fig, path)
def fig_fsm101(p, w, h): _fsm101(p, w, h)
def fig_fsm101_s3(p, w, h): _fsm101(p, w, h, 'S3')

def fig_mealy(path, w, h):
    fig, ax, H = canvas(w, h, need=46)
    y = H / 2 + 2
    st = {'S0': (18, y, 'IDLE'), 'S1': (50, y, 'got "1"'), 'S2': (82, y, 'got "10"')}
    ed = [('S0', 'S1', '1 / 0', 0.0), ('S1', 'S2', '0 / 0', 0.0), ('S0', 'S0', '0 / 0', 90), ('S1', 'S1', '1 / 0', 90),
          ('S2', 'S1', '1 / 1  ← output here', 0.45, C['orange']), ('S2', 'S0', '0 / 0', -0.5)]
    fsm(ax, st, ed, r=7.5, fs=19, efs=18)
    txt(ax, 50, 3, 'Mealy version: labels are input / output — one fewer state, answer a cycle sooner', 18, C['mut'])
    save(fig, path)

def fig_traffic(path, w, h):
    fig, ax, H = canvas(w, h, need=70)
    st = {'A': (20, H - 16, 'N-S green\nE-W red', C['lgreen']), 'B': (80, H - 16, 'N-S yellow\nE-W red', C['lyellow']),
          'C': (80, 16, 'N-S red\nE-W green', C['lgreen']), 'D': (20, 16, 'N-S red\nE-W yellow', C['lyellow'])}
    ed = [('A', 'B', 'timer = 30 s', 0.0), ('B', 'C', 'timer = 4 s', 0.0), ('C', 'D', 'timer = 30 s\n(or no cars)', 0.0), ('D', 'A', 'timer = 4 s', 0.0)]
    fsm(ax, st, ed, r=11, fs=19, efs=20)
    txt(ax, 50, H / 2, 'a counter in each state\ncounts clock ticks;\nwhen it hits the limit,\nmove on and reset it', 20, C['mut'])
    save(fig, path)

def fig_tb(path, w, h):
    fig, ax, H = canvas(w, h, need=120, exact=True)
    box(ax, 3, 4, 94, H - 18, '', fc=C['pale'], ec=C['gray'], ls='--')
    txt(ax, 50, H - 7, 'testbench entity\n(no ports — a closed world)', 24, C['mut'])
    box(ax, 14, H - 44, 72, 20, 'stimulus\nloop over all inputs, wait 10 ns', fc=C['lyellow'], ec=C['yellow'], fs=24)
    box(ax, 14, H - 78, 72, 20, 'DUT\n(design under test)', fc=C['lblue'], fs=26, bold=True)
    box(ax, 14, H - 112, 72, 20, 'checker\nassert s = expected, else report', fc=C['lgreen'], ec=C['green'], fs=24)
    arrow(ax, (50, H - 44), (50, H - 58), lw=3.5); arrow(ax, (50, H - 78), (50, H - 92), lw=3.5)
    save(fig, path)

# ======================================================================= lesson
LESSON = {
 'code': 'EGCP 281', 'title': 'Designing with VHDL', 'tag': 'Year 2 · Digital design',
 'folder': 'EGCP-281 Digital Logic Design (VHDL)',
 'slides': [
 {'t': 'title', 'h': 'Designing with VHDL', 'sub': 'Describing hardware with code — and why the real world still runs on it', 'img': 'a:fpga_board',
  'say': "Welcome to E G C P two eighty one, Designing with V H D L. In this lecture you'll learn how engineers describe digital hardware using code, how that code becomes a real circuit on a chip, and who actually does this for a living. We'll go from the very first idea, all the way to adders, state machines, timing, and test benches. That little board on the screen is an F P G A board, and by the end of this lesson you'll understand exactly what's inside that chip and how to program it."},

 {'t': 'v', 'h': 'Why describe hardware with code?', 'img': 'fig:scale',
  'pts': ['1971: ~2,300 transistors — drawn by hand', 'Today: **tens of billions** per chip', 'Nobody can draw that. We **describe behavior** and let tools build the gates'],
  'say': ["Let's start with the why. In nineteen seventy one, Intel's first microprocessor, the four zero zero four, had about two thousand three hundred transistors. Engineers literally drew the circuit by hand on large sheets.",
          "Today, a laptop processor like Apple's M one has sixteen billion transistors. Look at the chart. That's a log scale, so every grid line is ten times more than the one below it.",
          "No human team can draw sixteen billion transistors. So instead, engineers write a precise description of what the hardware should do, in a hardware description language, and software tools turn that description into gates. That's what this course teaches. V H D L is one of the two big hardware description languages, and Verilog is the other."]},

 {'t': 'v', 'h': 'Where did VHDL come from?', 'img': 'fig:timeline',
  'say': ["V H D L stands for V H S I C Hardware Description Language, and V H S I C stands for Very High Speed Integrated Circuit. It was a U S Department of Defense program in the early nineteen eighties. The military was buying chips from many suppliers, and the documentation was written in plain English, which was ambiguous. Worse, when a part became obsolete, nobody could rebuild it exactly.",
          "So the D o D funded a language that could describe a chip so precisely that a computer could simulate it. The syntax was borrowed from the Ada programming language, which is why V H D L is wordy and strict. It became I E E E standard ten seventy six in nineteen eighty seven. Around the same time, a company called Gateway Design Automation created Verilog, which has a shorter, C like syntax. Both languages are still alive, both are I E E E standards, and most professional engineers can read both."]},

 {'t': 'v', 'h': 'Who uses VHDL today — and why?', 'img': ['a:antenna_5g', 'a:antenna_5g', 'a:perseverance', 'a:fpga_router', 'a:wafer_pentium|0.2,0,1,1'],
  'pts': ['**Telecom:** 4G/5G radios and network gear', '**Aerospace & defense:** satellites, rovers, radar', '**Products:** routers, cameras, medical imaging, factory robots', '**Chip companies:** prototype and verify before manufacturing'],
  'say': ["So who writes V H D L for a living? Mostly people who design F P G A based products and custom chips. Let's look at four real examples.",
          "Telecom. Cell towers like these process radio signals in real time, billions of samples per second. Software on a normal processor is too slow, so that processing is done in custom hardware, very often on F P G As, designed in V H D L or Verilog.",
          "Aerospace and defense, which is V H D L's home turf, especially in Europe. Spacecraft need hardware that's reliable and well documented. NASA's Perseverance rover used an F P G A based vision computer to recognize the terrain and steer its own landing on Mars. And the European Space Agency's LEON family of processors, which fly in many satellites, was written in V H D L.",
          "Everyday products. This is the circuit board inside a home internet router. That square chip is a Xilinx Spartan F P G A. Companies use F P G As when they need custom, very fast logic but can't afford to manufacture their own chip.",
          "And chip companies. Before spending millions of dollars to manufacture a chip on a silicon wafer like this one, designers write the whole thing in a hardware description language, simulate it, and often prototype it on F P G As first. A mistake found in simulation costs minutes. A mistake found after manufacturing can cost months."]},

 {'t': 'v', 'h': 'What is an FPGA?', 'img': ['fig:fpga', 'fig:lut', 'a:fpga_chip'],
  'pts': ['Field-Programmable Gate Array', 'Thousands to millions of small **logic blocks**', 'Each block: a **look-up table** + a flip-flop', 'Programmable wiring connects them'],
  'say': ["Since V H D L is so often used with F P G As, let's open one up. F P G A stands for field programmable gate array. Field programmable means you can reconfigure it after it leaves the factory, right on your desk.",
          "Inside is a grid of small logic blocks, shown in blue. Between them is a mesh of programmable wiring, the orange lines, with switches where wires cross. Around the edge are the input and output pins, in green.",
          "Here's the clever part. Each logic block contains a look-up table, which is just a tiny memory that holds a truth table. This one has three inputs, so it has eight memory cells, one for every input combination. Store the right eight bits and it becomes any three input logic function you want. Here it's programmed as a majority function. Next to each look-up table is a flip-flop, so the block can also remember a bit.",
          "So when you program an F P G A, you're loading a configuration file that fills in all of those truth tables and closes all the right wiring switches. In about a second, this chip becomes your circuit. Change your code, reload, and it becomes a different circuit. That's why F P G As are perfect for learning, prototyping, and products that need updates."]},

 {'t': 'v', 'h': 'From code to chip: the design flow', 'img': ['fig:flow0', 'fig:flow1', 'fig:flow2', 'fig:flow3', 'fig:flow4', 'fig:flow5', 'fig:flow6'],
  'say': ["Here's the workflow you'll repeat for every design, whether you're a student or working at a chip company.",
          "Step one, write the V H D L. You describe what the hardware should do.",
          "Step two, simulate. You write a test bench that feeds inputs to your design and checks the outputs, and a simulator shows you waveforms. This is where you catch most bugs, because it's fast and cheap.",
          "Step three, synthesis. The tool reads your code and turns it into a netlist, which is a list of gates or look-up tables and flip-flops, plus how they connect.",
          "Step four, place and route. The tool decides which physical logic blocks on the chip to use and which wires connect them, while trying to meet your timing goals.",
          "Step five, generate the bitstream, the configuration file for the F P G A.",
          "And step six, load it onto the board and test it in the real world. The tools you'd use are Vivado from Xilinx, which is now part of A M D, Quartus from Intel's Altera, ModelSim or Questa for simulation, and GHDL, which is a free, open source V H D L simulator you can install today."]},

 {'t': 'v', 'h': 'The big mindset shift: everything runs at once', 'img': 'fig:seqpar',
  'say': ["Now the single most important idea in this course. On the left is ordinary C code. The computer runs line one, then line two, then line three. Order matters, and each line happens once.",
          "On the right is the same logic as hardware. In V H D L, each of those statements becomes a physical gate. The AND gate, the NOT gate, and the OR gate all exist at the same time, and they're all working continuously, forever. If input a changes, the output z changes a few nanoseconds later, automatically. There's no program counter stepping through lines.",
          "So here's the rule I want you to carry for the rest of your career. Before you write a line of hardware description code, picture the circuit it will become. If you can't picture the gates or flip-flops, you don't really understand that line yet. Code is just a way to draw a schematic."]},

 {'t': 'ex', 'h': 'Anatomy of a design: entity + architecture', 'img': 'fig:entity', 'split': 0.55,
  'code': "library ieee;\nuse ieee.std_logic_1164.all;\n\nentity full_adder is\n  port ( a, b, cin : in  std_logic;\n         s, cout   : out std_logic );\nend full_adder;\n\narchitecture dataflow of full_adder is\nbegin\n  s    <= a xor b xor cin;\n  cout <= (a and b) or (cin and (a xor b));\nend dataflow;",
  'cl': [2, 7, 13],
  'say': ["Every V H D L design has the same skeleton. First, we include the I E E E library, which gives us the standard logic type we'll use for wires.",
          "Next is the entity. Think of it as the outside of the chip: its name, and its ports, which are the pins. Each port has a direction, in or out, and a type. Our full adder has three inputs, a, b and carry in, and two outputs, sum and carry out. Look at the diagram on the right: the entity is exactly that black box with five pins.",
          "Then the architecture describes what's inside the box. Here we use two concurrent assignment statements, one for the sum and one for the carry. The arrow made of a less than sign and an equals sign means: this signal is driven by this logic. Remember, both lines are hardware that exists at the same time. The order you write them in doesn't matter at all."]},

 {'t': 'v', 'h': 'Designing a full adder, step by step', 'img': ['fig:fa_table', 'fig:fa_table', 'fig:fa_gates', 'fig:fa_table_hl'],
  'pts': ['Add three bits: a + b + carry-in', '**Sum** is 1 when an odd number of inputs are 1 → XOR', '**Carry** is 1 when two or more inputs are 1', 'Check: 1 + 1 + 0 = binary 10 = 2 ✓'],
  'say': ["But where did those equations come from? Let's derive them, the way you would on an exam. A full adder adds three single bits: a, b, and a carry coming in from the previous column. The result is two bits, a carry out and a sum.",
          "Here's the full truth table, all eight combinations. Look at the sum column. It's one whenever an odd number of the inputs are one. That's exactly what X O R does, so the sum is a X O R b X O R carry in.",
          "Now the carry column. It's one when at least two inputs are one. You can write that as: a AND b, OR carry in AND, a X O R b. Here's that circuit drawn as gates. Two X O R gates make the sum. Two AND gates and an OR gate make the carry. Notice the first X O R is shared by both outputs. Real designers love sharing logic, because it saves gates.",
          "Let's check one row. a equals one, b equals one, carry in equals zero. The sum: one X O R one is zero, X O R zero is still zero. The carry: a AND b is one, so carry out is one. Reading carry then sum gives one zero, which is binary for two. And one plus one plus zero is two. The table, the equations, and the circuit all agree."]},

 {'t': 'v', 'h': 'Real gates have delay — and delay causes glitches', 'img': 'fig:glitch',
  'pts': ['Every gate takes time: **propagation delay**', 'Inputs that change at slightly different times → brief wrong output', 'VHDL can model it:  s <= a xor b after 2 ns;'],
  'say': ["Here's something software never makes you think about. Every real gate takes time to respond, usually a few picoseconds to nanoseconds. That's called propagation delay.",
          "Now look at this timing diagram. Input a rises, and b is supposed to fall at the same moment, but b's path is a little slower. For a brief instant, both a and b are one, so a X O R b drops to zero, then pops back up. That spike is called a glitch, or a hazard. The final answer is right, but for a moment the output lied.",
          "V H D L lets you model this with the keyword after, like s gets a X O R b after two nanoseconds. In this course's first lab, students add delays like that to a full adder and watch glitches appear in the simulator. Later we'll see the professional fix: synchronous design, where we only look at outputs on a clock edge, after everything has settled."]},

 {'t': 'v', 'h': 'Structural design: chaining four full adders', 'img': ['fig:rca0', 'fig:rca1', 'fig:rca2', 'fig:rca3', 'fig:rca4'],
  'say': ["One full adder adds one column. To add whole numbers, we copy it. Here are four full adders in a row, making a four bit ripple carry adder. Each carry out feeds the next adder's carry in, exactly like carrying a one in grade school addition. Let's add seven plus three: zero one one one, plus zero zero one one.",
          "Column zero: one plus one plus a carry in of zero gives sum zero, carry one.",
          "Column one: one plus one plus that carry of one gives sum one, carry one.",
          "Column two: one plus zero plus one gives sum zero, carry one.",
          "Column three: zero plus zero plus one gives sum one, carry zero. Reading the sums from left to right: one zero one zero, which is ten. Seven plus three is ten. Notice the catch, though. Each stage had to wait for the carry from its neighbor. The carry ripples through, so a thirty two bit ripple adder waits through thirty two stages. That's why real processors use faster carry look ahead adders, which compute all the carries in parallel."]},

 {'t': 'ex', 'h': 'Port maps: wiring components like a schematic',
  'code': "architecture structural of adder4 is\n  signal c : std_logic_vector(4 downto 0);\nbegin\n  c(0) <= cin;\n  stages: for i in 0 to 3 generate\n    fa: entity work.full_adder\n      port map ( a => a(i), b => b(i), cin => c(i),\n                 s => s(i), cout => c(i+1) );\n  end generate;\n  cout <= c(4);\nend structural;",
  'pts': ['Internal **signals** are the wires between components', '**port map** connects each pin to a wire', '**for … generate** stamps out copies — 4 or 64 adders, same code'],
  'say': "Here's how you build that in V H D L. This is called structural design. First, declare internal signals, which are wires. Here, c is a five bit bus of carry wires. Then instantiate the full adder four times. The port map connects each pin of the component to a wire: a goes to a of i, carry in goes to c of i, carry out goes to c of i plus one. And instead of typing it four times, a for generate loop stamps out the copies. Change the three to a sixty three and you have a sixty four bit adder. This is exactly how big designs are built: small, tested pieces, wired together like a schematic. In this course's second lab, students build this adder and then extend it."},

 {'t': 'v', 'h': "Negative numbers: two's complement", 'img': ['fig:wheel', 'fig:addsub'],
  'pts': ['−x = (NOT x) + 1', '4 bits hold −8 … +7', 'Subtract = add the complement → one adder does both', 'Overflow: carry into MSB ≠ carry out'],
  'say': ["How does hardware handle negative numbers? Almost every computer uses two's complement. Picture the sixteen four bit patterns arranged on a wheel. Adding one means stepping clockwise. The top half of the patterns represents zero through seven, and the patterns with a leading one represent minus eight through minus one. To negate a number, flip every bit and add one. Five is zero one zero one. Flip it to get one zero one zero, add one, and you get one zero one one, which is minus five. The beautiful part is that the same adder circuit works for negative numbers with no changes. But watch the orange line. Seven plus one wraps around to minus eight. That's overflow: the true answer didn't fit in four bits. The hardware detects it when the carry into the top bit differs from the carry out of it.",
          "And here's the payoff. Since A minus B equals A plus NOT B plus one, we can build a subtractor from our adder with almost no extra hardware. Put an X O R gate on each B input, controlled by a single SUB line. When SUB is zero, X O R passes B through unchanged and the circuit adds. When SUB is one, X O R flips every bit of B, and SUB also feeds the carry in, supplying the plus one. One control wire turns an adder into a subtractor. That's the heart of every A L U you'll ever meet."]},

 {'t': 'v', 'h': 'std_logic: a wire has nine possible values', 'img': 'fig:stdlogic',
  'say': ["In V H D L, wires usually have the type standard logic, and it has nine possible values, not two. That sounds strange, but it's because real wires do more than zero and one. The important ones are highlighted. Capital U means uninitialized. If you see U in your simulation, something never got a value, usually because you forgot a reset. Capital X means unknown, and it usually means two different circuits are driving the same wire, one pushing a zero and the other a one. That's a real short circuit in hardware, so treat X as an alarm bell. Capital Z means high impedance: the driver has disconnected itself. That's how many devices can share one bus, taking turns, with everyone else in Z. The weak values model pull up and pull down resistors, and the dash means don't care, which gives the synthesis tool freedom to optimize. Rule of thumb: a clean simulation shows only zeros and ones where it matters."]},

 {'t': 'ex', 'h': 'Three ways to write combinational logic', 'img': 'fig:mux', 'split': 0.6,
  'code': "-- 1. simple concurrent assignment\ny1 <= (a and b) or c;\n\n-- 2. conditional: when / else  (priority)\ny2 <= a when sel = \"00\" else\n      b when sel = \"01\" else\n      c when sel = \"10\" else d;\n\n-- 3. selected: with / select  (a true mux)\nwith sel select\n  y3 <= a when \"00\",\n        b when \"01\",\n        c when \"10\",\n        d when others;",
  'cl': [2, 7, 14],
  'say': ["For combinational logic, logic with no memory, V H D L gives you three styles outside of processes. The first is the plain concurrent assignment you've already seen: a Boolean equation.",
          "The second is the conditional assignment, using when and else. It checks conditions in order, so it naturally builds a priority structure: the first true condition wins.",
          "The third is the selected assignment, with select. Every choice has equal priority, so it maps directly onto a multiplexer, like the four to one mux on the right. The two select bits choose which of the four inputs reaches the output. Notice the when others line at the end. Standard logic has nine values, so two select bits have far more than four combinations. When others covers all the rest, and it keeps the synthesis tool from inventing memory. You'll see why that matters in a minute."]},

 {'t': 'v', 'h': 'Example: driving a seven-segment display', 'img': ['a:sevenseg', 'fig:seg2', 'fig:seg2'],
  'pts': ['Seven LEDs, named a through g', 'Decoder: 4-bit number in → 7 segment bits out', 'Perfect job for **with … select**'],
  'say': ["Here's a real, everyday example: the seven segment display, used in microwaves, alarm clocks, gas pumps and lab equipment.",
          "Each digit is just seven L E Ds, named a through g, going around the outside and then the middle bar. To show a two, we turn on segments a, b, g, e and d. So the pattern for a, b, c, d, e, f, g is one one zero one one zero one.",
          "A seven segment decoder is a circuit that takes a four bit number and outputs those seven bits. It's a perfect job for with select: one line per digit, zero through nine, plus when others to blank the display. In this course's third lab, students build exactly this decoder, along with a small arithmetic logic unit, and see their numbers light up on the board. One practical gotcha: many boards use active low segments, meaning a zero turns the L E D on. Always check the board's manual."]},

 {'t': 'ex', 'h': 'Processes: how VHDL describes memory', 'img': 'fig:dff', 'split': 0.52,
  'code': "process (clk)\nbegin\n  if rising_edge(clk) then\n    if reset = '1' then\n      q <= '0';\n    else\n      q <= d;\n    end if;\n  end if;\nend process;",
  'say': ["So far, everything has been combinational. Now let's add memory. In V H D L, memory is described inside a process. A process is a block whose statements read top to bottom, like software, but it still becomes hardware. The list in parentheses is the sensitivity list: the process wakes up whenever one of those signals changes.",
          "The key phrase is if rising edge of clock. Any signal you assign inside that if becomes a flip-flop, a one bit memory that only updates on the clock's rising edge. Look at the timing diagram. The input d can wiggle whenever it likes, but q only copies d at the instant the clock goes from zero to one, then holds that value until the next edge. That's the foundation of every register, counter and state machine. The reset branch gives the flip-flop a known starting value, which is how you avoid those U values in simulation. In this course's fourth lab, students build flip-flops, then registers, then a small accumulator machine out of them."]},

 {'t': 'ex', 'h': 'Signals vs. variables', 'img': 'fig:swap', 'split': 0.5,
  'code': "-- signals: update when the process suspends\nprocess (clk) begin\n  if rising_edge(clk) then\n    a <= b;      -- uses OLD b\n    b <= a;      -- uses OLD a  → swap!\n  end if;\nend process;\n\n-- variables: update immediately\nprocess (x)\n  variable t : integer;\nbegin\n  t := x * 2;    -- t changes right now\n  y <= t + 1;\nend process;",
  'say': "Here's a subtle rule that trips up every beginner. Inside a process, a signal assignment doesn't take effect immediately. All signal updates are scheduled, and they happen together when the process finishes. So look at the top example: a gets b, and b gets a. In software, that would make both equal. In V H D L, both assignments use the old values, so the two registers genuinely swap on every clock edge, just like the picture: two flip-flops feeding each other. That's exactly how real hardware behaves, because both flip-flops sample at the same instant. Variables are different. They use the colon equals symbol, they live only inside the process, and they update immediately, like software. Use signals for wires and registers. Use variables only for temporary calculations inside a process."},

 {'t': 'ex', 'h': 'The #1 beginner bug: the accidental latch', 'img': 'fig:latch', 'split': 0.5,
  'code': "-- BAD: no else branch\nprocess (a, en) begin\n  if en = '1' then\n    y <= a;\n  end if;        -- en = '0' → y must\nend process;     -- REMEMBER → latch!\n\n-- GOOD: default first\nprocess (a, en) begin\n  y <= '0';      -- default value\n  if en = '1' then\n    y <= a;\n  end if;\nend process;",
  'cl': [6, 14],
  'say': ["Now the most common bug in all of beginner H D L. Look at the top process. If enable is one, y gets a. But what happens to y when enable is zero? The code doesn't say. In software, nothing happens and y keeps its old value. In hardware, keeping an old value requires memory, so the synthesis tool quietly builds a latch, a level sensitive memory element, to remember it. You meant to build a simple gate and you got a storage element with tricky timing. The tool usually just prints a warning that's easy to miss.",
          "The fix is simple. In a combinational process, give every output a default value at the very top, then override it in the branches. Now y is defined on every path, so the tool builds pure logic: a multiplexer that outputs a or zero. The two rules for combinational processes: list every input in the sensitivity list, or use the V H D L twenty oh eight keyword all, and assign every output on every path."]},

 {'t': 'v', 'h': 'How fast can your design run?', 'img': 'fig:timingpath',
  'pts': ['Data leaves a flip-flop (clock-to-Q)', 'Travels through logic', 'Must arrive **before** the next edge (setup)', 'f max = 1 / (t clk→q + t logic + t setup)'],
  'say': ["Every synchronous design is a loop: flip-flop, then some combinational logic, then another flip-flop. On each clock edge, data leaves the first flip-flop. That takes the clock to Q delay, say half a nanosecond.",
          "Then it travels through the logic. Say the slowest path, called the critical path, takes three nanoseconds.",
          "It has to arrive at the next flip-flop a little before the next clock edge. That's the setup time, say zero point three nanoseconds.",
          "Add them up: three point eight nanoseconds is the shortest legal clock period. One divided by three point eight nanoseconds is about two hundred sixty three megahertz. That's the maximum clock frequency. If you want it faster, you have to shorten the critical path, for example by using a faster adder, or by splitting the logic in half with another register in the middle. That trick is called pipelining, and it's how processors reach gigahertz speeds. The tools report this for you after place and route, in a timing report, and learning to read it is a real job skill."]},

 {'t': 'ex', 'h': 'Clock dividers: slowing 100 MHz down to human speed', 'img': 'fig:clkdiv', 'split': 0.5,
  'code': "process (clk) begin\n  if rising_edge(clk) then\n    if count = N - 1 then\n      count   <= 0;\n      slow_clk <= not slow_clk;\n    else\n      count <= count + 1;\n    end if;\n  end if;\nend process;",
  'say': "Lab boards usually run at a hundred megahertz, a hundred million ticks per second. If you blink an L E D at that rate, it just looks dimly on. So we build a clock divider: a counter that counts input cycles and flips a slow output every N cycles. Each full cycle of the output takes two N input cycles, so the output frequency is the input frequency divided by two N. In the diagram, N is four, so the output is eight times slower. Now a real calculation. To get one hertz from a hundred megahertz, N must be fifty million. How many bits does the counter need? Two to the twenty fifth is about thirty three million, too small. Two to the twenty sixth is about sixty seven million, enough. So you need a twenty six bit counter. One professional tip: in real designs, we usually don't use the divided signal as a new clock. We generate a one cycle enable pulse instead and keep the whole design on a single clock. It avoids a whole class of timing problems."},

 {'t': 'v', 'h': 'Multiplexed displays: tricking your eyes', 'img': ['a:sevenseg', 'fig:muxdisp'],
  'pts': ['4 digits share the same 7 segment wires', 'Light **one digit at a time**', 'Cycle at ~1 kHz → persistence of vision'],
  'say': ["Here's a lovely engineering trick that combines everything so far. A four digit display has four times seven, which is twenty eight L E Ds. Giving each one its own pin would waste pins.",
          "So all four digits share the same seven segment wires, and each digit gets its own enable line, called an anode. A circuit turns on one digit at a time, putting that digit's pattern on the shared segment lines, then moves to the next digit, about a thousand times per second. Each digit is actually lit only a quarter of the time, but your eye blends it together, an effect called persistence of vision, so you see all four steadily. In this course's sixth lab, students build exactly this: a clock divider, a counter that selects the digit, a multiplexer for the data, and the seven segment decoder from earlier. It's a small but complete digital system."]},

 {'t': 'v', 'h': 'Finite state machines', 'img': ['fig:fsm101', 'fig:fsm101', 'fig:fsm101_s3', 'fig:mealy'],
  'pts': ['State register + next-state logic + output logic', 'Example: detect the bit pattern 1-0-1', '**Moore:** outputs depend only on the state', '**Mealy:** outputs depend on state **and** input'],
  'say': ["Now the most useful design pattern in all of digital logic: the finite state machine. Every state machine has three parts: a register holding the current state, logic that computes the next state from the current state and the inputs, and logic that computes the outputs.",
          "Let's design one. A serial input delivers one bit per clock cycle, and we want to raise an output whenever the last three bits were one, zero, one. We start in IDLE. If we see a one, we move to got one. From there, a zero moves us to got one zero. A one in got one also keeps us there, because that one could be the start of a new pattern.",
          "From got one zero, a one completes the pattern, so we go to FOUND, where the output is one. A zero there breaks the pattern and sends us back to IDLE. And from FOUND, the final one can begin a new pattern, so a following zero takes us straight to got one zero. This is a Moore machine, because the output depends only on which state we're in.",
          "Here's the Mealy version. Outputs are written on the arrows as input slash output, because they depend on the current state and the input. The output fires on the transition itself, the orange arrow, so we don't need a FOUND state. That's one fewer state, and the answer arrives one cycle sooner. The trade off is that a Mealy output can glitch if the input glitches, while a Moore output is clean. Simplicity versus speed is a trade off you'll make over and over as an engineer."]},

 {'t': 'ex', 'h': 'Writing a state machine in VHDL', 'img': 'fig:traffic', 'split': 0.52,
  'code': "type state_t is (NS_GREEN, NS_YELLOW,\n                 EW_GREEN, EW_YELLOW);\nsignal state : state_t;\n\nprocess (clk) begin\n  if rising_edge(clk) then\n    if reset = '1' then state <= NS_GREEN;\n    else\n      case state is\n        when NS_GREEN  => if t = 30 then\n                            state <= NS_YELLOW; end if;\n        when NS_YELLOW => if t = 4 then\n                            state <= EW_GREEN; end if;\n        -- ... and so on\n      end case;\n    end if;\n  end if;\nend process;",
  'say': "Let's turn a real controller into code: a traffic light at an intersection, a classic state machine. There are four states: north south green, north south yellow, east west green, and east west yellow. Each state lasts a set number of seconds, which we measure with a counter that counts ticks of a divided clock. In V H D L, you first declare an enumerated type listing the states by name, which makes the code readable and lets the tool choose the binary encoding. Then a clocked process uses a case statement: in each state, check the condition, and move to the next state when it's met. The outputs, which lights are on, come from the state. Real intersections add sensor inputs, for example staying green for the main road until a car arrives on the side street, which is just another condition on an arrow. In this course's fifth lab, students design state machines like this, including counters and a controller, in Vivado."},

 {'t': 'ex', 'h': 'Test benches: prove it before you build it', 'img': 'fig:tb', 'split': 0.55,
  'code': "entity tb is end tb;      -- no ports!\n\narchitecture sim of tb is\n  signal a, b, cin, s, cout : std_logic;\nbegin\n  dut: entity work.full_adder\n    port map (a, b, cin, s, cout);\n\n  process\n    variable v : unsigned(2 downto 0);\n  begin\n    for i in 0 to 7 loop\n      v := to_unsigned(i, 3);\n      a <= v(2); b <= v(1); cin <= v(0);\n      wait for 10 ns;\n      assert (s = (a xor b xor cin))\n        report \"sum wrong\" severity error;\n    end loop;\n    wait;\n  end process;\nend sim;",
  'say': "Finally, how do professionals know their design works? A test bench. It's a V H D L entity with no ports, a closed world that exists only in the simulator and is never turned into hardware. Inside, it instantiates your design, called the D U T, the design under test. A process then drives the inputs. Here, a loop walks through all eight combinations, waits ten nanoseconds for things to settle, and uses assert to check the answer. If the output is wrong, the simulator prints an error message. That's a self checking test bench: instead of staring at waveforms and hoping you notice a mistake, the test tells you. In industry, verification engineers often outnumber design engineers, because finding a bug before manufacturing is so valuable. Wait statements like wait for ten nanoseconds only make sense in simulation, which is one reason a test bench can't be synthesized."},

 {'t': 'b', 'h': 'Pro tips and common mistakes',
  'pts': ['Draw the circuit (or block diagram) **before** coding', 'Combinational process: default every output — no latches', 'Clocked process: one clock, reset everything', 'Treat **U** and **X** in simulation as bugs', 'Read the synthesis warnings and the timing report', 'Write a self-checking test bench for every module'],
  'say': ["Let's collect the habits that separate working designs from frustrating ones.",
          "First, draw the circuit or at least a block diagram before you write code. Code is the schematic written in words.",
          "Second, in combinational processes, give every output a default, so you never infer latches.",
          "Third, in clocked processes, use one clock for the whole design and reset everything that matters.",
          "Fourth, if your simulation shows U or X, stop and find out why. It's almost always a missing reset or two drivers on one wire.",
          "Fifth, read the warnings and the timing report. The tools tell you about latches, unused signals and slow paths, but only if you look.",
          "And sixth, write a test bench for every module, ideally self checking. A small tested module is worth more than a big untested one."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'VHDL is a precise way to **draw circuits with words**. Picture the hardware, simulate it, then build it.',
  'cap': 'Next: EGEE 203 Electric Circuits.  Later: build a whole CPU (EGCP 381) and do it all again in Verilog (EGCP 446).',
  'say': "Let's wrap up. V H D L is a precise way to draw circuits with words. Concurrent statements are gates that all run at once. Processes with rising edge build flip-flops. State machines organize behavior over time. Timing sets your speed limit. And test benches prove it all works before you build it. These ideas come back again and again: in computer design you'll use them to build an entire processor, and in the Verilog course you'll see the very same concepts in a different language. If you remember one thing from today, make it this: picture the hardware first. Thanks for watching, and I'll see you in the next lecture."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B

def draw_fsm101(ax, n, w, h):
    r = 62; P = {'S0': (130, h - 170), 'S1': (520, h - 170), 'S2': (520, h - 520), 'S3': (130, h - 520)}
    outs = {'S0': 'S0/0', 'S1': 'S1/0', 'S2': 'S2/0', 'S3': 'S3/1'}
    if n >= 1:
        for k, (x, y) in P.items(): B.circle(ax, x, y, r, fc='#e3f2e8' if k == 'S3' else '#dfe8f7', c='green' if k == 'S3' else 'ink', text=outs[k], fs=28)
        B.arr(ax, 20, h - 60, P['S0'][0] - 45, P['S0'][1] + 45, 'gray', 2.5, 20); B.lab(ax, 40, h - 40, 'reset', 22, 'gray', ha='left')
    if n >= 2:
        def e(a, b, lbl, rad=0.0, lx=0, ly=0, f=0.5):
            (x0, y0), (x1, y1) = P[a], P[b]; d = np.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / d, (y1 - y0) / d
            B.arr(ax, x0 + ux * r, y0 + uy * r, x1 - ux * r, y1 - uy * r, 'blue', 2.8, 24, rad=rad)
            B.lab(ax, x0 + (x1 - x0) * f + lx, y0 + (y1 - y0) * f + ly, lbl, 32, 'red', bbox=dict(fc='white', ec='none', pad=1))
        e('S0', 'S1', '1', 0, 0, 25); e('S1', 'S2', '0', 0, 25, 0); e('S2', 'S3', '1', -0.25, 0, -55); e('S3', 'S2', '0', -0.25, 0, 55)
        e('S2', 'S0', '0', 0.0, 0, 0, f=0.25); e('S3', 'S1', '1', 0.0, 0, 0, f=0.25)
        B.selfloop(ax, *P['S0'], r, '0', 'blue'); B.selfloop(ax, *P['S1'], r, '1', 'blue')

def draw_path(ax, n, w, h):
    y = h * 0.55
    if n >= 1:
        B.node(ax, 20, y - 70, 130, 140, 'FF', fc='#dfe8f7', fs=34); B.node(ax, w - 150, y - 70, 130, 140, 'FF', fc='#dfe8f7', fs=34)
        t = np.linspace(0, 2 * np.pi, 120); B.poly(ax, list(zip(w / 2 + 170 * np.cos(t) + 14 * np.sin(5 * t), y + 90 * np.sin(t))), fc='#f6d6c4', c='orange')
        B.lab(ax, w / 2, y, 'logic', 32, 'orange'); B.arr(ax, 150, y, w / 2 - 175, y, 'ink', 3, 24); B.arr(ax, w / 2 + 175, y, w - 155, y, 'ink', 3, 24)
    if n >= 2:
        B.lab(ax, 85, y - 120, '0.8 ns\nclk→Q', 24, 'blue'); B.lab(ax, w / 2, y - 140, '5.2 ns', 28, 'orange'); B.lab(ax, w - 85, y - 120, '0.5 ns\nsetup', 24, 'blue')
    if n >= 3:
        B.lab(ax, w / 2, y + 170, 'split the logic with a register:', 26, 'green'); B.lab(ax, w / 2, y + 130, '0.8 + 2.6 + 0.5 = 3.9 ns', 28, 'green')

B.insert(LESSON, "Negative numbers: two's complement", {'t': 'wb', 'h': "Worked example: 6 + (−5) with two's complement", 'steps': [
    {'say': "Let's compute six plus negative five in four bit two's complement, exactly as the adder hardware does. First, build negative five. Start from five: zero one zero one.",
     'w': [{'k': '  +5  =   0101', 'plain': True, 'fs': 48, 'at': 2}]},
    {'say': "Flip every bit: one zero one zero. Then add one: one zero one one. That's negative five.",
     'w': [{'k': 'flip  =   1010', 'plain': True, 'fs': 48}, {'k': '  +1  =   1011   = -5', 'plain': True, 'fs': 48, 'c': 'red', 'at': 1}]},
    {'say': "Now add six, zero one one zero, and negative five, one zero one one, with an ordinary binary adder. Column by column from the right: zero plus one is one. One plus one is zero, carry one. One plus zero plus the carry is zero, carry one. Zero plus one plus the carry is zero, carry one, out of the top.",
     'w': [{'k': 'carry    111', 'plain': True, 'fs': 48, 'c': 'gray', 'gap': 20, 'at': 3}, {'k': '          0110   (+6)', 'plain': True, 'fs': 48, 'at': 1}, {'k': '       +  1011   (-5)', 'plain': True, 'fs': 48, 'at': 1},
           {'k': '       --------', 'plain': True, 'fs': 48, 'at': 2}, {'k': '         10001', 'plain': True, 'fs': 48, 'at': 6}]},
    {'say': "Drop the carry out of the fourth bit, and the answer is zero zero zero one: plus one. Correct! The same adder handles subtraction for free, which is exactly why every processor uses two's complement.",
     'w': [{'m': 'drop the carry:  0001 = +1', 'c': 'red', 'box': True, 'fs': 50, 'gap': 14, 'at': 1}, {'m': 'the same adder does subtraction', 'c': 'green', 'at': 3}]},
]})

B.insert(LESSON, 'Finite state machines', {'t': 'wb', 'h': "Worked example: designing a '101' detector", 'draw': 'fsm101', 'split': 0.44, 'steps': [
    {'say': "Let's design a state machine that outputs one whenever the last three input bits were one, zero, one. Name each state after what it remembers. S zero: nothing useful yet. S one: just saw a one. S two: saw one zero. S three: saw one zero one, so output one. This is a Moore machine: the output depends only on the state.",
     'w': [{'m': 'S0: nothing yet', 'at': 2}, {'m': 'S1: saw 1', 'at': 3}, {'m': 'S2: saw 10', 'at': 4}, {'m': 'S3: saw 101: output 1', 'c': 'green', 'at': 5}, {'d': 1, 'at': 2}]},
    {'say': "Now the arrows. From S zero, a one moves to S one. In S one, a zero moves to S two, but another one stays put, since that one could start a new pattern. From S two, a one completes the pattern: go to S three. A zero means one zero zero, so start over at S zero. From S three, a zero gives one zero again, S two. A one starts fresh at S one.",
     'w': [{'d': 2, 'at': 1}]},
    {'say': "Let's trace the input one, one, zero, one, zero, one, one. The states go: S one, S one, S two, S three, S two, S three, S one. The output is one exactly twice, once for each one zero one in the input. And notice they overlap, sharing a one.",
     'w': [{'m': 'in:     1  1  0  1  0  1  1', 'gap': 14, 'at': 0}, {'m': 'state:  S1 S1 S2 S3 S2 S3 S1', 'at': 1}, {'m': 'out:    0  0  0  1  0  1  0', 'c': 'red', 'at': 2}]},
    {'say': "Once the diagram is right, the VHDL is mechanical: one case branch per state, one if per arrow. Always draw the diagram first.",
     'w': [{'m': 'diagram first, then one case per state', 'c': 'blue', 'gap': 12, 'at': 1}]},
]})

B.insert(LESSON, 'How fast can your design run?', {'t': 'wb', 'h': 'Worked example: finding the maximum clock speed', 'draw': 'path', 'split': 0.45, 'steps': [
    {'say': "Every clocked design has a slowest path between two flip-flops. Here, data leaves the first flip-flop, passes through some logic, and must reach the second flip-flop before the next clock edge.",
     'w': ['register to register path', {'d': 1, 'at': 1}]},
    {'say': "The datasheet and timing report give us three delays. The clock to Q delay of the first flip-flop: point eight nanoseconds. The logic: five point two. And the setup time of the second flip-flop: point five.",
     'w': [{'d': 2, 'at': 1}, {'m': r'$T_{min} = t_{cq} + t_{logic} + t_{setup}$', 'at': 1}, {'m': r'$= 0.8 + 5.2 + 0.5 = 6.5\ \mathrm{ns}$', 'at': 3}]},
    {'say': "The clock period can't be shorter than the sum, six point five nanoseconds. So the maximum frequency is one over six point five nanoseconds, about one hundred fifty four megahertz.",
     'w': [{'m': r'$f_{max} = \frac{1}{6.5\ \mathrm{ns}} \approx 154\ \mathrm{MHz}$', 'c': 'red', 'box': True, 'at': 1}]},
    {'say': "Need it faster? Split the logic in half with an extra register in the middle. Each stage now needs point eight plus two point six plus point five, three point nine nanoseconds, about two hundred fifty six megahertz. That's pipelining, and you'll see it again when we build a processor.",
     'w': [{'d': 3, 'at': 1}, {'m': r'pipelined: $1/3.9\ \mathrm{ns} \approx 256\ \mathrm{MHz}$', 'c': 'green', 'at': 2}]},
]})

# ---------------- the teacher's pen ----------------
G = "Worked example: 6 + (−5) with two's complement"
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '1010', 'c': 'blue', 'at': 0}, {'p': ('circle',), 'on': '1011   = -5', 'at': 1})
B.pen(LESSON, G, 2, *[{'p': ('span',), 'on': '0110   (+6)', 'to': '10001', 'cols': (c, c + 1), 'c': 'blue', 'at': a, 'solo': a > 1} for a, c in ((1, 13), (2, 12), (3, 11), (4, 10))])
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'the same adder does subtraction', 'at': 3})
G = "Worked example: designing a '101' detector"
B.pen(LESSON, G, 0, {'p': ('box',), 'on': 'S3: saw 101', 'c': 'green', 'at': 5})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'state:  S1', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': 'out:', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'diagram first', 'at': 1})
G = 'Worked example: finding the maximum clock speed'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$T_{min}', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': r'$= 0.8 + 5.2', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': 'pipelined:', 'c': 'green', 'at': 2})

# ---------------- the pen on ordinary slides ----------------
B.spen(LESSON, 'Why describe hardware with code?', 2, {'p': 'underline', 'on': 'describe behavior', 'at': 1})
S = 'The big mindset shift'
B.spen(LESSON, S, 0, *[{'fig': [('box', .07, y0, .31, y1)], 'c': 'blue', 'at': 2, 'dt': t} for y0, y1, t in ((.24, .37, 0.2), (.43, .56, 1.0), (.62, .75, 1.8))])
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, y, rx, ry)], 'c': 'green', 'at': 2, 'dt': t} for x, y, rx, ry, t in
       ((.67, .34, .08, .09, 0.6), (.67, .66, .07, .07, 1.4), (.86, .5, .08, .09, 2.2))])
S = 'Anatomy of a design'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'library ieee;', 'at': 1}, {'p': 'highlight', 'on': 'use ieee.std_logic_1164.all;', 'at': 1, 'dt': 1.0})
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'entity full_adder is', 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': 'a, b, cin : in', 'c': 'blue', 'at': 3},
       {'p': 'underline', 'on': 's, cout   : out', 'c': 'blue', 'at': 3, 'dt': 2.5})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'architecture dataflow of full_adder is', 'c': 'green', 'at': 0},
       {'p': 'highlight', 'on': 's    <= a xor b xor cin;', 'at': 1}, {'p': 'highlight', 'on': 'cout <= (a and b) or (cin and (a xor b));', 'at': 1, 'dt': 2.0},
       {'p': 'circle', 'on': '<=', 'at': 2})
S = 'Designing a full adder, step by step'
B.spen(LESSON, S, 1, {'fig': [('box', .74, .07, .87, .93)], 'c': 'blue', 'at': 1}, {'p': 'underline', 'on': 'odd number of inputs are 1', 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'two or more inputs are 1', 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'box', 'on': '1 + 1 + 0 = binary 10 = 2', 'c': 'green', 'at': 5})
S = 'Real gates have delay'
B.spen(LESSON, S, 1, {'fig': [('circle', .42, .1, .03, .07)], 'c': 'blue', 'at': 1, 'dt': 0.4}, {'fig': [('circle', .5, .27, .03, .07)], 'c': 'blue', 'at': 1, 'dt': 2.5},
       {'fig': [('circle', .54, .47, .08, .11)], 'at': 3})
B.spen(LESSON, S, 2, {'p': 'highlight', 'on': 's <= a xor b after 2 ns;', 'at': 0})
S = 'Port maps'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'signal c : std_logic_vector(4 downto 0);', 'at': 3},
       {'p': 'box', 'on': 'fa: entity work.full_adder', 'c': 'blue', 'at': 4},
       {'p': 'underline', 'on': 'a => a(i)', 'c': 'green', 'at': 5, 'dt': 4.0}, {'p': 'underline', 'on': 'cin => c(i)', 'c': 'green', 'at': 5, 'dt': 5.0},
       {'p': 'underline', 'on': 'cout => c(i+1)', 'c': 'green', 'at': 5, 'dt': 6.5}, {'p': 'circle', 'on': 'for i in 0 to 3 generate', 'at': 6},
       {'p': 'circle', 'on': '3 generate', 'c': 'orange', 'at': 7})
S = 'Negative numbers'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': '−x = (NOT x) + 1', 'at': 5}, {'fig': [('circle', .345, .83, .07, .09)], 'c': 'orange', 'at': 9},
       {'fig': [('circle', .4, .79, .045, .06)], 'at': 10, 'dt': 0.2}, {'fig': [('circle', .3, .81, .045, .06)], 'at': 10, 'dt': 1.2})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'Subtract = add the complement', 'c': 'green', 'at': 1})
S = 'std_logic: a wire has nine possible values'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .125, .97, .215)], 'at': 3}, {'fig': [('box', .03, .22, .97, .31)], 'at': 5},
       {'fig': [('box', .03, .505, .97, .595)], 'c': 'blue', 'at': 7}, {'fig': [('box', .03, .89, .97, .985)], 'c': 'green', 'at': 9})
S = 'Three ways to write combinational logic'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'y1 <= (a and b) or c;', 'at': 1})
B.spen(LESSON, S, 1, {'p': 'highlight', 'on': 'y2 <= a when sel = "00" else', 'at': 0}, {'p': 'underline', 'on': 'b when sel = "01" else', 'c': 'blue', 'at': 1, 'dt': 1.5})
B.spen(LESSON, S, 2, {'p': 'highlight', 'on': 'with sel select', 'at': 0}, {'p': 'circle', 'on': 'd when others;', 'at': 3})
S = 'Example: driving a seven-segment display'
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'with … select', 'c': 'green', 'at': 1})
S = 'Processes: how VHDL describes memory'
B.spen(LESSON, S, 0, {'p': 'box', 'on': 'process (clk)', 'at': 2}, {'p': 'circle', 'on': '(clk)', 'c': 'blue', 'at': 4})
B.spen(LESSON, S, 1, {'p': 'highlight', 'on': 'if rising_edge(clk) then', 'at': 0}, {'p': 'underline', 'on': 'q <= d;', 'c': 'green', 'at': 1},
       {'p': 'underline', 'on': "if reset = '1' then", 'c': 'blue', 'at': 5})
S = 'Signals vs. variables'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'a <= b;', 'at': 3}, {'p': 'highlight', 'on': 'b <= a;', 'at': 3, 'dt': 1.0},
       {'p': 'circle', 'on': 'swap!', 'c': 'green', 'at': 5, 'dt': 2.0}, {'p': 'circle', 'on': ':=', 'c': 'blue', 'at': 8})
S = 'The #1 beginner bug'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': "if en = '1' then", 'at': 2}, {'p': 'underline', 'on': "en = '0' → y must", 'at': 3},
       {'p': 'circle', 'on': '→ latch!', 'at': 6})
B.spen(LESSON, S, 1, {'p': 'highlight', 'on': "y <= '0';", 'c': 'green', 'at': 1}, {'p': 'check', 'on': '-- GOOD: default first', 'c': 'green', 'at': 2})
S = 'How fast can your design run?'
B.spen(LESSON, S, 0, {'fig': [('box', .1, .73, .2, .82)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('box', .2, .73, .83, .82)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .83, .73, .9, .82)], 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('underline', .14, .49, .7)], 'at': 0}, {'fig': [('circle', .72, .665, .14, .05)], 'c': 'green', 'at': 1})
S = 'Clock dividers'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'if count = N - 1 then', 'at': 2}, {'p': 'underline', 'on': 'slow_clk <= not slow_clk;', 'c': 'blue', 'at': 2, 'dt': 3.5},
       {'p': 'underline', 'on': 'count <= count + 1;', 'c': 'green', 'at': 3})
S = 'Multiplexed displays'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'one digit at a time', 'at': 1})
S = 'Finite state machines'
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, .48, .07, .1)], 'c': 'blue', 'at': a} for x, a in ((.12, 2), (.38, 3), (.64, 4))])
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'Moore:', 'c': 'green', 'at': 3})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Mealy:', 'c': 'orange', 'at': 0})
S = 'Writing a state machine in VHDL'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'type state_t is (NS_GREEN, NS_YELLOW,', 'at': 3}, {'p': 'box', 'on': 'case state is', 'c': 'blue', 'at': 4},
       {'p': 'underline', 'on': 'if t = 30 then', 'c': 'green', 'at': 4, 'dt': 2.5})
S = 'Test benches'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': '-- no ports!', 'at': 2}, {'p': 'box', 'on': 'dut: entity work.full_adder', 'c': 'blue', 'at': 3},
       {'p': 'highlight', 'on': 'for i in 0 to 7 loop', 'at': 5}, {'p': 'highlight', 'on': 'wait for 10 ns;', 'at': 5, 'dt': 2.0},
       {'p': 'highlight', 'on': 'assert (s = (a xor b xor cin))', 'c': 'green', 'at': 5, 'dt': 4.0}, {'p': 'circle', 'on': 'report "sum wrong"', 'at': 6})
S = 'Pro tips and common mistakes'
for b, t in ((1, 'before'), (2, 'default every output'), (3, 'one clock, reset everything'), (4, 'Treat U and X'), (5, 'Read the synthesis warnings'), (6, 'self-checking test bench')):
    B.spen(LESSON, S, b, {'p': 'underline', 'on': t, 'n': 0, 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Worked example: 6 + (', {'t': 'wb', 'h': 'Numbers in VHDL: bits vs unsigned vs signed', 'lang': 'vhdl', 'cfs': 32, 'steps': [
    {'say': "Here's the error every beginner hits in their first hour. You write count gets count plus one, and the compiler refuses. Why? Because a standard logic vector is just a bundle of wires. It has no idea whether those bits are a number, let alone a positive or negative one.",
     'w': [{'k': 'signal count : std_logic_vector(3 downto 0);', 'at': 1}, {'k': 'count <= count + 1;     -- ERROR: no "+" for plain bits', 'at': 1}]},
    {'say': "The fix is the numeric standard library. It adds two types made of the same bits. Unsigned means the bits are a plain binary number. Signed means they're two's complement. The same pattern, one zero one one, is eleven as unsigned, and minus five as signed.",
     'w': [{'k': 'use ieee.numeric_std.all;', 'at': 1, 'gap': 14}, {'m': '1011  as unsigned = 11      as signed = −5', 'c': 'blue', 'at': 4}]},
    {'say': "So declare counters as unsigned, and plus just works. When you need to move between worlds, convert explicitly. To integer turns unsigned into an integer. To unsigned, with a width, goes the other way. And wrapping a value in standard logic vector turns it back into plain bits for a port.",
     'w': [{'k': 'signal count : unsigned(3 downto 0);', 'at': 0, 'gap': 14}, {'k': 'count <= count + 1;                        -- OK', 'at': 0},
           {'k': 'n   := to_integer(count);', 'at': 2}, {'k': 'cnt := to_unsigned(9, 4);                  -- 9 as 4 bits', 'at': 3},
           {'k': 'leds <= std_logic_vector(count);', 'at': 4}]},
    {'say': "And one small rule that causes a lot of syntax errors: a single bit uses single quotes, like quote one quote. A vector uses double quotes, like quote zero one zero one quote. Mix them up, and the compiler complains about types.",
     'w': [{'k': "a <= '1';        -- one bit: single quotes", 'at': 1, 'gap': 14}, {'k': 'v <= "0101";     -- a vector: double quotes', 'at': 2}]},
]})

G = 'Numbers in VHDL: bits vs unsigned vs signed'
B.pen(LESSON, G, 0, {'p': ('cross',), 'on': 'count <= count + 1;     -- ERROR', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': '1011  as unsigned', 'c': 'blue', 'at': 4})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'count <= count + 1;                        -- OK', 'at': 0})
