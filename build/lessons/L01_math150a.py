import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

X = np.linspace

def fig_two_q(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, grid=False)
    x = X(0, 4, 300); f = lambda t: 0.25 * t ** 2 + 0.5
    for a in (a1, a2):
        a.plot(x, f(x), color=C['blue']); a.set_xlim(0, 4); a.set_ylim(0, 5); a.set_xticks([]); a.set_yticks([])
    x0 = 2.5; m = 0.5 * x0
    a1.plot(x, f(x0) + m * (x - x0), color=C['orange'], lw=2.6); soliddot(a1, x0, f(x0), C['orange'])
    a1.set_title('Derivative'); note(a1, 0.2, 4.3, 'how steep, right here?', C['orange'])
    xs = X(1, 3.5, 200); a2.fill_between(xs, 0, f(xs), color=C['lblue']); a2.set_title('Integral')
    note(a2, 0.2, 4.3, 'how much, in total?', C['blue'])
    fig.subplots_adjust(wspace=0.25)
    note(a2, 1.4, 0.6, 'area under the curve', C['blue'])
    save(fig, path)

def fig_history(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    txt(ax, 50, 30, 'Newton (1660s)  — motion, gravity, "fluxions"', 24, C['blue'], bold=True)
    txt(ax, 50, 20, 'Leibniz (1670s–1684)  — the notation we still use:', 24, C['orange'], bold=True)
    txt(ax, 50, 8, r'$\dfrac{dy}{dx}$          $\int f(x)\,dx$', 40, C['ink'])
    save(fig, path)

def fig_sinc(path, w, h):
    fig, ax = plot(w, h)
    x = X(-10, 10, 800); x = x[np.abs(x) > 1e-3]
    ax.plot(x, np.sin(x) / x, color=C['blue']); hole(ax, 0, 1)
    axes0(ax); ax.set_ylim(-0.4, 1.25); ax.set_title(r'$y = \sin(x)/x$ is undefined at 0 … but heads to 1')
    note(ax, 1.2, 1.05, 'limit = 1', C['orange'], 22)
    save(fig, path)

def fig_hole(path, w, h):
    fig, ax = plot(w, h)
    x = X(-1, 5, 300); ax.plot(x, x + 2, color=C['blue']); hole(ax, 2, 4)
    axes0(ax); ax.set_xlim(-1, 5); ax.set_ylim(-0.5, 7.5)
    ax.set_title(r'$f(x) = \dfrac{x^2-4}{x-2}$', pad=18)
    note(ax, 2.25, 3.0, 'hole at (2, 4):\nf(2) undefined,\nbut the limit is 4', C['orange'], 20)
    save(fig, path)

def fig_cont(path, w, h):
    fig, axs = plot(w, h, ncols=3, grid=False)
    x = X(-2, 2, 300)
    a = axs[0]; a.plot(x, 0.5 * x ** 2 + 1, color=C['blue']); hole(a, 1, 1.5); soliddot(a, 1, 3, C['red']); a.set_title('removable\n(hole)')
    a = axs[1]; xl, xr = x[x < 0.5], x[x >= 0.5]; a.plot(xl, xl * 0 + 1, color=C['blue']); a.plot(xr, xr * 0 + 3, color=C['blue'])
    soliddot(a, 0.5, 3); hole(a, 0.5, 1); a.set_title('jump'); a.set_ylim(0, 4)
    a = axs[2]; xl, xr = x[x < -0.05], x[x > 0.05]; a.plot(xl, 1 / xl, color=C['blue']); a.plot(xr, 1 / xr, color=C['blue']); a.set_ylim(-8, 8)
    a.axvline(0, color=C['gray'], ls='--', lw=1.5); a.set_title('infinite\n(asymptote)')
    for a in axs: a.set_xticks([]); a.set_yticks([])
    save(fig, path)

def fig_ivt(path, w, h):
    fig, ax = plot(w, h)
    f = lambda t: t ** 3 - t - 1; x = X(0, 2, 300)
    ax.plot(x, f(x), color=C['blue']); axes0(ax)
    lo, hi = 1.0, 2.0; steps = []
    for k in range(4):
        mid = (lo + hi) / 2; steps.append(f'{mid:.4g}')
        ax.plot([mid], [0], 'v', color=C['orange'], ms=12)
        if f(mid) > 0: hi = mid
        else: lo = mid
    note(ax, 0.05, -2.6, 'midpoints tried: ' + ' → '.join(steps), C['orange'], 18)
    soliddot(ax, 1, f(1), C['red']); soliddot(ax, 2, f(2), C['green'])
    note(ax, 0.05, 3.2, r'$f(1)=-1 < 0$,  $f(2)=5 > 0$' + '\n→ a root lies between 1 and 2', fs=19)
    ax.set_title(r'$f(x)=x^3-x-1$ : bisection homes in on 1.3247')
    ax.set_ylim(-3, 5.5)
    save(fig, path)

def _secant(path, w, h, k):
    fig, ax = plot(w, h)
    x = X(0, 5.5, 300); ax.plot(x, x ** 2, color=C['blue']); axes0(ax)
    x0 = 3; hs = [2, 1, 0.5, None]
    for i, hh in enumerate(hs[:k + 1]):
        last = i == k
        if hh is None:
            ax.plot(x, 9 + 6 * (x - 3), color=C['orange'], lw=3); note(ax, 0.2, 26, 'tangent: slope = 6', C['orange'], 22)
        else:
            m = ((x0 + hh) ** 2 - 9) / hh
            ax.plot(x, 9 + m * (x - 3), color=C['gray'] if not last else C['purple'], lw=2 if not last else 2.8, ls='-' if last else ':')
            soliddot(ax, x0 + hh, (x0 + hh) ** 2, C['purple'] if last else C['gray'], 9)
            if last: note(ax, 0.2, 26, f'h = {hh}:  slope = {m:g}', C['purple'], 22)
    soliddot(ax, 3, 9, C['orange'])
    ax.set_xlim(0, 5.5); ax.set_ylim(-2, 30); ax.set_title(r'slope of $x^2$ at $x=3$:   $\dfrac{(3+h)^2-9}{h} = 6+h \to 6$', pad=16)
    save(fig, path)
for _k in range(4):
    globals()[f'fig_secant{_k}'] = (lambda kk: (lambda p, w, h: _secant(p, w, h, kk)))(_k)

def fig_rules(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    rows = [('power', r'$x^n \to n\,x^{n-1}$', r'$x^5 \to 5x^4$'), ('constant ×', r'$c\,f \to c\,f\,\prime$', r'$7x^2 \to 14x$'),
            ('sum', r"$f+g \to f\,'+g\,'$", r'$x^3+x \to 3x^2+1$'), ('product', r"$fg \to f\,'g+fg\,'$", r'$x\sin x \to \sin x + x\cos x$'),
            ('quotient', r"$\dfrac{f}{g} \to \dfrac{f\,'g-fg\,'}{g^2}$", r'$\dfrac{1}{x} \to -\dfrac{1}{x^2}$'), ('chain', r"$f(g(x)) \to f\,'(g)\cdot g\,'$", r'$(3x+1)^4 \to 12(3x+1)^3$')]
    table(ax, 3, H - 2, ['rule', 'pattern', 'example'], rows, [18, 38, 38], 8.4, 28)
    save(fig, path)

def fig_chain(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    box(ax, 2, 18, 12, 12, 'x', fc=C['pale'], fs=30, bold=True)
    box(ax, 26, 16, 22, 16, r'$u = 3x^2$', fc=C['lblue'], fs=26)
    box(ax, 60, 16, 22, 16, r'$y = \sin u$', fc=C['lorange'], ec=C['orange'], fs=26)
    box(ax, 90, 18, 9, 12, 'y', fc=C['pale'], fs=30, bold=True)
    arrow(ax, (14, 24), (26, 24)); arrow(ax, (48, 24), (60, 24)); arrow(ax, (82, 24), (90, 24))
    txt(ax, 37, 38, r'$\dfrac{du}{dx} = 6x$', 26, C['blue']); txt(ax, 71, 38, r'$\dfrac{dy}{du} = \cos u$', 26, C['orange'])
    txt(ax, 50, 6, r'$\dfrac{dy}{dx} = \dfrac{dy}{du}\cdot\dfrac{du}{dx} = \cos(3x^2)\cdot 6x$', 28, C['ink'])
    save(fig, path)

def fig_sincos(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    x = X(0, 2 * np.pi, 400); a1.plot(x, np.sin(x), color=C['blue']); a2.plot(x, np.cos(x), color=C['orange'])
    for x0 in (0, np.pi / 2, np.pi):
        m = np.cos(x0); xs = X(x0 - 0.6, x0 + 0.6, 10)
        a1.plot(xs, np.sin(x0) + m * (xs - x0), color=C['orange'], lw=2.4); soliddot(a1, x0, np.sin(x0), C['orange'], 8)
        soliddot(a2, x0, m, C['orange'], 9)
    a1.set_ylabel('sin x'); a2.set_ylabel("slope = cos x"); a1.set_ylim(-1.4, 1.4); a2.set_ylim(-1.4, 1.4)
    a2.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]); a2.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    save(fig, path)

def fig_motion(path, w, h):
    fig, axs = plot(w, h, nrows=3, sharex=True)
    t = X(0, 4.08, 300)
    axs[0].plot(t, -4.9 * t ** 2 + 20 * t, color=C['blue']); axs[0].set_ylabel('height\n(m)')
    axs[1].plot(t, -9.8 * t + 20, color=C['orange']); axs[1].axhline(0, color=C['ink'], lw=1.2); axs[1].set_ylabel('velocity\n(m/s)')
    axs[2].plot(t, -9.8 + 0 * t, color=C['red']); axs[2].set_ylabel('accel.\n(m/s²)'); axs[2].set_ylim(-12, 2); axs[2].set_xlabel('time (s)')
    for a in axs: a.axvline(2.04, color=C['gray'], ls='--', lw=1.5)
    note(axs[0], 2.15, 8, 'peak: 20.4 m at t = 2.04 s', C['blue'], 17); note(axs[1], 2.15, 8, 'v = 0 at the top', C['orange'], 17)
    save(fig, path)

def fig_linapprox(path, w, h):
    fig, ax = plot(w, h)
    x = X(0, 9, 300); ax.plot(x, np.sqrt(x), color=C['blue'], label=r'$\sqrt{x}$')
    ax.plot(x, 2 + 0.25 * (x - 4), color=C['orange'], lw=2.6, label='tangent at x = 4')
    soliddot(ax, 4, 2, C['orange']); ax.legend(loc='lower right'); ax.set_xlim(0, 9); ax.set_ylim(0, 3.6)
    note(ax, 0.3, 3.0, r'$\sqrt{4.1} \approx 2 + \frac{1}{4}(0.1) = 2.025$' + '\n(true: 2.02485)', fs=21)
    save(fig, path)

def fig_ladder(path, w, h):
    fig, ax, H = canvas(w, h, need=82, exact=True)
    ax.add_patch(Rectangle((14, 10), 7, 68, fc='#D9DEE7', ec=C['gray'])); line(ax, [(14, 10), (96, 10)], C['ink'], 3)
    line(ax, [(21, 66), (63, 10)], C['orange'], 8)
    txt(ax, 47, 44, '10 ft', 30, C['orange'], bold=True)
    line(ax, [(21, 5), (63, 5)], C['blue'], 2.5); txt(ax, 42, 1.5, 'x = 6 ft', 26, C['blue'], bold=True)
    line(ax, [(9, 10), (9, 66)], C['purple'], 2.5); txt(ax, 7, 38, 'y = 8 ft', 26, C['purple'], ha='right', bold=True, rotation=90)
    arrow(ax, (66, 16), (88, 16), color=C['blue'], lw=4); txt(ax, 77, 21, '1 ft/s', 26, C['blue'], bold=True)
    arrow(ax, (25, 70), (25, 56), color=C['purple'], lw=4); txt(ax, 28, 70, '? ft/s', 26, C['purple'], ha='left', bold=True)
    save(fig, path)

def fig_box(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, grid=False, gridspec_kw={'width_ratios': [1, 1.3]})
    a1.set_aspect('equal'); a1.axis('off'); a1.set_xlim(-1, 13); a1.set_ylim(-1, 13)
    a1.add_patch(Rectangle((0, 0), 12, 12, fc=C['lblue'], ec=C['blue'], lw=2.5))
    for cx, cy in ((0, 0), (10, 0), (0, 10), (10, 10)): a1.add_patch(Rectangle((cx, cy), 2, 2, fc='white', ec=C['red'], lw=2, ls='--'))
    a1.text(1, 1, 'x', ha='center', va='center', fontsize=20, color=C['red']); a1.text(6, 6, '12 − 2x', ha='center', va='center', fontsize=22)
    a1.set_title('12 in × 12 in sheet:\ncut corners, fold up')
    x = X(0, 6, 300); V = x * (12 - 2 * x) ** 2
    a2.plot(x, V, color=C['blue']); a2.grid(True); soliddot(a2, 2, 128, C['orange'])
    a2.set_xlabel('corner cut x (in)'); a2.set_ylabel('volume (in³)'); a2.set_title(r"$V = x(12-2x)^2$,  $V\,'=0 \Rightarrow x=2$")
    note(a2, 2.3, 132, 'max: 128 in³', C['orange'], 20)
    fig.subplots_adjust(wspace=0.5)
    save(fig, path)

def fig_sketch(path, w, h):
    fig, ax = plot(w, h)
    x = X(-2.3, 2.3, 400); ax.plot(x, x ** 3 - 3 * x, color=C['blue']); axes0(ax)
    soliddot(ax, -1, 2, C['green']); soliddot(ax, 1, -2, C['red']); soliddot(ax, 0, 0, C['purple'])
    note(ax, -1.9, 2.5, "local max (−1, 2)\nf ' = 0, f '' < 0", C['green'], 18)
    note(ax, 1.1, -3.1, "local min (1, −2)\nf ' = 0, f '' > 0", C['red'], 18)
    note(ax, 0.15, 0.5, 'inflection: f \'\' = 0', C['purple'], 18)
    ax.set_title(r"$f = x^3-3x$,   $f\,'=3x^2-3$,   $f\,''=6x$"); ax.set_ylim(-4.5, 4.5)
    save(fig, path)

def fig_newton(path, w, h):
    fig, ax = plot(w, h)
    f = lambda t: t ** 2 - 2; x = X(0.8, 2.2, 300); ax.plot(x, f(x), color=C['blue']); axes0(ax)
    xn = 1.0; cols = [C['orange'], C['purple'], C['green']]
    for i in range(3):
        m = 2 * xn; nx = xn - f(xn) / m; xs = X(min(nx, xn) - 0.05, max(nx, xn) + 0.05, 10)
        ax.plot(xs, f(xn) + m * (xs - xn), color=cols[i], lw=2.4); soliddot(ax, xn, f(xn), cols[i], 8)
        ax.plot([nx, nx], [0, f(nx)], ':', color=cols[i]); xn = nx
    ax.set_xlim(0.8, 2.2); ax.set_ylim(-1.3, 2.9)
    note(ax, 0.85, 1.6, r'$x_{n+1} = x_n - \dfrac{f(x_n)}{f\,\prime(x_n)}$' + '\n1 → 1.5 → 1.41667 → 1.414216', fs=20)
    ax.set_title(r'Newton’s method for $\sqrt{2}$:  $f(x) = x^2 - 2$')
    save(fig, path)

def _riemann(path, w, h, n):
    fig, ax = plot(w, h)
    x = X(0, 2, 300); ax.plot(x, x ** 2, color=C['blue'], zorder=5)
    dx = 2 / n; xs = np.arange(1, n + 1) * dx; S = float(np.sum(xs ** 2) * dx)
    for xr in xs: ax.add_patch(Rectangle((xr - dx, 0), dx, xr ** 2, fc=C['lorange'], ec=C['orange'], lw=1.5, zorder=2))
    ax.set_xlim(0, 2.05); ax.set_ylim(0, 4.3); axes0(ax)
    ax.set_title(f'{n} rectangles:  total area = {S:.4f}', color=C['orange'])
    note(ax, 0.1, 3.5, r'exact $\int_0^2 x^2\,dx = 8/3 \approx 2.6667$', C['blue'], 21)
    save(fig, path)
for _n in (4, 8, 32):
    globals()[f'fig_riemann{_n}'] = (lambda nn: (lambda p, w, h: _riemann(p, w, h, nn)))(_n)

def fig_battery(path, w, h):
    fig, ax = plot(w, h)
    t = [0, 0.5, 0.5, 1.0]; i = [2, 2, 1, 1]
    ax.fill_between([0, 0.5], 0, 2, color=C['lblue']); ax.fill_between([0.5, 1.0], 0, 1, color=C['lgreen'])
    ax.plot(t, i, color=C['blue'], lw=3.5); ax.set_xlim(0, 1.1); ax.set_ylim(0, 2.6)
    ax.set_xlabel('time (hours)'); ax.set_ylabel('current (A)')
    ax.text(0.25, 1.0, '2 A × 0.5 h\n= 1.0 Ah', ha='center', fontsize=21); ax.text(0.75, 0.5, '1 A × 0.5 h\n= 0.5 Ah', ha='center', fontsize=21)
    ax.set_title(r'charge used $= \int i\,dt =$ 1.5 Ah = 1500 mAh')
    save(fig, path)

def fig_ftc(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 10, 300); v = 3 * t; ax.plot(t, v, color=C['blue'])
    ax.fill_between(t[t <= 6], 0, 3 * t[t <= 6], color=C['lblue'])
    ax.set_xlabel('time (s)'); ax.set_ylabel('speed (m/s)'); ax.set_xlim(0, 10); ax.set_ylim(0, 32)
    note(ax, 5.2, 4.0, r'$v(t)=3t$' + '\n' + r'distance $=\int_0^6 3t\,dt$' + '\n' + r'$= [1.5\,t^2]_0^6 = 54$ m', fs=21)
    ax.text(3.2, 4.5, 'area =\ndistance', ha='center', fontsize=20, color=C['blue'])
    save(fig, path)

LESSON = {
 'code': 'MATH 150A', 'title': 'Calculus I', 'tag': 'Year 1 · Foundations', 'folder': 'MATH-150A Calculus I',
 'slides': [
 {'t': 'title', 'h': 'Calculus I', 'sub': 'Limits, derivatives and integrals — the mathematics of change', 'img': 'a:coaster',
  'say': "Welcome to Calculus one. Calculus is the mathematics of change: how fast something is changing right now, and how much it adds up to over time. Every engineering course you'll take later leans on it. Circuits, signals, physics, even machine learning. So in this lecture we'll build it from scratch: limits, then derivatives, then integrals, with lots of examples and pictures. If you've forgotten all of it, that's fine. Start here."},

 {'t': 'v', 'h': 'Why engineers need calculus', 'img': ['a:dashboard_digital', 'a:odometer', 'fig:two_q'],
  'pts': ['Speedometer: **rate** of change of position', 'Odometer: speed **added up** over time', 'Derivative ↔ integral: two sides of one idea'],
  'say': ["Look at a car dashboard. The speedometer tells you how fast your position is changing right now, in miles per hour. That's a rate of change, and in calculus it's called a derivative.",
          "The odometer does the opposite job. It adds up your speed over every moment of the trip to get the total distance. That running total is called an integral.",
          "So calculus asks two big questions. On the left: how steep is a curve at one exact point? That's the derivative, the slope of the tangent line. On the right: how much area is under a curve? That's the integral. The amazing discovery, which we'll reach at the end of this lecture, is that these two questions are inverses of each other. In engineering you'll see this everywhere. Current is the rate of change of charge. The current through a capacitor is proportional to how fast its voltage changes. Energy is power added up over time."]},

 {'t': 'v', 'h': 'Who invented it?', 'img': ['a:newton+leibniz', 'fig:history'],
  'say': ["Calculus was invented twice, independently, in the late sixteen hundreds. Isaac Newton in England developed it to explain motion and gravity. Gottfried Leibniz in Germany developed it on his own a few years later, and published first.",
          "The two men argued bitterly about who deserved credit. But Leibniz's notation won, and we still use it today. d y over d x for the derivative, and the tall S shaped integral sign, which is a stretched letter S for sum. Keep that in mind: an integral is a sum of infinitely many tiny pieces."]},

 {'t': 'section', 'kicker': 'Part 1', 'h': 'Limits', 'sub': 'What value is a function heading toward?',
  'say': "Part one. Limits. Everything in calculus is built on this one idea."},

 {'t': 'v', 'h': 'A limit is where a function is heading', 'img': 'fig:sinc',
  'pts': ['sin(x)/x is undefined at x = 0 (zero over zero)', 'x = 0.1 → 0.99833 · x = 0.01 → 0.99998', 'Written: lim x→0 of sin(x)/x = 1'],
  'say': ["Here's the function sine of x divided by x. Try to plug in zero, and you get zero divided by zero, which is undefined. There's literally a hole in the graph at zero.",
          "But watch what happens as x gets close to zero. At x equals point one, the value is point nine nine eight three. At point zero one, it's point nine nine nine nine eight. The closer we get, the closer the output gets to one.",
          "So we say the limit as x approaches zero of sine x over x equals one. A limit doesn't care what happens exactly at the point. It asks where the function is heading as you get closer and closer. That's the key idea, because the derivative is going to be exactly this kind of zero over zero situation."]},

 {'t': 'v', 'h': 'Computing limits: fix the zero-over-zero', 'img': 'fig:hole',
  'pts': ['Plug in first. If you get a number, done', 'If you get 0/0: factor, cancel, try again', '(x² − 4)/(x − 2) = (x − 2)(x + 2)/(x − 2) = x + 2 → 4'],
  'say': ["How do you actually compute a limit? Step one: just plug the number in. If the function is well behaved there, you get a number, and that's the limit.",
          "If you get zero over zero, the function is hiding something. Usually a common factor in the top and bottom.",
          "Example: x squared minus four, over x minus two, as x goes to two. Plugging in gives zero over zero. But x squared minus four factors into x minus two times x plus two. Cancel the x minus two, and you're left with x plus two, which is four when x is two. So the limit is four. The graph is just the line y equals x plus two, with a single hole punched out at the point two comma four."]},

 {'t': 'v', 'h': 'Continuity: no holes, jumps, or blow-ups', 'img': ['fig:cont', 'fig:ivt'],
  'pts': ['Continuous at a: f(a) exists, the limit exists, and they match', 'Intermediate Value Theorem: a continuous function crossing from − to + must hit 0', 'Bisection: halve the interval again and again'],
  'say': ["A function is continuous at a point if you can draw through it without lifting your pen. Formally, three things must be true: f of a exists, the limit exists, and they're equal. These three pictures show the three ways that fails: a hole, where the point is missing or misplaced, a jump, and an infinite blow up called an asymptote.",
          "Continuous functions have a very useful property called the intermediate value theorem. Look at f of x equals x cubed minus x minus one. At x equals one it's negative one. At x equals two it's positive five. Since it's continuous, it must cross zero somewhere in between. There has to be a root.",
          "And that gives us an algorithm that computers actually use: bisection. Check the midpoint, one point five. It's positive, so the root is between one and one point five. Check one point two five, it's negative, so the root is between one point two five and one point five. Each step cuts the interval in half, and after about twenty steps you know the root, one point three two four seven, to six decimal places. That's math turning directly into code."]},

 {'t': 'section', 'kicker': 'Part 2', 'h': 'Derivatives', 'sub': 'The slope at a single point',
  'say': "Part two. Derivatives."},

 {'t': 'v', 'h': 'The derivative: zooming in until a curve looks straight', 'img': ['fig:secant0', 'fig:secant1', 'fig:secant2', 'fig:secant3'],
  'say': ["Here's the problem. Slope is rise over run, and that needs two points. But we want the slope of the curve y equals x squared at one point, x equals three. So we cheat: take a second point a distance h away, and draw the line through both. That's called a secant line. With h equals two, the second point is at five, twenty five, so the slope is twenty five minus nine, over two: eight.",
          "Move the second point closer. With h equals one, the slope is seven.",
          "With h equals one half, it's six and a half. Do the algebra in general: the slope is three plus h, all squared, minus nine, all over h. Expand, and you get six h plus h squared, over h, which is six plus h.",
          "Now let h shrink to zero. That's a limit! Six plus h heads to six. So the slope of the tangent line at x equals three is exactly six. That's the derivative: f prime of x is the limit, as h goes to zero, of f of x plus h minus f of x, over h. It's the instantaneous rate of change. Notice we needed limits, because plugging in h equals zero directly gives zero over zero."]},

 {'t': 'v', 'h': 'Shortcut rules (so you never use the limit by hand again)', 'img': 'fig:rules',
  'say': "Computing limits every time would be painful, so we derive rules once and reuse them. The power rule: the derivative of x to the n is n times x to the n minus one. So x to the fifth becomes five x to the fourth, and our x squared becomes two x, which is six at x equals three, matching what we found. Constants just come along for the ride. Derivatives of sums are sums of derivatives. Products need the product rule: derivative of the first times the second, plus the first times the derivative of the second. Quotients have the quotient rule: low d high minus high d low, over low squared. And the most important one, the chain rule, for functions inside functions. Let's look at that one more closely."},

 {'t': 'v', 'h': 'The chain rule: rates multiply', 'img': 'fig:chain',
  'pts': ['Function inside a function: y = sin(3x²)', 'Inner rate × outer rate', 'Gears: if A turns B 3× as fast, and B turns C 2× as fast, C turns 6× as fast as A'],
  'say': ["The chain rule handles composition, a function inside another function. Take y equals sine of three x squared. There's an inner function, u equals three x squared, and an outer function, y equals sine of u.",
          "Each stage has its own rate. The inner one changes at six x. The outer one changes at cosine of u. The chain rule says: multiply them. So d y d x equals cosine of three x squared, times six x.",
          "Think of gears. If gear A turns gear B three times as fast, and B turns C twice as fast, then C turns six times as fast as A. Rates multiply through the chain. You'll use this constantly, including in machine learning, where training a neural network is the chain rule applied millions of times. That algorithm is called backpropagation."]},

 {'t': 'v', 'h': 'Derivatives of the special functions', 'img': 'fig:sincos',
  'pts': ['(sin x)′ = cos x  ·  (cos x)′ = −sin x', '(eˣ)′ = eˣ — its own slope', '(ln x)′ = 1/x'],
  'say': ["Some derivatives you just memorize. Look at the sine wave on top. At zero it's climbing steeply, slope one. At pi over two it's flat at the peak, slope zero. At pi it's falling, slope negative one. Plot those slopes on the bottom and you trace out the cosine wave. So the derivative of sine is cosine.",
          "The derivative of cosine is negative sine. This pair is why sine waves are everywhere in electrical engineering: differentiate a sine wave and you get another sine wave of the same frequency, just shifted.",
          "The exponential function, e to the x, is the only function that's its own derivative. Its slope at every point equals its height. That's why it describes anything whose growth is proportional to its size, like populations, compound interest, and, with a negative sign, a capacitor discharging.",
          "And the natural log, ln x, has derivative one over x."]},

 {'t': 'section', 'kicker': 'Part 3', 'h': 'Using derivatives', 'sub': 'Motion, approximation, related rates, optimization',
  'say': "Part three. What can you do with derivatives? A lot."},

 {'t': 'v', 'h': 'Motion: position → velocity → acceleration', 'img': 'fig:motion',
  'pts': ['Throw a ball up at 20 m/s:  s(t) = −4.9t² + 20t', 'v(t) = s′(t) = −9.8t + 20', 'a(t) = v′(t) = −9.8 m/s² (gravity)', 'Top of flight: v = 0 → t = 2.04 s, height 20.4 m'],
  'say': ["Here's the classic example. Throw a ball straight up at twenty meters per second. Its height is s of t equals negative four point nine t squared plus twenty t.",
          "Velocity is the derivative of position. Using the power rule: negative nine point eight t plus twenty.",
          "Acceleration is the derivative of velocity: a constant negative nine point eight meters per second squared. That's gravity.",
          "Where is the ball highest? At the top it stops for an instant, so the velocity is zero. Solve negative nine point eight t plus twenty equals zero: t is about two point zero four seconds. Plug back in: the height is about twenty point four meters. Look at the three graphs lined up. The slope of each graph is the height of the next one down."]},

 {'t': 'v', 'h': 'Linear approximation: the tangent line as a shortcut', 'img': 'fig:linapprox',
  'pts': ['Near a point, a curve ≈ its tangent line', 'f(x) ≈ f(a) + f′(a)(x − a)', '√4.1 ≈ 2 + ¼(0.1) = 2.025 (true 2.02485)'],
  'say': ["Zoom in far enough on any smooth curve and it looks like a straight line, its tangent line. So near a point, we can replace a complicated function with a simple line.",
          "The formula: f of x is approximately f of a, plus f prime of a times x minus a.",
          "Example: estimate the square root of four point one without a calculator. We know the square root of four is two, and the derivative of root x is one over two root x, which is one quarter at x equals four. So root four point one is about two plus one quarter of point one, which is two point zero two five. The true value is two point zero two four eight five. Very close! Engineers use this idea constantly. In electronics, transistors are wildly nonlinear, but for small signals we replace them with their tangent line. That's called small signal analysis, and it's how amplifiers are designed."]},

 {'t': 'v', 'h': 'Related rates: the sliding ladder', 'img': 'fig:ladder', 'reveal': False,
  'pts': ['Always true: x² + y² = 100', 'Differentiate in time: 2x·x′ + 2y·y′ = 0', 'y′ = −x·x′ / y = −6·1 / 8', '**y′ = −0.75 ft/s** (top slides down)'],
  'say': "Related rates problems connect how fast different quantities change. A ten foot ladder leans against a wall, and the bottom slides away at one foot per second. How fast is the top sliding down when the bottom is six feet from the wall? First, write an equation that's always true: x squared plus y squared equals one hundred, by Pythagoras. Then differentiate both sides with respect to time, using the chain rule: two x times d x d t, plus two y times d y d t, equals zero. Why do d x d t and d y d t appear? Because x and y both change with time. y squared is a function of y, and y is a function of t, so the chain rule multiplies by d y d t. This step is called implicit differentiation. When x is six, y is eight. Plug in: d y d t equals negative x times d x d t over y, which is negative six over eight, or negative point seven five feet per second. The negative sign means the top is moving down. The recipe always works: relate the quantities, differentiate with respect to time, then plug in numbers last."},

 {'t': 'v', 'h': 'Optimization: find the best design', 'img': 'fig:box',
  'pts': ['Maximum or minimum → slope is zero', 'Box from a 12×12 sheet: V = x(12 − 2x)²', "V′ = (12 − 2x)(12 − 6x) = 0 → x = 2", 'Best box: 2 × 8 × 8 = 128 in³'],
  'say': ["Engineering is full of optimization: least material, lowest power, maximum range. Calculus finds the best design, because at a maximum or minimum, the curve is momentarily flat. The derivative is zero.",
          "Example: take a twelve by twelve inch sheet of cardboard, cut an x by x square from each corner, and fold up the sides into an open box. The base is twelve minus two x on each side, and the height is x. So the volume is x times twelve minus two x, squared.",
          "Take the derivative and factor it: twelve minus two x, times twelve minus six x. Set it to zero: x equals six, which gives a flat box with no volume, or x equals two.",
          "So cut two inch squares. The box is two by eight by eight, for a volume of one hundred twenty eight cubic inches. The graph confirms it: the volume peaks exactly where the slope is zero. One more habit: when x is limited to a range, here between zero and six, also check the two endpoints. Both give zero volume, so x equals two really is the best."]},

 {'t': 'v', 'h': 'Curve sketching: reading a function from its derivatives', 'img': 'fig:sketch',
  'pts': ["f ′ > 0: rising · f ′ < 0: falling", "f ′ = 0: possible max or min", "f ′′ > 0: cupped up (min) · f ′′ < 0: cupped down (max)", "f ′′ changes sign: inflection point"],
  'say': ["The derivative tells you the shape of a graph without plotting a single point. Where f prime is positive, the function is rising. Where it's negative, it's falling.",
          "Where f prime is zero, the graph is flat: a possible peak or valley. For f of x equals x cubed minus three x, f prime is three x squared minus three, which is zero at x equals plus and minus one. But careful: a zero slope doesn't guarantee a peak or a valley. x cubed is flat at zero and keeps rising straight through it. So we need one more test.",
          "The second derivative tells you which way the curve bends. Here f double prime is six x. At x equals negative one it's negative, so the curve is cupped downward: a local maximum, at height two. At x equals one it's positive, cupped upward: a local minimum, at negative two.",
          "And where the second derivative changes sign, at x equals zero, the curve switches its bend. That's called an inflection point."]},

 {'t': 'v', 'h': "Newton's method: how calculators find roots", 'img': 'fig:newton',
  'pts': ['Guess → follow the tangent line to zero → repeat', 'x(n+1) = x(n) − f(x(n)) / f′(x(n))', '√2: 1 → 1.5 → 1.41667 → 1.414216 (correct digits double each step)'],
  'say': ["How does a calculator compute the square root of two? Often with Newton's method, which uses tangent lines. Start with a guess, follow the tangent line down to where it hits zero, and use that as your next guess.",
          "The formula is: the next x equals the current x minus f of x over f prime of x.",
          "To find root two, solve x squared minus two equals zero. Start at one. The next guess is one minus negative one over two, which is one point five. Then one point four one six six seven. Then one point four one four two one six, which is already correct to six digits. Each step roughly doubles the number of correct digits. Bisection, from earlier, is slower but never fails. Newton's method is fast but needs a decent starting guess. Choosing between reliable and fast is a trade off you'll make again and again."]},

 {'t': 'section', 'kicker': 'Part 4', 'h': 'Integrals', 'sub': 'Adding up infinitely many tiny pieces',
  'say': "Part four. Integrals."},

 {'t': 'v', 'h': 'Area by rectangles: Riemann sums', 'img': ['fig:riemann4', 'fig:riemann8', 'fig:riemann32'],
  'pts': ['Approximate area with rectangles', 'More, thinner rectangles → better answer', 'Limit of infinitely many → the integral ∫'],
  'say': ["How do you find the area under the curve y equals x squared, from zero to two? There's no formula from geometry for that shape. So we approximate it with rectangles. Four rectangles, each half a unit wide, with each height taken from the curve at the rectangle's right edge, give a total area of three point seven five. That's too big, because the rectangles poke above the curve.",
          "Use eight thinner rectangles, and the total drops to about three point one nine. Closer.",
          "With thirty two rectangles, we get about two point seven nine. As the number of rectangles goes to infinity, the sum approaches the exact area, eight thirds, about two point six six seven. That limit is the definition of the definite integral. The integral sign really does mean sum: a sum of infinitely many infinitely thin rectangles."]},

 {'t': 'v', 'h': 'The Fundamental Theorem of Calculus', 'img': 'fig:ftc',
  'pts': ['Antiderivative F: a function whose derivative is f', '∫ from a to b of f(x) dx = F(b) − F(a)', '∫₀² x² dx = [x³/3]₀² = 8/3 exactly', 'Distance = ∫ speed dt'],
  'say': ["Adding up infinitely many rectangles sounds impossible to do by hand. Here's the miracle that makes it easy. First, an antiderivative of f is a function F whose derivative is f. Run the derivative backwards.",
          "The fundamental theorem of calculus says: the integral of f from a to b equals F of b minus F of a. Find an antiderivative, evaluate at the two ends, and subtract.",
          "Let's check our rectangle problem. An antiderivative of x squared is x cubed over three, because its derivative is x squared. Evaluate from zero to two: eight thirds minus zero. Exactly eight thirds, the number our rectangles were creeping toward.",
          "Here's what it means physically. If your speed is three t meters per second, the distance you travel in six seconds is the area under the speed graph. The antiderivative is three halves t squared. At six seconds that's fifty four meters. The speedometer and the odometer, the derivative and the integral, are two sides of the same coin. That's why it's called fundamental."]},

 {'t': 'ex', 'h': 'u-substitution: the chain rule in reverse', 'split': 0.58, 'img': 'fig:battery',
  'code': "∫ 2x·cos(x²) dx\n\nlet u = x²   →   du = 2x dx\n\n= ∫ cos(u) du\n= sin(u) + C\n= sin(x²) + C\n\ncheck: d/dx sin(x²) = cos(x²)·2x  ✓",
  'say': ["Not every integral is a simple power. A common trick is substitution, which is the chain rule run backwards. Look at the integral of two x times cosine of x squared. The inside function is x squared, and its derivative, two x, is sitting right there. So let u equal x squared. Then d u equals two x d x, and the whole integral becomes the integral of cosine u d u. That's sine u, plus a constant. Put x back in: sine of x squared, plus C. Always check by differentiating. The derivative of sine of x squared is cosine of x squared, times two x. It matches.",
          "And here's an everyday engineering integral. On the right is the current drawn from a phone battery: two amps for half an hour, then one amp for half an hour. The total charge used is the integral of current over time, which is just the area under this graph. Two times one half, plus one times one half: one point five amp hours, or fifteen hundred milliamp hours. That's exactly the unit printed on every battery you own."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Derivative = **rate** right now. Integral = **total** over time. The Fundamental Theorem says they undo each other.',
  'cap': 'Next: MATH 150B, Calculus II, where we learn many more integration techniques and infinite series.',
  'say': "Let's wrap up. A limit tells you where a function is heading. The derivative is the instantaneous rate of change, the slope of the tangent line, built from a limit. Derivatives find velocities, approximations, maximums and minimums. The integral adds up infinitely many tiny pieces to find areas and totals. And the fundamental theorem of calculus says derivatives and integrals undo each other. Every later course will use these tools, so if anything felt shaky, rewatch that section and work the examples yourself with pencil and paper. Next up, Calculus two. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B

def draw_root_limit(ax, n, w, h):
    X0, Y0, sx, sy = 70, 90, 120, 1500     # x in [-4, 1.2], y in [0, 0.4]
    P = lambda x, y: (X0 + (x + 4) * sx, Y0 + y * sy)
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 5.6 * sx, Y0 + 0.43 * sy, 'x', 'y')
        xs = np.linspace(-3.95, 1.1, 120); ys = 1 / (np.sqrt(xs + 4) + 2)
        B.ln(ax, *zip(*[P(a, b) for a, b in zip(xs, ys)]), c='blue', lw=3.5)
        B.ln(ax, [P(0, 0)[0]] * 2, [Y0, P(0, 0.25)[1]], c='gray', lw=1.5, ls='--')
        B.lab(ax, P(0, 0)[0], Y0 - 28, '0', 28, 'gray')
    if n >= 2:
        B.dot(ax, *P(0, 0.25), c='red', s=14, hollow=True)
        B.lab(ax, P(0, 0.25)[0] + 20, P(0, 0.25)[1] + 50, 'hole at (0, 1/4)', 30, 'red', ha='left')

def draw_tangent_recip(ax, n, w, h):
    X0, Y0, s = 80, 80, 150          # x in [0, 4], y in [0, 4]
    P = lambda x, y: (X0 + x * s, Y0 + y * s)
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 4.4 * s, Y0 + 4.4 * s)
        xs = np.linspace(0.26, 4.2, 150)
        B.ln(ax, *zip(*[P(a, 1 / a) for a in xs]), c='blue', lw=3.5)
        B.lab(ax, *P(0.55, 3.6), 'y = 1/x', 32, 'blue', ha='left')
    if n >= 2:
        xs = np.linspace(0.6, 3.6, 2)
        B.ln(ax, *zip(*[P(a, 1 - (a - 2) / 4) for a in xs]), c='red', lw=3)
        B.dot(ax, *P(2, 0.5), c='red', s=13)
        B.lab(ax, *P(2.1, 1.25), 'slope −1/4', 32, 'red', ha='left')

def draw_ripple(ax, n, w, h):
    cx, cy = w / 2, h / 2
    for k, r in enumerate((90, 170, 250)):
        if n >= 1:
            t = np.linspace(0, 2 * np.pi, 200)
            B.ln(ax, cx + r * np.cos(t), cy + r * np.sin(t), c='blue' if r == 250 else 'gray', lw=3 if r == 250 else 2)
    if n >= 1: B.dot(ax, cx, cy, s=10)
    if n >= 2:
        B.arr(ax, cx, cy, cx + 250, cy, c='red'); B.lab(ax, cx + 130, cy + 34, 'r = 5 cm', 30, 'red', bbox=dict(fc='white', ec='none', pad=1))
        B.arr(ax, cx + 255, cy - 40, cx + 330, cy - 40, c='orange', lw=3); B.lab(ax, cx + 300, cy - 80, 'dr/dt = 2', 28, 'orange')

def draw_fence(ax, n, w, h):
    if n >= 1:
        t = np.linspace(40, w - 40, 60)
        B.ln(ax, t, h * 0.78 + 12 * np.sin(t / 30), c='blue', lw=3); B.ln(ax, t, h * 0.82 + 12 * np.sin(t / 30 + 1), c='blue', lw=2)
        B.lab(ax, w / 2, h * 0.9, 'river (no fence needed)', 30, 'blue')
    if n >= 2:
        x0, x1, yb, yt = 150, w - 150, h * 0.25, h * 0.72
        B.ln(ax, [x0, x0, x1, x1], [yt, yb, yb, yt], c='ink', lw=4)
        B.lab(ax, x0 - 30, (yb + yt) / 2, 'x', 36, 'red'); B.lab(ax, x1 + 30, (yb + yt) / 2, 'x', 36, 'red')
        B.lab(ax, w / 2, yb - 40, '100 − 2x', 36, 'red')
    if n >= 3:
        B.lab(ax, w / 2, (h * 0.25 + h * 0.72) / 2, 'A = x(100 − 2x)', 34, 'green')

def draw_ftc_area(ax, n, w, h):
    X0, Y0, sx, sy = 70, 70, 280, 36      # x in [0, 2.3], y in [0, 18.5]
    P = lambda x, y: (X0 + x * sx, Y0 + y * sy)
    f = lambda x: 3 * x * x + 2 * x
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 2.4 * sx, Y0 + 18.5 * sy)
        xs = np.linspace(0, 2.12, 100); B.ln(ax, *zip(*[P(a, f(a)) for a in xs]), c='blue', lw=3.5)
        B.lab(ax, *P(0.9, 12), 'y = 3x² + 2x', 30, 'blue')
        for xv in (0, 2): B.lab(ax, P(xv, 0)[0], Y0 - 28, str(xv), 28, 'gray')
    if n >= 2:
        xs = np.linspace(0, 2, 60)
        B.poly(ax, [P(0, 0)] + [P(a, f(a)) for a in xs] + [P(2, 0)], fc='#f6d6c4', c='orange', lw=2)
        B.lab(ax, *P(1.45, 3.5), 'area = 12', 34, 'red')

B.insert(LESSON, 'Computing limits', {'t': 'wb', 'h': 'Worked example: a limit that needs a trick', 'draw': 'root_limit', 'split': 0.55, 'steps': [
    {'say': "Let's work one together, step by step. Find the limit as x goes to zero of the square root of x plus four, minus two, all over x. First, always try plugging in. The top is root four minus two, which is zero, and the bottom is zero. Zero over zero, so there's a hole hiding here.",
     'w': [r'$\lim_{x\to 0}\ \frac{\sqrt{x+4}\,-\,2}{x}$', {'m': 'plug in x = 0:  (2 − 2)/0 = 0/0', 'at': 2, 'c': 'gray'}, {'d': 1, 'at': 3}]},
    {'say': "Factoring won't work with a square root, so we use a different trick: multiply the top and bottom by the conjugate, root x plus four, plus two. On top, that's a difference of squares: x plus four, minus four, which is just x. So we get x over x times root x plus four plus two.",
     'w': [r'$= \frac{\sqrt{x+4}-2}{x}\cdot\frac{\sqrt{x+4}+2}{\sqrt{x+4}+2}$', {'m': r'$= \frac{(x+4)-4}{x\,(\sqrt{x+4}+2)}$', 'at': 1}, {'m': r'$= \frac{x}{x\,(\sqrt{x+4}+2)}$', 'at': 2}]},
    {'say': "Now the x on top cancels the x on the bottom. That leaves one over root x plus four, plus two. Plug in zero: one over two plus two, which is one quarter. On the graph, the curve heads smoothly toward one quarter, with a single missing point exactly at zero.",
     'w': [r'$= \frac{1}{\sqrt{x+4}+2}$', {'m': r'$\to \frac{1}{2+2} = \frac{1}{4}$', 'c': 'red', 'box': True, 'at': 1}, {'d': 2, 'at': 2}]},
]})

B.insert(LESSON, 'The derivative: zooming in', {'t': 'wb', 'h': 'Worked example: a derivative from the definition', 'draw': 'tangent_recip', 'split': 0.56, 'steps': [
    {'say': "Let's use the definition ourselves, on a new function: f of x equals one over x. Write the definition first: the limit as h goes to zero of f of x plus h, minus f of x, over h. Substitute our function: one over x plus h, minus one over x, all over h.",
     'w': [r'$f(x)=\frac{1}{x}$', r"$f'(x)=\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$", r'$=\lim_{h\to 0}\frac{\frac{1}{x+h}-\frac{1}{x}}{h}$', {'d': 1, 'at': 0}]},
    {'say': "Combine the two fractions on top over a common denominator, x times x plus h. The numerator becomes x minus x plus h, which is just negative h. So the whole thing is negative h over x times x plus h times h.",
     'w': [r'$=\lim_{h\to 0}\frac{x-(x+h)}{x\,(x+h)\,h}$', {'m': r'$=\lim_{h\to 0}\frac{-h}{x\,(x+h)\,h}$', 'at': 1}]},
    {'say': "The h's cancel, which is exactly what removes the zero over zero. Now let h go to zero: we get negative one over x squared. At x equals two, the slope is negative one quarter, and you can see that tangent line on the graph, gently sloping downward.",
     'w': [r'$=\lim_{h\to 0}\frac{-1}{x\,(x+h)}$', {'m': r"$f'(x) = -\frac{1}{x^2}$", 'c': 'red', 'box': True, 'at': 1}, {'m': r"$f'(2) = -\frac{1}{4}$", 'at': 2}, {'d': 2, 'at': 2}]},
]})

B.insert(LESSON, 'The chain rule', {'t': 'wb', 'h': 'Worked example: the chain rule', 'steps': [
    {'say': "Let's differentiate y equals three x squared plus one, all to the fifth power. Don't expand it! Instead, name the inside: u equals three x squared plus one. Then y is just u to the fifth.",
     'w': [r'$y = (3x^2+1)^5$', {'m': r'inside:  $u = 3x^2+1$,   outside:  $y = u^5$', 'at': 2}]},
    {'say': "Find each rate separately. The outer rate, d y d u, is five u to the fourth. The inner rate, d u d x, is six x.",
     'w': [r'$\frac{dy}{du} = 5u^4$', {'m': r'$\frac{du}{dx} = 6x$', 'at': 1}]},
    {'say': "The chain rule says multiply them. Five u to the fourth times six x. Now put u back in terms of x: thirty x times three x squared plus one, to the fourth.",
     'w': [r'$\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx} = 5u^4\cdot 6x$', {'m': r'$\frac{dy}{dx} = 30x\,(3x^2+1)^4$', 'c': 'red', 'box': True, 'at': 1}]},
    {'say': "Let's get a number. At x equals one, the inside is four, four to the fourth is two hundred fifty six, and thirty times two hundred fifty six is seven thousand six hundred eighty. Expanding the fifth power by hand would have taken a page. The chain rule took three lines.",
     'w': [{'m': r'at $x=1$:  $30\cdot 1\cdot 4^4 = 30\cdot 256 = 7680$', 'gap': 14}]},
]})

B.insert(LESSON, 'Related rates', {'t': 'wb', 'h': 'Worked example: a growing ripple', 'draw': 'ripple', 'split': 0.56, 'steps': [
    {'say': "Here's another related rates problem, worked from scratch. A stone drops into a pond and a circular ripple spreads out. The radius grows at two centimeters per second. How fast is the area growing when the radius is five centimeters?",
     'w': [{'d': 1}, 'Given:  dr/dt = 2 cm/s.   Find dA/dt when r = 5', {'d': 2, 'at': 3}]},
    {'say': "Step one: write an equation that's always true. The area of a circle is pi r squared. Step two: differentiate both sides with respect to time. Using the chain rule, d A d t equals two pi r, times d r d t.",
     'w': [r'$A = \pi r^2$', {'m': r'$\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}$', 'at': 1}]},
    {'say': "Step three, and only now, plug in the numbers: two pi times five times two. That's twenty pi, about sixty three square centimeters per second. Notice the area grows faster as the ripple gets bigger, even though the radius grows at a steady rate.",
     'w': [r'$= 2\pi\,(5)(2)$', {'m': r'$\frac{dA}{dt} = 20\pi \approx 62.8\ \mathrm{cm^2/s}$', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Optimization', {'t': 'wb', 'h': 'Worked example: the biggest pen by a river', 'draw': 'fence', 'split': 0.52, 'steps': [
    {'say': "Let's do a full optimization problem on the board. You have one hundred meters of fence to build a rectangular pen along a straight river. The river side needs no fence. What dimensions give the largest area?",
     'w': [{'d': 1}, '100 m of fence, river on one side.', 'Maximize the area.']},
    {'say': "Draw it. Call the two sides that touch the river x. The fence covers x, plus x, plus the far side, so the far side is one hundred minus two x. The area is x times one hundred minus two x.",
     'w': [{'d': 2}, {'m': r'$A(x) = x\,(100-2x) = 100x - 2x^2$', 'at': 2}, {'d': 3, 'at': 2}]},
    {'say': "At the maximum, the slope is zero. The derivative is one hundred minus four x. Set it equal to zero, and x equals twenty five.",
     'w': [r"$A'(x) = 100 - 4x$", {'m': r'$100 - 4x = 0 \;\Rightarrow\; x = 25$', 'at': 2}]},
    {'say': "So the sides are twenty five meters and the far side is fifty meters, for an area of twelve hundred fifty square meters. Check that it's a maximum: the second derivative is negative four, so the curve bends downward. It's a peak, not a valley.",
     'w': [{'m': r'$25 \times 50 = 1250\ \mathrm{m^2}$', 'c': 'red', 'box': True}, {'m': r"check: $A''(x) = -4 < 0$  so it's a maximum", 'at': 1}]},
]})

B.insert(LESSON, 'The Fundamental Theorem', {'t': 'wb', 'h': 'Worked example: an exact area in three lines', 'draw': 'ftc_area', 'split': 0.55, 'steps': [
    {'say': "Let's use the fundamental theorem on a fresh example. Find the area under y equals three x squared plus two x, from zero to two.",
     'w': [r'$\int_0^2 (3x^2 + 2x)\,dx$', {'d': 1, 'at': 0}]},
    {'say': "First, find an antiderivative, term by term, using the power rule backwards. Three x squared comes from x cubed, and two x comes from x squared. So F of x is x cubed plus x squared. Check it: the derivative is three x squared plus two x.",
     'w': [r'$F(x) = x^3 + x^2$', {'m': r"check: $F'(x) = 3x^2 + 2x$", 'c': 'gray', 'at': 3}]},
    {'say': "Now evaluate at the top and the bottom and subtract. At two: eight plus four, which is twelve. At zero: zero. So the area is exactly twelve. That shaded region would take thousands of rectangles to approximate, and we got it exactly in three lines.",
     'w': [r'$= F(2) - F(0) = (8 + 4) - 0$', {'m': r'$= 12$', 'c': 'red', 'box': True, 'at': 2}, {'d': 2, 'at': 2}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: a limit that needs a trick'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': '0/0', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'\cdot\frac{\sqrt{x+4}+2}', 'c': 'blue', 'at': 0}, {'p': ('strike',), 'on': r'$= \frac{x}{x\,(', 'at': 2})
G = 'Worked example: a derivative from the definition'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'\frac{-h}', 'at': 1})
G = 'Worked example: the chain rule'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'inside:', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'= 5u^4$', 'at': 0}, {'p': ('circle',), 'on': r'= 6x$', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': r'\cdot\frac{du}{dx} = 5u^4', 'at': 0})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '7680', 'at': 0})
G = 'Worked example: a growing ripple'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'= 2\pi r\,', 'at': 1})
G = 'Worked example: the biggest pen by a river'
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'x = 25', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': "so it's a maximum", 'c': 'green', 'at': 1})
G = 'Worked example: an exact area in three lines'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$F(x) = x^3 + x^2$', 'c': 'blue', 'at': 0}, {'p': ('check',), 'on': "check: $F'(x)", 'c': 'green', 'at': 3})

# ---------------- the pen on ordinary slides (figures; the bullet underlines are added automatically) ----------------
S = 'A limit is where'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .235, .03, .045)], 'c': 'red', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('arrow', .42, .5, .475, .28)], 'c': 'blue', 'at': 0}, {'fig': [('arrow', .58, .5, .525, .28)], 'c': 'blue', 'at': 0, 'dt': 0.8},
       {'fig': [('circle', .5, .235, .03, .045)], 'c': 'orange', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('underline', .54, .69, .245)], 'c': 'orange', 'at': 0})
S = 'Computing limits'
B.spen(LESSON, S, 2, {'fig': [('box', .36, .02, .66, .19)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .55, .84, .595)], 'c': 'orange', 'at': 4},
       {'fig': [('circle', .5, .487, .03, .045)], 'c': 'red', 'at': 5})
S = 'Continuity'
B.spen(LESSON, S, 0, {'fig': [('circle', .23, .74, .03, .045)], 'c': 'red', 'at': 2, 'dt': 2.5}, {'fig': [('circle', .23, .216, .03, .045)], 'c': 'red', 'at': 2, 'dt': 3.2},
       {'fig': [('circle', .52, .565, .05, .23)], 'c': 'blue', 'at': 2, 'dt': 5.0}, {'fig': [('circle', .807, .55, .05, .4)], 'c': 'purple', 'at': 2, 'dt': 7.0})
B.spen(LESSON, S, 1, {'fig': [('underline', .17, .53, .305)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .5, .7, .025, .035)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .837, .158, .025, .035)], 'c': 'green', 'at': 3}, {'fig': [('circle', .609, .608, .045, .06)], 'c': 'orange', 'at': 5})
B.spen(LESSON, S, 2, {'fig': [('circle', .668, .608, .022, .04)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .585, .608, .022, .04)], 'c': 'orange', 'at': 3},
       {'fig': [('underline', .17, .76, .885)], 'c': 'orange', 'at': 4})
S = 'The derivative: zooming'
B.spen(LESSON, S, 0, {'fig': [('circle', .56, .634, .025, .04)], 'c': 'orange', 'at': 2}, {'fig': [('circle', .895, .275, .025, .04)], 'c': 'purple', 'at': 3},
       {'fig': [('underline', .09, .29, .27)], 'c': 'purple', 'at': 5})
B.spen(LESSON, S, 1, {'fig': [('underline', .09, .29, .27)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .09, .29, .27)], 'c': 'purple', 'at': 0}, {'fig': [('box', .5, .02, .84, .17)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .815, .11, .03, .06)], 'c': 'orange', 'at': 2}, {'fig': [('underline', .09, .31, .27)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .56, .634, .025, .04)], 'c': 'orange', 'at': 3, 'dt': 1.2})
S = 'Shortcut rules'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .05, y0, .95, y1)], 'c': 'orange', 'at': a, 'solo': True}
       for a, y0, y1 in ((1, .157, .289), (3, .295, .43), (4, .437, .574), (5, .58, .716), (6, .723, .86), (7, .866, .98))])
S = 'The chain rule: rates'
B.spen(LESSON, S, 0, {'fig': [('box', .25, .26, .49, .64)], 'c': 'blue', 'at': 2}, {'fig': [('box', .59, .26, .83, .64)], 'c': 'orange', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .37, .14, .085, .14)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .71, .14, .105, .14)], 'c': 'orange', 'at': 2},
       {'fig': [('underline', .25, .75, .995)], 'c': 'red', 'at': 4})
S = 'Derivatives of the special'
B.spen(LESSON, S, 0, {'fig': [('circle', .249, .223, .03, .045)], 'c': 'red', 'at': 2}, {'fig': [('circle', .418, .086, .03, .045)], 'c': 'red', 'at': 3},
       {'fig': [('circle', .589, .223, .03, .045)], 'c': 'red', 'at': 4},
       *[{'fig': [('circle', x, y, .03, .045)], 'c': 'blue', 'at': 5, 'dt': t} for x, y, t in ((.249, .546, 0), (.418, .68, .7), (.589, .819, 1.4))])
S = 'Motion:'
B.spen(LESSON, S, 1, {'fig': [('box', .2, .3, .97, .555)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('box', .2, .58, .97, .83)], 'c': 'red', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .587, .425, .03, .045)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .587, .045, .03, .045)], 'c': 'blue', 'at': 3},
       {'fig': [('underline', .607, .95, .215)], 'c': 'blue', 'at': 3, 'dt': 1.2})
S = 'Linear approximation'
B.spen(LESSON, S, 0, {'fig': [('circle', .486, .403, .03, .045)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('underline', .13, .58, .13)], 'c': 'orange', 'at': 3}, {'fig': [('underline', .13, .39, .215)], 'c': 'green', 'at': 4})
S = 'Related rates'
B.spen(LESSON, S, 0, {'fig': [('circle', .77, .75, .1, .06)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .325, .13, .07, .05)], 'c': 'purple', 'at': 2},
       {'fig': [('underline', .42, .52, .48)], 'c': 'orange', 'at': 3}, {'fig': [('circle', .05, .55, .035, .17)], 'c': 'purple', 'at': 9},
       {'fig': [('circle', .42, .963, .09, .035)], 'c': 'blue', 'at': 9, 'dt': 0.8}, {'fig': [('arrow', .3, .2, .3, .36)], 'c': 'purple', 'at': 11})
S = 'Optimization:'
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, y, .03, .04)], 'c': 'red', 'at': 0, 'dt': t} for x, y, t in ((.14, .355, 2.0), (.325, .355, 2.4), (.14, .59, 2.8), (.325, .59, 3.2))],
       {'fig': [('underline', .17, .3, .51)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .39, .6, .1)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .94, .06, .045, .05)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .63, .145, .035, .05)], 'c': 'orange', 'at': 1}, {'fig': [('check', .7, .25)], 'c': 'green', 'at': 2})
S = 'Curve sketching'
B.spen(LESSON, S, 0, {'fig': [('arrow', .17, .8, .3, .42)], 'c': 'green', 'at': 1}, {'fig': [('arrow', .4, .38, .62, .62)], 'c': 'red', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .357, .331, .035, .05)], 'c': 'green', 'at': 1}, {'fig': [('circle', .693, .672, .035, .05)], 'c': 'red', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 2, {'fig': [('box', .19, .21, .47, .32)], 'c': 'green', 'at': 2}, {'fig': [('box', .69, .68, .97, .8)], 'c': 'red', 'at': 3})
B.spen(LESSON, S, 3, {'fig': [('circle', .524, .5, .035, .05)], 'c': 'purple', 'at': 0}, {'fig': [('underline', .55, .8, .475)], 'c': 'purple', 'at': 1})
S = "Newton's method"
B.spen(LESSON, S, 0, {'fig': [('circle', .217, .83, .03, .045)], 'c': 'orange', 'at': 2}, {'fig': [('arrow', .23, .82, .5, .67)], 'c': 'orange', 'at': 2, 'dt': 1.5})
B.spen(LESSON, S, 1, {'fig': [('box', .11, .18, .43, .32)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .137, .345, .025, .035)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .23, .345, .04, .035)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .517, .6, .025, .04)], 'c': 'purple', 'at': 2, 'dt': 1.0}, {'fig': [('circle', .375, .345, .07, .04)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .58, .345, .085, .04)], 'c': 'green', 'at': 4})
S = 'Area by rectangles'
B.spen(LESSON, S, 0, {'fig': [('circle', .84, .055, .09, .05)], 'c': 'orange', 'at': 3}, {'fig': [('circle', .78, .26, .05, .09)], 'c': 'red', 'at': 4},
       {'fig': [('circle', .55, .55, .045, .07)], 'c': 'red', 'at': 4, 'dt': 0.8})
B.spen(LESSON, S, 1, {'fig': [('circle', .85, .055, .09, .05)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .86, .055, .085, .05)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .11, .63, .29)], 'c': 'blue', 'at': 1})
S = 'The Fundamental Theorem'
B.spen(LESSON, S, 3, {'fig': [('circle', .4, .68, .1, .07)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .56, .86, .765)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .82, .7, .05, .045)], 'c': 'red', 'at': 3})
S = 'u-substitution'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'u = x²', 'c': 'blue', 'at': 4}, {'p': 'underline', 'on': 'du = 2x dx', 'c': 'blue', 'at': 5},
       {'p': 'box', 'on': '= ∫ cos(u) du', 'c': 'orange', 'at': 5, 'dt': 2.0}, {'p': 'circle', 'on': '= sin(x²) + C', 'c': 'green', 'at': 7},
       {'p': 'circle', 'on': '✓', 'c': 'green', 'at': 10})
B.spen(LESSON, S, 1, {'fig': [('box', .23, .27, .475, .83)], 'c': 'blue', 'at': 3}, {'fig': [('box', .475, .55, .72, .83)], 'c': 'green', 'at': 3, 'dt': 2.0},
       {'fig': [('circle', .845, .055, .12, .05)], 'c': 'red', 'at': 4})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_dne(ax, n, w, h):
    X0, Y0, s = w / 2, h / 2, 150
    P = lambda x, y: (X0 + x * s, Y0 + y * s)
    if n >= 1:
        B.arr(ax, *P(-2.6, 0), *P(2.6, 0), 'gray', 2, 18); B.arr(ax, *P(0, -1.9), *P(0, 1.9), 'gray', 2, 18)
        B.lab(ax, *P(2.55, -0.25), 'x', 28, 'gray'); B.lab(ax, *P(0.25, 1.8), 'y', 28, 'gray')
        B.ln(ax, [P(-2.4, -1)[0], P(-0.06, -1)[0]], [P(0, -1)[1]] * 2, c='blue', lw=4)
        B.dot(ax, *P(0, -1), c='blue', s=13, hollow=True); B.lab(ax, *P(-1.4, -1.35), 'from the left: −1', 28, 'blue')
    if n >= 2:
        B.ln(ax, [P(0.06, 1)[0], P(2.4, 1)[0]], [P(0, 1)[1]] * 2, c='green', lw=4)
        B.dot(ax, *P(0, 1), c='green', s=13, hollow=True); B.lab(ax, *P(1.4, 1.35), 'from the right: +1', 28, 'green')
    if n >= 3:
        B.arr(ax, *P(0.25, -0.85), *P(0.25, 0.85), 'red', 3, 22); B.lab(ax, *P(0.45, 0.45), 'jump!', 30, 'red', ha='left')

def draw_plusc(ax, n, w, h):
    X0, Y0, sx, sy = w / 2, h * 0.42, 170, 95
    P = lambda x, y: (X0 + x * sx, Y0 + y * sy)
    xs = np.linspace(-1.7, 1.7, 80)
    if n >= 1:
        B.arr(ax, *P(-2, 0), *P(2, 0), 'gray', 2, 18); B.arr(ax, *P(0, -2.2), *P(0, 3.6), 'gray', 2, 18)
        B.ln(ax, *zip(*[P(x, x ** 3 / 3) for x in xs]), c='blue', lw=4); B.lab(ax, *P(1.75, 1.95), 'C = 0', 26, 'blue', ha='left')
    if n >= 2:
        for c, col in ((1, 'green'), (2, 'orange'), (-1, 'purple')):
            B.ln(ax, *zip(*[P(x, x ** 3 / 3 + c) for x in xs]), c=col, lw=3); B.lab(ax, *P(1.75, 1.64 + c), f'C = {c}', 26, col, ha='left')
    if n >= 3:
        for c in (0, 1, 2, -1):
            x = 0.9; y = x ** 3 / 3 + c
            B.ln(ax, *zip(P(x - 0.35, y - 0.35 * 0.81), P(x + 0.35, y + 0.35 * 0.81)), c='red', lw=3)
        B.lab(ax, *P(-1.0, 3.2), 'same slope at every x', 28, 'red')

B.insert(LESSON, 'Worked example: a limit that needs a trick', {'t': 'wb', 'h': 'When a limit does NOT exist', 'draw': 'dne', 'split': 0.5, 'steps': [
    {'say': "A question students always ask: does every function have a limit? No. Look at f of x equals the absolute value of x, divided by x. For any negative x, that's negative one. Approach zero from the left, and the function is stuck at negative one.",
     'w': [{'m': r'$f(x) = \frac{|x|}{x}$', 'at': 1}, {'d': 1, 'at': 2}, {'m': r'$\lim_{x\to 0^-} f(x) = -1$', 'c': 'blue', 'at': 3}]},
    {'say': "For any positive x, it's positive one. So approaching from the right gives a different answer. The little minus and plus signs on the zero mean from the left and from the right. These are called one sided limits.",
     'w': [{'d': 2, 'at': 0}, {'m': r'$\lim_{x\to 0^+} f(x) = +1$', 'c': 'green', 'at': 1}]},
    {'say': "The rule: the limit exists only if both one sided limits exist and agree. Here they disagree, so the limit does not exist. That's a jump. A function that blows up to infinity, like one over x squared at zero, also has no limit as a number. We just write that it goes to infinity.",
     'w': [{'d': 3, 'at': 0}, {'m': 'left ≠ right  →  limit does not exist', 'c': 'red', 'box': True, 'at': 1, 'fs': 36},
           {'m': r'$\frac{1}{x^2} \to \infty$ : no finite limit', 'at': 3, 'fs': 36}]},
]})

B.insert(LESSON, 'Worked example: a derivative from the definition', {'t': 'wb', 'h': 'Three notations for one idea', 'steps': [
    {'say': "Before we go on, let's clear up the notation, because textbooks mix it freely. If y equals f of x, its derivative can be written f prime of x, y prime, d y d x, or d d x of f of x. These all mean exactly the same thing: the slope of f at x.",
     'w': [{'m': r"$f'(x)\ =\ y'\ =\ \frac{dy}{dx}\ =\ \frac{d}{dx}\,f(x)$", 'at': 1, 'fs': 52}, {'m': 'all mean: the slope of f at x', 'c': 'green', 'at': 2}]},
    {'say': "Prime notation, from Lagrange, is short and handy. Leibniz notation, d y over d x, reminds you it came from a tiny change in y over a tiny change in x. And d over d x, on its own, is an instruction: take the derivative of whatever comes next, with respect to x.",
     'w': [{'m': r"$f'$ : short and handy", 'at': 0}, {'m': r'$\frac{dy}{dx}$ : tiny change in y  over  tiny change in x', 'at': 1},
           {'m': r'$\frac{d}{dx}$ : an instruction, "differentiate"', 'at': 2}]},
    {'say': "One warning. d y d x is not really a fraction, because it's a limit. But in the chain rule it behaves like one, which is exactly why Leibniz's notation won.",
     'w': [{'m': r'$\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}$  (looks like cancelling!)', 'c': 'blue', 'at': 1}]},
]})

B.insert(LESSON, 'Shortcut rules', {'t': 'wb', 'h': 'Worked example: product and quotient rules', 'steps': [
    {'say': "Let's actually use the product rule. y equals x squared times sine x. Call the first factor f, x squared, and the second g, sine x. The rule: f prime g plus f g prime.",
     'w': [r'$y = x^2\,\sin x$', {'m': r"$(fg)' = f'g + fg'$", 'c': 'blue', 'at': 2}]},
    {'say': "f prime is two x, so the first term is two x sine x. g prime is cosine x, so the second term is x squared cosine x. Add them.",
     'w': [{'m': r"$y' = 2x\,\sin x + x^2\cos x$", 'at': 2, 'box': True}]},
    {'say': "Now a quotient: x over x squared plus one. Low d high, minus high d low, over low squared. The low is x squared plus one, d high is one. The high is x, d low is two x.",
     'clear': True,
     'w': [r'$y = \frac{x}{x^2+1}$', {'m': r"$(f/g)' = \frac{f'g - fg'}{g^2}$", 'c': 'blue', 'at': 1},
           {'m': r"$y' = \frac{(1)(x^2+1) - x\,(2x)}{(x^2+1)^2} = \frac{1 - x^2}{(x^2+1)^2}$", 'at': 2}]},
    {'say': "And the most common mistake on every first exam: the derivative of a product is not the product of the derivatives. Test it on x times x. The product of the derivatives is one times one, which is one. But x times x is x squared, whose derivative is two x. Wrong.",
     'w': [{'m': r"$(fg)' \neq f'\,g'$", 'c': 'red', 'at': 1, 'fs': 50}, {'m': r"test $f = g = x$:  $f'g' = 1$,  but  $(x^2)' = 2x$", 'at': 2}]},
]})

B.insert(LESSON, 'The Fundamental Theorem of Calculus', {'t': 'wb', 'h': "Why '+ C'? Indefinite vs definite integrals", 'draw': 'plusc', 'split': 0.52, 'steps': [
    {'say': "Every student asks where the plus C comes from. Differentiate x cubed over three, and you get x squared. But add five, or subtract seven, and the derivative is still x squared, because a constant has slope zero.",
     'w': [{'m': r'$\frac{d}{dx}\,\frac{x^3}{3} = x^2$', 'at': 1}, {'d': 1, 'at': 1}, {'m': r'$\frac{d}{dx}(\frac{x^3}{3} + 5) = x^2$', 'at': 2}]},
    {'say': "So going backwards, we can't know which constant was there. The answer is a whole family of curves, each shifted up or down, all with the same slope at every x. We write the family as x cubed over three, plus C.",
     'w': [{'d': 2, 'at': 1}, {'d': 3, 'at': 1}, {'m': r'$\int x^2\,dx = \frac{x^3}{3} + C$', 'c': 'blue', 'box': True, 'at': 2}]},
    {'say': "The d x at the end means: with respect to x. It's the width of those thin rectangles. Now a definite integral, from zero to two. The C appears at both ends, and cancels when we subtract. That's why definite integrals never need it.",
     'w': [{'m': r'$\int_0^2 x^2\,dx = (\frac{8}{3} + C) - (0 + C) = \frac{8}{3}$', 'at': 1, 'fs': 36}]},
    {'say': "So remember: an indefinite integral, with no limits, is a function, really a family of functions, so it needs plus C. A definite integral, with limits, is a number, an area.",
     'w': [{'m': 'indefinite → a family of functions (+ C)', 'c': 'purple', 'at': 0}, {'m': 'definite → a number (an area)', 'c': 'green', 'at': 1}]},
]})

G = 'When a limit does NOT exist'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'0^+', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'left ≠ right', 'at': 1})
G = 'Three notations for one idea'
B.pen(LESSON, G, 0, {'p': ('box',), 'on': r"$f'(x)\ =\ y'", 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'$\frac{dy}{dx} = \frac{dy}{du}', 'c': 'red', 'at': 1})
G = 'Worked example: product and quotient rules'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r"$y' = 2x\,\sin x", 'c': 'green', 'at': 0})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': r"$(fg)' \neq f'\,g'$", 'c': 'red', 'at': 1}, {'p': ('underline',), 'on': r"test $f = g = x$", 'c': 'blue', 'at': 4})
G = "Why '+ C'? Indefinite vs definite integrals"
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'$\int_0^2 x^2\,dx', 'c': 'blue', 'at': 2}, {'p': ('check',), 'on': r'(0 + C) = \frac{8}{3}$', 'at': 3})
