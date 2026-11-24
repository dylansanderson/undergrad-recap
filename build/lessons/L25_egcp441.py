import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import schemdraw, schemdraw.elements as elm
X = np.linspace

def fig_switches(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    rows = [('NMOS', 'gate = 1 → ON', 'passes a strong 0, weak 1', 'pull-DOWN network'), ('PMOS', 'gate = 0 → ON', 'passes a strong 1, weak 0', 'pull-UP network')]
    table(ax, 2, 44, ['transistor', 'conducts when', 'quality', 'so CMOS uses it for'], rows, [16, 24, 30, 26], 10, 17)
    txt(ax, 50, 10, 'CMOS = Complementary MOS: one network pulls up, the other pulls down,\nnever both on in steady state → almost no static current', 16, C['mut'])
    save(fig, path)

def mos(ax, x, y, p=False, lab=None, s=1.0):
    """MOS symbol: top terminal (x, y+5s), bottom (x, y-5s), gate input at (x-6s, y)."""
    k = C['ink']
    line(ax, [(x, y + 5 * s), (x, y + 2.5 * s), (x - 2 * s, y + 2.5 * s)], k, 2.4)
    line(ax, [(x, y - 5 * s), (x, y - 2.5 * s), (x - 2 * s, y - 2.5 * s)], k, 2.4)
    line(ax, [(x - 2 * s, y + 3.2 * s), (x - 2 * s, y - 3.2 * s)], k, 3)
    line(ax, [(x - 3.2 * s, y + 3 * s), (x - 3.2 * s, y - 3 * s)], k, 3)
    if p:
        ax.add_patch(Circle((x - 4.1 * s, y), 0.9 * s, fc='white', ec=k, lw=2.2, zorder=5)); line(ax, [(x - 6 * s, y), (x - 5 * s, y)], k, 2.4)
    else:
        line(ax, [(x - 6 * s, y), (x - 3.2 * s, y)], k, 2.4)
    if lab: txt(ax, x - 7 * s, y, lab, 17, C['blue'], ha='right', bold=True)
    return (x, y + 5 * s), (x, y - 5 * s), (x - 6 * s, y)

def _vdd(ax, x, y):
    line(ax, [(x - 3, y), (x + 3, y)], C['ink'], 3); txt(ax, x, y + 2.5, 'V_DD', 15, C['ink'], bold=True)
def _gnd(ax, x, y):
    for i, wd in enumerate((3, 2, 1)): line(ax, [(x - wd, y - i * 1.1), (x + wd, y - i * 1.1)], C['ink'], 2.5)

def fig_inv(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    pt, pb, pg = mos(ax, 50, 42, p=True, s=1.2); nt, nb, ng = mos(ax, 50, 18, s=1.2)
    _vdd(ax, 50, pt[1]); line(ax, [pb, nt], C['ink'], 2.4); _gnd(ax, 50, nb[1])
    line(ax, [pg, (36, 42), (36, 18), ng], C['ink'], 2.4); line(ax, [(36, 30), (22, 30)], C['ink'], 2.4); dot(ax, 36, 30, 0.8, C['ink'])
    txt(ax, 18, 30, 'IN', 20, C['blue'], bold=True)
    dot(ax, 50, 30, 0.8, C['ink']); line(ax, [(50, 30), (68, 30)], C['ink'], 2.4); txt(ax, 73, 30, 'OUT', 20, C['orange'], bold=True)
    txt(ax, 60, 42, 'PMOS\n(pull-up)', 15, C['mut'], ha='left'); txt(ax, 60, 18, 'NMOS\n(pull-down)', 15, C['mut'], ha='left')
    save(fig, path)

def fig_vtc(path, w, h):
    fig, ax = plot(w, h)
    vin = X(0, 1.2, 400); vm = 0.6; vout = 0.6 * (1 - np.tanh((vin - vm) / 0.06))
    ax.plot(vin, vout, color=C['blue']); ax.plot([0, 1.2], [0, 1.2], color=C['gray'], ls=':', lw=1.5)
    soliddot(ax, vm, vm, C['orange']); ax.text(vm + 0.03, vm + 0.05, 'V_M (V_in = V_out)', fontsize=16, color=C['orange'])
    for v, t in ((0.53, 'V_IL'), (0.67, 'V_IH')): ax.axvline(v, color=C['red'], ls='--', lw=1.5); ax.text(v, 1.25, t, ha='center', fontsize=15, color=C['red'])
    ax.set_xlabel('V_in (V)'); ax.set_ylabel('V_out (V)'); ax.set_ylim(-0.05, 1.32)
    ax.set_title('inverter VTC: noise margins NM_L = V_IL − V_OL, NM_H = V_OH − V_IH', fontsize=16)
    save(fig, path)

def fig_nand(path, w, h):
    fig, ax, H = canvas(w, h, need=62, exact=True)
    p1t, p1b, _ = mos(ax, 34, 48, p=True, lab='A'); p2t, p2b, _ = mos(ax, 58, 48, p=True, lab='B')
    line(ax, [(30, 56), (62, 56)], C['ink'], 3); txt(ax, 46, 59, 'V_DD', 15, bold=True); line(ax, [p1t, (34, 56)], C['ink'], 2.4); line(ax, [p2t, (58, 56)], C['ink'], 2.4)
    line(ax, [p1b, (34, 38), (58, 38), p2b], C['ink'], 2.4); dot(ax, 46, 38, 0.8, C['ink'])
    line(ax, [(46, 38), (46, 33)], C['ink'], 2.4); line(ax, [(46, 38), (76, 38)], C['ink'], 2.4); txt(ax, 78, 38, 'Y = NOT(A·B)', 18, C['orange'], ha='left', bold=True)
    n1t, n1b, _ = mos(ax, 46, 28, lab='A'); n2t, n2b, _ = mos(ax, 46, 14, lab='B')
    line(ax, [n1b, n2t], C['ink'], 2.4); _gnd(ax, 46, 9)
    txt(ax, 70, 50, 'PMOS in PARALLEL:\neither input 0 → Y = 1', 14, C['green'], ha='left'); txt(ax, 60, 20, 'NMOS in SERIES:\nboth inputs 1 → Y = 0', 14, C['red'], ha='left')
    save(fig, path)

def fig_delay(path, w, h):
    fig, a2 = plot(w, h)
    t = X(0, 5, 300); a2.plot(t, np.where(t < 1, 1, np.exp(-(t - 1))), color=C['blue'], label='output (discharging C through R)'); a2.plot(t, np.where(t < 1, 0, 1), color=C['gray'], ls='--', label='input step')
    a2.axhline(0.5, color=C['orange'], ls=':'); a2.annotate('', (1.69, 0.5), (1, 0.5), arrowprops=dict(arrowstyle='<->', color=C['orange'], lw=2.5)); a2.text(2.3, 0.62, 't_PHL = 0.69 RC', color=C['orange'], fontsize=17, fontweight='bold')
    a2.set_xlabel('time (units of RC)'); a2.set_yticks([0, 0.5, 1]); a2.set_ylim(-0.05, 1.35); a2.legend(loc='upper right', fontsize=14)
    a2.set_title('on-transistor ≈ R, load (gates + wire + diffusion) ≈ C', fontsize=17)
    save(fig, path)

def fig_power(path, w, h):
    fig, ax = plot(w, h, grid=False)
    v = np.array([1.2, 1.0, 0.9, 0.8]); p = 0.1 * 10e-9 * v ** 2 * 3e9
    b = ax.bar([f'{x} V' for x in v], p, color=[C['red'], C['orange'], C['yellow'], C['green']])
    for r, val in zip(b, p): ax.text(r.get_x() + r.get_width() / 2, val + 0.06, f'{val:.2f} W', ha='center', fontsize=17, fontweight='bold')
    ax.set_ylabel('dynamic power (W)'); ax.set_xlabel('supply voltage V_DD')
    ax.set_title('P = α C V_DD² f   (α = 0.1, C = 10 nF, f = 3 GHz)', fontsize=18)
    save(fig, path)

def fig_wire(path, w, h):
    fig, ax = plot(w, h)
    L = X(0, 10, 200); ax.plot(L, 0.38 * L ** 2, color=C['red'], label='unbuffered wire: ∝ L²')
    n = 4; seg = L / n; ax.plot(L, n * 0.38 * seg ** 2 + (n - 1) * 0.12 * L, color=C['green'], label='with 3 repeaters: ≈ linear')
    ax.set_xlabel('wire length (mm, illustrative)'); ax.set_ylabel('delay (relative)'); ax.legend(loc='upper left')
    ax.set_title('Elmore delay of a distributed RC wire ≈ 0.38 r c L²', fontsize=18)
    save(fig, path)

def fig_tgate(path, w, h):
    fig, ax, H = canvas(w, h, need=52, exact=True)
    txt(ax, 50, 49, '2:1 multiplexer from two transmission gates', 18, bold=True)
    for k, (y, inp, sel) in enumerate(((34, 'A', 'S = 0'), (14, 'B', 'S = 1'))):
        txt(ax, 6, y, inp, 22, C['blue'], bold=True); line(ax, [(10, y), (36, y)], C['ink'], 2.5)
        box(ax, 36, y - 6, 22, 12, 'NMOS ∥ PMOS\n(on when ' + sel + ')', fc=C['lpurple'], ec=C['purple'], fs=14, r=0.6)
        line(ax, [(58, y), (74, y), (74, 24)], C['ink'], 2.5)
    line(ax, [(74, 24), (86, 24)], C['ink'], 2.5); txt(ax, 92, 24, 'Y', 22, C['orange'], bold=True)
    txt(ax, 50, 3, 'passes strong 0 AND strong 1 · only 4 transistors + an inverter for S̄', 15, C['mut'])
    save(fig, path)

def fig_layout(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    ax.add_patch(Rectangle((14, 32), 44, 24, fc='#F6E7B0', ec='#C9A227', lw=2)); txt(ax, 16, 54, 'n-well', 14, '#8A6D0B', ha='left')
    ax.add_patch(Rectangle((20, 38), 32, 12, fc='#E59C9C', ec=C['red'], lw=2)); txt(ax, 21, 39.8, 'p+ active', 13, C['red'], ha='left', z=7)
    ax.add_patch(Rectangle((20, 10), 32, 12, fc='#9CD3A8', ec=C['green'], lw=2)); txt(ax, 21, 20.2, 'n+ active', 13, C['green'], ha='left', z=7)
    ax.add_patch(Rectangle((34, 6), 4, 48, fc='#D9534F', ec='#A12B27', lw=2, alpha=0.85)); txt(ax, 33, 29, 'poly gate', 13, '#A12B27', ha='right', z=7)
    ax.add_patch(Rectangle((8, 56), 56, 4, fc='#7FA7E0', ec=C['blue'], lw=2)); txt(ax, 66, 58, 'V_DD (metal 1)', 14, C['blue'], ha='left')
    ax.add_patch(Rectangle((8, 0), 56, 4, fc='#7FA7E0', ec=C['blue'], lw=2)); txt(ax, 66, 2, 'GND (metal 1)', 14, C['blue'], ha='left')
    ax.add_patch(Rectangle((42, 14), 6, 32, fc='#7FA7E0', ec=C['blue'], lw=2, alpha=0.9)); txt(ax, 66, 30, 'OUT (metal 1)', 14, C['blue'], ha='left')
    line(ax, [(48, 30), (64, 30)], C['blue'], 2)
    for (x, y) in ((24, 42), (44, 42), (24, 14), (44, 14)): ax.add_patch(Rectangle((x, y), 4, 4, fc='#333333', ec='black'))
    line(ax, [(26, 46), (26, 58)], C['blue'], 6); line(ax, [(26, 14), (26, 2)], C['blue'], 6)
    txt(ax, 82, 45, 'design rules (λ) →\nDRC · LVS ·\nparasitic extraction', 14, C['mut'])
    save(fig, path)

LESSON = {
 'code': 'EGCP 441', 'title': 'Advanced Electronics for Computer Engineers', 'tag': 'Year 4 · VLSI', 'folder': 'EGCP-441 Advanced Electronics (CMOS)',
 'slides': [
 {'t': 'title', 'h': 'CMOS Circuit Design', 'sub': 'Advanced electronics for computer engineers: inverters, gates, delay, power, wires and layout', 'img': 'a:cleanroom',
  'say': "Welcome to E G C P four forty one, advanced electronics for computer engineers. In digital logic, gates were ideal boxes that switched instantly and cost nothing. In this course we open the boxes. Every gate is built from MOS transistors, and their physics decides how fast a chip can run, how much power it burns, and how small it can be. Chips like the ones made in clean rooms like this are designed from the ideas in this lecture: the CMOS inverter, static logic gates, delay and power, interconnect, and physical layout."},

 {'t': 'v', 'h': 'MOSFETs as switches: NMOS and PMOS', 'img': 'fig:switches',
  'pts': ['NMOS: on when gate high — good at pulling DOWN', 'PMOS: on when gate low — good at pulling UP', 'Threshold V_t: below it, (mostly) off', 'In this course’s labs: measure V_t and I–V curves of real MOSFETs'],
  'say': ["Recall the MOSFET from electronics. An N channel MOSFET conducts when its gate is high. It passes a strong zero, pulling a node all the way to ground, but only a weak one, because it turns off as the output rises to within a threshold voltage of the gate.",
          "A P channel MOSFET is the mirror image. It conducts when its gate is low, and it passes a strong one but a weak zero.",
          "So CMOS, complementary MOS, uses each where it's strong: PMOS transistors to pull outputs up to the supply, and NMOS transistors to pull them down to ground. Below the threshold voltage, a transistor is mostly off, though a small leakage current still flows.",
          "In this course's first labs, students characterize real MOSFETs on the bench, measuring threshold voltages and current voltage curves for both N and P channel devices, to see the square law models from electronics in actual hardware."]},

 {'t': 'v', 'h': 'The CMOS inverter', 'img': ['fig:inv', 'fig:vtc'],
  'pts': ['PMOS on top, NMOS on bottom, gates tied together', 'IN = 0 → PMOS on → OUT = V_DD; IN = 1 → NMOS on → OUT = 0', 'Switching threshold V_M set by PMOS/NMOS strength', 'Noise margins: how much noise an input can tolerate'],
  'say': ["The simplest CMOS gate is the inverter: a PMOS transistor from the supply to the output, an NMOS from the output to ground, and both gates tied to the input. When the input is low, the PMOS is on and the NMOS is off, so the output is pulled up to V D D. When the input is high, the NMOS is on and the PMOS is off, so the output is pulled to ground. In either steady state, one transistor is always off, so there's no path from supply to ground and almost no current flows. That's why CMOS took over the industry.",
          "Sweep the input slowly and plot the output, and you get the voltage transfer characteristic. The switching threshold, V M, is where input equals output. It depends on the relative strength of the two transistors. Holes move more slowly than electrons, so designers make the PMOS two to three times wider to center V M at half the supply. The noise margins measure how much noise an input can tolerate and still be read correctly. They're set by the points where the curve's slope is minus one, V I L and V I H. A steep curve, like this one, means large noise margins, which is why digital logic is so robust. In the labs, students measure exactly this curve, then the inverter's switching delay."]},

 {'t': 'v', 'h': 'Static CMOS gates: NAND and NOR', 'img': 'fig:nand',
  'pts': ['Pull-down network (NMOS) + complementary pull-up (PMOS)', 'Series in one ⇔ parallel in the other', 'NAND: NMOS in series, PMOS in parallel', 'CMOS gates invert naturally; AND = NAND + inverter'],
  'say': ["Every static CMOS gate follows one recipe. Build a pull down network of NMOS transistors that conducts exactly when the output should be zero. Then build the complementary pull up network of PMOS transistors: wherever the NMOS network has transistors in series, the PMOS network has them in parallel, and vice versa. It's De Morgan's law in silicon.",
          "Look at the NAND gate. The output should be zero only when A and B are both one, so the two NMOS transistors are in series: both must be on to pull the output down. The PMOS transistors are in parallel: if either input is zero, its PMOS pulls the output up. A NOR gate is the opposite, with NMOS in parallel and PMOS in series.",
          "Because NMOS transistors are faster, NAND gates, with their series NMOS, are usually preferred over NOR gates, whose slow PMOS transistors end up in series.",
          "Notice that CMOS gates naturally invert. An AND gate is really a NAND followed by an inverter, costing six transistors instead of four. That's why logic synthesis tools love NAND and NOR. In this course's labs, students build NOT, NAND, NOR, and three input versions as transistor level schematics and physical layouts."]},

 {'t': 'v', 'h': 'Delay: it’s all R and C', 'img': 'fig:delay',
  'pts': ['On transistor ≈ resistor R; everything it drives ≈ capacitor C', 't_p ≈ 0.69 RC (time to cross 50%)', 'Wider transistor → lower R, but more input C', 'Logical effort: size stages ≈ 4× apart (fanout-of-4)'],
  'say': ["Why does a gate take time to switch? Model the on transistor as a resistor, and everything the output drives, the gates of the next stage, the wire, and the transistor's own diffusion regions, as a capacitor.",
          "When the input switches, the output charges or discharges through that resistor, the R C exponential from the circuits course. The propagation delay is the time to cross fifty percent of the swing, which is the natural log of two, about point six nine, times R C. Average the rising and falling delays, t P L H and t P H L, to get the gate's delay.",
          "To go faster, make the transistor wider to lower its resistance. But a wider transistor also has a bigger gate capacitance, which slows down whatever drives it. There's no free lunch.",
          "The method of logical effort optimizes this trade off. One famous result: to drive a big load, use a chain of inverters that grow by about a factor of four at each stage, called the fanout of four rule. Chip designers use F O four delays as a technology independent unit of speed."]},

 {'t': 'v', 'h': 'Power: why chips get hot', 'img': 'fig:power',
  'pts': ['Dynamic: P = α C V_DD² f', 'Voltage is the biggest lever (squared!)', 'Short-circuit power during transitions', 'Leakage (static) dominates at nanometer scales'],
  'say': ["Every time a node switches, its capacitance is charged from the supply and then dumped to ground, burning energy C V squared per full cycle. Multiply by how often nodes switch, the activity factor alpha, and the clock frequency, and you get dynamic power: alpha C V D D squared f.",
          "Voltage is the biggest lever, because it's squared. With an activity factor of point one, ten nanofarads of total switched capacitance and a three gigahertz clock, a one point two volt chip burns over four watts. Drop to point eight volts and it's under two watts, less than half. That's why phones constantly scale voltage and frequency up and down, called D V F S.",
          "During each transition, both networks are briefly on at once, so a little short circuit current flows straight from supply to ground.",
          "And in modern nanometer transistors, which can't fully turn off, leakage current flows all the time, even when nothing switches. Leakage is a major part of a modern chip's power, which is why unused blocks are power gated, switched off completely. In this course's labs, students measure the power and energy of their gates in simulation."]},

 {'t': 'v', 'h': 'Interconnect: wires are the new bottleneck', 'img': 'fig:wire',
  'pts': ['Wires have distributed resistance and capacitance', 'Unbuffered delay grows with length² (Elmore)', 'Fix: insert repeaters → roughly linear', 'Crosstalk couples neighboring wires'],
  'say': ["Transistors have shrunk enormously, but the wires connecting them haven't kept up. A wire has resistance along its length and capacitance to everything around it, distributed all along it.",
          "For a long wire, both resistance and capacitance grow with length, so the delay grows with length squared. The Elmore delay of a distributed R C line is about point three eight times r times c times L squared. Double a wire's length, and its delay quadruples.",
          "The fix is to break long wires into segments with buffers, called repeaters, in between. Each segment is short, so the total delay grows roughly linearly with length instead.",
          "Wires also couple to their neighbors. When one switches, it can inject noise into the wire next to it, called crosstalk. In many modern chips, the critical path is dominated by wires, not transistors. In the interconnect lab, students model exactly this R C wire delay."]},

 {'t': 'v', 'h': 'Transmission gates and other logic styles', 'img': 'fig:tgate',
  'pts': ['Transmission gate: NMOS ∥ PMOS with complementary controls', 'Passes both 0 and 1 cleanly', 'Ideal for multiplexers, XORs and latches', 'Other styles: pass-transistor, pseudo-NMOS, dynamic/domino'],
  'say': ["A single NMOS transistor passes zeros well but ones poorly, and a PMOS the opposite. Put them in parallel, with complementary control signals, and you get a transmission gate, a nearly ideal switch that passes both values cleanly.",
          "Two transmission gates make an elegant two to one multiplexer. When the select signal is zero, the top gate passes A. When it's one, the bottom gate passes B. Just four transistors, plus an inverter for the complemented select, far fewer than building a mux from NAND gates.",
          "Transmission gates are also the heart of efficient X O R gates and of latches and flip flops. As a final project in this course, student teams design a CMOS multiplexer from transmission gates and trade off its power, area and delay.",
          "Other logic styles exist for special needs. Pseudo N MOS uses a weak always on pull up, which is small but burns static power. Dynamic, or domino, logic precharges a node and then conditionally discharges it, which is very fast but sensitive to noise. Static CMOS remains the default because it's robust."]},

 {'t': 'v', 'h': 'From schematic to silicon: layout and fabrication', 'img': ['a:mask_aligner', 'fig:layout'],
  'pts': ['Photolithography: pattern one layer at a time', 'Layers: wells, active, poly (gates), contacts, metals', 'Design rules (λ) guarantee manufacturability', 'DRC, LVS, extraction → back to SPICE'],
  'say': ["Chips are manufactured by photolithography. A light sensitive resist is exposed through a patterned mask, using machines like this mask aligner in a university lab, or vastly more advanced scanners in commercial fabs. Each exposure defines one layer, and a modern chip is built up from dozens of them.",
          "A designer draws the layout, the actual shapes on each layer. Here's an inverter. The PMOS sits in an n well at the top, where the red polysilicon gate crosses the p plus active region. The NMOS sits at the bottom where the same gate crosses the n plus active region. Black squares are contacts, and blue metal connects the supply, ground and the output. Design rules, often expressed in units of lambda, set minimum widths and spacings so the chip can actually be manufactured. Tools then check the layout against the rules, called D R C, verify that it matches the schematic, called L V S, and extract the real resistances and capacitances back into SPICE for accurate simulation. In this course, students draw layouts like this in the Magic layout tool and simulate them in LT spice."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'CMOS = complementary **pull-up and pull-down** networks. Speed is **RC**, power is **α C V² f**, and long **wires** need repeaters.',
  'cap': 'Next: EGCP 446, Advanced Digital Design with Verilog.',
  'say': "To recap. NMOS transistors pull down and PMOS transistors pull up, so CMOS gates combine complementary networks that draw almost no static current. The inverter's transfer curve gives noise margins. NAND and NOR follow the series parallel duality. Delay comes from charging capacitance through transistor resistance, power from charging it at all, scaled by voltage squared, and leakage adds static power. Long wires are slow and need repeaters. Transmission gates make efficient muxes, and layout turns schematics into manufacturable silicon. Next, advanced digital design with Verilog. See you there."},
 ]}

# ---------------- whiteboard worked examples (transistor circuits drawn live) ----------------
import board as B

def _vdd(ax, x, y, wdt=120):
    B.ln(ax, [x - wdt / 2, x + wdt / 2], [y, y], lw=4); B.lab(ax, x, y + 30, 'VDD', 28)
def _gnd(ax, x, y):
    for k, ww in enumerate((60, 38, 16)): B.ln(ax, [x - ww / 2, x + ww / 2], [y - k * 12, y - k * 12], lw=3)

def draw_inv(ax, n, w, h):
    cx = w * 0.45; yp, yn = h * 0.70, h * 0.30
    if n >= 1:
        p = B.mos(ax, cx, yp, 'p', 1.3); _vdd(ax, p['top'][0], p['top'][1]); B.lab(ax, cx + 110, yp, 'PMOS', 30, 'blue', ha='left')
    if n >= 2:
        q = B.mos(ax, cx, yn, 'n', 1.3); _gnd(ax, q['bot'][0], q['bot'][1]); B.lab(ax, cx + 110, yn, 'NMOS', 30, 'blue', ha='left')
        B.ln(ax, [p['bot'][0]] * 2, [p['bot'][1], q['top'][1]], lw=3); B.dot(ax, p['bot'][0], h * 0.5, s=12)
    if n >= 3:
        gx = p['g'][0]; B.ln(ax, [gx, gx], [p['g'][1], q['g'][1]], lw=3); B.ln(ax, [gx - 90, gx], [h * 0.5, h * 0.5], lw=3)
        B.dot(ax, gx, h * 0.5, s=12); B.dot(ax, gx - 90, h * 0.5, s=12, hollow=True); B.lab(ax, gx - 110, h * 0.5, 'IN', 32, ha='right')
        B.ln(ax, [p['bot'][0], p['bot'][0] + 160], [h * 0.5, h * 0.5], lw=3); B.dot(ax, p['bot'][0] + 160, h * 0.5, c='red', s=12, hollow=True)
        B.lab(ax, p['bot'][0] + 180, h * 0.5, 'OUT', 32, 'red', ha='left')

def draw_nand(ax, n, w, h):
    s = 1.1; xa, xb, yp = w * 0.30, w * 0.62, h * 0.78; xo = xb + 42 * s
    if n >= 1:
        pa = B.mos(ax, xa, yp, 'p', s); pb = B.mos(ax, xb, yp, 'p', s)
        B.ln(ax, [pa['top'][0], pb['top'][0]], [pa['top'][1]] * 2, lw=4); B.lab(ax, (pa['top'][0] + pb['top'][0]) / 2, pa['top'][1] + 30, 'VDD', 28)
        B.ln(ax, [pa['bot'][0], pb['bot'][0]], [pa['bot'][1]] * 2, lw=3)
        for g, l in ((pa['g'], 'A'), (pb['g'], 'B')): B.lab(ax, g[0] - 18, g[1], l, 30, 'blue', ha='right')
        B.lab(ax, xb + 110, yp + 30, 'parallel\nPMOS', 26, 'green', ha='left')
        yo = pa['bot'][1]; B.dot(ax, pa['bot'][0], yo, s=12)
    if n >= 2:
        na = B.mos(ax, xa, yo - 85 * s - 30, 'n', s); nb = B.mos(ax, xa, yo - 2 * 85 * s - 60, 'n', s)
        B.ln(ax, [pa['bot'][0]] * 2, [yo, na['top'][1]], lw=3); B.ln(ax, [na['bot'][0]] * 2, [na['bot'][1], nb['top'][1]], lw=3)
        _gnd(ax, nb['bot'][0], nb['bot'][1])
        for g, l in ((na['g'], 'A'), (nb['g'], 'B')): B.lab(ax, g[0] - 18, g[1], l, 30, 'blue', ha='right')
        B.lab(ax, xa + 210, na['bot'][1], 'NMOS in series', 26, 'green', ha='left')
    if n >= 3:
        B.ln(ax, [pb['bot'][0], pb['bot'][0] + 130], [yo, yo], lw=3); B.dot(ax, pb['bot'][0] + 130, yo, c='red', s=12, hollow=True)
        B.lab(ax, pb['bot'][0] + 150, yo, 'OUT', 30, 'red', ha='left')

B.insert(LESSON, 'The CMOS inverter', {'t': 'wb', 'h': 'Worked example: building an inverter from two transistors', 'draw': 'inv', 'split': 0.5, 'steps': [
    {'say': "Let's draw the most important circuit in digital electronics. Put a P M O S transistor at the top, with its source connected to the supply, V D D.",
     'w': [{'m': 'PMOS: ON when its gate is LOW', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Below it, an N M O S transistor, with its source at ground. Their drains meet in the middle, and that's the output.",
     'w': [{'m': 'NMOS: ON when its gate is HIGH', 'at': 0}, {'d': 2, 'at': 1}]},
    {'say': "Tie both gates together as the input. Now, input low: the P M O S turns on and the N M O S turns off, so the output connects to V D D. A one. Input high: the N M O S turns on, the P M O S off, and the output connects to ground. A zero. It's a NOT gate.",
     'w': [{'d': 3, 'at': 0}, {'m': 'IN = 0: PMOS on, NMOS off  so OUT = 1', 'c': 'blue', 'at': 1}, {'m': 'IN = 1: NMOS on, PMOS off  so OUT = 0', 'c': 'blue', 'at': 2}]},
    {'say': "Here's the magic. In either steady state, one transistor is always off, so there's no path from the supply to ground. A CMOS gate burns almost no power while it sits still. That one property is why CMOS won, and why your phone can have billions of these.",
     'w': [{'m': 'never a path VDD to GND in steady state', 'c': 'red', 'box': True, 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Static CMOS gates: NAND and NOR', {'t': 'wb', 'h': 'Worked example: a CMOS NAND gate, transistor by transistor', 'draw': 'nand', 'split': 0.45, 'steps': [
    {'say': "A NAND output should be zero only when A and B are both one. Build the pull up network first: two P M O S transistors in parallel from V D D to the output. If either input is low, at least one of them conducts, and the output is pulled high.",
     'w': [{'m': 'NAND: OUT = 0 only if A = B = 1', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "The pull down network is the complement: two N M O S transistors in series from the output to ground. Current only gets through if both are on, which needs A and B both high.",
     'w': [{'d': 2, 'at': 0}, {'m': 'series in one network ⇔ parallel in the other', 'c': 'green', 'at': 1}]},
    {'say': "Check every row. Zero zero: both P M O S on, output one. Zero one, and one zero: one P M O S on, and the series N M O S chain is broken, so output one. One one: both P M O S off, both N M O S on, output zero. That's NAND, with just four transistors.",
     'w': [{'k': 'A B | OUT', 'plain': True, 'fs': 38, 'gap': 10, 'at': 0}, {'k': '0 0 |  1', 'plain': True, 'fs': 38, 'at': 1}, {'k': '0 1 |  1', 'plain': True, 'fs': 38, 'at': 2},
           {'k': '1 0 |  1', 'plain': True, 'fs': 38, 'at': 2}, {'k': '1 1 |  0', 'plain': True, 'fs': 38, 'c': 'red', 'at': 3}, {'d': 3, 'at': 4}]},
]})

B.insert(LESSON, 'Delay: it’s all R and C', {'t': 'wb', 'h': 'Worked example: how long does a gate take?', 'steps': [
    {'say': "Model an on transistor as a resistor, about ten kilohms for a small one in this example, and everything it drives as a capacitor, say ten femtofarads for one gate input plus wire.",
     'w': [{'m': r'$R_{on} \approx 10\ \mathrm{k\Omega}$,   $C_{load} \approx 10\ \mathrm{fF}$', 'at': 0}]},
    {'say': "The output is an RC circuit charging or discharging. It crosses the halfway point after point six nine times R C. Ten thousand times ten femtofarads is a hundred picoseconds, so the delay is about sixty nine picoseconds.",
     'w': [r'$t_p = 0.69\,RC = 0.69(10^4)(10^{-14})$', {'m': r'$t_p \approx 69\ \mathrm{ps}$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "Now make this gate drive four others, a fan out of four. The load capacitance quadruples to forty femtofarads, and so does the delay: two hundred seventy six picoseconds.",
     'w': [{'m': r'fan-out 4: $C = 40\ \mathrm{fF} \Rightarrow t_p \approx 276\ \mathrm{ps}$', 'at': 1}]},
    {'say': "The fix is to make the driving transistor wider, which lowers its resistance. But a wider transistor has more gate capacitance, which slows down whatever drives it. That trade off is exactly what logical effort and gate sizing are about.",
     'w': [{'m': 'wider: lower R, but more input C', 'c': 'blue', 'at': 1}, {'m': 'size each stage about 4× the previous', 'c': 'green', 'at': 3}]},
]})

B.insert(LESSON, 'Power: why chips get hot', {'t': 'wb', 'h': 'Worked example: the power equation in numbers', 'steps': [
    {'say': "Dynamic power is alpha times C times V squared times f. Take a chip whose switched capacitance totals one nanofarad, with ten percent of nodes switching each cycle, at one volt and two gigahertz.",
     'w': [r'$P = \alpha\,C\,V_{DD}^2\,f$', {'m': r'$\alpha = 0.1$,  $C = 1\ \mathrm{nF}$,  $V = 1.0\ \mathrm{V}$,  $f = 2\ \mathrm{GHz}$', 'at': 1}]},
    {'say': "Point one times ten to the minus nine times one squared times two times ten to the ninth: point two watts.",
     'w': [{'m': r'$P = 0.1\times 10^{-9}\times 1^2\times 2\times 10^9 = 0.2\ \mathrm{W}$', 'at': 0}]},
    {'say': "Now lower the supply to point eight volts. Voltage is squared, so power drops to point six four of the original: point one two eight watts, thirty six percent less, for a twenty percent voltage cut.",
     'w': [{'m': r'$V = 0.8\ \mathrm{V}$:  $P = 0.2\times 0.8^2 = 0.128\ \mathrm{W}$', 'c': 'red', 'at': 0}, {'m': '20% less voltage  =  36% less power', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "That's why phones and laptops constantly scale voltage and frequency together, running slow and low when idle, and only boosting when you need speed. The quadratic dependence on voltage is the biggest power lever in chip design.",
     'w': [{'m': 'DVFS: lower V and f together when idle', 'c': 'green', 'gap': 10, 'at': 0}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: building an inverter from two transistors'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'gate is LOW', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'gate is HIGH', 'c': 'blue', 'at': 0})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'IN = 0', 'at': 1}, {'p': ('circle',), 'on': 'IN = 1', 'at': 2})
G = 'Worked example: a CMOS NAND gate, transistor by transistor'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'OUT = 0 only if', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'series in one network', 'c': 'green', 'at': 1})
B.pen(LESSON, G, 2, *[{'p': ('highlight',), 'on': row, 'line': True, 'at': a, 'solo': a > 1} for a, row in ((1, '0 0 |  1'), (2, '0 1 |  1'), (4, '1 1 |  0'))])
G = 'Worked example: how long does a gate take?'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '0.69', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'fan-out 4', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'wider: lower R', 'at': 2})
G = 'Worked example: the power equation in numbers'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': r'$P = \alpha', 'cols': None, 'at': 0})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'0.8^2', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'DVFS', 'c': 'green', 'at': 1})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'MOSFETs as switches'
B.spen(LESSON, S, 0, {'fig': [('highlight', .01, .3, .99, .49)], 'c': 'blue', 'at': 1, 'solo': True}, {'fig': [('circle', .58, .41, .12, .06)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .5, .99, .69)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('circle', .58, .61, .12, .06)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .72, .3, .99, .69)], 'c': 'green', 'at': 0}, {'fig': [('underline', .09, .9, .76)], 'c': 'purple', 'at': 0, 'dt': 4.0})
S = 'The CMOS inverter'
B.spen(LESSON, S, 0, {'fig': [('circle', .48, .29, .07, .1)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .48, .7, .07, .1)], 'c': 'blue', 'at': 0, 'dt': 2.0},
       {'fig': [('arrow', .52, .2, .52, .45)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .73, .5, .05, .05)], 'c': 'orange', 'at': 1, 'dt': 2.0},
       {'fig': [('arrow', .52, .55, .52, .78)], 'c': 'blue', 'at': 2}, {'fig': [('cross', .5, .5, .05)], 'c': 'red', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .51, .44, .04, .06)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .455, .14, .035, .04)], 'c': 'red', 'at': 5},
       {'fig': [('circle', .545, .14, .035, .04)], 'c': 'red', 'at': 5, 'dt': 0.8})
S = 'Static CMOS gates'
B.spen(LESSON, S, 0, {'fig': [('box', .38, .48, .5, .87)], 'c': 'blue', 'at': 1}, {'fig': [('box', .26, .05, .78, .3)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .44, .67, .08, .23)], 'c': 'red', 'at': 1}, {'fig': [('underline', .6, .82, .74)], 'c': 'red', 'at': 1, 'dt': 2.5},
       {'fig': [('box', .3, .1, .78, .3)], 'c': 'green', 'at': 2}, {'fig': [('underline', .6, .88, .24)], 'c': 'green', 'at': 2, 'dt': 2.5})
B.spen(LESSON, S, 3, {'fig': [('box', .76, .32, .98, .4)], 'c': 'orange', 'at': 0})
S = 'Delay: it'
B.spen(LESSON, S, 1, {'fig': [('arrow', .3, .3, .38, .52)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .4, .55, .06, .04)], 'c': 'orange', 'at': 1, 'dt': 1.0}, {'fig': [('box', .48, .4, .72, .47)], 'c': 'orange', 'at': 1, 'dt': 2.5})
S = 'Power: why chips'
B.spen(LESSON, S, 0, {'fig': [('underline', .14, .44, .08)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .22, .1, .08, .05)], 'c': 'red', 'at': 1}, {'fig': [('circle', .84, .5, .08, .05)], 'c': 'green', 'at': 2},
       {'fig': [('arrow', .25, .15, .82, .48)], 'c': 'purple', 'at': 2, 'dt': 1.5})
S = 'Interconnect'
B.spen(LESSON, S, 1, {'fig': [('circle', .91, .15, .05, .08)], 'c': 'red', 'at': 0}, {'fig': [('box', .1, .03, .98, .1)], 'c': 'red', 'at': 1},
       {'fig': [('circle', .5, .68, .04, .05)], 'c': 'red', 'at': 2}, {'fig': [('arrow', .53, .66, .89, .2)], 'c': 'red', 'at': 2, 'dt': 1.0})
B.spen(LESSON, S, 2, {'fig': [('underline', .28, .73, .21)], 'c': 'green', 'at': 0}, {'fig': [('arrow', .2, .78, .9, .55)], 'c': 'green', 'at': 1})
S = 'Transmission gates'
B.spen(LESSON, S, 0, {'fig': [('box', .35, .2, .58, .45)], 'c': 'blue', 'at': 0}, {'fig': [('box', .35, .62, .58, .87)], 'c': 'orange', 'at': 0, 'dt': 2.0},
       {'fig': [('arrow', .1, .38, .9, .55)], 'c': 'green', 'at': 1})

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
