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
