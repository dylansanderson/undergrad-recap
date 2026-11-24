import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_vectors(path, w, h):
    fig, ax, H = canvas(w, h, need=70, exact=True)
    s = 11; o = (14, 10)
    arrow(ax, o, (o[0] + 3 * s, o[1]), color=C['blue'], lw=4); txt(ax, o[0] + 1.5 * s, o[1] - 4, '3 km east', 22, C['blue'], bold=True)
    arrow(ax, (o[0] + 3 * s, o[1]), (o[0] + 3 * s, o[1] + 4 * s), color=C['green'], lw=4); txt(ax, o[0] + 3 * s + 2, o[1] + 2 * s, '4 km\nnorth', 22, C['green'], bold=True, ha='left')
    arrow(ax, o, (o[0] + 3 * s, o[1] + 4 * s), color=C['orange'], lw=5); txt(ax, o[0] + 1.0 * s, o[1] + 2.6 * s, '5 km', 26, C['orange'], bold=True)
    ax.add_patch(Arc(o, 14, 14, theta1=0, theta2=53.13, color=C['ink'], lw=2)); txt(ax, o[0] + 9, o[1] + 3.5, '53.1°', 20)
    txt(ax, 80, 52, r'$|R| = \sqrt{3^2+4^2} = 5$', 26); txt(ax, 79, 40, r'$\theta = \tan^{-1}(4/3) = 53.1°$', 22)
    txt(ax, 80, 26, 'add vectors by\nadding components', 20, C['mut'])
    save(fig, path)

def fig_vt(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 8, 200); v = np.minimum(4.5 * t, 27)
    ax.plot(t, v, color=C['blue']); ax.fill_between(t[t <= 6], 0, v[t <= 6], color=C['lblue'])
    ax.set_xlabel('time (s)'); ax.set_ylabel('speed (m/s)'); ax.set_ylim(0, 32); ax.set_xlim(0, 8)
    ax.text(3.8, 6, 'area = distance\n½ · 6 s · 27 m/s = 81 m', fontsize=20, ha='center')
    note(ax, 0.3, 28.5, 'slope = acceleration = 27/6 = 4.5 m/s²', C['orange'], 19)
    save(fig, path)

def fig_projectile(path, w, h):
    fig, ax = plot(w, h)
    v0, g = 20, 9.8
    for th, col in ((30, C['green']), (45, C['orange']), (60, C['blue'])):
        r = np.radians(th); T = 2 * v0 * np.sin(r) / g; t = X(0, T, 200)
        ax.plot(v0 * np.cos(r) * t, v0 * np.sin(r) * t - 0.5 * g * t ** 2, color=col, label=f'{th}°: range {v0**2*np.sin(2*r)/g:.1f} m')
    ax.set_xlabel('distance (m)'); ax.set_ylabel('height (m)'); ax.set_ylim(0, 27); ax.legend(loc='upper right', fontsize=17); ax.set_aspect('equal')
    ax.set_title('launched at 20 m/s (no air resistance)')
    save(fig, path)

def fig_incline(path, w, h):
    fig, ax, H = canvas(w, h, need=72, exact=True)
    th = np.radians(30); L = 80; base = (8, 8)
    top = (base[0] + L * np.cos(th), base[1] + L * np.sin(th))
    ax.add_patch(Polygon([base, (top[0], base[1]), top], fc='#E4E8EF', ec=C['gray'], lw=2))
    c = (base[0] + 0.55 * L * np.cos(th), base[1] + 0.55 * L * np.sin(th)); bw = 12
    ux, uy = np.cos(th), np.sin(th); nx, ny = -uy, ux
    corners = [(c[0] - ux * bw / 2, c[1] - uy * bw / 2), (c[0] + ux * bw / 2, c[1] + uy * bw / 2),
               (c[0] + ux * bw / 2 + nx * bw * 0.8, c[1] + uy * bw / 2 + ny * bw * 0.8), (c[0] - ux * bw / 2 + nx * bw * 0.8, c[1] - uy * bw / 2 + ny * bw * 0.8)]
    ax.add_patch(Polygon(corners, fc=C['lblue'], ec=C['blue'], lw=2.5, zorder=3))
    cm = (c[0] + nx * bw * 0.4, c[1] + ny * bw * 0.4)
    arrow(ax, cm, (cm[0], cm[1] - 22), color=C['red'], lw=4, z=5); txt(ax, cm[0] + 2, cm[1] - 22, 'mg = 98 N', 19, C['red'], ha='left', bold=True)
    arrow(ax, cm, (cm[0] + nx * 17, cm[1] + ny * 17), color=C['green'], lw=4, z=5); txt(ax, cm[0] + nx * 19, cm[1] + ny * 19 + 1, 'N = 84.9 N', 19, C['green'], bold=True)
    arrow(ax, cm, (cm[0] + ux * 14, cm[1] + uy * 14), color=C['purple'], lw=4, z=5); txt(ax, cm[0] + ux * 16 + 2, cm[1] + uy * 16, 'friction\n17.0 N', 18, C['purple'], ha='left', bold=True)
    ax.add_patch(Arc(base, 26, 26, theta1=0, theta2=30, color=C['ink'], lw=2)); txt(ax, base[0] + 17, base[1] + 3.2, '30°', 19)
    txt(ax, 22, 62, '10 kg box, μk = 0.2', 21, bold=True)
    save(fig, path)

def fig_elevator(path, w, h):
    fig, ax = plot(w, h, grid=False)
    cases = ['at rest', 'accelerating\nup 2 m/s²', 'accelerating\ndown 2 m/s²', 'free fall']
    vals = [686, 826, 546, 0]
    b = bars(ax, cases, vals, colors=[C['gray'], C['orange'], C['blue'], C['red']], fmt='{:.0f} N')
    ax.set_ylabel('scale reading (N)'); ax.set_ylim(0, 950); ax.set_title('70 kg person: N = m(g + a)')
    ax.spines['left'].set_visible(False); ax.set_yticks([]); ax.tick_params(axis='x', labelsize=17)
    save(fig, path)

def fig_circular(path, w, h):
    fig, ax, H = canvas(w, h, need=66, exact=True)
    cx, cy, R = 34, 33, 25
    ax.add_patch(Circle((cx, cy), R, fc='none', ec=C['gray'], lw=10, alpha=0.4)); dot(ax, cx, cy, 0.8)
    ang = np.radians(40); p = (cx + R * np.cos(ang), cy + R * np.sin(ang))
    ax.add_patch(Circle(p, 2.6, fc=C['blue'], zorder=5))
    arrow(ax, p, (p[0] - 16 * np.sin(ang), p[1] + 16 * np.cos(ang)), color=C['green'], lw=4); txt(ax, p[0] - 16 * np.sin(ang) - 2, p[1] + 16 * np.cos(ang) + 2.5, 'velocity', 19, C['green'], bold=True)
    arrow(ax, p, (p[0] - 13 * np.cos(ang), p[1] - 13 * np.sin(ang)), color=C['red'], lw=4); txt(ax, p[0] - 7 * np.cos(ang) + 1, p[1] - 7 * np.sin(ang) - 5, 'a = v²/r', 19, C['red'], bold=True)
    line(ax, [(cx, cy), (cx + R * np.cos(-0.6), cy + R * np.sin(-0.6))], C['ink'], 1.8, ls='--'); txt(ax, cx + 13, cy - 11, 'r = 50 m', 18)
    txt(ax, 80, 50, 'v = 20 m/s, r = 50 m', 22, bold=True); txt(ax, 80, 40, 'a = 400 / 50 = 8 m/s²', 22, C['red'])
    txt(ax, 80, 28, 'friction must supply it:\nμ ≥ a/g = 0.82', 20, C['ink']); txt(ax, 80, 12, 'wet road (μ ≈ 0.5)\n→ the car slides out', 19, C['mut'])
    save(fig, path)

def fig_energy(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, grid=False, gridspec_kw={'height_ratios': [1.3, 1]})
    x = X(0, 10, 300); y = 30 * (0.5 + 0.5 * np.cos(x * np.pi / 6)) * np.exp(-x / 18) + 2
    a1.plot(x, y, color=C['ink'], lw=3); a1.fill_between(x, 0, y, color='#EEF1F6')
    pts = [0, 6, 9.5]
    for xp, lab in zip(pts, ['A', 'B', 'C']):
        yp = np.interp(xp, x, y); soliddot(a1, xp, yp, C['orange']); a1.text(xp, yp + 2.5, lab, fontsize=22, ha='center', fontweight='bold')
    a1.set_ylabel('height (m)'); a1.set_ylim(0, 40); a1.set_xticks([])
    m, g = 1, 9.8; H0 = np.interp(0, x, y)
    labs, pes, kes = [], [], []
    for xp, lab in zip(pts, ['A', 'B', 'C']):
        yp = np.interp(xp, x, y); labs.append(lab); pes.append(g * yp); kes.append(g * (H0 - yp))
    xi = np.arange(3); a2.bar(xi, pes, color=C['blue'], label='potential mgh'); a2.bar(xi, kes, bottom=pes, color=C['orange'], label='kinetic ½mv²')
    a2.set_xticks(xi); a2.set_xticklabels(labs); a2.set_yticks([]); a2.legend(loc='upper center', ncol=2, fontsize=17, bbox_to_anchor=(0.5, -0.18)); a2.set_ylim(0, 340)
    a2.set_ylabel('energy'); fig.subplots_adjust(hspace=0.25)
    save(fig, path)

def fig_collision(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    txt(ax, 8, 50, 'before', 22, C['mut'], ha='left', bold=True); txt(ax, 8, 22, 'after', 22, C['mut'], ha='left', bold=True)
    box(ax, 10, 36, 18, 10, '1000 kg', fc=C['lblue'], fs=19, bold=True); arrow(ax, (28, 41), (40, 41), color=C['blue'], lw=4, text='20 m/s', fs=18)
    box(ax, 56, 36, 24, 10, '1500 kg', fc=C['lorange'], ec=C['orange'], fs=19, bold=True); txt(ax, 68, 32, 'at rest', 17, C['mut'])
    box(ax, 30, 11, 42, 10, '2500 kg (stuck together)', fc=C['lpurple'], ec=C['purple'], fs=18, bold=True); arrow(ax, (72, 16), (84, 16), color=C['purple'], lw=4, text='8 m/s', fs=18)
    txt(ax, 50, 5, 'momentum p: 20,000 → 20,000 kg·m/s (conserved)\nkinetic energy: 200 kJ → 80 kJ (120 kJ crushes metal)', 16, C['ink'])
    save(fig, path)

def fig_torque(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    ax.add_patch(Circle((20, 30), 5, fc=C['gray'], ec=C['ink'], lw=2)); ax.add_patch(Polygon([(20, 26), (78, 27.5), (78, 32.5), (20, 34)], fc='#C9D1DE', ec=C['ink'], lw=2))
    arrow(ax, (75, 32), (75, 50), color=C['red'], lw=4.5); txt(ax, 77, 46, 'F = 50 N', 21, C['red'], ha='left', bold=True)
    line(ax, [(20, 20), (75, 20)], C['blue'], 2); txt(ax, 47, 16, 'r = 0.30 m', 21, C['blue'], bold=True)
    ax.add_patch(Arc((20, 30), 22, 22, theta1=20, theta2=160, color=C['orange'], lw=3)); txt(ax, 20, 45, 'τ = r F = 15 N·m', 22, C['orange'], bold=True)
    txt(ax, 50, 5, 'longer wrench → same torque with less force', 19, C['mut'])
    save(fig, path)

def fig_analog(path, w, h):
    fig, ax, H = canvas(w, h, need=55, exact=True)
    rows = [('position x', 'angle θ'), ('velocity v', 'angular velocity ω'), ('acceleration a', 'angular accel. α'), ('mass m', 'moment of inertia I'),
            ('force F = ma', 'torque τ = Iα'), ('momentum p = mv', 'angular momentum L = Iω'), ('KE = ½mv²', 'KE = ½Iω²')]
    table(ax, 6, H - 2, ['linear', 'rotational'], rows, [44, 44], 6.2, 21)
    save(fig, path)

def fig_arm(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    ax.add_patch(Rectangle((6, 6), 10, 34, fc='#C9D1DE', ec=C['ink'], lw=2)); ax.add_patch(Circle((11, 40), 4.5, fc=C['orange'], ec=C['ink'], lw=2, zorder=4))
    txt(ax, 11, 48, 'motor', 18, C['orange'], bold=True)
    ax.add_patch(Rectangle((11, 38), 70, 4, fc=C['lblue'], ec=C['blue'], lw=2))
    box(ax, 76, 26, 10, 10, '2 kg', fc=C['lred'], ec=C['red'], fs=17, bold=True); line(ax, [(81, 38), (81, 36)], C['ink'], 2)
    arrow(ax, (81, 26), (81, 14), color=C['red'], lw=4); txt(ax, 83, 18, '19.6 N', 18, C['red'], ha='left', bold=True)
    line(ax, [(11, 33), (81, 33)], C['blue'], 1.6, ls='--'); txt(ax, 46, 29, '0.5 m', 19, C['blue'])
    txt(ax, 46, 56, 'holding torque = 19.6 N × 0.5 m = 9.8 N·m', 21, bold=True)
    txt(ax, 58, 8, '+ the arm’s own weight\n→ size motor & gearbox for ≈ 12 N·m', 18, C['mut'])
    save(fig, path)

def fig_orbit(path, w, h):
    fig, ax, H = canvas(w, h, need=64, exact=True)
    ax.add_patch(Circle((30, 32), 9, fc=C['lblue'], ec=C['blue'], lw=2)); txt(ax, 30, 32, 'Earth', 18, C['blue'], bold=True)
    ax.add_patch(Circle((30, 32), 26, fc='none', ec=C['gray'], lw=2, ls='--'))
    sp = (30 + 26 * np.cos(0.6), 32 + 26 * np.sin(0.6)); ax.add_patch(Rectangle((sp[0] - 2, sp[1] - 1.5), 4, 3, fc=C['orange'], zorder=5))
    arrow(ax, sp, (sp[0] - 10 * np.sin(0.6), sp[1] + 10 * np.cos(0.6)), color=C['green'], lw=3.5)
    arrow(ax, sp, (sp[0] - 9 * np.cos(0.6), sp[1] - 9 * np.sin(0.6)), color=C['red'], lw=3.5)
    txt(ax, 78, 54, 'gravity provides the\ncentripetal force:', 20); txt(ax, 78, 42, r'$\frac{GMm}{r^2} = \frac{mv^2}{r}\ \Rightarrow\ v = \sqrt{\frac{GM}{r}}$', 26)
    txt(ax, 78, 26, 'GPS: r ≈ 26,600 km', 21, C['blue'], bold=True); txt(ax, 78, 18, 'v ≈ 3.9 km/s, period ≈ 12 h', 20, C['ink'])
    save(fig, path)

LESSON = {
 'code': 'PHYS 225', 'title': 'Mechanics', 'tag': 'Year 1 · Foundations', 'folder': 'PHYS-225 Mechanics',
 'slides': [
 {'t': 'title', 'h': 'Mechanics', 'sub': 'Motion, forces, energy, momentum and rotation', 'img': 'a:rocket_launch',
  'say': "Welcome to physics two twenty five, mechanics. This is the physics of things that move: rockets, cars, robot arms, and the tiny vibrating structures inside your phone. We'll build up from describing motion, to Newton's laws, energy, momentum and rotation, with real numbers at every step. Grab a calculator."},

 {'t': 'v', 'h': 'Why does a computer engineer need mechanics?', 'img': ['a:robot_arm', 'a:mpu6050', 'a:falcon_landing'],
  'pts': ['Robots & drones: motors, torque, balance', 'Sensors: your phone’s accelerometer is a tiny mass on a spring', 'Control: software that steers physical things'],
  'say': ["Computer engineers increasingly build things that move. A robot arm like this one has to be programmed knowing how much torque each motor can supply and how heavy the payload is. Drones, self driving cars and warehouse robots are the same story.",
          "Sensors too. This tiny chip is an accelerometer and gyroscope, the same kind of part inside your phone and game controllers. Inside is a microscopic mass on springs etched in silicon. When the chip accelerates, the mass lags behind, and the circuit measures that tiny shift. It's literally F equals m a, on a chip.",
          "And control. This rocket booster landed itself, with software reading sensors and steering the engine hundreds of times per second. Software that controls physical things has to be built on mechanics."]},

 {'t': 'v', 'h': 'Vectors: quantities with direction', 'img': 'fig:vectors',
  'pts': ['Scalar: just a size (mass, time, speed)', 'Vector: size + direction (displacement, velocity, force)', 'Add vectors tip-to-tail, or by components', '3 km east + 4 km north = 5 km at 53.1°'],
  'say': ["Some quantities only have a size, like mass or temperature. Those are scalars.",
          "Others have a size and a direction, like displacement, velocity and force. Those are vectors. Push a box with fifty newtons, and it matters a lot whether you push left or right.",
          "To add vectors, place them tip to tail, or more practically, break each into x and y components and add the components separately.",
          "Example: walk three kilometers east, then four kilometers north. Your net displacement has length square root of three squared plus four squared, which is five kilometers, at an angle of inverse tangent of four over three, which is fifty three point one degrees north of east. Breaking things into components is the single most useful trick in this course."]},

 {'t': 'v', 'h': 'Kinematics: describing motion', 'img': 'fig:vt',
  'pts': ['v = v₀ + at', 'x = x₀ + v₀t + ½at²', 'v² = v₀² + 2a(x − x₀)', 'Car 0 → 60 mph (27 m/s) in 6 s: a = 4.5 m/s², 81 m'],
  'say': ["Kinematics describes motion without asking what causes it. For constant acceleration, three equations do almost everything. Velocity grows linearly: v equals v naught plus a t.",
          "Position follows x equals x naught plus v naught t plus one half a t squared. That should look familiar from calculus: position is the integral of velocity.",
          "And when you don't know the time: v squared equals v naught squared plus two a times the distance.",
          "Example: a car goes from zero to sixty miles per hour, about twenty seven meters per second, in six seconds. The acceleration is twenty seven divided by six, four point five meters per second squared. That's the slope of the velocity graph. The distance covered is the area under it: one half times six times twenty seven, which is eighty one meters."]},

 {'t': 'v', 'h': 'Projectile motion: two independent problems', 'img': 'fig:projectile',
  'pts': ['Horizontal: constant velocity', 'Vertical: constant acceleration (−9.8 m/s²)', '20 m/s at 45°: range 40.8 m, peak 10.2 m, 2.9 s', '30° and 60° land at the same spot'],
  'say': ["Throw something, and its motion splits into two independent problems. Horizontally, nothing pushes it, so it moves at constant velocity, ignoring air resistance.",
          "Vertically, gravity accelerates it downward at nine point eight meters per second squared, exactly like the ball we threw straight up in calculus.",
          "Launch at twenty meters per second at forty five degrees. The vertical speed is twenty times sine forty five, about fourteen point one. It stays in the air for two times fourteen point one over nine point eight, about two point nine seconds, and in that time travels about forty point eight meters horizontally, peaking at ten point two meters.",
          "Notice that thirty and sixty degrees land at the same spot, about thirty five meters, because the range depends on sine of twice the angle. Forty five degrees gives the maximum range, at least without air resistance."]},

 {'t': 'v', 'h': "Newton's three laws", 'img': ['a:rocket_launch', 'a:rocket_launch', 'a:rocket_launch'],
  'pts': ['1. Objects keep doing what they’re doing unless a net force acts', '2. F_net = m a', '3. Every force has an equal and opposite partner'],
  'say': ["Now, what causes motion? Isaac Newton's three laws. First: an object at rest stays at rest, and an object moving stays moving in a straight line at constant speed, unless a net force acts on it. Motion doesn't need a cause. Changes in motion do.",
          "Second: the net force equals mass times acceleration. Double the force, double the acceleration. Double the mass, half the acceleration. This one equation is the engine of all of mechanics.",
          "Third: forces come in pairs. If A pushes on B, B pushes back on A equally hard in the opposite direction. A rocket pushes hot gas down out of its engines, and the gas pushes the rocket up. It doesn't need air to push against, which is why rockets work in space."]},

 {'t': 'v', 'h': 'Free-body diagrams: a box on a ramp', 'img': 'fig:incline',
  'pts': ['Draw every force on ONE object', 'Tilt the axes along the slope', 'Along: 98 sin30° − 0.2 × 84.9 = 32.0 N', 'a = 32.0 / 10 = 3.2 m/s² down the ramp'],
  'say': ["To use F equals m a, draw a free body diagram: the object alone, with an arrow for every force acting on it. Here's a ten kilogram box sliding down a thirty degree ramp, with a friction coefficient of point two. Gravity pulls straight down with m g, ninety eight newtons. The ramp pushes back perpendicular to its surface with the normal force. And friction opposes the sliding.",
          "Trick: tilt your axes so x runs along the slope. Then the normal force and the perpendicular part of gravity cancel: N equals m g cosine thirty, eighty four point nine newtons.",
          "Along the slope, gravity's component is ninety eight times sine thirty, forty nine newtons. Friction is the coefficient times the normal force: point two times eighty four point nine, about seventeen newtons, pointing up the slope. The net force is about thirty two newtons down the slope.",
          "Divide by the mass: the box accelerates at about three point two meters per second squared. Every mechanics problem, from bridges to robot joints, follows this same recipe: isolate the object, draw the forces, pick smart axes, apply F equals m a. One detail: point two is the kinetic friction coefficient, for a box that's already sliding. Static friction, which holds a resting box in place, is usually a little larger. That's why it takes more force to start something moving than to keep it moving."]},

 {'t': 'v', 'h': 'Apparent weight: what your phone’s accelerometer feels', 'img': 'fig:elevator',
  'pts': ['Scale reads the normal force N, not mg', 'N = m(g + a)', 'Going up faster: you feel heavier', 'Free fall: N = 0 — "weightless"'],
  'say': ["Stand on a bathroom scale in an elevator. The scale doesn't measure gravity directly. It measures how hard it has to push up on you: the normal force.",
          "Apply Newton's second law: N minus m g equals m a, so N equals m times g plus a.",
          "A seventy kilogram person reads six hundred eighty six newtons at rest. Accelerating upward at two meters per second squared, the reading jumps to eight hundred twenty six newtons. You feel heavier. Accelerating downward, it drops to five hundred forty six.",
          "And in free fall, the reading is zero. That's why astronauts in orbit float: they're falling around the Earth continuously. An accelerometer works exactly like this scale. That's why a phone lying still on a table reports about one g pointing up, and how it knows which way is up to rotate your screen."]},

 {'t': 'v', 'h': 'Circular motion: why cars slide on curves', 'img': 'fig:circular',
  'pts': ['Moving in a circle = constantly changing direction', 'Centripetal acceleration a = v²/r, toward the center', 'Something must supply that force: friction, tension, gravity'],
  'say': ["Even at constant speed, moving in a circle means your velocity keeps changing direction. And a change in velocity is an acceleration.",
          "That centripetal acceleration points toward the center, with size v squared over r. A car at twenty meters per second, about forty five miles per hour, on a curve of radius fifty meters needs eight meters per second squared toward the center.",
          "Something has to supply that force. For a car, it's friction between the tires and the road. The friction coefficient must be at least eight over nine point eight, about point eight two. Dry pavement can do that. A wet road, with a coefficient around point five, can't, and the car slides outward. That's why curve speed limits exist, and why highway curves are banked. The same equation sizes the spin speed of hard drive platters and the forces in a centrifuge."]},

 {'t': 'v', 'h': 'Energy: the bookkeeping shortcut', 'img': 'fig:energy',
  'pts': ['Kinetic energy ½mv² · potential energy mgh', 'Without friction, the total never changes', 'Drop 30 m: v = √(2gh) = 24.2 m/s (87 km/h)', 'Work W = F·d changes energy'],
  'say': ["Forces and accelerations can get messy. Energy is often a much faster route. Moving objects have kinetic energy, one half m v squared. Raised objects have gravitational potential energy, m g h.",
          "Without friction, energy just converts between these forms, and the total stays constant. Look at the roller coaster. At A, it's all potential energy, the blue bar. At B, the bottom, most of it has become kinetic, orange. At C, it's partly back to potential.",
          "So how fast is a coaster after dropping thirty meters? Set m g h equal to one half m v squared. The mass cancels, and v is the square root of two g h, about twenty four point two meters per second, or eighty seven kilometers per hour. No forces, no time, no calculus. Just bookkeeping.",
          "Work, force times distance, is how energy enters or leaves. Friction does negative work, turning motion into heat. In electronics, you'll see the same conservation idea: energy delivered by a battery ends up as heat in resistors, light in LEDs, or stored in capacitors."]},

 {'t': 'v', 'h': 'Momentum and collisions', 'img': 'fig:collision',
  'pts': ['Momentum p = mv; total is conserved in collisions', '1000 kg at 20 m/s hits 1500 kg at rest, they stick: 8 m/s', 'Kinetic energy: 200 kJ → 80 kJ (rest crushes metal)', 'Impulse: F·Δt = Δp → airbags stretch Δt, cut the force'],
  'say': ["Momentum is mass times velocity. When objects collide, the forces between them are equal and opposite, so the total momentum before equals the total after.",
          "A thousand kilogram car at twenty meters per second hits a fifteen hundred kilogram car at rest, and they stick together. Momentum before: twenty thousand. After, two thousand five hundred kilograms share it, so they move at eight meters per second.",
          "But kinetic energy is not conserved here. It drops from two hundred kilojoules to eighty. The missing one hundred twenty kilojoules went into crushing metal, heat and sound. Car crumple zones are designed to absorb exactly that energy. Two names to know: a collision that keeps kinetic energy, like billiard balls bouncing, is called elastic. One where the objects stick together, like these cars, is perfectly inelastic, and loses the most energy possible. Momentum is conserved in both.",
          "And impulse explains safety design. Force times time equals the change in momentum. Your momentum has to drop to zero in a crash either way. An airbag stretches the stopping time from a few milliseconds to tens of milliseconds, so the force on you drops by roughly the same factor. Electronics borrowed a related trick: many laptops with spinning hard drives used an accelerometer to detect a fall and park the drive's read head before impact."]},

 {'t': 'v', 'h': 'Rotation: torque', 'img': ['fig:torque', 'fig:analog'],
  'pts': ['Torque τ = r F sin θ: the “twisting force”', '0.3 m wrench × 50 N = 15 N·m', 'Every linear idea has a rotational twin'],
  'say': ["Spinning things are described by rotational versions of everything we've done. The rotational version of force is torque: how hard you twist. Torque equals the distance from the pivot times the force times the sine of the angle between them. Push at the end of a thirty centimeter wrench with fifty newtons, at a right angle, and you apply fifteen newton meters. Use a longer wrench and you need less force for the same torque. That's why it's easier to open a door by pushing far from the hinges.",
          "Every linear quantity has a twin. Position becomes angle. Velocity becomes angular velocity. Mass becomes moment of inertia, which depends on how far the mass is from the axis. F equals m a becomes torque equals I alpha. And kinetic energy becomes one half I omega squared. Learn one column, and the other comes almost for free."]},

 {'t': 'v', 'h': 'Engineering example: sizing a robot arm motor', 'img': 'fig:arm',
  'pts': ['Holding torque = weight × horizontal distance', '2 kg at 0.5 m → 9.8 N·m (+ the arm itself)', 'Small motors give ≈ 0.5 N·m → need ≈ 25:1 gearing', 'Worst case: arm fully extended'],
  'say': ["Here's mechanics doing real engineering work. A robot arm holds a two kilogram object at the end of a half meter arm, held horizontal. The payload's weight is nineteen point six newtons.",
          "The motor at the shoulder must supply a torque of nineteen point six times point five, about nine point eight newton meters, just to hold still. Add the arm's own weight, acting at its middle, and the requirement is closer to twelve.",
          "A typical small hobby motor might deliver around half a newton meter. So you'd need a gearbox of roughly twenty five to one, trading speed for torque.",
          "And notice that the worst case is the arm stretched out horizontally, when the lever arm is longest. Engineers always size motors for the worst case, plus a safety margin. Robot arm projects, like the one in this degree's senior design course, start exactly with this calculation."]},

 {'t': 'v', 'h': 'Gravity and orbits: how GPS satellites stay up', 'img': ['a:gps_sat', 'fig:orbit'],
  'pts': ['F = G m₁m₂ / r²', 'Orbit: gravity supplies the centripetal force', 'v = √(GM/r) — no fuel needed to stay in orbit', 'GPS: ~26,600 km radius, 3.9 km/s, 12-hour orbit'],
  'say': ["Newton's law of gravitation says every two masses attract with a force G m one m two over r squared. At the Earth's surface, that gives the familiar nine point eight meters per second squared.",
          "Now combine it with circular motion. A satellite in orbit is falling toward Earth the whole time, but it's moving sideways so fast that it keeps missing. Gravity provides exactly the centripetal force: G M m over r squared equals m v squared over r. The satellite's mass cancels, and the orbital speed is the square root of G M over r. No engine needed to stay up. GPS satellites like this one orbit at a radius of about twenty six thousand six hundred kilometers, moving at about three point nine kilometers per second, and circle the Earth every twelve hours. Your phone finds your position by timing signals from several of them, which you'll appreciate more after the electromagnetism and signals courses."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Draw the forces, apply **F = ma** — or skip straight to **energy and momentum** conservation. Rotation is the same physics, spinning.',
  'cap': 'Next: MATH 170A, Mathematical Structures — the logic and discrete math behind computing.',
  'say': "Let's recap. Vectors are broken into components. Kinematics describes motion with three equations for constant acceleration. Newton's laws explain what causes motion, and free body diagrams are how you apply them. Energy and momentum conservation are shortcuts that skip the details. And rotation, with torque and moment of inertia, mirrors everything linear. You'll see these ideas again in robotics, sensors and control, and the math patterns, like conservation and equal and opposite pairs, come back in circuits. Next up, discrete mathematics, the math of logic and computing. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B

def draw_walk(ax, n, w, h):
    s = 120; X0, Y0 = 120, 120
    if n >= 1:
        B.arr(ax, X0, Y0, X0 + 3 * s, Y0, 'blue', 4); B.lab(ax, X0 + 1.5 * s, Y0 - 35, '3 km east', 30, 'blue')
    if n >= 2:
        B.arr(ax, X0 + 3 * s, Y0, X0 + 3 * s, Y0 + 4 * s, 'green', 4); B.lab(ax, X0 + 3 * s + 20, Y0 + 2 * s, '4 km north', 30, 'green', ha='left')
    if n >= 3:
        B.arr(ax, X0, Y0, X0 + 3 * s, Y0 + 4 * s, 'red', 4.5); B.lab(ax, X0 + 1.2 * s, Y0 + 2.4 * s, '5 km', 34, 'red', rotation=53)
        t = np.linspace(0, np.radians(53.13), 30); B.ln(ax, X0 + 70 * np.cos(t), Y0 + 70 * np.sin(t), c='orange', lw=2.5)
        B.lab(ax, X0 + 100, Y0 + 38, '53°', 28, 'orange', ha='left')

def draw_cliff(ax, n, w, h):
    X0, Y0, sx, sy = 40, 70, 20, 26      # cliff top at y = 20 m
    P = lambda x, y: (X0 + 140 + x * sx, Y0 + y * sy)
    if n >= 1:
        B.poly(ax, [(X0, Y0), (X0 + 140, Y0), (X0 + 140, Y0 + 20 * sy), (X0, Y0 + 20 * sy)], fc='#e3dccf', c='ink', lw=3)
        B.ln(ax, [X0, X0 + 140 + 34 * sx], [Y0, Y0], c='ink', lw=3)
        B.arr(ax, X0 + 100, Y0 + 20 * sy, X0 + 100, Y0, 'red', 2, 18, '<|-|>'); B.lab(ax, X0 + 70, Y0 + 10 * sy, '20 m', 30, 'red', rotation=90)
        B.dot(ax, *P(0, 20), s=14); B.arr(ax, *P(0, 20), *P(5, 20), 'blue', 3.5); B.lab(ax, *P(3, 21.6), '15 m/s', 28, 'blue')
    if n >= 2:
        ts = np.linspace(0, 2.02, 40); B.ln(ax, *zip(*[P(15 * t, 20 - 4.9 * t * t) for t in ts]), c='blue', lw=3, ls='--')
    if n >= 3:
        B.dot(ax, *P(30.3, 0), c='red', s=14); B.lab(ax, P(30.3, 0)[0] + 10, Y0 - 35, 'x = 30.3 m', 30, 'red', ha='right')

def draw_pulley(ax, n, w, h):
    ty = h * 0.6; tx1 = w * 0.62
    if n >= 1:
        B.rect(ax, 30, ty - 30, tx1 - 30, 30, fc='#e3dccf'); B.ln(ax, [50, 50], [ty - 30, 60]); B.ln(ax, [tx1 - 20, tx1 - 20], [ty - 30, 60])
        t = np.linspace(0, 2 * np.pi, 60); B.ln(ax, tx1 + 30 + 28 * np.cos(t), ty + 28 + 28 * np.sin(t), lw=3)
        B.rect(ax, 160, ty, 150, 110, fc='#dfe8f7'); B.lab(ax, 235, ty + 55, '4 kg', 32)
        B.ln(ax, [310, tx1 + 30], [ty + 56, ty + 56], lw=2.5); B.ln(ax, [tx1 + 58, tx1 + 58], [ty + 28, ty - 160], lw=2.5)
        B.rect(ax, tx1 + 8, ty - 260, 100, 100, fc='#f6d6c4'); B.lab(ax, tx1 + 58, ty - 210, '2 kg', 30)
    if n >= 2:
        B.arr(ax, 310, ty + 90, 420, ty + 90, 'green', 3.5); B.lab(ax, 370, ty + 125, 'T', 34, 'green')
        B.arr(ax, tx1 + 58, ty - 160, tx1 + 58, ty - 70, 'green', 3.5); B.lab(ax, tx1 + 95, ty - 100, 'T', 34, 'green')
        B.arr(ax, tx1 + 58, ty - 260, tx1 + 58, ty - 380, 'red', 3.5); B.lab(ax, tx1 + 110, ty - 350, '2g', 34, 'red')
    if n >= 3:
        B.arr(ax, 200, ty + 150, 300, ty + 150, 'orange', 3); B.lab(ax, 250, ty + 185, 'a', 32, 'orange')
        B.arr(ax, tx1 + 150, ty - 170, tx1 + 150, ty - 270, 'orange', 3); B.lab(ax, tx1 + 180, ty - 220, 'a', 32, 'orange')

def draw_spring(ax, n, w, h):
    cx, by = w * 0.35, 70
    if n >= 1:
        B.ln(ax, [cx - 90, cx + 90], [by, by], lw=4)
        ys = np.linspace(by, by + 120, 13); xs = cx + np.array([0, 30, -30] * 4 + [0])[:13]
        B.ln(ax, xs, ys, lw=3); B.dot(ax, cx, by + 145, c='red', s=40)
        B.lab(ax, cx + 70, by + 60, 'compressed 0.1 m', 26, 'gray', ha='left'); B.lab(ax, cx + 70, by + 150, '50 g', 28, 'red', ha='left')
    if n >= 2:
        B.ln(ax, [cx, cx], [by + 175, by + 640], c='blue', lw=2.5, ls='--'); B.dot(ax, cx, by + 650, c='red', s=40, hollow=True)
        B.arr(ax, cx - 120, by + 145, cx - 120, by + 650, 'green', 2, 18, '<|-|>'); B.lab(ax, cx - 150, by + 400, 'h', 36, 'green')

def draw_seesaw(ax, n, w, h):
    py = h * 0.4; cx = w * 0.5; s = 140
    if n >= 1:
        B.poly(ax, [(cx - 50, py - 110), (cx + 50, py - 110), (cx, py - 10)], fc='#e3dccf')
        B.rect(ax, cx - 2.6 * s, py - 10, 5.2 * s, 18, fc='#c9a77a')
        B.rect(ax, cx - 2 * s - 40, py + 8, 80, 90, fc='#dfe8f7'); B.lab(ax, cx - 2 * s, py + 53, '30', 28)
        B.arr(ax, cx - 2 * s, py - 20, cx - 2 * s, py - 160, 'red', 3); B.lab(ax, cx - 2 * s, py - 190, '30g', 30, 'red')
        B.arr(ax, cx, py - 230, cx - 2 * s, py - 230, 'gray', 2, 18, '<|-|>'); B.lab(ax, cx - s, py - 260, '2 m', 30, 'gray')
    if n >= 2:
        B.rect(ax, cx + 1.5 * s - 45, py + 8, 90, 100, fc='#f6d6c4'); B.lab(ax, cx + 1.5 * s, py + 58, '40', 28)
        B.arr(ax, cx + 1.5 * s, py - 20, cx + 1.5 * s, py - 160, 'red', 3); B.lab(ax, cx + 1.5 * s, py - 190, '40g', 30, 'red')
        B.arr(ax, cx, py - 230, cx + 1.5 * s, py - 230, 'gray', 2, 18, '<|-|>'); B.lab(ax, cx + 0.75 * s, py - 260, 'd = ?', 30, 'gray')

B.insert(LESSON, 'Vectors: quantities with direction', {'t': 'wb', 'h': 'Worked example: adding two displacements', 'draw': 'walk', 'split': 0.55, 'steps': [
    {'say': "Let's add two vectors by hand. You walk three kilometers east, then four kilometers north. Where do you end up, and in what direction? Draw them tip to tail: first the east arrow, then the north arrow starting where the first one ends.",
     'w': [{'m': '3 km east, then 4 km north', 'at': 1}, {'d': 1, 'at': 3}, {'d': 2, 'at': 3}]},
    {'say': "The total displacement is the arrow from the start to the finish. It's the hypotenuse of a right triangle, so use Pythagoras: the square root of three squared plus four squared, which is the square root of twenty five, five kilometers.",
     'w': [{'d': 3}, {'m': r'$|\vec{d}| = \sqrt{3^2 + 4^2} = \sqrt{25}$', 'at': 1}, {'m': r'$= 5\ \mathrm{km}$', 'at': 1}]},
    {'say': "For the direction, use the tangent: opposite over adjacent is four over three. The inverse tangent gives fifty three degrees north of east. Notice you walked seven kilometers, but you're only five kilometers from where you started. Distance and displacement are different things.",
     'w': [r'$\tan\theta = \frac{4}{3}$', {'m': r'$\theta = \tan^{-1}(4/3) \approx 53°$ north of east', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Projectile motion', {'t': 'wb', 'h': 'Worked example: a ball thrown off a cliff', 'draw': 'cliff', 'split': 0.52, 'steps': [
    {'say': "Here's a new projectile problem, worked on the board. A ball is thrown horizontally at fifteen meters per second from the top of a twenty meter cliff. How far from the base does it land?",
     'w': [{'d': 1}, {'m': r'$v_x = 15\ \mathrm{m/s}$,   $v_{y0} = 0$,   drop $= 20\ \mathrm{m}$', 'at': 1}]},
    {'say': "Split it into two problems. Vertically, it's just falling from rest. So twenty equals one half times nine point eight times t squared. Solve: t squared is about four point zero eight, so t is about two point zero two seconds.",
     'w': [{'d': 2}, {'m': r'vertical:  $20 = \frac{1}{2}(9.8)\,t^2$', 'at': 2}, {'m': r'$t = \sqrt{40/9.8} \approx 2.02\ \mathrm{s}$', 'at': 3}]},
    {'say': "Horizontally, nothing slows it down, so the distance is speed times time: fifteen times two point zero two, about thirty point three meters.",
     'w': [r'horizontal:  $x = v_x\,t = 15 \times 2.02$', {'m': r'$x \approx 30.3\ \mathrm{m}$', 'c': 'red', 'box': True, 'at': 1}, {'d': 3, 'at': 1}]},
    {'say': "And how fast is it going when it hits? The vertical speed is nine point eight times two point zero two, about nineteen point eight. Combine the two components with Pythagoras: about twenty four point eight meters per second.",
     'w': [{'m': r'$v_y = 9.8 \times 2.02 \approx 19.8$', 'at': 1}, {'m': r'$v = \sqrt{15^2 + 19.8^2} \approx 24.8\ \mathrm{m/s}$', 'at': 2}]},
]})

B.insert(LESSON, 'Free-body diagrams', {'t': 'wb', 'h': 'Worked example: two blocks and a pulley', 'draw': 'pulley', 'split': 0.48, 'steps': [
    {'say': "Now a problem with two objects. A four kilogram block sits on a frictionless table. A string runs over a pulley at the edge to a two kilogram block hanging below. What's the acceleration, and what's the tension in the string?",
     'w': [{'d': 1, 'at': 1}, {'m': 'Find a and T (no friction)', 'at': 3}]},
    {'say': "Draw a free body diagram for each block. The table block feels only the tension T pulling it sideways. The hanging block feels T pulling up and its weight, two g, pulling down. The string keeps them moving together, so they share the same acceleration a.",
     'w': [{'d': 2}, {'m': r'table block:  $T = 4a$', 'at': 1}, {'m': r'hanging block:  $2g - T = 2a$', 'at': 2}, {'d': 3, 'at': 3}]},
    {'say': "Add the two equations, and the tension cancels: two g equals six a. So a is two times nine point eight over six, about three point two seven meters per second squared.",
     'w': [r'add:  $2g = 6a$', {'m': r'$a = \frac{2(9.8)}{6} \approx 3.27\ \mathrm{m/s^2}$', 'c': 'red', 'box': True, 'at': 1}]},
    {'say': "Then the tension is four times a: about thirteen point one newtons. Sanity check: that's less than the hanging block's weight of nineteen point six newtons, which makes sense, because the hanging block is accelerating downward. If the tension equaled its weight, nothing would move.",
     'w': [{'m': r'$T = 4a \approx 13.1\ \mathrm{N}$', 'c': 'red', 'box': True}, {'m': r'check: $T < 2g = 19.6\ \mathrm{N}$', 'c': 'gray', 'at': 1}]},
]})

B.insert(LESSON, 'Energy: the bookkeeping shortcut', {'t': 'wb', 'h': 'Worked example: a spring launcher', 'draw': 'spring', 'split': 0.58, 'steps': [
    {'say': "Let's use energy bookkeeping on a spring launcher. A spring with stiffness eight hundred newtons per meter is compressed ten centimeters, with a fifty gram ball on top. How fast does the ball leave, and how high does it go?",
     'w': [{'d': 1}, {'m': r'$k = 800\ \mathrm{N/m}$,   $x = 0.1\ \mathrm{m}$,   $m = 0.05\ \mathrm{kg}$', 'at': 1}]},
    {'say': "The energy stored in the spring is one half k x squared: one half times eight hundred times point one squared, which is four joules.",
     'w': [r'$E_{spring} = \frac{1}{2}kx^2 = \frac{1}{2}(800)(0.1)^2 = 4\ \mathrm{J}$']},
    {'say': "All four joules become kinetic energy as the ball leaves. One half m v squared equals four, so v squared is eight over point zero five, one hundred sixty, and v is about twelve point six meters per second.",
     'w': [{'m': r'$\frac{1}{2}mv^2 = 4$', 'at': 1}, {'m': r'$v = \sqrt{\frac{2(4)}{0.05}} = \sqrt{160} \approx 12.6\ \mathrm{m/s}$', 'at': 1}]},
    {'say': "At the top, it's all potential energy: m g h equals four. So h is four over point zero five times nine point eight, about eight point two meters. We never needed the time or the acceleration. Energy skipped straight to the answer.",
     'w': [{'d': 2}, {'m': r'$mgh = 4 \;\Rightarrow\; h = \frac{4}{0.05(9.8)} \approx 8.2\ \mathrm{m}$', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Rotation: torque', {'t': 'wb', 'h': 'Worked example: balancing a seesaw', 'draw': 'seesaw', 'split': 0.5, 'steps': [
    {'say': "Here's torque on the board. A thirty kilogram child sits two meters from the pivot of a seesaw. Where must a forty kilogram child sit to balance it?",
     'w': [{'d': 1, 'at': 1}, {'d': 2, 'at': 2}, {'m': '30 kg at 2 m.  40 kg at d = ?', 'at': 2}]},
    {'say': "Balance means the torques cancel: the counterclockwise torque equals the clockwise torque. Each torque is weight times distance from the pivot.",
     'w': [r'balance:  $\tau_{left} = \tau_{right}$', {'m': r'$(30g)(2) = (40g)\,d$', 'at': 1}]},
    {'say': "The g cancels from both sides, so sixty equals forty d, and d is one and a half meters. The heavier child sits closer to the pivot. This is exactly how a balance scale, a crane's counterweight, and the robot arm on the next slide are designed.",
     'w': [r'$60 = 40\,d$', {'m': r'$d = 1.5\ \mathrm{m}$', 'c': 'red', 'box': True, 'at': 1}]},
]})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Vectors:'
B.spen(LESSON, S, 2, {'fig': [('arrow', .15, .8, .46, .8)], 'c': 'blue', 'at': 0, 'dt': 2.0}, {'fig': [('arrow', .5, .8, .5, .27)], 'c': 'green', 'at': 0, 'dt': 3.2})
B.spen(LESSON, S, 3, {'fig': [('circle', .3, .9, .12, .04)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .54, .54, .08, .07)], 'c': 'green', 'at': 0, 'dt': 1.5},
       {'fig': [('underline', .63, .96, .29)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .62, .95, .45)], 'c': 'orange', 'at': 1, 'dt': 5.0},
       {'fig': [('circle', .23, .8, .05, .04)], 'c': 'red', 'at': 1, 'dt': 6.5})
S = 'Kinematics'
B.spen(LESSON, S, 0, {'fig': [('arrow', .17, .76, .7, .2)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('underline', .17, .77, .155)], 'c': 'orange', 'at': 1}, {'fig': [('box', .32, .57, .75, .69)], 'c': 'blue', 'at': 3})
S = 'Projectile motion'
B.spen(LESSON, S, 0, {'fig': [('arrow', .3, .62, .6, .62)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('arrow', .52, .3, .52, .55)], 'c': 'red', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .75, .245, .18, .035)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .54, .545, .03, .045)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .896, .8, .025, .045)], 'c': 'orange', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 3, {'fig': [('circle', .81, .8, .03, .05)], 'c': 'purple', 'at': 0}, {'fig': [('underline', .6, .92, .235)], 'c': 'green', 'at': 0, 'dt': 1.0},
       {'fig': [('underline', .6, .92, .363)], 'c': 'blue', 'at': 0, 'dt': 1.6}, {'fig': [('check', .94, .245)], 'c': 'green', 'at': 1})
S = 'Free-body diagrams'
B.spen(LESSON, S, 0, {'fig': [('underline', .07, .36, .175)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .53, .81, .08, .04)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .34, .265, .08, .04)], 'c': 'green', 'at': 3}, {'fig': [('circle', .645, .405, .06, .06)], 'c': 'purple', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('arrow', .15, .83, .45, .66)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .27, .41, .29)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .25, .82, .04, .04)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .645, .405, .06, .06)], 'c': 'purple', 'at': 1})
S = 'Apparent weight'
B.spen(LESSON, S, 1, {'fig': [('underline', .38, .86, .09)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .21, .285, .06, .035)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .42, .175, .06, .035)], 'c': 'orange', 'at': 1},
       {'fig': [('circle', .63, .39, .06, .035)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 3, {'fig': [('circle', .84, .81, .05, .035)], 'c': 'red', 'at': 0})
S = 'Circular motion'
B.spen(LESSON, S, 0, {'fig': [('circle', .48, .33, .06, .07)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('underline', .63, .97, .26)], 'c': 'blue', 'at': 1}, {'fig': [('box', .63, .33, .97, .43)], 'c': 'red', 'at': 1, 'dt': 2.5})
B.spen(LESSON, S, 2, {'fig': [('underline', .69, .91, .645)], 'c': 'green', 'at': 2}, {'fig': [('box', .66, .76, .94, .89)], 'c': 'purple', 'at': 4})
S = 'Energy: the bookkeeping'
B.spen(LESSON, S, 1, {'fig': [('circle', .18, .12, .03, .045)], 'c': 'blue', 'at': 2}, {'fig': [('box', .17, .52, .4, .81)], 'c': 'blue', 'at': 2, 'dt': 0.8},
       {'fig': [('circle', .63, .4, .03, .045)], 'c': 'orange', 'at': 3}, {'fig': [('box', .44, .52, .67, .81)], 'c': 'orange', 'at': 3, 'dt': 0.8},
       {'fig': [('circle', .89, .3, .03, .045)], 'c': 'purple', 'at': 4}, {'fig': [('box', .7, .52, .94, .81)], 'c': 'purple', 'at': 4, 'dt': 0.8})
S = 'Momentum and collisions'
B.spen(LESSON, S, 1, {'fig': [('box', .09, .15, .29, .35)], 'c': 'blue', 'at': 0}, {'fig': [('box', .55, .15, .81, .35)], 'c': 'orange', 'at': 0, 'dt': 3.0},
       {'fig': [('highlight', .21, .84, .79, .885)], 'c': 'blue', 'at': 1}, {'fig': [('box', .29, .6, .73, .8)], 'c': 'purple', 'at': 2},
       {'fig': [('circle', .78, .65, .05, .04)], 'c': 'purple', 'at': 2, 'dt': 1.5})
B.spen(LESSON, S, 2, {'fig': [('highlight', .21, .89, .79, .93)], 'c': 'red', 'at': 1})
S = 'Rotation: torque'
B.spen(LESSON, S, 0, {'fig': [('underline', .2, .75, .65)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .83, .16, .07, .05)], 'c': 'red', 'at': 2, 'dt': 1.5},
       {'fig': [('box', .06, .12, .34, .23)], 'c': 'orange', 'at': 3}, {'fig': [('underline', .21, .79, .93)], 'c': 'purple', 'at': 4},
       {'fig': [('circle', .2, .45, .05, .1)], 'c': 'purple', 'at': 5})
B.spen(LESSON, S, 1, *[{'fig': [('highlight', .06, y0, .94, y1)], 'c': 'orange', 'at': a, 'solo': True}
       for a, y0, y1 in ((1, .13, .24), (2, .24, .35), (3, .47, .58), (4, .58, .69), (5, .81, .92))])
S = 'Engineering example: sizing'
B.spen(LESSON, S, 0, {'fig': [('circle', .81, .5, .06, .1)], 'c': 'red', 'at': 1}, {'fig': [('underline', .11, .76, .46)], 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'fig': [('circle', .87, .68, .06, .04)], 'c': 'red', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .11, .33, .06, .1)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .73, .045, .07, .05)], 'c': 'orange', 'at': 0, 'dt': 3.0},
       {'fig': [('underline', .35, .82, .935)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('arrow', .11, .43, .78, .43)], 'c': 'blue', 'at': 0})
S = 'Gravity and orbits'
B.spen(LESSON, S, 1, {'fig': [('circle', .515, .28, .04, .06)], 'c': 'orange', 'at': 1}, {'fig': [('box', .57, .28, .97, .42)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .9, .35, .07, .07)], 'c': 'red', 'at': 3}, {'fig': [('underline', .63, .92, .63)], 'c': 'blue', 'at': 5},
       {'fig': [('underline', .59, .95, .745)], 'c': 'purple', 'at': 5, 'dt': 3.0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_pairs(ax, n, w, h):
    cx, by = w * 0.25, h * 0.42                          # left panel: forces ON the book (free-body diagram)
    rx = w * 0.75                                        # right panel: their partners
    if n >= 1:
        B.lab(ax, cx, h * 0.93, 'forces ON the book', 28)
        B.rect(ax, cx - 90, by, 180, 100, fc='#dfe8f7'); B.lab(ax, cx, by + 50, 'book', 28); B.anchor(ax, 'book', cx, by + 50)
    if n >= 2:
        B.arr(ax, cx, by + 100, cx, by + 290, 'blue', 4, 26); B.lab(ax, cx + 18, by + 250, 'N: table on book', 26, 'blue', ha='left')
        B.arr(ax, cx, by, cx, by - 200, 'red', 4, 26); B.lab(ax, cx + 18, by - 165, 'W: Earth on book', 26, 'red', ha='left')
    if n >= 3:
        B.ln(ax, [w * 0.52, w * 0.52], [h * 0.05, h * 0.97], c='gray', lw=1.5, ls='--')
        B.lab(ax, rx, h * 0.93, 'their partners', 28, 'green')
        ty = h * 0.55
        B.rect(ax, rx - 130, ty, 260, 30, fc='#e9dcc8'); B.lab(ax, rx + 150, ty + 15, 'table', 24, 'gray', ha='left')
        B.arr(ax, rx, ty + 210, rx, ty + 34, 'blue', 4, 26); B.lab(ax, rx, ty + 240, 'book on table', 26, 'blue')
        t = np.linspace(0.32 * np.pi, 0.68 * np.pi, 40)
        B.ln(ax, rx + 330 * np.cos(t), -190 + 330 * np.sin(t), c='green', lw=4); B.lab(ax, rx, 70, 'Earth', 26, 'green')
        B.arr(ax, rx, 140, rx, 330, 'red', 4, 26); B.lab(ax, rx + 18, 300, 'book on Earth', 26, 'red', ha='left')

B.insert(LESSON, 'Kinematics: describing motion', {'t': 'wb', 'h': 'Which equation? The missing-variable trick', 'steps': [
    {'say': "Students always ask which of the three equations to use. Here's the trick. There are five quantities: v naught, v, a, t, and the distance x. Each equation leaves exactly one of them out.",
     'w': [{'m': r'$v = v_0 + at$', 'at': 1}, {'m': r'$x = v_0 t + \frac{1}{2}at^2$', 'at': 1}, {'m': r'$v^2 = v_0^2 + 2ax$', 'at': 1},
           {'m': r'quantities:  $v_0,\ v,\ a,\ t,\ x$', 'c': 'blue', 'at': 2}]},
    {'say': "The first has no x. The second has no final v. The third has no t. So list what you know, find the one quantity the problem doesn't mention and doesn't ask for, and pick the equation that leaves it out.",
     'w': [{'m': 'no x      no v      no t', 'c': 'green', 'at': 0}]},
    {'say': "Example: a ball is thrown up at twenty meters per second. How high does it go? We know v naught is twenty, v at the top is zero, and a is gravity. Time isn't asked for, so use the equation with no t.",
     'w': [{'m': r'$v_0 = +20,\ v = 0,\ a = -9.8,\ x = ?$', 'at': 3, 'gap': 14}]},
    {'say': "Now the signs. Pick up as positive and stick with it. Then gravity is negative nine point eight, because it points down. Zero equals twenty squared plus two times negative nine point eight times x, so x is about twenty point four meters, matching what we found in calculus. Mixing sign conventions halfway through is the most common way to lose points.",
     'w': [{'m': 'choose  up = +  , then  a = −9.8', 'c': 'red', 'at': 1},
           {'m': r'$0 = 20^2 + 2(-9.8)\,x \;\Rightarrow\; x \approx 20.4\ \mathrm{m}$', 'box': True, 'at': 2}]},
]})

B.insert(LESSON, "Newton's three laws", {'t': 'wb', 'h': 'Third-law pairs act on different objects', 'draw': 'pairs', 'split': 0.40, 'steps': [
    {'say': "The third law causes more confusion than the other two combined. Here's the classic puzzle. A book rests on a table. Two forces act on it: its weight, the Earth pulling it down, and the normal force, the table pushing it up. They're equal and opposite. Is that a third law pair?",
     'w': [{'d': 1, 'at': 1}, {'d': 2, 'at': 2}, {'m': 'W and N: equal & opposite', 'at': 3}, {'m': 'a 3rd-law pair?', 'c': 'red', 'at': 4}]},
    {'say': "No! Both of those forces act on the same object, the book. They cancel because of the second law: the book isn't accelerating, so the net force on it is zero. A third law pair always acts on two different objects.",
     'w': [{'m': 'NO: both act on the book', 'c': 'red', 'at': 0}, {'m': 'they cancel by the 2nd law (a = 0)', 'at': 1}]},
    {'say': "The real partner of the weight is the book pulling the Earth up, just as hard. And the partner of the normal force is the book pushing down on the table. Each pair is the same kind of force, between the same two objects.",
     'w': [{'d': 3, 'at': 0}, {'m': 'pairs: Earth ↔ book,  table ↔ book', 'c': 'green', 'at': 2}]},
    {'say': "That also answers the horse and cart puzzle. If the cart pulls back on the horse as hard as the horse pulls the cart, how does anything move? Because the forces act on different objects. The cart moves if the pull on it beats the friction on it. And one more fix: mass, in kilograms, is how much stuff there is. Weight, in newtons, is a force, m times g.",
     'w': [{'m': 'pairs never cancel each other', 'c': 'blue', 'box': True, 'at': 2}, {'m': 'mass: kg  ·  weight W = mg: newtons', 'at': 4}]},
]})

G = 'Which equation? The missing-variable trick'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'$v^2 = v_0^2 + 2ax$', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'choose  up = +', 'c': 'red', 'at': 1})
G = 'Third-law pairs act on different objects'
B.pen(LESSON, G, 1, {'p': lambda A, w, h: [('circle', A['book'][0], A['book'][1], 120, 70)], 'c': 'red', 'at': 0})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'pairs never cancel', 'c': 'blue', 'at': 2})
