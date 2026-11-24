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
