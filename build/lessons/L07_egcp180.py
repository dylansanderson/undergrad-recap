import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_noise(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    t = X(0, 8, 800); rng = np.random.default_rng(2); noise = 0.35 * rng.standard_normal(len(t))
    sig = np.sin(t * 1.3) * 1.5 + 2.5
    a1.plot(t, sig + noise, color=C['orange'], lw=1.5); a1.plot(t, sig, color=C['ink'], lw=2.5); a1.set_ylabel('analog'); a1.set_title('noise corrupts an analog value forever …', fontsize=20)
    bits = (np.floor(t) % 3 != 1).astype(float) * 5
    a2.plot(t, bits + noise, color=C['orange'], lw=1.5); a2.axhline(2.5, color=C['blue'], ls='--', lw=2)
    a2.plot(t, np.where(bits + noise > 2.5, 5, 0), color=C['green'], lw=3); a2.set_ylabel('digital'); a2.set_xlabel('time')
    a2.set_title('… but a digital receiver just asks: above or below the threshold?', fontsize=20)
    for a in (a1, a2): a.set_yticks([])
    save(fig, path)

def fig_binary(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    bits = '10011100'; pv = [128, 64, 32, 16, 8, 4, 2, 1]
    for i, (b, p) in enumerate(zip(bits, pv)):
        x = 6 + i * 11
        box(ax, x, 22, 9.5, 11, b, fc=C['lorange'] if b == '1' else C['pale'], ec=C['orange'] if b == '1' else C['gray'], fs=30, bold=True, r=0.4)
        txt(ax, x + 4.75, 38, str(p), 20, C['blue'] if b == '1' else C['mut'], bold=b == '1')
    txt(ax, 50, 46, 'place values (powers of 2)', 18, C['mut'])
    ax.add_patch(Rectangle((5, 20), 45.5, 15, fc='none', ec=C['purple'], lw=2.5, ls='--')); ax.add_patch(Rectangle((50.5, 20), 44, 15, fc='none', ec=C['purple'], lw=2.5, ls='--'))
    txt(ax, 27.5, 15, '1001 = 9', 21, C['purple'], bold=True); txt(ax, 72.5, 15, '1100 = C', 21, C['purple'], bold=True)
    txt(ax, 50, 5, '128 + 16 + 8 + 4 = 156   =   0x9C', 26, C['ink'], bold=True)
    save(fig, path)

def fig_gray(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    rows = []
    for n in range(8):
        g = n ^ (n >> 1); rows.append((n, f'{n:03b}', f'{g:03b}'))
    table(ax, 4, H - 2, ['n', 'binary', 'Gray code'], rows, [12, 20, 22], 6.4, 21)
    txt(ax, 78, 44, '3 → 4 in binary:\n011 → 100\n(all 3 bits flip!)', 20, C['red'])
    txt(ax, 78, 22, 'in Gray code:\n010 → 110\n(only 1 bit flips)', 20, C['green'])
    save(fig, path)

def fig_cmos(path, w, h):
    fig, ax, H = canvas(w, h, need=66, exact=True)
    for k, (vin, top_on) in enumerate((('0', True), ('1', False))):
        x0 = 6 + k * 50
        line(ax, [(x0 + 20, 60), (x0 + 20, 52)], C['ink'], 3); txt(ax, x0 + 20, 63, 'VDD (1)', 18, C['red'], bold=True)
        box(ax, x0 + 13, 40, 14, 12, 'PMOS\n' + ('ON' if top_on else 'off'), fc=C['lgreen'] if top_on else '#EEEEEE', ec=C['green'] if top_on else C['gray'], fs=16, bold=top_on)
        line(ax, [(x0 + 20, 40), (x0 + 20, 26)], C['ink'], 3); dot(ax, x0 + 20, 33, 0.9)
        box(ax, x0 + 13, 14, 14, 12, 'NMOS\n' + ('off' if top_on else 'ON'), fc='#EEEEEE' if top_on else C['lgreen'], ec=C['gray'] if top_on else C['green'], fs=16, bold=not top_on)
        line(ax, [(x0 + 20, 14), (x0 + 20, 6)], C['ink'], 3); txt(ax, x0 + 20, 3, 'GND (0)', 18, C['blue'], bold=True)
        line(ax, [(x0 + 20, 33), (x0 + 32, 33)], C['ink'], 3); txt(ax, x0 + 33, 33, 'out=' + ('1' if top_on else '0'), 19, C['orange'], ha='left', bold=True)
        line(ax, [(x0 + 4, 46), (x0 + 13, 46)], C['ink'], 2); line(ax, [(x0 + 4, 20), (x0 + 13, 20)], C['ink'], 2); line(ax, [(x0 + 4, 46), (x0 + 4, 20)], C['ink'], 2)
        txt(ax, x0 + 4, 50, 'in = ' + vin, 20, C['purple'], bold=True)
    save(fig, path)

def fig_gates(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    kinds = [('and', 'AND', '0001'), ('or', 'OR', '0111'), ('not', 'NOT', '10'), ('nand', 'NAND', '1110'), ('nor', 'NOR', '1000'), ('xor', 'XOR', '0110')]
    for i, (k, nm, tt) in enumerate(kinds):
        col, row = i % 3, i // 3
        x = 6 + col * 33; y = 42 - row * 26
        g = gate(ax, k, x + 4, y, 12, fc=C['lblue'])
        for p in g['in']: wire(ax, [(x, p[1]), p])
        wire(ax, [g['out'], (g['out'][0] + 4, g['out'][1])])
        txt(ax, x + 10, y + 9, nm, 20, C['blue'], bold=True)
        txt(ax, x + 10, y - 9, ('out for 00,01,10,11: ' if len(tt) == 4 else 'out for 0,1: ') + ' '.join(tt), 15, C['mut'])
    save(fig, path)

def fig_kmap(path, w, h, groups=0):
    fig, ax, H = canvas(w, h, need=64, exact=True)
    ones = {0, 2, 5, 7, 8, 10, 13, 15}; gray = ['00', '01', '11', '10']
    x0, y0, cs = 26, 52, 11
    txt(ax, x0 - 6, y0 + 6, 'AB \\ CD', 18, C['mut'])
    for j, cd in enumerate(gray): txt(ax, x0 + j * cs + cs / 2, y0 + 3, cd, 20, C['blue'], bold=True)
    for i, ab in enumerate(gray):
        txt(ax, x0 - 4, y0 - i * cs - cs / 2, ab, 20, C['blue'], bold=True)
        for j, cd in enumerate(gray):
            m = int(ab + cd, 2)
            ax.add_patch(Rectangle((x0 + j * cs, y0 - (i + 1) * cs), cs, cs, fc='white', ec=C['ink'], lw=1.8))
            txt(ax, x0 + j * cs + cs / 2, y0 - i * cs - cs / 2, '1' if m in ones else '0', 26, C['ink'] if m in ones else '#B0B6C2', bold=m in ones)
            txt(ax, x0 + j * cs + cs - 1.2, y0 - i * cs - cs + 1.5, str(m), 12, C['mut'])
    if groups >= 1:
        ax.add_patch(FancyBboxPatch((x0 + cs + 1, y0 - 3 * cs + 1), 2 * cs - 2, 2 * cs - 2, boxstyle='round,pad=0,rounding_size=2', fc='none', ec=C['orange'], lw=4))
        txt(ax, 82, 40, 'BD', 26, C['orange'], bold=True)
    if groups >= 2:
        for (cx, cy) in ((x0, y0 - cs), (x0 + 3 * cs, y0 - cs), (x0, y0 - 4 * cs), (x0 + 3 * cs, y0 - 4 * cs)):
            ax.add_patch(FancyBboxPatch((cx + 1, cy + 1), cs - 2, cs - 2, boxstyle='round,pad=0,rounding_size=2', fc='none', ec=C['green'], lw=4))
        txt(ax, 84, 28, "B'D'", 26, C['green'], bold=True); txt(ax, 84, 18, '(4 corners\nwrap around)', 16, C['green'])
    if groups >= 2: txt(ax, 50, 3, "F = BD + B'D'", 28, C['ink'], bold=True)
    else: txt(ax, 50, 3, 'F = Σm(0,2,5,7,8,10,13,15)', 24, C['ink'])
    save(fig, path)
def fig_kmap0(p, w, h): fig_kmap(p, w, h, 0)
def fig_kmap1(p, w, h): fig_kmap(p, w, h, 1)
def fig_kmap2(p, w, h): fig_kmap(p, w, h, 2)

def fig_bool(path, w, h):
    fig, ax, H = canvas(w, h, need=72, exact=True)
    steps = [("AB + AB' + A'B", 'start: 3 ANDs + OR', C['pale']), ("A(B + B') + A'B", 'factor out A', C['pale']),
             ("A·1 + A'B  =  A + A'B", "B + B' = 1", C['pale']), ('A + B', "A + A'B = A + B", C['lgreen'])]
    for i, (e, why, fc) in enumerate(steps):
        y = H - 14 - i * 14
        box(ax, 6, y - 5, 52, 10, e, fc=fc, ec=C['green'] if i == 3 else C['gray'], fs=24, bold=i == 3)
        txt(ax, 62, y, why, 19, C['mut'], ha='left')
        if i < 3: arrow(ax, (32, y - 5), (32, y - 9), lw=2.2, ms=14)
    txt(ax, 50, 2.5, 'same truth table, one gate instead of four', 19, C['green'], bold=True)
    save(fig, path)

def fig_majority(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    rows = [(a, b, c, int(a + b + c >= 2)) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    table(ax, 3, H - 2, ['A', 'B', 'C', 'F'], rows, [8, 8, 8, 9], 6.2, 21, hl={3, 5, 6, 7}, hlc=C['lgreen'])
    txt(ax, 70, 50, 'minterms: m3, m5, m6, m7', 20, C['mut'])
    txt(ax, 70, 40, "F = A'BC + AB'C + ABC' + ABC", 18)
    txt(ax, 70, 30, 'simplify ↓', 18, C['mut'])
    txt(ax, 70, 20, 'F = AB + AC + BC', 26, C['blue'], bold=True)
    txt(ax, 70, 8, '(2-out-of-3 voting — used in\nfault-tolerant spacecraft computers)', 16, C['mut'])
    save(fig, path)

def fig_blocks(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    items = [('MUX', 'select one of\nmany inputs'), ('decoder', 'n bits → one of\n2ⁿ outputs'), ('encoder', 'which input is\nactive? → n bits'),
             ('adder', 'binary addition\n(full adders)'), ('comparator', 'A = B ?  A > B ?')]
    for i, (nm, d) in enumerate(items):
        x = 2 + i * 19.6; box(ax, x, 22, 17.6, 16, nm, fc=C['lblue'], fs=22, bold=True); txt(ax, x + 8.8, 12, d, 19, C['ink'])
    txt(ax, 50, 46, 'Combinational building blocks: outputs depend only on current inputs', 19, bold=True)
    save(fig, path)

def fig_srlatch(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    g1 = gate(ax, 'nor', 34, 40, 14); g2 = gate(ax, 'nor', 34, 16, 14)
    wire(ax, [(14, g1['in'][0][1]), g1['in'][0]]); txt(ax, 12, g1['in'][0][1], 'R', 24, ha='right', bold=True)
    wire(ax, [(14, g2['in'][1][1]), g2['in'][1]]); txt(ax, 12, g2['in'][1][1], 'S', 24, ha='right', bold=True)
    o1, o2 = g1['out'], g2['out']
    wire(ax, [o1, (70, o1[1])]); txt(ax, 72, o1[1], 'Q', 24, ha='left', bold=True, c=C['orange'])
    wire(ax, [o2, (70, o2[1])]); txt(ax, 72, o2[1], "Q'", 24, ha='left', bold=True, c=C['orange'])
    wire(ax, [(60, o1[1]), (60, 31), (28, 25), (28, g2['in'][0][1]), g2['in'][0]], C['orange'], 2.8)
    wire(ax, [(62, o2[1]), (62, 25), (30, 31), (30, g1['in'][1][1]), g1['in'][1]], C['orange'], 2.8)
    dot(ax, 60, o1[1], 0.7, C['orange']); dot(ax, 62, o2[1], 0.7, C['orange'])
    txt(ax, 50, 3, 'feedback: each output feeds the other gate → the circuit remembers', 18, C['mut'])
    txt(ax, 2, 52, 'S=1: set Q=1 · R=1: reset Q=0 · both 0: hold', 18, C['ink'], ha='left')
    save(fig, path)

def fig_counter(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    n = 16; q0 = [k % 2 for k in range(n)]; q1 = [(k // 2) % 2 for k in range(n)]; q2 = [(k // 4) % 2 for k in range(n)]
    timing(ax, 16, H - 10, [('clk', 'clk'), ('Q0', q0), ('Q1', q1), ('Q2', q2), ('count', [str(k % 8) for k in range(n)])], cw=5, rh=10, hi=5.5, fs=19, ncyc=n,
           colors={'Q0': C['orange'], 'Q1': C['green'], 'Q2': C['purple']})
    save(fig, path)

def fig_memory(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    box(ax, 4, 14, 16, 34, 'address\ndecoder\n11 → 2048', fc=C['lorange'], ec=C['orange'], fs=17)
    for i in range(8):
        y = 50 - i * 5.2
        for b in range(8): ax.add_patch(Rectangle((30 + b * 7, y - 4), 6.4, 4.4, fc=C['lblue'] if i != 3 else C['lyellow'], ec=C['blue'], lw=1.2))
        line(ax, [(20, y - 1.8), (30, y - 1.8)], C['orange'] if i == 3 else C['gray'], 2 if i == 3 else 1)
    txt(ax, 58, 56, '2048 words × 8 bits = 16 Kbit', 20, bold=True); txt(ax, 92, 34, '← selected\n   word', 17, C['orange'], ha='right')
    arrow(ax, (2, 31), (4, 31), lw=2); txt(ax, 12, 9, 'A10…A0', 17, C['orange'])
    arrow(ax, (58, 8), (58, 2), lw=2.4); txt(ax, 62, 5, 'D7…D0 (data)', 17, C['blue'], ha='left')
    save(fig, path)

def fig_cpu(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    box(ax, 3, 8, 54, 46, '', fc=C['pale'], ec=C['blue'], lw=3); txt(ax, 30, 50, 'CPU', 22, C['blue'], bold=True)
    box(ax, 7, 30, 22, 14, 'control\nunit', fc=C['lorange'], ec=C['orange'], fs=19, bold=True)
    box(ax, 32, 30, 22, 14, 'registers\nPC  IR  R0…R7', fc=C['lblue'], fs=16)
    box(ax, 18, 12, 24, 13, 'ALU\n+  −  AND  OR', fc=C['lgreen'], ec=C['green'], fs=17, bold=True)
    box(ax, 70, 12, 26, 42, 'memory\n\ninstructions\n+\ndata', fc=C['lyellow'], ec=C['yellow'], fs=18, bold=True)
    arrow(ax, (57, 38), (70, 38), style='<|-|>', lw=3, text='address / data bus', fs=15); arrow(ax, (43, 30), (35, 25), style='<|-|>', lw=2.4)
    arrow(ax, (18, 30), (25, 25), lw=2.4, color=C['orange'])
    txt(ax, 50, 3, 'fetch → decode → execute → repeat, billions of times per second', 18, C['ink'], bold=True)
    save(fig, path)

LESSON = {
 'code': 'EGCP 180', 'title': 'Digital Logic and Computer Structures', 'tag': 'Year 1 · Digital design', 'folder': 'EGCP-180 Digital Logic',
 'slides': [
 {'t': 'title', 'h': 'Digital Logic', 'sub': 'Binary, Boolean algebra, gates, flip-flops and the structure of a computer', 'img': 'a:sn7400',
  'say': "Welcome to E G C P one eighty, digital logic and computer structures. This is the course where you learn how a computer is built from the bottom up. That little black chip is a seventy four hundred, containing four NAND gates, and believe it or not, you could build an entire computer out of nothing but NAND gates. We'll go from binary numbers, to Boolean algebra, to gates, to memory, and finally to how a C P U fits together."},

 {'t': 'v', 'h': 'Why digital? Because noise can’t fool a threshold', 'img': 'fig:noise',
  'pts': ['Analog: every bit of noise changes the value', 'Digital: only two levels — 0 or 1', 'Receiver asks one question: above or below threshold?', 'Copies and long cables stay perfect'],
  'say': ["Why do we build computers out of ones and zeros? Look at the top graph. An analog signal stores information in its exact voltage. Add noise, the orange wiggle, and the value is corrupted. Copy it again and again, and the errors pile up, like a photocopy of a photocopy.",
          "A digital signal uses just two levels. Here, zero volts means zero and five volts means one.",
          "The receiver only asks one question: is the voltage above or below the threshold, the dashed line? Even with plenty of noise, it recovers the exact bits, the green line.",
          "That's why digital information can be copied billions of times, stored for decades and sent across the planet without degrading. Every phone call, photo and video you've ever streamed relies on that idea."]},

 {'t': 'v', 'h': 'Binary and hexadecimal', 'img': 'fig:binary',
  'pts': ['Each bit position is a power of 2', '10011100₂ = 128 + 16 + 8 + 4 = 156', 'Hex: each digit = 4 bits (0–9, A–F)', '1001 1100 → 9C → written 0x9C'],
  'say': ["In binary, each position is a power of two instead of a power of ten: one, two, four, eight, sixteen, and so on, up to one hundred twenty eight for eight bits.",
          "To convert one zero zero one one one zero zero to decimal, add the place values where there's a one: one twenty eight plus sixteen plus eight plus four is one hundred fifty six. To go the other way, keep subtracting the largest power of two that fits.",
          "Long binary strings are hard for humans to read, so engineers use hexadecimal, base sixteen. Each hex digit stands for exactly four bits, using zero through nine and then A through F for ten through fifteen.",
          "Split the byte into groups of four: one zero zero one is nine, and one one zero zero is twelve, which is C. So the byte is nine C, written zero x nine C. You'll see hex everywhere: memory addresses, color codes like hash F F zero zero zero zero for red, and register values in a debugger."]},

 {'t': 'v', 'h': 'Codes: BCD, ASCII and Gray code', 'img': ['fig:gray', 'a:rotary_encoder'],
  'pts': ['BCD: each decimal digit in 4 bits (calculators, clocks)', 'ASCII: 7-bit codes for text', 'Gray code: neighbors differ in exactly one bit', 'Used in rotary encoders to avoid glitches'],
  'say': ["Bits can encode more than plain numbers. Binary coded decimal stores each decimal digit in its own four bits, which makes driving digit displays easy. ASCII, as you saw in programming, encodes text. And Gray code is a clever ordering where neighboring values differ in exactly one bit. Look at three to four. In normal binary, all three bits flip at once: zero one one becomes one zero zero. In real hardware, those bits never flip at exactly the same instant, so for a moment you might read a garbage value like one one one. In Gray code, three to four is zero one zero to one one zero. Only one bit changes, so there's no in between garbage.",
          "That's why rotary position sensors, like this encoder used to measure the angle of a motor shaft or a robot joint, mark their tracks in Gray code. It's also why the rows and columns of the Karnaugh maps you're about to learn are in Gray order."]},

 {'t': 'v', 'h': 'From transistors to gates: the CMOS inverter', 'img': 'fig:cmos',
  'pts': ['A transistor is a voltage-controlled switch', 'PMOS connects output to 1; NMOS connects it to 0', 'Exactly one is on → output = NOT input', 'Billions of these = a modern chip'],
  'say': ["What's a logic gate made of? Transistors, used as switches. In today's C M O S technology, there are two kinds. A P M O S transistor turns on when its input is zero. An N M O S transistor turns on when its input is one.",
          "Put a P M O S between the power supply and the output, and an N M O S between the output and ground. That's an inverter.",
          "When the input is zero, the top switch closes and the bottom opens, so the output connects to one. When the input is one, it flips, and the output connects to zero. Exactly one switch is on at a time, which means almost no current flows when nothing is switching. That's why C M O S chips use so little power.",
          "Combine a few more transistors in series and parallel, and you get NAND and NOR gates. A modern processor is billions of these tiny switches. You'll study exactly how they work, and how fast they switch, in the electronics courses."]},

 {'t': 'v', 'h': 'The logic gates', 'img': ['fig:gates', 'a:sn7400'],
  'pts': ['AND, OR, NOT — the basics', 'NAND, NOR — each one alone can build anything', 'XOR — true when inputs differ (adders, parity)'],
  'say': ["Here's the full set of basic gates with their symbols. AND outputs one only when both inputs are one. OR outputs one when either is. NOT inverts. NAND and NOR are AND and OR followed by an inverter, and X O R outputs one when its inputs differ, which makes it perfect for adders and parity checks.",
          "NAND and NOR are called universal gates, because you can build every other gate from just one of them. A NAND with its inputs tied together is a NOT. A NAND followed by a NOT is an AND. In C M O S, NAND is also the cheapest and fastest gate to build, so chip designers love it. Chips like this seventy four hundred, with four NAND gates in a fourteen pin package, are what you'd wire up on a breadboard in this course's lab."]},

 {'t': 'v', 'h': 'Boolean algebra: simplifying logic', 'img': 'fig:bool',
  'pts': ['A + A′ = 1 · A·A′ = 0 · A + 1 = 1 · A·1 = A', 'Distributive: AB + AC = A(B + C)', "Example: AB + AB′ + A′B", "= A(B + B′) + A′B = A + A′B = A + B"],
  'say': ["Boolean algebra is the arithmetic of logic, where plus means OR, multiplication means AND, and a prime means NOT. Some rules look like normal algebra, and some don't. A plus not A is always one: something is either true or false. A times not A is always zero. A plus one is one.",
          "The distributive law lets you factor: A B plus A C equals A times B plus C.",
          "Why bother? Because simpler expressions mean fewer gates, which means less area, less power, and more speed. Let's simplify A B plus A B prime plus A prime B.",
          "Factor A out of the first two terms: A times B plus B prime, and B plus B prime is one, so that's just A. Now we have A plus A prime B. A useful identity says that equals A plus B. So three AND gates and an OR gate collapse into a single OR gate. That's a real saving, and the tools that design chips do this kind of simplification millions of times. Why is A plus A prime B equal to A plus B? In Boolean algebra, OR also distributes over AND, which ordinary algebra can't do. So A plus A prime B equals A plus A prime, times A plus B. And A plus A prime is one, leaving A plus B. Or simply check all four rows of the truth table."]},

 {'t': 'v', 'h': 'From a truth table to a circuit', 'img': 'fig:majority',
  'pts': ['Write the truth table', 'OR together the rows where F = 1 (minterms)', 'Simplify', 'Majority vote: F = AB + AC + BC'],
  'say': ["Any logic function can be built straight from its truth table. Here's a majority function: the output is one when at least two of the three inputs are one.",
          "For each row where the output is one, write an AND term that matches exactly that row. These terms are called minterms. Then OR them all together. That's called sum of products form, and it always works.",
          "But it's rarely the simplest. These four minterms simplify down to three terms.",
          "F equals A B plus A C plus B C: any two agreeing inputs win. This isn't just a toy. Spacecraft and aircraft computers use triple modular redundancy: three copies of the same circuit, with a majority voter on the output, so a single fault, like a radiation strike, gets outvoted."]},

 {'t': 'v', 'h': 'Karnaugh maps: simplification by eye', 'img': ['fig:kmap0', 'fig:kmap1', 'fig:kmap2'],
  'say': ["Algebra works, but it's easy to miss a simplification. A Karnaugh map, or K map, makes it visual. Arrange the truth table in a grid with the rows and columns in Gray code order, so that neighboring cells differ by exactly one variable. Here's a four variable function, with ones in eight cells.",
          "Now circle groups of adjacent ones, in sizes that are powers of two. Within a group, any variable that changes drops out. This orange group of four covers rows where B equals one and columns where D equals one, while A and C both change. So the whole group simplifies to just B D.",
          "Here's the trick that surprises everyone: the map wraps around, like a donut. The four corners are all neighbors. They share B equals zero and D equals zero, so they form the group B prime D prime. The final answer is B D plus B prime D prime. Eight minterms with four variables each became two terms with two variables each. And notice that's actually an X N O R of B and D, which you might never have spotted from the equation."]},

 {'t': 'v', 'h': 'Combinational building blocks', 'img': 'fig:blocks',
  'say': "Real designs aren't built gate by gate. They're built from standard blocks. A multiplexer selects one of several inputs using select lines, like a digital switch. A decoder takes an n bit number and activates exactly one of two to the n outputs, which is how memory chooses a row and how a C P U chooses which register to use. An encoder does the reverse. Adders, built from the full adders you'll meet again in the V H D L course, do arithmetic. Comparators check whether two numbers are equal or which is bigger. All of these are combinational: the output depends only on the current inputs. To build a computer, though, we need something more. We need memory."},

 {'t': 'v', 'h': 'Memory from feedback: the SR latch', 'img': 'fig:srlatch',
  'pts': ['Feed outputs back into inputs → the circuit can remember', 'S (set) = 1 → Q = 1', 'R (reset) = 1 → Q = 0', 'S = R = 0 → hold the last value'],
  'say': ["Here's the most important trick in sequential logic: feedback. Take two NOR gates and connect each one's output to the other's input. The orange wires loop back.",
          "Pulse S, the set input, to one, and Q becomes one. Now let S go back to zero. Q stays at one, because the loop holds it there.",
          "Pulse R, the reset input, and Q flips to zero, and again stays there.",
          "With both inputs at zero, the circuit simply holds whatever it last stored. That's one bit of memory, made from two gates. It's called an S R latch. The one forbidden case is setting S and R to one at the same time, which leaves the latch in an undefined state when they're released."]},

 {'t': 'v', 'h': 'Flip-flops, registers and counters', 'img': 'fig:counter',
  'pts': ['D flip-flop: copies D to Q on the clock edge', 'Register: n flip-flops sharing a clock', 'Counter: register + adder (or toggling flip-flops)', 'Each bit toggles at half the rate of the one before'],
  'say': ["Latches respond whenever their inputs change, which makes timing tricky. A flip-flop only updates at the instant the clock rises, the edge. A D flip-flop simply copies its D input to Q on each rising edge, then holds it.",
          "Put n flip-flops side by side with a shared clock and you have a register, which stores an n bit number. Every C P U register is exactly this.",
          "Feed a register's output through an adder that adds one, back into its input, and you have a counter. On every clock edge, the count goes up by one.",
          "Look at the timing diagram. Q zero toggles every clock cycle. Q one toggles at half that rate, and Q two at half again. Read the three bits together and they count zero, one, two, up to seven, then wrap around to zero. That halving is also why a counter makes a perfect clock divider."]},

 {'t': 'v', 'h': 'Memory chips: addresses and data', 'img': 'fig:memory',
  'pts': ['Memory = huge grid of storage cells', 'Address lines pick one word (decoder)', 'n address bits → 2ⁿ words', '2048 × 8 memory: 11 address lines, 8 data lines'],
  'say': ["Scale that up and you get memory chips. A memory is a huge grid of storage cells, organized into words.",
          "To read or write, you send an address. A decoder turns that address into a single selected row, here highlighted in yellow, and that row's bits appear on the data lines.",
          "With n address bits, you can select two to the n words.",
          "Example: a sixteen kilobit memory organized as two thousand forty eight words of eight bits. How many address lines? Two to the eleventh is two thousand forty eight, so eleven. And eight data lines, one per bit. That same arithmetic tells you that a thirty two bit address can reach four gigabytes, which is why older thirty two bit computers couldn't use more than four gigabytes of memory."]},

 {'t': 'v', 'h': 'Putting it together: the structure of a computer', 'img': ['a:i4004_layout', 'fig:cpu'],
  'pts': ['Datapath: registers + ALU', 'Control unit: decodes instructions, drives the datapath', 'Memory holds instructions AND data (von Neumann)', 'Fetch → decode → execute, forever'],
  'say': ["Now we have every piece needed for a computer. This is the layout of the Intel four zero zero four from nineteen seventy one, the first commercial single chip microprocessor, with about two thousand three hundred transistors.",
          "Every processor has the same main parts. The datapath: registers that hold values, and an arithmetic logic unit, the A L U, that adds, subtracts and does logic operations. The control unit is a big state machine that reads each instruction and drives the datapath.",
          "And memory holds both the program's instructions and its data, an arrangement called the von Neumann architecture.",
          "The C P U runs one loop forever. Fetch: read the instruction at the address in the program counter. Decode: figure out what it means. Execute: do it, using the A L U and registers. Then move to the next instruction. A modern processor does this billions of times per second. You'll design one of these yourself, in V H D L, in the computer design course."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Transistors → **gates** → combinational blocks + **flip-flops** → registers, counters, memory → a **computer**.',
  'cap': 'Next: MATH 250A, Calculus III. Later: EGCP 281 (VHDL) and EGCP 381 (Computer Design) build directly on this.',
  'say': "Let's recap the whole tower. Binary and hex represent information. Transistors make gates. Boolean algebra and Karnaugh maps simplify logic into fewer gates. Gates make combinational blocks like multiplexers, decoders and adders. Feedback makes latches and flip-flops, which make registers, counters and memory. And registers, an A L U, memory and a control unit make a computer. Every later digital course builds on this one, so it's worth knowing cold. Next up, Calculus three. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B

def draw_kmap(ax, n, w, h):
    x0, y0, cw, rh = 150, h - 120, 130, 110
    cols = ['00', '01', '11', '10']; ones = {(0, 1), (0, 2), (1, 1), (1, 2), (1, 3)}
    if n >= 1:
        B.lab(ax, x0 - 70, y0 + 40, 'A \\ BC', 26, 'gray')
        for j, c in enumerate(cols): B.lab(ax, x0 + (j + 0.5) * cw, y0 + 30, c, 30, 'blue')
        for i in range(2):
            B.lab(ax, x0 - 40, y0 - (i + 0.5) * rh, str(i), 30, 'blue')
            for j in range(4): B.rect(ax, x0 + j * cw, y0 - (i + 1) * rh, cw, rh, lw=2)
    if n >= 2:
        for i in range(2):
            for j in range(4): B.lab(ax, x0 + (j + 0.5) * cw, y0 - (i + 0.5) * rh, '1' if (i, j) in ones else '0', 36, 'ink' if (i, j) in ones else 'gray')
    if n >= 3:
        B.rect(ax, x0 + cw + 12, y0 - 2 * rh + 12, 2 * cw - 24, 2 * rh - 24, c='green', lw=3.5); B.lab(ax, x0 + 2 * cw, y0 - 2 * rh - 35, 'C', 34, 'green')
    if n >= 4:
        B.rect(ax, x0 + 2 * cw + 22, y0 - 2 * rh + 22, 2 * cw - 44, rh - 44, c='red', lw=3.5); B.lab(ax, x0 + 3.6 * cw, y0 - 2 * rh - 35, 'AB', 34, 'red')
    if n >= 5:
        import schemdraw.logic as lg
        def build(d, elm, v):
            g1 = lg.And().at((0, 0)).anchor('out').right().color(v(5))
            d += g1; d += elm.Line().left(0.6).at(g1.in1).label('A', loc='left').color(v(5)); d += elm.Line().left(0.6).at(g1.in2).label('B', loc='left').color(v(5))
            d += (g2 := lg.Or().at((2.5, -0.7)).anchor('in1').right().color(v(5)))
            d += elm.Wire('-|').at(g1.out).to(g2.in1).color(v(5))
            d += elm.Line().left(3.4).at(g2.in2).label('C', loc='left').color(v(5))
            d += elm.Line().right(0.6).at(g2.out).label('F', loc='right').color(v(5, 'red'))
        sub = ax.inset_axes([0.0, 0.0, 1.0, 0.42]); B.circuit(sub, n, build, fs=26, lw=3)

def draw_counter(ax, n, w, h):
    clk = [0, 1] * 8; edges = 0; q0, q1 = [], []
    for k, c in enumerate(clk):
        if c == 1: edges += 1
        q0.append(edges % 2); q1.append((edges // 2) % 2)
    x0, cw = 110, 62
    if n >= 1: B.wave(ax, x0, h - 160, clk, cw, 80, 'gray', 'clk', fs=34)
    if n >= 2: B.wave(ax, x0, h - 320, q0, cw, 80, 'blue', 'Q0', fs=34)
    if n >= 3: B.wave(ax, x0, h - 480, q1, cw, 80, 'red', 'Q1', fs=34)
    if n >= 4:
        for k in range(8):
            B.lab(ax, x0 + (2 * k + 1.5) * cw, h - 560, str(2 * q1[2 * k + 1] + q0[2 * k + 1]), 40, 'green')
        B.lab(ax, x0 - 14, h - 560, 'count', 30, 'green', ha='right')

B.insert(LESSON, 'Binary and hexadecimal', {'t': 'wb', 'h': 'Worked example: 200 in binary and hex, by hand', 'steps': [
    {'say': "Let's convert the decimal number two hundred to binary, the way you would on an exam. Divide by two over and over, and write down each remainder. Two hundred divided by two is one hundred, remainder zero. One hundred over two is fifty, remainder zero. Fifty over two is twenty five, remainder zero.",
     'w': [{'m': '200 ÷ 2 = 100   remainder 0', 'at': 2}, {'m': '100 ÷ 2 = 50     remainder 0', 'at': 3}, {'m': '50 ÷ 2 = 25       remainder 0', 'at': 4}]},
    {'say': "Twenty five over two is twelve, remainder one. Twelve over two is six, remainder zero. Six over two is three, remainder zero. Three over two is one, remainder one. And one over two is zero, remainder one. We stop at zero.",
     'w': [{'m': '25 ÷ 2 = 12       remainder 1'}, {'m': '12 ÷ 2 = 6         remainder 0', 'at': 1}, {'m': '6 ÷ 2 = 3           remainder 0', 'at': 2}, {'m': '3 ÷ 2 = 1           remainder 1', 'at': 3}, {'m': '1 ÷ 2 = 0           remainder 1', 'at': 4}]},
    {'say': "Now read the remainders from the bottom up: one, one, zero, zero, one, zero, zero, zero. Check it: one twenty eight plus sixty four plus eight is two hundred. Correct.",
     'w': [{'m': 'read upward:  11001000', 'c': 'red', 'box': True, 'gap': 10, 'at': 1}, {'m': 'check: 128 + 64 + 8 = 200', 'c': 'gray', 'at': 2}]},
    {'say': "For hex, split the bits into groups of four. One one zero zero is twelve, which is the hex digit C. One zero zero zero is eight. So two hundred is hex C eight. That's why hex is everywhere in computing: two hex digits are exactly one byte.",
     'w': [{'m': 'hex: group by 4 bits', 'at': 0, 'newcol': True}, {'m': '1100 | 1000', 'at': 1, 'fs': 52}, {'m': '  C    |    8', 'at': 3, 'fs': 52}, {'m': '200 = 0xC8', 'c': 'red', 'box': True, 'at': 3, 'gap': 10}]},
]})

B.insert(LESSON, 'Karnaugh maps', {'t': 'wb', 'h': 'Worked example: a K-map from start to circuit', 'draw': 'kmap', 'split': 0.45, 'steps': [
    {'say': "Here's a complete K-map problem. F of A, B, C is one for minterms one, three, five, six and seven. Draw a two by four map. Rows are A. Columns are B C, in Gray code order: zero zero, zero one, one one, one zero.",
     'w': [{'m': r'$F(A,B,C) = \sum m(1,3,5,6,7)$', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "Fill in the ones. Minterm one is A B C equals zero zero one: row zero, column zero one. Three is zero one one. Five is one zero one. Six is one one zero. And seven is one one one. Everything else is zero.",
     'w': [{'m': 'm1 = 001, m3 = 011, m5 = 101', 'at': 1}, {'m': 'm6 = 110, m7 = 111', 'at': 3}, {'d': 2, 'at': 5}]},
    {'say': "Now circle the biggest groups of ones, in powers of two. The two middle columns form a block of four. In those columns C is always one, while A and B both change. So this group is just C.",
     'w': [{'d': 3, 'at': 1}, {'m': 'group of 4: only C stays constant, so it is C', 'c': 'green', 'at': 2}]},
    {'say': "One one is still uncovered: minterm six. Pair it with seven next to it. In that pair, A is one and B is one, while C changes. So the group is A B.",
     'w': [{'d': 4, 'at': 1}, {'m': 'pair 6, 7: A = 1 and B = 1, so it is AB', 'c': 'red', 'at': 2}]},
    {'say': "So F equals C plus A B. That's one AND gate and one OR gate, instead of five three-input AND gates. The map did the Boolean algebra for us, just by looking. Two exam tips. Make every group as large as possible, and let groups overlap, because a one may be covered more than once. And if some input combinations can never happen, mark them with an X, a don't care, and treat an X as a one whenever it lets you draw a bigger group.",
     'w': [{'m': r'$F = C + AB$', 'c': 'red', 'box': True, 'fs': 48}, {'d': 5, 'at': 1}]},
]})

B.insert(LESSON, 'Flip-flops, registers and counters', {'t': 'wb', 'h': 'Worked example: drawing a 2-bit counter’s timing diagram', 'draw': 'counter', 'split': 0.34, 'steps': [
    {'say': "Let's draw the timing diagram of a two bit counter, the way you would in lab. Start with the clock: a square wave. The flip-flops only act on the rising edges, where the clock goes from low to high.",
     'w': ['2-bit counter', {'m': 'acts on rising edges', 'at': 2}, {'d': 1, 'at': 1}]},
    {'say': "Bit zero is a toggle flip-flop: it flips on every rising edge. So it runs at half the clock frequency.",
     'w': [{'m': 'Q0 toggles on every edge'}, {'d': 2, 'at': 0}, {'m': 'f(Q0) = f(clk) / 2', 'at': 1}]},
    {'say': "Bit one toggles only when bit zero falls from one back to zero. That's every second edge, so it runs at a quarter of the clock frequency.",
     'w': [{'m': 'Q1 toggles when Q0 falls'}, {'d': 3, 'at': 0}, {'m': 'f(Q1) = f(clk) / 4', 'at': 1}]},
    {'say': "Now read the two bits together after each edge, with Q one as the high bit: one, two, three, zero, one, two, three, zero. It counts! And each extra bit halves the frequency again, which is exactly how a clock divider turns one hundred megahertz into one hertz.",
     'w': [{'d': 4, 'at': 0}, {'m': 'count: 1, 2, 3, 0, 1, 2, 3, 0', 'c': 'green', 'at': 1}]},
]})

B.insert(LESSON, 'Memory chips', {'t': 'wb', 'h': 'Worked example: how many address lines?', 'steps': [
    {'say': "Every memory problem starts with the same question: how many address lines? Take a sixty four kilobyte memory, with one byte per address. Sixty four K is sixty four times one thousand twenty four, or sixty five thousand five hundred thirty six bytes.",
     'w': [{'m': r'64 KB $= 64 \times 1024 = 65{,}536$ addresses', 'at': 2}]},
    {'say': "With n address lines, you can name two to the n locations. Two to the sixteenth is sixty five thousand five hundred thirty six. So we need sixteen address lines, A zero through A fifteen.",
     'w': [r'$2^n = 65{,}536 \;\Rightarrow\; n = 16$  lines (A0 to A15)', {'m': 'addresses: 0x0000 to 0xFFFF', 'at': 2}]},
    {'say': "Now suppose we build it from two thirty two kilobyte chips. Each chip needs fifteen lines, A zero to A fourteen. The leftover line, A fifteen, chooses the chip. When A fifteen is zero, the lower chip answers, addresses zero to seven F F F. When it's one, the upper chip answers, eight thousand to F F F F.",
     'w': [{'m': r'two 32 KB chips: each uses A0 to A14 ($2^{15}$)', 'at': 1}, {'m': 'A15 = 0: chip 0, 0x0000 to 0x7FFF', 'c': 'blue', 'at': 3}, {'m': 'A15 = 1: chip 1, 0x8000 to 0xFFFF', 'c': 'orange', 'at': 4}]},
    {'say': "That extra line feeding a chip select is called address decoding. It's how every computer's memory map is built, and you'll see it again in the microcontrollers course.",
     'w': [{'m': 'the top address bit selects the chip: address decoding', 'c': 'red', 'gap': 10}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: 200 in binary and hex'
B.pen(LESSON, G, 2, {'p': ('link',), 'on': '1 ÷ 2 = 0', 'to': '200 ÷ 2 = 100', 'at': 0}, {'p': ('check',), 'on': 'check: 128', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': '1100 | 1000', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': '  C    |    8', 'at': 3})
G = 'Worked example: a K-map from start to circuit'
KX, KW_, KR = 150, 130, 110
cell = lambda i, j, h: (KX + (j + 0.5) * KW_, h - 120 - (i + 0.5) * KR)
B.pen(LESSON, G, 0, {'p': lambda A, w, h: [('underline', KX + 10, KX + 4 * KW_ - 10, h - 120 + 8)], 'c': 'blue', 'at': 3},
      {'p': lambda A, w, h: [('circle', KX + 2.5 * KW_, h - 120 + 30, 42, 26)], 'at': 3})
B.pen(LESSON, G, 1, *[{'p': (lambda i, j: lambda A, w, h: [('circle', *cell(i, j, h), 50, 42)])(i, j), 'at': a, 'solo': a > 1}
                     for a, (i, j) in zip((1, 2, 3, 4, 5), ((0, 1), (0, 2), (1, 1), (1, 2), (1, 3)))])
G = 'Worked example: drawing a 2-bit counter'
CX, CW = 110, 62
B.pen(LESSON, G, 0, {'p': lambda A, w, h: [('arrow', CX + k * CW, h - 215, CX + k * CW, h - 168) for k in (1, 3, 5, 7)], 'at': 2})
B.pen(LESSON, G, 2, {'p': lambda A, w, h: [('circle', CX + k * CW, h - 280, 24, 52) for k in (3, 7, 11, 15)], 'at': 0})
B.pen(LESSON, G, 3, {'p': lambda A, w, h: [('underline', CX, CX + 16 * CW, h - 592)], 'c': 'green', 'at': 0})
G = 'Worked example: how many address lines?'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': '64 KB', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('box',), 'on': 'n = 16', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'A15 = 0', 'c': 'blue', 'at': 3}, {'p': ('circle',), 'on': 'A15 = 1', 'c': 'orange', 'at': 4})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'address decoding', 'at': 0})

# ---------------- the pen on ordinary slides ----------------
S = 'Why digital?'
B.spen(LESSON, S, 0, {'fig': [('box', .14, .07, .83, .43)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .28, .19, .07, .08)], 'at': 3, 'dt': 0.9})
B.spen(LESSON, S, 2, {'fig': [('underline', .17, .84, .70)], 'c': 'blue', 'at': 0, 'dt': 2.5}, {'fig': [('check', .88, .55, 22)], 'c': 'green', 'at': 1, 'dt': 2.0})
S = 'Binary and hexadecimal'
B.spen(LESSON, S, 0, {'fig': [('underline', .06, .98, .27)], 'c': 'blue', 'at': 0, 'dt': 1.5})
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, .23, .045, .05)], 'at': 0, 'dt': t} for x, t in ((.11, 6.3), (.44, 7.2), (.55, 7.8), (.66, 8.4))],
       {'fig': [('underline', .19, .67, .95)], 'c': 'green', 'at': 0, 'dt': 9.5})
B.spen(LESSON, S, 3, {'fig': [('box', .05, .30, .5, .59)], 'c': 'purple', 'at': 0, 'dt': 1.2}, {'fig': [('box', .5, .30, .97, .59)], 'c': 'purple', 'at': 0, 'dt': 3.6},
       {'fig': [('circle', .76, .89, .07, .06)], 'at': 1})
S = 'Codes: BCD, ASCII and Gray code'
B.spen(LESSON, S, 0, {'fig': [('box', .04, .45, .57, .66)], 'c': 'blue', 'at': 4},
       {'fig': [('circle', .26, .505, .06, .045)], 'at': 5, 'dt': 1.8}, {'fig': [('circle', .26, .61, .06, .045)], 'at': 5, 'dt': 2.8},
       {'fig': [('circle', .46, .505, .06, .045)], 'c': 'green', 'at': 7, 'dt': 1.5}, {'fig': [('circle', .46, .61, .06, .045)], 'c': 'green', 'at': 7, 'dt': 2.5},
       {'p': 'underline', 'on': 'neighbors differ in exactly one bit', 'c': 'green', 'at': 8})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'Used in rotary encoders', 'at': 0})
S = 'From transistors to gates'
B.spen(LESSON, S, 0, {'fig': [('circle', .26, .285, .09, .11)], 'c': 'blue', 'at': 3}, {'fig': [('circle', .26, .685, .09, .11)], 'c': 'blue', 'at': 4})
B.spen(LESSON, S, 2, {'fig': [('circle', .43, .49, .06, .04)], 'c': 'orange', 'at': 0, 'dt': 2.5}, {'fig': [('circle', .76, .685, .09, .11)], 'c': 'green', 'at': 1, 'dt': 1.0},
       {'fig': [('circle', .93, .49, .06, .04)], 'c': 'orange', 'at': 1, 'dt': 2.5}, {'p': 'underline', 'on': 'Exactly one is on', 'at': 2})
S = 'The logic gates'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, y, .13, .12)], 'c': c, 'at': a, 'dt': t} for x, y, c, a, t in
       ((.15, .22, 'blue', 1, 0.3), (.48, .22, 'blue', 2, 0.2), (.8, .22, 'blue', 3, 0.2), (.15, .7, 'orange', 4, 0.3), (.48, .7, 'orange', 4, 2.0), (.8, .7, 'green', 4, 4.2))])
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'each one alone can build anything', 'at': 0})
S = 'Boolean algebra'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': 'A + A′ = 1', 'at': 2}, {'p': 'circle', 'on': 'A·A′ = 0', 'at': 3}, {'p': 'circle', 'on': 'A + 1 = 1', 'at': 4})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'AB + AC = A(B + C)', 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'AB + AB′ + A′B', 'at': 2})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'A(B + B′)', 'c': 'blue', 'at': 0}, {'p': 'circle', 'on': 'A + A′B', 'c': 'blue', 'at': 1},
       {'p': 'box', 'on': '= A + B', 'c': 'green', 'at': 2})
S = 'From a truth table to a circuit'
B.spen(LESSON, S, 1, {'fig': [('box', .03, .46, .35, .545)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .45, .96, .37)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('box', .52, .6, .89, .72)], 'c': 'green', 'at': 0})
S = 'Combinational building blocks'
B.spen(LESSON, S, 0, *[{'fig': [('box', x0, .23, x1, .59)], 'c': 'blue', 'at': a, 'dt': .3} for x0, x1, a in
       ((.01, .2, 2), (.21, .39, 3), (.41, .59, 4), (.61, .79, 5), (.8, .99, 6))])
S = 'Memory from feedback'
B.spen(LESSON, S, 0, {'fig': [('circle', .45, .47, .17, .15)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .1, .74, .04, .06)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .73, .25, .045, .06)], 'c': 'green', 'at': 0, 'dt': 1.8})
B.spen(LESSON, S, 2, {'fig': [('circle', .1, .23, .04, .06)], 'at': 0})
S = 'Flip-flops, registers and counters'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'copies D to Q on the clock edge', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('box', .14, .22, .98, .37)], 'c': 'orange', 'at': 1}, {'fig': [('box', .14, .4, .98, .56)], 'c': 'green', 'at': 2},
       {'fig': [('box', .14, .58, .98, .73)], 'c': 'purple', 'at': 2, 'dt': 2.0}, {'fig': [('box', .14, .77, .98, .91)], 'c': 'blue', 'at': 3})
S = 'Memory chips'
B.spen(LESSON, S, 1, {'fig': [('box', .29, .41, .87, .54)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': '2ⁿ words', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': '11 address lines', 'c': 'green', 'at': 2}, {'fig': [('circle', .12, .85, .07, .045)], 'c': 'green', 'at': 2, 'dt': 1.2})
S = 'Putting it together: the structure of a computer'
B.spen(LESSON, S, 1, {'fig': [('box', .31, .28, .55, .49)], 'c': 'blue', 'at': 1}, {'fig': [('box', .17, .59, .43, .8)], 'c': 'green', 'at': 1, 'dt': 2.5},
       {'fig': [('box', .06, .28, .3, .49)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .69, .1, .97, .83)], 'at': 0})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Fetch → decode → execute, forever', 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Worked example: 200 in binary and hex, by hand', {'t': 'wb', 'h': "Negative numbers: two's complement", 'fs': 48, 'cfs': 44, 'steps': [
    {'say': "Hardware has no minus sign, so how does a computer store negative five? Almost every computer uses two's complement. The trick: in eight bits, the top bit's place value isn't plus one twenty eight. It's minus one twenty eight. Everything else stays positive.",
     'w': [{'k': 'weights:  -128  64  32  16   8   4   2   1', 'lang': 'plain', 'at': 3}]},
    {'say': "To negate a number, invert every bit, then add one. Five is zero zero zero zero zero one zero one. Invert: one one one one one zero one zero. Add one: one one one one one zero one one. That's negative five.",
     'w': [{'k': ' 5      =  0000 0101', 'lang': 'plain', 'at': 1}, {'k': 'invert  =  1111 1010', 'lang': 'plain', 'at': 2},
           {'k': '+1      =  1111 1011   = -5', 'lang': 'plain', 'at': 3}]},
    {'say': "Check it with the weights: minus one twenty eight, plus sixty four, thirty two, sixteen, eight, two and one. That's minus five. And here's the beautiful part. Add five and negative five with an ordinary binary adder. Every column carries, and the final carry falls off the end of the eight bits, leaving zero.",
     'w': [{'m': r'$-128 + 64 + 32 + 16 + 8 + 2 + 1 = -5$', 'c': 'green', 'at': 1},
           {'k': '   0000 0101   (5)', 'lang': 'plain', 'at': 3, 'gap': 14}, {'k': ' + 1111 1011  (-5)', 'lang': 'plain', 'at': 3},
           {'k': ' 1 0000 0000   -> drop carry -> 0', 'lang': 'plain', 'at': 4}]},
    {'say': "So the same adder circuit does subtraction: a minus b is just a plus negative b. That's why everyone uses this format. Eight bits hold minus one twenty eight up to plus one twenty seven. Add one to one twenty seven, and you get one zero zero zero zero zero zero zero, which is minus one twenty eight. That's the integer overflow from the programming course: the wheel wraps around.",
     'w': [{'m': 'subtract = add the negative', 'c': 'blue', 'at': 0, 'gap': 10}, {'m': 'range (8 bits):  −128 … +127', 'at': 2},
           {'k': '0111 1111 + 1 = 1000 0000   127 + 1 = -128 !', 'lang': 'plain', 'at': 3}]},
]})

G = "Negative numbers: two's complement"
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'weights:', 'cols': (10, 14), 'at': 3})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'invert  =', 'c': 'blue', 'at': 2}, {'p': ('box',), 'on': '+1      =', 'c': 'red', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': ' 1 0000 0000', 'cols': (1, 2), 'at': 4})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '0111 1111 + 1', 'cols': (28, 43), 'c': 'red', 'at': 3})
