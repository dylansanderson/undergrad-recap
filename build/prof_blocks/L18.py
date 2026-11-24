# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Random variables, PDFs and CDFs', {'t': 'wb', 'h': 'Worked example: mean and variance, by hand', 'steps': [
    {'say': "Let's actually compute an expected value, starting with a fair die. Multiply each outcome by its probability and add: one through six, each times one sixth. That's twenty one sixths, three point five.",
     'w': [{'m': r'die:  $E[X] = \sum x\,p(x) = \frac{1+2+3+4+5+6}{6} = 3.5$', 'at': 2}]},
    {'say': "Notice you can never roll a three point five. The expected value is the long run average, the balance point of the distribution, not a value you expect to see on any single roll.",
     'w': [{'m': 'E[X] = long-run average, not a likely outcome', 'c': 'blue', 'at': 0}]},
    {'say': "Now a continuous one: X uniform between zero and two. The density is one half across that range, so the total area is one. The mean is the integral of x times one half, from zero to two: one. Then E of X squared is the integral of x squared times one half: four thirds.",
     'w': [{'m': r'uniform on $[0,2]$:  $f(x) = \frac{1}{2}$', 'at': 1, 'gap': 14},
           {'m': r'$E[X] = \int_0^2 x\cdot\frac{1}{2}\,dx = 1$', 'at': 2}, {'m': r'$E[X^2] = \int_0^2 x^2\cdot\frac{1}{2}\,dx = \frac{4}{3}$', 'at': 3}]},
    {'say': "Variance is E of X squared minus the mean squared: four thirds minus one, one third. The standard deviation is its square root, about point five eight. And one warning: a density can be bigger than one. Uniform on zero to one half has height two. Only areas are probabilities.",
     'w': [{'m': r'$\sigma^2 = \frac{4}{3} - 1^2 = \frac{1}{3}$,   $\sigma \approx 0.58$', 'c': 'green', 'box': True, 'at': 0},
           {'m': r'$f(x)$ can exceed 1:  only AREA is probability', 'c': 'red', 'at': 3}]},
]})

G = 'Worked example: mean and variance, by hand'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': r'= 3.5$', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': r'$f(x)$ can exceed 1', 'c': 'red', 'at': 3})
