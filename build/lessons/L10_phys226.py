import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def charge(ax, x, y, q, r=4):
    ax.add_patch(Circle((x, y), r, fc=C['red'] if q > 0 else C['blue'], ec='white', lw=2, zorder=5))
    txt(ax, x, y, '+' if q > 0 else '−', 28, 'white', bold=True, z=6)

def fig_coulomb(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    charge(ax, 22, 42, 1); charge(ax, 48, 42, 1)
    arrow(ax, (17, 42), (6, 42), color=C['ink'], lw=3.5); arrow(ax, (53, 42), (64, 42), color=C['ink'], lw=3.5); txt(ax, 35, 51, 'like charges repel', 20, bold=True)
    charge(ax, 22, 16, 1); charge(ax, 48, 16, -1)
    arrow(ax, (27, 16), (36, 16), color=C['ink'], lw=3.5); arrow(ax, (43, 16), (34, 16), color=C['ink'], lw=3.5); txt(ax, 35, 25, 'opposites attract', 20, bold=True)
    txt(ax, 84, 40, r'$F = k\,\frac{q_1 q_2}{r^2}$', 34); txt(ax, 84, 28, 'k ≈ 9 × 10⁹ N·m²/C²', 19, C['mut'])
    txt(ax, 82, 12, 'two 1 μC charges,\n1 cm apart: F = 90 N\n(≈ 9 kg weight!)', 18, C['orange'])
    save(fig, path)

def _dipole_field(Xg, Yg, charges):
    Ex = np.zeros_like(Xg); Ey = np.zeros_like(Yg); V = np.zeros_like(Xg)
    for (qx, qy, q) in charges:
        dx, dy = Xg - qx, Yg - qy; r2 = dx ** 2 + dy ** 2 + 0.01; r = np.sqrt(r2)
        Ex += q * dx / r2 ** 1.5; Ey += q * dy / r2 ** 1.5; V += q / r
    return Ex, Ey, V

def fig_field(path, w, h):
    fig, ax = plot(w, h, grid=False)
    x = X(-3, 3, 200); Xg, Yg = np.meshgrid(x, x); ch = [(-1, 0, 1), (1, 0, -1)]
    Ex, Ey, V = _dipole_field(Xg, Yg, ch)
    ax.streamplot(Xg, Yg, Ex, Ey, color=C['gray'], density=1.5, linewidth=1.3, arrowsize=1.4)
    ax.contour(Xg, Yg, V, levels=np.linspace(-3, 3, 13), colors=C['orange'], linewidths=1.2, alpha=0.7)
    for qx, qy, q in ch: ax.add_patch(Circle((qx, qy), 0.22, color=C['red'] if q > 0 else C['blue'], zorder=5))
    ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([]); ax.set_title('field lines (gray) and equipotentials (orange)', fontsize=19)
    save(fig, path)

def fig_gauss(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    cx, cy = 34, 30
    ax.add_patch(Circle((cx, cy), 20, fc=C['lblue'], ec=C['blue'], lw=3, ls='--', alpha=0.5)); charge(ax, cx, cy, 1, 3.5)
    for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        arrow(ax, (cx + 5 * np.cos(a), cy + 5 * np.sin(a)), (cx + 27 * np.cos(a), cy + 27 * np.sin(a)), color=C['red'], lw=2, ms=14)
    txt(ax, 80, 46, r'$\oint \vec E \cdot d\vec A = \frac{Q_{enc}}{\varepsilon_0}$', 30)
    txt(ax, 80, 30, 'total field poking out of\nANY closed surface depends\nonly on the charge inside', 19, C['ink'])
    txt(ax, 80, 12, 'inside a metal box: E = 0\n(why a car protects you\nfrom lightning)', 18, C['orange'])
    save(fig, path)

def fig_capacitor(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    ax.add_patch(Rectangle((14, 8), 3, 40, fc=C['red'])); ax.add_patch(Rectangle((47, 8), 3, 40, fc=C['blue']))
    for y in np.linspace(11, 45, 7):
        txt(ax, 19.5, y, '+', 20, C['red'], bold=True); txt(ax, 44.5, y, '−', 20, C['blue'], bold=True)
        arrow(ax, (22, y), (42, y), color=C['gray'], lw=2, ms=14)
    txt(ax, 32, 52, 'uniform field E', 19, C['mut']); line(ax, [(17, 4), (47, 4)], C['ink'], 1.5); txt(ax, 32, 1.5, 'gap d', 17)
    txt(ax, 78, 44, r'$C = \frac{\varepsilon_0 A}{d}$', 32); txt(ax, 78, 32, r'$U = \frac{1}{2} C V^2$', 28)
    txt(ax, 78, 16, '1 cm² plates, 1 μm gap:\nC ≈ 0.9 nF', 19, C['orange'])
    save(fig, path)

def fig_current(path, w, h):
    fig, ax, H = canvas(w, h, need=44, exact=True)
    ax.add_patch(FancyBboxPatch((6, 14), 70, 14, boxstyle='round,pad=0,rounding_size=7', fc='#E9C29B', ec=C['orange'], lw=2.5))
    rng = np.random.default_rng(1)
    for i in range(26):
        x, y = 10 + rng.random() * 62, 17 + rng.random() * 8; dot(ax, x, y, 0.8, C['blue'])
        arrow(ax, (x, y), (x + rng.uniform(-3, 3), y + rng.uniform(-2, 2)), color=C['gray'], lw=1, ms=8)
    arrow(ax, (30, 33), (12, 33), color=C['blue'], lw=3, text='electron drift ≈ 0.07 mm/s', fs=16)
    txt(ax, 88, 30, r'$R = \rho \frac{L}{A}$', 30); txt(ax, 88, 16, '1 m of 1 mm²\ncopper ≈ 0.017 Ω', 17, C['mut'])
    txt(ax, 42, 6, 'but the signal (the field) travels at a large fraction of light speed', 17, C['orange'])
    save(fig, path)

def fig_lorentz(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    for x in range(8, 64, 8):
        for y in range(6, 54, 8): ax.add_patch(Circle((x, y), 0.6, color=C['purple'])); ax.add_patch(Circle((x, y), 1.4, fc='none', ec=C['purple'], lw=1))
    txt(ax, 36, 58, 'B out of the page (⊙)', 18, C['purple'])
    ax.add_patch(Circle((36, 30), 16, fc='none', ec=C['orange'], lw=3.5, ls='-'))
    pt = (36 + 16, 30); charge(ax, pt[0], pt[1], 1, 2.6)
    arrow(ax, pt, (pt[0], pt[1] + 11), color=C['green'], lw=3.5); txt(ax, pt[0] + 2, pt[1] + 9, 'v', 22, C['green'], bold=True, ha='left')
    arrow(ax, pt, (pt[0] - 10, pt[1]), color=C['red'], lw=3.5); txt(ax, pt[0] - 8, pt[1] - 4, 'F', 22, C['red'], bold=True)
    txt(ax, 84, 44, r'$\vec F = q\,\vec v \times \vec B$', 30); txt(ax, 84, 30, 'always sideways →\ncircles, no speed change', 18)
    txt(ax, 84, 14, r'$r = \frac{mv}{qB}$', 28)
    save(fig, path)

def fig_bwire(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    cx, cy = 30, 28
    for r in (6, 12, 18, 24): ax.add_patch(Arc((cx, cy), 2 * r, 2 * r * 0.45, theta1=0, theta2=360, color=C['blue'], lw=2))
    ax.add_patch(Rectangle((cx - 1.2, 2), 2.4, 52, fc=C['orange'], zorder=5)); arrow(ax, (cx + 4, 40), (cx + 4, 52), color=C['orange'], lw=3); txt(ax, cx + 6, 48, 'I', 24, C['orange'], ha='left', bold=True)
    arrow(ax, (cx + 11.6, cy - 2.6), (cx + 6, cy - 5.3), color=C['blue'], lw=2.5, ms=16)
    txt(ax, 78, 44, r'$B = \frac{\mu_0 I}{2\pi r}$', 32); txt(ax, 78, 30, '10 A, 1 cm away:\nB = 0.2 mT\n(≈ 4× Earth’s field)', 18)
    txt(ax, 78, 10, 'right-hand rule: thumb = I,\nfingers curl with B', 17, C['mut'])
    save(fig, path)

def fig_faraday(path, w, h):
    fig, ax, H = canvas(w, h, need=59, exact=True)
    for i in range(7): ax.add_patch(matplotlib.patches.Ellipse((50 + i * 4, 28), 5, 22, fc='none', ec=C['orange'], lw=2.5))
    box(ax, 12, 23, 22, 10, 'N        S', fc=C['lred'], ec=C['red'], fs=22, bold=True)
    arrow(ax, (36, 28), (46, 28), color=C['ink'], lw=3.5, text='push magnet in', fs=17)
    line(ax, [(50, 17), (50, 6), (90, 6), (90, 17)], C['ink'], 2.5); box(ax, 64, 2, 12, 8, 'bulb', fc=C['lyellow'], ec=C['yellow'], fs=16)
    txt(ax, 50, 52, r'emf $= -\frac{d\Phi_B}{dt}$   (changing flux → voltage)', 24)
    txt(ax, 50, 44, 'Lenz: the induced current opposes the change', 18, C['red'])
    save(fig, path)

def fig_xfmr(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    ax.add_patch(Rectangle((30, 8), 40, 40, fc='#D5DAE3', ec=C['gray'], lw=2)); ax.add_patch(Rectangle((38, 16), 24, 24, fc='white', ec=C['gray'], lw=2))
    for i in range(8): ax.add_patch(matplotlib.patches.Ellipse((34, 14 + i * 4), 10, 3, fc='none', ec=C['orange'], lw=2.5))
    for i in range(3): ax.add_patch(matplotlib.patches.Ellipse((66, 22 + i * 5), 10, 3.5, fc='none', ec=C['blue'], lw=2.5))
    txt(ax, 16, 28, 'primary\nN₁ turns\n7200 V', 19, C['orange'], bold=True); txt(ax, 86, 28, 'secondary\nN₂ turns\n240 V', 19, C['blue'], bold=True)
    txt(ax, 50, 53, r'$\frac{V_2}{V_1} = \frac{N_2}{N_1}$   →   30 : 1', 26)
    txt(ax, 50, 3, 'works only with AC: the flux must keep changing', 17, C['mut'])
    save(fig, path)

def fig_spectrum(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    bands = [('radio', '1 m – km', 'AM/FM, TV', '#8E9CB8'), ('microwave', '1 mm – 1 m', 'Wi-Fi, 5G, radar', '#7A8FC7'), ('infrared', '700 nm – 1 mm', 'remotes, heat', '#C0504D'),
             ('visible', '400 – 700 nm', 'eyes, cameras', None), ('ultraviolet', '10 – 400 nm', 'sunburn, chip lithography', '#8064A2'), ('X-ray / γ', '< 10 nm', 'medical imaging', '#4B3A6B')]
    x = 2
    for nm, lam, use, col in bands:
        wdt = 16
        if col is None:
            for k, c in enumerate(['#8B00FF', '#0000FF', '#00A0FF', '#00C000', '#FFE000', '#FF8000', '#FF0000']):
                ax.add_patch(Rectangle((x + k * wdt / 7, 18), wdt / 7, 10, fc=c, ec='none'))
        else: ax.add_patch(Rectangle((x, 18), wdt, 10, fc=col, ec='white', lw=2))
        txt(ax, x + wdt / 2, 23, nm, 15, 'white', bold=True); txt(ax, x + wdt / 2, 13, lam, 14, C['ink']); txt(ax, x + wdt / 2, 6, use.replace(', ', ',\n'), 13, C['mut'])
        x += wdt
    txt(ax, 50, 35, 'all the same thing: electromagnetic waves at c = 1/√(μ₀ε₀) ≈ 3×10⁸ m/s', 18, bold=True)
    save(fig, path)

LESSON = {
 'code': 'PHYS 226', 'title': 'Electricity & Magnetism', 'tag': 'Year 2 · Foundations', 'folder': 'PHYS-226 Electricity & Magnetism',
 'slides': [
 {'t': 'title', 'h': 'Electricity & Magnetism', 'sub': 'Charges, fields, circuits, magnetism, induction — and light itself', 'img': 'a:lightning',
  'say': "Welcome to Physics two twenty six, electricity and magnetism. For a computer engineer, this is the physics of everything. Every bit in your processor is a tiny packet of charge, every wire carries current, every motor and speaker runs on magnetic forces, and every wireless signal is an electromagnetic wave. Circuits class gives you rules. This class explains where those rules come from."},

 {'t': 'v', 'h': 'Electric charge and Coulomb’s law', 'img': 'fig:coulomb',
  'pts': ['Two kinds of charge: + and −', 'Like repel, opposites attract', 'F = k q₁q₂ / r² — inverse square, like gravity', 'But ~10⁴² times stronger than gravity between electrons'],
  'say': ["Matter is made of positive protons and negative electrons. Charge comes in exactly those two flavors.",
          "Like charges repel, and opposite charges attract.",
          "Coulomb's law gives the force: k times q one times q two, over r squared, with k about nine billion. Double the distance and the force drops to a quarter.",
          "This force is enormous compared to gravity. Between two electrons, the electric force is about ten to the forty two times stronger than their gravitational pull. Even two tiny one microcoulomb charges, a centimeter apart, push on each other with ninety newtons, the weight of nine kilograms. The only reason we don't feel these forces every day is that ordinary matter is almost perfectly neutral."]},

 {'t': 'v', 'h': 'Electric fields and potential', 'img': 'fig:field',
  'pts': ['Field E = force per unit charge, at every point', 'Field lines leave + and end on −', 'Potential V = energy per unit charge (volts)', 'E points “downhill” in V and crosses equipotentials at 90°'],
  'say': ["Instead of computing forces between every pair of charges, we describe the electric field: the force a tiny positive test charge would feel at each point, per coulomb. It's a vector field, like the ones from Calculus three.",
          "Field lines start on positive charges and end on negative ones. Here, the gray lines show the field of a positive and negative pair, called a dipole.",
          "The electric potential, measured in volts, is the potential energy per unit charge. A volt is a joule per coulomb. The orange curves connect points at equal potential.",
          "The field points downhill in potential, from high voltage to low, and always crosses equipotentials at right angles, exactly like the gradient and contour lines from Calculus three. In fact, E is minus the gradient of V. That's the physics behind every voltage in a circuit."]},

 {'t': 'v', 'h': 'Gauss’s law', 'img': 'fig:gauss',
  'pts': ['Flux of E through a closed surface = Q_inside / ε₀', 'Use symmetry to make hard problems easy', 'Inside a conductor in equilibrium: E = 0', 'Excess charge sits on the outer surface'],
  'say': ["Gauss's law says the total electric flux out of any closed surface equals the charge enclosed, divided by epsilon naught. It's the divergence theorem from Calculus three applied to the electric field.",
          "When there's symmetry, it turns a hard integral into one line. For example, it shows that a uniformly charged sphere looks exactly like a point charge from outside.",
          "It also proves that inside a conductor in equilibrium, the field is zero. Any field would push the free electrons around until they cancel it.",
          "So excess charge sits on the outer surface. That's why a car, a metal box, is a relatively safe place in a lightning storm, and why sensitive electronics are wrapped in metal shields called Faraday cages."]},

 {'t': 'v', 'h': 'Capacitors: storing charge and energy', 'img': 'fig:capacitor',
  'pts': ['C = Q / V', 'Parallel plates: C = ε₀A/d (bigger, closer → more C)', 'Energy U = ½CV²', 'Touchscreens, DRAM bits, camera flashes'],
  'say': ["A capacitor is two conductors separated by a gap. Put a voltage across it and charge piles up, plus on one side and minus on the other. Capacitance is the charge stored per volt.",
          "For parallel plates, C equals epsilon naught times the area over the gap. Bigger plates or a smaller gap store more charge. One square centimeter plates a micrometer apart give about point nine nanofarads. Filling the gap with an insulating material multiplies it by the dielectric constant.",
          "The energy stored is one half C V squared, the same triangle we integrated in calculus two.",
          "Capacitors are everywhere in computer engineering. Every bit in a computer's D RAM memory is a tiny capacitor that's either charged or not. Your phone's touchscreen senses your finger because your finger changes the capacitance of a grid of electrodes. And every chip has capacitors next to it to smooth out its power supply."]},

 {'t': 'v', 'h': 'Current and resistance', 'img': 'fig:current',
  'pts': ['Current I = dq/dt (amperes = coulombs/second)', 'R = ρL/A — longer, thinner wires resist more', 'Electrons drift slowly; the field moves fast', 'Power P = I²R = V²/R → heat'],
  'say': ["Current is the rate at which charge flows: one ampere is one coulomb per second.",
          "A wire's resistance depends on its material, its length and its cross section: R equals rho L over A. A meter of copper wire one square millimeter thick has only about point zero one seven ohms. On a chip, wires are thousands of times thinner, so their resistance matters a lot, as you'll see in advanced electronics.",
          "Here's a surprise. In a wire carrying one amp, the electrons themselves drift at only about seven hundredths of a millimeter per second, slower than a snail. But when you flip a switch, the light comes on instantly, because the electric field that pushes all the electrons travels down the wire at a large fraction of the speed of light.",
          "And resistance turns electrical energy into heat: power equals I squared R. That's how toasters work, and also why processors need fans."]},

 {'t': 'v', 'h': 'Magnetic force: why motors spin', 'img': ['fig:lorentz', 'a:motor_cutaway'],
  'pts': ['F = q v × B: always perpendicular to motion', 'Charges circle in a uniform field', 'Force on a wire: F = I L × B', 'Current loop in a field feels a torque → motor'],
  'say': ["Magnetic fields push on moving charges with the force q v cross B. Because it's a cross product, the push is always sideways, perpendicular to the velocity. So a magnetic field can bend a charge's path into a circle, but never speed it up or slow it down. The radius is m v over q B. That's how particle accelerators steer beams, and how old tube televisions aimed their electron beam. For the direction, point your right hand's fingers along v, curl them toward B, and your thumb gives the force on a positive charge. For an electron, which is negative, flip it: the force points the opposite way. Forgetting that flip is the classic mistake.",
          "A current carrying wire is just many moving charges, so it feels a force too: I L cross B. Put a loop of wire in a magnetic field, and the forces on opposite sides push in opposite directions, creating a torque. Switch the current direction at the right moments, and the loop keeps spinning. That's an electric motor, like this cutaway industrial motor. Your hard drive, cooling fans, drones and electric cars all depend on this one equation."]},

 {'t': 'v', 'h': 'Currents create magnetic fields', 'img': ['fig:bwire', 'a:mri'],
  'pts': ['Long straight wire: B = μ₀I / (2πr)', 'Field circles the wire (right-hand rule)', 'Coil (solenoid): B = μ₀nI — an electromagnet', 'MRI magnets: 1.5–3 T (≈ 50,000× Earth’s field)'],
  'say': ["The connection runs both ways: currents create magnetic fields. Around a long straight wire, the field forms circles, with strength mu naught I over two pi r. Ten amps, one centimeter away, gives about point two millitesla, a few times stronger than Earth's magnetic field. Point your right thumb along the current, and your fingers curl in the direction of the field.",
          "Wind the wire into a coil, a solenoid, and the fields add up inside to make a strong, uniform field: an electromagnet. Relays, speakers, and the read and write heads of hard drives use this. And an MRI scanner uses a superconducting coil to create a field of one and a half to three tesla, tens of thousands of times stronger than Earth's."]},

 {'t': 'v', 'h': 'Induction: changing fields make voltage', 'img': ['fig:faraday', 'a:qi_charger'],
  'pts': ['Faraday: emf = −dΦ/dt', 'Lenz: induced current opposes the change', 'Generators, wireless chargers, induction cooktops', 'Inductors: v = L di/dt (current can’t jump)'],
  'say': ["In eighteen thirty one, Michael Faraday discovered that a changing magnetic field creates a voltage. Push a magnet into a coil, and a current flows. Hold it still, and the current stops. The induced voltage equals minus the rate of change of magnetic flux through the coil. And Lenz's law explains the minus sign: the induced current always flows so as to oppose the change. Push the magnet in, and the coil pushes back. That's energy conservation in action. Almost all the electricity on the grid comes from generators that spin coils past magnets.",
          "Wireless phone chargers use induction directly. A coil in the pad carries alternating current, creating a changing field, which induces a current in a coil inside the phone. No wires touching. Inductors, the circuit component, are coils that resist changes in current, with voltage L d i d t. That's why inductor current can't jump instantly, a rule you'll use in circuits."]},

 {'t': 'v', 'h': 'Transformers: how the power grid works', 'img': ['fig:xfmr', 'a:pole_xfmr'],
  'pts': ['Two coils sharing an iron core', 'V₂/V₁ = N₂/N₁', 'Step up for transmission (less current → less I²R loss)', 'Step down near homes: e.g. 7200 V → 240 V'],
  'say': ["A transformer is two coils wound on a shared iron core. Alternating current in the first coil creates a changing magnetic flux in the core, which induces a voltage in the second coil. The voltage ratio equals the turns ratio. With thirty times fewer turns on the secondary, seven thousand two hundred volts becomes two hundred forty.",
          "Why bother? Power lost in a long transmission line is I squared R. For the same power, raising the voltage by a factor of ten cuts the current by ten, and the losses by a hundred. So power plants step voltage up to hundreds of thousands of volts for long distance transmission, and transformers like this one on a utility pole step it back down near your home. This is also why the grid uses AC: transformers only work when the flux keeps changing."]},

 {'t': 'v', 'h': 'Maxwell’s equations and electromagnetic waves', 'img': 'fig:spectrum', 'split': 0.33, 'fs': 36,
  'pts': ['Gauss (E) · Gauss (B) · Faraday · Ampère–Maxwell', 'A changing E makes B, a changing B makes E', 'Self-sustaining wave at c = 1/√(μ₀ε₀) ≈ 3×10⁸ m/s', 'Radio, Wi-Fi, light, X-rays: same physics'],
  'say': ["In the eighteen sixties, James Clerk Maxwell collected everything into four equations: Gauss's law for electric fields, Gauss's law for magnetism, which says there are no magnetic monopoles, Faraday's law, and Ampère's law, to which Maxwell added one crucial term.",
          "That term says a changing electric field creates a magnetic field, just as a changing magnetic field creates an electric field.",
          "Put those together and you get a wave: a changing E makes B, which makes E, and so on, sustaining itself through empty space. Maxwell calculated its speed from two lab constants, one over the square root of mu naught epsilon naught, and got three hundred million meters per second, the measured speed of light. Light is an electromagnetic wave.",
          "And so is everything on this chart. Radio and TV, the microwaves your Wi Fi uses at two point four gigahertz with a wavelength of about twelve centimeters, infrared, visible light, ultraviolet, and X rays. Every wireless technology you'll ever design is an application of these four equations."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Charges make **E fields**, currents make **B fields**, changing fields make each other — and that makes **light, motors, transformers and radio**.',
  'cap': 'Next: PHYS 227 — waves, optics and modern physics (the quantum ideas behind semiconductors).',
  'say': "To recap. Charges exert forces through electric fields, and voltage is energy per charge. Gauss's law relates fields to charge. Capacitors store charge and energy, and resistance turns current into heat. Moving charges feel magnetic forces, which drive motors, and currents create magnetic fields. Changing magnetic flux induces voltage, which gives us generators, transformers and wireless charging. And Maxwell's equations unite it all and predict electromagnetic waves. Circuits are the low frequency, simplified version of all this. Next up, waves, optics and modern physics. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B

def draw_dipole(ax, n, w, h):
    y = h * 0.5; x1, x2 = 90, w - 90; xm = (x1 + x2) / 2
    if n >= 1:
        B.dot(ax, x1, y, c='red', s=40); B.lab(ax, x1, y, '+', 40, 'white'); B.lab(ax, x1, y - 60, '+2 nC', 30, 'red')
        B.dot(ax, x2, y, c='blue', s=40); B.lab(ax, x2, y, '−', 40, 'white'); B.lab(ax, x2, y - 60, '−2 nC', 30, 'blue')
        B.arr(ax, x1, y - 110, x2, y - 110, 'gray', 2, 18, '<|-|>'); B.lab(ax, xm, y - 140, '0.6 m', 30, 'gray')
        B.dot(ax, xm, y, s=12); B.lab(ax, xm, y + 40, 'P', 32)
    if n >= 2:
        B.arr(ax, xm, y + 90, xm + 140, y + 90, 'red', 4); B.lab(ax, xm + 70, y + 125, 'E₁ (pushed away from +)', 24, 'red')
    if n >= 3:
        B.arr(ax, xm, y + 180, xm + 140, y + 180, 'blue', 4); B.lab(ax, xm + 70, y + 215, 'E₂ (pulled toward −)', 24, 'blue')
    if n >= 4:
        B.arr(ax, xm, y - 200, xm + 280, y - 200, 'green', 5); B.lab(ax, xm + 140, y - 240, 'E = E₁ + E₂ ≈ 400 N/C', 28, 'green')

def draw_plates(ax, n, w, h):
    x1, x2, y0, y1 = w * 0.3, w * 0.62, h * 0.18, h * 0.82
    if n >= 1:
        B.rect(ax, x1 - 22, y0, 22, y1 - y0, fc='#f6d6c4', c='red'); B.rect(ax, x2, y0, 22, y1 - y0, fc='#dfe8f7', c='blue')
        B.lab(ax, x1 - 60, y1 + 30, '10 cm × 10 cm', 26, 'gray')
        B.arr(ax, x1, y0 - 40, x2, y0 - 40, 'ink', 2, 16, '<|-|>'); B.lab(ax, (x1 + x2) / 2, y0 - 75, 'd = 0.1 mm', 28)
    if n >= 2:
        for k in range(6):
            yy = y0 + (k + 0.5) * (y1 - y0) / 6
            B.lab(ax, x1 - 50, yy, '+', 34, 'red'); B.lab(ax, x2 + 52, yy, '−', 34, 'blue')
            B.arr(ax, x1 + 8, yy, x2 - 8, yy, 'orange', 2, 16)
        B.lab(ax, (x1 + x2) / 2, y1 + 30, 'E', 32, 'orange')

def draw_bwire(ax, n, w, h):
    cx, cy = w * 0.45, h * 0.5
    if n >= 1:
        B.dot(ax, cx, cy, c='ink', s=26); B.lab(ax, cx, cy, '•', 20, 'white'); B.lab(ax, cx, cy - 320, 'I = 10 A, out of the page', 26, 'ink')
    if n >= 2:
        t = np.linspace(0, 2 * np.pi, 120)
        for r in (110, 190, 270):
            B.ln(ax, cx + r * np.cos(t), cy + r * np.sin(t), c='blue', lw=2.5)
            B.arr(ax, cx + r, cy - 5, cx + r, cy + 15, 'blue', 2.5, 22)
        B.lab(ax, cx + 200, cy + 210, 'B circles the wire', 26, 'blue')
    if n >= 3:
        B.ln(ax, [cx, cx + 190 * np.cos(np.radians(140))], [cy, cy + 190 * np.sin(np.radians(140))], c='red', lw=2.5)
        B.lab(ax, cx - 100, cy + 45, 'r = 5 cm', 26, 'red', bbox=dict(fc='white', ec='none', pad=1))

def draw_coil(ax, n, w, h):
    cx, cy = w * 0.32, h * 0.62
    if n >= 1:
        for k in range(6):
            t = np.linspace(0, 2 * np.pi, 80); B.ln(ax, cx + 22 * k - 55 + 30 * np.cos(t), cy + 110 * np.sin(t), c='orange', lw=2.5)
        B.lab(ax, cx, cy - 150, 'N = 100 turns, A = 0.01 m²', 24, 'orange')
    if n >= 2:
        for dy in (-60, 0, 60): B.arr(ax, cx - 200, cy + dy, cx + 200, cy + dy, 'blue', 2.5, 20)
        B.lab(ax, cx + 225, cy, 'B', 32, 'blue')
    if n >= 3:
        X0, Y0 = w * 0.1, h * 0.08
        B.axes(ax, X0, Y0, X0 + 360, Y0 + 170, 't', 'B')
        B.ln(ax, [X0, X0 + 220, X0 + 330], [Y0, Y0 + 140, Y0 + 140], c='blue', lw=3)
        B.lab(ax, X0 + 220, Y0 - 25, '0.1 s', 24, 'gray'); B.lab(ax, X0 + 300, Y0 + 165, '0.5 T', 24, 'blue')

B.insert(LESSON, 'Electric fields and potential', {'t': 'wb', 'h': 'Worked example: adding electric fields', 'draw': 'dipole', 'split': 0.5, 'steps': [
    {'say': "Let's add fields from two charges, step by step. A plus two nanocoulomb charge and a minus two nanocoulomb charge sit sixty centimeters apart. What's the electric field at point P, exactly halfway between them?",
     'w': [{'d': 1, 'at': 1}, {'m': r'$q = \pm 2\ \mathrm{nC}$,   P is $r = 0.3\ \mathrm{m}$ from each', 'at': 2}]},
    {'say': "One charge at a time. The field from a point charge is k q over r squared. For the positive charge: nine times ten to the ninth, times two times ten to the minus ninth, over point three squared. That's eighteen over point zero nine, two hundred newtons per coulomb. It points away from the positive charge, so to the right.",
     'w': [r'$E = \frac{kq}{r^2}$', {'m': r'$E_1 = \frac{(9\times 10^9)(2\times 10^{-9})}{0.3^2} = \frac{18}{0.09} = 200\ \mathrm{N/C}$', 'at': 2, 'fs': 36}, {'d': 2, 'at': 4}]},
    {'say': "The negative charge has the same size and distance, so its field is also two hundred. Fields point toward negative charges, so this one points to the right as well.",
     'w': [{'m': r'$E_2 = 200\ \mathrm{N/C}$, also to the right'}, {'d': 3, 'at': 1}]},
    {'say': "Fields are vectors, so add them with direction. Both point right, so they add: four hundred newtons per coulomb, pointing from plus toward minus. If both charges had been positive, the two fields would have cancelled to zero. Direction matters.",
     'w': [{'m': r'$E = E_1 + E_2 \approx 400\ \mathrm{N/C}$  (to the right)', 'c': 'red', 'box': True, 'at': 1}, {'d': 4, 'at': 1}]},
]})

B.insert(LESSON, 'Capacitors', {'t': 'wb', 'h': 'Worked example: a parallel-plate capacitor', 'draw': 'plates', 'split': 0.55, 'steps': [
    {'say': "Let's size a real capacitor. Two square plates, ten centimeters on a side, separated by a tenth of a millimeter of air. What's the capacitance? The plate area is point one times point one, point zero one square meters.",
     'w': [{'d': 1, 'at': 1}, {'m': r'$A = (0.1)(0.1) = 0.01\ \mathrm{m^2}$,   $d = 10^{-4}\ \mathrm{m}$', 'at': 3}]},
    {'say': "Use C equals epsilon naught A over d. Epsilon naught is eight point eight five times ten to the minus twelve. Multiply by point zero one and divide by ten to the minus four: about eight point eight five times ten to the minus ten farads, or eight hundred eighty five picofarads.",
     'w': [r'$C = \frac{\varepsilon_0 A}{d}$', {'m': r'$= \frac{(8.85\times 10^{-12})(0.01)}{10^{-4}}$', 'at': 1}, {'m': r'$C \approx 885\ \mathrm{pF}$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "Connect it to five volts. The charge is C V: about four point four nanocoulombs. The stored energy is one half C V squared: about eleven nanojoules. Tiny! That's why real capacitors use thin insulating films, rolled up or stacked in layers, to get far more area in far less space.",
     'w': [{'d': 2}, {'m': r'$Q = CV = (885\ \mathrm{pF})(5\ \mathrm{V}) \approx 4.4\ \mathrm{nC}$', 'at': 1}, {'m': r'$U = \frac{1}{2}CV^2 \approx 11\ \mathrm{nJ}$', 'at': 2}]},
]})

B.insert(LESSON, 'Current and resistance', {'t': 'wb', 'h': 'Worked example: how much power does a wire waste?', 'steps': [
    {'say': "Here's a practical one. A ten meter copper wire, one millimeter in diameter, carries ten amps. What's its resistance, and how much power turns into heat? The cross section is a circle of radius half a millimeter: pi times five times ten to the minus four, squared, about seven point eight five times ten to the minus seven square meters.",
     'w': [{'m': r'copper: $\rho = 1.68\times 10^{-8}\ \Omega\,\mathrm{m}$,   $L = 10\ \mathrm{m}$,   $d = 1\ \mathrm{mm}$', 'at': 1}, {'m': r'$A = \pi r^2 = \pi(5\times 10^{-4})^2 \approx 7.85\times 10^{-7}\ \mathrm{m^2}$', 'at': 3}]},
    {'say': "Resistance is rho L over A. One point six eight times ten to the minus eight, times ten, divided by seven point eight five times ten to the minus seven. That's about point two one ohms.",
     'w': [r'$R = \frac{\rho L}{A} = \frac{(1.68\times 10^{-8})(10)}{7.85\times 10^{-7}}$', {'m': r'$R \approx 0.21\ \Omega$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "At ten amps, the voltage lost along the wire is I R, about two point one volts. The power turned into heat is I squared R: one hundred times point two one, about twenty one watts. That's why high current cables are thick, and why the power grid uses high voltage: for the same power, less current, and the loss drops with the square of the current.",
     'w': [{'m': r'$V = IR = 10(0.21) \approx 2.1\ \mathrm{V}$', 'at': 1}, {'m': r'$P = I^2R = 100(0.21) \approx 21\ \mathrm{W}$', 'c': 'red', 'box': True, 'at': 2}]},
]})

B.insert(LESSON, 'Currents create magnetic fields', {'t': 'wb', 'h': 'Worked example: why compasses fail near wires', 'draw': 'bwire', 'split': 0.55, 'steps': [
    {'say': "How strong is the magnetic field near an ordinary wire? Take a wire carrying ten amps, and a point five centimeters away. The field circles the wire, following the right hand rule.",
     'w': [{'d': 1, 'at': 1}, {'m': r'$I = 10\ \mathrm{A}$,   $r = 5\ \mathrm{cm}$', 'at': 1}, {'d': 2, 'at': 2}, {'d': 3, 'at': 2}]},
    {'say': "Use B equals mu naught I over two pi r. Mu naught is four pi times ten to the minus seven. The pi's cancel, leaving two times ten to the minus seven, times ten, over point zero five. That's four times ten to the minus five tesla, forty microtesla.",
     'w': [r'$B = \frac{\mu_0 I}{2\pi r}$', {'m': r'$= \frac{(4\pi\times 10^{-7})(10)}{2\pi (0.05)}$', 'at': 1}, {'m': r'$B = 4\times 10^{-5}\ \mathrm{T} = 40\ \mu\mathrm{T}$', 'c': 'red', 'box': True, 'at': 3}]},
    {'say': "Compare that to the Earth's magnetic field, about fifty microtesla. They're about the same size! So a compass next to a wire carrying ten amps can point the wrong way entirely. That's why electronic compasses in phones and drones are calibrated, and placed away from high current wiring.",
     'w': [{'m': r'Earth: $\approx 50\ \mu\mathrm{T}$:  same size!', 'at': 1}]},
]})

B.insert(LESSON, 'Induction', {'t': 'wb', 'h': "Worked example: Faraday's law in numbers", 'draw': 'coil', 'split': 0.52, 'steps': [
    {'say': "Let's put numbers into Faraday's law. A coil of one hundred turns, each with an area of point zero one square meters, sits in a magnetic field that ramps from zero to half a tesla in a tenth of a second. What voltage appears across the coil?",
     'w': [{'d': 1, 'at': 1}, {'d': 2, 'at': 1}, {'d': 3, 'at': 2}, {'m': r'$N = 100$,  $A = 0.01\ \mathrm{m^2}$,  $\Delta B = 0.5\ \mathrm{T}$ in $0.1\ \mathrm{s}$', 'at': 2, 'fs': 34}]},
    {'say': "The flux through one turn is B times A. It changes from zero to point five times point zero one, which is point zero zero five webers.",
     'w': [r'$\Delta\Phi = A\,\Delta B = (0.01)(0.5) = 0.005\ \mathrm{Wb}$']},
    {'say': "Faraday's law: the voltage equals the number of turns times the rate of change of flux. One hundred times point zero zero five over point one. That's five volts. Flip the field back and forth sixty times a second, and you have the principle of every generator and transformer on the power grid.",
     'w': [r'$\mathcal{E} = N\frac{\Delta\Phi}{\Delta t} = 100\cdot\frac{0.005}{0.1}$', {'m': r'$\mathcal{E} = 5\ \mathrm{V}$', 'c': 'red', 'box': True, 'at': 2}]},
]})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Electric charge'
B.spen(LESSON, S, 0, {'fig': [('circle', .22, .23, .05, .08)], 'c': 'red', 'at': 0}, {'fig': [('circle', .48, .7, .05, .08)], 'c': 'blue', 'at': 0, 'dt': 1.5})
B.spen(LESSON, S, 1, {'fig': [('underline', .22, .48, .11)], 'c': 'red', 'at': 0}, {'fig': [('underline', .23, .51, .57)], 'c': 'blue', 'at': 0, 'dt': 1.5})
B.spen(LESSON, S, 2, {'fig': [('box', .73, .15, .95, .36)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .9, .3, .03, .06)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('box', .68, .67, .97, .86)], 'c': 'orange', 'at': 2})
S = 'Electric fields and potential'
B.spen(LESSON, S, 1, {'fig': [('circle', .372, .524, .03, .045)], 'c': 'red', 'at': 0}, {'fig': [('circle', .626, .524, .03, .045)], 'c': 'blue', 'at': 0, 'dt': 1.0},
       {'fig': [('arrow', .4, .45, .6, .45)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .372, .524, .1, .15)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('arrow', .45, .7, .55, .7)], 'c': 'red', 'at': 0})
S = 'Gauss'
B.spen(LESSON, S, 0, {'fig': [('circle', .34, .48, .21, .35)], 'c': 'blue', 'at': 0}, {'fig': [('box', .66, .13, .94, .3)], 'c': 'blue', 'at': 0, 'dt': 3.0})
B.spen(LESSON, S, 1, {'fig': [('underline', .62, .98, .56)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .63, .69, .97, .86)], 'c': 'orange', 'at': 0})
S = 'Capacitors'
B.spen(LESSON, S, 0, {'fig': [('box', .13, .11, .16, .86)], 'c': 'red', 'at': 1}, {'fig': [('box', .465, .11, .495, .86)], 'c': 'blue', 'at': 1, 'dt': 0.8},
       {'fig': [('box', .69, .12, .86, .28)], 'c': 'purple', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .31, .95, .06, .045)], 'c': 'orange', 'at': 1}, {'fig': [('box', .62, .62, .94, .77)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .68, .33, .87, .48)], 'c': 'blue', 'at': 0})
S = 'Current and resistance'
B.spen(LESSON, S, 1, {'fig': [('box', .8, .18, .95, .38)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .78, .98, .71)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .07, .35, .21)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .04, .8, .88)], 'c': 'orange', 'at': 2})
S = 'Magnetic force'
B.spen(LESSON, S, 0, {'fig': [('box', .72, .17, .96, .33)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .44, .53, .04, .06)], 'c': 'red', 'at': 1},
       {'fig': [('circle', .55, .33, .03, .06)], 'c': 'green', 'at': 1, 'dt': 1.0}, {'fig': [('arrow', .52, .6, .4, .72)], 'c': 'orange', 'at': 2},
       {'fig': [('box', .77, .67, .91, .84)], 'c': 'orange', 'at': 3})
S = 'Currents create magnetic'
B.spen(LESSON, S, 0, {'fig': [('circle', .3, .5, .24, .2)], 'c': 'blue', 'at': 1}, {'fig': [('box', .69, .12, .86, .29)], 'c': 'blue', 'at': 1, 'dt': 1.5},
       {'fig': [('box', .65, .35, .93, .55)], 'c': 'orange', 'at': 2}, {'fig': [('underline', .62, .95, .89)], 'c': 'green', 'at': 3},
       {'fig': [('arrow', .34, .3, .34, .08)], 'c': 'orange', 'at': 3, 'dt': 1.0})
S = 'Induction'
B.spen(LESSON, S, 0, {'fig': [('circle', .23, .54, .13, .11)], 'c': 'red', 'at': 1}, {'fig': [('box', .63, .8, .77, .97)], 'c': 'orange', 'at': 1, 'dt': 1.5},
       {'fig': [('underline', .18, .82, .15)], 'c': 'blue', 'at': 3}, {'fig': [('underline', .21, .79, .27)], 'c': 'red', 'at': 4})
S = 'Transformers'
B.spen(LESSON, S, 0, {'fig': [('box', .28, .18, .4, .79)], 'c': 'orange', 'at': 1}, {'fig': [('box', .6, .36, .72, .64)], 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'fig': [('circle', .6, .03, .06, .05)], 'c': 'red', 'at': 2}, {'fig': [('circle', .16, .5, .08, .09)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .88, .5, .09, .09)], 'c': 'blue', 'at': 3, 'dt': 1.5})
S = 'Maxwell'
B.spen(LESSON, S, 2, {'fig': [('underline', .53, .97, .15)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 3, *[{'fig': [('box', x0, .25, x1, .97)], 'c': 'orange', 'at': 1, 'dt': t, 'solo': True} for x0, x1, t in
       ((.015, .18, 0), (.18, .34, 2.0), (.34, .5, 5.0), (.5, .66, 6.0), (.66, .82, 7.0), (.82, .985, 8.0))])

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_gsphere(ax, n, w, h):
    cx, cy, R = w * 0.5, h * 0.5, 200
    if n >= 1: B.dot(ax, cx, cy, c='red', s=16); B.lab(ax, cx - 22, cy + 30, '+Q', 30, 'red', ha='right')
    if n >= 2:
        t = np.linspace(0, 2 * np.pi, 200); B.ln(ax, cx + R * np.cos(t), cy + R * np.sin(t), c='blue', lw=3, ls='--')
        B.lab(ax, cx, cy - R - 120, 'imaginary sphere, radius r', 26, 'blue')
        B.arr(ax, cx, cy, cx + R * 0.707, cy + R * 0.707, 'gray', 2, 14); B.lab(ax, cx + R * 0.30, cy + R * 0.50, 'r', 28, 'gray')
    if n >= 3:
        for k in range(12):
            a = k * np.pi / 6; B.arr(ax, cx + R * np.cos(a), cy + R * np.sin(a), cx + (R + 75) * np.cos(a), cy + (R + 75) * np.sin(a), 'orange', 3, 18)
        B.lab(ax, cx, cy + R + 130, 'E: same size everywhere, straight out', 26, 'orange')

B.insert(LESSON, 'Electric fields and potential', {'t': 'wb', 'h': 'Force, field, energy, potential: four look-alikes', 'steps': [
    {'say': "These four quantities sound alike, and mixing them up is the most common mistake in this course. Let's put them side by side. Force, in newtons, is a vector: the push on a particular charge. Field is force per coulomb, also a vector. It describes the space itself, whether or not a charge is there.",
     'w': [{'m': r'force  $\vec F$ : newtons, VECTOR', 'at': 3}, {'m': r'field  $\vec E = \vec F/q$ : N/C, VECTOR', 'at': 4}]},
    {'say': "Potential energy, in joules, is a scalar: the energy a particular charge has at that spot. And potential, the voltage, is energy per coulomb: joules per coulomb, volts. Also a scalar. Notice the pattern: divide by the charge, and you go from a property of one charge to a property of the place.",
     'w': [{'m': r'potential energy  $U$ : joules, scalar', 'at': 0, 'gap': 14}, {'m': r'potential  $V = U/q$ : volts, scalar', 'at': 1},
           {'m': '÷ q :  one charge  →  the place itself', 'c': 'blue', 'at': 3}]},
    {'say': "Gravity has the same four. Your weight is a force. g, nine point eight newtons per kilogram, is the field. m g h is the potential energy. And g h alone is the potential. Height is to gravity what voltage is to charge.",
     'w': [{'m': 'gravity:  mg (F)   g (field)   mgh (U)   gh (potential)', 'c': 'green', 'at': 1}]},
    {'say': "And one more thing. Only differences in potential matter, just like only differences in height matter. Where you call zero volts is a choice. That's why a voltage is always measured between two points, and why every circuit needs a ground reference.",
     'w': [{'m': 'voltage = a DIFFERENCE between two points', 'c': 'red', 'box': True, 'at': 2, 'gap': 14}]},
]})

B.insert(LESSON, 'Gauss’s law', {'t': 'wb', 'h': "Worked example: Gauss's law finds a field in two lines", 'draw': 'gsphere', 'split': 0.5, 'steps': [
    {'say': "Gauss's law is a tool, so let's use it. Find the field at distance r from a point charge Q, without Coulomb's law. Step one: draw an imaginary closed surface that matches the symmetry. Here, a sphere of radius r centered on the charge.",
     'w': [{'d': 1, 'at': 1}, {'m': r'$\oint \vec E\cdot d\vec A = \frac{Q_{inside}}{\varepsilon_0}$', 'at': 2}, {'d': 2, 'at': 3}]},
    {'say': "Step two: use the symmetry. Every point on the sphere is the same distance from the charge, so the field has the same size everywhere on it, and points straight outward. So the flux integral is just E times the sphere's area, four pi r squared.",
     'w': [{'d': 3, 'at': 1}, {'m': r'$E\,(4\pi r^2) = \frac{Q}{\varepsilon_0}$', 'c': 'blue', 'at': 2}]},
    {'say': "Step three: solve for E. E equals Q over four pi epsilon naught r squared, which is exactly k Q over r squared, Coulomb's law. The same three steps, with a cylinder instead of a sphere, give the field of a long charged wire, which falls off as one over r instead of one over r squared.",
     'w': [{'m': r'$E = \frac{Q}{4\pi\varepsilon_0 r^2} = \frac{kQ}{r^2}$', 'c': 'red', 'box': True, 'at': 1},
           {'m': r'line of charge:  $E = \frac{\lambda}{2\pi\varepsilon_0 r}$', 'at': 2}]},
    {'say': "The recipe: pick a surface where the field is constant and perpendicular, pull E out of the integral, and divide by the area. If the problem has no symmetry, Gauss's law is still true, just not useful for calculation.",
     'w': [{'m': 'symmetry → constant E → pull it out', 'c': 'green', 'at': 0}]},
]})

G = 'Force, field, energy, potential: four look-alikes'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': '÷ q', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'voltage = a DIFFERENCE', 'c': 'red', 'at': 2})
G = "Worked example: Gauss's law finds a field in two lines"
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'(4\pi r^2)', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': r'= \frac{kQ}{r^2}$', 'at': 1})
