import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_slope(path, w, h):
    fig, ax = plot(w, h, grid=False)
    t = X(0, 40, 21); T = X(10, 100, 19); Tg, Yg = np.meshgrid(t, T)
    dT = -0.1 * (Yg - 20); dt = np.ones_like(dT)
    L = np.sqrt(dt ** 2 + (dT / 3) ** 2); ax.quiver(Tg, Yg, dt / L, dT / L / 3 * 3, color=C['gray'], angles='xy', scale=40, width=0.003)
    tt = X(0, 40, 300)
    for T0, col in ((90, C['orange']), (60, C['blue']), (10, C['green'])):
        ax.plot(tt, 20 + (T0 - 20) * np.exp(-0.1 * tt), color=col, lw=3)
    ax.axhline(20, color=C['red'], ls='--', lw=2); ax.text(39.5, 9, 'room = 20 °C (equilibrium)', color=C['red'], fontsize=17, ha='right', zorder=7, bbox=dict(fc='white', ec='none', alpha=0.9, pad=2))
    ax.set_xlabel('time (min)'); ax.set_ylabel('temperature (°C)'); ax.set_title('slope field of dT/dt = −0.1 (T − 20)', fontsize=20)
    save(fig, path)

def fig_coffee(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 40, 300); ax.plot(t, 20 + 70 * np.exp(-0.1 * t), color=C['orange']); soliddot(ax, 10, 20 + 70 * np.exp(-1), C['blue'])
    ax.axhline(20, color=C['gray'], ls='--'); ax.set_xlabel('time (min)'); ax.set_ylabel('°C')
    note(ax, 11, 50, 'T(10) = 20 + 70/e ≈ 45.8 °C', C['blue'], 20)
    ax.set_title('T(t) = 20 + 70 e^(−0.1t)', fontsize=21)
    save(fig, path)

def fig_rref(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    def mat(x, y, rows, hl=None):
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                txt(ax, x + j * 9, y - i * 8, v, 22, C['orange'] if (hl and (i, j) in hl) else C['ink'], bold=bool(hl and (i, j) in hl))
        line(ax, [(x - 4, y + 4), (x - 4, y - len(rows) * 8 + 4)], C['ink'], 2.5); line(ax, [(x + len(rows[0]) * 9 - 5, y + 4), (x + len(rows[0]) * 9 - 5, y - len(rows) * 8 + 4)], C['ink'], 2.5)
        line(ax, [(x + (len(rows[0]) - 1) * 9 - 4.5, y + 4), (x + (len(rows[0]) - 1) * 9 - 4.5, y - len(rows) * 8 + 4)], C['gray'], 1.5, ls='--')
    mat(8, 44, [['2', '1', '5'], ['1', '3', '5']]); txt(ax, 18, 54, 'augmented [A | b]', 18, C['mut'])
    arrow(ax, (36, 40), (46, 40), text='R2 − ½R1', fs=16)
    mat(54, 44, [['2', '1', '5'], ['0', '2.5', '2.5']], hl={(1, 0)}); arrow(ax, (80, 40), (88, 40))
    txt(ax, 50, 18, 'back-substitute:  2.5y = 2.5 → y = 1;   2x + 1 = 5 → x = 2', 21, C['blue'], bold=True)
    txt(ax, 50, 6, '2x + y = 5,   x + 3y = 5   →   (x, y) = (2, 1)', 20, C['ink'])
    save(fig, path)

def fig_transform(path, w, h):
    fig, axs = plot(w, h, ncols=3, grid=False)
    sq = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]])
    mats = [(np.array([[2, 0], [0, 1]]), 'scale x by 2\ndet = 2'), (np.array([[0, -1], [1, 0]]), 'rotate 90°\ndet = 1'), (np.array([[1, 1], [0, 1]]), 'shear\ndet = 1')]
    for a, (M, t) in zip(axs, mats):
        P = M @ sq; a.fill(sq[0], sq[1], color=C['lblue'], alpha=0.6); a.plot(sq[0], sq[1], color=C['blue'], lw=2)
        a.fill(P[0], P[1], color=C['lorange'], alpha=0.6); a.plot(P[0], P[1], color=C['orange'], lw=3)
        a.set_xlim(-1.3, 2.3); a.set_ylim(-0.5, 1.6); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([]); a.axhline(0, color=C['gray'], lw=1); a.axvline(0, color=C['gray'], lw=1)
        a.set_title(t, fontsize=18)
    save(fig, path)

def fig_basis(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, grid=False, gridspec_kw={'width_ratios': [1, 1.4]})
    a1.set_aspect('equal'); a1.set_xlim(-0.3, 3.6); a1.set_ylim(-0.3, 2.6)
    for v, c in (((1, 0), C['blue']), ((0, 1), C['green'])): a1.annotate('', xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=c, lw=3.5))
    a1.annotate('', xy=(3, 2), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=C['orange'], lw=3.5))
    a1.plot([1, 2, 3, 3, 3], [0, 0, 0, 1, 2], ':', color=C['gray']); a1.text(0.15, 1.8, 'v = 3e₁ + 2e₂', fontsize=16, color=C['orange'])
    a1.set_xticks([]); a1.set_yticks([]); a1.set_title('a basis builds every vector', fontsize=18)
    t = X(0, 2 * np.pi, 600); s = np.zeros_like(t)
    for k, c in zip((1, 3, 5), (C['blue'], C['green'], C['purple'])):
        term = 4 / np.pi * np.sin(k * t) / k; s += term; a2.plot(t, term, color=c, lw=1.4, alpha=0.7)
    a2.plot(t, s, color=C['orange'], lw=3); a2.plot(t, np.sign(np.sin(t)), color=C['ink'], lw=1.5, ls='--')
    a2.set_xticks([]); a2.set_yticks([]); a2.set_title('sines as a basis for signals\n(3 terms ≈ square wave)', fontsize=18)
    save(fig, path)

def fig_lsq(path, w, h):
    fig, ax = plot(w, h)
    rng = np.random.default_rng(4); x = X(0, 10, 12); y = 1.8 * x + 3 + rng.normal(0, 2.0, len(x))
    A = np.vstack([x, np.ones_like(x)]).T; m, b = np.linalg.lstsq(A, y, rcond=None)[0]
    ax.plot(x, y, 'o', color=C['blue'], ms=9); xx = X(0, 10, 50); ax.plot(xx, m * xx + b, color=C['orange'], lw=3)
    for xi, yi in zip(x, y): ax.plot([xi, xi], [yi, m * xi + b], color=C['red'], lw=1.5, ls=':')
    ax.set_title(f'least squares: y ≈ {m:.2f}x + {b:.2f}', fontsize=20); ax.set_xlabel('input'); ax.set_ylabel('measurement')
    note(ax, 0.3, max(y) - 2, 'minimizes the sum of\nsquared red gaps', C['red'], 17)
    save(fig, path)

def fig_eigen(path, w, h):
    fig, ax = plot(w, h, grid=False); ax.set_aspect('equal')
    A = np.array([[2, 1], [1, 2]])
    for ang in np.linspace(0, np.pi, 9, endpoint=False):
        v = np.array([np.cos(ang), np.sin(ang)]); Av = A @ v
        special = abs(v[0] * Av[1] - v[1] * Av[0]) < 1e-6
        ax.annotate('', xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=C['gray'], lw=1.5))
        ax.annotate('', xy=Av, xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=C['orange'] if special else C['lblue'], lw=3 if special else 1.6))
    ax.text(2.2, 2.4, 'λ = 3 along (1, 1)', fontsize=19, color=C['orange'], fontweight='bold'); ax.text(0.5, -1.4, 'λ = 1 along (1, −1)', fontsize=19, color=C['orange'], fontweight='bold')
    ax.set_xlim(-3.2, 3.6); ax.set_ylim(-2, 3.4); ax.axhline(0, color=C['ink'], lw=1); ax.axvline(0, color=C['ink'], lw=1)
    ax.set_title('A = [[2,1],[1,2]] turns most vectors;\neigenvectors only stretch', fontsize=18)
    save(fig, path)

def fig_damping(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 10, 400)
    ax.plot(t, np.exp(-0.25 * t) * np.cos(2 * t), color=C['blue'], label='underdamped (rings)')
    ax.plot(t, (1 + 2 * t) * np.exp(-2 * t), color=C['green'], label='critically damped (fastest, no overshoot)')
    ax.plot(t, 1.17 * np.exp(-0.54 * t) - 0.17 * np.exp(-3.7 * t), color=C['orange'], label='overdamped (sluggish)')
    ax.axhline(0, color=C['ink'], lw=1); ax.legend(loc='upper right', fontsize=16); ax.set_xlabel('time'); ax.set_ylabel('displacement')
    ax.set_title("a y'' + b y' + c y = 0", fontsize=21)
    save(fig, path)

def fig_phase(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, grid=False)
    x = X(-2, 2, 15); Xg, Yg = np.meshgrid(x, x)
    for a, A, t in ((a1, np.array([[-1, -2], [2, -1]]), 'eigenvalues −1 ± 2i\nspirals in: STABLE'), (a2, np.array([[1, 0], [0, -1]]), 'eigenvalues +1, −1\nescapes: UNSTABLE')):
        U = A[0, 0] * Xg + A[0, 1] * Yg; V = A[1, 0] * Xg + A[1, 1] * Yg
        a.streamplot(Xg, Yg, U, V, color=C['blue'] if a is a1 else C['red'], density=1.0, linewidth=1.4)
        a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([]); a.set_title(t, fontsize=18)
    save(fig, path)

LESSON = {
 'code': 'MATH 250B', 'title': 'Linear Algebra & Differential Equations', 'tag': 'Year 2 · Foundations', 'folder': 'MATH-250B Differential Equations & Linear Algebra',
 'slides': [
 {'t': 'title', 'h': 'Linear Algebra & Differential Equations', 'sub': 'Equations of change, systems of equations, and the matrices that tie them together', 'img': 'a:suspension',
  'say': "Welcome to Math two fifty B, linear algebra and differential equations. These two subjects look different at first, but they turn out to be one subject. Differential equations describe how things change: a cooling cup of coffee, a charging capacitor, a car's suspension. Linear algebra handles many equations at once with matrices. By the end, you'll see that eigenvalues of a matrix decide whether a system settles down or blows up, which is the core idea of every circuit and control system you'll ever design."},

 {'t': 'section', 'kicker': 'Part 1', 'h': 'First-order differential equations', 'sub': 'Equations that describe change',
  'say': "Part one. First order differential equations."},

 {'t': 'v', 'h': 'A differential equation describes how something changes', 'img': ['a:coffee', 'fig:slope'],
  'pts': ['Unknown is a function, not a number', 'dT/dt = −k(T − T_room): cools faster when hotter', 'Slope field: the slope at every point', 'Solutions follow the arrows; equilibrium where slope = 0'],
  'say': ["In algebra, you solve for a number. In a differential equation, you solve for a whole function, given a rule for how it changes. Take a hot cup of coffee. Newton's law of cooling says it loses heat at a rate proportional to how much hotter it is than the room.",
          "Written as an equation: d T d t equals minus k times T minus twenty, for a room at twenty degrees. Hot coffee cools fast. Lukewarm coffee cools slowly.",
          "Even before solving it, we can draw it. A slope field puts a little arrow at every point, showing the slope the equation demands there.",
          "Every solution is a curve that follows the arrows. Start at ninety degrees, the orange curve, and it bends down toward twenty. Start below room temperature, the green curve, and it warms up toward twenty. The flat red line, where the slope is zero, is the equilibrium. Everything is attracted to it."]},

 {'t': 'ex', 'h': 'Solving it: separation of variables', 'img': 'fig:coffee', 'split': 0.55,
  'code': "dT/dt = −0.1 (T − 20)      T(0) = 90 °C\n\nseparate:   dT / (T − 20) = −0.1 dt\nintegrate:  ln|T − 20| = −0.1 t + C\nsolve:      T(t) = 20 + A e^(−0.1 t)\ninitial:    90 = 20 + A  →  A = 70\n\nT(t) = 20 + 70 e^(−0.1 t)\nT(10) = 20 + 70/e ≈ 45.8 °C",
  'say': "When a differential equation is separable, put everything with T on one side and everything with t on the other. Integrate both sides: the natural log of T minus twenty equals negative point one t, plus a constant. Exponentiate, and T equals twenty plus some constant A times e to the minus point one t. The initial condition, ninety degrees at time zero, gives A equals seventy. So after ten minutes, the coffee is at twenty plus seventy over e, about forty six degrees. Notice the shape: an exponential decay toward a final value. That's exactly the formula for a capacitor charging or discharging through a resistor, which you'll use constantly in circuits. Same equation, different physics. The other main technique, for linear first order equations, is the integrating factor, which handles equations with a forcing term like a changing outside temperature or an input voltage."},

 {'t': 'section', 'kicker': 'Part 2', 'h': 'Linear algebra', 'sub': 'Many equations at once',
  'say': "Part two. Linear algebra."},

 {'t': 'v', 'h': 'Systems of equations and row reduction', 'img': 'fig:rref',
  'pts': ['Write as A x = b', 'Row-reduce the augmented matrix', 'Outcomes: one solution, infinitely many, or none', 'Circuit analysis produces exactly these systems'],
  'say': ["Many problems give you several linear equations in several unknowns. We write them compactly as A x equals b, where A is a matrix of coefficients.",
          "To solve, row reduce the augmented matrix: swap rows, scale rows, and add multiples of one row to another, until it's triangular. Here, subtracting half of row one from row two eliminates x. Then back substitute: y equals one, so x equals two.",
          "There are only three possible outcomes. Exactly one solution, infinitely many solutions with free variables, or no solution at all, which shows up as a row saying zero equals something nonzero.",
          "In circuits, nodal analysis writes Kirchhoff's current law at each node, and you get exactly this kind of system. A circuit with fifty nodes is a fifty by fifty matrix, and circuit simulators like SPICE solve systems like this millions of times."]},

 {'t': 'v', 'h': 'A matrix is a transformation', 'img': 'fig:transform',
  'pts': ['Multiplying by A moves every point', 'Columns of A = where the basis vectors land', 'det A = area (or volume) scaling factor', 'det A = 0 → space gets squashed → not invertible'],
  'say': ["Here's the most useful way to think about a matrix: it's a machine that moves every point in space. Multiply a vector by A and you get a new vector. These pictures show the unit square, in blue, transformed into the orange shape.",
          "The columns of A tell you where the basis vectors land. The first column is where the x direction goes, the second is where the y direction goes. That's how 3D graphics rotate and scale every point of a model: one matrix multiply per point.",
          "The determinant is the factor by which areas get scaled. Stretching x by two doubles areas, so the determinant is two. Rotations and shears keep area the same, so their determinant is one.",
          "And if the determinant is zero, the matrix squashes the plane flat onto a line. Information is lost, so you can't undo it: the matrix has no inverse. This connects a dozen facts into one theorem. A is invertible exactly when the determinant isn't zero, exactly when the columns are independent, exactly when A x equals b always has a unique solution."]},

 {'t': 'v', 'h': 'Vector spaces, basis and dimension', 'img': 'fig:basis',
  'pts': ['Vector space: anything you can add and scale', 'Rⁿ, polynomials, solutions of linear ODEs, signals', 'Basis: independent vectors that build everything', 'Rank + nullity = number of columns'],
  'say': ["Linear algebra generalizes far beyond arrows. A vector space is any collection of objects you can add together and multiply by numbers, following the usual rules.",
          "That includes ordinary vectors, but also polynomials, matrices, the solutions of a linear differential equation, and audio signals. That's why the same tools work in so many places.",
          "A basis is a minimal set of vectors from which you can build every vector in the space, using combinations. The number of vectors in a basis is the dimension. Sine and cosine waves at different frequencies form a basis for signals, which is the idea behind the Fourier series you'll study in signals and systems.",
          "And the rank nullity theorem: the dimension of the output space a matrix reaches, plus the dimension of the inputs it crushes to zero, always equals the number of columns. Nothing is lost without being accounted for."]},

 {'t': 'v', 'h': 'Least squares: fitting a line to noisy data', 'img': 'fig:lsq',
  'pts': ['More equations than unknowns → no exact solution', 'Find the closest one: minimize squared error', 'Normal equations: AᵀA x = Aᵀb', 'Calibration, trend lines, machine learning'],
  'say': ["Real measurements are noisy. If you have twelve data points and want the best line through them, you have twelve equations and only two unknowns, the slope and intercept. There's no exact solution.",
          "So we find the closest one: the line that minimizes the sum of the squared vertical gaps, the red dotted lines.",
          "Linear algebra solves this in one step with the normal equations: A transpose A x equals A transpose b. Geometrically, it projects the data onto the space of possible lines.",
          "Engineers use least squares to calibrate sensors, fit trend lines, estimate positions from GPS signals, and it's the starting point of machine learning. Linear regression is literally this slide."]},

 {'t': 'v', 'h': 'Eigenvalues: directions a matrix only stretches', 'img': 'fig:eigen',
  'pts': ['A v = λ v: v keeps its direction, scaled by λ', 'Solve det(A − λI) = 0', 'A = [[2,1],[1,2]] → λ = 3 on (1,1), λ = 1 on (1,−1)', 'Google’s PageRank is an eigenvector'],
  'say': ["Most vectors get turned when you multiply by a matrix. Look at the light blue arrows: their directions change. But a few special directions only get stretched. Those are eigenvectors, and the stretch factor is the eigenvalue.",
          "To find them, solve the determinant of A minus lambda I equals zero. For this matrix, that's two minus lambda squared, minus one, equals zero.",
          "So lambda is three or one. The eigenvector for three is one, one: multiplying gives three, three, the same direction tripled. The eigenvector for one is one, negative one, which comes back unchanged. Those are the orange arrows.",
          "Eigenvectors are everywhere. Google's original PageRank algorithm ranked web pages by finding the main eigenvector of an enormous matrix of links between pages. Vibration engineers find the eigenvectors of a structure to learn its natural shapes of vibration. And as we'll see in a moment, eigenvalues decide whether a system is stable."]},

 {'t': 'section', 'kicker': 'Part 3', 'h': 'Higher-order equations and systems', 'sub': 'Springs, circuits and stability',
  'say': "Part three. Where the two halves of the course meet."},

 {'t': 'v', 'h': 'Second-order equations: springs, suspensions and RLC circuits', 'img': ['fig:damping', 'a:tacoma'],
  'pts': ["a y″ + b y′ + c y = 0 → try y = e^(rt)", 'Real roots: overdamped · repeated: critical', 'Complex α ± iβ: rings at β while decaying at α', 'Car suspensions aim for near-critical damping'],
  'say': ["A mass on a spring with friction, a car's suspension, and a resistor, inductor and capacitor circuit all obey the same equation: a y double prime plus b y prime plus c y equals zero. Guess y equals e to the r t, and you get the characteristic equation, a r squared plus b r plus c equals zero. Its roots decide everything. Two real roots: overdamped. The system creeps back without oscillating, the orange curve. A repeated root: critically damped, the fastest return without overshooting, the green curve. That's what a car's shock absorbers are designed to approach. Complex roots, alpha plus or minus i beta: underdamped. It rings at frequency beta while dying off at rate alpha, the blue curve. Add a forcing term, like a bumpy road or an input voltage, and the full solution is this homogeneous part plus one particular solution.",
          "And when the forcing frequency matches a system's natural frequency, the response can grow huge. That's resonance. The famous nineteen forty collapse of the Tacoma Narrows Bridge is often described as resonance, though engineers today attribute it to a related effect called aeroelastic flutter, where the wind fed energy into the bridge's twisting oscillation. Either way, the lesson is the same: you must know your system's natural modes. In circuits, resonance is a feature: it's how a radio tunes to one station."]},

 {'t': 'v', 'h': 'Systems of ODEs: eigenvalues decide stability', 'img': 'fig:phase',
  'pts': ['x′ = A x for a vector of states', 'Solutions built from e^(λt) v for each eigenpair', 'All Re(λ) < 0 → everything decays: STABLE', 'Any Re(λ) > 0 → something blows up: UNSTABLE'],
  'say': ["Real systems have many interacting states: positions and velocities, voltages and currents. We stack them into a vector x and write x prime equals A x.",
          "The solutions are built from e to the lambda t times v, one term for each eigenvalue and eigenvector pair of A. So the eigenvalues of A control the behavior of the whole system.",
          "If every eigenvalue has a negative real part, every term decays, and the system settles down. On the left, the eigenvalues are negative one plus or minus two i, so trajectories spiral inward. That's stable.",
          "If any eigenvalue has a positive real part, some term grows exponentially, and the system runs away, like the trajectories escaping on the right. This is the bridge to signals and systems and to control engineering, where those eigenvalues are called poles, and the first question about any design, from an amplifier to a drone, is: are all the poles in the left half plane?"]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Differential equations describe **change**; matrices handle **many equations at once**; **eigenvalues** decide whether a system settles or explodes.',
  'cap': 'Next: PHYS 226, Electricity & Magnetism. Later: circuits (EGEE 203) and signals (EGCP 371) use all of this.',
  'say': "To wrap up. First order differential equations model exponential change, and separation of variables solves them. Linear algebra solves many equations at once, matrices transform space, the determinant measures scaling and invertibility, and least squares fits models to data. Eigenvalues are the special stretch factors of a matrix. Second order equations describe springs and circuits, with damping set by their characteristic roots. And for systems, the eigenvalues decide stability. You'll lean on this course in circuits, signals, control, graphics and machine learning. Next up, electricity and magnetism. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B
M2 = lambda a, b, c, d: r'\genfrac{[}{]}{0}{0}{%s\quad %s}{%s\quad %s}' % (a, b, c, d)
V2 = lambda a, b: r'\genfrac{[}{]}{0}{0}{%s}{%s}' % (a, b)

def draw_lsq(ax, n, w, h):
    X0, Y0, sx, sy = 90, 90, 220, 120
    P = lambda x, y: (X0 + x * sx, Y0 + y * sy)
    pts = [(0, 1), (1, 3), (2, 4)]
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 2.8 * sx, Y0 + 5 * sy)
        for x, y in pts: B.dot(ax, *P(x, y), c='blue', s=15); B.lab(ax, P(x, y)[0] - 14, P(x, y)[1] + 30, f'({x}, {y})', 26, 'blue', ha='right')
    if n >= 2:
        B.ln(ax, *zip(P(-0.1, 1.5 * -0.1 + 7 / 6), P(2.5, 1.5 * 2.5 + 7 / 6)), c='red', lw=3.5)
        for x, y in pts: B.ln(ax, [P(x, y)[0]] * 2, [P(x, y)[1], P(x, 1.5 * x + 7 / 6)[1]], c='orange', lw=2.5, ls='--')
        B.lab(ax, *P(1.6, 4.6), 'y = 1.5x + 1.17', 30, 'red')

def draw_eig(ax, n, w, h):
    cx, cy, s = w * 0.36, h * 0.5, 62
    if n >= 1:
        B.arr(ax, cx - 2.5 * s, cy, cx + 6 * s, cy, 'gray', 2, 18); B.arr(ax, cx, cy - 5 * s, cx, cy + 5.8 * s, 'gray', 2, 18)
    if n >= 2:
        B.arr(ax, cx, cy, cx + s, cy + s, 'blue', 4.5); B.arr(ax, cx, cy, cx + 5 * s, cy + 5 * s, 'blue', 2, 22, '-|>')
        B.lab(ax, cx + 5 * s + 10, cy + 5 * s - 10, 'A(1,1) = (5,5)', 26, 'blue', ha='left')
    if n >= 3:
        B.arr(ax, cx, cy, cx + s, cy - 2 * s, 'green', 4.5); B.arr(ax, cx, cy, cx + 2 * s, cy - 4 * s, 'green', 2, 22)
        B.lab(ax, cx + 2 * s + 12, cy - 4 * s, 'A(1,−2) = (2,−4)', 26, 'green', ha='left')

def draw_overdamped(ax, n, w, h):
    X0, Y0, sx, sy = 80, h * 0.3, 210, 380
    P = lambda t, y: (X0 + t * sx, Y0 + y * sy)
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 3.3 * sx, Y0 + 1.25 * sy, 't', 'y')
        B.lab(ax, X0 - 15, Y0 + sy, '1', 28, 'gray', ha='right')
    if n >= 2:
        ts = np.linspace(0, 3.1, 150)
        B.ln(ax, *zip(*[P(t, 3 * np.exp(-2 * t) - 2 * np.exp(-3 * t)) for t in ts]), c='red', lw=3.5)
        B.lab(ax, *P(1.6, 0.55), 'no overshoot,\nno ringing', 30, 'red')

B.insert(LESSON, 'Systems of equations and row reduction', {'t': 'wb', 'h': 'Worked example: solving three equations by elimination', 'steps': [
    {'say': "Let's solve a system of three equations by hand. x plus y plus z equals six. Two y plus five z equals negative four. Two x plus five y minus z equals twenty seven.",
     'w': [{'m': r'$(1)\quad x + y + z = 6$', 'at': 1}, {'m': r'$(2)\quad 2y + 5z = -4$', 'at': 2}, {'m': r'$(3)\quad 2x + 5y - z = 27$', 'at': 3}]},
    {'say': "Step one: eliminate x from equation three. Subtract two times equation one. Two x cancels, five y minus two y is three y, minus z minus two z is minus three z, and twenty seven minus twelve is fifteen. Divide by three: y minus z equals five.",
     'w': [{'m': r'$(3) - 2(1):\quad 3y - 3z = 15$', 'at': 1}, {'m': r'$y - z = 5 \;\Rightarrow\; y = z + 5$', 'at': 4}]},
    {'say': "Step two: substitute y equals z plus five into equation two. Two times z plus five, plus five z, equals negative four. That's seven z plus ten equals negative four, so z equals negative two.",
     'w': [r'$2(z+5) + 5z = -4$', {'m': r'$7z = -14 \;\Rightarrow\; z = -2$', 'at': 2}]},
    {'say': "Back substitute. y is z plus five, which is three. And x is six minus y minus z: six minus three plus two, which is five. Always check in the equation you didn't use last: two times five plus five times three minus negative two is ten plus fifteen plus two, twenty seven. Correct. This is exactly what circuit simulators do, with thousands of equations instead of three.",
     'w': [{'m': r'$y = 3$,     $x = 6 - 3 + 2 = 5$', 'at': 1}, {'m': r'$(x, y, z) = (5,\ 3,\ -2)$', 'c': 'red', 'box': True, 'at': 2}, {'m': r'check (3): $10 + 15 + 2 = 27$', 'c': 'gray', 'at': 3}]},
]})

B.insert(LESSON, 'A matrix is a transformation', {'t': 'wb', 'h': 'Worked example: inverting a 2 × 2 matrix', 'steps': [
    {'say': "Let's solve A x equals b using an inverse. A is four, seven, two, six, and b is one, two. For a two by two matrix, the inverse has a shortcut. First the determinant: a d minus b c, four times six minus seven times two, which is ten. It's not zero, so A can be inverted.",
     'w': [{'m': r'$A = ' + M2(4, 7, 2, 6) + r',\qquad b = ' + V2(1, 2) + '$', 'at': 1}, {'m': r'$\det A = (4)(6) - (7)(2) = 10$', 'at': 3}]},
    {'say': "The shortcut: swap the two diagonal entries, negate the other two, and divide by the determinant. So the inverse is one tenth of six, negative seven, negative two, four.",
     'w': [{'m': r'$A^{-1} = \frac{1}{10}' + M2(6, -7, -2, 4) + '$', 'at': 1}]},
    {'say': "Now x equals A inverse times b. Top row: six times one minus seven times two is negative eight. Bottom row: negative two times one plus four times two is six. Divide by ten: x is negative point eight, point six.",
     'w': [{'m': r'$x = A^{-1}b = \frac{1}{10}' + V2(r'6(1) - 7(2)', r'-2(1) + 4(2)') + r' = \frac{1}{10}' + V2(-8, 6) + '$', 'at': 1}, {'m': r'$x = (-0.8,\ 0.6)$', 'c': 'red', 'box': True, 'at': 3}]},
    {'say': "Check it in the original equations. Four times negative point eight plus seven times point six is one. Two times negative point eight plus six times point six is two. Both match. In practice, computers solve by elimination rather than computing inverses, because it's faster and more accurate, but the inverse is the cleanest way to see what's happening.",
     'w': [{'m': r'check: $4(-0.8) + 7(0.6) = 1$,   $2(-0.8) + 6(0.6) = 2$', 'c': 'gray', 'at': 1}]},
]})

B.insert(LESSON, 'Least squares', {'t': 'wb', 'h': 'Worked example: the best-fit line through three points', 'draw': 'lsq', 'split': 0.55, 'steps': [
    {'say': "Let's fit a line to three measurements by hand: zero comma one, one comma three, and two comma four. No straight line passes through all three, so we want the one that minimizes the squared errors.",
     'w': [{'m': r'data: $(0,1),\ (1,3),\ (2,4)$'}, {'d': 1, 'at': 1}]},
    {'say': "Compute the averages. The average x is one. The average y is eight thirds, about two point six seven. Then subtract the averages: the x deviations are negative one, zero, one.",
     'w': [{'m': r'$\bar x = 1$,    $\bar y = \frac{8}{3}$', 'at': 1}, {'m': r'$x - \bar x:\ -1,\ 0,\ 1$', 'at': 3}]},
    {'say': "The best slope is the sum of the x deviations times the y values, over the sum of the squared x deviations. On top: negative one times one, plus zero, plus one times four, which is three. On the bottom: one plus zero plus one, two. So the slope is one point five.",
     'w': [r'$m = \frac{\sum (x-\bar x)\,y}{\sum (x-\bar x)^2}$', {'m': r'$= \frac{(-1)(1) + 0 + (1)(4)}{1 + 0 + 1} = \frac{3}{2}$', 'at': 1}]},
    {'say': "The line always passes through the averages, so the intercept is eight thirds minus one point five times one, which is seven sixths, about one point one seven. Look at the dashed orange errors: two points sit above the line and one below, and the squared errors are as small as any line can make them.",
     'w': [{'m': r'$b = \bar y - m\bar x = \frac{8}{3} - 1.5 = \frac{7}{6}$', 'at': 0}, {'m': r'$y = 1.5x + 1.17$', 'c': 'red', 'box': True, 'at': 0}, {'d': 2, 'at': 1}]},
]})

B.insert(LESSON, 'Eigenvalues', {'t': 'wb', 'h': 'Worked example: finding eigenvalues and eigenvectors', 'draw': 'eig', 'split': 0.55, 'steps': [
    {'say': "Let's find the eigenvalues of A equals four, one, two, three. Subtract lambda from the diagonal and set the determinant to zero. Four minus lambda, times three minus lambda, minus one times two, equals zero.",
     'w': [{'m': r'$A = ' + M2(4, 1, 2, 3) + '$'}, {'m': r'$\det(A - \lambda I) = (4-\lambda)(3-\lambda) - 2 = 0$', 'at': 2}, {'d': 1, 'at': 2}]},
    {'say': "Multiply out: lambda squared minus seven lambda plus twelve minus two, so lambda squared minus seven lambda plus ten. That factors as lambda minus five, times lambda minus two. The eigenvalues are five and two.",
     'w': [r'$\lambda^2 - 7\lambda + 10 = 0$', {'m': r'$(\lambda - 5)(\lambda - 2) = 0$', 'at': 1}, {'m': r'$\lambda = 5,\ \ \lambda = 2$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "For lambda equals five, solve A minus five I times v equals zero. The first row says negative x plus y equals zero, so v is one, one. Check: A times one, one is five, five. Same direction, stretched by five.",
     'w': [r'$\lambda=5$:  $-x + y = 0 \;\Rightarrow\; v_1 = (1,\ 1)$', {'d': 2, 'at': 2}]},
    {'say': "For lambda equals two, the first row says two x plus y equals zero, so v is one, negative two. A times that is two, negative four, which is exactly twice v. On the drawing, these two directions are special: A only stretches them. Every other vector gets turned.",
     'w': [r'$\lambda=2$:  $2x + y = 0 \;\Rightarrow\; v_2 = (1,\ -2)$', {'d': 3, 'at': 1}]},
]})

B.insert(LESSON, 'Second-order equations', {'t': 'wb', 'h': 'Worked example: an overdamped system', 'draw': 'overdamped', 'split': 0.55, 'steps': [
    {'say': "Let's solve a second order equation completely. y double prime plus five y prime plus six y equals zero, starting at y equals one, at rest. Guess y equals e to the r t. Every derivative brings down an r, so we get the characteristic equation: r squared plus five r plus six equals zero.",
     'w': [{'m': r"$y'' + 5y' + 6y = 0$,   $y(0)=1,\ y'(0)=0$"}, {'m': r'try $y = e^{rt}$:   $r^2 + 5r + 6 = 0$', 'at': 3}]},
    {'say': "It factors as r plus two times r plus three. Two real, negative roots: negative two and negative three. So the general solution is c one e to the minus two t, plus c two e to the minus three t.",
     'w': [r'$(r+2)(r+3) = 0 \;\Rightarrow\; r = -2,\ -3$', {'m': r'$y = c_1 e^{-2t} + c_2 e^{-3t}$', 'at': 2}]},
    {'say': "Use the starting conditions. At t equals zero, y is one, so c one plus c two equals one. The starting velocity is zero, so negative two c one minus three c two equals zero. Solve: c one is three and c two is negative two.",
     'w': [{'m': r'$c_1 + c_2 = 1$', 'at': 1}, {'m': r'$-2c_1 - 3c_2 = 0$', 'at': 2}, {'m': r'$c_1 = 3,\ \ c_2 = -2$', 'at': 3}]},
    {'say': "So y equals three e to the minus two t minus two e to the minus three t. Because both roots are real, the system just glides back to zero, with no overshoot and no ringing. That's overdamped, like a slow door closer. Complex roots would have made it oscillate.",
     'w': [{'d': 1}, {'m': r'$y(t) = 3e^{-2t} - 2e^{-3t}$', 'c': 'red', 'box': True}, {'d': 2, 'at': 1}]},
]})

# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'A differential equation describes'
B.spen(LESSON, S, 2, {'fig': [('circle', .6, .3, .1, .12)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .195, .2, .03, .04)], 'c': 'orange', 'at': 1}, {'fig': [('arrow', .22, .27, .4, .55)], 'c': 'orange', 'at': 1, 'dt': 1.0},
       {'fig': [('circle', .195, .8, .03, .04)], 'c': 'green', 'at': 2}, {'fig': [('arrow', .22, .79, .45, .75)], 'c': 'green', 'at': 2, 'dt': 1.0},
       {'fig': [('underline', .53, .92, .86)], 'c': 'red', 'at': 3})
S = 'Solving it: separation'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'dT / (T − 20) = −0.1 dt', 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': 'ln|T − 20| = −0.1 t + C', 'c': 'blue', 'at': 1},
       {'p': 'underline', 'on': 'T(t) = 20 + A e^(−0.1 t)', 'c': 'blue', 'at': 2}, {'p': 'circle', 'on': 'A = 70', 'c': 'orange', 'at': 3},
       {'p': 'box', 'on': 'T(10) = 20 + 70/e ≈ 45.8 °C', 'c': 'red', 'at': 4}, {'fig': [('circle', .36, .56, .03, .04)], 'c': 'red', 'at': 4, 'dt': 1.5},
       {'p': 'box', 'on': 'T(t) = 20 + 70 e^(−0.1 t)', 'c': 'green', 'at': 6})
S = 'Systems of equations and row'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .12, .31, .43)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('underline', .35, .47, .27)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .54, .33, .03, .06)], 'c': 'orange', 'at': 1, 'dt': 1.5},
       {'fig': [('underline', .07, .93, .7)], 'c': 'blue', 'at': 2})
S = 'A matrix is a transformation'
B.spen(LESSON, S, 2, {'fig': [('box', .02, .05, .31, .95)], 'c': 'orange', 'at': 1}, {'fig': [('box', .35, .05, .64, .95)], 'c': 'blue', 'at': 2},
       {'fig': [('box', .68, .05, .97, .95)], 'c': 'blue', 'at': 2, 'dt': 2.0})
S = 'Vector spaces'
B.spen(LESSON, S, 2, {'fig': [('circle', .17, .68, .04, .04)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .12, .61, .03, .06)], 'c': 'green', 'at': 0, 'dt': 0.6},
       {'fig': [('underline', .13, .36, .52)], 'c': 'orange', 'at': 0, 'dt': 2.0}, {'fig': [('box', .5, .02, .96, .97)], 'c': 'purple', 'at': 2})
S = 'Least squares'
B.spen(LESSON, S, 1, {'fig': [('circle', .45, .6, .03, .07)], 'c': 'red', 'at': 0}, {'fig': [('circle', .72, .4, .03, .08)], 'c': 'red', 'at': 0, 'dt': 1.0},
       {'fig': [('underline', .2, .52, .218)], 'c': 'red', 'at': 0, 'dt': 2.0})
B.spen(LESSON, S, 2, {'fig': [('underline', .28, .83, .1)], 'c': 'blue', 'at': 0})
S = 'Eigenvalues: directions'
B.spen(LESSON, S, 0, {'fig': [('circle', .6, .38, .12, .12)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .27, .67, .142)], 'c': 'orange', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('underline', .69, .97, .308)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .5, .8, .838)], 'c': 'orange', 'at': 2})
S = 'Second-order equations'
B.spen(LESSON, S, 0, {'fig': [('underline', .44, .73, .275)], 'c': 'orange', 'at': 3}, {'fig': [('underline', .44, .94, .22)], 'c': 'green', 'at': 5},
       {'fig': [('underline', .44, .7, .165)], 'c': 'blue', 'at': 8}, {'fig': [('circle', .33, .8, .04, .06)], 'c': 'blue', 'at': 8, 'dt': 1.5})
S = 'Systems of ODEs'
B.spen(LESSON, S, 2, {'fig': [('circle', .25, .56, .06, .08)], 'c': 'blue', 'at': 1}, {'fig': [('box', .06, .02, .44, .2)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('box', .53, .2, .97, .95)], 'c': 'red', 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_ringing(ax, n, w, h):
    X0, Y0, sx, sy = 60, h * 0.5, (w - 140) / 3.3, h * 0.36
    P = lambda t, y: (X0 + t * sx, Y0 + y * sy)
    t = np.linspace(0, 3.3, 300)
    if n >= 1:
        B.arr(ax, X0, Y0, X0 + 3.35 * sx, Y0, 'gray', 2, 16); B.lab(ax, X0 + 3.3 * sx, Y0 - 26, 't', 26, 'gray')
        B.ln(ax, *zip(*[P(a, np.exp(-a) * (np.cos(5 * a) + 0.2 * np.sin(5 * a))) for a in t]), c='blue', lw=3.5)
    if n >= 2:
        env = np.sqrt(1.04)
        B.ln(ax, *zip(*[P(a, env * np.exp(-a)) for a in t]), c='orange', lw=2.5, ls='--')
        B.ln(ax, *zip(*[P(a, -env * np.exp(-a)) for a in t]), c='orange', lw=2.5, ls='--')
        B.lab(ax, *P(0.9, 0.62), r'envelope $\pm e^{-t}$', 26, 'orange', ha='left')
        B.lab(ax, *P(1.6, -0.62), r'rings at $\beta = 5$ rad/s', 26, 'blue', ha='left')

B.insert(LESSON, 'Solving it: separation of variables', {'t': 'wb', 'h': 'Worked example: the integrating factor', 'steps': [
    {'say': "Separation doesn't work when there's an input term, so here's the integrating factor, worked out. Take y prime plus two y equals four, starting at zero. It's the shape of a capacitor charging toward a supply voltage.",
     'w': [{'m': r"$y' + 2y = 4$,    $y(0) = 0$", 'at': 1}, {'m': r"form:  $y' + p\,y = q$", 'c': 'gray', 'at': 2}]},
    {'say': "Multiply both sides by e to the integral of p, here e to the two t. Why that? Because now the left side is exactly the product rule result for e to the two t times y. That's the whole trick.",
     'w': [{'m': r'$\mu = e^{\int 2\,dt} = e^{2t}$', 'c': 'blue', 'at': 0}, {'m': r"$e^{2t}y' + 2e^{2t}y = (e^{2t}\,y)' = 4e^{2t}$", 'at': 2}]},
    {'say': "Integrate both sides: e to the two t times y equals two e to the two t, plus C. Divide by e to the two t: y equals two plus C e to the minus two t. The starting value zero gives C equals minus two.",
     'w': [{'m': r'$e^{2t}y = 2e^{2t} + C$', 'at': 0}, {'m': r'$y = 2 + Ce^{-2t}$,   $y(0) = 0 \Rightarrow C = -2$', 'at': 2}]},
    {'say': "So y equals two times one minus e to the minus two t. It starts at zero and rises toward two, fast at first, then slowly. That's exactly the voltage on a charging capacitor, with a time constant of one half.",
     'w': [{'m': r'$y(t) = 2\,(1 - e^{-2t})$', 'c': 'red', 'box': True, 'at': 0}]},
]})

B.insert(LESSON, 'Worked example: solving three equations by elimination', {'t': 'wb', 'h': 'Matrix multiplication: row times column', 'steps': [
    {'say': "Before we treat matrices as transformations, let's make sure the multiplication itself is clear, because it isn't done entry by entry. Each entry of the product is a row of the first matrix times a column of the second: multiply matching entries and add.",
     'w': [{'m': r'$A = \genfrac{[}{]}{0}{0}{1\quad 2}{3\quad 4}$,    $B = \genfrac{[}{]}{0}{0}{0\quad 1}{1\quad 0}$', 'at': 1, 'fs': 46},
           {'m': 'entry (i, j) = row i of A  ·  column j of B', 'c': 'blue', 'at': 2}]},
    {'say': "Top left of A B: row one of A, one two, times column one of B, zero one. One times zero plus two times one: two. Top right: one two times one zero: one. The bottom row the same way gives four and three.",
     'w': [{'m': r'top-left: $1(0) + 2(1) = 2$', 'at': 1}, {'m': r'top-right: $1(1) + 2(0) = 1$', 'at': 2},
           {'m': r'$AB = \genfrac{[}{]}{0}{0}{2\quad 1}{4\quad 3}$', 'c': 'green', 'at': 3, 'fs': 46}]},
    {'say': "Now swap the order. B A comes out as three, four, one, two. Different! A B swapped A's columns, but B A swapped its rows. Matrix multiplication is not commutative, so order always matters. And for A times a vector x, it's the same rule: each row of A dotted with x.",
     'w': [{'m': r'$BA = \genfrac{[}{]}{0}{0}{3\quad 4}{1\quad 2}$', 'c': 'orange', 'at': 0, 'fs': 46}, {'m': r'$AB \neq BA$', 'c': 'red', 'box': True, 'at': 2, 'fs': 46}]},
]})

B.insert(LESSON, 'Worked example: an overdamped system', {'t': 'wb', 'h': 'Worked example: complex roots mean oscillation', 'draw': 'ringing', 'split': 0.5, 'steps': [
    {'say': "Now the case students find hardest: complex roots. Take y double prime plus two y prime plus twenty six y equals zero. The characteristic equation r squared plus two r plus twenty six has roots minus one plus or minus five i.",
     'w': [{'m': r"$y'' + 2y' + 26y = 0$", 'at': 1}, {'m': r'$r = \frac{-2 \pm \sqrt{4 - 104}}{2} = -1 \pm 5i$', 'at': 2}]},
    {'say': "We don't want imaginary numbers in a real answer. Euler's formula fixes it. e to the minus one plus five i, times t, splits into e to the minus t times cosine five t plus i sine five t. The real and imaginary parts are both real solutions.",
     'w': [{'m': r'$e^{(-1+5i)t} = e^{-t}(\cos 5t + i\sin 5t)$', 'at': 1, 'fs': 36},
           {'m': r'$y = e^{-t}\,(c_1\cos 5t + c_2\sin 5t)$', 'c': 'blue', 'box': True, 'at': 2}]},
    {'say': "So the rule is simple. For roots alpha plus or minus i beta, the solution is e to the alpha t, times a cosine and a sine at frequency beta. Starting at one, at rest, gives c one equals one and c two equals one fifth.",
     'w': [{'m': r'$\alpha \pm i\beta \;\to\; e^{\alpha t}(c_1\cos\beta t + c_2\sin\beta t)$', 'c': 'purple', 'at': 1, 'fs': 36},
           {'m': r'$y(0)=1,\ y^\prime(0)=0:\ \ c_1 = 1,\ c_2 = \frac{1}{5}$', 'at': 2}, {'d': 1, 'at': 2}]},
    {'say': "Look at the graph. The real part, minus one, sets the shrinking envelope. The imaginary part, five, sets how fast it rings. That's an underdamped spring, or an R L C circuit ringing after a switch closes.",
     'w': [{'d': 2, 'at': 1}, {'m': 'α: decay rate     β: ringing frequency', 'c': 'orange', 'at': 3}]},
]})

G = 'Worked example: the integrating factor'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r"(e^{2t}\,y)'", 'c': 'red', 'at': 1})
G = 'Matrix multiplication: row times column'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'top-left: $1(0) + 2(1) = 2$', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': r'$AB \neq BA$', 'c': 'red', 'at': 3})
G = 'Worked example: complex roots mean oscillation'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': r'-1 \pm 5i$', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': r'$\alpha \pm i\beta', 'c': 'purple', 'at': 1})
