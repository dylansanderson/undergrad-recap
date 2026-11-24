# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_cpm(ax, n, w, h):
    boxes = {'A': (60, h * 0.45, 'A  3 d'), 'B': (330, h * 0.70, 'B  5 d'), 'C': (330, h * 0.20, 'C  2 d'), 'D': (600, h * 0.45, 'D  2 d')}
    def node(k, col):
        x, y, t = boxes[k]; B.node(ax, x, y, 190, 80, t, fc='#dfe8f7' if col == 'ink' else '#fde3d3', c=col, fs=40)
    if n >= 1:
        for k in boxes: node(k, 'ink')
        B.arr(ax, 250, h * 0.45 + 60, 330, h * 0.70 + 30, 'gray', 2.5, 16); B.arr(ax, 250, h * 0.45 + 20, 330, h * 0.20 + 50, 'gray', 2.5, 16)
        B.arr(ax, 520, h * 0.70 + 30, 600, h * 0.45 + 60, 'gray', 2.5, 16); B.arr(ax, 520, h * 0.20 + 50, 600, h * 0.45 + 20, 'gray', 2.5, 16)
    if n >= 2:
        for k in 'ABD': node(k, 'red')
        B.lab(ax, 425, h * 0.93, 'critical path: A → B → D = 10 days', 36, 'red')
    if n >= 3: B.lab(ax, 425, h * 0.08, 'C has 3 days of slack', 36, 'green')

B.insert(LESSON, 'Planning, estimation and risk', {'t': 'wb', 'h': 'Worked example: velocity, critical path and risk', 'draw': 'cpm', 'split': 0.46, 'steps': [
    {'say': "Let's put real numbers on planning. The backlog holds one hundred twenty story points. The team finished eighteen, twenty two and twenty points in its first three sprints, so its velocity is about twenty. One hundred twenty over twenty is six more sprints. With two week sprints, that's about twelve weeks. Velocity is measured, not hoped for.",
     'w': [{'m': 'backlog: 120 points', 'at': 1}, {'m': 'velocity ≈ (18 + 22 + 20) / 3 = 20', 'c': 'blue', 'at': 2},
           {'m': '120 / 20 = 6 sprints ≈ 12 weeks', 'box': True, 'at': 4}]},
    {'say': "Now a dependency chart. Task A takes three days. B and C can start after A. D needs both. Each path from start to finish adds up: A, B, D is ten days. A, C, D is seven.",
     'w': [{'d': 1, 'at': 1}, {'m': 'A→B→D = 3 + 5 + 2 = 10 days', 'at': 3}, {'m': 'A→C→D = 3 + 2 + 2 = 7 days', 'at': 4}]},
    {'say': "The longest path is the critical path: it sets the earliest possible finish, ten days. Any delay on A, B or D delays the whole project. C has three days of slack, so it can slip without hurting anything. That tells a manager exactly where to put the best people.",
     'w': [{'d': 2, 'at': 0}, {'d': 3, 'at': 3}, {'m': 'longest path = the earliest finish', 'c': 'red', 'at': 1}]},
    {'say': "And risk exposure is probability times impact. If there's a thirty percent chance the Google sign in A P I changes, costing ten days, the expected cost is three days. Rank every risk that way, and mitigate the top few first.",
     'w': [{'m': 'risk exposure = probability × impact', 'c': 'purple', 'at': 0}, {'m': '0.3 × 10 days = 3 days', 'at': 1}]},
]})

G = 'Worked example: velocity, critical path and risk'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'velocity ≈', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'A→B→D = 3', 'c': 'red', 'at': 3})
