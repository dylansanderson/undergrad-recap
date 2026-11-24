import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_supply(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    st = ['3rd-party\nIP cores', 'EDA tools', 'design\nhouse', 'foundry\n(offshore)', 'test &\nassembly', 'distributors', 'your\nproduct']
    for i, s in enumerate(st):
        x = 1 + i * 14.1; box(ax, x, 18, 12.5, 12, s, fc=C['lred'] if i in (0, 1, 3, 4, 5) else C['lgreen'], ec=C['red'] if i in (0, 1, 3, 4, 5) else C['green'], fs=12, bold=True, r=0.4)
        if i < 6: arrow(ax, (x + 12.5, 24), (x + 14.1, 24), lw=2, ms=11)
    txt(ax, 50, 40, 'every red step is a party you must trust', 17, C['red'], bold=True)
    txt(ax, 50, 8, 'threats: Trojans · overproduction · cloning · recycled & remarked chips\nand unlike software, silicon can’t be patched', 15, C['mut'])
    save(fig, path)

def fig_trojan(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    box(ax, 4, 30, 30, 20, 'original\ncircuit', fc=C['lblue'], fs=18, bold=True)
    g1 = gate(ax, 'and', 48, 41, 12, n_in=3)
    for i, (n, p) in enumerate(zip(('n12', 'n27', 'n33'), g1['in'])): line(ax, [(34, p[1]), p], C['gray'], 1.8); txt(ax, 39, p[1] + 1.4, n, 12, C['mut'])
    txt(ax, 76, 49, 'TRIGGER: rare pattern\n(all three = 1, p ≈ 10⁻⁶)\nor a counter reaching N', 13, C['red'], bold=True)
    g2 = gate(ax, 'xor', 70, 18, 12)
    o1 = g1['out']; line(ax, [o1, (66, o1[1]), (66, g2['in'][0][1]), g2['in'][0]], C['red'], 2.4)
    line(ax, [(34, 34), (40, 34), (40, g2['in'][1][1]), g2['in'][1]], C['ink'], 2.4); txt(ax, 42, g2['in'][1][1] + 2, 'normal output', 13, C['mut'], ha='left')
    o2 = g2['out']; line(ax, [o2, (95, o2[1])], C['red'], 2.6); txt(ax, 88, o2[1] - 6, 'PAYLOAD:\noutput flipped', 13, C['red'], bold=True)
    txt(ax, 50, 3, 'functional tests almost never hit the trigger → the Trojan stays hidden', 15, C['mut'])
    save(fig, path)

def fig_lock(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    g = gate(ax, 'xor', 32, 24, 14)
    line(ax, [(6, g['in'][0][1]), g['in'][0]], C['ink'], 2.4); txt(ax, 6, g['in'][0][1] + 2.5, 'internal wire', 14, C['mut'], ha='left')
    line(ax, [(20, g['in'][1][1]), g['in'][1]], C['orange'], 2.4); txt(ax, 18, g['in'][1][1], 'key bit K', 15, C['orange'], ha='right', bold=True)
    line(ax, [g['out'], (62, g['out'][1])], C['ink'], 2.4); txt(ax, 64, g['out'][1], 'K = 0 → correct\nK = 1 → inverted (wrong)', 15, ha='left')
    txt(ax, 50, 41, 'logic locking: the chip only works after the secret key is loaded', 16, bold=True)
    txt(ax, 50, 6, 'attack: SAT solver + a working chip as an oracle prunes wrong keys → Anti-SAT, SFLL defenses', 14, C['mut'])
    save(fig, path)

def fig_spa(path, w, h):
    fig, ax = plot(w, h)
    key = '1011001'; t = []; lab = []; x = 0
    rng = np.random.default_rng(1)
    for b in key:
        seg = np.ones(30) * 1.0 + rng.normal(0, 0.05, 30); t.append(seg); lab.append((x + 15, 'S'));  x += 30
        t.append(np.ones(8) * 0.2 + rng.normal(0, 0.03, 8)); x += 8
        if b == '1':
            seg = np.ones(30) * 1.6 + rng.normal(0, 0.05, 30); t.append(seg); lab.append((x + 15, 'M')); x += 30; t.append(np.ones(8) * 0.2 + rng.normal(0, 0.03, 8)); x += 8
    tr = np.concatenate(t); ax.plot(tr, color=C['blue'], lw=1.6)
    for xx, l in lab: ax.text(xx, 1.85 if l == 'M' else 1.25, l, ha='center', fontsize=14, color=C['orange'] if l == 'M' else C['ink'], fontweight='bold')
    ax.set_yticks([]); ax.set_xticks([]); ax.set_ylim(0, 2.1); ax.set_xlabel('time →')
    ax.set_title('SPA on square-and-multiply: “S M” = key bit 1, “S” alone = 0 → key 1011001', fontsize=16)
    save(fig, path)

def fig_cpa(path, w, h):
    fig, ax = plot(w, h)
    rng = np.random.default_rng(7); sbox = rng.permutation(256); hw = np.array([bin(v).count('1') for v in range(256)])
    p = rng.integers(0, 256, 2000); k = 0x3C
    leak = hw[sbox[p ^ k]] + rng.normal(0, 1.5, p.size)
    corr = np.array([np.corrcoef(hw[sbox[p ^ g]], leak)[0, 1] for g in range(256)])
    ax.bar(np.arange(256), corr, color=[C['orange'] if g == k else C['gray'] for g in range(256)], width=1.0)
    ax.annotate('correct key byte 0x3C', (k, corr[k]), (k + 30, corr[k] * 0.95), fontsize=16, color=C['orange'], arrowprops=dict(arrowstyle='->', color=C['orange']))
    ax.set_xlabel('key-byte guess'); ax.set_ylabel('correlation with power'); ax.set_xlim(-2, 258)
    ax.set_title('CPA: 2,000 power traces vs. a Hamming-weight model — one guess stands out', fontsize=16)
    save(fig, path)

def fig_hamming(path, w, h):
    fig, ax, H = canvas(w, h, need=59, exact=True)          # the bit-position labels at y = 56 touched the top edge
    pos = ['1\np1', '2\np2', '3\nd1', '4\np4', '5\nd2', '6\nd3', '7\nd4']; sent = '0110011'; recv = '0110001'
    txt(ax, 6, 49, 'sent', 17, ha='left', bold=True); txt(ax, 6, 31, 'received', 17, ha='left', bold=True)
    for i in range(7):
        x = 24 + i * 10; txt(ax, x + 4, 56, pos[i], 12, C['mut'])
        box(ax, x, 45, 8, 8, sent[i], fc=C['lorange'] if pos[i][-2] == 'p' else C['lblue'], ec=C['gray'], fs=19, bold=True, r=0.3)
        bad = i == 5; box(ax, x, 27, 8, 8, recv[i], fc=C['lred'] if bad else 'white', ec=C['red'] if bad else C['gray'], fs=19, bold=True, r=0.3)
    txt(ax, 50, 40, 'data 1011 → parity bits at positions 1, 2, 4', 14, C['mut'])
    txt(ax, 6, 16, 's1 (1,3,5,7) = 0    s2 (2,3,6,7) = 1    s4 (4,5,6,7) = 1', 16, ha='left', family='Consolas')
    txt(ax, 6, 7, 'syndrome s4 s2 s1 = 110₂ = 6 → flip bit 6 → corrected!', 18, C['green'], ha='left', bold=True)
    save(fig, path)

def fig_stuck(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    g1 = gate(ax, 'and', 22, 28, 14); g2 = gate(ax, 'or', 54, 20, 14)
    for p, t in zip(g1['in'], ('a=1', 'b=1')): line(ax, [(10, p[1]), p], C['ink'], 2.4); txt(ax, 8, p[1], t, 15, ha='right')
    o = g1['out']; line(ax, [o, (46, o[1]), (46, g2['in'][0][1]), g2['in'][0]], C['red'], 2.6); txt(ax, 44, o[1] + 2.5, 'stuck-at-0', 14, C['red'], bold=True)
    line(ax, [(10, g2['in'][1][1]), g2['in'][1]], C['ink'], 2.4); txt(ax, 8, g2['in'][1][1], 'c=0', 15, ha='right')
    line(ax, [g2['out'], (78, g2['out'][1])], C['ink'], 2.4); txt(ax, 89, g2['out'][1], 'good: y=1\nfaulty: y=0', 16, C['green'], bold=True)
    txt(ax, 50, 41, 'test vector (1,1,0) ACTIVATES the fault and PROPAGATES it to y', 16, bold=True)
    txt(ax, 50, 4, 'fault coverage = detected faults / total faults · scan chains make flip-flops testable', 14, C['mut'])
    save(fig, path)

LESSON = {
 'code': 'EGCP 447', 'title': 'Cyber-Physical Systems Security', 'tag': 'Year 4 · Security', 'folder': 'EGCP-447 Cyber-Physical Systems Security',
 'slides': [
 {'t': 'title', 'h': 'Hardware & Cyber-Physical Systems Security', 'sub': 'Trojans, counterfeits, IP protection, side channels, testing, error correction and IoT', 'img': 'a:smartcard',
  'say': "Welcome to E G C P four forty seven, introduction to cyber physical systems security, with a focus on hardware. Most security courses assume the hardware is trustworthy and defend the software. This course asks what happens when the chip itself is the problem: when it was modified by someone in the supply chain, when it's a counterfeit, or when its power consumption leaks the secret key on a credit card chip like this one. You'll learn how these attacks work, how engineers detect them, and how to design hardware that resists them."},

 {'t': 'v', 'h': 'Why hardware security?', 'img': 'fig:supply',
  'pts': ['Chips pass through many untrusted hands', 'Malicious logic, overproduction, cloning, recycling', 'Hardware flaws can’t be patched like software', 'Physical access enables new attacks'],
  'say': "A modern chip passes through many hands before it reaches a product. Designers license third party I P cores, use commercial design tools, send the layout to a foundry that is often overseas, then to separate test and assembly houses, then through distributors. Every one of those steps is a party you have to trust. Any of them could insert hidden malicious logic, manufacture extra chips to sell on the side, clone the design, or sell old chips pulled from electronic waste as new. And unlike software, you can't push an update to fix silicon. A flaw in the hardware is there for the life of the product. Finally, cyber physical systems, like cars, medical devices and power grid controllers, are often physically accessible, which opens attacks that never apply to a server in a locked data center."},

 {'t': 'v', 'h': 'Hardware Trojans: trigger + payload', 'img': 'fig:trojan',
  'pts': ['Trigger: rare input pattern, counter, or physical condition', 'Payload: flip outputs, leak secrets, deny service', 'Designed to escape functional testing', 'Detection: rare-node testing, side-channel fingerprints, reverse engineering'],
  'say': ["A hardware Trojan is a malicious modification to a circuit. It has two parts. The trigger decides when it activates, and it's designed to be rare: here, three internal nodes that are almost never all one at the same time, perhaps a one in a million event. A sequential trigger might instead count events, activating only after the thousandth occurrence.",
          "The payload is what it does: flip an output, as this X O R gate does, leak a secret key through an unused pin or a subtle power pattern, shut the chip down, or quietly reduce its reliability.",
          "Because the trigger is so rare, ordinary functional testing almost never activates it. The Trojan sits silently through verification and manufacturing tests. In this course, students design Trojans themselves, including a counter triggered Trojan inserted into a standard benchmark circuit in V H D L, to understand exactly why they're hard to find.",
          "Detection methods include test generation that deliberately drives rarely activated nodes, comparing a chip's power and timing fingerprint against a trusted golden chip, and in the extreme, destructively reverse engineering samples layer by layer. Prevention includes design for trust techniques and on chip monitors."]},

 {'t': 'v', 'h': 'Counterfeit chips', 'img': 'a:fake_sd',
  'pts': ['Recycled, remarked, overproduced, out-of-spec, cloned', 'Detect: X-ray, decapsulation, electrical tests, aging sensors', 'PUFs: chip fingerprints from manufacturing variation', 'Buy through trusted, authorized supply chains'],
  'say': "Counterfeits are a huge problem, especially for military and aerospace systems that need parts long after they're out of production. These microSD cards were opened up by a researcher: from the outside they look similar, but the dies inside reveal genuine, questionable and fake parts. Counterfeits come in many forms: recycled chips pulled from old boards and sanded and remarked as new, chips remarked as a faster or higher temperature grade, overproduced chips sold out the back door of a foundry, out of spec rejects, and outright clones. Detection uses physical inspection, X rays, decapsulation, electrical testing, and on chip aging sensors that reveal a used part. A powerful defense is the physically unclonable function, or PUF. Tiny random manufacturing variations make every chip slightly different, for example in which way each S RAM cell settles at power up, or which of two identical ring oscillators runs faster. That gives each chip a fingerprint that even the manufacturer can't copy, usable for authentication and for generating keys."},

 {'t': 'v', 'h': 'Protecting the design: locking, camouflage, split manufacturing', 'img': 'fig:lock',
  'pts': ['Logic locking: key gates; chip works only with the secret key', 'SAT attack breaks naive locking → Anti-SAT, SFLL', 'Camouflaging: look-alike cells defeat image-based RE', 'Split manufacturing: untrusted fab never sees the full design'],
  'say': ["How do you stop a foundry from overproducing or pirating your design? Logic locking inserts extra key gates, like an X O R on an internal wire. With the correct key bit, the signal passes unchanged. With the wrong one, it's inverted. Insert a hundred and twenty eight of these, load the key into tamper resistant memory only after manufacturing, and the foundry holds a chip that doesn't work.",
          "Researchers found a powerful attack: if you have one working chip as an oracle, a SAT solver can choose inputs that eliminate large groups of wrong keys at a time, recovering the key surprisingly quickly. That led to SAT resistant schemes like Anti SAT and S F L L, a classic attack and defense arms race.",
          "Camouflaging uses cells that look identical under a microscope but implement different functions, defeating reverse engineering from layout images.",
          "And split manufacturing sends the transistor layers and lower wiring to an untrusted foundry, and adds the top metal layers at a trusted one, so the untrusted foundry never sees how the circuit is actually connected."]},

 {'t': 'v', 'h': 'Side-channel attacks: power and timing', 'img': ['fig:spa', 'fig:cpa'],
  'pts': ['Secrets leak through power, timing, EM, even sound', 'SPA: read operations straight off one trace', 'DPA/CPA: statistics over many traces → AES key', 'Defenses: constant time, masking, hiding'],
  'say': ["Side channel attacks don't break the math. They watch the hardware. Every operation draws a slightly different amount of power and takes a slightly different time. Here's simple power analysis on R S A implemented with square and multiply. For each key bit, the chip squares, and if the bit is one, it also multiplies. On a single power trace, the pattern is visible: square multiply means one, square alone means zero. You can literally read the key off the oscilloscope.",
          "Differential and correlation power analysis are subtler and more powerful. Collect thousands of traces while the chip encrypts known inputs. For each guess of one key byte, predict the power the chip should draw, using the Hamming weight of an intermediate value, and correlate the prediction with the measurements. Wrong guesses give near zero correlation, the right guess stands out clearly, here hex three C. Repeat for each byte and you have the whole A E S key. Defenses include constant time code, masking, which randomizes intermediate values so they don't correlate with the key, and hiding, which adds noise or shuffles operations. Fault injection, glitching the clock or voltage, and timing attacks on caches, like Spectre and Meltdown, belong to the same family."]},

 {'t': 'v', 'h': 'Testing: stuck-at faults and test vectors', 'img': 'fig:stuck',
  'pts': ['Model: any net stuck at 0 or stuck at 1', 'A test must activate the fault and propagate it', 'Fault coverage = detected / total faults', 'Scan chains: testable — and an attack surface'],
  'say': ["Security and manufacturing test share tools. To check that a chip was built correctly, engineers use the stuck at fault model: assume any wire might be stuck permanently at zero or one.",
          "A test vector detects a fault only if it activates the fault, driving the wire to the opposite value, and propagates the difference to an output you can observe. Here, to test the AND gate's output stuck at zero, set a and b to one so the good circuit produces a one there, and c to zero so the OR gate doesn't mask it. The good circuit outputs one, the faulty circuit outputs zero. Detected.",
          "Automatic test pattern generators find small sets of vectors that cover nearly all possible faults, and fault coverage measures the fraction detected. In this course's first homework, students identify fault sites and test vectors for a small circuit.",
          "For sequential chips, scan chains link all the flip flops into a long shift register, so testers can load and read internal state directly. But that same access lets an attacker dump the internal state of a crypto engine, so secure chips lock down or scramble their scan chains."]},

 {'t': 'v', 'h': 'Error-correcting codes: Hamming (7,4)', 'img': 'fig:hamming',
  'pts': ['4 data bits + 3 parity bits at positions 1, 2, 4', 'Parity bit k covers positions with bit k set', 'Syndrome = position of a single-bit error', 'SECDED (ECC RAM) adds an overall parity bit'],
  'say': ["Not every error is malicious. Radiation, noise and aging flip bits too, and error correcting codes fix them. The classic is the Hamming seven four code. Four data bits are placed at positions three, five, six and seven, and three parity bits at the power of two positions one, two and four.",
          "Each parity bit covers the positions whose binary index has that bit set. Parity one covers one, three, five and seven. Parity two covers two, three, six and seven. Parity four covers four through seven. To send data one zero one one, the parity bits come out zero, one and zero, giving the codeword zero one one zero zero one one.",
          "Now suppose bit six flips in transit. The receiver recomputes the three parity checks. Check one passes, checks two and four fail, so the syndrome, read as a binary number, is one one zero: six. The syndrome literally points at the bad bit, so the receiver flips it back. If the syndrome is zero, there was no error.",
          "Hamming codes correct any single bit error, or detect two. Adding one more overall parity bit gives SECDED, single error correct, double error detect, which is exactly what E C C memory in servers uses. In this course's project, students implement a Hamming encoder and decoder in V H D L."]},

 {'t': 'v', 'h': 'IoT security', 'img': 'a:ip_camera',
  'pts': ['Constrained devices, long lifetimes, physical access', 'Mirai (2016): default passwords → huge botnet', 'Secure boot + root of trust + hardware crypto', 'PUF keys, signed updates, network segmentation'],
  'say': "The internet of things puts small computers everywhere: cameras, thermostats, door locks, medical devices, factory sensors. They're hard to secure. They have little processing power or energy for heavy cryptography, they stay deployed for years, often with no update mechanism, and attackers can get their hands on them physically. In two thousand sixteen, the Mirai malware scanned the internet for cameras and routers still using factory default passwords, took over hundreds of thousands of them, and used them to launch some of the largest denial of service attacks ever seen, knocking major websites offline. The defenses start in hardware: secure boot, which only runs firmware signed by the manufacturer, anchored in an immutable root of trust; hardware crypto accelerators; keys derived from PUFs instead of stored in memory; signed over the air updates; lightweight cryptography; and network segmentation so a compromised camera can't reach anything important. A term paper in this course explores hardware Trojans in IoT devices specifically."},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Hardware is part of the attack surface: **trust the supply chain carefully**, assume **physical leakage**, and build security in from the **root of trust**.',
  'cap': 'Next: EGCP 470, Senior Design I — planning a real engineering project.',
  'say': "To recap. Chips pass through many untrusted hands, and hardware can't be patched. Hardware Trojans hide behind rare triggers. Counterfeits are detected by inspection, testing and PUF fingerprints. Logic locking, camouflaging and split manufacturing protect designs, while SAT attacks keep defenders honest. Side channels leak keys through power and timing, countered by constant time code, masking and hiding. Stuck at fault testing and Hamming codes catch accidental errors, and IoT security starts with secure boot and a hardware root of trust. Next, senior design. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B

def draw_ham(ax, n, w, h):
    code = [0, 1, 1, 0, 0, 1, 1]; nm = ['p1', 'p2', 'd1', 'p4', 'd2', 'd3', 'd4']
    x0, u, y = 40, 108, h - 200
    for k in range(7):
        par = nm[k][0] == 'p'
        if n >= 1:
            B.lab(ax, x0 + k * u + u / 2, y + 120, str(k + 1), 24, 'gray'); B.lab(ax, x0 + k * u + u / 2, y + 80, nm[k], 26, 'orange' if par else 'blue')
        if n >= (1 if not par else 2):
            B.node(ax, x0 + k * u, y - 40, u - 8, 90, str(code[k]), fc='#f6d6c4' if par else '#dfe8f7', fs=40)
        if n >= 3:
            r = code[k] ^ (1 if k == 5 else 0)
            B.node(ax, x0 + k * u, y - 260, u - 8, 90, str(r), fc='#f6c9c4' if k == 5 else 'white', fs=40, c='red' if k == 5 else 'ink')
    if n >= 3: B.lab(ax, x0 + 3.5 * u, y - 110, 'received (one bit flipped by noise)', 24, 'red')
    if n >= 4: B.arr(ax, x0 + 5.5 * u, y - 330, x0 + 5.5 * u, y - 280, 'red', 3, 22); B.lab(ax, x0 + 5.5 * u, y - 360, 'position 6!', 28, 'red')

def draw_stuck(ax, n, w, h):
    import schemdraw.logic as lg
    def build(d, elm, v):
        d += (g1 := lg.And().at((0, 0)).color(v(1)))
        d += elm.Label().at(g1.in1).label('A', loc='left').color(v(1)); d += elm.Label().at(g1.in2).label('B', loc='left').color(v(1))
        d += elm.Line().at(g1.out).right(0.8).color(v(1)); d += (k := elm.Dot().color(v(1)))
        d += (g2 := lg.Or().anchor('in1').at(k.center).color(v(1)))
        d += elm.Line().at(g2.in2).left(0.4).color(v(1)); d += elm.Line().down(1.4).color(v(1))
        d += (cw := elm.Line().left().tox(g1.in2[0]).color(v(1))); d += elm.Label().label('C', loc='left').color(v(1))
        d += elm.Line().at(g2.out).right(0.6).color(v(1)); d += elm.Label().label('F', loc='right').color(v(1))
        d += elm.Label().at((k.center[0] - 0.2, k.center[1] + 0.6)).label('stuck-at-0 ?').color(v(2, 'red'))
        d += elm.Label().at((g1.in1[0] - 0.9, g1.in1[1] + 0.05)).label('1').color(v(3, 'blue'))
        d += elm.Label().at((g1.in2[0] - 0.9, g1.in2[1] - 0.05)).label('1').color(v(3, 'blue'))
        d += elm.Label().at((cw.end[0] - 0.9, cw.end[1])).label('0').color(v(3, 'blue'))
        d += elm.Label().at((g2.out[0] + 0.6, g2.out[1] + 0.6)).label('good 1 / bad 0').color(v(4, 'red'))
    B.circuit(ax, n, build, fs=26, lw=3)

def draw_lock(ax, n, w, h):
    import schemdraw.logic as lg
    def build(d, elm, v):
        d += (g := lg.And().at((0, 0)).color(v(1)))
        d += elm.Label().at(g.in1).label('A', loc='left').color(v(1)); d += elm.Label().at(g.in2).label('B', loc='left').color(v(1))
        d += elm.Line().at(g.out).right(0.6).color(v(1))
        d += (x := lg.Xor().anchor('in1').color(v(2, 'red')))
        d += elm.Line().at(x.in2).left(0.5).color(v(2, 'red')); d += elm.Line().down(1.2).color(v(2, 'red'))
        d += elm.Dot(open=True).label('key K', loc='bottom').color(v(2, 'red'))
        d += elm.Line().at(x.out).right(0.8).color(v(1)); d += elm.Label().label('F', loc='right').color(v(1))
    B.circuit(ax, n, build, fs=28, lw=3)

B.insert(LESSON, 'Error-correcting codes', {'t': 'wb', 'h': 'Worked example: Hamming(7,4) finds and fixes a flipped bit', 'draw': 'ham', 'split': 0.5, 'steps': [
    {'say': "Protect the four data bits one zero one one. Put them in positions three, five, six and seven. Positions one, two and four, the powers of two, will hold parity bits.",
     'w': [{'m': 'data: 1011', 'at': 0}, {'m': 'parity at positions 1, 2, 4', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Each parity bit makes its group even. P one covers positions one, three, five and seven: data one, zero, one, so p one is zero. P two covers two, three, six, seven: one, one, one, so p two is one. P four covers four through seven: zero, one, one, so p four is zero.",
     'w': [{'m': 'p1: 1,3,5,7  (1+0+1)  p1 = 0', 'at': 1}, {'m': 'p2: 2,3,6,7  (1+1+1)  p2 = 1', 'at': 2}, {'m': 'p4: 4,5,6,7  (0+1+1)  p4 = 0', 'at': 3}, {'d': 2, 'at': 3}]},
    {'say': "Send zero one one zero zero one one. Noise flips position six. The receiver gets zero one one zero zero zero one.",
     'w': [{'m': 'sent 0110011, received 0110001', 'c': 'red', 'at': 1}, {'d': 3, 'at': 1}]},
    {'say': "The receiver rechecks each group. Group one: even, so s one is zero. Group two: odd, s two is one. Group four: odd, s four is one. Read the checks as binary, s four s two s one: one one zero, which is six. The syndrome is the exact position of the error. Flip bit six back, and the data is recovered with no retransmission.",
     'w': [{'m': 's1 = 0,  s2 = 1,  s4 = 1', 'at': 0}, {'m': 'syndrome = 110 = 6: flip bit 6', 'c': 'red', 'box': True, 'at': 2}, {'d': 4, 'at': 3}]},
]})

B.insert(LESSON, 'Testing: stuck-at faults', {'t': 'wb', 'h': 'Worked example: finding a test vector for a stuck-at fault', 'draw': 'stuck', 'split': 0.44, 'steps': [
    {'say': "Here's a tiny circuit: F equals A and B, or C. Suppose a manufacturing defect shorts the AND gate's output to ground. That's a stuck at zero fault. Which input pattern will reveal it?",
     'w': [{'m': r'$F = AB + C$', 'at': 0}, {'d': 1, 'at': 0}, {'d': 2, 'at': 1}]},
    {'say': "Two jobs. First, activate the fault: drive the faulty wire to the opposite of its stuck value. To make the AND output one, A and B must both be one. Second, propagate it: make the difference visible at F. The OR gate passes its first input through only if its other input is zero, so C must be zero.",
     'w': [{'m': 'activate: AND output = 1  so A = B = 1', 'c': 'blue', 'at': 1}, {'m': 'propagate: C = 0 (non-controlling)', 'c': 'blue', 'at': 3}, {'d': 3, 'at': 3}]},
    {'say': "So the test vector is A B C equals one one zero. A good chip outputs one; the faulty chip outputs zero. Different answers, so the tester catches it. Automatic test pattern generators do exactly this reasoning, for millions of wires, before a chip ships.",
     'w': [{'m': 'test vector ABC = 110', 'c': 'red', 'box': True, 'at': 0}, {'d': 4, 'at': 1}]},
]})

B.insert(LESSON, 'Protecting the design', {'t': 'wb', 'h': 'Worked example: logic locking with a key gate', 'draw': 'lock', 'split': 0.5, 'steps': [
    {'say': "Logic locking hides a design from an untrusted factory. Start with a simple function: F equals A and B.",
     'w': [{'m': r'original: $F = AB$', 'at': 0}, {'d': 1, 'at': 0}]},
    {'say': "Insert an XOR gate on the wire, with a secret key bit as its other input. With K equals zero, XOR passes the signal unchanged: the chip works. With K equals one, the output is inverted: the chip computes garbage.",
     'w': [{'d': 2, 'at': 0}, {'m': r'K = 0:  $F = AB$  correct', 'c': 'green', 'at': 1}, {'m': r'K = 1:  $F = \overline{AB}$  wrong', 'c': 'red', 'at': 2}]},
    {'say': "The key is programmed into tamper-proof memory only after the chip returns from the foundry. A real design uses a hundred or more key gates, so guessing means two to the hundred twenty eight possibilities. Researchers then try clever attacks, like the SAT attack, which is why this is still an active research area.",
     'w': [{'m': r'128 key gates: $2^{128}$ guesses', 'at': 1}, {'m': 'but: SAT attacks, so research continues', 'c': 'gray', 'at': 2}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: Hamming(7,4) finds and fixes a flipped bit'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'p1: 1,3,5,7', 'c': 'blue', 'at': 1, 'solo': False}, {'p': ('underline',), 'on': 'p2: 2,3,6,7', 'c': 'blue', 'at': 2},
      {'p': ('underline',), 'on': 'p4: 4,5,6,7', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'received 0110001', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 's1 = 0', 'c': 'blue', 'at': 1}, {'p': ('check',), 'on': 'syndrome = 110', 'c': 'green', 'at': 4})
G = 'Worked example: finding a test vector for a stuck-at fault'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'activate:', 'at': 1}, {'p': ('underline',), 'on': 'propagate:', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'test vector ABC = 110', 'c': 'green', 'at': 2})
G = 'Worked example: logic locking with a key gate'
B.pen(LESSON, G, 1, {'p': ('check',), 'on': 'K = 0:', 'c': 'green', 'at': 1}, {'p': ('cross',), 'on': 'K = 1:', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '128 key gates', 'at': 1})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Why hardware security'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, .47, .07, .15)], 'c': 'red', 'at': 1, 'dt': t} for x, t in ((.07, 0), (.21, 1.5), (.49, 3.5), (.64, 5.5), (.78, 7.0))],
       {'fig': [('underline', .14, .86, .82)], 'c': 'red', 'at': 3}, {'fig': [('underline', .27, .73, .87)], 'c': 'purple', 'at': 4})
S = 'Hardware Trojans'
B.spen(LESSON, S, 0, {'fig': [('box', .33, .17, .6, .37)], 'c': 'red', 'at': 2}, {'fig': [('underline', .62, .88, .23)], 'c': 'red', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .78, .67, .1, .11)], 'c': 'red', 'at': 0}, {'fig': [('underline', .75, .97, .84)], 'c': 'red', 'at': 0, 'dt': 1.5})
B.spen(LESSON, S, 2, {'fig': [('arrow', .3, .73, .65, .7)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .14, .86, .97)], 'c': 'blue', 'at': 1})
S = 'Protecting the design'
B.spen(LESSON, S, 0, {'fig': [('circle', .38, .5, .1, .14)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .14, .55, .08, .06)], 'c': 'orange', 'at': 1, 'dt': 2.0},
       {'fig': [('underline', .64, .88, .47)], 'c': 'green', 'at': 2}, {'fig': [('underline', .64, .9, .53)], 'c': 'red', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('underline', .06, .94, .85)], 'c': 'purple', 'at': 0})
S = 'Side-channel attacks'
B.spen(LESSON, S, 0, {'fig': [('circle', .19, .42, .025, .04)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .25, .2, .03, .04)], 'c': 'orange', 'at': 4, 'dt': 1.0},
       {'fig': [('box', .17, .14, .29, .9)], 'c': 'green', 'at': 5}, {'fig': [('box', .3, .38, .36, .9)], 'c': 'purple', 'at': 5, 'dt': 2.0},
       {'fig': [('box', .79, .0, .99, .07)], 'c': 'red', 'at': 6})
B.spen(LESSON, S, 1, {'fig': [('circle', .31, .16, .03, .06)], 'c': 'orange', 'at': 3}, {'fig': [('underline', .4, .64, .17)], 'c': 'orange', 'at': 3, 'dt': 1.0},
       {'fig': [('box', .15, .55, .85, .78)], 'c': 'blue', 'at': 3, 'dt': -1.5})
S = 'Testing: stuck-at'
B.spen(LESSON, S, 1, {'fig': [('circle', .44, .32, .06, .06)], 'c': 'red', 'at': 1}, {'fig': [('circle', .06, .38, .05, .1)], 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'fig': [('circle', .06, .6, .04, .05)], 'c': 'orange', 'at': 1, 'dt': 4.0}, {'fig': [('box', .8, .49, .99, .63)], 'c': 'green', 'at': 2},
       {'fig': [('check', .97, .7)], 'c': 'green', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('underline', .1, .52, .93)], 'c': 'blue', 'at': 0})
S = 'Error-correcting codes'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, .16, .045, .07)], 'c': 'orange', 'at': 3, 'dt': t, 'keep': False} for x, t in ((.27, 4.0), (.37, 4.6), (.57, 5.2))])
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, .16, .045, .07)], 'c': 'blue', 'at': 1, 'dt': t, 'keep': False} for x, t in ((.27, 0), (.47, .5), (.67, 1.0), (.87, 1.5))])
B.spen(LESSON, S, 2, {'fig': [('circle', .77, .52, .055, .09)], 'c': 'red', 'at': 0}, {'fig': [('underline', .05, .26, .8)], 'c': 'green', 'at': 2},
       {'fig': [('underline', .32, .54, .8)], 'c': 'red', 'at': 2, 'dt': 0.8}, {'fig': [('underline', .58, .8, .8)], 'c': 'red', 'at': 2, 'dt': 1.3},
       {'fig': [('box', .04, .82, .77, .93)], 'c': 'green', 'at': 3})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Side-channel attacks: power and timing', {'t': 'wb', 'h': 'Worked example: correlation power analysis on a toy chip', 'cfs': 36, 'steps': [
    {'say': "Correlation power analysis sounds like magic, so let's do it by hand on a toy four bit chip. The chip computes p X O R k, a plaintext with a secret key. Driving more ones onto the wires costs more power, so the power is roughly the Hamming weight, the number of ones, of that result.",
     'w': [{'m': r'chip computes  $v = p \oplus k$', 'at': 1}, {'m': 'power ≈ Hamming weight of v  (number of 1s)', 'c': 'blue', 'at': 2}]},
    {'say': "We send four known plaintexts and measure the power each time. The numbers are noisy: one point one, two point nine, one point oh, one point two.",
     'w': [{'k': 'p:          0000  1111  0011  0101', 'lang': 'plain', 'at': 0, 'gap': 14}, {'k': 'measured:    1.1   2.9   1.0   1.2', 'lang': 'plain', 'at': 1}]},
    {'say': "Now guess the key. If k were zero zero zero zero, v would equal p, with weights zero, four, two, two. That doesn't track the measurements at all. Try k equals zero zero zero one: v becomes zero zero zero one, one one one zero, zero zero one zero, zero one zero zero, with weights one, three, one, one. That rises and falls exactly with the measured power.",
     'w': [{'k': 'guess 0000:  0     4     2     2', 'lang': 'plain', 'at': 1}, {'k': 'guess 0001:  1     3     1     1', 'lang': 'plain', 'at': 3}]},
    {'say': "The guess with the highest correlation is the key: zero zero zero one. We never broke the math. A real attack does this for each byte of an A E S key, with two hundred fifty six guesses per byte and thousands of traces to beat the noise. That's why masking, which randomizes v so its weight no longer depends on the key, is the standard defense.",
     'w': [{'m': 'best correlation  →  k = 0001', 'c': 'green', 'box': True, 'at': 0}, {'m': 'AES: 16 bytes × 256 guesses each, not 2^128', 'c': 'red', 'at': 2}]},
]})

G = 'Worked example: correlation power analysis on a toy chip'
B.pen(LESSON, G, 2, {'p': ('cross',), 'on': 'guess 0000:', 'at': 1}, {'p': ('check',), 'on': 'guess 0001:', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'AES: 16 bytes', 'c': 'red', 'at': 2})
