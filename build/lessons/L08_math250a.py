import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def hill(x, y): return 3 * np.exp(-((x - 0.5) ** 2 + (y - 0.3) ** 2) / 1.2) + 1.6 * np.exp(-((x + 1.3) ** 2 + (y + 1.0) ** 2) / 0.6)

def _fig3d(w, h):
    fig = plt.figure(figsize=(w * 0.8 / 100, h * 0.8 / 100), dpi=100); return fig

def fig_surface(path, w, h):
    fig = _fig3d(w, h)
    a1 = fig.add_subplot(1, 2, 1, projection='3d'); a2 = fig.add_subplot(1, 2, 2)
    x = X(-3, 3, 80); Xg, Yg = np.meshgrid(x, x); Z = hill(Xg, Yg)
    a1.plot_surface(Xg, Yg, Z, cmap='viridis', linewidth=0, alpha=0.95); a1.set_title('surface  z = f(x, y)', fontsize=20); a1.set_zticks([])
    cs = a2.contour(Xg, Yg, Z, levels=10, cmap='viridis', linewidths=2.2); a2.set_aspect('equal'); a2.set_title('contour map (top view)', fontsize=20)
    a2.clabel(cs, fontsize=12, fmt='%.1f')
    save(fig, path)

def fig_dot(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    o = (14, 10)
    arrow(ax, o, (o[0] + 70, o[1]), color=C['blue'], lw=4); txt(ax, o[0] + 72, o[1], 'b', 26, C['blue'], ha='left', bold=True)
    th = np.radians(40); a = (o[0] + 55 * np.cos(th), o[1] + 55 * np.sin(th))
    arrow(ax, o, a, color=C['orange'], lw=4); txt(ax, a[0] + 1, a[1] + 2, 'a', 26, C['orange'], bold=True)
    line(ax, [a, (a[0], o[1])], C['gray'], 2, ls='--'); line(ax, [(o[0], o[1] - 3), (a[0], o[1] - 3)], C['green'], 5)
    txt(ax, (o[0] + a[0]) / 2, o[1] - 7, 'projection of a onto b = |a| cos θ', 19, C['green'], bold=True)
    ax.add_patch(Arc(o, 18, 18, theta1=0, theta2=40, color=C['ink'], lw=2)); txt(ax, o[0] + 12, o[1] + 4, 'θ', 22)
    txt(ax, 50, 56, 'a · b = |a| |b| cos θ = a₁b₁ + a₂b₂ + a₃b₃', 24, bold=True)
    save(fig, path)

def fig_cross(path, w, h):
    fig = _fig3d(w, h); ax = fig.add_subplot(projection='3d')
    a = np.array([2, 0.3, 0]); b = np.array([0.5, 1.8, 0]); c = np.cross(a, b)
    for v, col, lab in ((a, C['blue'], 'a'), (b, C['orange'], 'b'), (c / 1.5, C['green'], 'a × b')):
        ax.quiver(0, 0, 0, *v, color=col, linewidth=4, arrow_length_ratio=0.12); ax.text(*(v * 1.08), lab, fontsize=22, color=col, fontweight='bold')
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    P = np.array([[0, 0, 0], a, a + b, b]); ax.add_collection3d(Poly3DCollection([P], alpha=0.25, facecolor=C['lpurple']))
    ax.set_xlim(0, 2.5); ax.set_ylim(0, 2.5); ax.set_zlim(0, 2.5); ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_title('a × b is perpendicular to both;\nits length = area of the parallelogram', fontsize=20)
    save(fig, path)

def fig_partial(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2)
    x = X(-1, 3, 200)
    a1.plot(x, x ** 2 * 2 + 6, color=C['blue']); a1.plot(x, 8 + 4 * (x - 1), color=C['orange'], lw=2.4); soliddot(a1, 1, 8, C['orange'])
    a1.set_title('slice y = 2:  f = 2x² + 6\nslope f_x = 4 at x = 1', fontsize=18); a1.set_xlabel('x'); a1.set_ylim(0, 25)
    y = X(-1, 4, 200)
    a2.plot(y, y * 1 + 3 * y, color=C['green']); a2.plot(y, 8 + 4 * (y - 2), color=C['orange'], lw=2.4, ls='--'); soliddot(a2, 2, 8, C['orange'])
    a2.set_title('slice x = 1:  f = 4y\nslope f_y = 4', fontsize=18); a2.set_xlabel('y')
    fig.subplots_adjust(wspace=0.3)
    save(fig, path)

def fig_gradient(path, w, h):
    fig, ax = plot(w, h, grid=False)
    x = X(-3, 3, 200); Xg, Yg = np.meshgrid(x, x); Z = hill(Xg, Yg)
    ax.contour(Xg, Yg, Z, levels=12, cmap='viridis', linewidths=1.8)
    xs = X(-2.6, 2.6, 13); Xq, Yq = np.meshgrid(xs, xs); e = 1e-4
    gx = (hill(Xq + e, Yq) - hill(Xq - e, Yq)) / (2 * e); gy = (hill(Xq, Yq + e) - hill(Xq, Yq - e)) / (2 * e)
    ax.quiver(Xq, Yq, gx, gy, color=C['red'], scale=18, width=0.004)
    ax.set_aspect('equal'); ax.set_title('∇f (red) points uphill, perpendicular to contours', fontsize=20)
    save(fig, path)

def fig_gd(path, w, h):
    fig, ax = plot(w, h, grid=False)
    x = X(-3, 3, 200); Xg, Yg = np.meshgrid(x, x); Z = Xg ** 2 + 3 * Yg ** 2
    ax.contour(Xg, Yg, Z, levels=14, cmap='Blues', linewidths=1.6)
    p = np.array([2.6, 1.6]); path_ = [p.copy()]
    for _ in range(14): p = p - 0.12 * np.array([2 * p[0], 6 * p[1]]); path_.append(p.copy())
    P = np.array(path_); ax.plot(P[:, 0], P[:, 1], 'o-', color=C['orange'], lw=2.6, ms=7)
    ax.set_aspect('equal'); ax.set_title('gradient descent on f = x² + 3y²:   step ← −η ∇f', fontsize=19)
    note(ax, -2.9, -2.6, 'machine learning trains models\nexactly like this (millions of variables)', fs=17)
    save(fig, path)

def fig_saddle(path, w, h):
    fig = _fig3d(w, h)
    x = X(-1.5, 1.5, 60); Xg, Yg = np.meshgrid(x, x)
    for i, (Z, t) in enumerate(((-(Xg ** 2 + Yg ** 2), 'maximum'), (Xg ** 2 + Yg ** 2, 'minimum'), (Xg ** 2 - Yg ** 2, 'saddle'))):
        a = fig.add_subplot(1, 3, i + 1, projection='3d'); a.plot_surface(Xg, Yg, Z, cmap='coolwarm', linewidth=0)
        a.set_title(t, fontsize=21); a.set_xticks([]); a.set_yticks([]); a.set_zticks([])
    save(fig, path)

def fig_lagrange(path, w, h):
    fig, ax = plot(w, h, grid=False)
    x = X(0.1, 10, 300); Xg, Yg = np.meshgrid(x, x); Z = Xg * Yg
    cs = ax.contour(Xg, Yg, Z, levels=[5, 10, 16, 25, 36, 49], cmap='viridis', linewidths=2); ax.clabel(cs, fontsize=13)
    ax.plot(x, 10 - x, color=C['red'], lw=3.5, label='constraint x + y = 10')
    soliddot(ax, 5, 5, C['orange'], 14); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect('equal'); ax.legend(loc='upper right')
    note(ax, 5.3, 5.6, 'best: (5, 5), area 25\ncontour just touches\nthe constraint', C['orange'], 17)
    ax.set_title('maximize xy subject to x + y = 10:  ∇f = λ∇g', fontsize=19)
    save(fig, path)

def fig_double(path, w, h):
    fig = _fig3d(w, h); ax = fig.add_subplot(projection='3d')
    n = 8; xs = X(0, 2, n + 1)[:-1]; ys = X(0, 1, n + 1)[:-1]; dx, dy = 2 / n, 1 / n
    Xg, Yg = np.meshgrid(xs, ys); Xf, Yf = Xg.ravel(), Yg.ravel(); Zf = (Xf + dx / 2) + (Yf + dy / 2)
    ax.bar3d(Xf, Yf, 0 * Zf, dx, dy, Zf, color=C['lblue'], edgecolor=C['blue'], alpha=0.9, linewidth=0.4)
    ax.set_title('volume under z = x + y over [0,2]×[0,1] = 3', fontsize=20); ax.set_xlabel('x', labelpad=18); ax.set_ylabel('y', labelpad=22)
    save(fig, path)

def fig_polar(path, w, h):
    fig, ax = plot(w, h, grid=False); ax.set_aspect('equal')
    for r in (0.6, 0.8): ax.add_patch(Circle((0, 0), r, fc='none', ec=C['gray'], lw=1))
    t1, t2 = np.radians(25), np.radians(40)
    th = X(t1, t2, 30)
    ax.fill(np.concatenate([0.6 * np.cos(th), 0.8 * np.cos(th[::-1])]), np.concatenate([0.6 * np.sin(th), 0.8 * np.sin(th[::-1])]), color=C['orange'], alpha=0.8)
    for t in (t1, t2): ax.plot([0, 1.0 * np.cos(t)], [0, 1.0 * np.sin(t)], color=C['gray'], lw=1)
    ax.text(0.83, 0.38, 'dA = r dr dθ', fontsize=22, color=C['orange'], fontweight='bold')
    ax.set_xlim(-0.1, 1.4); ax.set_ylim(-0.1, 1.0); ax.axis('off')
    ax.set_title(r'$\iint e^{-(x^2+y^2)}dA = \int_0^{2\pi}\int_0^\infty e^{-r^2} r\,dr\,d\theta = \pi$', fontsize=20)
    save(fig, path)

def fig_fields(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, grid=False)
    x = X(-2, 2, 13); Xg, Yg = np.meshgrid(x, x); R = np.sqrt(Xg ** 2 + Yg ** 2) + 0.3
    a1.quiver(Xg, Yg, Xg / R ** 2, Yg / R ** 2, color=C['red']); a1.add_patch(Circle((0, 0), 0.18, color=C['red'])); a1.set_title('divergence: a source\n(field of a + charge)', fontsize=19)
    a2.quiver(Xg, Yg, -Yg / R, Xg / R, color=C['blue']); a2.set_title('curl: rotation\n(magnetic field around a wire)', fontsize=19)
    for a in (a1, a2): a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([])
    save(fig, path)

def fig_theorems(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    rows = [('Fundamental Thm (1D)', '∫ₐᵇ f′ dx = f(b) − f(a)', 'ends of an interval'), ('Green (2D)', '∬ curl F dA = ∮ F·dr', 'boundary curve of a region'),
            ('Stokes (3D surface)', '∬ (∇×F)·dS = ∮ F·dr', 'edge of a surface'), ('Divergence (Gauss)', '∭ ∇·F dV = ∯ F·dS', 'skin of a solid')]
    table(ax, 1, H - 2, ['theorem', 'statement', 'inside ⇄ boundary'], rows, [28, 38, 32], 9, 16)
    txt(ax, 50, 6, 'All say: the total “change” inside = what crosses the boundary', 20, C['blue'], bold=True)
    save(fig, path)

LESSON = {
 'code': 'MATH 250A', 'title': 'Calculus III', 'tag': 'Year 2 · Foundations', 'folder': 'MATH-250A Calculus III',
 'slides': [
 {'t': 'title', 'h': 'Calculus III', 'sub': 'Multivariable and vector calculus: surfaces, gradients, multiple integrals and fields', 'img': 'a:topo_relief',
  'say': "Welcome to Calculus three. So far, our functions have had one input. But the real world has three dimensions, and quantities like temperature, air pressure and electric field vary from point to point in space. This course extends calculus to many variables. You'll learn to see a function of two variables as a landscape, find the steepest direction uphill, add up quantities over areas and volumes, and describe fields that fill space. It's the language you'll need for electricity and magnetism, and, surprisingly, for machine learning."},

 {'t': 'v', 'h': 'Vectors in 3D: the dot product', 'img': 'fig:dot',
  'pts': ['a·b = a₁b₁ + a₂b₂ + a₃b₃ = |a||b| cos θ', 'Zero → perpendicular', '(1,2,2)·(2,0,1) = 4 → θ ≈ 53.4°', '3D graphics: brightness = normal · light direction'],
  'say': ["Vectors now have three components. The dot product multiplies matching components and adds them. Geometrically, it equals the lengths times the cosine of the angle between them.",
          "So if the dot product is zero, the vectors are perpendicular. It also gives the projection: how much of one vector points along another.",
          "Example: one, two, two dotted with two, zero, one is two plus zero plus two, which is four. The lengths are three and root five, so the cosine of the angle is four over three root five, about point six, and the angle is about fifty three degrees.",
          "Every video game uses this billions of times per second. The brightness of a surface depends on the dot product between its normal vector and the direction to the light. Facing the light, it's bright. Turned edge on, the dot product is zero, and it's dark."]},

 {'t': 'v', 'h': 'The cross product: a perpendicular vector', 'img': 'fig:cross',
  'pts': ['a × b is perpendicular to both a and b', 'Length = |a||b| sin θ = parallelogram area', 'Direction: right-hand rule', 'Torque τ = r × F · surface normals in graphics'],
  'say': "The cross product of two 3D vectors produces a third vector perpendicular to both. Its length equals the area of the parallelogram they span, and its direction follows the right hand rule: curl your fingers from a to b, and your thumb points along a cross b. For example, x hat cross y hat is z hat. Torque from mechanics is really a cross product: r cross F. In 3D graphics, the normal vector of each triangle in a model is the cross product of two of its edges. And in electromagnetism, the force on a moving charge is q v cross B. Same operation, everywhere."},

 {'t': 'v', 'h': 'Functions of two variables: landscapes', 'img': ['a:topo_relief', 'fig:surface'],
  'pts': ['z = f(x, y) is a surface', 'Contour lines: points with equal height', 'Like a topographic hiking map'],
  'say': ["A function of two variables, z equals f of x and y, assigns a height to every point on a map. Its graph is a surface, a landscape of hills and valleys.",
          "We can draw it two ways. As a 3D surface, on the left. Or as a contour map, on the right, where each curve connects points with the same height. That's exactly a topographic hiking map: contour lines packed close together mean steep terrain, and lines spread apart mean gentle slopes. Weather maps draw temperature and pressure the same way."]},

 {'t': 'v', 'h': 'Partial derivatives: slope in one direction', 'img': 'fig:partial',
  'pts': ['∂f/∂x: change x, hold y fixed', '∂f/∂y: change y, hold x fixed', 'f = x²y + 3y → f_x = 2xy, f_y = x² + 3', 'At (1, 2): f_x = 4, f_y = 4'],
  'say': ["On a landscape, the slope depends on which direction you walk. A partial derivative measures the slope in one coordinate direction. The partial with respect to x: change x, and treat y as a constant.",
          "The partial with respect to y: change y, and treat x as a constant.",
          "Example: f equals x squared y plus three y. With respect to x, y is just a constant, so the derivative is two x y. With respect to y, x squared is a constant multiplier, so it's x squared plus three.",
          "At the point one, two, both partials equal four. All the single variable rules still work. You just have to be disciplined about which variables you're holding still."]},

 {'t': 'v', 'h': 'The gradient: which way is uphill?', 'img': 'fig:gradient',
  'pts': ['∇f = (∂f/∂x, ∂f/∂y)', 'Points in the direction of steepest ascent', 'Its length = the steepest slope', 'Always perpendicular to contour lines'],
  'say': ["Collect the partial derivatives into a vector, and you get the gradient, written with an upside down triangle called nabla.",
          "Here's the key fact: the gradient points in the direction of steepest ascent. If you're standing on a hillside in the fog, the gradient tells you which way is straight uphill.",
          "Its length tells you how steep that steepest direction is. The slope in any other direction, called the directional derivative, is the gradient dotted with a unit vector in that direction.",
          "And the gradient is always perpendicular to the contour lines. Look at the red arrows. They cross every contour at a right angle, pointing toward the peaks. Water flows in the opposite direction, straight downhill, which is why streams cross contour lines at right angles on a topographic map."]},

 {'t': 'v', 'h': 'Gradient descent: how machines learn', 'img': 'fig:gd',
  'pts': ['Want the minimum of an error function?', 'Step opposite the gradient: x ← x − η∇f', 'Repeat until the slope is ~0', 'Neural networks: the same idea with billions of variables'],
  'say': ["Now an application that runs much of modern technology. Suppose you want the lowest point of a function, like the error of a prediction model.",
          "Start anywhere, compute the gradient, and take a small step in the opposite direction, downhill. The step size, eta, is called the learning rate.",
          "Repeat. Here, on the bowl f equals x squared plus three y squared, the orange path zigzags down into the minimum at the center. It zigzags because the bowl is steeper in y than in x.",
          "This is gradient descent, and it's how neural networks are trained. The error is a function of millions or billions of parameters, the gradient is computed with the chain rule, and the computer takes millions of small downhill steps. Every image recognizer and language model you've used was trained this way, using exactly this Calculus three idea."]},

 {'t': 'v', 'h': 'Finding maxima and minima', 'img': ['fig:saddle', 'fig:lagrange'],
  'pts': ['Critical point: ∇f = 0', 'Second-derivative test: max, min, or saddle', 'With a constraint g = c: ∇f = λ∇g (Lagrange)', 'Max xy with x + y = 10 → x = y = 5'],
  'say': ["To find peaks and valleys, look for critical points where the gradient is zero: the surface is flat in every direction. But flat doesn't always mean a peak or a valley. Look at the third surface. It's a saddle: it curves up in one direction and down in the other, like a mountain pass. A second derivative test, using all the second partial derivatives, tells the three cases apart.",
          "Often you're optimizing with a constraint. Maximize the area x y of a rectangle, given that x plus y must equal ten, say because you have twenty meters of fence. Lagrange's insight: at the best point, the contour line of f just touches the constraint curve, so their gradients are parallel. Gradient of f equals lambda times gradient of g. Solving gives x equals y equals five, a square, with area twenty five. Engineers use this to maximize performance subject to power, cost or size limits."]},

 {'t': 'v', 'h': 'Double integrals: volume under a surface', 'img': 'fig:double',
  'pts': ['∬ f dA adds f over an area', 'Compute as two nested single integrals', '∫₀² ∫₀¹ (x + y) dy dx = ∫₀² (x + ½) dx = 3', 'Mass from density, total charge, average temperature'],
  'say': ["A double integral adds up a function over a two dimensional region, just like a single integral adds up over an interval. Geometrically, it's the volume under the surface, made of thin columns, like these bars.",
          "You compute it as two nested single integrals: integrate over y with x held fixed, then integrate the result over x.",
          "Example: x plus y over the rectangle from zero to two in x and zero to one in y. The inner integral over y gives x plus one half. Then integrate from zero to two: two plus one, which is three. When the region isn't a rectangle, the inner limits become functions of the outer variable. Over the triangle under the line y equals x, for example, y runs from zero up to x, and then x runs over its range. Always draw the region first, then read the limits off the picture.",
          "Double integrals compute total mass from a density, total charge on a surface, the average temperature over a chip, or the probability that two random variables land in a region, which you'll do in the statistics course."]},

 {'t': 'v', 'h': 'Change of coordinates: polar, cylindrical, spherical', 'img': 'fig:polar',
  'pts': ['Polar: dA = r dr dθ (the extra r matters!)', 'Gaussian integral: ∫ e^(−x²) dx = √π', 'Spherical: dV = ρ² sin φ dρ dφ dθ', 'Sphere volume (4/3)πr³ falls right out'],
  'say': ["Circular regions are painful in x and y, so we switch coordinates. In polar coordinates, a tiny area element is r d r d theta. That extra r is crucial: the little patches get bigger as you move outward.",
          "Here's a famous trick. The integral of e to the minus x squared has no antiderivative. But square it, turning it into a double integral over the whole plane, and switch to polar. The extra r makes it easy: the answer is pi. Take the square root, and the integral of e to the minus x squared is root pi. That's why root pi appears in the normal distribution's formula.",
          "In three dimensions, cylindrical and spherical coordinates do the same job, with their own volume elements. In spherical coordinates, it's rho squared sine phi.",
          "Integrate one over a ball in spherical coordinates, and the volume of a sphere, four thirds pi r cubed, falls right out in a couple of lines."]},

 {'t': 'v', 'h': 'Vector fields, divergence and curl', 'img': 'fig:fields',
  'pts': ['Vector field: an arrow at every point (wind, E, B)', 'Divergence ∇·F: is stuff flowing out? (sources)', 'Curl ∇×F: is it swirling? (rotation)', 'Maxwell’s equations are written with these'],
  'say': ["A vector field attaches an arrow to every point in space: wind velocity on a weather map, water flow in a pipe, the electric field around a charge.",
          "Divergence measures whether a field is spreading out from a point, like the electric field of a positive charge on the left. A positive divergence means a source. Negative means a sink.",
          "Curl measures how much the field swirls around a point, like the magnetic field circling a wire carrying current, on the right.",
          "These aren't abstract. Maxwell's equations, the four equations of electricity and magnetism, say: the divergence of E is proportional to charge density, the divergence of B is zero, the curl of E comes from a changing magnetic field, and the curl of B comes from current and a changing electric field. You'll meet them next year in physics."]},

 {'t': 'v', 'h': 'Line integrals and the big theorems', 'img': 'fig:theorems',
  'pts': ['Line integral ∫ F·dr: work along a path', 'Conservative fields: only the endpoints matter', 'Green, Stokes, Divergence: inside ⇄ boundary', 'All are cousins of the Fundamental Theorem'],
  'say': ["A line integral adds up a field along a path. The work done moving through a force field is the integral of F dot d r along the path.",
          "For conservative fields, like gravity, the work depends only on the starting and ending points, not on the route. That's exactly why we can define potential energy, and in circuits, voltage.",
          "Then come the three great theorems of vector calculus. Green's theorem, Stokes' theorem and the divergence theorem all say the same thing in different dimensions: adding up a derivative over the inside of a region equals adding up the field over its boundary.",
          "Look at the first row: the fundamental theorem of calculus is the one dimensional version, where the boundary of an interval is just its two endpoints. The divergence theorem is what turns Maxwell's equations into Gauss's law, which says the electric flux out of any closed surface equals the charge inside. It's one beautiful idea, from Calculus one all the way to electromagnetism."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'The **gradient** points uphill. **Multiple integrals** add up over areas and volumes. **Divergence & curl** describe fields — the language of E&M.',
  'cap': 'Next: MATH 250B, Linear Algebra and Differential Equations.',
  'say': "To recap. Dot and cross products measure angles, projections, areas and perpendicular directions. Functions of two variables are landscapes, partial derivatives measure slopes along each axis, and the gradient points straight uphill, which is the engine of machine learning. Critical points and Lagrange multipliers find the best designs. Double and triple integrals add up quantities over regions, often in polar or spherical coordinates. And vector fields, with divergence, curl and the big theorems, are the language of electricity and magnetism. Next, linear algebra and differential equations. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B

def draw_para(ax, n, w, h):
    O = (110, 170); A = (520, 230); Bv = (300, 420)
    if n >= 1:
        B.arr(ax, *O, *A, 'blue', 4); B.lab(ax, A[0] + 20, A[1] - 20, 'a', 38, 'blue', ha='left')
        B.arr(ax, *O, *Bv, 'green', 4); B.lab(ax, Bv[0] - 20, Bv[1] + 20, 'b', 38, 'green', ha='right')
    if n >= 2:
        B.poly(ax, [O, A, (A[0] + Bv[0] - O[0], A[1] + Bv[1] - O[1]), Bv], fc='#f6d6c4', c='orange', lw=2, alpha=0.8)
        B.lab(ax, 400, 340, 'area = |a × b|', 30, 'red')
    if n >= 3:
        B.arr(ax, *O, O[0] - 20, O[1] + 520, 'red', 4.5); B.lab(ax, O[0] + 20, O[1] + 500, 'a × b', 34, 'red', ha='left')
        B.lab(ax, O[0] + 30, O[1] + 440, '⊥ to both', 28, 'red', ha='left')

def draw_saddle(ax, n, w, h):
    X0, Y0, sx, sy = w / 2, h / 2, 170, 70
    P = lambda x, y: (X0 + x * sx, Y0 + y * sy)
    if n >= 1:
        B.arr(ax, X0 - 2.3 * sx, Y0, X0 + 2.3 * sx, Y0, 'gray', 2.5, 22); B.arr(ax, X0, Y0 - 4.5 * sy, X0, Y0 + 4.5 * sy, 'gray', 2.5, 22)
        xs = np.linspace(-2.1, 2.1, 120); B.ln(ax, *zip(*[P(a, a ** 3 - 3 * a) for a in xs]), c='blue', lw=3.5)
        B.lab(ax, X0 + 2.2 * sx, Y0 - 30, 'x', 30, 'gray'); B.lab(ax, *P(-2.1, -3.9), 'slice y = 0:  x³ − 3x', 28, 'blue', ha='left')
    if n >= 2:
        B.dot(ax, *P(1, -2), c='green', s=15); B.lab(ax, *P(1.1, -2.9), '(1, 0): minimum', 30, 'green', ha='left')
    if n >= 3:
        B.dot(ax, *P(-1, 2), c='red', s=15); B.lab(ax, *P(-1.2, 2.9), '(−1, 0): saddle', 30, 'red', ha='center')

def draw_disk(ax, n, w, h):
    cx, cy, R = w / 2, h / 2, 300
    t = np.linspace(0, 2 * np.pi, 200)
    if n >= 1:
        B.poly(ax, list(zip(cx + R * np.cos(t), cy + R * np.sin(t))), fc='#dfe8f7', c='blue', lw=3)
        B.arr(ax, cx, cy, cx + R, cy, 'ink', 2.5, 20); B.lab(ax, cx + R / 2, cy - 28, 'r = 2', 30)
    if n >= 2:
        r1, r2, a1, a2 = 170, 215, np.radians(35), np.radians(55)
        tt = np.linspace(a1, a2, 20)
        pts = list(zip(cx + r1 * np.cos(tt), cy + r1 * np.sin(tt))) + list(zip(cx + r2 * np.cos(tt[::-1]), cy + r2 * np.sin(tt[::-1])))
        B.poly(ax, pts, fc='#f6d6c4', c='red', lw=3)
        B.lab(ax, cx - 40, cy + 230, 'dA = r dr dθ', 30, 'red', bbox=dict(fc='white', ec='none', pad=2))
        B.lab(ax, cx + 120 * np.cos(np.radians(30)), cy + 120 * np.sin(np.radians(30)) - 10, 'thicker\nfarther out', 22, 'gray')

def draw_gd(ax, n, w, h):
    cx, cy, s = w * 0.35, h * 0.38, 210
    t = np.linspace(0, 2 * np.pi, 200)
    if n >= 1:
        for c in (0.5, 1.7, 3.04, 7):
            B.ln(ax, cx + s * np.sqrt(c) * np.cos(t), cy + s * np.sqrt(c / 3) * np.sin(t), c='gray', lw=1.8)
        B.dot(ax, cx, cy, c='green', s=12); B.lab(ax, cx, cy - 30, 'min', 26, 'green')
    pts = [(2, 1), (1.6, 0.4), (1.28, 0.16)]
    for k, (x, y) in enumerate(pts):
        if n >= k + 2:
            B.dot(ax, cx + s * x, cy + s * y, c='red', s=13)
            if k: B.arr(ax, cx + s * pts[k - 1][0], cy + s * pts[k - 1][1], cx + s * x, cy + s * y, 'red', 3)
            B.lab(ax, cx + s * x - 22, cy + s * y + (30 if k == 0 else -34), f'({x}, {y})', 26, 'red', ha='right', bbox=dict(fc='white', ec='none', pad=1))

B.insert(LESSON, 'Vectors in 3D: the dot product', {'t': 'wb', 'h': 'Worked example: the angle between two vectors', 'steps': [
    {'say': "Let's compute an angle with the dot product, start to finish. Take a equals three, four, zero, and b equals four, zero, three. Step one: multiply matching components and add. Three times four, plus four times zero, plus zero times three, is twelve.",
     'w': [{'m': r'$\vec a = (3,4,0)$,    $\vec b = (4,0,3)$', 'at': 1}, {'m': r'$\vec a\cdot\vec b = 3(4) + 4(0) + 0(3) = 12$', 'at': 3}]},
    {'say': "Step two: the lengths. The length of a is the square root of nine plus sixteen plus zero, which is five. The length of b is the square root of sixteen plus zero plus nine, also five.",
     'w': [{'m': r'$|\vec a| = \sqrt{9+16+0} = 5$', 'at': 1}, {'m': r'$|\vec b| = \sqrt{16+0+9} = 5$', 'at': 2}]},
    {'say': "Step three: the dot product equals the product of the lengths times cosine of the angle. So cosine theta is twelve over twenty five, point four eight. The inverse cosine gives about sixty one point three degrees. A positive dot product means the angle is less than ninety degrees: the vectors point roughly the same way.",
     'w': [r'$\cos\theta = \frac{\vec a\cdot\vec b}{|\vec a||\vec b|} = \frac{12}{25} = 0.48$', {'m': r'$\theta = \cos^{-1}(0.48) \approx 61.3°$', 'c': 'red', 'box': True, 'at': 2}]},
]})

B.insert(LESSON, 'The cross product', {'t': 'wb', 'h': 'Worked example: computing a cross product', 'draw': 'para', 'split': 0.58, 'steps': [
    {'say': "Now a cross product, worked by hand. Take a equals one, zero, two, and b equals zero, three, one. Each component of the cross product uses the other two components, in a crisscross pattern.",
     'w': [{'m': r'$\vec a = (1,0,2)$,    $\vec b = (0,3,1)$', 'at': 1}, {'d': 1, 'at': 1}, {'m': r'$\vec a\times\vec b = (a_2b_3 - a_3b_2,\; a_3b_1 - a_1b_3,\; a_1b_2 - a_2b_1)$', 'at': 2, 'fs': 32}]},
    {'say': "First component: zero times one minus two times three, negative six. Second: two times zero minus one times one, negative one. Third: one times three minus zero times zero, three. So a cross b is negative six, negative one, three.",
     'w': [{'m': r'$x:\ 0(1) - 2(3) = -6$'}, {'m': r'$y:\ 2(0) - 1(1) = -1$', 'at': 1}, {'m': r'$z:\ 1(3) - 0(0) = 3$', 'at': 2}, {'m': r'$\vec a\times\vec b = (-6,\,-1,\,3)$', 'c': 'red', 'box': True, 'at': 3}]},
    {'say': "Always check it: the result must be perpendicular to both. Dot it with a: negative six plus zero plus six, zero. Dot it with b: zero minus three plus three, zero. Both zero, so it's correct. And its length, the square root of forty six, about six point seven eight, is the area of the parallelogram the two vectors span.",
     'w': [{'d': 3}, {'m': r'check: $(-6,-1,3)\cdot\vec a = -6+0+6 = 0$', 'at': 1, 'fs': 36}, {'m': r'$(-6,-1,3)\cdot\vec b = 0-3+3 = 0$', 'at': 2, 'fs': 36}, {'d': 2, 'at': 4}, {'m': r'area $= \sqrt{36+1+9} = \sqrt{46} \approx 6.78$', 'at': 4, 'fs': 36}]},
]})

B.insert(LESSON, 'Finding maxima and minima', {'t': 'wb', 'h': 'Worked example: minimum or saddle?', 'draw': 'saddle', 'split': 0.52, 'steps': [
    {'say': "Let's classify the critical points of f equals x cubed minus three x plus y squared. Step one: set both partial derivatives to zero. f x is three x squared minus three, which is zero at x equals plus or minus one. f y is two y, zero at y equals zero. So there are two critical points: one comma zero, and negative one comma zero.",
     'w': [r'$f(x,y) = x^3 - 3x + y^2$', {'m': r'$f_x = 3x^2 - 3 = 0 \;\Rightarrow\; x = \pm 1$', 'at': 2}, {'m': r'$f_y = 2y = 0 \;\Rightarrow\; y = 0$', 'at': 3}, {'d': 1, 'at': 4}]},
    {'say': "Step two: the second derivative test. Compute D equals f x x times f y y, minus f x y squared. Here f x x is six x, f y y is two, and f x y is zero. So D equals twelve x.",
     'w': [r'$D = f_{xx}f_{yy} - f_{xy}^2$', {'m': r'$= (6x)(2) - 0^2 = 12x$', 'at': 2}]},
    {'say': "At one comma zero, D is twelve, positive, and f x x is six, positive. So it's a local minimum, with value negative two.",
     'w': [{'m': r"$(1,0)$:  $D = 12 > 0$, $f_{xx} > 0$  so it's a minimum", 'c': 'green'}, {'d': 2, 'at': 1}]},
    {'say': "At negative one comma zero, D is negative twelve. A negative D means a saddle point: it's a peak if you walk along x, but a valley if you walk along y, like a horse's saddle. Gradient descent can stall near saddles like this, which is a real problem when training neural networks.",
     'w': [{'m': r"$(-1,0)$:  $D = -12 < 0$  so it's a saddle", 'c': 'red'}, {'d': 3, 'at': 1}]},
]})

B.insert(LESSON, 'Change of coordinates', {'t': 'wb', 'h': 'Worked example: a double integral in polar coordinates', 'draw': 'disk', 'split': 0.56, 'steps': [
    {'say': "Here's why polar coordinates are worth it. Integrate x squared plus y squared over a disk of radius two. In x and y, the limits are square roots and the algebra gets ugly. In polar, x squared plus y squared is just r squared, and the disk is simply r from zero to two, theta from zero to two pi.",
     'w': [{'m': r'$\iint_{disk} (x^2 + y^2)\,dA$', 'at': 1}, {'d': 1, 'at': 1}, {'m': r'$x^2 + y^2 = r^2$', 'at': 3}]},
    {'say': "Don't forget the extra r: a little patch of area is r d r d theta, because patches farther from the center are wider. So the integrand becomes r squared times r, r cubed.",
     'w': [{'d': 2}, {'m': r'$dA = r\,dr\,d\theta$', 'at': 0}, {'m': r'$= \int_0^{2\pi}\int_0^2 r^2 \cdot r\;dr\,d\theta$', 'at': 2}]},
    {'say': "The inner integral of r cubed is r to the fourth over four, which from zero to two is four. The outer integral of four, over a full turn, is four times two pi. Eight pi, about twenty five point one. Two short lines, instead of a page of square roots.",
     'w': [r'$\int_0^2 r^3\,dr = \frac{2^4}{4} = 4$', {'m': r'$\int_0^{2\pi} 4\;d\theta = 8\pi \approx 25.1$', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Gradient descent', {'t': 'wb', 'h': 'Worked example: two steps of gradient descent', 'draw': 'gd', 'split': 0.5, 'steps': [
    {'say': "Let's run gradient descent by hand on f equals x squared plus three y squared. Its minimum is obviously at the origin, so we can watch the algorithm find it. The gradient is two x, six y. Start at two comma one, with a learning rate of point one.",
     'w': [{'m': r'$f = x^2 + 3y^2$', 'at': 0}, {'d': 1, 'at': 1}, {'m': r'$\nabla f = (2x,\ 6y)$', 'at': 2}, {'m': r'start $(2, 1)$,  $\eta = 0.1$,  $f = 7$', 'at': 3}, {'d': 2, 'at': 3}]},
    {'say': "Step one. At two comma one, the gradient is four comma six. Move opposite to it, scaled by point one: two minus point four, and one minus point six. The new point is one point six comma point four, and f has dropped from seven to about three.",
     'w': [r'$\nabla f(2,1) = (4,\ 6)$', {'m': r'$(2,1) - 0.1(4,6) = (1.6,\ 0.4)$', 'at': 2}, {'m': r'$f = 3.04$', 'at': 3}, {'d': 3, 'at': 3}]},
    {'say': "Step two. The gradient at the new point is three point two comma two point four. Subtract a tenth of it: one point two eight comma point one six. Now f is about one point seven. Each step heads downhill, perpendicular to the contour lines. Notice y shrinks faster than x, because the bowl is steeper in y. Training a neural network is exactly this loop, with millions of variables instead of two.",
     'w': [r'$\nabla f(1.6,0.4) = (3.2,\ 2.4)$', {'m': r'$(1.6,0.4) - 0.1(3.2,2.4) = (1.28,\ 0.16)$', 'at': 1, 'fs': 36}, {'m': r'$f \approx 1.72$', 'c': 'red', 'box': True, 'at': 2}, {'d': 4, 'at': 1}]},
]})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Vectors in 3D'
B.spen(LESSON, S, 0, {'fig': [('underline', .5, .84, .115)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .21, .48, .115)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .26, .75, .03, .05)], 'c': 'orange', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('box', .12, .89, .58, .975)], 'c': 'green', 'at': 1})
S = 'The cross product'
B.spen(LESSON, S, 0, {'fig': [('circle', .19, .405, .07, .04)], 'c': 'green', 'at': 0}, {'fig': [('underline', .04, .92, .165)], 'c': 'blue', 'at': 1},
       {'fig': [('arrow', .45, .84, .4, .62)], 'c': 'purple', 'at': 1, 'dt': 3.5})
S = 'Partial derivatives'
B.spen(LESSON, S, 0, {'fig': [('box', .08, .03, .48, .12)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('box', .6, .03, .94, .12)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .28, .615, .03, .04)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .81, .425, .03, .04)], 'c': 'orange', 'at': 0, 'dt': 0.8})
S = 'The gradient'
B.spen(LESSON, S, 1, {'fig': [('arrow', .8, .3, .58, .43)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .55, .45, .06, .08)], 'c': 'red', 'at': 1}, {'fig': [('arrow', .6, .47, .85, .6)], 'c': 'blue', 'at': 3})
S = 'Gradient descent'
B.spen(LESSON, S, 1, {'fig': [('circle', .815, .285, .03, .04)], 'c': 'orange', 'at': 0}, {'fig': [('arrow', .81, .3, .75, .43)], 'c': 'red', 'at': 0, 'dt': 2.0},
       {'fig': [('underline', .7, .96, .09)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .5, .495, .04, .05)], 'c': 'green', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 3, {'fig': [('underline', .14, .79, .875)], 'c': 'purple', 'at': 0})
S = 'Finding maxima'
B.spen(LESSON, S, 0, {'fig': [('circle', .17, .33, .06, .09)], 'c': 'red', 'at': 0}, {'fig': [('circle', .5, .62, .06, .09)], 'c': 'blue', 'at': 0, 'dt': 2.0},
       {'fig': [('box', .68, .08, .99, .9)], 'c': 'purple', 'at': 2}, {'fig': [('underline', .75, .9, .12)], 'c': 'purple', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('underline', .38, .84, .225)], 'c': 'red', 'at': 1}, {'fig': [('box', .51, .31, .91, .46)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .5, .49, .03, .04)], 'c': 'orange', 'at': 4})
S = 'Double integrals'
B.spen(LESSON, S, 0, {'fig': [('underline', .04, .55, .1)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .93, .055, .04, .05)], 'c': 'red', 'at': 2})
S = 'Change of coordinates'
B.spen(LESSON, S, 0, {'fig': [('underline', .61, .89, .62)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .47, .58, .08, .12)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('underline', .18, .82, .13)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .8, .08, .03, .06)], 'c': 'red', 'at': 3})
S = 'Vector fields'
B.spen(LESSON, S, 1, {'fig': [('circle', .23, .57, .04, .07)], 'c': 'red', 'at': 0}, {'fig': [('box', .03, .0, .43, .19)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .7, .58, .1, .2)], 'c': 'blue', 'at': 0})
S = 'Line integrals'
B.spen(LESSON, S, 2, {'fig': [('highlight', .03, .34, .97, .495)], 'c': 'green', 'at': 1, 'dt': 1.0}, {'fig': [('highlight', .03, .5, .97, .65)], 'c': 'green', 'at': 1, 'dt': 2.0},
       {'fig': [('highlight', .03, .665, .97, .82)], 'c': 'green', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 3, {'fig': [('box', .0, .18, 1, .335)], 'c': 'orange', 'at': 0}, {'fig': [('box', .0, .665, 1, .82)], 'c': 'blue', 'at': 1},
       {'fig': [('underline', .04, .96, .935)], 'c': 'blue', 'at': 2})

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
