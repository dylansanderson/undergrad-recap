# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def _field(ax, cx, cy, s, fn, col):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i == 0 and j == 0: continue
            u, v = fn(i, j); L = max(1e-9, np.hypot(u, v)); k = 34 / L
            B.arr(ax, cx + i * s, cy + j * s, cx + i * s + u * k, cy + j * s + v * k, col, 2.2, 14)
    B.dot(ax, cx, cy, s=8)

def draw_nabla(ax, n, w, h):
    if n >= 1: _field(ax, w * 0.5, h * 0.76, 58, lambda x, y: (x, y), 'blue'); B.lab(ax, w * 0.5, h * 0.76 - 158, 'F = (x, y): spreads out', 26, 'blue')
    if n >= 2: _field(ax, w * 0.5, h * 0.23, 58, lambda x, y: (-y, x), 'orange'); B.lab(ax, w * 0.5, h * 0.23 - 158, 'F = (−y, x): swirls', 26, 'orange')

def draw_paths(ax, n, w, h):
    X0, Y0, s = 90, 90, 520
    P = lambda x, y: (X0 + x * s, Y0 + y * s)
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 1.15 * s, Y0 + 1.15 * s); B.dot(ax, *P(0, 0), s=12); B.dot(ax, *P(1, 1), s=12)
        B.lab(ax, *P(0.05, -0.08), '(0,0)', 24, 'gray', ha='left'); B.lab(ax, *P(1.02, 1.06), '(1,1)', 24, 'gray', ha='left')
    if n >= 2: B.ln(ax, *zip(P(0, 0), P(1, 1)), c='blue', lw=4); B.lab(ax, *P(0.3, 0.5), 'y = x', 28, 'blue')
    if n >= 3:
        t = np.linspace(0, 1, 50); B.ln(ax, *zip(*[P(a, a * a) for a in t]), c='orange', lw=4); B.lab(ax, *P(0.72, 0.28), 'y = x²', 28, 'orange')

B.insert(LESSON, 'Vector fields, divergence and curl', {'t': 'wb', 'h': 'One symbol, three operations: grad, div, curl', 'draw': 'nabla', 'split': 0.6, 'steps': [
    {'say': "The nabla symbol confuses everyone, because it shows up three ways. Think of nabla as a vector of derivative instructions: d by d x, d by d y. What you get depends on what you combine it with. Apply it to a scalar function, and you get the gradient, a vector.",
     'w': [{'m': r'$\nabla = (\frac{\partial}{\partial x},\ \frac{\partial}{\partial y})$', 'at': 1},
           {'m': r'$\nabla f$  : scalar in, VECTOR out  (gradient)', 'c': 'green', 'at': 3}]},
    {'say': "Dot it with a vector field, and you get the divergence, a single number at each point: d P d x plus d Q d y. For the field x comma y, every arrow points outward. The divergence is one plus one, two, positive everywhere: a source.",
     'w': [{'m': r'$\nabla\cdot\vec F = \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y}$ : vector in, NUMBER out', 'c': 'blue', 'at': 0},
           {'d': 1, 'at': 1}, {'m': r'$\vec F = (x,\,y)$:  $1 + 1 = 2 > 0$  source', 'at': 2}]},
    {'say': "Cross it with the field, and you get the curl, which measures rotation. In two dimensions, it's d Q d x minus d P d y. For the field minus y comma x, the arrows circle the origin. The curl is one minus negative one, two, so it swirls counterclockwise. And its divergence? Zero minus zero, zero. Pure rotation, nothing spreading.",
     'w': [{'m': r'curl: $\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}$ : measures rotation', 'c': 'orange', 'at': 0},
           {'d': 2, 'at': 1}, {'m': r'$\vec F = (-y,\,x)$:  curl $= 1 - (-1) = 2$', 'at': 2}, {'m': 'div = 0 − 0 = 0', 'at': 4}]},
]})

B.insert(LESSON, 'Line integrals and the big theorems', {'t': 'wb', 'h': 'Worked example: work along two different paths', 'draw': 'paths', 'split': 0.55, 'steps': [
    {'say': "Let's actually compute a line integral, and see path independence happen. The field is F equals y comma x. We'll move from the origin to the point one comma one, along two different paths.",
     'w': [{'m': r'$\vec F = (y,\ x)$,   $W = \int \vec F\cdot d\vec r$', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "Path one: the straight line y equals x. Write it as r of t equals t comma t, with t from zero to one. Then d r is one comma one, d t, and F along the path is t comma t. The dot product is two t. Integrate from zero to one: one.",
     'w': [{'d': 2, 'at': 1}, {'m': r'$\vec r = (t,t)$,  $d\vec r = (1,1)\,dt$', 'at': 2}, {'m': r'$\int_0^1 (t,t)\cdot(1,1)\,dt = \int_0^1 2t\,dt = 1$', 'c': 'blue', 'at': 4}]},
    {'say': "Path two: the parabola y equals x squared. r of t is t comma t squared, so d r is one comma two t, d t. F along it is t squared comma t. The dot product is t squared plus two t squared, three t squared. Integrate: again exactly one.",
     'w': [{'d': 3, 'at': 0}, {'m': r'$\vec r = (t,t^2)$,  $d\vec r = (1,2t)\,dt$', 'at': 1}, {'m': r'$\int_0^1 (t^2 + 2t^2)\,dt = \int_0^1 3t^2\,dt = 1$', 'c': 'orange', 'at': 4}]},
    {'say': "Same answer, different paths. That's because this field is conservative: it's the gradient of f equals x y. So the work is just f at the end minus f at the start, one minus zero. That's the fundamental theorem of calculus again, and it's exactly why voltage is well defined in circuits.",
     'w': [{'m': r'$\vec F = \nabla(xy)$  so  $W = f(1,1) - f(0,0) = 1$', 'c': 'red', 'box': True, 'at': 2}]},
]})

G = 'One symbol, three operations: grad, div, curl'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'scalar in, VECTOR out', 'c': 'green', 'at': 3})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '1 + 1 = 2', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'curl $= 1 - (-1) = 2$', 'c': 'orange', 'at': 2})
G = 'Worked example: work along two different paths'
B.pen(LESSON, G, 3, {'p': ('check',), 'on': r'\int_0^1 2t\,dt = 1', 'at': 0}, {'p': ('check',), 'on': r'\int_0^1 3t^2\,dt = 1', 'at': 0, 'dt': 0.6})
