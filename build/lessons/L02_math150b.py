import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_xex(path, w, h):
    fig, ax = plot(w, h)
    x = X(0, 2, 200); ax.plot(x, x * np.exp(x), color=C['blue'], label=r'$x\,e^x$')
    ax.fill_between(x, 0, x * np.exp(x), color=C['lblue']); axes0(ax)
    ax.set_title(r'$\int_0^2 x e^x\,dx = [x e^x - e^x]_0^2 = e^2 + 1 \approx 8.39$')
    save(fig, path)

def fig_sin2(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 4 * np.pi, 600)
    ax.plot(t, np.sin(t), color=C['gray'], lw=2, label=r'$\sin t$'); ax.plot(t, np.sin(t) ** 2, color=C['blue'], label=r'$\sin^2 t$')
    ax.axhline(0.5, color=C['orange'], ls='--', lw=2.5, label='average = 1/2'); axes0(ax)
    ax.legend(loc='lower right', ncol=3); ax.set_ylim(-1.3, 1.4); ax.set_xticks([])
    ax.set_title(r'$\sin^2 t = \frac{1}{2} - \frac{1}{2}\cos 2t$  →  average value $\frac{1}{2}$')
    save(fig, path)

def fig_circle(path, w, h):
    fig, ax = plot(w, h, grid=False); ax.set_aspect('equal')
    th = X(0, 2 * np.pi, 300); ax.plot(np.cos(th), np.sin(th), color=C['blue'])
    x0 = 0.45; y0 = np.sqrt(1 - x0 ** 2)
    ax.add_patch(Rectangle((x0, -y0), 0.05, 2 * y0, fc=C['orange'], ec=C['orange'], alpha=0.8))
    ax.plot([0, 1], [0, 0], color=C['ink'], lw=2); ax.text(0.5, 0.05, 'r', fontsize=22, ha='center')
    ax.text(1.08, 0.35, r'strip height' + '\n' + r'$2\sqrt{r^2-x^2}$', fontsize=19, color=C['orange'], va='center')
    ax.set_xlim(-1.2, 1.9); ax.set_ylim(-1.2, 1.2); ax.axis('off')
    ax.set_title(r'Area $= \int_{-r}^{r} 2\sqrt{r^2-x^2}\,dx = \pi r^2$' + '\n' + r'(substitute $x = r\sin\theta$)', fontsize=22)
    save(fig, path)

def fig_improper(path, w, h):
    fig, ax = plot(w, h)
    x = X(1, 10, 300)
    ax.plot(x, 1 / x, color=C['red'], label=r'$1/x$: area = ∞ (diverges)'); ax.plot(x, 1 / x ** 2, color=C['blue'], label=r'$1/x^2$: area = 1')
    ax.fill_between(x, 0, 1 / x ** 2, color=C['lblue']); ax.set_xlim(0, 10); ax.set_ylim(0, 1.1); ax.legend(loc='upper right')
    ax.set_title(r'$\int_1^{\infty}\frac{1}{x^2}dx = \lim_{b\to\infty}\left(1-\frac{1}{b}\right) = 1$')
    save(fig, path)

def fig_simpson(path, w, h):
    fig, ax = plot(w, h)
    f = lambda t: np.exp(-t ** 2); x = X(0, 1, 200); ax.plot(x, f(x), color=C['blue'], zorder=5)
    xs = X(0, 1, 5)
    for a, b in zip(xs[:-1], xs[1:]):
        ax.add_patch(Polygon([(a, 0), (a, f(a)), (b, f(b)), (b, 0)], fc=C['lorange'], ec=C['orange'], lw=1.8, alpha=0.8))
    ax.set_xlim(0, 1.02); ax.set_ylim(0, 1.15)
    ax.set_title(r'$\int_0^1 e^{-x^2}dx$ has no formula — compute it numerically')
    note(ax, 0.03, 0.12, 'trapezoids (n=4): 0.74298\nSimpson (n=4):    0.74686\ntrue value:          0.74682', fs=20)
    save(fig, path)

def fig_disk(path, w, h):
    fig = plt.figure(figsize=(w * 0.8 / 100, h * 0.8 / 100), dpi=100); ax = fig.add_subplot(projection='3d')
    xs = X(0, 4, 60); th = X(0, 2 * np.pi, 60); Xg, T = np.meshgrid(xs, th); R = np.sqrt(Xg)
    ax.plot_surface(Xg, R * np.cos(T), R * np.sin(T), color=C['lblue'], alpha=0.55, linewidth=0)
    xd = 2.5; r = np.sqrt(xd)
    for dx in (0, 0.15):
        ax.plot(np.full_like(th, xd + dx), r * np.cos(th), r * np.sin(th), color=C['orange'], lw=2.5)
    ax.plot(xs, np.sqrt(xs), 0 * xs, color=C['blue'], lw=3.5)
    ax.set_box_aspect((2, 1, 1)); ax.set_yticks([]); ax.set_zticks([])
    ax.set_title(r'disk at x: area $\pi(\sqrt{x})^2$;  $V=\pi\int_0^4 x\,dx = 8\pi$', fontsize=21)
    save(fig, path)

def fig_spring(path, w, h):
    fig, ax = plot(w, h)
    x = X(0, 0.1, 100); ax.plot(x, 200 * x, color=C['blue']); ax.fill_between(x, 0, 200 * x, color=C['lblue'])
    ax.set_xlabel('stretch x (m)'); ax.set_ylabel('force F = kx (N)'); ax.set_xlim(0, 0.11); ax.set_ylim(0, 22)
    ax.text(0.068, 5, r'$W=\int_0^{0.1} 200x\,dx$' + '\n' + r'$= \frac{1}{2}(200)(0.1)^2 = 1$ J', fontsize=21, ha='center')
    ax.set_title('Work = area under the force curve')
    save(fig, path)

def fig_zeno(path, w, h):
    fig, ax = plot(w, h, grid=False); ax.set_aspect('equal'); ax.axis('off')
    x0, y0, W_, H_ = 0, 0, 1.0, 1.0; cols = [C['blue'], C['orange'], C['green'], C['purple'], C['teal'], C['red'], C['yellow']]
    labels = ['1/2', '1/4', '1/8', '1/16', '1/32', '', '']
    for k in range(7):
        if k % 2 == 0:
            ax.add_patch(Rectangle((x0, y0), W_ / 2, H_, fc=cols[k], ec='white', lw=2)); ax.text(x0 + W_ / 4, y0 + H_ / 2, labels[k], ha='center', va='center', color='white', fontsize=26 - 3 * k, fontweight='bold'); x0 += W_ / 2; W_ /= 2
        else:
            ax.add_patch(Rectangle((x0, y0), W_, H_ / 2, fc=cols[k], ec='white', lw=2)); ax.text(x0 + W_ / 2, y0 + H_ / 4, labels[k], ha='center', va='center', color='white', fontsize=26 - 3 * k, fontweight='bold'); y0 += H_ / 2; H_ /= 2
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
    ax.set_title('1/2 + 1/4 + 1/8 + … fills the square exactly: sum = 1')
    save(fig, path)

def fig_harmonic(path, w, h):
    fig, ax = plot(w, h)
    n = np.arange(1, 201)
    ax.plot(n, np.cumsum(1 / n), color=C['red'], label='1 + 1/2 + 1/3 + … (diverges)')
    ax.plot(n, np.cumsum(1 / n ** 2), color=C['blue'], label='1 + 1/4 + 1/9 + … → π²/6 ≈ 1.645')
    ax.axhline(np.pi ** 2 / 6, color=C['blue'], ls=':', lw=1.8)
    ax.set_xlabel('number of terms'); ax.set_ylabel('partial sum'); ax.legend(loc='upper left'); ax.set_ylim(0, 9)
    note(ax, 110, 2.4, 'grows like ln n:\n100 terms ≈ 5.19\n1000 terms ≈ 7.49', C['red'], 18)
    save(fig, path)

def fig_tests(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    rows = [('n-th term', 'terms don’t → 0  ⇒  diverges', 'Σ n/(n+1)'), ('geometric', 'Σ arⁿ converges iff |r| < 1', 'Σ (2/3)ⁿ = 3'),
            ('p-series', 'Σ 1/nᵖ converges iff p > 1', 'Σ 1/n² ✓  Σ 1/n ✗'), ('ratio', 'lim |aₙ₊₁/aₙ| < 1 ⇒ converges', 'Σ n/2ⁿ = 2'),
            ('comparison', 'smaller than a convergent series', 'Σ 1/(n²+1)'), ('alternating', 'terms shrink to 0, signs alternate', '1 − 1/2 + 1/3 … = ln 2')]
    table(ax, 1, H - 2, ['test', 'rule', 'example'], rows, [17, 50, 31], 7.6, 17)
    save(fig, path)

def _taylor(path, w, h, k):
    fig, ax = plot(w, h)
    x = X(-2 * np.pi, 2 * np.pi, 500); ax.plot(x, np.sin(x), color=C['ink'], lw=4, label='sin x')
    terms = [1, 3, 5, 7, 9]; cols = [C['orange'], C['green'], C['purple'], C['red'], C['teal']]
    from math import factorial
    for i, n in enumerate(terms[:k + 1]):
        p = sum((-1) ** j * x ** (2 * j + 1) / factorial(2 * j + 1) for j in range((n + 1) // 2))
        ax.plot(x, p, color=cols[i], lw=2.6 if i == k else 1.6, alpha=1 if i == k else 0.5, label=f'degree {n}')
    ax.set_ylim(-2, 2); axes0(ax); ax.legend(loc='upper right', ncol=2, fontsize=17)
    ax.set_title(r'$\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots$')
    save(fig, path)
for _k in range(5):
    globals()[f'fig_taylor{_k}'] = (lambda kk: (lambda p, w, h: _taylor(p, w, h, kk)))(_k)

def fig_geom(path, w, h):
    fig, ax = plot(w, h)
    x = X(-1.5, 1.5, 400); xx = x[x < 0.97]
    ax.plot(xx, 1 / (1 - xx), color=C['ink'], lw=4, label='1/(1−x)')
    for n, c in ((2, C['orange']), (5, C['green']), (12, C['purple'])):
        ax.plot(x, sum(x ** k for k in range(n + 1)), color=c, lw=2, label=f'1 + x + … + x^{n}')
    ax.axvspan(-1, 1, color=C['lgreen'], alpha=0.5); ax.text(0, -2.4, 'converges for −1 < x < 1', ha='center', fontsize=19, color=C['green'])
    ax.set_ylim(-3, 8); axes0(ax); ax.legend(loc='upper left', fontsize=17)
    save(fig, path)

def fig_euler(path, w, h):
    fig, ax = plot(w, h, grid=False); ax.set_aspect('equal')
    th = X(0, 2 * np.pi, 300); ax.plot(np.cos(th), np.sin(th), color=C['gray'], lw=2)
    a = 0.9; ax.annotate('', xy=(np.cos(a), np.sin(a)), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', lw=3.5, color=C['blue'], mutation_scale=25))
    ax.plot([np.cos(a), np.cos(a)], [0, np.sin(a)], '--', color=C['orange'], lw=2.5); ax.plot([0, np.cos(a)], [0, 0], color=C['green'], lw=4)
    ax.text(np.cos(a) / 2, -0.13, r'$\cos\theta$', fontsize=24, ha='center', color=C['green'])
    ax.text(np.cos(a) + 0.05, np.sin(a) / 2, r'$\sin\theta$', fontsize=24, color=C['orange'])
    ax.text(0.15, 0.08, r'$\theta$', fontsize=24); ax.text(np.cos(a) + 0.03, np.sin(a) + 0.07, r'$e^{i\theta}$', fontsize=26, color=C['blue'])
    ax.axhline(0, color=C['ink'], lw=1.2); ax.axvline(0, color=C['ink'], lw=1.2)
    ax.text(1.12, 0.03, 'real', fontsize=18); ax.text(0.03, 1.12, 'imaginary', fontsize=18)
    ax.set_xlim(-1.3, 1.5); ax.set_ylim(-1.3, 1.3); ax.axis('off')
    ax.set_title(r'$e^{i\theta} = \cos\theta + i\sin\theta$', fontsize=28)
    save(fig, path)

def fig_cardioid(path, w, h):
    fig = plt.figure(figsize=(w * 0.8 / 100, h * 0.8 / 100), dpi=100); ax = fig.add_subplot(projection='polar')
    th = X(0, 2 * np.pi, 400); ax.plot(th, 0.5 * (1 + np.cos(th)), color=C['blue'], lw=3.5); ax.fill(th, 0.5 * (1 + np.cos(th)), color=C['lblue'], alpha=0.6)
    ax.set_theta_zero_location('N'); ax.set_yticklabels([]); ax.set_title(r'cardioid pickup pattern: $r = \frac{1}{2}(1+\cos\theta)$', fontsize=21, pad=20)
    ax.text(1.02, 0.92, 'front (0°):\nfull sensitivity', transform=ax.transAxes, fontsize=18, color=C['green'])
    ax.text(1.02, 0.05, 'back (180°):\nrejects sound', transform=ax.transAxes, fontsize=18, color=C['red'])
    save(fig, path)

LESSON = {
 'code': 'MATH 150B', 'title': 'Calculus II', 'tag': 'Year 1 · Foundations', 'folder': 'MATH-150B Calculus II',
 'slides': [
 {'t': 'title', 'h': 'Calculus II', 'sub': 'Integration techniques, applications, and infinite series', 'img': 'a:calculator',
  'say': "Welcome to Calculus two. In Calculus one, we learned what derivatives and integrals are. In Calculus two, we get good at integrals, we use them to compute real quantities like volume and work, and then we take a fascinating detour into infinite sums, which turn out to be how your calculator computes sine, cosine and e to the x. Let's go."},

 {'t': 'v', 'h': 'Where Calculus II shows up in engineering', 'img': ['a:water_tower', 'a:calculator', 'fig:euler'],
  'pts': ['Volumes, work, energy: tanks, springs, capacitors', 'Series: how calculators and computers evaluate sin, cos, eˣ', "Euler's formula → phasors, the language of AC circuits"],
  'say': ["Here's why this course matters. Engineers compute volumes, like how much water a tank like this holds. They compute work and energy, like the energy stored in a spring or a capacitor. All of those are integrals.",
          "Your calculator, and every computer math library, evaluates functions like sine and e to the x using polynomials built from infinite series. You'll see exactly how by the end of this lecture.",
          "And infinite series give us Euler's formula, e to the i theta equals cosine theta plus i sine theta. That one formula is the foundation of how electrical engineers analyze AC circuits and signals. So this course quietly sets up half of your later degree."]},

 {'t': 'section', 'kicker': 'Part 1', 'h': 'Integration techniques', 'sub': 'Tools for integrals that aren’t simple powers',
  'say': "Part one. Integration techniques. Integration is harder than differentiation, because there's no product rule or chain rule that always works. Instead, we have a toolbox."},

 {'t': 'ex', 'h': 'Integration by parts: the product rule in reverse', 'img': 'fig:xex', 'split': 0.52,
  'code': "∫ u dv = u·v − ∫ v du\n\nExample:  ∫ x·eˣ dx\n  u  = x      dv = eˣ dx\n  du = dx     v  = eˣ\n\n= x·eˣ − ∫ eˣ dx\n= x·eˣ − eˣ + C\n\nPick u by LIATE:\nLog, Inverse trig, Algebraic,\nTrig, Exponential",
  'say': "The first tool is integration by parts. It comes from the product rule, run backwards, and it says the integral of u d v equals u times v, minus the integral of v d u. The idea is to trade an integral you can't do for one you can. Example: the integral of x times e to the x. Choose u equals x, because its derivative is simpler, just one. Then d v is e to the x d x, so v is e to the x. Plug in: x e to the x, minus the integral of e to the x, which gives x e to the x minus e to the x, plus C. To choose u, a handy rule is LIATE: logs first, then inverse trig, then algebraic, then trig, then exponentials. Pick whichever comes first in that list as u. You'll use this exact technique in signals and systems to compute Laplace and Fourier transforms."},

 {'t': 'v', 'h': 'Trig integrals — and why your outlet says 120 volts', 'img': 'fig:sin2',
  'pts': ['Half-angle identity: sin²t = ½ − ½cos 2t', 'Average of sin² over a cycle = ½', 'RMS voltage: V_rms = V_peak / √2', 'US outlet: 120 V rms → peaks at ≈ 170 V'],
  'say': ["Integrals of powers of sine and cosine use trig identities. The most useful is the half angle identity: sine squared t equals one half minus one half cosine two t.",
          "Integrate that over a full cycle. The cosine part averages to zero, so the average of sine squared is exactly one half. You can see it in the graph: the blue sine squared wave bounces between zero and one, centered on one half.",
          "Here's why engineers care. The power delivered by an AC voltage depends on the voltage squared. So the effective voltage, called R M S for root mean square, is the square root of the average of the square. For a sine wave, that's the peak times the square root of one half, which is the peak divided by root two.",
          "That's why a U S wall outlet labeled one hundred twenty volts actually swings up to about one hundred seventy volts at its peak. One twenty times root two is about one seventy. That label comes straight from this integral."]},

 {'t': 'v', 'h': 'Trig substitution: proving the area of a circle', 'img': 'fig:circle',
  'pts': ['√(r² − x²) → let x = r sin θ', 'Then √(r² − r²sin²θ) = r cos θ', 'Area = 2r²∫cos²θ dθ = πr²'],
  'say': ["When you see a square root like root of r squared minus x squared, substitute x equals r sine theta. Here's a beautiful use: proving the area of a circle.",
          "Slice the circle into thin vertical strips. A strip at position x has height two times root r squared minus x squared. With x equals r sine theta, that square root becomes r cosine theta, because one minus sine squared is cosine squared.",
          "The integral turns into two r squared times the integral of cosine squared, and using the half angle identity from the last slide, it comes out to exactly pi r squared. The formula you memorized in grade school, proved with calculus."]},

 {'t': 'ex', 'h': 'Partial fractions: break a fraction into simple pieces',
  'code': "∫ 1 / ((x+1)(x+2)) dx\n\n1/((x+1)(x+2)) = A/(x+1) + B/(x+2)\n1 = A(x+2) + B(x+1)\nx = −1:  1 = A       x = −2:  1 = −B\n\n= ∫ [ 1/(x+1) − 1/(x+2) ] dx\n= ln|x+1| − ln|x+2| + C",
  'pts': ['Factor the bottom, split into simple fractions', 'Plug in the roots to find A and B instantly', 'Used constantly in circuits & signals (inverse Laplace transforms)'],
  'say': "For rational functions, one polynomial over another, we use partial fractions. Take one over x plus one times x plus two. Write it as A over x plus one, plus B over x plus two. Multiply through by the denominator: one equals A times x plus two, plus B times x plus one. Now a shortcut: plug in x equals negative one, and the B term vanishes, leaving one equals A. Plug in x equals negative two, and you get one equals negative B. So the integral splits into one over x plus one, minus one over x plus two, and each piece integrates to a natural log. Remember this one, because in signals and systems, the response of almost every circuit comes out as a fraction like this, and partial fractions is how you turn it back into a time signal. Two cautions for exams. The plug in shortcut works when the bottom splits into different linear factors and the top has a lower degree. If the top's degree is as big as the bottom's, do long division first. And a repeated factor, like x plus one squared, needs one term for each power: A over x plus one, plus B over x plus one squared."},

 {'t': 'v', 'h': 'Improper integrals: area out to infinity', 'img': 'fig:improper',
  'pts': ['Replace ∞ with b, then take the limit', '∫ 1/x² from 1 to ∞ = 1 (finite!)', '∫ 1/x from 1 to ∞ = ∞ (diverges)', 'Key in probability and Laplace transforms'],
  'say': ["Can an infinitely long region have a finite area? Surprisingly, yes. An improper integral has an infinite limit. To handle it, replace infinity with a variable b, integrate, then let b go to infinity.",
          "For one over x squared from one to infinity, the antiderivative is negative one over x. From one to b, that's one minus one over b. As b goes to infinity, that heads to one. Finite area!",
          "But one over x, which looks almost the same, has antiderivative ln x, which grows forever. Its area is infinite. The difference is how fast the curve drops.",
          "You'll use improper integrals all the time. In probability, the total area under a probability curve, over the whole number line, must equal one. And the Laplace transform, the main tool of signals and systems, is an integral from zero to infinity."]},

 {'t': 'v', 'h': 'When there is no formula: numerical integration', 'img': 'fig:simpson',
  'pts': ['Some integrals have no elementary antiderivative', 'Trapezoid rule: connect the dots with lines', "Simpson's rule: fit parabolas — far more accurate", 'This is what computers actually do'],
  'say': ["Here's a secret: many integrals have no formula at all. The integral of e to the minus x squared, which is the bell curve you'll meet in probability, can't be written with ordinary functions.",
          "So we compute it numerically. The trapezoid rule splits the area into slices and connects the tops with straight lines. With just four slices, we get point seven four two nine eight.",
          "Simpson's rule fits little parabolas instead of straight lines. With the same four slices, it gets point seven four six eight six. The true value is point seven four six eight two, so Simpson is already correct to four decimal places.",
          "This is how engineering software, from circuit simulators to MATLAB, really computes integrals. Not with clever antiderivatives, but with smart sums."]},

 {'t': 'section', 'kicker': 'Part 2', 'h': 'Applications', 'sub': 'Volume, work and energy',
  'say': "Part two. Applications. Integrals add up tiny pieces, so whenever a quantity is made of pieces that vary, you integrate."},

 {'t': 'v', 'h': 'Volumes of revolution: the disk method', 'img': 'fig:disk',
  'pts': ['Spin a curve around an axis → a solid', 'Slice into disks: area π·r(x)²', 'V = π∫ r(x)² dx', 'y = √x from 0 to 4: V = π∫x dx = 8π ≈ 25.1'],
  'say': ["Spin a curve around an axis and you sweep out a solid, like a vase on a pottery wheel. Many real parts are made this way, on a lathe.",
          "To find the volume, slice the solid into thin disks. A disk at position x has radius equal to the height of the curve, so its face has area pi times r squared.",
          "Add up all the disks: the volume is pi times the integral of r of x squared, d x.",
          "Example: spin y equals root x from zero to four. The radius squared is just x, so the volume is pi times the integral of x from zero to four, which is pi times eight, about twenty five point one cubic units. Tank designers, engine designers and anyone shaping parts on a lathe use exactly this."]},

 {'t': 'v', 'h': 'Work and energy: springs and capacitors', 'img': 'fig:spring',
  'pts': ['Work = ∫ F dx (force can change along the way)', 'Spring: F = kx → W = ½kx²', 'k = 200 N/m, stretch 10 cm → W = 1 J', 'Same math: capacitor energy = ½CV²'],
  'say': ["Work is force times distance, but only when the force is constant. When the force changes, you integrate: work equals the integral of F d x.",
          "A spring pushes back harder the more you stretch it: F equals k x. Integrate from zero to x and you get one half k x squared. Geometrically, it's the area of the triangle under the force line.",
          "Example: a spring with k equals two hundred newtons per meter, stretched ten centimeters. The work is one half times two hundred times point one squared, which is one joule.",
          "And here's the connection to electronics. Charging a capacitor is the same math. The voltage grows in proportion to the charge, so the energy stored is one half C V squared. Same integral, same triangle, different physics. Once you see these patterns, a lot of engineering becomes the same few ideas reused."]},

 {'t': 'section', 'kicker': 'Part 3', 'h': 'Sequences and series', 'sub': 'Adding up infinitely many numbers',
  'say': "Part three. Infinite series. Can you add up infinitely many numbers and get a finite answer?"},

 {'t': 'v', 'h': 'Infinite sums can be finite', 'img': ['fig:zeno', 'a:bouncing_ball'],
  'pts': ['1/2 + 1/4 + 1/8 + … = 1', 'Geometric series: a + ar + ar² + … = a / (1 − r) if |r| < 1', 'Ball dropped 10 m, bounces to 60%: total distance = 10 + 2·(6/0.4) = 40 m'],
  'say': ["Look at this square. Shade half of it. Then half of what's left, a quarter. Then an eighth, a sixteenth, and so on forever. You never run out of square, and you never go past it either. So one half plus one quarter plus one eighth, forever, equals exactly one.",
          "That's a geometric series, where each term is the previous one times a fixed ratio r. If the ratio is between negative one and one, the sum is the first term divided by one minus r. Here that's one half over one minus one half, which is one. Notice how much easier the formula is than adding forever.",
          "Real example. Drop a ball from ten meters, and each bounce reaches sixty percent of the previous height. The total distance is the first ten meters down, plus twice each bounce height, up and down. The bounces form a geometric series: six, three point six, two point one six, and so on, summing to six over point four, which is fifteen. So the total is ten plus two times fifteen: forty meters, even though the ball bounces infinitely many times."]},

 {'t': 'v', 'h': 'But some sums blow up — testing convergence', 'img': ['fig:harmonic', 'fig:tests'],
  'pts': ['Terms shrinking to 0 is NOT enough', 'Harmonic series 1 + 1/2 + 1/3 + … diverges', 'Use convergence tests'],
  'say': ["Here's the trap. The harmonic series, one plus one half plus one third plus one fourth and so on, has terms that shrink to zero. Yet the sum grows forever. Slowly, like the natural log of n: a hundred terms gives about five point two, a thousand terms gives about seven point five, but it never stops growing. Meanwhile, one plus a quarter plus a ninth, the sum of one over n squared, settles down to pi squared over six. A famous and surprising result.",
          "So how do you know whether a series converges? We use tests. If the terms don't go to zero, it diverges, period. Geometric series converge when the ratio is less than one. P series, one over n to the p, converge when p is greater than one. The ratio test compares each term to the one before, so for n over two to the n the ratio heads to one half, and it converges. Comparison tests bound your series by one you already know. And alternating series, with signs flipping and terms shrinking, converge too. For example, one minus a half plus a third minus a quarter equals the natural log of two."]},

 {'t': 'v', 'h': 'Power series: a polynomial that never ends', 'img': 'fig:geom',
  'pts': ['1/(1 − x) = 1 + x + x² + x³ + …', 'Works only inside the radius of convergence (|x| < 1)', 'More terms → better match, but only inside that interval'],
  'say': ["Now the big idea. What if the terms of a series contain x? Then the series is a function. Take the geometric series one plus x plus x squared plus x cubed and so on. By our formula, that equals one over one minus x.",
          "But only when x is between negative one and one. That interval is called the interval of convergence, and half its width is the radius of convergence.",
          "Look at the graph. Inside the green band, adding more terms makes the polynomial hug the true curve, in black, more and more closely. Outside the band, the polynomials fly off. A power series is like an infinitely long polynomial, and polynomials are easy for computers, because they only need multiplication and addition."]},

 {'t': 'v', 'h': 'Taylor series: how your calculator computes sin x', 'img': ['fig:taylor0', 'fig:taylor1', 'fig:taylor2', 'fig:taylor3', 'fig:taylor4'],
  'say': ["Taylor series let you write almost any smooth function as a power series. The recipe: match the function's value, slope, curvature, and every higher derivative at one point. For sine around zero, start with just the first term, x. That's the tangent line, the small angle approximation. It's good near zero, but drifts away quickly.",
          "Add the next term, minus x cubed over three factorial. Now the curve bends back the right way and matches much farther out.",
          "Add plus x to the fifth over five factorial, and it hugs the sine wave across nearly a full hump.",
          "With the seventh degree term, it's accurate to the eye from about minus four to four. Let's test it numerically. Sine of point five: point five, minus point five cubed over six, plus point five to the fifth over one twenty. That gives point four seven nine four two seven. The true value is point four seven nine four two five five. Three terms, six correct digits.",
          "This is genuinely how computers do it. A math library first uses symmetry to shrink the angle into a small range, then evaluates a short polynomial like this one. Similar series give e to the x as one plus x plus x squared over two factorial plus x cubed over three factorial and so on, and cosine as one minus x squared over two factorial plus x to the fourth over four factorial."]},

 {'t': 'v', 'h': "Euler's formula: the bridge to electrical engineering", 'img': 'fig:euler',
  'pts': ['Put iθ into the series for eˣ', 'Real terms → cos θ, imaginary terms → sin θ', 'e^(iθ) = cos θ + i sin θ', 'A rotating arrow = a sine wave → phasors'],
  'say': ["Now something remarkable. Take the Taylor series for e to the x, and plug in an imaginary number, i theta, where i squared is negative one.",
          "The powers of i cycle: i, negative one, negative i, one. Sort the terms, and all the real ones form exactly the series for cosine theta, and all the imaginary ones form the series for sine theta.",
          "So e to the i theta equals cosine theta plus i sine theta. This is Euler's formula. Geometrically, e to the i theta is an arrow of length one, rotated by angle theta, on the complex plane.",
          "Let theta increase with time, and the arrow spins around the circle, while its shadow on the horizontal axis traces out a cosine wave. That's the key insight behind phasors in your circuits course, where every sine wave voltage becomes a rotating arrow, and calculus turns into algebra. We'll come back to this many times."]},

 {'t': 'v', 'h': 'Polar coordinates: describing shapes by angle', 'img': ['a:microphone', 'fig:cardioid'],
  'pts': ['Point = (distance r, angle θ) instead of (x, y)', 'x = r cos θ, y = r sin θ', 'Antenna and microphone patterns are polar plots'],
  'say': ["One more tool. Some shapes are easier to describe by angle and distance than by x and y. In polar coordinates, a point is given by its distance r from the origin and its angle theta. Converting is easy: x is r cosine theta, and y is r sine theta.",
          "Here's where engineers see it. Microphones like this one are described by a polar pickup pattern. This one is a cardioid, a heart shape, with r equals one half times one plus cosine theta. Sound from the front, at zero degrees, gets full sensitivity. Sound from the back, at one hundred eighty degrees, gets zero. That's why a singer's monitor speaker is placed behind the microphone. Antenna engineers describe radiation patterns exactly the same way."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Integrals **add up pieces** — volumes, work, energy. Series turn functions into **polynomials** computers can evaluate.',
  'cap': "Next: CPSC 120, Introduction to Programming. Later: Euler's formula returns in Circuits and in Signals & Systems.",
  'say': "Let's recap. Integration techniques, by parts, trig identities, substitution and partial fractions, let you handle most integrals, and numerical methods handle the rest. Integrals compute real quantities: area, volume, work and energy, including RMS voltage and capacitor energy. Infinite series can converge to finite values, and convergence tests tell you when. Taylor series turn functions into polynomials, which is how computers evaluate them. And Euler's formula links exponentials to sines and cosines, which will power your circuits and signals courses. Next, we switch gears completely and learn to program. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B

def draw_decay(ax, n, w, h):
    X0, Y0, sx, sy = 70, 80, 200, 520
    P = lambda x, y: (X0 + x * sx, Y0 + y * sy)
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 3.4 * sx, Y0 + 1.2 * sy, 't', 'y')
        xs = np.linspace(0, 3.2, 120); B.ln(ax, *zip(*[P(a, np.exp(-2 * a)) for a in xs]), c='blue', lw=3.5)
        B.lab(ax, *P(0.75, 0.75), r'$y = e^{-2t}$', 34, 'blue', ha='left')
        B.lab(ax, X0 - 20, P(0, 1)[1], '1', 28, 'gray', ha='right')
    if n >= 2:
        xs = np.linspace(0, 3.2, 80)
        B.poly(ax, [P(0, 0)] + [P(a, np.exp(-2 * a)) for a in xs] + [P(3.2, 0)], fc='#f6d6c4', c='orange', lw=1.5)
        B.lab(ax, *P(1.6, 0.3), 'area = 1/2', 34, 'red'); B.lab(ax, *P(2.9, -0.12), '→ ∞', 28, 'gray')

def draw_cone(ax, n, w, h):
    X0, Yc, Hh, R = 70, h * 0.5, w * 0.78, 230
    if n >= 1:
        B.arr(ax, X0 - 20, Yc, X0 + Hh + 70, Yc, 'gray', 2.5, 22); B.lab(ax, X0 + Hh + 60, Yc - 30, 'x', 30, 'gray')
        B.ln(ax, [X0, X0 + Hh], [Yc, Yc + R], c='blue', lw=3.5); B.ln(ax, [X0, X0 + Hh], [Yc, Yc - R], c='blue', lw=3.5)
        t = np.linspace(0, 2 * np.pi, 100); B.ln(ax, X0 + Hh + 45 * np.cos(t), Yc + R * np.sin(t), c='blue', lw=3)
        B.lab(ax, X0 + Hh * 0.45, Yc + R * 0.45 + 40, 'y = (R/H) x', 30, 'blue', rotation=np.degrees(np.arctan(R / Hh)) * 0.9)
        B.lab(ax, X0 + Hh + 75, Yc + R / 2, 'R', 34, 'red'); B.lab(ax, X0 + Hh / 2, Yc - R - 40, 'H', 34, 'red')
        B.arr(ax, X0, Yc - R - 15, X0 + Hh, Yc - R - 15, 'red', 2, 18, '<|-|>')
    if n >= 2:
        xd = X0 + Hh * 0.6; rd = R * 0.6; t = np.linspace(0, 2 * np.pi, 100)
        B.poly(ax, list(zip(xd + 26 * np.cos(t), Yc + rd * np.sin(t))), fc='#f6d6c4', c='orange', lw=3)
        B.lab(ax, X0 + Hh * 0.42, Yc - R * 0.78, 'disk: radius (R/H)x,  thickness dx', 26, 'orange')

B.insert(LESSON, 'Integration by parts', {'t': 'wb', 'h': 'Worked example: parts with a logarithm', 'steps': [
    {'say': "Let's do one where the choice of u really matters: the integral of x times the natural log of x. LIATE says logs come first, so u is ln x. That means d v is x d x.",
     'w': [r'$\int x\,\ln x\;dx$', {'m': r'LIATE: log first, so  $u = \ln x$,   $dv = x\,dx$', 'at': 1}, {'at': 2, 'm': r'$du = \frac{1}{x}\,dx$,     $v = \frac{x^2}{2}$', 'gap': 6}]},
    {'say': "Now apply the formula: u v minus the integral of v d u. That's x squared over two times ln x, minus the integral of x squared over two times one over x. Look what happened: the log is gone, and x squared over x is just x.",
     'w': [r'$= \frac{x^2}{2}\ln x - \int \frac{x^2}{2}\cdot\frac{1}{x}\,dx$', {'m': r'$= \frac{x^2}{2}\ln x - \int \frac{x}{2}\,dx$', 'at': 2}]},
    {'say': "The last integral is easy: x squared over four. So the answer is x squared over two ln x, minus x squared over four, plus C. As a numerical check, from one to e it comes out to e squared plus one, over four, about two point one. If we'd picked u equals x instead, we'd have needed the integral of ln x, which is harder. The right choice of u makes the problem collapse.",
     'w': [{'m': r'$= \frac{x^2}{2}\ln x - \frac{x^2}{4} + C$', 'c': 'red', 'box': True, 'at': 1}, {'m': r'from 1 to e:  $\left(\frac{e^2}{2}-\frac{e^2}{4}\right) - \left(0-\frac{1}{4}\right) = \frac{e^2+1}{4} \approx 2.097$', 'at': 2, 'gap': 10, 'fs': 38}]},
]})

B.insert(LESSON, 'Improper integrals', {'t': 'wb', 'h': 'Worked example: a decaying signal has finite area', 'draw': 'decay', 'split': 0.54, 'steps': [
    {'say': "Here's an improper integral you'll meet again in signals and systems: the integral of e to the minus two t, from zero to infinity. This curve decays like a capacitor discharging, and we want the total area under it, all the way out.",
     'w': [r'$\int_0^{\infty} e^{-2t}\,dt$', {'d': 1, 'at': 1}]},
    {'say': "Step one: replace infinity with b and write a limit. Step two: the antiderivative of e to the minus two t is negative one half e to the minus two t. Evaluate from zero to b.",
     'w': [r'$= \lim_{b\to\infty}\int_0^{b} e^{-2t}\,dt$', {'m': r'$= \lim_{b\to\infty}\left[-\frac{1}{2}e^{-2t}\right]_0^{b}$', 'at': 1}, {'m': r'$= \lim_{b\to\infty}\left(-\frac{1}{2}e^{-2b} + \frac{1}{2}\right)$', 'at': 2}]},
    {'say': "Now let b go to infinity. E to the minus two b shrinks to zero, so the whole limit is one half. An infinitely long region, with an area of exactly one half. This exact calculation, with a general s in place of the two, is the Laplace transform of a constant.",
     'w': [r'$e^{-2b}\to 0$', {'m': r'$= \frac{1}{2}$', 'c': 'red', 'box': True, 'at': 1}, {'d': 2, 'at': 1}]},
]})

B.insert(LESSON, 'Volumes of revolution', {'t': 'wb', 'h': "Worked example: proving the cone's volume formula", 'draw': 'cone', 'split': 0.5, 'steps': [
    {'say': "Where does the cone formula, one third pi R squared H, come from? Let's derive it. Lay the cone on its side. Its edge is a straight line through the origin, rising to radius R at length H, so its equation is y equals R over H times x.",
     'w': [r'Cone: radius $R$, height $H$', {'d': 1, 'at': 2}, {'m': r'edge:  $y = \frac{R}{H}\,x$', 'at': 3}]},
    {'say': "Slice it into thin disks. A disk at position x has radius R over H times x, so its volume is pi times that radius squared, times d x. Add them up from zero to H.",
     'w': [{'d': 2}, {'m': r'$V = \int_0^H \pi\left(\frac{R}{H}x\right)^2 dx$', 'at': 2}]},
    {'say': "Pull the constants out: pi R squared over H squared, times the integral of x squared. That integral is x cubed over three, which at H is H cubed over three. Two powers of H cancel, and we're left with one third pi R squared H. The cone holds exactly one third of the cylinder around it.",
     'w': [r'$= \frac{\pi R^2}{H^2}\int_0^H x^2\,dx$', {'m': r'$= \frac{\pi R^2}{H^2}\cdot\frac{H^3}{3}$', 'at': 1}, {'m': r'$V = \frac{1}{3}\pi R^2 H$', 'c': 'red', 'box': True, 'at': 2}]},
]})

B.insert(LESSON, 'Infinite sums can be finite', {'t': 'wb', 'h': 'Worked example: a repeating decimal is a geometric series', 'steps': [
    {'say': "Here's a neat use of the geometric series formula. Write zero point two seven two seven repeating, forever, as a fraction. Split it into pieces: point two seven, plus point zero zero two seven, plus point zero zero zero zero two seven, and so on.",
     'w': [{'m': r'$0.272727\ldots = \;?$', 'at': 1}, {'m': r'$= 0.27 + 0.0027 + 0.000027 + \ldots$', 'at': 2}]},
    {'say': "Each piece is the previous one times one hundredth. So it's geometric, with first term a equals point two seven and ratio r equals point zero one. The ratio is less than one, so it converges.",
     'w': [{'m': r'$a = 0.27$,    $r = 0.01$', 'at': 1}, {'m': r'$|r| < 1$, so the sum converges', 'at': 2, 'c': 'gray'}]},
    {'say': "Use the formula, a over one minus r: point two seven over point nine nine, which is twenty seven over ninety nine, which reduces to three elevenths. Check it on a calculator: three divided by eleven is point two seven two seven, repeating. Every repeating decimal is a geometric series in disguise, which is why every repeating decimal is a fraction.",
     'w': [r'$S = \frac{a}{1-r} = \frac{0.27}{0.99} = \frac{27}{99}$', {'m': r'$= \frac{3}{11}$', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Taylor series', {'t': 'wb', 'h': 'Worked example: computing e by hand', 'steps': [
    {'say': "Let's use a Taylor series to compute the number e itself, the way a computer might. Every derivative of e to the x is e to the x, and at zero they all equal one. So the Taylor series around zero is one, plus x, plus x squared over two factorial, plus x cubed over three factorial, and so on.",
     'w': [r'$f(x)=e^x$:   $f(0)=f\,{}^{\prime}(0)=f\,{}^{\prime\prime}(0)=\ldots=1$', {'m': r'$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \ldots$', 'at': 2}]},
    {'say': "Set x equal to one. Then e is one, plus one, plus one half, plus one sixth, plus one twenty fourth, plus one over one hundred twenty, and so on.",
     'w': [r'$e = 1 + 1 + \frac{1}{2} + \frac{1}{6} + \frac{1}{24} + \frac{1}{120} + \ldots$']},
    {'say': "Add them up as decimals. One plus one is two. Plus point five is two point five. Plus point one six seven is two point six six seven. Plus point zero four two is two point seven zero eight. Plus point zero zero eight is two point seven one seven. The true value is two point seven one eight two eight. Six terms, already three correct decimals, and each new term adds about one more, because factorials grow so fast.",
     'w': [{'m': r'$= 2 \;\to\; 2.5 \;\to\; 2.667 \;\to\; 2.708 \;\to\; 2.717$', 'at': 1}, {'m': r'true:  $e = 2.71828\ldots$', 'c': 'red', 'box': True, 'at': 6}]},
]})

# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'Integration by parts'
B.spen(LESSON, S, 0, {'p': 'box', 'on': '∫ u dv = u·v − ∫ v du', 'c': 'blue', 'at': 1}, {'p': 'circle', 'on': 'u  = x', 'c': 'orange', 'at': 4},
       {'p': 'underline', 'on': 'dv = eˣ dx', 'c': 'green', 'at': 5}, {'p': 'underline', 'on': 'v  = eˣ', 'c': 'green', 'at': 5, 'dt': 1.5},
       {'p': 'underline', 'on': '= x·eˣ − ∫ eˣ dx', 'c': 'blue', 'at': 6}, {'p': 'box', 'on': '= x·eˣ − eˣ + C', 'c': 'red', 'at': 6, 'dt': 3.0},
       {'p': 'underline', 'on': 'Log, Inverse trig, Algebraic,', 'c': 'purple', 'at': 7})
S = 'Trig integrals'
B.spen(LESSON, S, 0, {'fig': [('underline', .15, .51, .13)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .79, .075, .19, .06)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .28, .245, .03, .05)], 'c': 'blue', 'at': 2, 'dt': 1.5},
       {'fig': [('circle', .37, .545, .03, .05)], 'c': 'blue', 'at': 2, 'dt': 2.3})
S = 'Trig substitution'
B.spen(LESSON, S, 0, {'fig': [('underline', .195, .8, .115)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .51, .28, .57, .86)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .71, .92, .535)], 'c': 'orange', 'at': 1},
       {'fig': [('underline', .27, .73, .175)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .745, .07, .07, .05)], 'c': 'red', 'at': 0})
S = 'Partial fractions'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'A/(x+1) + B/(x+2)', 'c': 'blue', 'at': 2}, {'p': 'underline', 'on': '1 = A(x+2) + B(x+1)', 'c': 'blue', 'at': 3},
       {'p': 'circle', 'on': 'x = −1:  1 = A', 'c': 'orange', 'at': 4}, {'p': 'circle', 'on': 'x = −2:  1 = −B', 'c': 'orange', 'at': 5},
       {'p': 'box', 'on': '= ∫ [ 1/(x+1) − 1/(x+2) ] dx', 'c': 'green', 'at': 6}, {'p': 'underline', 'on': '= ln|x+1| − ln|x+2| + C', 'c': 'red', 'at': 6, 'dt': 3.0})
S = 'Improper integrals'
B.spen(LESSON, S, 0, {'fig': [('box', .25, .02, .79, .14)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .77, .07, .03, .06)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .6, .28, .13, .045)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('circle', .7, .2, .22, .045)], 'c': 'red', 'at': 1}, {'fig': [('arrow', .52, .58, .46, .7)], 'c': 'red', 'at': 2})
S = 'When there is no formula'
B.spen(LESSON, S, 0, {'fig': [('circle', .105, .075, .08, .06)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, y, .02, .035)], 'c': 'orange', 'at': 1, 'dt': t} for x, y, t in ((.33, .27, 1.0), (.49, .375, 1.6), (.66, .51, 2.2))],
       {'fig': [('highlight', .17, .665, .54, .712)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('highlight', .17, .715, .54, .757)], 'c': 'green', 'at': 1}, {'fig': [('highlight', .17, .762, .54, .802)], 'c': 'blue', 'at': 2},
       {'fig': [('check', .57, .79)], 'c': 'green', 'at': 2, 'dt': 2.0})
S = 'Volumes of revolution'
B.spen(LESSON, S, 1, {'fig': [('circle', .6, .55, .07, .15)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .045, .565, .12)], 'c': 'orange', 'at': 1, 'dt': 2.5})
B.spen(LESSON, S, 2, {'fig': [('underline', .6, .955, .12)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .93, .08, .035, .05)], 'c': 'red', 'at': 1})
S = 'Work and energy'
B.spen(LESSON, S, 0, {'fig': [('underline', .37, .95, .085)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('arrow', .14, .835, .895, .17)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .48, .52, .83, .68)], 'c': 'blue', 'at': 1})
S = 'Infinite sums can be finite'
B.spen(LESSON, S, 0, {'fig': [('circle', .384, .52, .06, .1)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .617, .715, .05, .1)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .56, .32, .04, .08)], 'c': 'green', 'at': 3}, {'fig': [('circle', .675, .42, .04, .06)], 'c': 'purple', 'at': 3, 'dt': 1.0},
       {'fig': [('underline', .82, .97, .1)], 'c': 'red', 'at': 5})
S = 'But some sums blow up'
B.spen(LESSON, S, 0, {'fig': [('underline', .27, .78, .145)], 'c': 'red', 'at': 1}, {'fig': [('box', .57, .48, .87, .645)], 'c': 'red', 'at': 3},
       {'fig': [('underline', .27, .88, .222)], 'c': 'blue', 'at': 4}, {'fig': [('underline', .17, .97, .71)], 'c': 'blue', 'at': 4, 'dt': 2.0})
B.spen(LESSON, S, 1, *[{'fig': [('highlight', .01, y0, .99, y1)], 'c': 'orange', 'at': a, 'solo': True}
       for a, y0, y1 in ((2, .15, .28), (3, .28, .42), (4, .42, .55), (5, .56, .69), (6, .69, .83), (7, .83, .97))])
S = 'Power series'
B.spen(LESSON, S, 0, {'fig': [('circle', .275, .105, .06, .04)], 'c': 'blue', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('box', .27, .04, .8, .88)], 'c': 'green', 'at': 0}, {'fig': [('underline', .33, .74, .875)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .55, .58, .12, .07)], 'c': 'green', 'at': 1}, {'fig': [('circle', .21, .15, .05, .12)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .73, .2, .05, .15)], 'c': 'red', 'at': 2, 'dt': 1.0})
S = 'Taylor series'
B.spen(LESSON, S, 0, {'fig': [('circle', .44, .07, .025, .05)], 'c': 'orange', 'at': 2}, {'fig': [('circle', .528, .5, .06, .1)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .62, .22, .05, .1)], 'c': 'red', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('circle', .49, .065, .035, .06)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .555, .065, .03, .06)], 'c': 'purple', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .62, .065, .03, .06)], 'c': 'red', 'at': 0}, {'fig': [('underline', .267, .79, .96)], 'c': 'blue', 'at': 0, 'dt': 1.5})
S = "Euler's formula"
B.spen(LESSON, S, 1, {'fig': [('underline', .51, .63, .59)], 'c': 'green', 'at': 1, 'dt': 2.0}, {'fig': [('circle', .745, .4, .06, .04)], 'c': 'orange', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 2, {'fig': [('box', .22, .0, .78, .12)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .7, .27, .06, .06)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .53, .49, .03, .04)], 'c': 'purple', 'at': 2, 'dt': 1.5})
B.spen(LESSON, S, 3, {'fig': [('arrow', .78, .45, .65, .24)], 'c': 'purple', 'at': 0}, {'fig': [('underline', .47, .67, .555)], 'c': 'green', 'at': 0, 'dt': 2.0})
S = 'Polar coordinates'
B.spen(LESSON, S, 1, {'fig': [('underline', .07, .77, .125)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .42, .21, .03, .04)], 'c': 'green', 'at': 3},
       {'fig': [('box', .73, .17, .96, .25)], 'c': 'green', 'at': 3, 'dt': 0.5}, {'fig': [('circle', .42, .54, .03, .04)], 'c': 'red', 'at': 4},
       {'fig': [('box', .73, .77, .96, .86)], 'c': 'red', 'at': 4, 'dt': 0.5})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'When there is no formula: numerical integration', {'t': 'wb', 'h': 'Which technique? A checklist for any integral', 'fs': 38, 'steps': [
    {'say': "The question every Calculus two student asks: how do I know which technique to use? Here's the checklist I give my students. Go down it in order. One: is it a basic form you already know, like a power, e to the x, or sine? Then just integrate.",
     'w': [{'m': r'1. basic form?  $\int x^5\,dx$, $\int e^x dx$  $\to$  just integrate', 'at': 2}]},
    {'say': "Two: is an inside function sitting there with its own derivative beside it? Use u substitution. Three: is it a product of two different kinds of function, like x times e to the x? Use integration by parts, with LIATE to pick u.",
     'w': [{'m': r'2. inside + its derivative?  $\int 2x\cos(x^2)dx$  $\to$  u-sub', 'at': 0},
           {'m': r'3. product of two kinds?  $\int x e^x dx$  $\to$  by parts', 'at': 1}]},
    {'say': "Four: powers of sine and cosine? Use identities, like the half angle formula. Five: a square root of a squared minus x squared? Trig substitution. Six: one polynomial over another? Partial fractions.",
     'w': [{'m': r'4. powers of sin, cos?  →  identities', 'at': 0}, {'m': r'5. $\sqrt{a^2 - x^2}$ ?  $\to$  $x = a\sin\theta$', 'at': 1},
           {'m': r'6. polynomial / polynomial?  →  partial fractions', 'at': 2}]},
    {'say': "And seven: if nothing works, the integral may have no formula at all. Compute it numerically. With practice you'll spot the right tool in seconds, but this list never fails you on an exam.",
     'w': [{'m': '7. nothing works?  →  numerical (Simpson)', 'c': 'orange', 'at': 0}]},
]})

B.insert(LESSON, 'But some sums blow up', {'t': 'wb', 'h': 'Sequences vs series, and the ratio test', 'fs': 36, 'steps': [
    {'say': "First, two words students mix up. A sequence is a list of numbers: one half, one quarter, one eighth. A series is what you get when you add the list up. The sequence can go to zero while the series still diverges, like the harmonic series.",
     'w': [{'m': r'sequence:  $\frac{1}{2},\ \frac{1}{4},\ \frac{1}{8},\ \ldots$   (a list)', 'at': 1, 'c': 'blue'},
           {'m': r'series:  $\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\ldots$   (a sum)', 'at': 2, 'c': 'green'}]},
    {'say': "Now the ratio test, worked out. Take the sum of n over two to the n. Divide each term by the one before it: n plus one over two to the n plus one, times two to the n over n.",
     'w': [{'m': r'$\sum \frac{n}{2^n}$', 'at': 1}, {'m': r'$\frac{a_{n+1}}{a_n} = \frac{n+1}{2^{n+1}}\cdot\frac{2^n}{n} = \frac{n+1}{2n}$', 'at': 2}]},
    {'say': "As n grows, n plus one over two n heads to one half. The rule: if that limit is less than one, the series converges. More than one, it diverges.",
     'w': [{'m': r'$\to \frac{1}{2} < 1$   so it converges', 'c': 'green', 'box': True, 'at': 1}, {'m': r'$L < 1$ converges,   $L > 1$ diverges', 'at': 2}]},
    {'say': "And here's the trap. If the limit equals exactly one, the test tells you nothing. The harmonic series gives one, and diverges. One over n squared also gives one, and converges. When you get one, switch to another test, like the p series or comparison test.",
     'w': [{'m': r'$L = 1$ : the test is silent!', 'c': 'red', 'box': True, 'at': 1},
           {'m': r'$\sum\frac{1}{n}$ diverges,   $\sum\frac{1}{n^2}$ converges,   both give $L = 1$', 'at': 3}]},
]})

B.insert(LESSON, 'Taylor series: how your calculator computes sin x', {'t': 'wb', 'h': 'The Taylor formula: where the factorials come from', 'steps': [
    {'say': "Let's write the recipe as a formula, because it's on every exam. Around a point a, f of x equals f of a, plus f prime of a times x minus a, plus f double prime of a over two factorial, times x minus a squared, and so on. The n th term uses the n th derivative, divided by n factorial.",
     'w': [{'m': r"$f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \frac{f'''(a)}{3!}(x-a)^3 + \ldots$", 'fs': 36, 'at': 1},
           {'m': r'n-th term:  $\frac{f^{(n)}(a)}{n!}\,(x-a)^n$', 'c': 'blue', 'at': 3}]},
    {'say': "Why factorials? Differentiate x cubed three times: three x squared, then six x, then six, which is three factorial. Each power leaves a factorial behind when you differentiate it down to a constant. Dividing by n factorial cancels it, so every derivative of the polynomial matches the function exactly.",
     'w': [{'m': r'$x^3 \to 3x^2 \to 6x \to 6 = 3!$', 'at': 1}, {'m': 'divide by n! so the derivatives match', 'c': 'green', 'at': 3}]},
    {'say': "Now build sine around zero. Its derivatives repeat in a cycle: sine, cosine, minus sine, minus cosine. At zero, those are zero, one, zero, minus one. So only odd powers survive, with alternating signs, and that's exactly the series we just graphed.",
     'w': [{'m': r'$\sin,\ \cos,\ -\sin,\ -\cos,\ \ldots$  at 0:  $0,\ 1,\ 0,\ -1,\ \ldots$', 'at': 1},
           {'m': r'$\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \ldots$', 'c': 'red', 'box': True, 'at': 3}]},
]})

G = 'Which technique? A checklist for any integral'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'u-sub', 'c': 'blue', 'at': 0}, {'p': ('underline',), 'on': 'by parts', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'partial fractions', 'c': 'blue', 'at': 2})
G = 'Sequences vs series, and the ratio test'
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'$\to \frac{1}{2} < 1$', 'c': 'green', 'at': 0})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'both give', 'c': 'red', 'at': 3})
G = 'The Taylor formula: where the factorials come from'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'6 = 3!$', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': r'at 0:', 'c': 'blue', 'at': 1})
