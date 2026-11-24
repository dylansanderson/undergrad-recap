# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'The Laplace transform: poles decide stability', {'t': 'wb', 'h': 'Worked example: solving a circuit with Laplace', 'steps': [
    {'say': "Let's actually use the Laplace transform, start to finish. An R C circuit with R C equal to one second, starting empty, is hit by a one volt step at time zero. Its equation is v prime plus v equals one.",
     'w': [{'m': r"$v' + v = u(t)$,    $v(0) = 0$", 'at': 2}]},
    {'say': "Step one: transform every term. The derivative becomes s V minus the initial value, which is zero. v becomes capital V. And the unit step becomes one over s. Calculus has turned into algebra.",
     'w': [{'m': r"$\mathcal{L}\{v'\} = sV - v(0)$,   $\mathcal{L}\{u(t)\} = \frac{1}{s}$", 'c': 'gray', 'at': 1},
           {'m': r'$sV + V = \frac{1}{s}$', 'c': 'blue', 'at': 3}]},
    {'say': "Step two: solve for V. V equals one over s times s plus one. Step three: partial fractions, from Calculus two. Plug s equals zero to get A equals one, and s equals minus one to get B equals minus one.",
     'w': [{'m': r'$V(s) = \frac{1}{s(s+1)} = \frac{A}{s} + \frac{B}{s+1}$', 'at': 0}, {'m': r'$A = 1$,   $B = -1$', 'at': 2}]},
    {'say': "Step four: transform back using the table. One over s is a step, one. One over s plus one is e to the minus t. So v of t equals one minus e to the minus t. That's the same charging curve we found with an integrating factor in math two fifty B, and notice the pole at s equals minus one sets the time constant.",
     'w': [{'m': r'$v(t) = 1 - e^{-t}$', 'c': 'red', 'box': True, 'at': 2, 'fs': 52}, {'m': r'pole at $s = -1$  $\to$  $e^{-t}$,  $\tau = 1\ \mathrm{s}$', 'c': 'green', 'at': 3}]},
]})

G = 'Worked example: solving a circuit with Laplace'
B.pen(LESSON, G, 1, {'p': ('box',), 'on': r'$sV + V = \frac{1}{s}$', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': r'pole at $s = -1$', 'c': 'green', 'at': 3})
