# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'The rule to memorize: blocking vs. non-blocking', {'t': 'wb', 'h': 'Worked example: the latch you never asked for', 'lang': 'verilog', 'cfs': 34, 'steps': [
    {'say': "The latch rule is easier to see than to hear. This combinational block sets y to a when select is one. But what should y be when select is zero? The code doesn't say.",
     'w': [{'k': 'always @(*) begin', 'at': 1}, {'k': '  if (sel) y = a;', 'at': 1}, {'k': 'end', 'at': 1}]},
    {'say': "Hardware can't leave a question unanswered, so the tool assumes y must keep its old value. Keeping a value means memory, and a memory controlled by a level, not a clock edge, is a latch. The synthesis report will warn: inferring latch for y. Latches cause timing headaches and glitchy behavior, and they're almost never what you meant.",
     'w': [{'m': 'sel = 0:  y = ?   →  "keep old value"  →  LATCH', 'c': 'red', 'at': 2}]},
    {'say': "Fix one: add an else branch, so every path assigns y. Now it's a plain two to one multiplexer.",
     'w': [{'k': 'always @(*) begin', 'at': 1, 'gap': 14}, {'k': '  if (sel) y = a;', 'at': 1}, {'k': '  else     y = b;', 'at': 1}, {'k': 'end', 'at': 1}]},
    {'say': "Fix two, the habit professionals use: put a default assignment at the very top of the block. Then any branch you forget simply falls back to the default. This matters most in big case statements for state machines, where it's easy to miss one output in one state.",
     'w': [{'k': 'always @(*) begin', 'at': 1, 'gap': 14}, {'k': '  y = 0;            // default first', 'at': 1}, {'k': '  if (sel) y = a;', 'at': 1}, {'k': 'end', 'at': 1},
           {'m': 'every output, every path', 'c': 'green', 'box': True, 'at': 2}]},
]})

def draw_slack(ax, n, w, h):
    y = h * 0.55; x0 = 40; sc = (w - 80) / 10.0
    if n >= 1:
        B.ln(ax, [x0, x0 + 10 * sc], [y - 70, y - 70], 'gray', 2)
        for t in range(0, 11, 2):
            B.ln(ax, [x0 + t * sc] * 2, [y - 78, y - 62], 'gray', 2); B.lab(ax, x0 + t * sc, y - 100, f'{t} ns', 30, 'gray')
        segs = [(0, 0.5, '#9ab', 'clk→Q'), (0.5, 8.5, '#e9a', 'logic + wires  8.0'), (8.5, 8.9, '#cb6', 'setup')]
        for a, b, col, t in segs:
            B.rect(ax, x0 + a * sc, y - 40, (b - a) * sc, 80, fc=col, c='ink', lw=2)
        B.lab(ax, x0 + 4.5 * sc, y, 'logic + wires  8.0', 34, 'ink')
        B.ln(ax, [x0 + 10 * sc] * 2, [y - 60, y + 80], 'red', 3); B.lab(ax, x0 + 10 * sc, y - 140, 'next edge', 30, 'red', ha='right')
    if n >= 2:
        B.arr(ax, x0 + 8.9 * sc, y + 55, x0 + 10 * sc, y + 55, 'green', 2.5, 14); B.lab(ax, x0 + 9.45 * sc, y + 95, 'slack', 32, 'green')

B.insert(LESSON, 'From RTL to bitstream: implementation and timing', {'t': 'wb', 'h': 'Worked example: reading a timing report', 'draw': 'slack', 'split': 0.5, 'steps': [
    {'say': "What is slack, exactly? Follow one path between two flip flops on a one hundred megahertz clock: ten nanoseconds per cycle. The launching flip flop takes half a nanosecond to change its output. The logic and wires take eight. And the capturing flip flop needs its input steady for point four nanoseconds of setup time before the next edge.",
     'w': [{'m': r'$T = 10$ ns,  $t_{cq} = 0.5$,  $t_{logic} = 8.0$,  $t_{su} = 0.4$', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Slack is the time to spare: the period minus everything the path needs. Ten minus point five minus eight minus point four: one point one nanoseconds. Positive, so this path is fine.",
     'w': [{'m': r'slack $= T - (t_{cq} + t_{logic} + t_{su})$', 'c': 'blue', 'at': 0}, {'m': r'$= 10 - 8.9 = +1.1$ ns', 'c': 'green', 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "Now someone adds a multiplier and the logic grows to ten nanoseconds. The slack becomes ten minus ten point nine: minus point nine. The worst negative slack is negative, so this design may fail in hardware at one hundred megahertz, even though the simulation looked perfect, because simulation doesn't model delays.",
     'w': [{'m': r'$t_{logic} = 10$:  slack $= 10 - 10.9 = -0.9$ ns', 'c': 'red', 'at': 1}]},
    {'say': "The cure is pipelining: put a register in the middle, splitting the ten nanoseconds into two paths of five. Each now has plenty of slack, at the cost of one extra cycle of latency. Or lower the clock: with a twelve nanosecond period, about eighty three megahertz, the original path fits too.",
     'w': [{'m': 'pipeline: 10 ns → 5 + 5 ns  (+1 cycle latency)', 'c': 'green', 'box': True, 'at': 0}, {'m': 'or slow the clock: T = 12 ns ≈ 83 MHz', 'at': 3}]},
]})

G = 'Worked example: the latch you never asked for'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'LATCH', 'c': 'red', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': '  y = 0;', 'c': 'green', 'at': 1})
G = 'Worked example: reading a timing report'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'$= 10 - 8.9 = +1.1$ ns', 'c': 'green', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('cross',), 'on': r'$t_{logic} = 10$', 'at': 2})
