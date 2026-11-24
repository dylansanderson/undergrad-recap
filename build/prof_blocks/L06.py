# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Permutations and combinations', {'t': 'wb', 'h': 'Permutation or combination? Ask one question', 'steps': [
    {'say': "The most common question in counting: is this a permutation or a combination? Ask one thing. If I rearrange my choices, do I get a different outcome? If yes, order matters, and it's a permutation. If no, it's a combination.",
     'w': [{'m': 'Rearrange the choices: a different outcome?', 'c': 'blue', 'at': 1, 'fs': 44},
           {'m': 'yes  →  permutation (order matters)', 'at': 2}, {'m': 'no   →  combination (order does not)', 'at': 3}]},
    {'say': "Let's see it with four people, A, B, C, D, choosing two. As an ordered list there are twelve: A B, B A, A C, C A, and so on. That's P of four, two. But as a team, A B and B A are the same team, so every team was counted twice. Twelve over two factorial is six. That's C of four, two.",
     'w': [{'m': 'ordered: AB BA AC CA AD DA BC CB BD DB CD DC  = 12', 'at': 1, 'fs': 36},
           {'m': 'teams: {A,B} {A,C} {A,D} {B,C} {B,D} {C,D}  = 6', 'at': 3, 'fs': 36},
           {'m': r'$C(4,2) = \frac{P(4,2)}{2!} = \frac{12}{2} = 6$', 'c': 'green', 'at': 4}]},
    {'say': "Test yourself. Picking a president and a vice president from ten people: swapping them changes the outcome, so it's P of ten, two, ninety. Picking a two person committee: swapping changes nothing, so C of ten, two, forty five. A four digit PIN: digits can repeat, so it's neither. It's the product rule, ten to the fourth.",
     'w': [{'m': r'president + VP of 10:  $P(10,2) = 90$', 'at': 1}, {'m': r'2-person committee:  $C(10,2) = 45$', 'at': 2},
           {'m': r'4-digit PIN (repeats OK):  $10^4$', 'at': 4}]},
    {'say': "So there are really three formulas. Order matters with repeats allowed: n to the k. Order matters, no repeats: permutations. Order doesn't matter, no repeats: combinations.", 'clear': True,
     'w': [{'m': 'Three counting formulas', 'c': 'blue', 'at': 0, 'fs': 48},
           {'m': r'order matters, repeats allowed:   $n^k$', 'at': 1, 'fs': 48, 'gap': 20},
           {'m': r'order matters, no repeats:   $P(n,k) = \frac{n!}{(n-k)!}$', 'at': 2, 'fs': 48, 'gap': 20},
           {'m': r'order ignored, no repeats:   $C(n,k) = \frac{n!}{k!\,(n-k)!}$', 'at': 3, 'fs': 48, 'gap': 20}]},
]})

G = 'Permutation or combination? Ask one question'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'ordered: AB BA', 'c': 'red', 'at': 2}, {'p': ('underline',), 'on': 'teams:', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'president + VP', 'at': 1}, {'p': ('check',), 'on': '2-person committee', 'at': 2}, {'p': ('circle',), 'on': '4-digit PIN', 'c': 'orange', 'at': 4})
