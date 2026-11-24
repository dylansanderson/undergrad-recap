import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import schemdraw, schemdraw.elements as elm
X = np.linspace

def fig_doping(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    box(ax, 4, 10, 44, 34, '', fc=C['lred'], ec=C['red']); box(ax, 52, 10, 44, 34, '', fc=C['lblue'], ec=C['blue'])
    txt(ax, 26, 50, 'p-type (boron): extra holes', 19, C['red'], bold=True); txt(ax, 74, 50, 'n-type (phosphorus): extra electrons', 19, C['blue'], bold=True)
    rng = np.random.default_rng(3)
    for _ in range(26):
        ax.add_patch(Circle((rng.uniform(7, 37), rng.uniform(13, 41)), 1.1, fc='white', ec=C['red'], lw=1.8, zorder=4))
        dot(ax, rng.uniform(63, 93), rng.uniform(13, 41), 1.0, C['blue'])
    ax.add_patch(Rectangle((40, 10), 20, 34, fc='#F2F2F2', ec='none', alpha=0.95, zorder=3)); txt(ax, 50, 27, 'depletion\nregion\n(no free\ncarriers)', 16, C['mut'])
    for y in (16, 24, 32, 40): txt(ax, 43, y, '−', 18, C['red'], bold=True); txt(ax, 57, y, '+', 18, C['blue'], bold=True)
    txt(ax, 50, 4, 'pn junction: a built-in barrier (~0.7 V in silicon) — the heart of diodes and transistors', 15)
    save(fig, path)

def fig_diode_iv(path, w, h):
    fig, ax = plot(w, h)
    v = X(-1.0, 0.75, 400); i = 1e-12 * (np.exp(v / 0.026) - 1) * 1000
    ax.plot(v, np.clip(i, -0.5, 25), color=C['blue']); axes0(ax)
    ax.set_xlabel('diode voltage (V)'); ax.set_ylabel('current (mA)'); ax.set_ylim(-2, 25)
    note(ax, 0.05, 20, 'forward: current rises\nexponentially past ~0.6–0.7 V', C['blue'], 17)
    note(ax, -0.95, 4, 'reverse: only tiny\nleakage current', C['red'], 17)
    ax.set_title('I = I_S (e^(V/V_T) − 1),   V_T ≈ 26 mV', fontsize=19)
    save(fig, path)

def fig_loadline(path, w, h):
    fig, ax = plot(w, h)
    v = X(0, 0.8, 400); i = 1e-12 * (np.exp(v / 0.026) - 1) * 1000
    ax.plot(v, i, color=C['blue'], label='diode curve'); vl = X(0, 5, 10)
    ax.plot(vl, (5 - vl) / 1.0, color=C['orange'], label='load line  I = (5 − V)/1 kΩ')
    soliddot(ax, 0.68, 4.32, C['red'], 13); note(ax, 0.9, 3.6, '← Q-point ≈ (0.68 V, 4.3 mA)', C['red'], 18)
    ax.set_xlim(0, 5); ax.set_ylim(0, 6.8); ax.set_xlabel('V (V)'); ax.set_ylabel('I (mA)'); ax.legend(loc='upper right', fontsize=16)
    save(fig, path)

def fig_rectifier(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    t = X(0, 3 / 60, 1200); vin = 17 * np.sin(2 * np.pi * 60 * t)
    a1.plot(t * 1000, vin, color=C['gray'], lw=1.5, label='input (12 V rms)'); a1.plot(t * 1000, np.abs(vin) - 1.4, color=C['blue'], label='full-wave rectified')
    a1.legend(loc='lower right', fontsize=15); a1.set_ylabel('V')
    vc = np.zeros_like(t); vc[0] = 0; RC = 0.1 * 0.001 * 1000
    for k in range(1, len(t)):
        r = abs(vin[k]) - 1.4; vc[k] = max(r, vc[k - 1] * np.exp(-(t[k] - t[k - 1]) / 0.1))
    a2.plot(t * 1000, np.abs(vin) - 1.4, color=C['gray'], lw=1); a2.plot(t * 1000, vc, color=C['orange'], lw=3, label='with filter capacitor')
    a2.set_ylim(10, 17); a2.set_xlabel('time (ms)'); a2.set_ylabel('V'); a2.legend(loc='lower right', fontsize=15)
    a2.set_title('ripple ≈ V_p / (2 f R C)', fontsize=17)
    save(fig, path)

def fig_bridge(path, w, h):
    def b(d):
        d += (D1 := elm.Diode().theta(-45).label('D1'))
        d += (D2 := elm.Diode().theta(45).label('D2'))
        d += (D3 := elm.Diode().theta(135).reverse().label('D3'))
        d += (D4 := elm.Diode().theta(-135).reverse().label('D4'))
        d += elm.Line().at(D1.start).left(1.5); d += elm.SourceSin().down().label('AC in').length(d.unit * 1.4)
        d += elm.Line().tox(D2.start)
        d += elm.Line().at(D1.end).right(5).label('+ DC out', loc='right', color=C['orange'])
        d += elm.Line().at(D3.end).right(1)
    schem(path, b)

def fig_mosfet(path, w, h):
    fig, ax, H = canvas(w, h, need=58, exact=True)
    ax.add_patch(Rectangle((6, 4), 88, 26, fc=C['lred'], ec=C['red'], lw=2)); txt(ax, 50, 8, 'p-type silicon body', 18, C['red'])
    ax.add_patch(Rectangle((10, 20), 18, 10, fc=C['lblue'], ec=C['blue'], lw=2)); txt(ax, 19, 25, 'n+ source', 16, C['blue'], bold=True)
    ax.add_patch(Rectangle((72, 20), 18, 10, fc=C['lblue'], ec=C['blue'], lw=2)); txt(ax, 81, 25, 'n+ drain', 16, C['blue'], bold=True)
    ax.add_patch(Rectangle((28, 30), 44, 3, fc='#F7E6A0', ec=C['yellow'], lw=1.5)); txt(ax, 50, 36, 'thin oxide (insulator)', 14, C['mut'])
    ax.add_patch(Rectangle((30, 38), 40, 6, fc='#9AA4B2', ec=C['ink'], lw=2)); txt(ax, 50, 41, 'gate', 18, 'white', bold=True)
    ax.add_patch(Rectangle((28, 27), 44, 3, fc=C['blue'], alpha=0.55)); txt(ax, 50, 16, '↑ V_GS > V_t pulls electrons up → channel forms', 16, C['blue'])
    for x, lab in ((19, 'S'), (50, 'G'), (81, 'D')): line(ax, [(x, 44 if x == 50 else 30), (x, 52)], C['ink'], 2.5); txt(ax, x, 55, lab, 20, bold=True)
    save(fig, path)

def fig_mos_iv(path, w, h):
    fig, ax = plot(w, h)
    vds = X(0, 5, 300); vt = 0.7; k = 2.0
    for vgs, c in ((1.5, C['gray']), (2.0, C['green']), (2.5, C['blue']), (3.0, C['purple'])):
        vov = vgs - vt; idd = np.where(vds < vov, k * (vov * vds - vds ** 2 / 2), 0.5 * k * vov ** 2) * (1 + 0.04 * vds)
        ax.plot(vds, idd, color=c, label=f'V_GS = {vgs} V')
    vov = X(0, 2.3, 50); ax.plot(vov, 0.5 * k * vov ** 2, color=C['red'], ls='--', lw=1.8)
    ax.text(0.15, 5.6, 'triode\n(switch ON /\nresistor)', fontsize=16, color=C['red']); ax.text(2.6, 2.75, 'saturation\n(amplifier region)', fontsize=16, color=C['mut'])   # below the legend (it overlapped)
    ax.set_xlabel('V_DS (V)'); ax.set_ylabel('I_D (mA)'); ax.legend(loc='upper left', bbox_to_anchor=(0.3, 1.0), fontsize=15)
    save(fig, path)

def fig_switch(path, w, h):
    def b(d):
        d += elm.Vdd().label('+5 V')
        d += elm.Resistor().down().label('220 Ω'); d += elm.LED().down().label('LED')
        d += (Q := elm.NFet(bulk=False).anchor('drain').reverse())
        d += elm.Ground().at(Q.source)
        d += elm.Line().at(Q.gate).left(1.5); d += elm.Dot(open=True).label('MCU pin\n(3.3 V)', loc='left', color=C['blue'])
    schem(path, b)

def fig_ce(path, w, h):
    def b(d):
        d += (Q := elm.BjtNpn(circle=True).label('Q', loc='right'))
        d += elm.Resistor().up().at(Q.collector).label('R_C 4.7 kΩ', loc='bottom'); d += elm.Vdd().label('V_CC = 12 V')
        d += elm.Line().right(1.2).at(Q.collector); d += elm.Dot(open=True).label('v_out', loc='right', color=C['orange'])
        d += elm.Resistor().down().at(Q.emitter).label('R_E 1 kΩ', loc='bottom'); d += elm.Ground()
        d += elm.Line().left(2.4).at(Q.base); d += (B := elm.Dot())
        d += elm.Resistor().up().label('R1 47 kΩ'); d += elm.Vdd()
        d += elm.Resistor().down().at(B.center).label('R2 10 kΩ', loc='bottom'); d += elm.Ground()
        d += elm.Capacitor().left().at(B.center).label('C_in'); d += elm.Dot(open=True).label('v_in', loc='left', color=C['blue'])
    schem(path, b)

def fig_ce_wave(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 2, 500); ax.plot(t, 0.02 * np.sin(2 * np.pi * t), color=C['blue'], label='input: 20 mV peak')
    ax.plot(t, 0.094 * -np.sin(2 * np.pi * t), color=C['orange'], label='output: ≈ 94 mV, inverted (gain ≈ −4.7)')
    ax.legend(loc='upper right', fontsize=15); ax.set_xticks([]); ax.set_ylabel('volts (AC part)')
    ax.set_title('degenerated CE amp: gain ≈ −R_C / R_E', fontsize=19)
    save(fig, path)

def fig_smallsig(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, gridspec_kw={'width_ratios': [1.1, 1]})
    v = X(0.60, 0.72, 300); ic = 1e-14 * np.exp(v / 0.026) * 1000
    vq = 0.026 * np.log(1.4e11); iq = 1e-14 * np.exp(vq / 0.026) * 1000; gm = iq / 26
    a1.plot(v, ic, color=C['blue']); a1.plot(v, iq + gm * (v - vq) * 1000, color=C['orange'], lw=2.4)
    soliddot(a1, vq, iq, C['red']); a1.set_ylim(0, 4); a1.set_xlabel('v_BE (V)'); a1.set_ylabel('i_C (mA)')
    a1.set_title(f'tangent at Q: slope g_m = I_C/V_T\n≈ {gm*1000:.0f} mS at {iq:.1f} mA', fontsize=16)
    a2.axis('off'); a2.grid(False)
    rows = [('common emitter/source', 'high, inverting', 'main amplifier'), ('common base/gate', 'high, non-inv.', 'high frequency'), ('emitter/source follower', '≈ 1', 'buffer')]
    for i, (a, b_, c) in enumerate(rows):
        y = 0.82 - i * 0.3
        a2.text(0.0, y, a, fontsize=16, fontweight='bold', color=C['blue'], transform=a2.transAxes)
        a2.text(0.0, y - 0.1, f'gain: {b_}  ·  {c}', fontsize=15, color=C['ink'], transform=a2.transAxes)
    save(fig, path)

def fig_bode(path, w, h):
    fig, ax = plot(w, h)
    f = np.logspace(0, 7, 400); fl, fh, A = 50, 2e5, 40
    H = A - 10 * np.log10(1 + (fl / f) ** 2) - 10 * np.log10(1 + (f / fh) ** 2)
    ax.semilogx(f, H, color=C['blue']); ax.axhline(A - 3, color=C['orange'], ls='--', lw=1.8)
    ax.text(3, A - 7, '−3 dB', color=C['orange'], fontsize=17); ax.axvline(fl, color=C['gray'], ls=':'); ax.axvline(fh, color=C['gray'], ls=':')
    ax.text(fl * 1.2, 5, 'f_L: coupling\ncapacitors', fontsize=15); ax.text(fh * 1.2, 5, 'f_H: transistor\ncapacitance\n(Miller effect)', fontsize=15)
    ax.set_xlabel('frequency (Hz)'); ax.set_ylabel('gain (dB)'); ax.set_ylim(0, 46); ax.set_title('midband gain 40 dB (100×), bandwidth = f_H − f_L', fontsize=18)
    save(fig, path)

def fig_gbw(path, w, h):
    fig, ax = plot(w, h)
    f = np.logspace(0, 7, 400); gbw = 1e6
    ax.loglog(f, np.minimum(1e5, gbw / f), color=C['gray'], label='open-loop (GBW = 1 MHz)')
    for G, c in ((100, C['orange']), (10, C['blue'])):
        ax.loglog(f, G / np.sqrt(1 + (f * G / gbw) ** 2), color=c, label=f'closed-loop gain {G}: BW ≈ {gbw/G/1000:.0f} kHz')
    ax.set_xlabel('frequency (Hz)'); ax.set_ylabel('gain (V/V)'); ax.legend(loc='lower left', fontsize=15); ax.set_ylim(0.5, 2e5)
    ax.set_title('gain × bandwidth ≈ constant', fontsize=19)
    save(fig, path)

LESSON = {
 'code': 'EGEE 303', 'title': 'Electronics', 'tag': 'Year 2 · Electronics', 'folder': 'EGEE-303 Electronics',
 'slides': [
 {'t': 'title', 'h': 'Electronics', 'sub': 'Semiconductors, diodes, MOSFETs, BJTs, amplifiers and frequency response', 'img': 'a:first_transistor',
  'say': "Welcome to E G E E three oh three, electronics. That odd looking object is a replica of the first transistor, built at Bell Labs in nineteen forty seven. Transistors are now the most manufactured object in human history, with billions on a single chip. In this lecture, you'll learn where their behavior comes from, how diodes and transistors work, how to use transistors as switches and amplifiers, and what limits how fast they can go."},

 {'t': 'v', 'h': 'Semiconductors and the pn junction', 'img': 'fig:doping',
  'pts': ['Pure silicon: a poor conductor', 'Doping: add phosphorus → n-type (electrons), boron → p-type (holes)', 'Junction: carriers diffuse, leaving a depletion region', 'Built-in barrier ≈ 0.7 V in silicon'],
  'say': ["Pure silicon is a poor conductor. Its electrons are locked in bonds, and only a few break free at room temperature, thanks to the band gap you met in physics.",
          "Doping changes that. Add a tiny amount of phosphorus, which has one extra electron, and you get n type silicon with free electrons. Add boron, which is missing one, and you get p type silicon, with holes: missing electrons that move like positive charges.",
          "Put p and n regions side by side and something interesting happens. Electrons near the junction drift across and fill holes, leaving a thin region with no free carriers at all, the depletion region.",
          "The fixed charges left behind create a built in voltage barrier, about point seven volts in silicon. Every diode, transistor and solar cell is built around junctions like this."]},

 {'t': 'v', 'h': 'The diode: a one-way valve', 'img': 'fig:diode_iv',
  'pts': ['Forward bias: barrier lowered → current flows (≈ 0.7 V drop)', 'Reverse bias: barrier raised → almost no current', 'Shockley: I = I_S(e^(V/V_T) − 1), V_T ≈ 26 mV', 'Every +60 mV → 10× more current'],
  'say': ["A pn junction makes a diode, which lets current flow one way only. Apply a positive voltage to the p side, forward bias, and the barrier shrinks, so current flows.",
          "Reverse the voltage, and the barrier grows, so only a tiny leakage current flows.",
          "The Shockley equation describes it: current grows exponentially with voltage, with the thermal voltage, about twenty six millivolts at room temperature, setting the scale.",
          "Exponential is the key word. Every extra sixty millivolts or so multiplies the current by ten. That's why, in practice, we treat a conducting silicon diode as having a roughly constant point seven volt drop: the voltage barely changes while the current changes enormously."]},

 {'t': 'v', 'h': 'Solving diode circuits: the load line', 'img': 'fig:loadline',
  'pts': ['Two equations: the diode curve + the circuit (KVL)', 'Circuit: I = (5 V − V) / 1 kΩ → a straight line', 'Intersection = operating point (Q-point)', 'Quick model: assume 0.7 V → I = 4.3 mA'],
  'say': ["Since the diode is nonlinear, we can't just use Ohm's law. Take a five volt source, a one k resistor and a diode in series. Two things must both be true: the diode's own curve, and Kirchhoff's voltage law for the circuit.",
          "The circuit equation says the current equals five volts minus the diode voltage, divided by one k. That's a straight line on the same axes, called the load line.",
          "Where the two cross is the only point satisfying both: the operating point, or Q point. Here, about point six eight volts and four point three milliamps.",
          "Engineers usually skip the graph and use the constant drop model: assume point seven volts, so the current is four point three volts over one k, four point three milliamps. Same answer, in your head. Graphical load line analysis, though, is exactly how you understand transistors too."]},

 {'t': 'v', 'h': 'Power supplies: rectifiers and ripple', 'img': ['a:bridge_rect', 'fig:rectifier'],
  'pts': ['Bridge of 4 diodes: flips negative halves up', 'Filter capacitor holds the peak between pulses', 'Ripple ≈ V_p / (2 f R C) for full-wave', 'Then a regulator gives clean DC'],
  'say': ["Every device that plugs into the wall needs to turn AC into DC. The first step is a rectifier. A bridge of four diodes, like the one in this package, steers current so that both halves of the AC wave come out positive.",
          "That bumpy output isn't DC yet, so we add a big filter capacitor. It charges up to the peak, then slowly discharges into the load between peaks, leaving a small sawtooth called ripple. For a full wave rectifier, the ripple is about the peak voltage divided by two times the frequency times R times C. A bigger capacitor or a lighter load means less ripple. Finally, a voltage regulator, often built from a Zener diode or a dedicated chip, smooths out what's left. Modern phone chargers use high frequency switching converters instead, but the rectifier and filter capacitor are still right there at the input."]},

 {'t': 'v', 'h': 'The MOSFET: a voltage-controlled switch', 'img': ['fig:mosfet', 'fig:mos_iv'],
  'pts': ['Gate voltage creates a conducting channel', 'Gate draws no DC current (insulated)', 'Triode: acts like a resistor/switch ON', 'Saturation: I_D = ½ k (V_GS − V_t)² — an amplifier'],
  'say': ["The MOSFET is the transistor inside every digital chip. Here's an N channel MOSFET in cross section. Two heavily doped n regions, the source and drain, sit in p type silicon. Above the gap between them is the gate, separated by a very thin insulating oxide. Apply a positive gate voltage above the threshold, and it attracts electrons up to the surface, forming a conducting channel from source to drain. No gate voltage, no channel, no current. And because the gate is insulated, it draws essentially no DC current at all.",
          "These are its output curves. At small drain voltages, in the triode region, the channel acts like a resistor whose value is set by the gate voltage. That's the switch on state used in logic. At larger drain voltages, the current levels off, in the saturation region, at one half k times the overdrive voltage squared. There, the gate voltage controls the current almost independently of the drain voltage, like a voltage controlled current source. That's the amplifier region. Logic uses the transistor as a switch. Analog circuits use it as an amplifier."]},

 {'t': 'v', 'h': 'Driving loads from a microcontroller pin', 'img': 'fig:switch',
  'pts': ['MCU pins: a few mA, 3.3 V — too weak for motors, relays, LED strips', 'Logic-level N-MOSFET as a low-side switch', 'Pin high → transistor on → load powered', 'Add a flyback diode for motors/relays (inductive kick)'],
  'say': ["Here's the transistor circuit computer engineers build most often. A microcontroller pin can only supply a few milliamps at three point three volts. That's fine for one small L E D, but not for a motor, a relay or an L E D strip.",
          "So the pin drives the gate of an N channel MOSFET, which switches the load's ground connection. This is called a low side switch. The load has its own power supply, here five volts.",
          "When the pin goes high, the transistor turns on and the load runs. When the pin goes low, it turns off. The MOSFET's gate draws almost no current, so the microcontroller barely notices. Choose a logic level MOSFET, one that turns fully on at three point three volts.",
          "One warning for motors, solenoids and relays: they're inductors, and when you switch them off, their current can't stop instantly, so the voltage spikes. Put a diode backwards across the load, a flyback diode, to give that current a safe path, or it can destroy the transistor."]},

 {'t': 'v', 'h': 'The BJT and the common-emitter amplifier', 'img': ['a:transistors', 'fig:ce', 'fig:ce_wave'],
  'pts': ['BJT: base current controls collector current, i_C = β i_B', 'Active region: V_BE ≈ 0.7 V', 'Divider bias + emitter resistor → stable Q-point', 'Gain ≈ −R_C / R_E = −4.7'],
  'say': ["The bipolar junction transistor, or B J T, came first and is still widely used in analog circuits. Transistors come in many packages, from tiny surface mount parts to big metal cans for high power. In a B J T, a small base current controls a much larger collector current: i C equals beta times i B, where beta is typically around one hundred. In the active region, the base emitter junction is forward biased, at about point seven volts.",
          "Here's the classic common emitter amplifier. The resistor divider R one and R two sets the base voltage at about two point one volts, so the emitter sits near one point four volts, and with a one k emitter resistor that sets about one point four milliamps of collector current. This four resistor bias network is popular because the current depends on the resistors, not on beta, which varies a lot from part to part. The input capacitor blocks DC, so the signal rides on top of the bias.",
          "With the emitter resistor in place, the voltage gain is about minus R C over R E, minus four point seven here. A twenty millivolt input becomes about ninety four millivolts at the output, inverted. Notice the trade: removing R E's effect with a bypass capacitor would raise the gain a lot, but the gain would then depend on temperature and the transistor. Engineers trade gain for stability all the time."]},

 {'t': 'v', 'h': 'Small-signal analysis and amplifier types', 'img': 'fig:smallsig',
  'pts': ['Bias at a DC Q-point, then linearize around it', 'g_m = I_C / V_T: 1.4 mA → 54 mS', 'Common emitter/source: gain, inverting', 'Follower (common collector/drain): gain ≈ 1, a buffer'],
  'say': ["To analyze amplifiers, we use the linear approximation from Calculus one. Set a DC bias point, then treat the transistor's response to tiny signals as a straight line: the tangent line at the Q point.",
          "The slope is the transconductance, g m: the change in output current per change in input voltage. For a B J T, it's the collector current over the thermal voltage. At one point four milliamps, that's about fifty four milli siemens. We replace the transistor with a small signal model and use ordinary circuit analysis. Here's why that number matters. If the emitter resistor were bypassed by a capacitor, the gain would be minus g m times R C: fifty four milli siemens times four point seven k, about minus two hundred fifty. With the emitter resistor in place, it was minus four point seven. That's the gain you trade away for stability.",
          "Three basic configurations. Common emitter, or common source for a MOSFET, provides voltage gain and inverts the signal. It's the main amplifier stage.",
          "The emitter follower, or source follower, has a gain of about one, but a high input resistance and low output resistance, so it's a buffer: it can drive a heavy load without loading down the stage before it. The third type, common base, is used at high frequencies. Real amplifiers chain these stages together."]},

 {'t': 'v', 'h': 'Frequency response: amplifiers have a bandwidth', 'img': 'fig:bode',
  'pts': ['Coupling capacitors block very low frequencies', 'Internal capacitances short out high frequencies', 'Miller effect: C_μ multiplied by (1 + gain)', 'Bode plot: gain in dB vs log frequency'],
  'say': ["No amplifier works at every frequency. At low frequencies, the coupling and bypass capacitors start to block the signal, setting a lower corner frequency.",
          "At high frequencies, tiny capacitances inside the transistor itself start shorting the signal away, setting an upper corner.",
          "In a common emitter stage, one capacitance, from base to collector, is especially harmful. Because the output swings opposite to the input and much larger, that capacitance appears at the input multiplied by one plus the gain. That's the Miller effect, and it's often what limits the bandwidth.",
          "We plot this on a Bode plot: gain in decibels against frequency on a log axis. The corners are where the gain drops by three decibels, half power. Here, the midband gain is forty decibels, which is a hundred times, from fifty hertz to two hundred kilohertz. You'll use Bode plots constantly in signals and systems."]},

 {'t': 'v', 'h': 'Real op amps: gain–bandwidth and slew rate', 'img': 'fig:gbw',
  'pts': ['Gain × bandwidth ≈ constant (GBW)', '1 MHz op amp at gain 100 → only 10 kHz', 'Slew rate limits how fast the output can swing', 'Offsets, bias currents, output-swing limits'],
  'say': ["Op amps from the circuits course are built from transistors, so they inherit these limits. The most important one: the product of closed loop gain and bandwidth is roughly constant, called the gain bandwidth product.",
          "An op amp with a one megahertz gain bandwidth product, set to a gain of ten, works up to about one hundred kilohertz. Set it to a gain of one hundred, and it only works up to ten kilohertz. If you need both high gain and wide bandwidth, use two stages.",
          "There's also a slew rate: the fastest the output can change, in volts per microsecond. Ask for a big, fast swing, and the output turns into a triangle wave instead of a sine wave.",
          "And real op amps have small input offset voltages, input bias currents, and outputs that can't quite reach the supply rails, unless you choose a rail to rail part. Reading these specs on a datasheet is a core analog design skill."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Doped silicon makes **junctions**. Junctions make **diodes**; gates and junctions make **transistors** — switches for logic, amplifiers for analog.',
  'cap': 'Next: EGEE 303L, the electronics lab — measuring all of this on the bench.',
  'say': "To recap. Doping silicon makes n and p regions, and their junction creates a barrier. Diodes conduct one way with about point seven volts of drop, and power supplies use them in rectifiers. MOSFETs are voltage controlled switches and current sources, and are the building block of digital chips. B J Ts amplify with a stable bias network, and small signal models let us compute gain. And every amplifier has a limited bandwidth, set by capacitances and the gain bandwidth product. Next, we take this to the lab bench. See you there."},
 ]}

# ---------------- whiteboard worked examples (circuits drawn live) ----------------
import board as B
OF = 0.3

def draw_led(ax, n, w, h):
    def build(d, elm, v):
        d += (V := elm.SourceV().up().label('5 V', loc='top', ofst=OF).color(v(1)))
        d += elm.Resistor().right().label('R = ?', ofst=OF).color(v(1))
        d += elm.LED().down().label('LED: 2.0 V, 10 mA', loc='bottom', ofst=OF).color(v(1))
        d += elm.Line().left().to(V.start).color(v(1))
        d += elm.Label().at((1.5, 2.2)).label('3 V across R').color(v(2, 'red'))
        d += elm.Label().at((1.5, 0.6)).label('I = 10 mA').color(v(2, 'blue'))
    B.circuit(ax, n, build, fs=28, lw=3)

def draw_ripple(ax, n, w, h):
    X0, Y0, sx, sy = 60, 120, 75, 38
    P = lambda t, vv: (X0 + t * sx, Y0 + vv * sy)
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 9 * sx, Y0 + 14 * sy, 't', 'v')
        ts = np.linspace(0, 8.4, 400); B.ln(ax, *zip(*[P(t, 12 * abs(np.sin(np.pi * t / 2))) for t in ts]), c='gray', lw=2, ls='--')
        B.lab(ax, *P(1.0, 13.6), 'rectified', 24, 'gray', ha='left')
    if n >= 2:
        pts = []
        for k in range(4):
            t0 = 1 + 2 * k; pts += [P(t0, 12), P(t0 + 1.85, 10.2)]
        pts.append(P(8.85, 12)); B.ln(ax, [p[0] for p in pts], [p[1] for p in pts], c='blue', lw=3.5)
        B.lab(ax, *P(4.0, 13.6), 'with capacitor', 26, 'blue', ha='left')
    if n >= 3:
        B.arr(ax, *P(8.6, 12.2), *P(8.6, 10.0), 'red', 2, 16, '<|-|>'); B.lab(ax, *P(8.75, 11.1), 'Vr', 28, 'red', ha='left')

def draw_mosfet(ax, n, w, h):
    def build(d, elm, v):
        d += (vcc := elm.Vdd().label('+12 V').color(v(1)))
        d += elm.Line().down(0.6).color(v(1)); d += (top := elm.Dot().color(v(1)))
        d += (m := elm.Motor().down().label('motor\n1 A', loc='top', ofst=OF).color(v(1)))
        d += (dr := elm.Dot().color(v(1)))
        d += (q := elm.NFet().right().reverse().anchor('drain').at(dr.center).color(v(1)))
        d += elm.Ground().at(q.source).color(v(1))
        d += elm.Line().at(q.gate).left(0.8).color(v(2)); d += elm.Dot().color(v(2)); d.push()
        d += elm.Resistor().left().label('100 Ω', ofst=OF).color(v(2)); d += elm.Dot(open=True).label('MCU pin', loc='left').color(v(2)); d.pop()
        d += elm.Resistor().down().label('100 kΩ', loc='top', ofst=OF).color(v(2)); d += elm.Ground().color(v(2))
        d += elm.Line().at(top.center).right(1.8).color(v(3, 'red'))
        d += elm.Diode().down().reverse().toy(dr.center).label('flyback', loc='bottom', ofst=OF).color(v(3, 'red'))
        d += elm.Line().left().to(dr.center).color(v(3, 'red'))
    B.circuit(ax, n, build, fs=26, lw=3)

def draw_ce(ax, n, w, h):
    def build(d, elm, v):
        d += (q := elm.BjtNpn(circle=True).theta(0).color(v(1)))
        d += elm.Resistor().up().at(q.collector).label('RC 4.7 kΩ', loc='bottom', ofst=OF).color(v(1)); d += elm.Vdd().label('12 V').color(v(1))
        d += elm.Resistor().down().at(q.emitter).label('RE 1 kΩ', loc='bottom', ofst=OF).color(v(1)); d += elm.Ground().color(v(1))
        d += elm.Line().left(1.5).at(q.base).color(v(1)); d += (b := elm.Dot().color(v(1)))
        d += elm.Resistor().up().label('R1 47 kΩ', loc='top', ofst=OF).color(v(1)); d += elm.Vdd().label('12 V').color(v(1))
        d += elm.Resistor().down().at(b.center).label('R2 10 kΩ', loc='top', ofst=OF).color(v(1)); d += elm.Ground().color(v(1))
        d += elm.Label().at((b.center[0] - 1.9, b.center[1])).label('VB = 2.1 V').color(v(2, 'red'))
        d += elm.Label().at((q.emitter[0] + 1.6, q.emitter[1] - 0.4)).label('VE = 1.4 V').color(v(3, 'red'))
        d += elm.Label().at((q.collector[0] + 1.6, q.collector[1] + 0.5)).label('VC = 5.4 V').color(v(4, 'red'))
    B.circuit(ax, n, build, fs=24, lw=3)

B.insert(LESSON, 'Solving diode circuits', {'t': 'wb', 'h': 'Worked example: sizing an LED resistor', 'draw': 'led', 'split': 0.45, 'steps': [
    {'say': "The most common diode calculation of all: an LED needs a series resistor, or it draws too much current and burns out. Our supply is five volts. The LED drops about two volts when lit, and we want ten milliamps.",
     'w': [{'d': 1, 'at': 1}, {'m': r'$V_s = 5\ \mathrm{V}$,  $V_F = 2.0\ \mathrm{V}$,  $I = 10\ \mathrm{mA}$', 'at': 2}]},
    {'say': "Kirchhoff's voltage law: whatever the LED doesn't drop, the resistor must. Five minus two is three volts across the resistor. Ohm's law: three volts over ten milliamps is three hundred ohms.",
     'w': [{'m': r'$V_R = 5 - 2 = 3\ \mathrm{V}$', 'at': 1}, {'d': 2, 'at': 1}, {'m': r'$R = \frac{3\ \mathrm{V}}{10\ \mathrm{mA}} = 300\ \Omega$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "Three hundred ohms isn't a standard value, so round up to the next one, three thirty. That gives three over three thirty, about nine point one milliamps. Slightly dimmer, slightly safer. The resistor dissipates three volts times nine point one milliamps, about twenty seven milliwatts, so a common quarter watt resistor is plenty.",
     'w': [{'m': r'standard: $330\ \Omega \Rightarrow I = 3/330 \approx 9.1\ \mathrm{mA}$', 'at': 1}, {'m': r'$P_R = 3 \times 0.0091 \approx 27\ \mathrm{mW}$  (1/4 W is fine)', 'at': 3}]},
]})

B.insert(LESSON, 'Power supplies: rectifiers and ripple', {'t': 'wb', 'h': 'Worked example: how big is the ripple?', 'draw': 'ripple', 'split': 0.48, 'steps': [
    {'say': "A full wave rectifier turns sixty hertz AC into bumps at twelve volts peak, a hundred twenty times a second. Alone, that's useless for electronics.",
     'w': [{'m': r'full-wave: peaks 12 V, $f_{ripple} = 2 \times 60 = 120\ \mathrm{Hz}$', 'at': 0}, {'d': 1, 'at': 0}]},
    {'say': "A filter capacitor charges to the peak, then holds the voltage up while the load slowly drains it, until the next bump recharges it. The voltage now sags only a little between peaks. That sag is the ripple.",
     'w': [{'d': 2, 'at': 0}]},
    {'say': "Estimate it: ripple is about the peak voltage over two f R C, using the line frequency f. With a one kilohm load and a thousand microfarad capacitor: twelve over two times sixty times one thousand times point zero zero one, which is a tenth of a volt.",
     'w': [{'d': 3, 'at': 0}, {'m': r'$V_r \approx \frac{V_p}{2fRC} = \frac{12}{2(60)(1000)(0.001)} = 0.1\ \mathrm{V}$', 'c': 'red', 'box': True, 'at': 1, 'fs': 36}]},
    {'say': "Now draw ten times more current, with a hundred ohm load. The ripple grows ten times, to a full volt. Heavier loads need bigger capacitors, and a voltage regulator after the capacitor cleans up whatever ripple is left.",
     'w': [{'m': r'$R = 100\ \Omega$:  $V_r \approx 1\ \mathrm{V}$  (10× worse)', 'at': 0}, {'m': 'then a regulator cleans it up', 'c': 'green', 'at': 2}]},
]})

B.insert(LESSON, 'Driving loads from a microcontroller pin', {'t': 'wb', 'h': 'Worked example: a MOSFET motor driver', 'draw': 'mosfet', 'split': 0.42, 'steps': [
    {'say': "A microcontroller pin can supply a few milliamps at three point three volts. A twelve volt motor needs an amp. The fix is a logic level N channel MOSFET as a low side switch: the motor sits between twelve volts and the drain, and the source goes to ground.",
     'w': [{'m': 'pin: 3.3 V, few mA.  motor: 12 V, 1 A', 'at': 1}, {'d': 1, 'at': 3}]},
    {'say': "The gate connects to the pin through a small resistor, which limits the current spike when the gate capacitance charges. A hundred kilohm pull down resistor keeps the motor off while the microcontroller is booting and the pin is floating.",
     'w': [{'d': 2, 'at': 0}, {'m': '100 Ω: tames the gate charging spike', 'at': 0}, {'m': '100 kΩ: OFF while the MCU boots', 'at': 1}]},
    {'say': "Pin high: the MOSFET turns on, with an on resistance of about fifty milliohms. At one amp, it dissipates one squared times point zero five, just fifty milliwatts. No heatsink needed.",
     'w': [{'m': r'ON: $P = I^2 R_{DS(on)} = 1^2 \times 0.05 = 50\ \mathrm{mW}$', 'c': 'blue', 'at': 1}]},
    {'say': "And never forget the flyback diode. A motor is an inductor, and when the MOSFET switches off, the current can't stop instantly. Without a path, the voltage spikes high enough to destroy the transistor. The diode gives that current somewhere safe to circulate.",
     'w': [{'d': 3, 'at': 0}, {'m': 'flyback diode: absorbs the spike', 'c': 'red', 'box': True, 'at': 3}]},
]})

B.insert(LESSON, 'The BJT and the common-emitter amplifier', {'t': 'wb', 'h': 'Worked example: DC bias of a common-emitter amplifier', 'draw': 'ce', 'split': 0.46, 'steps': [
    {'say': "Before a transistor can amplify, we must find its DC operating point. Here's a classic divider bias circuit: R one and R two set the base voltage, R E sits under the emitter, and R C is the collector load.",
     'w': [{'m': 'step 1: DC bias first', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "The base current is tiny compared to the divider current, so treat R one and R two as a plain voltage divider: twelve times ten over fifty seven, about two point one volts at the base.",
     'w': [{'m': r'$V_B \approx 12\cdot\frac{10k}{47k + 10k} = 2.1\ \mathrm{V}$', 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "The base emitter junction drops about point seven volts, so the emitter sits at one point four volts. Across one kilohm, that's one point four milliamps, and the collector current is almost the same.",
     'w': [{'m': r'$V_E = 2.1 - 0.7 = 1.4\ \mathrm{V}$', 'at': 0}, {'m': r'$I_C \approx I_E = \frac{1.4}{1k} = 1.4\ \mathrm{mA}$', 'at': 1}, {'d': 3, 'at': 0}]},
    {'say': "The collector sits at twelve minus four point seven k times one point four milliamps, about five point four volts. That leaves four volts across the transistor, well inside the active region, with room to swing both ways. And notice: beta never appeared. That's what makes this bias stable. The voltage gain is about minus R C over R E: minus four point seven.",
     'w': [{'m': r'$V_C = 12 - (4.7k)(1.4\ \mathrm{mA}) \approx 5.4\ \mathrm{V}$', 'at': 0}, {'d': 4, 'at': 0}, {'m': r'$V_{CE} \approx 4\ \mathrm{V}$: active region', 'c': 'green', 'at': 1},
           {'m': r'gain $\approx -R_C/R_E = -4.7$', 'c': 'red', 'box': True, 'at': 4}]},
]})

B.insert(LESSON, 'Real op amps', {'t': 'wb', 'h': 'Worked example: will this op amp keep up?', 'steps': [
    {'say': "Real op amps have two speed limits. Take a common part: a gain bandwidth product of one megahertz, and a slew rate of half a volt per microsecond. First limit: bandwidth. Set the gain to one hundred, and the bandwidth is one megahertz divided by one hundred: just ten kilohertz.",
     'w': [{'m': r'GBW $= 1\ \mathrm{MHz}$,   slew rate $= 0.5\ \mathrm{V/\mu s}$', 'at': 1}, {'m': r'gain 100:  BW $= \frac{1\ \mathrm{MHz}}{100} = 10\ \mathrm{kHz}$', 'at': 4}]},
    {'say': "Second limit: the slew rate, the fastest the output can move. A sine wave of peak V p and frequency f changes fastest at its zero crossing, at a rate of two pi f V p.",
     'w': [{'m': r'max slope of $V_p\sin(2\pi ft)$ is $2\pi fV_p$', 'at': 1}]},
    {'say': "For a five volt peak output, set two pi f times five equal to half a volt per microsecond. Solve: f is about sixteen kilohertz. Above that, the sine wave turns into a triangle wave, no matter what the gain is.",
     'w': [{'m': r'$f_{max} = \frac{SR}{2\pi V_p} = \frac{0.5\times 10^6}{2\pi(5)} \approx 16\ \mathrm{kHz}$', 'c': 'red', 'box': True, 'at': 1}]},
    {'say': "So for a gain of one hundred and a five volt swing, this op amp is good to about ten kilohertz, fine for audio bass, but not for ultrasound. Always check both limits on the datasheet before choosing a part.",
     'w': [{'m': 'usable to about 10 kHz: check BOTH limits', 'c': 'green', 'gap': 12, 'at': 0}]},
]})

# ---------------- the teacher's pen (circuit marks in schematic units) ----------------
G = 'Worked example: sizing an LED resistor'
B.pen(LESSON, G, 1, {'p': [('circle', 3, 1.5, 0.62, 1.2)], 'c': 'blue', 'at': 0}, {'p': [('circle', 1.5, 3, 1.15, 0.6)], 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'standard: $330', 'at': 0}, {'p': ('check',), 'on': r'$P_R = 3', 'c': 'green', 'at': 3})
G = 'Worked example: how big is the ripple?'
B.pen(LESSON, G, 1, {'p': [('box', 60 + 75 * 0.92, 120 + 38 * 9.8, 60 + 75 * 2.95, 120 + 38 * 12.5)], 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': r'$R = 100\ \Omega$', 'at': 1})
G = 'Worked example: a MOSFET motor driver'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': '100 Ω: tames', 'c': 'blue', 'at': 0}, {'p': ('underline',), 'on': '100 kΩ: OFF', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 3, {'p': [('circle', 0, -2.1, 0.95, 1.25)], 'c': 'blue', 'at': 1}, {'p': [('circle', 1.8, -2.1, 0.6, 1.3)], 'at': 3})
G = 'Worked example: DC bias of a common-emitter amplifier'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$V_B \approx', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'$I_C \approx', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': r'$V_{CE} \approx', 'c': 'green', 'at': 1}, {'p': ('underline',), 'on': 'gain $\\approx -R_C', 'at': 4})
G = 'Worked example: will this op amp keep up?'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': '10\\ \\mathrm{kHz}$', 'at': 4})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'max slope of', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'check BOTH limits', 'at': 1})

# ---------------- the pen on ordinary slides ----------------
S = 'Semiconductors and the pn junction'
B.spen(LESSON, S, 1, {'fig': [('box', .5, .2, .96, .82)], 'c': 'blue', 'at': 1}, {'fig': [('box', .04, .2, .48, .82)], 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .48, .5, .1, .33)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': '≈ 0.7 V', 'at': 0})
S = 'The diode: a one-way valve'
B.spen(LESSON, S, 0, {'fig': [('circle', .73, .5, .06, .26)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .3, .78, .22, .05)], 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('underline', .2, .78, .07)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'box', 'on': 'Every +60 mV → 10× more current', 'at': 1})
S = 'Solving diode circuits: the load line'
B.spen(LESSON, S, 1, {'fig': [('underline', .49, .93, .17)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .23, .33, .045, .055)], 'at': 0}, {'fig': [('underline', .27, .71, .42)], 'at': 1})
B.spen(LESSON, S, 3, {'p': 'box', 'on': 'assume 0.7 V → I = 4.3 mA', 'c': 'green', 'at': 0})
S = 'Power supplies: rectifiers and ripple'
B.spen(LESSON, S, 1, {'fig': [('circle', .6, .62, .07, .07)], 'at': 1}, {'fig': [('underline', .35, .71, .47)], 'c': 'blue', 'at': 2},
       {'p': 'underline', 'on': 'Filter capacitor holds the peak', 'c': 'green', 'at': 1})
S = 'The MOSFET: a voltage-controlled switch'
B.spen(LESSON, S, 0, {'fig': [('circle', .19, .57, .1, .08)], 'c': 'blue', 'at': 2, 'dt': 0.5}, {'fig': [('circle', .81, .57, .1, .08)], 'c': 'blue', 'at': 2, 'dt': 1.5},
       {'fig': [('circle', .5, .29, .22, .08)], 'at': 3}, {'fig': [('box', .28, .43, .72, .53)], 'c': 'green', 'at': 4},
       {'fig': [('underline', .39, .61, .395)], 'at': 6})
B.spen(LESSON, S, 1, {'fig': [('circle', .17, .45, .09, .25)], 'at': 1}, {'fig': [('box', .45, .16, .97, .68)], 'c': 'blue', 'at': 3})
S = 'Driving loads from a microcontroller pin'
B.spen(LESSON, S, 0, {'fig': [('circle', .16, .72, .16, .07)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .52, .85, .12, .1)], 'at': 0}, {'fig': [('circle', .66, .05, .11, .05)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('check', .84, .66, 22)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'flyback diode', 'at': 1})
S = 'The BJT and the common-emitter amplifier'
B.spen(LESSON, S, 1, {'fig': [('circle', .4, .52, .1, .3)], 'c': 'blue', 'at': 1, 'dt': 0.5}, {'fig': [('circle', .79, .75, .14, .06)], 'c': 'blue', 'at': 1, 'dt': 5.0},
       {'fig': [('circle', .27, .48, .08, .07)], 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('underline', .4, .66, .19)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .4, .93, .255)], 'c': 'orange', 'at': 1, 'dt': 2.0},
       {'p': 'circle', 'on': '−4.7', 'at': 0})
S = 'Small-signal analysis and amplifier types'
B.spen(LESSON, S, 0, {'fig': [('circle', .32, .6, .045, .045)], 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('underline', .08, .52, .095)], 'c': 'blue', 'at': 0}, {'p': 'box', 'on': 'g_m = I_C / V_T', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .53, .21, .98, .36)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('box', .53, .63, .98, .78)], 'c': 'orange', 'at': 0})
S = 'Frequency response'
B.spen(LESSON, S, 0, {'fig': [('circle', .36, .73, .1, .07)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .83, .71, .12, .08)], 'at': 0})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'Miller effect', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('circle', .27, .28, .06, .035)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .14, .96, .075)], 'c': 'green', 'at': 2})
S = 'Real op amps: gain–bandwidth and slew rate'
B.spen(LESSON, S, 0, {'fig': [('underline', .31, .75, .09)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .68, .63, .05, .05)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .58, .5, .05, .05)], 'c': 'orange', 'at': 1},
       {'p': 'box', 'on': '1 MHz op amp at gain 100 → only 10 kHz', 'at': 1, 'dt': 1.5})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'Slew rate', 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'The MOSFET: a voltage-controlled switch', {'t': 'wb', 'h': 'Which region? The MOSFET checklist', 'steps': [
    {'say': "On every electronics exam, the first question about a MOSFET is: which region is it in? Here's the checklist, in order. First compare the gate source voltage with the threshold. If V G S is below V t, there's no channel: cutoff, and no current.",
     'w': [{'m': r'1.  $V_{GS} < V_t$  $\to$  cutoff:  $I_D = 0$', 'at': 3}]},
    {'say': "If it's above threshold, compute the overdrive, V G S minus V t. Then compare V D S with it. If V D S is smaller, the channel is fully formed along its length, and it acts like a resistor: triode. If V D S is at least the overdrive, the channel pinches off at the drain end: saturation.",
     'w': [{'m': r'2.  overdrive  $V_{ov} = V_{GS} - V_t$', 'at': 1},
           {'m': r'$V_{DS} < V_{ov}$  $\to$  triode (a resistor)', 'c': 'blue', 'at': 3},
           {'m': r'$V_{DS} \geq V_{ov}$  $\to$  saturation:  $I_D = \frac{1}{2}k\,V_{ov}^2$', 'c': 'green', 'at': 4}]},
    {'say': "Numbers. Threshold one volt, k equals two milliamps per volt squared. With V G S equals three volts, the overdrive is two volts. If V D S is five volts, that's more than two, so it's saturated, and the current is one half times two times two squared: four milliamps. Drop V D S to one volt, and it's in triode instead.",
     'w': [{'m': r'$V_t = 1$, $k = 2\ \mathrm{mA/V^2}$, $V_{GS} = 3$:  $V_{ov} = 2\ \mathrm{V}$', 'at': 0, 'gap': 14},
           {'m': r'$V_{DS} = 5 \geq 2$:  saturation,  $I_D = \frac{1}{2}(2)(2^2) = 4\ \mathrm{mA}$', 'at': 2},
           {'m': r'$V_{DS} = 1 < 2$:  triode', 'at': 3}]},
    {'say': "And beware a famous naming trap. For a MOSFET, saturation is the amplifier region, where the current saturates at a steady value. For a B J T, saturation means the opposite: the transistor is jammed fully on, like a closed switch. Same word, different meaning. Always ask which device.",
     'w': [{'m': 'MOSFET "saturation" = amplifier', 'c': 'red', 'at': 1, 'gap': 14}, {'m': 'BJT "saturation" = fully-on switch', 'c': 'red', 'at': 2}]},
]})

G = 'Which region? The MOSFET checklist'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'overdrive  $V_{ov}', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'= 4\ \mathrm{mA}$', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': 'MOSFET "saturation"', 'c': 'red', 'at': 1}, {'p': ('box',), 'on': 'BJT "saturation"', 'c': 'red', 'at': 2})
