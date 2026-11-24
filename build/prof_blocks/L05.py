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
