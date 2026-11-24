# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_gsphere(ax, n, w, h):
    cx, cy, R = w * 0.5, h * 0.5, 200
    if n >= 1: B.dot(ax, cx, cy, c='red', s=16); B.lab(ax, cx - 22, cy + 30, '+Q', 30, 'red', ha='right')
    if n >= 2:
        t = np.linspace(0, 2 * np.pi, 200); B.ln(ax, cx + R * np.cos(t), cy + R * np.sin(t), c='blue', lw=3, ls='--')
        B.lab(ax, cx, cy - R - 120, 'imaginary sphere, radius r', 26, 'blue')
        B.arr(ax, cx, cy, cx + R * 0.707, cy + R * 0.707, 'gray', 2, 14); B.lab(ax, cx + R * 0.30, cy + R * 0.50, 'r', 28, 'gray')
    if n >= 3:
        for k in range(12):
            a = k * np.pi / 6; B.arr(ax, cx + R * np.cos(a), cy + R * np.sin(a), cx + (R + 75) * np.cos(a), cy + (R + 75) * np.sin(a), 'orange', 3, 18)
        B.lab(ax, cx, cy + R + 130, 'E: same size everywhere, straight out', 26, 'orange')

B.insert(LESSON, 'Electric fields and potential', {'t': 'wb', 'h': 'Force, field, energy, potential: four look-alikes', 'steps': [
    {'say': "These four quantities sound alike, and mixing them up is the most common mistake in this course. Let's put them side by side. Force, in newtons, is a vector: the push on a particular charge. Field is force per coulomb, also a vector. It describes the space itself, whether or not a charge is there.",
     'w': [{'m': r'force  $\vec F$ : newtons, VECTOR', 'at': 3}, {'m': r'field  $\vec E = \vec F/q$ : N/C, VECTOR', 'at': 4}]},
    {'say': "Potential energy, in joules, is a scalar: the energy a particular charge has at that spot. And potential, the voltage, is energy per coulomb: joules per coulomb, volts. Also a scalar. Notice the pattern: divide by the charge, and you go from a property of one charge to a property of the place.",
     'w': [{'m': r'potential energy  $U$ : joules, scalar', 'at': 0, 'gap': 14}, {'m': r'potential  $V = U/q$ : volts, scalar', 'at': 1},
           {'m': '÷ q :  one charge  →  the place itself', 'c': 'blue', 'at': 3}]},
    {'say': "Gravity has the same four. Your weight is a force. g, nine point eight newtons per kilogram, is the field. m g h is the potential energy. And g h alone is the potential. Height is to gravity what voltage is to charge.",
     'w': [{'m': 'gravity:  mg (F)   g (field)   mgh (U)   gh (potential)', 'c': 'green', 'at': 1}]},
    {'say': "And one more thing. Only differences in potential matter, just like only differences in height matter. Where you call zero volts is a choice. That's why a voltage is always measured between two points, and why every circuit needs a ground reference.",
     'w': [{'m': 'voltage = a DIFFERENCE between two points', 'c': 'red', 'box': True, 'at': 2, 'gap': 14}]},
]})

B.insert(LESSON, 'Gauss’s law', {'t': 'wb', 'h': "Worked example: Gauss's law finds a field in two lines", 'draw': 'gsphere', 'split': 0.5, 'steps': [
    {'say': "Gauss's law is a tool, so let's use it. Find the field at distance r from a point charge Q, without Coulomb's law. Step one: draw an imaginary closed surface that matches the symmetry. Here, a sphere of radius r centered on the charge.",
     'w': [{'d': 1, 'at': 1}, {'m': r'$\oint \vec E\cdot d\vec A = \frac{Q_{inside}}{\varepsilon_0}$', 'at': 2}, {'d': 2, 'at': 3}]},
    {'say': "Step two: use the symmetry. Every point on the sphere is the same distance from the charge, so the field has the same size everywhere on it, and points straight outward. So the flux integral is just E times the sphere's area, four pi r squared.",
     'w': [{'d': 3, 'at': 1}, {'m': r'$E\,(4\pi r^2) = \frac{Q}{\varepsilon_0}$', 'c': 'blue', 'at': 2}]},
    {'say': "Step three: solve for E. E equals Q over four pi epsilon naught r squared, which is exactly k Q over r squared, Coulomb's law. The same three steps, with a cylinder instead of a sphere, give the field of a long charged wire, which falls off as one over r instead of one over r squared.",
     'w': [{'m': r'$E = \frac{Q}{4\pi\varepsilon_0 r^2} = \frac{kQ}{r^2}$', 'c': 'red', 'box': True, 'at': 1},
           {'m': r'line of charge:  $E = \frac{\lambda}{2\pi\varepsilon_0 r}$', 'at': 2}]},
    {'say': "The recipe: pick a surface where the field is constant and perpendicular, pull E out of the integral, and divide by the area. If the problem has no symmetry, Gauss's law is still true, just not useful for calculation.",
     'w': [{'m': 'symmetry → constant E → pull it out', 'c': 'green', 'at': 0}]},
]})

G = 'Force, field, energy, potential: four look-alikes'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': '÷ q', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'voltage = a DIFFERENCE', 'c': 'red', 'at': 2})
G = "Worked example: Gauss's law finds a field in two lines"
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'(4\pi r^2)', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': r'= \frac{kQ}{r^2}$', 'at': 1})
