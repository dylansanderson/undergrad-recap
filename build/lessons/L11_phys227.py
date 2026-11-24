import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_shm(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    t = X(0, 4 * np.pi, 400); x = np.cos(t)
    a1.plot(t, x, color=C['blue']); a1.set_ylabel('x(t)'); a1.set_title('x(t) = A cos(ωt + φ),   ω = √(k/m)', fontsize=19)
    a2.fill_between(t, 0, 0.5 * x ** 2, color=C['lblue'], label='potential ½kx²'); a2.fill_between(t, 0.5 * x ** 2, 0.5, color=C['lorange'], label='kinetic ½mv²')
    a2.set_ylabel('energy'); a2.legend(loc='upper right', ncol=2, fontsize=15); a2.set_yticks([]); a2.set_xticks([]); a2.set_ylim(0, 0.7)
    save(fig, path)

def fig_analogy(path, w, h):
    fig, ax, H = canvas(w, h, need=44, exact=True)
    rows = [('mass m', 'inductance L'), ('spring stiffness k', '1 / capacitance C'), ('friction b', 'resistance R'), ('position x', 'charge q'),
            ('ω₀ = √(k/m)', 'ω₀ = 1/√(LC)')]
    table(ax, 8, H - 2, ['mechanical oscillator', 'RLC circuit'], rows, [42, 42], 7, 21)
    save(fig, path)

def fig_wave(path, w, h):
    fig, ax = plot(w, h, grid=False)
    x = X(0, 4, 500); ax.plot(x, np.sin(2 * np.pi * x / 1.5), color=C['blue'], lw=3.5)
    ax.annotate('', xy=(1.875, 1.25), xytext=(0.375, 1.25), arrowprops=dict(arrowstyle='<->', lw=2.5, color=C['orange'])); ax.text(1.12, 1.35, 'wavelength λ', fontsize=19, color=C['orange'], ha='center')
    ax.annotate('', xy=(0.375, 1), xytext=(0.375, 0), arrowprops=dict(arrowstyle='<->', lw=2, color=C['green'])); ax.text(0.45, 0.45, 'amplitude', fontsize=17, color=C['green'])
    ax.annotate('', xy=(3.9, -1.3), xytext=(3.1, -1.3), arrowprops=dict(arrowstyle='->', lw=3, color=C['red'])); ax.text(3.5, -1.55, 'speed v', fontsize=18, color=C['red'], ha='center')
    ax.axhline(0, color=C['gray'], lw=1); ax.set_ylim(-1.8, 1.7); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('v = f λ', fontsize=24)
    save(fig, path)

def fig_standing(path, w, h):
    fig, axs = plot(w, h, nrows=3, sharex=True, grid=False)
    x = X(0, 1, 300)
    for n, a in zip((1, 2, 3), axs):
        for ph in np.linspace(0, np.pi, 6): a.plot(x, np.sin(n * np.pi * x) * np.cos(ph), color=C['blue'], alpha=0.35, lw=1.5)
        a.plot(x, np.sin(n * np.pi * x), color=C['blue'], lw=3); a.plot(x, -np.sin(n * np.pi * x), color=C['blue'], lw=3)
        a.set_yticks([]); a.text(1.02, 0, f'n = {n}: λ = 2L/{n}, f = {n}f₁', fontsize=17, va='center')
        a.plot([0, 1], [0, 0], 'o', color=C['ink'], ms=8)
    axs[-1].set_xticks([]); fig.subplots_adjust(right=0.68)
    save(fig, path)

def fig_db(path, w, h):
    fig, ax = plot(w, h, grid=False)
    items = [('hearing threshold', 0), ('whisper', 30), ('conversation', 60), ('busy street', 80), ('rock concert', 110), ('jet engine (30 m)', 140)]
    b = ax.barh([i[0] for i in items], [i[1] for i in items], color=[C['green'], C['green'], C['blue'], C['orange'], C['red'], C['red']])
    for r, (_, v) in zip(b, items): ax.text(v + 2, r.get_y() + r.get_height() / 2, f'{v} dB', va='center', fontsize=17)
    ax.set_xlim(0, 165); ax.set_xticks([]); ax.spines['bottom'].set_visible(False)
    ax.set_title('β = 10 log₁₀(I / I₀):  every +10 dB = 10× intensity', fontsize=19)
    save(fig, path)

def fig_doppler(path, w, h):
    fig, ax = plot(w, h, grid=False); ax.set_aspect('equal')
    v = 0.5
    for k in range(7):
        t = k * 1.0; cx = -v * t; r = (6 - k) * 1.0 + 0.2
        ax.add_patch(Circle((cx + v * 6 - 3, 0), r, fc='none', ec=C['blue'], lw=1.8, alpha=0.9))
    ax.add_patch(Circle((0, 0), 0.25, color=C['red'], zorder=5)); ax.annotate('', xy=(1.3, 0), xytext=(0.3, 0), arrowprops=dict(arrowstyle='->', lw=3, color=C['red']))
    ax.text(4.4, 4.6, 'ahead: squeezed\n→ higher pitch', fontsize=17, color=C['green']); ax.text(-12.5, 4.6, 'behind: stretched\n→ lower pitch', fontsize=17, color=C['orange'])
    ax.set_xlim(-12.8, 8.5); ax.set_ylim(-6.6, 6.5); ax.axis('off')
    ax.set_title('siren at 1000 Hz moving 30 m/s: 1096 Hz ahead, 920 Hz behind', fontsize=18)
    save(fig, path)

def fig_snell(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    ax.add_patch(Rectangle((0, 0), 100, 30, fc=C['lblue'], alpha=0.6)); txt(ax, 8, 50, 'air  n = 1.00', 19, C['mut'], ha='left'); txt(ax, 8, 8, 'glass  n = 1.50', 19, C['blue'], ha='left')
    line(ax, [(50, 2), (50, 58)], C['gray'], 1.5, ls='--')
    t1 = np.radians(30); t2 = np.arcsin(np.sin(t1) / 1.5)
    arrow(ax, (50 - 28 * np.tan(t1), 58), (50, 30), color=C['orange'], lw=4); arrow(ax, (50, 30), (50 + 28 * np.tan(t2), 2), color=C['orange'], lw=4)
    arrow(ax, (50, 30), (50 + 22 * np.tan(t1), 52), color=C['orange'], lw=1.8, ls='--')
    txt(ax, 45, 44, '30°', 20, C['ink']); txt(ax, 53, 18, '19.5°', 20, C['ink'], ha='left')
    txt(ax, 82, 45, 'n₁ sin θ₁ = n₂ sin θ₂', 22, bold=True); txt(ax, 82, 36, 'sin θ₂ = 0.5 / 1.5', 19); txt(ax, 82, 10, 'bends toward the normal\nwhen it slows down', 17, C['mut'])
    save(fig, path)

def fig_tir(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    ax.add_patch(Rectangle((2, 10), 96, 20, fc=C['lblue'], ec=C['blue'], lw=2)); txt(ax, 50, 35, 'glass fiber core (cladding has lower n)', 18, C['mut'])
    pts = [(4, 26), (18, 12), (32, 28), (46, 12), (60, 28), (74, 12), (88, 28), (96, 18)]
    for a, b in zip(pts[:-1], pts[1:]): arrow(ax, a, b, color=C['orange'], lw=3, ms=14)
    txt(ax, 50, 5, 'beyond the critical angle (41.8° for n = 1.5), light reflects 100%\n→ it stays trapped for kilometers', 16, C['ink'])
    save(fig, path)

def fig_lens(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    line(ax, [(2, 25), (98, 25)], C['gray'], 1.5)
    ax.add_patch(matplotlib.patches.Ellipse((50, 25), 4, 36, fc=C['lblue'], ec=C['blue'], lw=2))
    f = 16; do = 36; di = 1 / (1 / f - 1 / do); hi = -12 * di / do
    arrow(ax, (50 - do, 25), (50 - do, 37), color=C['green'], lw=4); arrow(ax, (50 + di, 25), (50 + di, 25 + hi), color=C['red'], lw=4)
    line(ax, [(50 - do, 37), (50, 37), (50 + di, 25 + hi)], C['orange'], 2); line(ax, [(50 - do, 37), (50 + di, 25 + hi)], C['purple'], 2)
    for xx in (50 - f, 50 + f): dot(ax, xx, 25, 0.8); txt(ax, xx, 21, 'F', 18)
    txt(ax, 50 - do, 41, 'object', 18, C['green']); txt(ax, 50 + di, 25 + hi - 4, 'image (real, inverted)', 18, C['red'])
    txt(ax, 82, 44, '1/f = 1/d_o + 1/d_i', 22, bold=True); txt(ax, 82, 37, 'f = 50 mm, d_o = 2 m\n→ d_i = 51.3 mm', 17)
    save(fig, path)

def fig_slits(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, grid=False, gridspec_kw={'height_ratios': [1, 1.2]})
    y = X(-40, 40, 2000); lam, d, L = 650e-9, 1e-4, 2.0
    th = y / 1000 / L; I = np.cos(np.pi * d * np.sin(th) / lam) ** 2 * np.sinc(2e-5 * np.sin(th) / lam) ** 2
    a1.imshow(np.tile(I, (40, 1)), cmap='Reds_r' if False else 'hot', aspect='auto', extent=[-40, 40, 0, 1]); a1.set_yticks([]); a1.set_xticks([])
    a1.set_title('red laser through two slits: bright & dark fringes', fontsize=18)
    a2.plot(y, I, color=C['red']); a2.set_xlabel('position on screen (mm)'); a2.set_yticks([])
    a2.set_ylim(0, 1.6); a2.text(-39, 1.15, 'spacing = λL/d = (650 nm)(2 m)/(0.1 mm) = 13 mm', fontsize=15)
    save(fig, path)

def fig_gps(path, w, h):
    fig, ax = plot(w, h, grid=False)
    lab = ['speed\n(special rel.)', 'gravity\n(general rel.)', 'net']
    vals = [-7, 45, 38]; b = ax.bar(lab, vals, color=[C['blue'], C['orange'], C['purple']])
    for r, v in zip(b, vals): ax.text(r.get_x() + r.get_width() / 2, v + 2 if v > 0 else 2, f'{v:+d} μs/day', ha='center', fontsize=19, fontweight='bold')
    ax.axhline(0, color=C['ink'], lw=1.5); ax.set_ylim(-12, 62); ax.set_yticks([]); ax.tick_params(axis='x', labelsize=16)
    ax.set_title('GPS satellite clocks vs. ground clocks\nuncorrected: ~10 km of position error per day', fontsize=18)
    save(fig, path)

def fig_levels(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    for n in range(1, 6):
        E = -13.6 / n ** 2; y = 54 + E * 3.6
        line(ax, [(6, y), (44, y)], C['ink'], 2.5)
        if n != 4: txt(ax, 46, y + (1.6 if n == 5 else 0), f'n={n}:  {E:.2f} eV' if n != 5 else 'n=4, 5: −0.85, −0.54 eV', 16, ha='left')
    for n2, col in ((3, '#FF3030'), (4, '#30B0FF'), (5, '#6040FF')):
        x = 12 + (n2 - 3) * 9; y1 = 54 - 13.6 / n2 ** 2 * 3.6; y2 = 54 - 13.6 / 4 * 3.6
        arrow(ax, (x, y1), (x, y2), color=col, lw=3)
    txt(ax, 25, 22, 'drops to n = 2 emit visible photons\n(656, 486, 434 nm)', 16, C['mut'])
    txt(ax, 80, 50, 'E = h f = hc / λ', 24, bold=True); txt(ax, 80, 40, 'E(eV) ≈ 1240 / λ(nm)', 20)
    txt(ax, 80, 28, 'red LED: 650 nm → 1.9 eV\nblue LED: 450 nm → 2.8 eV', 18, C['orange'])
    txt(ax, 80, 12, 'LED color = semiconductor\nband-gap energy', 17, C['mut'])
    save(fig, path)

LESSON = {
 'code': 'PHYS 227', 'title': 'Waves, Optics & Modern Physics', 'tag': 'Year 2 · Foundations', 'folder': 'PHYS-227 Physics',
 'slides': [
 {'t': 'title', 'h': 'Waves, Optics & Modern Physics', 'sub': 'Oscillations, sound, light, relativity and the quantum ideas behind semiconductors', 'img': 'a:prism',
  'say': "Welcome to Physics two twenty seven: waves, optics and modern physics. This is the physics of things that wiggle, from a vibrating guitar string to the light carrying internet traffic through glass fibers. And it ends with the twentieth century revolution: relativity and quantum physics, which explain why semiconductors work at all. Every chip you'll ever design rests on the last part of this lecture."},

 {'t': 'v', 'h': 'Simple harmonic motion: the universal oscillator', 'img': ['fig:shm', 'a:quartz_watch'],
  'pts': ['Restoring force F = −kx → x(t) = A cos(ωt + φ)', 'Spring: ω = √(k/m) · pendulum: ω = √(g/L)', 'Energy sloshes between kinetic and potential', 'Quartz crystal: 32,768 Hz = 2¹⁵ → divide 15× → 1 Hz'],
  'say': ["Anything with a restoring force proportional to displacement, like a spring, oscillates as a perfect cosine. That's simple harmonic motion. For a spring, the angular frequency is the square root of k over m: stiffer springs vibrate faster, heavier masses slower. For a small pendulum, it's the square root of g over L. Energy constantly sloshes back and forth, potential at the turning points, kinetic in the middle, with the total constant.",
          "Here's where computer engineers meet it every day. Inside every watch, phone and computer is a tiny quartz crystal that vibrates like a stiff spring when driven electrically. A watch crystal is cut to vibrate at thirty two thousand seven hundred sixty eight hertz. Why that odd number? It's two to the fifteenth. Divide it by two fifteen times with a chain of flip flops, the clock divider from digital logic, and you get exactly one tick per second."]},

 {'t': 'v', 'h': 'Damping, resonance — and the RLC connection', 'img': 'fig:analogy',
  'pts': ['Friction → amplitude decays', 'Drive near the natural frequency → resonance', 'Mass–spring–damper ≡ inductor–capacitor–resistor', 'Same differential equation, same behavior'],
  'say': ["Real oscillators lose energy to friction, so the amplitude decays. That's damping.",
          "Push an oscillator periodically, and if you push near its natural frequency, the amplitude grows dramatically. That's resonance, like pushing a child on a swing at just the right moments.",
          "Now look at this table. A mass, spring and damper obey exactly the same differential equation as an inductor, capacitor and resistor in series. Mass corresponds to inductance, spring stiffness to one over capacitance, friction to resistance.",
          "So the natural frequency of an L C circuit is one over the square root of L C, just as a spring's is the square root of k over m. Radios use this resonance to select one station out of thousands. Same physics, same math, different parts."]},

 {'t': 'v', 'h': 'Waves: v = f λ', 'img': 'fig:wave',
  'pts': ['A wave carries energy, not matter', 'Transverse (string, light) vs longitudinal (sound)', 'Middle A, 440 Hz in air: λ = 343/440 ≈ 78 cm', 'Wi-Fi at 2.4 GHz: λ = c/f ≈ 12.5 cm'],
  'say': ["A wave is a disturbance that travels, carrying energy without carrying matter along. A stadium wave moves around the stadium, but each person just stands up and sits down.",
          "In a transverse wave, like a wave on a string or light, the wiggle is perpendicular to the direction of travel. In a longitudinal wave, like sound, the air molecules are pushed back and forth along the direction of travel.",
          "Every wave obeys the simplest formula in physics: speed equals frequency times wavelength. Sound travels at about three hundred forty three meters per second in air. Middle A, at four hundred forty hertz, has a wavelength of about seventy eight centimeters.",
          "Radio waves travel at the speed of light. Wi Fi at two point four gigahertz has a wavelength of about twelve and a half centimeters, which is why Wi Fi antennas are a few centimeters long. Antenna size is set by wavelength."]},

 {'t': 'v', 'h': 'Superposition and standing waves', 'img': 'fig:standing',
  'pts': ['Waves add: constructive + destructive interference', 'String fixed at both ends: λₙ = 2L/n', 'Harmonics f, 2f, 3f … give instruments their tone', 'Noise-cancelling headphones: add the inverse wave'],
  'say': ["When two waves overlap, their displacements simply add. That's superposition. Crest on crest makes a bigger wave, constructive interference. Crest on trough cancels, destructive interference.",
          "A string fixed at both ends, like a guitar string, can only vibrate in patterns that fit: wavelengths of two L over n. These are standing waves, with fixed points called nodes.",
          "So a string vibrates at its fundamental frequency and at whole number multiples, called harmonics. The mix of harmonics is why a guitar and a piano playing the same note sound different. And the idea that any sound is a sum of sine waves at different frequencies is exactly Fourier analysis, which you'll use in signals and systems.",
          "Destructive interference is also how noise cancelling headphones work: a microphone hears the noise, and the electronics play the inverted wave, so the two cancel at your ear."]},

 {'t': 'v', 'h': 'Sound: decibels and the Doppler effect', 'img': ['fig:db', 'fig:doppler'],
  'pts': ['β = 10 log(I/I₀) dB — a logarithmic scale', '+10 dB = 10× intensity; +3 dB = 2×', 'Doppler: moving source → shifted frequency', 'Radar guns, weather radar, ultrasound blood flow'],
  'say': ["Our ears handle an enormous range of intensities, so sound is measured on a logarithmic scale, in decibels. Every ten decibels is ten times the intensity. A rock concert at one hundred ten decibels is a hundred billion times more intense than the faintest sound you can hear. Engineers use decibels for signal strength and amplifier gain too: plus three decibels means double the power.",
          "And when a source moves, its waves bunch up in front and stretch out behind. That's the Doppler effect. A siren at one thousand hertz moving toward you at thirty meters per second sounds like about one thousand ninety six hertz, then drops to about nine hundred twenty as it passes. Police radar guns, weather radar and medical ultrasound all measure speed by measuring this frequency shift."]},

 {'t': 'v', 'h': 'Light bends: refraction and Snell’s law', 'img': ['a:prism', 'fig:snell'],
  'pts': ['Light slows in glass: n = c / v', 'n₁ sin θ₁ = n₂ sin θ₂', 'Air → glass at 30°: bends to 19.5°', 'n depends on color → prisms split white light'],
  'say': ["Light travels slower in glass or water than in air. The index of refraction, n, is how many times slower. For glass, about one and a half. When light enters at an angle, the change in speed bends it. And since the index depends slightly on the color, a prism bends each color by a different amount, splitting white light into a rainbow.",
          "Snell's law gives the angle: n one sine theta one equals n two sine theta two. From air into glass at thirty degrees, the sine of the new angle is point five divided by one point five, so the light bends to about nineteen and a half degrees, toward the perpendicular, as it slows down."]},

 {'t': 'v', 'h': 'Total internal reflection: the internet is made of light', 'img': 'fig:tir',
  'pts': ['Dense → less dense, beyond the critical angle: 100% reflection', 'sin θc = n₂/n₁ → 41.8° for glass to air', 'Optical fiber traps light for kilometers', 'Undersea cables carry most intercontinental data'],
  'say': ["Going the other way, from glass into air, light bends away from the perpendicular. At a steep enough angle, the critical angle, it can't get out at all. Every bit of it reflects back inside. That's total internal reflection. For glass to air, the sine of the critical angle is one over one point five, about forty two degrees. An optical fiber is a thin glass core surrounded by cladding with a slightly lower index, so light bounces along the core for kilometers.",
          "These fibers carry the backbone of the internet. Undersea fiber cables carry the vast majority of data between continents, with lasers blinking billions of times per second. Every video you stream from another country probably traveled as light through glass, trapped by this one equation."]},

 {'t': 'v', 'h': 'Lenses and cameras', 'img': 'fig:lens',
  'pts': ['Thin lens: 1/f = 1/d_o + 1/d_i', 'Camera, f = 50 mm, subject at 2 m → image at 51.3 mm', 'Focusing = moving the lens a millimeter or so', 'Phone cameras, microscopes, chip lithography'],
  'say': ["A lens bends light so that rays from one point of an object meet again at one point of an image. The thin lens equation relates the focal length to the object and image distances: one over f equals one over d o plus one over d i.",
          "A camera with a fifty millimeter lens photographing someone two meters away forms the image fifty one point three millimeters behind the lens, right on the sensor.",
          "For something very far away, the image forms at exactly fifty millimeters. So focusing just means moving the lens by about a millimeter. Your phone does that with a tiny motor, often a voice coil like a speaker.",
          "The same optics, scaled up enormously in precision, is how chips are made: lithography machines use lenses and mirrors to project circuit patterns onto silicon wafers."]},

 {'t': 'v', 'h': 'Interference and diffraction: light is a wave', 'img': 'fig:slits',
  'pts': ['Two slits: bright where d sin θ = mλ', 'Fringe spacing = λL/d = 13 mm in this example', 'Diffraction limits how small you can image', 'Chipmakers use 13.5 nm extreme-UV light to print tiny features'],
  'say': ["Shine a laser through two narrow slits, and instead of two bright lines you get a whole row of bright and dark fringes. Light from the two slits interferes: where the path lengths differ by a whole number of wavelengths, the waves add, and where they differ by half a wavelength, they cancel. This experiment, first done by Thomas Young around eighteen hundred, proved light is a wave.",
          "The fringe spacing is wavelength times distance to the screen, over the slit separation. With a red laser at six hundred fifty nanometers, slits a tenth of a millimeter apart, and a screen two meters away, the fringes are thirteen millimeters apart.",
          "Diffraction also sets a fundamental limit: you can't focus light to a spot much smaller than its wavelength. That's a huge problem for chipmakers, who need to print transistor features just a few tens of nanometers across.",
          "So the most advanced chip factories use extreme ultraviolet light with a wavelength of thirteen and a half nanometers, generated by blasting tiny droplets of tin with a laser. Wave optics directly limits how small transistors can be."]},

 {'t': 'v', 'h': 'Relativity — and why GPS needs it', 'img': ['a:gps_sat', 'fig:gps'],
  'pts': ['Speed of light is the same for every observer', 'Moving clocks run slow: Δt = γΔt₀', 'Clocks in weaker gravity run fast', 'GPS: net +38 μs/day — uncorrected, ~10 km error per day'],
  'say': ["In nineteen oh five, Einstein built special relativity on one surprising fact: the speed of light is the same for every observer, no matter how they move. The consequences: moving clocks run slow, by the factor gamma. Moving objects contract. And mass and energy are equivalent, E equals m c squared. His later theory, general relativity, adds that clocks run faster where gravity is weaker.",
          "This isn't abstract. GPS satellites carry atomic clocks and move at about fourteen thousand kilometers per hour. Special relativity makes their clocks lose about seven microseconds per day. But they're high above Earth, in weaker gravity, so general relativity makes them gain about forty five. The net is about thirty eight microseconds per day fast. Since GPS measures distance by timing radio signals at the speed of light, thirty eight microseconds is about eleven kilometers of error, every single day, if engineers didn't correct for it. They do, by deliberately setting the satellite clocks slightly slow before launch."]},

 {'t': 'v', 'h': 'Photons and quantized energy', 'img': ['fig:levels', 'a:rgb_led'],
  'pts': ['Light comes in packets: E = hf', 'Photoelectric effect: only high-enough f frees electrons', 'Atoms have discrete energy levels → sharp spectral lines', 'LED color = semiconductor band gap'],
  'say': ["Light is also a particle. Each photon carries energy h times f. Shine dim blue light on certain metals, and electrons pop out. Shine intense red light, and nothing happens, because no single red photon has enough energy. Einstein explained this photoelectric effect in nineteen oh five, and it won him the Nobel Prize. Camera sensors and solar cells work on this principle: each photon can free one electron. And atoms can only hold electrons at specific, discrete energy levels. In hydrogen, they're minus thirteen point six electron volts over n squared. When an electron drops from one level to a lower one, it emits a photon with exactly that energy difference, which is why each element glows with its own fingerprint of colors.",
          "In a solid, those levels blur into bands separated by a gap, and the size of that gap decides whether a material is a conductor, an insulator or a semiconductor. An LED emits photons with energy roughly equal to its band gap. A handy rule: energy in electron volts is about twelve hundred forty divided by the wavelength in nanometers. So a red LED's band gap is about one point nine electron volts, and a blue LED's about two point eight. That's the bridge to the electronics course, where band gaps make diodes and transistors work."]},

 {'t': 'b', 'h': 'Matter waves and the quantum world',
  'pts': ['de Broglie: particles have wavelength λ = h / p', 'Electron microscopes resolve atoms', 'Tunneling: electrons can pass through thin barriers', 'Flash memory stores bits by tunneling charge onto a floating gate'],
  'say': ["One more twist. If waves can act like particles, particles can act like waves. Louis de Broglie proposed that every particle has a wavelength, h over its momentum.",
          "Electrons have wavelengths far shorter than visible light, which is why electron microscopes can image individual atoms, and why chipmakers use them to inspect their transistors.",
          "Waves can also leak through thin barriers that a classical particle could never cross. That's quantum tunneling.",
          "And you're using tunneling right now. Flash memory, in your phone and in every S S D, stores each bit by forcing electrons to tunnel through a very thin insulating layer onto an isolated floating gate, where they stay trapped for years. Quantum mechanics isn't just theory. It's in your pocket."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Oscillators keep time, **waves** carry energy and data, **light** bends and interferes, and **quantum** energy levels make semiconductors possible.',
  'cap': 'Next: CPSC 131, Data Structures.',
  'say': "To recap. Simple harmonic motion describes every oscillator, from quartz clocks to L C circuits. Waves obey v equals f lambda, superpose, and form standing waves and harmonics. Light refracts, reflects, and interferes, which gives us fiber optics, cameras and the limits of chip manufacturing. Relativity keeps GPS accurate. And quantum physics, with photons and discrete energy levels, explains LEDs, solar cells, flash memory and the semiconductors at the heart of computing. Next, back to software, with data structures. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B

def draw_shm(ax, n, w, h):
    y = h * 0.78
    if n >= 1:
        B.ln(ax, [40, 40], [y - 60, y + 60], lw=5)
        xs = np.linspace(40, 260, 15); B.ln(ax, xs, y + np.array([0, 22, -22] * 5)[:15], lw=2.5)
        B.rect(ax, 260, y - 50, 110, 100, fc='#dfe8f7'); B.lab(ax, 315, y, '0.5 kg', 26)
        B.lab(ax, 150, y + 60, 'k = 200 N/m', 24, 'gray')
    if n >= 2:
        X0, Y0, sx, sy = 60, h * 0.32, 700, 140
        B.arr(ax, X0, Y0, X0 + sx * 1.05, Y0, 'gray', 2, 18); B.lab(ax, X0 + sx * 1.05, Y0 - 25, 't', 26, 'gray')
        ts = np.linspace(0, 0.63, 200); B.ln(ax, X0 + ts / 0.63 * sx, Y0 + sy * np.cos(20 * ts), c='blue', lw=3)
        B.arr(ax, X0, Y0 - sy - 30, X0 + 0.314 / 0.63 * sx, Y0 - sy - 30, 'red', 2, 16, '<|-|>'); B.lab(ax, X0 + 0.157 / 0.63 * sx, Y0 - sy - 60, 'T = 0.314 s', 26, 'red')

def draw_modes(ax, n, w, h):
    L = w - 140; X0 = 70
    for k in (1, 2, 3):
        if n >= k:
            y0 = h - 150 - (k - 1) * 230
            xs = np.linspace(0, 1, 200)
            B.ln(ax, X0 + xs * L, y0 + 70 * np.sin(k * np.pi * xs), c='blue', lw=3)
            B.ln(ax, X0 + xs * L, y0 - 70 * np.sin(k * np.pi * xs), c='blue', lw=1.5, ls='--')
            B.dot(ax, X0, y0, s=12); B.dot(ax, X0 + L, y0, s=12)
            B.lab(ax, X0 + L / 2, y0 - 110, ['', '110 Hz  (λ = 1.3 m)', '220 Hz', '330 Hz'][k], 28, 'red')

def draw_doppler(ax, n, w, h):
    cy = h * 0.45; xs = w * 0.62
    if n >= 1:
        t = np.linspace(0, 2 * np.pi, 120)
        for r in (60, 130, 200, 270):          # older crests are bigger and were emitted further back
            B.ln(ax, xs - 0.4 * r + r * np.cos(t), cy + r * np.sin(t), c='gray', lw=2)
        B.dot(ax, xs, cy, c='red', s=26); B.arr(ax, xs + 20, cy, xs + 110, cy, 'red', 3); B.lab(ax, xs + 70, cy + 30, '30 m/s', 24, 'red')
    if n >= 2:
        B.lab(ax, w - 20, cy + 330, 'ahead: crests bunch up,\nhigher pitch', 24, 'blue', ha='right')
        B.lab(ax, 20, cy - 330, 'behind: crests spread out,\nlower pitch', 24, 'green', ha='left')

def draw_snell(ax, n, w, h):
    cx, cy = w * 0.5, h * 0.5
    if n >= 1:
        B.poly(ax, [(20, 20), (w - 20, 20), (w - 20, cy), (20, cy)], fc='#dfe8f7', c='none', lw=0)
        B.ln(ax, [20, w - 20], [cy, cy], c='blue', lw=3); B.ln(ax, [cx, cx], [40, h - 40], c='gray', lw=1.5, ls='--')
        B.lab(ax, 70, cy - 40, 'water  n = 1.33', 26, 'blue', ha='left'); B.lab(ax, 70, cy + 40, 'air  n = 1.00', 26, 'gray', ha='left')
    a1, a2, L = np.radians(40), np.radians(58.75), 300
    if n >= 2:
        B.arr(ax, cx - L * np.sin(a1), cy - L * np.cos(a1), cx, cy, 'red', 3.5); B.lab(ax, cx - 70, cy - 150, '40°', 28, 'red')
    if n >= 3:
        B.arr(ax, cx, cy, cx + L * np.sin(a2), cy + L * np.cos(a2), 'red', 3.5); B.lab(ax, cx + 95, cy + 120, '58.8°', 28, 'red')
    if n >= 4:
        ac = np.radians(48.75)
        B.ln(ax, [cx - L * np.sin(ac), cx], [cy - L * np.cos(ac), cy], c='orange', lw=2.5, ls='--')
        B.ln(ax, [cx, cx + L], [cy, cy], c='orange', lw=2.5, ls='--'); B.lab(ax, cx - 330, cy - 110, 'critical 48.8°', 26, 'orange', bbox=dict(fc='#dfe8f7', ec='none', pad=1))

B.insert(LESSON, 'Simple harmonic motion', {'t': 'wb', 'h': 'Worked example: a mass on a spring', 'draw': 'shm', 'split': 0.5, 'steps': [
    {'say': "Let's work out a spring and mass completely. A half kilogram mass hangs on a spring with stiffness two hundred newtons per meter. How fast does it oscillate? The angular frequency is the square root of k over m: two hundred over point five is four hundred, and its square root is twenty radians per second.",
     'w': [{'d': 1, 'at': 1}, {'m': r'$\omega = \sqrt{k/m} = \sqrt{200/0.5} = \sqrt{400} = 20\ \mathrm{rad/s}$', 'at': 3}]},
    {'say': "Convert to ordinary frequency by dividing by two pi: about three point one eight cycles per second. The period is one over that: about point three one four seconds per bounce.",
     'w': [r'$f = \frac{\omega}{2\pi} \approx 3.18\ \mathrm{Hz}$', {'m': r'$T = \frac{1}{f} = \frac{2\pi}{\omega} \approx 0.314\ \mathrm{s}$', 'c': 'red', 'box': True, 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "Pull it five centimeters and let go. The motion is x equals point zero five cosine twenty t. The fastest it moves, through the middle, is amplitude times omega: point zero five times twenty, one meter per second. Notice the period doesn't depend on how far you pull it. That's exactly why a quartz crystal or a pendulum makes a reliable clock.",
     'w': [{'m': r'$x(t) = 0.05\cos(20t)$', 'at': 1}, {'m': r'$v_{max} = A\omega = (0.05)(20) = 1\ \mathrm{m/s}$', 'at': 2}]},
]})

B.insert(LESSON, 'Superposition and standing waves', {'t': 'wb', 'h': 'Worked example: the notes of a guitar string', 'draw': 'modes', 'split': 0.5, 'steps': [
    {'say': "A guitar string is sixty five centimeters long and plays a fundamental of one hundred ten hertz, the note A. The fundamental fits half a wavelength on the string, so the wavelength is twice the length: one point three meters.",
     'w': [{'m': r'$L = 0.65\ \mathrm{m}$,   $f_1 = 110\ \mathrm{Hz}$'}, {'m': r'$\lambda_1 = 2L = 1.3\ \mathrm{m}$', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "So the wave speed on the string is f times lambda: one hundred ten times one point three, about one hundred forty three meters per second. That speed is set by the string's tension and thickness, which is why tightening a tuning peg raises the pitch.",
     'w': [r'$v = f\lambda = 110 \times 1.3 \approx 143\ \mathrm{m/s}$']},
    {'say': "The string can also vibrate with two half waves, or three. Those harmonics have wavelengths L and two thirds L, so their frequencies are two hundred twenty and three hundred thirty hertz: exactly two and three times the fundamental. The mix of these harmonics is what makes a guitar sound different from a flute playing the same note.",
     'w': [{'d': 2, 'at': 0}, {'d': 3, 'at': 0}, {'m': r'$f_n = n\,f_1$:   110, 220, 330 Hz', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Sound: decibels and the Doppler', {'t': 'wb', 'h': 'Worked example: the Doppler shift of a siren', 'draw': 'doppler', 'split': 0.5, 'steps': [
    {'say': "An ambulance siren sounds at seven hundred hertz and drives at thirty meters per second. Sound travels at three hundred forty three meters per second. What pitch do you hear as it approaches, and as it leaves? Look at the drawing: ahead of the ambulance, the wave crests bunch up.",
     'w': [{'m': r'$f = 700\ \mathrm{Hz}$,   $v_s = 30\ \mathrm{m/s}$,   $v = 343\ \mathrm{m/s}$', 'at': 1}, {'d': 1, 'at': 4}, {'d': 2, 'at': 4}]},
    {'say': "Approaching, the crests arrive closer together. The formula divides by the speed of sound minus the source speed: seven hundred times three forty three, over three thirteen. That's about seven hundred sixty seven hertz.",
     'w': [r'$f_{approach} = f\,\frac{v}{v - v_s} = 700\cdot\frac{343}{313}$', {'m': r'$\approx 767\ \mathrm{Hz}$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "Moving away, you add instead: seven hundred times three forty three over three seventy three, about six hundred forty four hertz. So the pitch drops by more than a hundred hertz as it passes you. Police radar and weather radar use the same shift, with radio waves, to measure speed.",
     'w': [r'$f_{away} = f\,\frac{v}{v + v_s} = 700\cdot\frac{343}{373}$', {'m': r'$\approx 644\ \mathrm{Hz}$', 'c': 'blue', 'box': True, 'at': 0}]},
]})

B.insert(LESSON, 'Light bends', {'t': 'wb', 'h': 'Worked example: light leaving water', 'draw': 'snell', 'split': 0.52, 'steps': [
    {'say': "Light travels from water into air. Water's index is one point three three, air's is one. The light hits the surface at forty degrees from the normal. Where does it go?",
     'w': [{'d': 1, 'at': 1}, {'d': 2, 'at': 2}, {'m': r'$n_1 = 1.33$,   $n_2 = 1.00$,   $\theta_1 = 40°$', 'at': 2}]},
    {'say': "Snell's law: n one sine theta one equals n two sine theta two. One point three three times sine forty is about point eight five five. Since air's index is one, that's sine theta two directly. The inverse sine gives fifty eight point eight degrees. It bends away from the normal, because it speeds up.",
     'w': [r'$n_1\sin\theta_1 = n_2\sin\theta_2$', {'m': r'$\sin\theta_2 = 1.33\,\sin 40° \approx 0.855$', 'at': 1}, {'m': r'$\theta_2 \approx 58.8°$', 'c': 'red', 'box': True, 'at': 3}, {'d': 3, 'at': 3}]},
    {'say': "Tilt the beam more and the outgoing angle grows until it reaches ninety degrees. That happens when sine theta one equals one over one point three three, at about forty eight point eight degrees: the critical angle. Beyond it, all the light reflects back into the water. That's total internal reflection, and it's how optical fiber traps light.",
     'w': [{'d': 4, 'at': 1}, {'m': r'$\sin\theta_c = \frac{1}{1.33} \;\Rightarrow\; \theta_c \approx 48.8°$', 'at': 1}]},
]})

B.insert(LESSON, 'Photons and quantized energy', {'t': 'wb', 'h': 'Worked example: counting photons in a laser pointer', 'steps': [
    {'say': "How many photons does a red laser pointer emit? Take a five milliwatt laser at six hundred fifty nanometers. First, the energy of one photon: E equals h c over lambda.",
     'w': [{'m': r'red laser: $P = 5\ \mathrm{mW}$,   $\lambda = 650\ \mathrm{nm}$', 'at': 1}, {'m': r'$E = \frac{hc}{\lambda}$', 'at': 2}]},
    {'say': "Plug in Planck's constant, six point six three times ten to the minus thirty four, times the speed of light, three times ten to the eighth, over six fifty times ten to the minus nine. That's about three point oh six times ten to the minus nineteen joules. In electron volts, about one point nine one.",
     'w': [r'$E = \frac{(6.63\times 10^{-34})(3\times 10^{8})}{650\times 10^{-9}}$', {'m': r'$\approx 3.06\times 10^{-19}\ \mathrm{J} \approx 1.91\ \mathrm{eV}$', 'at': 1}]},
    {'say': "The laser emits five thousandths of a joule every second. Divide by the energy per photon: about one point six times ten to the sixteen photons per second. Sixteen quadrillion! Each photon is tiny, which is why light looks smooth and continuous. And that one point nine electron volts is no accident: it matches the band gap of the semiconductor in a red laser diode or LED.",
     'w': [{'m': r'$\frac{P}{E} = \frac{5\times 10^{-3}}{3.06\times 10^{-19}} \approx 1.6\times 10^{16}$ photons/s', 'c': 'red', 'box': True, 'at': 1}]},
]})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Simple harmonic motion'
B.spen(LESSON, S, 0, {'fig': [('underline', .25, .84, .07)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .64, .84, .07)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .36, .47, .04, .05)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .31, .93, .04, .05)], 'c': 'orange', 'at': 4, 'dt': 2.0})
S = 'Damping, resonance'
B.spen(LESSON, S, 2, *[{'fig': [('highlight', .07, y0, .93, y1)], 'c': 'orange', 'at': 2, 'dt': t, 'solo': True} for y0, y1, t in
       ((.15, .3, 0), (.31, .46, 1.6), (.47, .62, 3.2))])
B.spen(LESSON, S, 3, {'fig': [('box', .07, .78, .93, .97)], 'c': 'green', 'at': 0})
S = 'Waves: v'
B.spen(LESSON, S, 0, {'fig': [('arrow', .7, .85, .95, .85)], 'c': 'red', 'at': 0, 'dt': 2.0})
B.spen(LESSON, S, 2, {'fig': [('circle', .505, .05, .09, .05)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .2, .48, .215)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('underline', .2, .48, .215)], 'c': 'orange', 'at': 1})
S = 'Superposition'
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, y, .025, .045)], 'c': 'red', 'at': 1, 'dt': t} for x, y, t in
       ((.06, .18, 0), (.62, .18, .5), (.34, .5, 1.0), (.25, .82, 1.5), (.435, .82, 2.0))])
B.spen(LESSON, S, 2, {'fig': [('box', .62, .1, .99, .23)], 'c': 'blue', 'at': 0}, {'fig': [('box', .62, .43, .99, .56)], 'c': 'blue', 'at': 0, 'dt': 1.0},
       {'fig': [('box', .62, .75, .99, .88)], 'c': 'blue', 'at': 0, 'dt': 2.0})
S = 'Sound: decibels'
B.spen(LESSON, S, 0, {'fig': [('underline', .28, .97, .09)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .72, .3, .06, .05)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .19, .79, .14, .04)], 'c': 'green', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('box', .72, .08, .98, .25)], 'c': 'green', 'at': 2}, {'fig': [('box', .1, .08, .38, .25)], 'c': 'orange', 'at': 2, 'dt': 3.0},
       {'fig': [('arrow', .6, .5, .78, .5)], 'c': 'green', 'at': 1})
S = 'Relativity'
B.spen(LESSON, S, 1, {'fig': [('circle', .22, .73, .13, .06)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .5, .3, .13, .05)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .78, .37, .13, .05)], 'c': 'purple', 'at': 4}, {'fig': [('underline', .1, .9, .14)], 'c': 'red', 'at': 5})
S = 'Total internal reflection'
B.spen(LESSON, S, 0, {'fig': [('circle', .32, .3, .04, .08)], 'c': 'red', 'at': 2}, {'fig': [('circle', .6, .3, .04, .08)], 'c': 'red', 'at': 2, 'dt': 0.8},
       {'fig': [('underline', .3, .47, .9)], 'c': 'orange', 'at': 4}, {'fig': [('box', .01, .19, .98, .7)], 'c': 'blue', 'at': 5})
S = 'Lenses and cameras'
B.spen(LESSON, S, 0, {'fig': [('circle', .14, .25, .04, .09)], 'c': 'green', 'at': 0}, {'fig': [('circle', .79, .65, .04, .09)], 'c': 'red', 'at': 0, 'dt': 2.0},
       {'fig': [('underline', .66, .98, .07)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .67, .17, .95, .3)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .66, .48, .03, .06)], 'c': 'purple', 'at': 0})
S = 'Interference and diffraction'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .25, .05, .17)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .44, .25, .025, .17)], 'c': 'blue', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 1, {'fig': [('underline', .09, .83, .59)], 'c': 'blue', 'at': 0}, {'fig': [('arrow', .5, .66, .63, .66)], 'c': 'red', 'at': 1, 'dt': 2.0},
       {'fig': [('circle', .79, .57, .05, .04)], 'c': 'red', 'at': 1, 'dt': 4.0})
S = 'Photons and quantized'
B.spen(LESSON, S, 0, {'fig': [('box', .65, .11, .95, .2)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .55, .9, .08, .04)], 'c': 'purple', 'at': 7},
       {'fig': [('circle', .12, .24, .025, .07)], 'c': 'red', 'at': 8}, {'fig': [('circle', .21, .21, .025, .1)], 'c': 'blue', 'at': 8, 'dt': 0.7},
       {'fig': [('circle', .3, .2, .025, .11)], 'c': 'purple', 'at': 8, 'dt': 1.4})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Worked example: the Doppler shift of a siren', {'t': 'wb', 'h': 'Decibels by hand: the 10 vs 20 rule', 'steps': [
    {'say': "Decibels will follow you into every electronics course, so let's get them exactly right. A decibel compares two powers: ten times the log of the power ratio. A power ratio of one hundred is ten log one hundred, twenty decibels. A ratio of two is about three decibels.",
     'w': [{'m': r'power:  $dB = 10\log_{10}\frac{P_2}{P_1}$', 'c': 'blue', 'at': 1},
           {'m': r'$\times 100 \to 20\ dB$     $\times 2 \to 3\ dB$     $\times\frac{1}{2} \to -3\ dB$', 'at': 3}]},
    {'say': "Here's the trap. Engineers often measure voltages, not powers. But power goes as voltage squared. The square comes out of the log as a factor of two, so for voltages, it's twenty log of the ratio.",
     'w': [{'m': r'$P \propto V^2$:   $10\log\frac{V_2^2}{V_1^2} = 20\log_{10}\frac{V_2}{V_1}$', 'c': 'green', 'at': 2}]},
    {'say': "So an amplifier that multiplies voltage by ten has a gain of twenty decibels, not ten. And it multiplies power by one hundred, which is also twenty decibels. Same answer, as it must be. Use ten for power ratios, twenty for voltage or current ratios.",
     'w': [{'m': r'voltage $\times 10$:  $20\log 10 = 20\ dB$  = power $\times 100$', 'at': 1, 'box': True}]},
    {'say': "The most important number: minus three decibels. It's half the power, and one over root two, point seven oh seven, of the voltage. When you meet a filter's cutoff frequency in circuits and signals, it's defined exactly there: the frequency where the output drops three decibels.",
     'w': [{'m': r'$-3\ dB$:  power $\times\frac{1}{2}$,  voltage $\times 0.707$', 'c': 'red', 'box': True, 'at': 1, 'gap': 16},
           {'m': 'a filter cutoff = the −3 dB point', 'c': 'purple', 'at': 2}]},
]})

G = 'Decibels by hand: the 10 vs 20 rule'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'= 20\log_{10}', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'a filter cutoff', 'c': 'purple', 'at': 2})
