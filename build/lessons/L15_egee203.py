import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import schemdraw, schemdraw.elements as elm
X = np.linspace

def fig_divider(path, w, h):
    def b(d):
        d += elm.SourceV().up().label('12 V')
        d += elm.Resistor().right().label('R1 = 4 kΩ')
        d += elm.Line().right().length(2.5)          # wider loop: R2's label sat on top of the source symbol
        d += elm.Dot()
        d.push()
        d += elm.Resistor().down().label('R2 = 8 kΩ', loc='top').label(('+', 'Vx = 8 V', '−'), loc='bottom', ofst=0.4, color=C['orange'])
        d += elm.Line().left().length(d.unit + 2.5)
        d.pop()
    schem(path, b)

def fig_nodal(path, w, h):
    def b(d):
        d += elm.SourceV().up().label('10 V')
        d += elm.Resistor().right().label('1 kΩ')
        A = d.add(elm.Dot().label('A', loc='top', color=C['blue']))
        d.push(); d += elm.Resistor().down().label('2 kΩ', loc='bottom'); d += elm.Line().left(); d.pop()
        d += elm.Resistor().right().label('1 kΩ')
        d += elm.Dot().label('B', loc='top', color=C['blue'])
        d += elm.Resistor().down().label('2 kΩ', loc='bottom')
        d += elm.Line().left()
        d += elm.Ground()
    schem(path, b)

def fig_nodal_eq(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    txt(ax, 50, 45, 'KCL at A:   (V_A − 10)/1 + V_A/2 + (V_A − V_B)/1 = 0', 20, family='Consolas')
    txt(ax, 50, 37, 'KCL at B:   (V_B − V_A)/1 + V_B/2 = 0', 20, family='Consolas')
    txt(ax, 50, 24, '[  2.5   −1  ] [V_A]   [10]\n[ −1    1.5 ] [V_B] = [ 0]', 22, C['blue'], family='Consolas')
    txt(ax, 50, 7, 'V_A ≈ 5.45 V,   V_B ≈ 3.64 V', 26, C['orange'], bold=True)
    save(fig, path)

def fig_thev1(path, w, h):
    def b(d):
        d += elm.SourceV().up().label('12 V')
        d += elm.Resistor().right().label('4 kΩ')
        d += elm.Dot(); d.push()
        d += elm.Resistor().down().label('12 kΩ', loc='bottom')
        d += elm.Line().left(); d.pop()
        d += elm.Line().right().length(3.5); d += elm.Dot(open=True).label('a', loc='right')   # far enough right that 'load?' clears '12 kΩ'
        d += elm.Gap().down().label(('', 'load?', ''), color=C['mut']); d += elm.Dot(open=True).label('b', loc='right')
        d += elm.Line().left().length(3.5)
    schem(path, b)

def fig_thev2(path, w, h):
    def b(d):
        d += elm.SourceV().up().label('V_th = 9 V', color=C['blue'])
        d += elm.Resistor().right().label('R_th = 3 kΩ', color=C['blue'])
        d += elm.Dot(open=True).label('a', loc='right')
        d += elm.Gap().down(); d += elm.Dot(open=True).label('b', loc='right')
        d += elm.Line().left()
    schem(path, b)

def fig_opamp(path, w, h):
    def b(d):
        op = elm.Opamp(leads=True); d += op
        d += elm.Line().down(d.unit / 4).at(op.in2); d += elm.Ground(lead=False)
        d += elm.Resistor().at(op.in1).left().idot().label('R_in = 1 kΩ', loc='bottom').label('v_in', loc='left')
        d += elm.Line().up(d.unit / 2).at(op.in1)
        d += elm.Resistor().tox(op.out).label('R_f = 10 kΩ')
        d += elm.Line().toy(op.out).dot()
        d += elm.Line().right(d.unit / 4).at(op.out).label('v_out = −10 v_in', loc='right', color=C['orange'])
    schem(path, b)

def fig_rc(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 5, 300); ax.plot(t, 5 * (1 - np.exp(-t)), color=C['blue'], label='capacitor voltage')
    for k in range(1, 6): ax.axvline(k, color=C['gray'], lw=1, ls=':')
    soliddot(ax, 1, 5 * (1 - np.exp(-1)), C['orange']); note(ax, 1.1, 2.2, '1 τ: 63% (3.16 V)', C['orange'], 18)
    note(ax, 3.3, 3.6, '5 τ: 99.3%', C['green'], 18)
    ax.set_xlabel('time (s)   —   τ = RC = 10 kΩ × 100 μF = 1 s'); ax.set_ylabel('volts'); ax.set_ylim(0, 5.6)
    ax.set_title('x(t) = x(∞) + [x(0) − x(∞)] e^(−t/τ)', fontsize=20)
    save(fig, path)

def fig_phasor(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, gridspec_kw={'width_ratios': [1.6, 1]})
    t = X(0, 2 / 60, 400); wt = 2 * np.pi * 60 * t
    a1.plot(t * 1000, 170 * np.cos(wt), color=C['blue'], label='v(t)'); a1.plot(t * 1000, 3.18 * 40 * np.cos(wt - np.pi / 4), color=C['orange'], label='i(t) (scaled)')
    a1.set_xlabel('time (ms)'); a1.legend(loc='upper right', fontsize=15); a1.set_title('current lags voltage by 45°', fontsize=18)
    a2.set_aspect('equal'); a2.grid(False); a2.axhline(0, color=C['gray'], lw=1); a2.axvline(0, color=C['gray'], lw=1)
    a2.annotate('', xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', lw=3.5, color=C['blue'])); a2.text(0.75, 0.07, 'V', fontsize=22, color=C['blue'])
    a2.annotate('', xy=(0.6, -0.6), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', lw=3.5, color=C['orange'])); a2.text(0.62, -0.55, 'I', fontsize=22, color=C['orange'])
    a2.set_xlim(-0.3, 1.2); a2.set_ylim(-0.9, 0.6); a2.set_xticks([]); a2.set_yticks([]); a2.set_title('phasors', fontsize=18)
    save(fig, path)

def fig_impedance(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    rows = [('resistor', 'R', 'in phase'), ('inductor', 'jωL', 'current lags 90°'), ('capacitor', '1 / (jωC)', 'current leads 90°')]
    table(ax, 6, H - 2, ['element', 'impedance Z', 'behavior'], rows, [26, 30, 32], 8.5, 22)
    txt(ax, 50, 5, '100 mH at 60 Hz:  ωL = 2π·60·0.1 ≈ 37.7 Ω', 20, C['orange'], bold=True)
    save(fig, path)

def fig_power(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    ax.add_patch(Polygon([(12, 8), (62, 8), (62, 44)], fc=C['pale'], ec='none'))
    arrow(ax, (12, 8), (62, 8), color=C['blue'], lw=4); txt(ax, 37, 4, 'P = 191 W (real: does work)', 18, C['blue'], bold=True)
    arrow(ax, (62, 8), (62, 44), color=C['orange'], lw=4); txt(ax, 64, 26, 'Q = 191 VAR\n(reactive:\nsloshes back\nand forth)', 17, C['orange'], ha='left', bold=True)
    arrow(ax, (12, 8), (62, 44), color=C['purple'], lw=4); txt(ax, 30, 31, 'S = 270 VA', 19, C['purple'], bold=True)
    ax.add_patch(Arc((12, 8), 16, 16, theta1=0, theta2=36, color=C['ink'], lw=2)); txt(ax, 22, 11, '45°', 17)
    txt(ax, 50, 51, 'power factor = cos θ = P / S = 0.71', 21, bold=True)
    save(fig, path)

def fig_3phase(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 2, 600)
    for k, c in zip(range(3), (C['red'], C['ink'], C['blue'])): ax.plot(t, np.cos(2 * np.pi * t - k * 2 * np.pi / 3), color=c, label=f'phase {"ABC"[k]}')
    ax.plot(t, sum(np.cos(2 * np.pi * t - k * 2 * np.pi / 3) for k in range(3)), color=C['green'], ls='--', lw=2, label='sum = 0')
    ax.legend(loc='upper right', ncol=4, fontsize=15); ax.set_ylim(-1.4, 1.6); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('three phases 120° apart → smooth, constant total power', fontsize=19)
    save(fig, path)

def fig_lissajous(path, w, h):
    fig, axs = plot(w, h, ncols=3, grid=False)
    t = X(0, 2 * np.pi, 600)
    for a, (fx, ph, lab) in zip(axs, ((1, 0, 'same f, 0°'), (1, np.pi / 2, 'same f, 90°'), (2, 0, 'f ratio 1 : 2'))):
        a.plot(np.sin(t), np.sin(fx * t + ph), color=C['green'], lw=3); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([]); a.set_title(lab, fontsize=18)
        a.set_facecolor('#0F1A12')
    save(fig, path)

LESSON = {
 'code': 'EGEE 203', 'title': 'Electric Circuits', 'tag': 'Year 2 · Circuits', 'folder': 'EGEE-203 Electric Circuits',
 'slides': [
 {'t': 'title', 'h': 'Electric Circuits', 'sub': 'Ohm, Kirchhoff, Thevenin, transients, phasors and AC power (with lab)', 'img': 'a:hv_lines',
  'say': "Welcome to E G E E two oh three, electric circuits. This is the foundation of everything electrical, from a phone charger to the power grid behind these towers. The good news: the entire course rests on three simple laws. The rest is a toolbox of clever ways to apply them, plus two big ideas, time constants and phasors, that turn hard problems into easy ones. We'll also cover the lab skills, like using an oscilloscope."},

 {'t': 'v', 'h': 'Voltage, current, power', 'img': ['a:breadboard', 'a:scope_screen'], 'reveal': False,   # all four are narrated in beat 0
  'pts': ['Current I: charge flow (amperes)', 'Voltage V: energy per charge (volts) — always between two points', 'Power P = V × I (watts)', 'Passive sign convention: current into + → absorbing power'],
  'say': ["Three quantities run through every circuit. Current is the flow of charge, measured in amperes. Voltage is the energy each coulomb of charge gains or loses between two points, measured in volts. A useful picture: voltage is the pressure, current is the flow rate. And power, the rate energy is delivered, is voltage times current. A five volt U S B port supplying two amps delivers ten watts. One bookkeeping rule, the passive sign convention: if current enters the plus terminal of an element, that element is absorbing power, like a resistor heating up. If it comes out of the plus terminal, it's supplying power, like a battery.",
          "In the lab, you'll build these circuits on a breadboard and measure them with a multimeter and an oscilloscope, which plots voltage against time, like this screen showing a triangle wave and a square wave. The lab sessions in this course start exactly there: learning the scope's timebase, volts per division and triggering."]},

 {'t': 'v', 'h': 'The three laws', 'img': 'fig:divider',
  'pts': ['Ohm: V = I R', 'KCL: currents into a node sum to zero (charge is conserved)', 'KVL: voltages around a loop sum to zero (energy is conserved)', 'Voltage divider: Vx = V · Rx / R_total → 12 · 8/12 = 8 V'],
  'say': ["Ohm's law: the voltage across a resistor equals the current through it times its resistance.",
          "Kirchhoff's current law: whatever current flows into a node must flow out, because charge can't pile up anywhere.",
          "Kirchhoff's voltage law: walk around any closed loop, adding up voltage rises and drops, and you get zero, because energy is conserved. You end up back at the same potential where you started.",
          "Put these together and you get the most useful shortcut in electronics: the voltage divider. Twelve volts across a four k and an eight k in series. The same current flows through both, so the voltage splits in proportion to resistance: twelve times eight over twelve is eight volts across the eight k. You'll use dividers to scale down sensor voltages for an A D C, and to bias transistors, constantly."]},

 {'t': 'v', 'h': 'Nodal analysis: the workhorse method', 'img': ['fig:nodal', 'fig:nodal_eq', 'fig:nodal_eq'],
  'pts': ['Pick a ground; label unknown node voltages', 'KCL at each node, every current = (V_a − V_b)/R', 'Solve the linear system A x = b'],
  'say': ["For bigger circuits, use nodal analysis, which works on any circuit. Pick one node as ground, zero volts. Label the unknown voltages at the other nodes. Here there are two, V A and V B.",
          "At each unknown node, write Kirchhoff's current law, expressing each branch current as the voltage difference divided by the resistance. At node A, the currents leaving through the one k to the source, the two k to ground and the one k to B must sum to zero. At node B, the currents through its two resistors must sum to zero.",
          "That's a system of linear equations, A x equals b, straight from linear algebra. Here it's a two by two matrix. Solving gives V A about five point four five volts and V B about three point six four volts. Circuit simulators like SPICE do exactly this, building and solving matrices with thousands of rows. Mesh analysis is the mirror image: unknown loop currents and Kirchhoff's voltage law around each loop."]},

 {'t': 'v', 'h': 'Thevenin: any circuit is a source and a resistor', 'img': ['fig:thev1', 'fig:thev1', 'fig:thev1', 'fig:thev2'],
  'pts': ['V_th = open-circuit voltage at the terminals', 'R_th = resistance seen with sources turned off', 'Then any load is a one-line calculation', 'Max power to the load when R_L = R_th'],
  'say': ["Now the most powerful idea in the course. Any linear circuit, no matter how complicated, looks from two terminals exactly like one voltage source in series with one resistor. That's the Thevenin equivalent. Let's find it for this circuit.",
          "Step one: the Thevenin voltage is the open circuit voltage at a b, with nothing connected. That's a voltage divider: twelve times twelve over sixteen, which is nine volts.",
          "Step two: turn off the independent sources. A voltage source becomes a wire, a current source becomes an open. Then look back into the terminals. The four k and twelve k are now in parallel: four times twelve over sixteen, three k.",
          "So this whole circuit behaves like a nine volt source with three k of internal resistance. Hook up any load and the answer is one line. And the load gets the most power when its resistance equals the Thevenin resistance, three k here, receiving nine squared over four times three k, about six point seven five milliwatts. Engineers model every sensor, battery and amplifier stage this way."]},

 {'t': 'v', 'h': 'Op amps: the ideal amplifier', 'img': 'fig:opamp',
  'pts': ['Huge gain + negative feedback', 'Rule 1: no current into the inputs', 'Rule 2: the inputs are forced equal (virtual short)', 'Inverting gain = −R_f/R_in = −10 · non-inverting = 1 + R_f/R_in'],
  'say': ["An operational amplifier is a chip with enormous voltage gain, often a hundred thousand or more. On its own that's hard to use, but with negative feedback, a resistor from the output back to the inverting input, it becomes a precise, predictable amplifier.",
          "Two golden rules make analysis easy. First, essentially no current flows into the inputs.",
          "Second, with negative feedback, the op amp adjusts its output until the two input voltages are equal. That's called a virtual short.",
          "Apply them to this inverting amplifier. The plus input is grounded, so the minus input sits at zero volts. The current through R in is v in over one k, and it can't enter the op amp, so it all flows through R f, making v out equal to minus ten times v in. The gain is minus R f over R in. The non inverting version has gain one plus R f over R in. Op amps amplify microphone and sensor signals, build filters, and condition signals before the A D C in nearly every embedded system."]},

 {'t': 'v', 'h': 'Capacitors, inductors and first-order transients', 'img': 'fig:rc',
  'pts': ['Capacitor: i = C dv/dt — voltage can’t jump', 'Inductor: v = L di/dt — current can’t jump', 'Find x(0), x(∞) and τ = RC or L/R', '10 kΩ, 100 μF → τ = 1 s; 63% after 1 τ, done after ~5 τ'],
  'say': ["Capacitors and inductors add time to circuits. A capacitor's current is C times the rate of change of its voltage, so its voltage can't jump instantly; that would take infinite current. At DC, a capacitor acts like an open circuit.",
          "An inductor is the mirror image: its voltage is L times the rate of change of current, so its current can't jump. At DC, it acts like a wire. One trap on every exam: capacitors combine the opposite way from resistors. Capacitors in parallel simply add, because the plate areas add. Capacitors in series combine like resistors in parallel, one over the sum of one overs. Inductors combine just like resistors.",
          "Any circuit with one capacitor or one inductor follows the same recipe, the solution of the first order differential equation you met in math. Find the initial value, the final value, and the time constant, tau, which is R C or L over R. Then the response is the final value plus the initial minus final, times e to the minus t over tau.",
          "Example: a ten k resistor charging a one hundred microfarad capacitor from a five volt step. Tau is one second. After one tau, it's at sixty three percent, about three point one six volts. After five tau, it's within one percent of five volts. In embedded systems, an R C circuit with a ten millisecond time constant is a classic way to debounce a mechanical button."]},

 {'t': 'v', 'h': 'AC circuits with phasors', 'img': ['fig:phasor', 'fig:impedance'],
  'pts': ['A sinusoid at one frequency = magnitude + phase', 'V_m cos(ωt + φ) → phasor V_m∠φ', 'Impedance: Z_R = R, Z_L = jωL, Z_C = 1/(jωC)', 'All DC methods now work with complex numbers'],
  'say': ["For sinusoidal sources, solving differential equations every time would be miserable. Here's the trick. In a linear circuit driven at one frequency, every voltage and current is a sinusoid at that same frequency. The only things that differ are amplitude and phase. So we represent each one by a complex number, a phasor, with that magnitude and angle: Euler's formula from Calculus two at work. On the left, the current lags the voltage by forty five degrees. On the right, the same information as two arrows.",
          "Then every element gets an impedance, a complex resistance. A resistor is R. An inductor is j omega L. A capacitor is one over j omega C. A one hundred millihenry inductor at sixty hertz has an impedance of about thirty seven point seven ohms. Now Ohm's law, dividers, nodal analysis and Thevenin all work exactly as before, just with complex numbers. Differential equations become algebra. In the lab, students verify superposition and Thevenin's theorem in AC networks exactly this way, and measure sinusoidal steady state in R L C circuits."]},

 {'t': 'v', 'h': 'AC power: real, reactive, apparent', 'img': 'fig:power',
  'pts': ['RMS: V_rms = V_peak / √2 (120 V outlet → 170 V peak)', 'Real power P = V_rms I_rms cos θ does work', 'Reactive power Q sloshes back and forth', 'Low power factor costs utilities; capacitors correct it'],
  'say': "With AC, voltage and current aren't always in step, and that changes the power. Take the thirty seven point seven ohm resistor in series with our thirty seven point seven ohm inductor, on a one hundred twenty volt R M S line. The impedance magnitude is fifty three point three ohms at forty five degrees, so the current is two point two five amps, lagging by forty five degrees. The real power, which actually heats the resistor or turns a motor, is V times I times the cosine of the angle: about one hundred ninety one watts. The reactive power, about one hundred ninety one volt amps reactive, just sloshes back and forth between the source and the inductor's magnetic field every cycle, doing no net work. The apparent power is their combination, two hundred seventy volt amps, and the ratio of real to apparent power, point seven one here, is the power factor. Utilities have to supply the full current even though only part of it does work, so large factories with motors are charged for poor power factor, and they install capacitor banks to cancel the inductive current."},

 {'t': 'v', 'h': 'Three-phase power', 'img': ['fig:3phase', 'a:hv_lines'],
  'pts': ['Three sinusoids 120° apart', 'Total power is constant — smooth motors', 'Balanced loads: currents sum to zero', 'V_line = √3 V_phase: 120 V → 208 V'],
  'say': ["Power plants and transmission lines use three phase power: three sinusoids, each shifted by one hundred twenty degrees. At every instant, the three add up to zero, the green dashed line, so in a balanced system there's no need for a heavy return wire, and the total power delivered is perfectly constant instead of pulsing. That's why big motors run smoothly on three phase.",
          "You can spot it in power lines, where conductors come in groups of three. And the voltage between two phases is root three times the voltage of each phase to neutral, which is why U S commercial buildings often have two hundred eight volt service: one hundred twenty times root three."]},

 {'t': 'v', 'h': 'Lab skills: the oscilloscope and Lissajous figures', 'img': ['a:scopes', 'fig:lissajous'],
  'pts': ['Timebase (s/div), volts/div, trigger level', 'AC vs DC coupling; 10× probes', 'X–Y mode: plot one signal against another', 'Lissajous shapes reveal phase and frequency ratio'],
  'say': ["The oscilloscope is the engineer's eyes. On the left is a classic analog scope from the nineteen seventies, and on the right a modern digital one. The key controls: the timebase, in seconds per division across the screen; the vertical scale, in volts per division; and the trigger, which tells the scope when to start drawing so a repeating waveform stands still. A C coupling removes the DC level so you can zoom in on small wiggles, and ten times probes reduce how much the scope disturbs your circuit.",
          "In X Y mode, the scope plots one signal horizontally against another vertically, producing Lissajous figures. Two signals at the same frequency and in phase make a diagonal line. At ninety degrees apart, a circle. In between, an ellipse whose shape tells you the phase shift. And if one frequency is double the other, you get a figure eight. Before digital measurements were everywhere, this was how engineers compared frequencies, and it's exactly what students do in the first labs of this course."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Three laws (**Ohm, KCL, KVL**), one big simplification (**Thevenin**), and two time tools: **τ** for transients and **phasors** for AC.',
  'cap': 'Next: EGEE 303, Electronics — diodes, transistors and amplifiers.',
  'say': "Let's wrap up. Ohm's law, Kirchhoff's current law and Kirchhoff's voltage law underlie everything. Dividers, nodal and mesh analysis, superposition and Thevenin equivalents are organized ways of applying them. Op amps with feedback obey two simple rules. Capacitors and inductors bring time constants and first order transients. Phasors and impedance turn AC analysis into complex algebra, and power factor and three phase explain how the grid really works. Next up, electronics, where we add diodes and transistors. See you there."},
 ]}

# ---------------- whiteboard worked examples (circuits drawn live) ----------------
import board as B
OF = 0.3   # label offset from component bodies

def draw_sp(ax, n, w, h):
    def build(d, elm, v):
        d += (V := elm.SourceV().up().label('12 V', loc='top', ofst=OF).color(v(1)))
        d += elm.Resistor().right().label('R1 = 4 Ω', ofst=OF).color(v(1))
        d += elm.Dot().color(v(1))
        d.push(); d += elm.Resistor().down().label('R2 = 6 Ω', loc='bottom', ofst=OF).color(v(1)); d.pop()
        d += elm.Line().right(3.2).color(v(1))
        d += elm.Resistor().down().label('R3 = 12 Ω', loc='bottom', ofst=OF).color(v(1))
        d += elm.Line().left().to(V.start).color(v(1))
        d += elm.Dot().at((3, 0)).color(v(1))
        d += elm.Label().at((1.5, 2.2)).label('I = 1.5 A').color(v(3, 'red'))
        d += elm.Label().at((2.3, 0.6)).label('1 A').color(v(4, 'red'))
        d += elm.Label().at((5.4, 0.6)).label('0.5 A').color(v(4, 'red'))
        d += elm.Label().at((4.6, 3.6)).label('6 V').color(v(4, 'blue'))
    B.circuit(ax, n, build, fs=28, lw=3)

def draw_nodal(ax, n, w, h):
    def build(d, elm, v):
        d += (V := elm.SourceV().up().label('10 V', loc='top', ofst=OF).color(v(1)))
        d += elm.Resistor().right().label('2 Ω', ofst=OF).color(v(1))
        d += (n1 := elm.Dot().color(v(1)))
        d.push(); d += elm.Resistor().down().label('4 Ω', loc='bottom', ofst=OF).color(v(1)); d.pop()
        d += elm.Resistor().right().label('4 Ω', ofst=OF).color(v(1))
        d += (n2 := elm.Dot().color(v(1)))
        d.push(); d += elm.Resistor().down().label('4 Ω', loc='bottom', ofst=OF).color(v(1)); d.pop()
        d += elm.Line().right(3).color(v(1))
        d += elm.SourceI().down().reverse().label('0.5 A', loc='bottom', ofst=OF).color(v(1))
        d += elm.Line().left().to(V.start).color(v(1))
        d += elm.Ground().at((3, 0)).color(v(1))
        d += elm.Label().at((3, 3.75)).label('V1').color(v(2, 'red')); d += elm.Label().at((6, 3.75)).label('V2').color(v(2, 'red'))
        d += elm.Label().at((3, 4.45)).label('= 6 V').color(v(3, 'green')); d += elm.Label().at((6, 4.45)).label('= 4 V').color(v(3, 'green'))
    B.circuit(ax, n, build, fs=26, lw=3)

def draw_thev(ax, n, w, h):
    def orig(d, elm, v):
        d += (V := elm.SourceV().up().label('12 V', loc='top', ofst=OF).color(v(1)))
        d += elm.Resistor().right().label('6 kΩ', ofst=OF).color(v(1)); d += elm.Dot().color(v(1))
        d.push(); d += elm.Resistor().down().label('3 kΩ', loc='bottom', ofst=OF).color(v(1)); d.pop()
        d += elm.Line().right(2).color(v(1)); d += elm.Dot(open=True).label('a', loc='right').color(v(1))
        d += elm.Line().at(V.start).right(5).color(v(1)); d += elm.Dot(open=True).label('b', loc='right').color(v(1))
    def thev(d, elm, v):
        d += (V := elm.SourceV().up().label('Vth = 4 V', loc='top', ofst=OF).color(v(4, 'green')))
        d += elm.Resistor().right().label('Rth = 2 kΩ', ofst=OF).color(v(4, 'green'))
        d += elm.Resistor().down().label('RL = 2 kΩ', loc='bottom', ofst=OF).color(v(5, 'orange'))
        d += elm.Line().left().to(V.start).color(v(4, 'green'))
        d += elm.Label().at((1.95, 0.8)).label('VL = 2 V').color(v(5, 'red'))
    B.circuit(ax.inset_axes([0, 0.52, 1, 0.48]), n, orig, fs=26, lw=3)
    if n >= 4: B.circuit(ax.inset_axes([0, 0, 1, 0.46]), n, thev, fs=26, lw=3)

def draw_opamp(ax, n, w, h):
    def build(d, elm, v):
        d += (op := elm.Opamp(leads=True).flip().color(v(1)))
        d += elm.Line().at(op.in2).left(1.2).color(v(1)); d += elm.Dot(open=True).label('vin = 0.2 V', loc='left').color(v(1))
        d += elm.Dot().at(op.in1).color(v(2))
        d += (q := elm.Line().at(op.in1).down(1.6).color(v(2)))
        d += elm.Resistor().at(q.end).right().tox(op.out).label('Rf = 10 kΩ', loc='bottom', ofst=OF).color(v(2))
        d += elm.Line().up().toy(op.out).color(v(2)); d += elm.Dot().color(v(2))
        d += elm.Resistor().at(q.end).left().label('Rg = 1 kΩ', loc='bottom', ofst=OF).color(v(2)); d += elm.Ground().color(v(2))
        d += elm.Line().at(op.out).right(1.2).color(v(1)); d += elm.Dot(open=True).label('vout = 2.2 V', loc='right').color(v(4, 'red'))
    B.circuit(ax, n, build, fs=26, lw=3)

def draw_rc(ax, n, w, h):
    def build(d, elm, v):
        d += (V := elm.SourceV().up().label('5 V', loc='top', ofst=OF).color(v(1)))
        d += elm.Switch(action='close').right().label('t = 0', ofst=OF).color(v(1))
        d += elm.Resistor().right().label('10 kΩ', ofst=OF).color(v(1))
        d += elm.Capacitor().down().label('100 µF', loc='bottom', ofst=OF).color(v(1))
        d += elm.Line().left().to(V.start).color(v(1))
    B.circuit(ax.inset_axes([0, 0.55, 1, 0.45]), n, build, fs=26, lw=3)
    if n >= 2:
        X0, Y0, sx, sy = 90, 40, 120, 60
        P = lambda t, vv: (X0 + t * sx, Y0 + vv * sy)
        B.axes(ax, X0, Y0, X0 + 5.6 * sx, Y0 + 5.8 * sy, 't (s)', 'v_C')
        B.ln(ax, [X0, X0 + 5.4 * sx], [Y0 + 5 * sy] * 2, c='gray', lw=1.5, ls='--'); B.lab(ax, X0 - 12, Y0 + 5 * sy, '5', 24, 'gray', ha='right')
        ts = np.linspace(0, 5.4, 120); B.ln(ax, *zip(*[P(t, 5 * (1 - np.exp(-t))) for t in ts]), c='blue', lw=3.5)
    if n >= 3:
        B.dot(ax, *P(1, 3.16), c='red', s=13); B.lab(ax, *P(1.15, 2.7), '1τ: 3.16 V (63%)', 24, 'red', ha='left')
        B.dot(ax, *P(5, 4.97), c='green', s=13); B.lab(ax, *P(4.6, 4.3), '5τ: done', 24, 'green')

B.insert(LESSON, 'The three laws', {'t': 'wb', 'h': 'Worked example: a series-parallel circuit', 'draw': 'sp', 'split': 0.44, 'steps': [
    {'say': "Let's solve a complete circuit. A twelve volt source drives R one, four ohms, in series with R two and R three in parallel. Find every current.",
     'w': [{'d': 1, 'at': 1}, {'m': 'find every current', 'at': 2}]},
    {'say': "First simplify. Six ohms in parallel with twelve ohms is their product over their sum: seventy two over eighteen, four ohms. Add R one in series: the total is eight ohms.",
     'w': [{'m': r'$R_2 \parallel R_3 = \frac{6\cdot 12}{6+12} = 4\ \Omega$', 'at': 1}, {'m': r'$R_{total} = 4 + 4 = 8\ \Omega$', 'at': 2}]},
    {'say': "Ohm's law gives the source current: twelve volts over eight ohms, one and a half amps. All of it flows through R one, which drops one and a half times four, six volts.",
     'w': [{'m': r'$I = \frac{12}{8} = 1.5\ \mathrm{A}$', 'c': 'red'}, {'d': 3, 'at': 0}, {'m': r'$V_{R1} = 1.5 \times 4 = 6\ \mathrm{V}$', 'at': 1}]},
    {'say': "By Kirchhoff's voltage law, the parallel pair gets the remaining six volts. So R two carries six over six, one amp, and R three carries six over twelve, half an amp. Now check with Kirchhoff's current law: one plus a half is one and a half, exactly the current that came in. Always check.",
     'w': [{'m': r'KVL: $12 - 6 = 6\ \mathrm{V}$ across both', 'at': 0}, {'m': r'$I_2 = 6/6 = 1\ \mathrm{A}$,   $I_3 = 6/12 = 0.5\ \mathrm{A}$', 'at': 1}, {'d': 4, 'at': 1}, {'m': r'KCL check: $1 + 0.5 = 1.5\ \mathrm{A}$', 'c': 'green', 'box': True, 'at': 2}]},
]})

B.insert(LESSON, 'Nodal analysis', {'t': 'wb', 'h': 'Worked example: nodal analysis with two unknowns', 'draw': 'nodal', 'split': 0.44, 'steps': [
    {'say': "Here's a circuit with two unknown node voltages. A ten volt source, four resistors and a half amp current source. Step one: choose ground at the bottom and name the unknown nodes V one and V two.",
     'w': [{'d': 1, 'at': 1}, {'d': 2, 'at': 2}, {'m': 'currents leaving each node sum to zero', 'at': 2}]},
    {'say': "Step two: Kirchhoff's current law at V one. Current leaving through the two ohm resistor toward the source, plus current down the four ohm, plus current toward V two, equals zero. Multiply through by four: four V one minus V two equals twenty.",
     'w': [{'m': r'V1:  $\frac{V_1-10}{2} + \frac{V_1}{4} + \frac{V_1-V_2}{4} = 0$', 'at': 1}, {'m': r'$\Rightarrow\ 4V_1 - V_2 = 20$', 'c': 'blue', 'at': 3}]},
    {'say': "At V two, the current leaving through its two resistors equals the half amp the source pushes in. Times four: two V two minus V one equals two.",
     'w': [{'m': r'V2:  $\frac{V_2-V_1}{4} + \frac{V_2}{4} = 0.5$', 'at': 0}, {'m': r'$\Rightarrow\ -V_1 + 2V_2 = 2$', 'c': 'blue', 'at': 1}]},
    {'say': "Two equations, two unknowns. From the second, V one equals two V two minus two. Substitute into the first: seven V two equals twenty eight, so V two is four volts, and V one is six volts. Every current follows instantly. This method scales to circuits with hundreds of nodes, which is exactly what SPICE does.",
     'w': [{'m': r'$V_1 = 2V_2 - 2 \;\Rightarrow\; 7V_2 = 28$', 'at': 1}, {'m': r'$V_2 = 4\ \mathrm{V}$,   $V_1 = 6\ \mathrm{V}$', 'c': 'red', 'box': True, 'at': 2}, {'d': 3, 'at': 2}]},
]})

B.insert(LESSON, 'Thevenin', {'t': 'wb', 'h': 'Worked example: finding a Thevenin equivalent', 'draw': 'thev', 'split': 0.46, 'steps': [
    {'say': "Let's replace this circuit, as seen from terminals a and b, with a single source and a single resistor. A twelve volt source feeds a six kilohm resistor, with a three kilohm resistor across the terminals.",
     'w': [{'d': 1, 'at': 1}, {'m': 'what does the load see at a-b?', 'at': 1}]},
    {'say': "Step one, the Thevenin voltage: the voltage at the open terminals. With nothing connected, it's a voltage divider: twelve times three over nine, four volts.",
     'w': [{'m': r'$V_{th} = 12\cdot\frac{3k}{6k+3k} = 4\ \mathrm{V}$', 'at': 1}]},
    {'say': "Step two, the Thevenin resistance: turn the voltage source off, which means replace it with a wire, and look back into the terminals. Six k and three k are now in parallel: two kilohms.",
     'w': [{'m': r'source off (short):  $R_{th} = 6k \parallel 3k = 2\ \mathrm{k\Omega}$', 'at': 2}]},
    {'say': "So the whole circuit acts like four volts behind two kilohms. Any load is now a one line problem.",
     'w': [{'d': 4, 'at': 0}]},
    {'say': "Connect a two kilohm load. The load voltage is four times two over four, two volts, and its power is two squared over two thousand, two milliwatts. That's the most power this circuit can ever deliver, because the load matches the Thevenin resistance.",
     'w': [{'d': 5, 'at': 0}, {'m': r'$V_L = 4\cdot\frac{2k}{2k+2k} = 2\ \mathrm{V}$,   $P_L = \frac{2^2}{2k} = 2\ \mathrm{mW}$', 'at': 1}, {'m': r'max power when $R_L = R_{th}$', 'c': 'red', 'box': True, 'at': 2}]},
]})

B.insert(LESSON, 'Op amps: the ideal amplifier', {'t': 'wb', 'h': 'Worked example: designing an amplifier with gain 11', 'draw': 'opamp', 'split': 0.4, 'steps': [
    {'say': "A sensor gives us point two volts, and our ADC wants about two volts. Let's design a non-inverting amplifier. The signal goes into the plus input.",
     'w': [{'m': 'need: 0.2 V → about 2 V', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "Feedback goes from the output, through R f, to the minus input, and R g goes from the minus input to ground. By the golden rules, no current enters the inputs, and the op amp drives its output until the minus input equals the plus input.",
     'w': [{'d': 2, 'at': 0}, {'m': 'rule 1: no current into the inputs', 'at': 1}, {'m': r'rule 2: $v_- = v_+ = v_{in}$', 'at': 1}]},
    {'say': "So R f and R g form a voltage divider from the output, and its middle must equal v in. That gives v out over v in equals one plus R f over R g.",
     'w': [{'m': r'$v_{in} = v_{out}\cdot\frac{R_g}{R_f + R_g}$', 'at': 0}, {'m': r'gain $= 1 + \frac{R_f}{R_g}$', 'c': 'blue', 'at': 1}]},
    {'say': "Choose R f equals ten kilohms and R g equals one kilohm: a gain of eleven. Point two volts in gives two point two volts out. Swap the input and ground connections, and you get the inverting amplifier instead, with a gain of minus R f over R g.",
     'w': [{'m': r'$1 + \frac{10k}{1k} = 11$:   $0.2\ \mathrm{V} \to 2.2\ \mathrm{V}$', 'c': 'red', 'box': True}, {'d': 4, 'at': 1}]},
]})

B.insert(LESSON, 'Capacitors, inductors and first-order transients', {'t': 'wb', 'h': 'Worked example: charging a capacitor', 'draw': 'rc', 'split': 0.44, 'steps': [
    {'say': "At time zero, a switch connects a five volt source to a ten kilohm resistor and an empty hundred microfarad capacitor. How does the capacitor voltage change?",
     'w': [{'d': 1, 'at': 0}, {'m': r'$v_C(0) = 0$,   switch closes at $t = 0$', 'at': 1}]},
    {'say': "Use the three step method. Initial value: the capacitor starts empty, zero volts. Final value: after a long time no current flows, so the capacitor reaches five volts. Time constant: R times C, ten thousand times a hundred millionths, one second.",
     'w': [{'m': r'$v(0) = 0$,   $v(\infty) = 5\ \mathrm{V}$', 'at': 2}, {'m': r'$\tau = RC = (10^4)(10^{-4}) = 1\ \mathrm{s}$', 'at': 3}, {'d': 2, 'at': 2}]},
    {'say': "The answer is always final, plus initial minus final, times e to the minus t over tau. Here: five times one minus e to the minus t. After one time constant, it reaches sixty three percent, three point one six volts. After five, it's within one percent of five volts. For engineering purposes, done.",
     'w': [{'m': r'$v(t) = v(\infty) + [v(0) - v(\infty)]\,e^{-t/\tau}$', 'at': 0}, {'m': r'$v(t) = 5(1 - e^{-t})\ \mathrm{V}$', 'c': 'red', 'box': True, 'at': 1}, {'d': 3, 'at': 2}]},
]})

# ---------------- the teacher's pen (circuit marks are in schematic units: one resistor = 3 long) ----------------
G = 'Worked example: a series-parallel circuit'
R1, R2, R3 = ('circle', 1.5, 3, 1.15, 0.6), ('circle', 3, 1.5, 0.62, 1.15), ('circle', 6.2, 1.5, 0.62, 1.15)
B.pen(LESSON, G, 0, {'p': [R1], 'c': 'blue', 'at': 1}, {'p': [('box', 2.35, -0.45, 6.95, 3.35)], 'c': 'orange', 'at': 1})
B.pen(LESSON, G, 1, {'p': [('box', 2.35, -0.45, 6.95, 3.35)], 'c': 'orange', 'at': 1}, {'p': ('underline',), 'on': 'R_{total}', 'at': 2})
B.pen(LESSON, G, 2, {'p': [R1], 'at': 1})
B.pen(LESSON, G, 3, {'p': [R2], 'c': 'blue', 'at': 1}, {'p': [R3], 'c': 'blue', 'at': 1}, {'p': [('circle', 3, 3, 0.42, 0.42)], 'c': 'green', 'at': 2})
G = 'Worked example: nodal analysis with two unknowns'
N1, N2 = ('circle', 3, 3, 0.45, 0.45), ('circle', 6, 3, 0.45, 0.45)
B.pen(LESSON, G, 0, {'p': [('underline', 0, 9, -0.35)], 'c': 'green', 'at': 2}, {'p': [N1, N2], 'at': 2})
B.pen(LESSON, G, 1, {'p': [N1], 'at': 0}, {'p': [('arrow', 2.7, 2.55, 1.4, 2.55), ('arrow', 3.45, 2.4, 3.45, 1.2), ('arrow', 3.4, 2.55, 4.6, 2.55)], 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': [N2], 'at': 0}, {'p': [('arrow', 5.6, 2.55, 4.4, 2.55), ('arrow', 6.45, 2.4, 6.45, 1.2), ('arrow', 8.4, 2.55, 6.6, 2.55)], 'c': 'blue', 'at': 0})
B.pen(LESSON, G, 3, {'p': [N1, N2], 'c': 'green', 'at': 2})
G = 'Worked example: finding a Thevenin equivalent'
B.pen(LESSON, G, 0, {'p': [('circle@0', 5, 3, 0.45, 0.45), ('circle@0', 5, 0, 0.45, 0.45)], 'at': 1})
B.pen(LESSON, G, 1, {'p': [('circle@0', 3, 1.5, 0.62, 1.15)], 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': [('cross@0', 0, 1.5, 34)], 'at': 0}, {'p': [('circle@0', 1.5, 3, 1.15, 0.6), ('circle@0', 3, 1.5, 0.62, 1.15)], 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 4, {'p': [('circle@1', 3, 1.5, 0.62, 1.15)], 'c': 'orange', 'at': 0})
G = 'Worked example: designing an amplifier with gain 11'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'rule 1: no current', 'c': 'blue', 'at': 1}, {'p': ('underline',), 'on': 'rule 2:', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': 'gain $= 1', 'at': 1})
G = 'Worked example: charging a capacitor'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$v(0) = 0$', 'c': 'blue', 'at': 2}, {'p': ('circle',), 'on': r'$\tau = RC', 'at': 3})
B.pen(LESSON, G, 2, {'p': [('circle', 210, 229.6, 30, 30)], 'at': 3}, {'p': [('circle', 690, 338, 30, 30)], 'c': 'green', 'at': 4})

# ---------------- the pen on ordinary slides ----------------
S = 'Voltage, current, power'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'charge flow (amperes)', 'c': 'blue', 'at': 1}, {'p': 'underline', 'on': 'energy per charge (volts)', 'c': 'blue', 'at': 2},
       {'p': 'box', 'on': 'P = V × I', 'at': 4}, {'p': 'underline', 'on': 'current into + → absorbing power', 'c': 'green', 'at': 6})
S = 'The three laws'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'Ohm: V = I R', 'at': 0})
B.spen(LESSON, S, 1, {'fig': [('circle', .71, .17, .035, .07)], 'c': 'blue', 'at': 0, 'dt': 2.0}, {'p': 'underline', 'on': 'currents into a node sum to zero', 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .45, .53, .34, .47)], 'c': 'green', 'at': 0, 'dt': 2.0}, {'p': 'underline', 'on': 'voltages around a loop sum to zero', 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .06, .53, .07, .08)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .29, .06, .12, .06)], 'c': 'blue', 'at': 1, 'dt': 1.2},
       {'fig': [('circle', .55, .53, .12, .07)], 'c': 'blue', 'at': 1, 'dt': 2.2}, {'fig': [('circle', .88, .5, .12, .09)], 'at': 2, 'dt': 4.0},
       {'p': 'box', 'on': '12 · 8/12 = 8 V', 'c': 'green', 'at': 2, 'dt': 4.5})
S = 'Nodal analysis: the workhorse method'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .93, .05, .06)], 'at': 1}, {'fig': [('circle', .5, .13, .04, .08)], 'c': 'blue', 'at': 3},
       {'fig': [('circle', .81, .13, .04, .08)], 'c': 'blue', 'at': 3, 'dt': 1.0})
B.spen(LESSON, S, 1, {'fig': [('underline', .06, .94, .14)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .18, .82, .29)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .23, .39, .77, .61)], 'at': 0}, {'fig': [('box', .22, .82, .77, .94)], 'c': 'green', 'at': 2})
S = 'Thevenin: any circuit is a source and a resistor'
B.spen(LESSON, S, 0, {'fig': [('box', .85, .14, .995, .96)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'V_th = open-circuit voltage', 'c': 'blue', 'at': 0}, {'fig': [('circle', .6, .55, .13, .17)], 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('cross', .21, .53, 34)], 'at': 1}, {'p': 'underline', 'on': 'R_th = resistance seen with sources turned off', 'c': 'blue', 'at': 0},
       {'fig': [('circle', .37, .16, .1, .1)], 'c': 'green', 'at': 3}, {'fig': [('circle', .6, .55, .13, .17)], 'c': 'green', 'at': 3, 'dt': 0.8})
B.spen(LESSON, S, 3, {'fig': [('circle', .19, .55, .19, .08)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .71, .08, .21, .07)], 'c': 'blue', 'at': 0, 'dt': 1.5},
       {'p': 'circle', 'on': 'R_L = R_th', 'c': 'green', 'at': 2})
S = 'Op amps: the ideal amplifier'
B.spen(LESSON, S, 0, {'fig': [('circle', .45, .07, .13, .07)], 'c': 'blue', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'no current into the inputs', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .4, .615, .035, .19)], 'at': 0}, {'p': 'underline', 'on': 'the inputs are forced equal', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .4, .73, .03, .06)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .24, .6, .13, .06)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .86, .58, .14, .06)], 'at': 2, 'dt': 4.0}, {'p': 'circle', 'on': '−R_f/R_in = −10', 'at': 3})
S = 'Capacitors, inductors and first-order transients'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'voltage can’t jump', 'at': 1})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'current can’t jump', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'x(0), x(∞) and τ', 'c': 'blue', 'at': 1}, {'fig': [('underline', .18, .83, .07)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('underline', .38, .96, .975)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .29, .545, .045, .055)], 'at': 2},
       {'fig': [('circle', .6, .43, .1, .04)], 'c': 'green', 'at': 3})
S = 'AC circuits with phasors'
B.spen(LESSON, S, 0, {'fig': [('underline', .1, .56, .045)], 'at': 5}, {'fig': [('circle', .84, .52, .15, .2)], 'c': 'blue', 'at': 6})
B.spen(LESSON, S, 1, *[{'fig': [('box', .06, y0, .94, y1)], 'c': 'blue', 'at': a} for y0, y1, a in ((.21, .37, 1), (.41, .57, 2), (.61, .77, 3))],
       {'fig': [('underline', .18, .82, .95)], 'at': 4})
S = 'AC power: real, reactive, apparent'
B.spen(LESSON, S, 0, {'fig': [('circle', .22, .79, .05, .05)], 'at': 2}, {'fig': [('circle', .39, .92, .19, .045)], 'c': 'blue', 'at': 3},
       {'fig': [('circle', .76, .45, .1, .11)], 'c': 'orange', 'at': 4}, {'fig': [('circle', .29, .41, .08, .045)], 'c': 'purple', 'at': 5},
       {'fig': [('circle', .7, .05, .05, .045)], 'c': 'green', 'at': 5, 'dt': 4.5})
S = 'Three-phase power'
B.spen(LESSON, S, 0, {'fig': [('underline', .16, .88, .58)], 'c': 'green', 'at': 1, 'dt': 2.0}, {'p': 'underline', 'on': 'Total power is constant', 'at': 2})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': 'V_line = √3 V_phase', 'c': 'blue', 'at': 1})
S = 'Lab skills: the oscilloscope'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'Timebase (s/div), volts/div, trigger level', 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, .5, .15, .33)], 'c': 'orange', 'at': a} for x, a in ((.15, 1), (.49, 2), (.82, 4))])

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_phasorrc(ax, n, w, h):
    O = (w * 0.25, h * 0.55); s = 34
    P = lambda re, im: (O[0] + re * s, O[1] + im * s)
    if n >= 1:
        B.arr(ax, O[0] - 40, O[1], O[0] + 12 * s, O[1], 'gray', 2, 14); B.arr(ax, O[0], O[1] - 9 * s, O[0], O[1] + 6 * s, 'gray', 2, 14)
        B.lab(ax, O[0] + 12 * s, O[1] - 26, 'Re', 24, 'gray'); B.lab(ax, O[0] + 26, O[1] + 6 * s, 'Im', 24, 'gray', ha='left')
        B.arr(ax, *O, *P(10, 0), 'blue', 4, 22); B.lab(ax, *P(10.3, 0.8), r'$V_s = 10\angle 0°$', 26, 'blue', ha='left')
    if n >= 2:
        B.arr(ax, *O, *P(5, 5), 'green', 4, 22); B.lab(ax, *P(5.2, 5.6), r'$I$ leads by 45°', 26, 'green', ha='left')
    if n >= 3:
        B.arr(ax, *O, *P(5, -5), 'red', 4, 22); B.lab(ax, *P(5.2, -5.9), r'$V_C = 7.07\angle -45°$', 26, 'red', ha='left')

B.insert(LESSON, 'AC circuits with phasors', {'t': 'wb', 'h': 'Worked example: an RC circuit with phasors', 'draw': 'phasorrc', 'split': 0.58, 'steps': [
    {'say': "Let's actually do a phasor problem, because the complex arithmetic is where students get stuck. A ten volt, one kilohertz sine wave drives a one kilohm resistor in series with a capacitor. At this frequency, the capacitor's impedance works out to minus j one kilohm.",
     'w': [{'m': r'$v_s = 10\cos(2\pi\,1000\,t)$  $\to$  $V_s = 10\angle 0°$', 'at': 1}, {'d': 1, 'at': 1},
           {'m': r'$Z_C = \frac{1}{j\omega C} = -j\,1\ \mathrm{k\Omega}$', 'at': 2}]},
    {'say': "Series impedances add, like resistors, and adding is easiest in rectangular form: one k minus j one k. To divide, switch to polar form: the magnitude is the square root of one plus one, so one point four one four k, at an angle of minus forty five degrees.",
     'w': [{'m': r'$Z = 1k - j1k = 1.414k\,\angle -45°$', 'c': 'blue', 'at': 2},
           {'m': 'add in rectangular,  multiply/divide in polar', 'c': 'gray', 'at': 2}]},
    {'say': "Now Ohm's law with complex numbers. To divide in polar form, divide the magnitudes and subtract the angles. Ten over one point four one four k is seven point oh seven milliamps, at zero minus minus forty five: plus forty five degrees. The current leads the voltage, as it always does in a capacitive circuit.",
     'w': [{'m': r'$I = \frac{10\angle 0°}{1.414k\angle -45°} = 7.07\ \mathrm{mA}\,\angle 45°$', 'c': 'green', 'at': 2}, {'d': 2, 'at': 3}]},
    {'say': "The capacitor's voltage is I times Z C. Multiply in polar: multiply magnitudes and add angles. Seven point oh seven milliamps times one k is seven point oh seven volts, at forty five minus ninety, minus forty five degrees. Finally, convert back to time: seven point oh seven cosine of two pi one thousand t, minus forty five degrees. No differential equation needed.",
     'w': [{'m': r'$V_C = (7.07m\angle 45°)(1k\angle -90°) = 7.07\angle -45°$', 'at': 2}, {'d': 3, 'at': 2},
           {'m': r'$v_C(t) = 7.07\cos(2\pi\,1000\,t - 45°)$', 'c': 'red', 'box': True, 'at': 4}]},
]})

G = 'Worked example: an RC circuit with phasors'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'add in rectangular', 'c': 'gray', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'7.07\ \mathrm{mA}\,\angle 45°', 'c': 'green', 'at': 2})
