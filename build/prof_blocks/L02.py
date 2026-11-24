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
