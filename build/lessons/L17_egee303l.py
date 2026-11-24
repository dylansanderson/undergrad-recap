import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import schemdraw, schemdraw.elements as elm
X = np.linspace

def fig_loading(path, w, h):
    fig, ax = plot(w, h)
    rin = np.logspace(3, 8, 200); rth = 50e3
    ax.semilogx(rin, 100 * rin / (rin + rth), color=C['blue'])
    for r, lab, xy in ((1e6, '1 MΩ (×1 probe): reads 95%', (3e3, 72)), (1e7, '10 MΩ (×10 probe / DMM): 99.5%', (3e3, 56))):
        y = 100 * r / (r + rth); soliddot(ax, r, y, C['orange']); ax.annotate(lab, (r, y), xy, fontsize=15, color=C['orange'], arrowprops=dict(arrowstyle='->', color=C['orange']))
    ax.set_xlabel('meter input resistance (Ω)'); ax.set_ylabel('% of true voltage read'); ax.set_ylim(0, 105)
    ax.set_title('measuring a node with R_th = 50 kΩ: the meter is part of the circuit', fontsize=17)
    save(fig, path)

def fig_ground(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    box(ax, 4, 18, 22, 18, 'circuit\n(powered from\nwall supply)', fc=C['lblue'], fs=16)
    box(ax, 72, 18, 24, 18, 'oscilloscope\n(chassis tied\nto earth)', fc=C['pale'], ec=C['gray'], fs=16)
    line(ax, [(26, 30), (72, 30)], C['blue'], 2.5); txt(ax, 49, 33, 'probe tip', 16, C['blue'])
    line(ax, [(26, 22), (40, 22), (40, 12), (72, 12), (72, 18)], C['red'], 2.5); txt(ax, 56, 9, 'ground clip = earth!', 16, C['red'], bold=True)
    txt(ax, 50, 44, 'Clip ground to a non-ground node → you short it to earth through the scope', 17, C['red'])
    txt(ax, 50, 3, 'fix: use two channels and math (A − B), or a differential probe', 16, C['mut'])
    save(fig, path)

def fig_zener(path, w, h):
    def b(d):
        d += elm.SourceV().up().label('V_in\n9–12 V')
        d += elm.Resistor().right().label('R_s')
        d += elm.Dot(); d.push()
        d += elm.Zener().down().reverse().label('5.1 V\nZener', loc='top')
        d += elm.Line().left(); d.pop()
        d += elm.Line().right(3); d += elm.Resistor().down().label('load', loc='bottom')
        d += elm.Line().left(3)
    schem(path, b)

def fig_clip(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    t = X(0, 2, 600); v = 5 * np.sin(2 * np.pi * t)
    a1.plot(t, v, color=C['gray'], lw=1.5, label='input'); a1.plot(t, np.minimum(v, 0.7), color=C['blue'], label='clipper (limits at +0.7 V)'); a1.legend(loc='lower left', fontsize=14)
    a2.plot(t, v, color=C['gray'], lw=1.5, label='input'); a2.plot(t, v + 4.3, color=C['orange'], label='clamper (shifts DC level)'); a2.legend(loc='lower left', fontsize=14)
    a2.set_xticks([])
    save(fig, path)

def fig_bjt_switch(path, w, h):
    def b(d):
        d += elm.Vdd().label('+12 V')
        d += (T := elm.Dot())
        d += elm.Inductor2().down().label('relay coil\n60 mA', loc='top')
        d += (Cn := elm.Dot())
        d += (Q := elm.BjtNpn(circle=True).theta(0).anchor('collector'))
        d += elm.Ground().at(Q.emitter)
        d += elm.Line().left(1).at(Q.base); d += elm.Resistor().left().label('R_B 2.2 kΩ', loc='top'); d += elm.Dot(open=True).label('3.3 V pin', loc='left', color=C['blue'])
        d += elm.Line().at(T.center).right(3)
        d += elm.Diode().down().reverse().label('flyback', loc='bottom', color=C['orange'])
        d += elm.Line().left(3)
    schem(path, b)

def fig_curves(path, w, h):
    fig, ax = plot(w, h)
    vce = X(0, 10, 300); VA = 60
    for ib, c in ((10, C['gray']), (20, C['green']), (30, C['blue']), (40, C['purple'])):
        ic = 0.1 * ib * (1 - np.exp(-vce / 0.15)) * (1 + vce / VA)
        ax.plot(vce, ic, color=c, label=f'I_B = {ib} μA')
    ax.set_xlabel('V_CE (V)'); ax.set_ylabel('I_C (mA)'); ax.legend(loc='upper left', fontsize=15, ncol=2)
    ax.axvspan(0, 0.3, color=C['lred'], alpha=0.6); ax.text(0.35, 0.3, '← saturation', fontsize=15, color=C['red'])
    ax.text(5, 0.6, 'active region: I_C ≈ β I_B  (β ≈ 100)\nslight upward slope = Early effect', fontsize=15)
    ax.set_ylim(0, 5.2)
    save(fig, path)

def fig_mirror(path, w, h):
    def b(d):
        d += (Q1 := elm.BjtNpn(circle=True).reverse().label('Q1', loc='left'))
        d += (Q2 := elm.BjtNpn(circle=True).at((Q1.base[0] + 1.6, Q1.base[1])).anchor('base').label('Q2', loc='right'))
        d += elm.Line().at(Q1.base).to(Q2.base)
        d += elm.Line().at(Q1.collector).up(0.6); d += (C1 := elm.Dot())
        d += elm.Line().at(C1.center).tox(Q1.base[0] + 0.8); d += elm.Line().toy(Q1.base)
        d += elm.Resistor().up().at(C1.center).label('R_ref'); d += elm.Vdd().label('V_CC')
        d += elm.Ground().at(Q1.emitter); d += elm.Ground().at(Q2.emitter)
        d += elm.Line().up(0.6).at(Q2.collector); d += elm.Resistor().up().label('load', loc='bottom'); d += elm.Vdd()
    schem(path, b)

def fig_bias(path, w, h):
    fig, ax = plot(w, h, grid=False)
    betas = np.array([50, 100, 200, 300])
    fixed = 0.026 * 0 + betas * 11.3e-6 * 1000
    divider = ((2.13 - 0.7) / 1.0) * betas / (betas + 1) / (1 + 8.25 / ((betas + 1) * 1.0))
    xi = np.arange(4); wd = 0.38
    ax.bar(xi - wd / 2, fixed, wd, color=C['red'], label='fixed base bias')
    ax.bar(xi + wd / 2, divider, wd, color=C['green'], label='divider + R_E bias')
    ax.set_xticks(xi); ax.set_xticklabels([f'β = {b}' for b in betas]); ax.set_ylabel('collector current (mA)'); ax.legend(loc='upper left')
    ax.set_title('same circuit, different transistors: divider bias barely moves', fontsize=18)
    save(fig, path)

def fig_report(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    parts = [('Objective', 'what are we testing?'), ('Theory / pre-lab', 'calculations & predictions'), ('Procedure', 'steps, schematic, equipment'),
             ('Data', 'tables + plots with units'), ('Analysis', 'theory vs measured, % error'), ('Conclusion', 'what matched, what didn’t, why')]
    for i, (t, d) in enumerate(parts):
        y = 50 - i * 8.2
        box(ax, 8, y - 6.4, 28, 6.8, t, fc=C['lblue'] if i % 2 == 0 else C['lorange'], ec=C['blue'] if i % 2 == 0 else C['orange'], fs=17, bold=True, r=0.4)
        txt(ax, 40, y - 3, d, 17, C['ink'], ha='left')
    save(fig, path)

LESSON = {
 'code': 'EGEE 303L', 'title': 'Electronics Laboratory', 'tag': 'Year 3 · Electronics', 'folder': 'EGEE-303L Electronics Lab',
 'slides': [
 {'t': 'title', 'h': 'Electronics Laboratory', 'sub': 'Measuring real diodes and transistors — and learning why the numbers never quite match', 'img': 'a:lab_bench',
  'say': "Welcome to E G E E three oh three L, the electronics lab. The lecture course gave you equations. The lab is where you discover that real components, real instruments and real wires don't quite follow them, and you learn to explain why. In this lecture, we'll walk through the core experiments: measurement basics, power supply circuits, diode shaping circuits, transistor switches, characteristic curves, current sources and stable biasing, plus how to write a lab report that an engineer would trust. Many students did these labs in simulation, with NI Multisim, but every one of them can be done on a real bench."},

 {'t': 'v', 'h': 'Every meter changes what it measures', 'img': ['a:multimeter', 'fig:loading'],
  'pts': ['Voltmeter: needs R_in ≫ R_th of the node', 'Ammeter: needs R ≪ the circuit (goes in series!)', 'Scope probe: 1 MΩ (×1) or 10 MΩ (×10)', 'Always ask: is my instrument part of the circuit?'],
  'say': ["The first lesson of every lab: your instrument becomes part of the circuit. A voltmeter connects in parallel with what it measures, and it has a finite input resistance, so it draws a little current and pulls the voltage down. An ammeter must be inserted in series, and it adds a little resistance.",
          "How much does it matter? Suppose you measure a node whose Thevenin resistance is fifty kilohms. A scope probe at times one has one megohm of input resistance, so you read about ninety five percent of the true value, a five percent error from the meter alone. Switch the probe to times ten, or use a ten megohm multimeter, and you read ninety nine and a half percent. The rule: the meter's input resistance must be much larger than the Thevenin resistance of the node you're probing. When your measurement disagrees with your calculation, the meter is always a suspect."]},

 {'t': 'v', 'h': 'Grounding: the oscilloscope trap', 'img': 'fig:ground',
  'pts': ['Scope ground clip is tied to earth via the power cord', 'Clip it to a non-ground node → short circuit', 'Use 2 channels + math (A − B) for floating voltages', 'Or a differential probe'],
  'say': ["Here's a classic way to destroy a circuit, or a scope. The ground clip on an ordinary oscilloscope probe is connected to the scope's chassis, which is connected to earth through the power cord's third prong.",
          "If your circuit is also referenced to earth, and you clip the probe's ground to some node that isn't ground, you've just connected that node directly to earth. Current flows through the probe's ground lead, and something gets damaged.",
          "To measure a voltage across a component that isn't at ground, use two channels, one on each side, both with grounds at true ground, and let the scope compute A minus B.",
          "Or use a differential probe, designed for exactly this. On a professional bench, knowing where ground really is matters as much as knowing Ohm's law."]},

 {'t': 'v', 'h': 'Lab: AC-to-DC power supplies', 'img': ['a:bridge_rect', 'fig:zener'],
  'pts': ['Transformer → rectifier → filter capacitor → regulator', 'Half-wave ripple at f; full-wave ripple at 2f', 'Ripple ≈ I_load / (f_ripple · C)', 'Zener holds V_Z; R_s must still feed it at the lowest input'],
  'say': ["In the power supply labs, students build the chain inside every wall adapter. A transformer steps the voltage down, a rectifier makes it one polarity, a capacitor smooths it, and a regulator holds it steady. A half wave rectifier uses one diode and ripples at the line frequency. A bridge uses both halves of the cycle, so its ripple is at twice the frequency and smaller, but the current passes through two diodes, costing two diode drops. Ripple is roughly the load current divided by the ripple frequency times the capacitance: draw a hundred milliamps from a full wave supply at one hundred twenty hertz ripple with a one thousand microfarad capacitor, and you get about point eight volts of ripple.",
          "A simple regulator uses a Zener diode, which is designed to operate in reverse breakdown, where it holds an almost constant voltage, five point one volts here. The series resistor drops the difference. The design trap: at the lowest input voltage and the highest load current, the resistor must still supply enough current for the load plus the Zener's minimum current. Otherwise the Zener drops out of regulation and the output sags."]},

 {'t': 'v', 'h': 'Lab: clippers and clampers', 'img': 'fig:clip',
  'pts': ['Clipper: diodes limit how far a signal can swing', 'Protects inputs from overvoltage', 'Clamper: capacitor + diode shift the DC level', 'Stack clampers → voltage doublers / multipliers'],
  'say': ["Diodes can also shape waveforms. A clipper uses a diode to limit how far a signal can swing. Here, whenever the input tries to go above about point seven volts, the diode turns on and holds it there. The same idea protects microcontroller inputs: tiny clamp diodes inside the chip keep input pins from going far beyond the supply voltage.",
          "A clamper uses a capacitor and a diode to shift the entire waveform's DC level, without changing its shape. The capacitor charges to the peak on one half cycle and then adds that voltage to the signal. Chain clampers with rectifiers and you get voltage doublers and multipliers, which is how old televisions and some modern sensors generate high voltages from low ones."]},

 {'t': 'v', 'h': 'Lab: the transistor as a switch', 'img': 'fig:bjt_switch',
  'pts': ['Goal: drive the BJT hard into saturation', 'I_B must exceed I_C / β_min (with 2–10× overdrive)', '60 mA relay, β_min = 50 → I_B > 1.2 mA', 'R_B = (3.3 − 0.7) / 1.2 mA ≈ 2.2 kΩ · flyback diode!'],
  'say': ["When a transistor is used as a switch, you want it either fully off or fully on, in saturation, where the collector to emitter voltage drops to about point two volts, so the transistor wastes very little power.",
          "To guarantee saturation, supply more base current than the collector current divided by the smallest beta the part might have, with some extra margin, called overdrive.",
          "Example: switching a sixty milliamp relay coil from a three point three volt microcontroller pin. With a worst case beta of fifty, you need at least one point two milliamps of base current.",
          "The base resistor drops three point three minus point seven volts, so two point six volts over one point two milliamps is about two point two kilohms. A smaller resistor gives more overdrive. And because a relay coil is an inductor, add the flyback diode across it. In the transistor switch lab, students see exactly what happens to the collector voltage at turn off with and without that diode."]},

 {'t': 'v', 'h': 'Lab: BJT characteristic curves', 'img': 'fig:curves',
  'pts': ['Sweep V_CE for several fixed base currents', 'Active region: flat lines spaced by β', 'Saturation near the y-axis', 'Early effect: slope → output resistance r_o = V_A / I_C'],
  'say': ["To see a transistor's personality, measure its characteristic curves: hold the base current constant, sweep the collector to emitter voltage, and record the collector current. Repeat for several base currents.",
          "In the active region, the curves are almost flat, and they're spaced evenly: every ten microamps of base current adds about one milliamp of collector current. Divide and you get beta, about one hundred here. That flatness is what makes the transistor act like a current source.",
          "Near the y axis, the curves bend down sharply. That's saturation, where the transistor is fully on, the switch region from the previous slide.",
          "And the curves aren't perfectly flat: they slope slightly upward, the Early effect. Extend the lines backwards and they meet near a point called minus V A, the Early voltage. That slope sets the transistor's output resistance, which limits how much gain an amplifier can achieve."]},

 {'t': 'v', 'h': 'Lab: current sources and the current mirror', 'img': 'fig:mirror',
  'pts': ['Active-region transistor ≈ constant current source', 'I_C ≈ (V_B − 0.7) / R_E, nearly independent of load', 'Mirror: Q1 sets V_BE, matched Q2 copies the current', 'The most common building block inside analog ICs'],
  'say': ["Because the collector current barely depends on the collector voltage in the active region, a transistor makes a good constant current source. Fix the base voltage, add an emitter resistor, and the current is set by V B minus point seven over R E, almost regardless of the load. That holds until the load voltage gets so large that the transistor saturates, a limit called the compliance range.",
          "The current mirror is an even neater trick. Q one is wired as a diode, with its collector tied to its base, and a resistor sets its current. Since Q two shares the same base emitter voltage, and the two transistors are matched, Q two carries the same current, copying, or mirroring, the reference. Inside integrated circuits, where matched transistors are easy to make side by side, current mirrors are everywhere, biasing almost every analog stage, including the inputs of op amps."]},

 {'t': 'v', 'h': 'Lab: stable bias that doesn’t depend on β', 'img': 'fig:bias',
  'pts': ['β varies 2–3× between parts and with temperature', 'Fixed base bias: I_C ∝ β — unreliable', 'Stiff divider + R_E: I_C set by resistors', 'Rule of thumb: R₂ ≤ 0.1 β R_E · bypass R_E for AC gain'],
  'say': ["Here's the most important design lesson of the lab. Beta varies a lot: two transistors with the same part number can differ by a factor of two or three, and beta also changes with temperature.",
          "With simple fixed base bias, a single resistor feeding the base, the collector current is proportional to beta. Swap the transistor and the operating point moves wildly, as the red bars show, and your amplifier may clip or even saturate.",
          "With the four resistor divider bias and an emitter resistor from the electronics course, the base voltage is set by the divider, and the emitter current by that voltage and R E. Beta hardly matters: the green bars barely move from beta fifty to beta three hundred. The trick is a stiff divider, one whose current is large compared to the base current. A rule of thumb is R two at most a tenth of beta times R E.",
          "The emitter resistor reduces the AC gain, so designers often bypass it with a capacitor: it disappears for AC signals but still stabilizes the DC bias. In the bias stability lab, students design exactly this and test it with transistors of different beta."]},

 {'t': 'v', 'h': 'Writing a lab report engineers trust', 'img': 'fig:report',
  'pts': ['State what you expected before measuring', 'Show data with units, uncertainty and plots', 'Compare theory vs measurement: % error', 'Explain differences: tolerances, meter loading, temperature'],
  'say': ["A lab report is how engineers convince other engineers. The structure is always similar: objective, theory and pre lab calculations, procedure, data, analysis and conclusion.",
          "The most important habit is predicting before measuring. If you calculate first, you'll notice immediately when a measurement doesn't make sense.",
          "Present data in tables and plots with units, and compute the percent error between theory and measurement.",
          "Then explain the differences honestly. Resistors are typically plus or minus five percent. Beta varies. Meters load circuits. Temperature drifts. A report that says the measured gain was eight percent below the prediction, mostly because the transistor's beta was lower than the datasheet's typical value, is worth far more than one with perfect looking numbers. This course carried part of the engineering writing requirement for exactly this reason."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Predict, then measure. Respect **meter loading** and **ground**. Design so the circuit works with **any** transistor off the shelf.',
  'cap': 'Next: EGEE 323, Engineering Probability and Statistics.',
  'say': "To recap. Instruments are part of the circuit, so choose them so they barely disturb it, and be careful where the scope's ground goes. Power supplies are rectifier, filter and regulator. Diodes clip and clamp signals. Transistors switch loads when driven into saturation, act as current sources in the active region, and mirrors copy currents. Good bias design makes a circuit work regardless of beta. And a good lab report predicts, measures, compares and explains. Next, we move to probability and statistics, the math of uncertainty and noise. See you there."},
 ]}

# ---------------- whiteboard worked examples (circuits drawn live) ----------------
import board as B
OF = 0.3

def draw_loading(ax, n, w, h):
    def build(d, elm, v):
        d += (V := elm.SourceV().up().label('10 V', loc='top', ofst=OF).color(v(1)))
        d += elm.Resistor().right().label('1 MΩ', ofst=OF).color(v(1)); d += (a := elm.Dot().color(v(1)))
        d += elm.Resistor().down().label('1 MΩ', loc='bottom', ofst=OF).color(v(1))
        d += elm.Line().left().to(V.start).color(v(1))
        d += elm.Line().at(a.center).right(2.2).color(v(2, 'red'))
        d += elm.MeterV().down().label('DMM 10 MΩ', loc='bottom', ofst=OF).color(v(2, 'red'))
        d += elm.Line().left(2.2).color(v(2, 'red'))
    B.circuit(ax, n, build, fs=28, lw=3)

def draw_switch(ax, n, w, h):
    def build(d, elm, v):
        d += (q := elm.BjtNpn(circle=True).theta(0).color(v(1)))
        d += elm.Ground().at(q.emitter).color(v(1))
        d += elm.Resistor().up().at(q.collector).label('LED strip\n200 mA', loc='bottom', ofst=OF).color(v(1)); d += elm.Vdd().label('5 V').color(v(1))
        d += elm.Resistor().left().at(q.base).label('RB = ?', ofst=OF).color(v(2, 'red')); d += elm.Dot(open=True).label('3.3 V pin', loc='left').color(v(2, 'red'))
    B.circuit(ax, n, build, fs=28, lw=3)

B.insert(LESSON, 'Every meter changes what it measures', {'t': 'wb', 'h': 'Worked example: when your meter lies', 'draw': 'loading', 'split': 0.48, 'steps': [
    {'say': "Two one megohm resistors divide ten volts. On paper, the middle sits at exactly five volts. Let's measure it with a typical digital multimeter, which has an input resistance of ten megohms.",
     'w': [{'d': 1, 'at': 0}, {'m': 'theory: 5.00 V', 'at': 1}, {'d': 2, 'at': 2}]},
    {'say': "The meter is now part of the circuit. Its ten megohms sits in parallel with the bottom resistor: one meg in parallel with ten meg is about point nine one megohms.",
     'w': [{'m': r'$1M \parallel 10M = \frac{1 \times 10}{1 + 10} = 0.909\ \mathrm{M\Omega}$', 'at': 1}]},
    {'say': "So the divider is really one meg over point nine one meg. The meter reads ten times point nine one over one point nine one: about four point seven six volts. That's nearly five percent low, and the meter is working perfectly. It's the circuit that changed.",
     'w': [{'m': r'reads $10\cdot\frac{0.909}{1 + 0.909} = 4.76\ \mathrm{V}$', 'c': 'red', 'box': True, 'at': 1}, {'m': r'error $= \frac{5 - 4.76}{5} = 4.8\%$', 'at': 3}]},
    {'say': "The rule: a voltmeter's resistance must be much larger, say a hundred times larger, than the resistance of the node you're measuring. In your lab report, an unexplained five percent error like this is exactly what you should catch and explain.",
     'w': [{'m': r'need $R_{meter} \gg R_{node}$  (100× or more)', 'c': 'green', 'gap': 10, 'at': 0}]},
]})

B.insert(LESSON, 'Lab: the transistor as a switch', {'t': 'wb', 'h': 'Worked example: designing a transistor switch', 'draw': 'switch', 'split': 0.5, 'steps': [
    {'say': "Let's design a switch for a five volt LED strip that draws two hundred milliamps, controlled by a three point three volt microcontroller pin. The datasheet promises a beta of at least one hundred.",
     'w': [{'d': 1, 'at': 0}, {'m': r'$I_C = 200\ \mathrm{mA}$,   $\beta_{min} = 100$', 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "To saturate, the base current must be at least the collector current over beta: two hundred milliamps over a hundred, two milliamps. Then overdrive it by two, to four milliamps, so it stays saturated even with a weak transistor or a cold day.",
     'w': [{'m': r'$I_{B,min} = \frac{200\ \mathrm{mA}}{100} = 2\ \mathrm{mA}$', 'at': 1}, {'m': r'overdrive 2×:  $I_B = 4\ \mathrm{mA}$', 'at': 2}]},
    {'say': "The base resistor drops the pin voltage minus the point seven volt base emitter drop. Three point three minus point seven is two point six volts, over four milliamps: six hundred fifty ohms. Pick the nearest standard value below, six twenty.",
     'w': [{'m': r'$R_B = \frac{3.3 - 0.7}{4\ \mathrm{mA}} = 650\ \Omega$', 'at': 2}, {'m': r'use $620\ \Omega$', 'c': 'red', 'box': True, 'at': 3}]},
    {'say': "One more check: four milliamps is within what the pin can safely supply. In saturation, the transistor drops only about point two volts, so it wastes about forty milliwatts. If the load were a relay or a motor, you'd add a flyback diode, just like the MOSFET driver in electronics.",
     'w': [{'m': r'saturated: $P \approx 0.2 \times 0.2 = 40\ \mathrm{mW}$', 'at': 1}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: when your meter lies'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$1M \parallel 10M', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'error $=', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': r'need $R_{meter}', 'c': 'green', 'at': 0})
G = 'Worked example: designing a transistor switch'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$I_{B,min}', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': 'overdrive 2', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': 'saturated:', 'c': 'green', 'at': 1})

# ---------------- the pen on ordinary slides ----------------
S = 'Every meter changes what it measures'
B.spen(LESSON, S, 1, {'fig': [('circle', .57, .17, .04, .05)], 'at': 2}, {'fig': [('circle', .7, .14, .04, .05)], 'c': 'green', 'at': 3},
       {'p': 'underline', 'on': 'R_in ≫ R_th', 'c': 'blue', 'at': 4})
S = 'Grounding: the oscilloscope trap'
B.spen(LESSON, S, 0, {'fig': [('box', .71, .25, .97, .64)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .55, .78, .17, .07)], 'at': 0}, {'fig': [('cross', .29, .55, 26)], 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .17, .83, .91)], 'c': 'green', 'at': 0})
S = 'Lab: AC-to-DC power supplies'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'Transformer → rectifier → filter capacitor → regulator', 'c': 'blue', 'at': 1},
       {'p': 'box', 'on': 'Ripple ≈ I_load / (f_ripple · C)', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('circle', .47, .68, .15, .17)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .4, .08, .06, .08)], 'at': 1},
       {'p': 'underline', 'on': 'R_s must still feed it at the lowest input', 'at': 2})
S = 'Lab: clippers and clampers'
B.spen(LESSON, S, 0, {'fig': [('circle', .67, .21, .09, .05)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('arrow', .65, .87, .65, .66)], 'c': 'orange', 'at': 0, 'dt': 2.5})
S = 'Lab: the transistor as a switch'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'I_B must exceed I_C / β_min', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .47, .42, .12, .12)], 'c': 'blue', 'at': 0}, {'p': 'box', 'on': 'I_B > 1.2 mA', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .32, .74, .12, .07)], 'c': 'green', 'at': 0}, {'fig': [('circle', .79, .32, .08, .1)], 'c': 'orange', 'at': 2})
S = 'Lab: BJT characteristic curves'
B.spen(LESSON, S, 1, {'fig': [('box', .2, .24, .92, .66)], 'c': 'blue', 'at': 0}, {'fig': [('arrow', .95, .67, .95, .49)], 'at': 0, 'dt': 4.0})
B.spen(LESSON, S, 2, {'fig': [('circle', .065, .52, .04, .36)], 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('underline', .52, .93, .73)], 'c': 'purple', 'at': 0})
S = 'Lab: current sources and the current mirror'
B.spen(LESSON, S, 0, {'p': 'box', 'on': 'I_C ≈ (V_B − 0.7) / R_E', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .3, .57, .55, .8)], 'at': 1}, {'fig': [('circle', .57, .78, .3, .1)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .58, .77, .07, .07)], 'c': 'green', 'at': 2, 'dt': 2.5})
S = 'Lab: stable bias that doesn’t depend on β'
B.spen(LESSON, S, 1, {'fig': [('circle', .78, .4, .05, .3)], 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .14, .82, .875)], 'c': 'green', 'at': 1}, {'p': 'underline', 'on': 'Stiff divider + R_E', 'c': 'green', 'at': 2})
S = 'Writing a lab report engineers trust'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'State what you expected before measuring', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': '% error', 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'tolerances, meter loading, temperature', 'c': 'green', 'at': 1})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Lab: AC-to-DC power supplies', {'t': 'wb', 'h': "Worked example: sizing a Zener regulator's resistor", 'steps': [
    {'say': "Let's work the Zener design problem, because it's always about the worst case. The unregulated input swings between nine and twelve volts. We want five point one volts out, for a load that draws up to twenty milliamps, and the Zener needs at least five milliamps to stay in regulation.",
     'w': [{'m': r'$V_{in} = 9 \ldots 12\ \mathrm{V}$,   $V_Z = 5.1\ \mathrm{V}$', 'at': 1},
           {'m': r'$I_{L,max} = 20\ \mathrm{mA}$,   $I_{Z,min} = 5\ \mathrm{mA}$', 'at': 3}]},
    {'say': "Worst case one, the hardest for regulation: lowest input and heaviest load. The resistor must still pass the load current plus the Zener's minimum: twenty five milliamps, from only nine minus five point one, three point nine volts. So R s can be at most three point nine over twenty five milliamps, about one hundred fifty six ohms. Choose one fifty.",
     'w': [{'m': 'worst case 1: lowest $V_{in}$, heaviest load', 'c': 'blue', 'at': 1},
           {'m': r'$R_s \leq \frac{9 - 5.1}{20 + 5\ \mathrm{mA}} = 156\ \Omega$  $\to$  use $150\ \Omega$', 'at': 3}]},
    {'say': "Worst case two, the hardest on the Zener: highest input and no load at all. Now every bit of the resistor's current goes through the Zener. That's twelve minus five point one, over one fifty: forty six milliamps.",
     'w': [{'m': 'worst case 2: highest $V_{in}$, no load', 'c': 'red', 'at': 0},
           {'m': r'$I_Z = \frac{12 - 5.1}{150} = 46\ \mathrm{mA}$', 'at': 2}]},
    {'say': "The Zener dissipates five point one volts times forty six milliamps, about a quarter of a watt. So a quarter watt Zener would be on the edge. Pick a half watt part. Two worst cases, one for each failure mode: that's how every regulator, and most real designs, are sized.",
     'w': [{'m': r'$P_Z = 5.1 \times 0.046 \approx 0.24\ \mathrm{W}$  $\to$  use a 0.5 W Zener', 'c': 'green', 'box': True, 'at': 2}]},
]})

G = "Worked example: sizing a Zener regulator's resistor"
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'use $150\ \Omega$', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'= 46\ \mathrm{mA}$', 'c': 'red', 'at': 2})
