import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

def fig_why(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    items = [('Logic', 'if-statements,\nlogic gates,\nverification', C['lblue'], C['blue']), ('Counting', 'password strength,\nprobability,\nalgorithm cost', C['lorange'], C['orange']),
             ('Number theory', 'encryption (RSA),\nchecksums,\nhashing', C['lgreen'], C['green']), ('Graphs', 'maps & routing,\nnetworks,\ndependencies', C['lpurple'], C['purple'])]
    for i, (t, d, fc, ec) in enumerate(items):
        x = 2 + i * 24.5; box(ax, x, 6, 22.5, 42, '', fc=fc, ec=ec); txt(ax, x + 11.25, 41, t, 24, ec, bold=True); txt(ax, x + 11.25, 22, d, 22)
    txt(ax, 50, 53, 'Computers are discrete: bits, steps, finite states', 20, C['ink'], bold=True)
    save(fig, path)

def fig_truth(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    rows = [(p, q, int(p and q), int(p or q), int(not p), int(p != q), int((not p) or q)) for p in (0, 1) for q in (0, 1)]
    table(ax, 4, H - 2, ['p', 'q', 'p ∧ q', 'p ∨ q', '¬p', 'p ⊕ q', 'p → q'], rows, [10, 10, 14, 14, 12, 14, 18], 7.0, 23, hl={2}, hlc=C['lred'])
    save(fig, path)

def fig_demorgan(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    txt(ax, 50, 52, '¬(A ∧ B)  ≡  ¬A ∨ ¬B          ¬(A ∨ B)  ≡  ¬A ∧ ¬B', 24, C['ink'], bold=True)
    g = gate(ax, 'nand', 14, 28, 14)
    for (px, py), nm in zip(g['in'], 'AB'): wire(ax, [(6, py), (px, py)]); txt(ax, 5, py, nm, 20, ha='right')
    wire(ax, [g['out'], (36, 28)]); txt(ax, 22, 16, 'NAND', 19, C['mut'])
    txt(ax, 46, 28, '=', 36, C['blue'], bold=True)
    n1 = gate(ax, 'not', 58, 34, 6); n2 = gate(ax, 'not', 58, 22, 6); o = gate(ax, 'or', 72, 28, 14)
    wire(ax, [(54, 34), n1['in'][0]]); wire(ax, [(54, 22), n2['in'][0]]); txt(ax, 53, 34, 'A', 20, ha='right'); txt(ax, 53, 22, 'B', 20, ha='right')
    wire(ax, [n1['out'], (68, 34), (68, o['in'][0][1]), o['in'][0]]); wire(ax, [n2['out'], (68, 22), (68, o['in'][1][1]), o['in'][1]])
    wire(ax, [o['out'], (94, 28)]); txt(ax, 78, 16, 'OR of inverted inputs', 19, C['mut'])
    txt(ax, 50, 5, 'code:   !(a && b)  ==  !a || !b', 21, C['blue'], family='Consolas')
    save(fig, path)

def fig_quant(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    res = [1, 1, 1, 0, 1, 1, 1, 1]
    for i, r in enumerate(res):
        x = 8 + i * 11
        box(ax, x, 22, 9, 12, '✓' if r else '✗', fc=C['lgreen'] if r else C['lred'], ec=C['green'] if r else C['red'], fs=30, bold=True, r=0.5)
        txt(ax, x + 4.5, 18, f'test {i+1}', 15, C['mut'])
    txt(ax, 50, 44, '∀ tests: pass?   FALSE', 24, C['red'], bold=True)
    txt(ax, 50, 8, '∃ a test that fails (test 4) — one counterexample is enough', 20, C['ink'])
    save(fig, path)

def fig_proofs(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    cols = [('Direct', 'assume p\n↓\nlogical steps\n↓\nconclude q', C['lblue'], C['blue']),
            ('Contrapositive', 'assume ¬q\n↓\nlogical steps\n↓\nconclude ¬p', C['lorange'], C['orange']),
            ('Contradiction', 'assume ¬(claim)\n↓\nlogical steps\n↓\nimpossible!', C['lpurple'], C['purple'])]
    for i, (t, d, fc, ec) in enumerate(cols):
        x = 3 + i * 32.5; box(ax, x, 4, 29, 44, '', fc=fc, ec=ec); txt(ax, x + 14.5, 43, t, 21, ec, bold=True); txt(ax, x + 14.5, 22, d, 19)
    save(fig, path)

def fig_pigeon(path, w, h):
    fig, ax, H = canvas(w, h, need=44, exact=True)
    for i in range(4):
        x = 12 + i * 20; box(ax, x, 8, 16, 18, '', fc=C['pale'], ec=C['ink'], r=0.3); txt(ax, x + 8, 4, f'hole {i+1}', 16, C['mut'])
    birds = [(20, 17), (40, 17), (60, 17), (76, 17), (84, 17)]
    for j, (x, y) in enumerate(birds): ax.add_patch(Circle((x, y), 3, fc=C['orange'] if j >= 3 else C['blue'], zorder=4))
    txt(ax, 50, 36, '5 pigeons, 4 holes → some hole holds at least 2', 22, bold=True)
    save(fig, path)

def fig_domino(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    for i in range(9):
        x = 6 + i * 9.5; tilt = 0 if i > 3 else (60 - i * 12)
        r = np.radians(tilt); cx, cy = x, 10
        pts = [(cx, cy), (cx + 3 * np.cos(r), cy - 3 * np.sin(r)), (cx + 3 * np.cos(r) + 16 * np.sin(r), cy - 3 * np.sin(r) + 16 * np.cos(r)), (cx + 16 * np.sin(r), cy + 16 * np.cos(r))]
        ax.add_patch(Polygon(pts, fc=C['lorange'] if i == 0 else C['lblue'], ec=C['blue'], lw=2))
        txt(ax, x + 1.5, 6, f'n={i+1}', 15, C['mut'])
    line(ax, [(2, 10), (98, 10)], C['ink'], 2)
    txt(ax, 50, 40, 'base case: the first domino falls', 20, C['orange'], bold=True); txt(ax, 50, 33, 'inductive step: if domino k falls, domino k+1 falls', 20, C['blue'], bold=True)
    save(fig, path)

def fig_venn(path, w, h):
    fig, ax, H = canvas(w, h, need=64, exact=True)
    ax.add_patch(Circle((38, 32), 22, fc=C['blue'], alpha=0.25, ec=C['blue'], lw=3)); ax.add_patch(Circle((62, 32), 22, fc=C['orange'], alpha=0.25, ec=C['orange'], lw=3))
    txt(ax, 28, 32, '35', 30, C['blue'], bold=True); txt(ax, 50, 32, '25', 30, C['purple'], bold=True); txt(ax, 72, 32, '20', 30, C['orange'], bold=True)
    txt(ax, 30, 58, 'C++: 60', 22, C['blue'], bold=True); txt(ax, 70, 58, 'Python: 45', 22, C['orange'], bold=True)
    txt(ax, 50, 4, '|C ∪ P| = 60 + 45 − 25 = 80   (20 of 100 take neither)', 21, C['ink'], bold=True)
    save(fig, path)

def fig_funcs(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    titles = [('one-to-one\n(injective)', [(0, 1), (1, 2), (2, 0)], 3, 4), ('onto\n(surjective)', [(0, 0), (1, 0), (2, 1), (3, 2)], 4, 3), ('both\n(bijective)', [(0, 2), (1, 0), (2, 1)], 3, 3)]
    for k, (t, maps, na, nb) in enumerate(titles):
        x0 = 4 + k * 33
        ax.add_patch(matplotlib.patches.Ellipse((x0 + 5, 24), 9, 34, fc=C['pale'], ec=C['gray'])); ax.add_patch(matplotlib.patches.Ellipse((x0 + 22, 24), 9, 34, fc=C['pale'], ec=C['gray']))
        ya = [36 - i * (24 / max(1, na - 1)) for i in range(na)]; yb = [36 - i * (24 / max(1, nb - 1)) for i in range(nb)]
        for y in ya: dot(ax, x0 + 5, y, 1.0, C['blue'])
        for y in yb: dot(ax, x0 + 22, y, 1.0, C['orange'])
        for a, b in maps: arrow(ax, (x0 + 6, ya[a]), (x0 + 21, yb[b]), lw=2, ms=14)
        txt(ax, x0 + 13.5, 50, t, 19, bold=True)
    save(fig, path)

def fig_passwords(path, w, h):
    fig, ax = plot(w, h)
    labs = ['8 lower-\ncase\n26⁸', '8 mixed\n+ digits\n62⁸', '12 mixed\n+ digits\n62¹²', '6 random\nwords\n7776⁶']
    combos = [float(26 ** 8), float(62 ** 8), float(62 ** 12), float(7776 ** 6)]
    secs = [c / 1e10 for c in combos]
    def human(s):
        if s < 60: return f'{s:.0f} seconds'
        if s < 86400: return f'{s/3600:.0f} hours'
        if s < 3.15e7 * 2: return f'{s/86400:.0f} days'
        return f'{s/3.15e7:,.0f} years'
    b = ax.bar(labs, combos, color=[C['red'], C['orange'], C['green'], C['blue']]); ax.set_yscale('log'); ax.set_ylim(1e9, 1e25)
    for r, s in zip(b, secs): ax.text(r.get_x() + r.get_width() / 2, r.get_height() * 3, human(s), ha='center', fontsize=17, fontweight='bold')
    ax.set_ylabel('possible passwords'); ax.tick_params(axis='x', labelsize=15)
    ax.set_title('time to try them all at 10 billion guesses / second', fontsize=20)
    save(fig, path)

def fig_pascal(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    from math import comb
    for n in range(7):
        for k in range(n + 1):
            x = 50 + (k - n / 2) * 10; y = 52 - n * 7.5; hl = (n == 6 and k == 2)
            ax.add_patch(Circle((x, y), 3.3, fc=C['lorange'] if hl else C['lblue'], ec=C['orange'] if hl else C['blue'], lw=2))
            txt(ax, x, y, str(comb(n, k)), 18, bold=hl)
    txt(ax, 50, 2.5, 'each number = sum of the two above   ·   row 6, position 2:  C(6,2) = 15', 18, C['mut'])
    save(fig, path)

def fig_euclid(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    rows = [('252 = 2 × 105 + 42', 'gcd(252,105) = gcd(105,42)'), ('105 = 2 × 42 + 21', '= gcd(42,21)'), ('42 = 2 × 21 + 0', '= 21  ✓')]
    table(ax, 6, H - 3, ['divide', 'keep the remainder'], rows, [42, 46], 8, 24, hl={2}, hlc=C['lgreen'])
    save(fig, path)

def fig_clock(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    cx, cy, R = 28, 30, 22
    ax.add_patch(Circle((cx, cy), R, fc=C['pale'], ec=C['ink'], lw=3))
    for k in range(12):
        a = np.pi / 2 - k * 2 * np.pi / 12; v = 12 if k == 0 else k
        txt(ax, cx + (R - 4.5) * np.cos(a), cy + (R - 4.5) * np.sin(a), str(v), 20, C['orange'] if v == 3 else C['ink'], bold=v == 3)
    a3 = np.pi / 2 - 3 * 2 * np.pi / 12; line(ax, [(cx, cy), (cx + 12 * np.cos(a3), cy + 12 * np.sin(a3))], C['orange'], 4); dot(ax, cx, cy, 1.0)
    txt(ax, 76, 50, '15 ≡ 3  (mod 12)', 26, C['ink'], bold=True)
    txt(ax, 76, 38, '(9 + 8) mod 12 = 5', 22); txt(ax, 76, 30, '(7 × 5) mod 12 = 11', 22)
    txt(ax, 76, 16, 'arithmetic that wraps around —\nlike an n-bit register (mod 2ⁿ)', 18, C['mut'])
    save(fig, path)

def fig_rsa(path, w, h):
    fig, ax, H = canvas(w, h, need=64, exact=True)
    rows = [('pick primes', 'p = 3, q = 11'), ('modulus', 'n = pq = 33'), ('φ(n) = (p−1)(q−1)', '20'), ('public exponent', 'e = 3'),
            ('private exponent', 'd = 7   (3·7 = 21 ≡ 1 mod 20)'), ('encrypt m = 4', 'c = 4³ mod 33 = 64 mod 33 = 31'), ('decrypt', '31⁷ mod 33 = 4  ✓')]
    table(ax, 3, H - 2, ['step', 'toy example'], rows, [34, 60], 7.6, 21, hl={5, 6}, hlc=C['lgreen'])
    save(fig, path)

def fig_graph(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    pos = {'A': (12, 40), 'B': (36, 48), 'C': (34, 22), 'D': (60, 36), 'E': (84, 46), 'F': (82, 16)}
    edges = [('A', 'B', 4), ('A', 'C', 2), ('B', 'D', 5), ('C', 'D', 8), ('C', 'B', 1), ('D', 'E', 3), ('D', 'F', 6), ('E', 'F', 2)]
    for a, b, wgt in edges:
        line(ax, [pos[a], pos[b]], C['gray'], 3); mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        txt(ax, mx, my + 2, str(wgt), 18, C['orange'], bold=True)
    for n, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 4, fc=C['lblue'], ec=C['blue'], lw=2.5, zorder=4)); txt(ax, x, y, n, 20, bold=True)
    txt(ax, 50, 5, 'vertices = places, edges = roads (weights = minutes)   ·   Σ degrees = 2 × edges', 17, C['mut'])
    save(fig, path)

LESSON = {
 'code': 'MATH 170A', 'title': 'Mathematical Structures I', 'tag': 'Year 1 · Foundations', 'folder': 'MATH-170A Mathematical Structures I',
 'slides': [
 {'t': 'title', 'h': 'Mathematical Structures', 'sub': 'Logic, proof, sets, counting and number theory — the discrete math of computing', 'img': 'a:enigma',
  'say': "Welcome to Math one seventy A, Mathematical Structures, often called discrete mathematics. Calculus is about smooth, continuous change. But computers are discrete: bits, steps, finite states. This course gives you the math of that world: logic, proofs, sets, counting and number theory. The machine on screen is an Enigma, a World War Two cipher machine, and breaking it took exactly this kind of mathematics, plus some of the first electronic computing machines."},

 {'t': 'v', 'h': 'Where discrete math shows up', 'img': 'fig:why',
  'say': "Here's where you'll use it. Logic is the language of if statements in software and of logic gates in hardware, and it's how engineers formally verify that a chip design is correct. Counting tells you how strong a password is, how many cases a test must cover, and how long an algorithm takes. Number theory, the study of whole numbers and remainders, is the foundation of encryption, error checking codes and hash tables. And graphs, dots connected by lines, model road maps, computer networks, and the dependencies in a build system. Let's start with logic."},

 {'t': 'v', 'h': 'Propositions and truth tables', 'img': 'fig:truth',
  'pts': ['Proposition: a statement that is true or false', 'AND ∧, OR ∨, NOT ¬, XOR ⊕', 'Truth table: list every combination', 'p → q is false only when p is true and q is false'],
  'say': ["A proposition is a statement that's either true or false. It is raining. Two plus two equals four. We'll write them as letters, like p and q, and represent true as one and false as zero.",
          "We combine them with connectives. AND is true only when both are true. OR is true when at least one is true. NOT flips the value. And exclusive or, X O R, is true when exactly one is true. These are exactly the gates you'll build in digital logic.",
          "A truth table lists every combination of inputs. With two variables there are four rows. With n variables there are two to the n rows, which is why exhaustive testing of a big circuit is impossible.",
          "The trickiest connective is implication, p implies q. Think of it as a promise: if it rains, I'll bring an umbrella. The promise is only broken in one case: it rains and I don't bring the umbrella. If it doesn't rain, I haven't broken my promise either way. That's the highlighted row: true implies false is false, and every other row is true."]},

 {'t': 'v', 'h': "Equivalences and De Morgan's laws", 'img': 'fig:demorgan',
  'pts': ['Contrapositive: (p → q) ≡ (¬q → ¬p)', 'Converse (q → p) is NOT equivalent', "De Morgan: ¬(A ∧ B) ≡ ¬A ∨ ¬B", 'Simplify code and circuits'],
  'say': ["Two formulas are equivalent if they have the same truth table. The most useful equivalence for proofs: p implies q is equivalent to not q implies not p, the contrapositive. If it rains, the ground is wet, is the same as: if the ground isn't wet, it didn't rain.",
          "But the converse, q implies p, is not equivalent. If the ground is wet, it rained? No, maybe the sprinklers were on. Confusing a statement with its converse is one of the most common reasoning errors, in math and in life. There's also the inverse, not p implies not q: if it didn't rain, the ground isn't wet. That fails for the same reason, sprinklers. The inverse is actually equivalent to the converse, and neither is equivalent to the original.",
          "De Morgan's laws tell you how to push a NOT through an AND or an OR: flip each piece and swap AND with OR. Not A and B equals not A or not B. In hardware, that means a NAND gate is the same as an OR gate with inverted inputs.",
          "And in code, not open parenthesis a and b equals not a or not b. Programmers use this constantly to simplify conditions, and chip design tools use it to rearrange logic into whatever gates are cheapest."]},

 {'t': 'v', 'h': 'Quantifiers: for all, there exists', 'img': 'fig:quant', 'reveal': False,
  'pts': ['∀x P(x): P is true for every x', '∃x P(x): P is true for at least one x', 'Negation flips them: ¬∀x P(x) ≡ ∃x ¬P(x)', '"Not every test passes" = "some test fails"'],
  'say': "Statements about whole collections use quantifiers. For all, written as an upside down A, means the statement holds for every element. There exists, written as a backwards E, means it holds for at least one. For all integers x, x squared is at least zero: true. There exists an integer x with x squared equal to two: false. Negating a quantified statement flips the quantifier and negates the inside. Not every test passes is the same as: there exists a test that fails. To disprove a for all claim, you only need one counterexample. To prove it, you need an argument that covers every case, and that's what proofs are for."},

 {'t': 'v', 'h': 'Three ways to prove something', 'img': 'fig:proofs', 'split': 0.5,
  'pts': ['Direct: even + even = 2a + 2b = 2(a + b) → even', 'Contrapositive: n² even → n even  ⇔  n odd → n² odd', 'Contradiction: assume √2 = a/b in lowest terms … impossible'],
  'say': ["A proof is an argument that leaves no case uncovered. The direct method: start from what you know and march to the conclusion. Claim: the sum of two even numbers is even. Any even number is two times some integer, so write them as two a and two b. Their sum is two times a plus b, which is even. Done.",
          "Sometimes the contrapositive is easier. Claim: if n squared is even, then n is even. Prove the contrapositive instead: if n is odd, then n squared is odd. Odd n is two k plus one. Squaring gives four k squared plus four k plus one, which is two times something, plus one. Odd. Done.",
          "And proof by contradiction: assume the opposite and derive something impossible. The classic: the square root of two is irrational. Assume it equals a over b in lowest terms. Then a squared equals two b squared, so a squared is even, so a is even, using the result we just proved. Write a as two c: four c squared equals two b squared, so b squared is even, and b is even too. But then a over b wasn't in lowest terms. Contradiction. So root two can't be a fraction."]},

 {'t': 'v', 'h': 'Mathematical induction: the domino proof', 'img': 'fig:domino',
  'pts': ['Base case: true for n = 1', 'Step: if true for k, then true for k + 1', 'Example: 1 + 2 + … + n = n(n+1)/2', 'Same idea proves loops and recursion correct'],
  'say': ["Induction proves a statement for every positive integer at once. Picture an infinite row of dominoes. First, show the first domino falls. That's the base case.",
          "Then show that whenever domino k falls, it knocks over domino k plus one. That's the inductive step. Together, every domino falls.",
          "Example: one plus two plus up to n equals n times n plus one over two. Base case: n equals one, and one equals one times two over two. Inductive step: assume it's true for k. Then the sum up to k plus one is k times k plus one over two, plus k plus one. Factor out k plus one, and you get k plus one times k plus two, over two, which is the formula for k plus one. Done, for every n. Students often worry that this is circular: aren't we assuming what we want to prove? No. We assume it for one particular k, and show that this forces it to hold for the next one. On its own, that proves nothing. Only together with the base case, the first domino, does the chain reach every n.",
          "Computer scientists use induction to prove programs correct. A loop invariant is a statement that's true before the loop starts, the base case, and stays true after each pass, the step. And a recursive function is correct if its base case is right and each call correctly uses smaller calls."]},

 {'t': 'v', 'h': 'Sets and Venn diagrams', 'img': 'fig:venn',
  'pts': ['Union A ∪ B, intersection A ∩ B, complement', 'Inclusion–exclusion: |A ∪ B| = |A| + |B| − |A ∩ B|', '100 students: 60 C++, 45 Python, 25 both', '→ 80 take at least one, 20 take neither'],
  'say': ["A set is an unordered collection of distinct things. The union of A and B contains everything in either one. The intersection contains only what's in both. The complement is everything not in the set.",
          "To count a union, add the sizes, then subtract the overlap, because the overlap got counted twice. That's the inclusion exclusion principle.",
          "Example: in a group of one hundred students, sixty take C plus plus, forty five take Python, and twenty five take both.",
          "Sixty plus forty five minus twenty five is eighty students taking at least one, so twenty take neither. Databases do this all day: a SQL query with AND and OR conditions is set intersection and union, and you'll see it again in the databases course."]},

 {'t': 'v', 'h': 'Functions: mapping inputs to outputs', 'img': 'fig:funcs',
  'pts': ['Function: every input maps to exactly one output', 'One-to-one: no two inputs share an output', 'Onto: every output is hit', 'Bijection = both → it can be inverted (e.g. encryption)'],
  'say': ["A function assigns each input exactly one output. Mathematicians care about two special properties.",
          "One to one, or injective: different inputs always give different outputs. No collisions.",
          "Onto, or surjective: every possible output is actually produced by some input.",
          "A function that's both is a bijection, a perfect pairing, and only bijections can be undone. That's why an encryption function must be a bijection: every ciphertext has to decrypt to exactly one message. A hash function, on the other hand, squeezes huge inputs into a small range of outputs, so it can't be one to one. Collisions are guaranteed, and the next slides show why."]},

 {'t': 'v', 'h': 'Counting: how strong is your password?', 'img': 'fig:passwords',
  'pts': ['Product rule: k choices, n times → kⁿ', '8 lowercase letters: 26⁸ ≈ 2.1 × 10¹¹', '8 letters+digits mixed case: 62⁸ ≈ 2.2 × 10¹⁴', 'Length beats complexity: 62¹² ≈ 3.2 × 10²¹'],
  'say': ["The basic tool of counting is the product rule. If you make a sequence of choices, multiply the number of options at each step. A license plate with three letters and four digits has twenty six cubed times ten to the fourth, about a hundred seventy six million possibilities.",
          "Passwords. Eight lowercase letters gives twenty six to the eighth, about two hundred billion. A modern graphics card can try around ten billion guesses per second against a weakly protected password file, so that falls in about twenty seconds.",
          "Use upper case, lower case and digits, sixty two choices per character, and eight characters gives about two times ten to the fourteen. Now it takes about six hours. Better, but not good.",
          "Now go to twelve characters: sixty two to the twelfth, about three times ten to the twenty one, which takes roughly ten thousand years. Length matters more than anything, because it's in the exponent. And six words chosen at random from a list of seven thousand seven hundred seventy six are even stronger, hundreds of thousands of years at this rate, while being much easier to remember."]},

 {'t': 'v', 'h': 'Permutations and combinations', 'img': 'fig:pascal',
  'pts': ['Order matters → permutations: P(n,k) = n!/(n−k)!', 'Order doesn’t → combinations: C(n,k) = n!/(k!(n−k)!)', 'Pick 2 of 6 teammates: C(6,2) = 15', 'Lottery 6 of 49: C(49,6) = 13,983,816'],
  'say': ["When order matters, you're counting permutations. How many ways can first, second and third place be awarded among ten runners? Ten times nine times eight, seven hundred twenty. In general, n factorial over n minus k factorial.",
          "When order doesn't matter, you're counting combinations: divide out the k factorial ways to arrange each group. That's n choose k.",
          "How many ways to pick two people from six for a project? Six choose two: six times five over two, fifteen. And look at Pascal's triangle, where each number is the sum of the two above it. Row six, position two, is fifteen. Every entry is a combination.",
          "And a famous one: picking six numbers out of forty nine, which is how many lotteries work. Forty nine choose six is almost fourteen million. So each ticket has about a one in fourteen million chance. Counting is also the foundation of probability, which you'll study in engineering statistics."]},

 {'t': 'v', 'h': 'The pigeonhole principle', 'img': 'fig:pigeon', 'reveal': False,
  'pts': ['n + 1 pigeons, n holes → some hole has 2+', '367 people → two share a birthday (guaranteed)', 'More possible files than hash values → collisions are certain', 'Lossless compression can’t shrink every file'],
  'say': "Here's a deceptively simple idea. If you put more than n pigeons into n holes, at least one hole gets two pigeons. With three hundred sixty seven people in a room, two must share a birthday, because there are only three hundred sixty six possible birthdays. It sounds obvious, but it proves powerful facts. A hash function maps an unlimited number of possible files onto a fixed number of hash values, so collisions must exist. Security depends on making them hard to find, not impossible. And no compression program can shrink every file: there are fewer short files than long ones, so some inputs must get bigger. Whenever someone claims a perfect compression or a collision free hash, the pigeonhole principle says they're wrong."},

 {'t': 'v', 'h': 'Number theory: divisibility and the GCD', 'img': 'fig:euclid',
  'pts': ['Primes: only divisible by 1 and themselves', 'GCD: the largest common divisor', "Euclid's algorithm (≈ 300 BC): replace (a, b) with (b, a mod b)", 'gcd(252, 105) = 21 in three steps'],
  'say': ["Number theory studies the integers. A prime is a number greater than one divisible only by one and itself: two, three, five, seven, eleven. Every integer factors uniquely into primes. Twelve is two times two times three.",
          "The greatest common divisor of two numbers is the largest number that divides both. It's how you reduce fractions, like the Fraction class from object oriented programming.",
          "Finding it by factoring is slow for big numbers. Euclid's algorithm, more than two thousand years old, is fast: the GCD of a and b equals the GCD of b and the remainder of a divided by b. Repeat until the remainder is zero.",
          "Let's run it on two fifty two and one oh five. Two fifty two is two times one oh five plus forty two. So find the GCD of one oh five and forty two. One oh five is two times forty two plus twenty one. Forty two is two times twenty one plus zero. The answer is twenty one. Three steps. This ancient algorithm runs inside every secure web connection today."]},

 {'t': 'v', 'h': 'Modular arithmetic: math on a clock', 'img': 'fig:clock',
  'pts': ['a mod n = remainder after dividing by n', '15:00 is 3 o’clock: 15 ≡ 3 (mod 12)', 'Add and multiply, then take the remainder', 'Computer integers ARE mod 2ⁿ (overflow wraps)'],
  'say': ["Modular arithmetic is arithmetic that wraps around, like a clock. a mod n is the remainder when a is divided by n.",
          "Fifteen hundred hours is three o'clock, because fifteen mod twelve is three. We write fifteen is congruent to three, mod twelve.",
          "You can add and multiply first and take the remainder at the end, or take remainders along the way, and get the same answer. Nine plus eight is seventeen, which is five mod twelve. Seven times five is thirty five, which is eleven mod twelve.",
          "This isn't just a curiosity. A thirty two bit register in a C P U literally does arithmetic mod two to the thirty two, which is exactly why integers overflow and wrap around. Check digits on credit cards and book I S B Ns use modular arithmetic to catch typos. And hash tables use mod to pick a slot for each key."]},

 {'t': 'v', 'h': 'Putting it together: RSA encryption (toy version)', 'img': 'fig:rsa',
  'pts': ['Public key (n, e) — anyone can encrypt', 'Private key d — only you can decrypt', 'c = mᵉ mod n,  m = cᵈ mod n', 'Security: factoring a 600-digit n is infeasible'],
  'say': ["Here's the payoff of number theory: R S A, one of the public key encryption systems that has secured the internet. You publish a public key so anyone can encrypt a message to you.",
          "But only you hold the private key that decrypts it. Let's build a toy version. Pick two primes, three and eleven. Multiply: n equals thirty three. Compute phi of n, two times ten, which is twenty. Choose e equals three. Find d so that e times d is one, mod twenty: d equals seven, since twenty one mod twenty is one. Two terms to decode. Phi of n counts the numbers below n that share no factor with it, and for a product of two primes it's p minus one times q minus one. And d is called the modular inverse of e. For big numbers, it's found with an extended version of Euclid's algorithm, the same one from two slides ago.",
          "Encrypt the message four: four cubed is sixty four, and sixty four mod thirty three is thirty one. That's the ciphertext. To decrypt, compute thirty one to the seventh, mod thirty three, which comes out to four. The message is back.",
          "Why is it secure? Anyone can see n and e, but finding d requires knowing p and q. With thirty three, that's trivial. With an n that's six hundred digits long, nobody knows how to factor it in any reasonable time. The whole scheme rests on modular arithmetic, Euclid's algorithm, and primes."]},

 {'t': 'v', 'h': 'Graphs: dots and connections', 'img': 'fig:graph',
  'pts': ['Graph = vertices + edges (optionally weighted)', 'Degree: number of edges at a vertex', 'Handshake theorem: Σ degrees = 2 × edges', 'Maps, networks, social media, task dependencies'],
  'say': ["Finally, graphs. Not charts, but networks: a set of vertices connected by edges. Edges can have weights, like travel times between places.",
          "The degree of a vertex is how many edges touch it.",
          "A neat fact, called the handshake theorem: add up all the degrees and you get twice the number of edges, because every edge has two ends. So the number of odd degree vertices is always even.",
          "Graphs model road maps, where your navigation app searches for the shortest path. Here, the fastest route from A to E isn't the direct looking one. Computer networks, social networks, and the order in which files must be compiled are all graphs. You'll learn the algorithms that search them in data structures."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Logic to reason precisely, **proof** to be sure, **counting** to size problems, **number theory** to secure them.',
  'cap': 'Next: EGCP 180, Digital Logic — where these truth tables become real circuits.',
  'say': "To wrap up. Logic gives us a precise language, and truth tables, De Morgan's laws and implications are the same rules used in code and circuits. Proofs, direct, by contrapositive, by contradiction and by induction, let us be certain, not just confident. Sets and functions describe collections and mappings. Counting tells us how big a problem is, from passwords to probabilities. And number theory, with modular arithmetic and primes, underlies encryption and hashing. Next, we take those truth tables and build them out of real gates in digital logic. See you there."},
 ]}

# ---------------- whiteboard worked examples (written out live) ----------------
import board as B

def draw_tt(ax, n, w, h):
    cols = ['p', 'q', r'$p \to q$', r'$\neg p$', r'$\neg p \vee q$']; cw = [90, 90, 170, 110, 190]
    rows = [(1, 1, 1, 0, 1), (1, 0, 0, 0, 0), (0, 1, 1, 1, 1), (0, 0, 1, 1, 1)]
    x0, ytop, rh = 40, h - 60, 95
    xs = np.cumsum([x0] + cw)
    if n >= 1:
        for j, c in enumerate(cols): B.lab(ax, (xs[j] + xs[j + 1]) / 2, ytop, c, 36, 'blue')
        B.ln(ax, [x0, xs[-1]], [ytop - 40, ytop - 40], lw=2.5); B.ln(ax, [xs[2], xs[2]], [ytop + 30, ytop - 40 - 4 * rh], lw=2.5)
    for i, r in enumerate(rows):
        if n >= 2 + i:
            y = ytop - 40 - rh * (i + 0.5)
            for j, v in enumerate(r): B.lab(ax, (xs[j] + xs[j + 1]) / 2, y, str(v), 38, 'red' if (i == 1 and j in (2, 4)) else 'ink')
    if n >= 6:
        for j in (2, 4):
            B.rect(ax, xs[j] + 15, ytop - 40 - 4 * rh - 10, cw[j] - 30, 4 * rh + 20, c='green', lw=3)
        B.lab(ax, (x0 + xs[-1]) / 2, ytop - 40 - 4 * rh - 70, 'same column  →  equivalent', 32, 'green')

def draw_odd(ax, n, w, h):
    s = 120; X0, Y0 = (w - 4 * s) / 2, (h - 4 * s) / 2 + 40
    cols = ['#f6d6c4', '#dfe8f7', '#d8efe1', '#efe0f7']
    for k in range(1, 5):
        if n >= k:
            for i in range(k):
                for j in range(k):
                    if max(i, j) == k - 1: B.rect(ax, X0 + i * s, Y0 + j * s, s, s, fc=cols[k - 1], lw=2.5)
            B.lab(ax, X0 + 4 * s + 40, Y0 + (k - 0.5) * s, f'+{2 * k - 1}', 34, 'red', ha='left')
    if n >= 5: B.lab(ax, X0 + 2 * s, Y0 - 50, '1 + 3 + 5 + 7 = 16 = 4²', 34, 'green')

B.insert(LESSON, 'Propositions and truth tables', {'t': 'wb', 'h': 'Worked example: proving an equivalence with a truth table', 'draw': 'tt', 'split': 0.42, 'steps': [
    {'say': "Let's build a truth table by hand and use it to prove something. Claim: p implies q means exactly the same thing as not p, or q. Set up columns: p, q, p implies q, not p, and finally not p or q.",
     'w': [{'m': r'Claim:  $(p \to q) \equiv (\neg p \vee q)$', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "Row one: p true, q true. The promise is kept, so p implies q is one. Not p is zero, and zero or one is one. Row two: p true, q false. That's the broken promise: zero. Not p is zero, and zero or zero is zero.",
     'w': [{'d': 2, 'at': 0}, {'d': 3, 'at': 3}]},
    {'say': "Rows three and four: whenever p is false, the implication is automatically true. And not p is one, so not p or q is one as well.",
     'w': [{'d': 4}, {'d': 5, 'at': 1}]},
    {'say': "Now compare the two highlighted columns: one, zero, one, one, and one, zero, one, one. They match in every row, so the two formulas are equivalent. That's a complete proof. Checking every row is exactly how chip verification tools prove two circuits do the same thing.",
     'w': [{'d': 6, 'at': 1}, {'m': 'every row matches,', 'at': 2}, {'m': 'so the formulas are equivalent', 'c': 'red', 'box': True, 'at': 2}]},
]})

B.insert(LESSON, "Equivalences and De Morgan", {'t': 'wb', 'h': "Worked example: simplifying code with De Morgan", 'steps': [
    {'say': "Here's De Morgan in real code. Suppose a program has this condition: if not, open parenthesis, x is greater than five and y is less than three. It's correct, but hard to read. Let's simplify it.",
     'w': [{'m': 'if not (x > 5 and y < 3):', 'at': 1, 'fs': 44}]},
    {'say': "De Morgan says: push the not inside, negate each piece, and swap and with or. So it becomes: not x greater than five, or, not y less than three.",
     'w': [{'m': r'$\neg(A \wedge B) \equiv \neg A \vee \neg B$', 'c': 'blue', 'at': 0}, {'m': 'if not (x > 5) or not (y < 3):', 'at': 1, 'fs': 44}]},
    {'say': "Now negate each comparison. Not greater than five means less than or equal to five. Not less than three means greater than or equal to three. Be careful with the equals signs, because that's where most bugs hide.",
     'w': [{'m': 'not (x > 5)  →  x <= 5', 'at': 1}, {'m': 'not (y < 3)  →  y >= 3', 'at': 2}]},
    {'say': "So the final condition is: if x is at most five, or y is at least three. Test it with x equals seven and y equals one. The original: seven is greater than five and one is less than three, so the and is true, and not makes it false. The new version: seven at most five, false. One at least three, false. False or false is false. They agree.",
     'w': [{'m': 'if x <= 5 or y >= 3:', 'c': 'red', 'box': True, 'fs': 46}, {'m': 'test x = 7, y = 1:   original → False,   new → False', 'at': 1, 'c': 'gray', 'gap': 8}]},
]})

B.insert(LESSON, 'Mathematical induction', {'t': 'wb', 'h': 'Worked example: an induction proof you can see', 'draw': 'odd', 'split': 0.55, 'steps': [
    {'say': "Let's write out a complete induction proof. Claim: the sum of the first n odd numbers is n squared. One plus three plus five, up to two n minus one, equals n squared. Look at the picture: each new odd number is an L shaped layer that grows the square by one.",
     'w': [{'m': r'Claim:  $1 + 3 + 5 + \ldots + (2n-1) = n^2$', 'at': 1}, {'d': 4, 'at': 3}]},
    {'say': "Base case: n equals one. The left side is just one. The right side is one squared, also one. True.",
     'w': [{'m': r'Base, $n=1$:   $1 = 1^2$', 'at': 1}]},
    {'say': "Inductive step: assume it's true for k, so the first k odd numbers add up to k squared. Now add the next odd number, two k plus one. The sum becomes k squared plus two k plus one.",
     'w': [r'Assume:  $1 + 3 + \ldots + (2k-1) = k^2$', {'m': r'Add next:  $k^2 + (2k+1)$', 'at': 1}]},
    {'say': "But k squared plus two k plus one factors as k plus one, squared. That's exactly the formula for k plus one. So the statement holds for one, and each case pushes over the next, like dominoes. True for every n. And the picture agrees: one plus three plus five plus seven is sixteen, a four by four square.",
     'w': [{'m': r'$= (k+1)^2$', 'c': 'red', 'box': True}, {'m': 'true for all n', 'at': 2}, {'d': 5, 'at': 3}]},
]})

B.insert(LESSON, 'Permutations and combinations', {'t': 'wb', 'h': 'Worked example: PINs with no repeated digit', 'steps': [
    {'say': "Here's a counting problem worked by hand. How many four digit PINs are there in total? Each of the four positions can be any of ten digits, so by the product rule it's ten to the fourth, ten thousand.",
     'w': [{'m': r'All PINs:  $10 \times 10 \times 10 \times 10 = 10{,}000$', 'at': 2}]},
    {'say': "Now, how many have no repeated digit? The first digit has ten choices. The second can't match the first, so nine. The third has eight, and the fourth has seven. Ten times nine times eight times seven is five thousand and forty. That's a permutation: P of ten, four.",
     'w': [{'m': r'No repeats:  $10 \times 9 \times 8 \times 7$', 'at': 1}, {'m': r'$= P(10,4) = \frac{10!}{6!} = 5040$', 'at': 4}]},
    {'say': "And how many PINs have at least one repeated digit? Counting those directly is messy, so count the complement: all PINs minus the ones with no repeats. Ten thousand minus five thousand and forty is four thousand nine hundred sixty. Almost half of all PINs repeat a digit. When a direct count is hard, count what you don't want and subtract.",
     'w': [{'m': r'At least one repeat $= 10{,}000 - 5040$', 'at': 2}, {'m': r'$= 4960$', 'c': 'red', 'box': True, 'at': 3}]},
]})

B.insert(LESSON, 'Modular arithmetic', {'t': 'wb', 'h': 'Worked example: 3²⁰ mod 7 without a calculator', 'steps': [
    {'say': "Encryption needs huge powers mod n, so let's see the trick computers use. Find three to the twentieth, mod seven. Three to the twentieth is about three and a half billion, but we never need to compute it.",
     'w': [{'m': r'$3^{20}$ mod 7 = ?', 'at': 1}]},
    {'say': "Square repeatedly, reducing mod seven every time. Three to the first is three. Three squared is nine, which is two mod seven. Three to the fourth is two squared, four. Three to the eighth is four squared, sixteen, which is two. Three to the sixteenth is two squared, four.",
     'w': [{'m': r'$3^1 \equiv 3$', 'at': 1}, {'m': r'$3^2 = 9 \equiv 2$', 'at': 2}, {'m': r'$3^4 \equiv 2^2 = 4$', 'at': 3}, {'m': r'$3^8 \equiv 4^2 = 16 \equiv 2$', 'at': 4}, {'m': r'$3^{16} \equiv 2^2 = 4$', 'at': 5}]},
    {'say': "Twenty is sixteen plus four, so three to the twentieth is three to the sixteenth times three to the fourth. That's four times four, sixteen, which is two mod seven. Five small multiplications instead of a ten digit number. This is called square and multiply, and it's how R S A handles exponents hundreds of digits long.",
     'w': [{'m': r'$20 = 16 + 4$', 'at': 0}, {'m': r'$3^{20} = 3^{16}\cdot 3^4 \equiv 4 \cdot 4 = 16$', 'at': 1}, {'m': r'$3^{20} \equiv 2$  (mod 7)', 'c': 'red', 'box': True, 'at': 1}]},
]})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Where discrete math'
B.spen(LESSON, S, 0, *[{'fig': [('box', x0, .12, x1, .9)], 'c': c, 'at': a} for a, x0, x1, c in
       ((1, .015, .25, 'blue'), (2, .26, .495, 'orange'), (3, .505, .74, 'green'), (4, .75, .985, 'purple'))])
S = 'Propositions and truth tables'
B.spen(LESSON, S, 1, *[{'fig': [('box', x0, .03, x1, .88)], 'c': 'blue', 'at': a, 'solo': True} for a, x0, x1 in
       ((1, .24, .38), (2, .38, .52), (3, .52, .64), (4, .64, .78))])
B.spen(LESSON, S, 2, {'fig': [('box', .04, .2, .24, .88)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('box', .78, .03, .95, .88)], 'c': 'purple', 'at': 0}, {'fig': [('circle', .865, .625, .04, .08)], 'c': 'red', 'at': 4})
S = "Equivalences and De Morgan"
B.spen(LESSON, S, 2, {'fig': [('underline', .08, .45, .11)], 'c': 'blue', 'at': 0}, {'fig': [('box', .04, .36, .32, .65)], 'c': 'blue', 'at': 2},
       {'fig': [('box', .5, .33, .95, .7)], 'c': 'orange', 'at': 2, 'dt': 2.5})
B.spen(LESSON, S, 3, {'fig': [('underline', .22, .78, .93)], 'c': 'blue', 'at': 0})
S = 'Quantifiers'
B.spen(LESSON, S, 0, {'fig': [('underline', .31, .53, .165)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .455, .42, .06, .15)], 'c': 'red', 'at': 6},
       {'fig': [('underline', .1, .9, .885)], 'c': 'red', 'at': 6, 'dt': 1.5}, {'fig': [('circle', .62, .09, .07, .06)], 'c': 'red', 'at': 7})
S = 'Three ways to prove'
B.spen(LESSON, S, 0, {'fig': [('box', .025, .12, .325, .93)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .345, .12, .65, .93)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .675, .12, .975, .93)], 'c': 'purple', 'at': 0}, {'fig': [('circle', .825, .71, .11, .05)], 'c': 'red', 'at': 6})
S = 'Mathematical induction'
B.spen(LESSON, S, 0, {'fig': [('circle', .13, .7, .09, .1)], 'c': 'orange', 'at': 2}, {'fig': [('underline', .27, .73, .17)], 'c': 'orange', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('arrow', .36, .6, .44, .45)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .13, .87, .32)], 'c': 'blue', 'at': 1},
       {'fig': [('arrow', .45, .92, .9, .92)], 'c': 'blue', 'at': 2})
S = 'Sets and Venn'
B.spen(LESSON, S, 0, {'fig': [('circle', .38, .48, .22, .36)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .62, .48, .22, .36)], 'c': 'orange', 'at': 1, 'dt': 0.8},
       {'fig': [('circle', .5, .48, .05, .07)], 'c': 'purple', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .3, .07, .1, .05)], 'c': 'blue', 'at': 0, 'dt': 3.0}, {'fig': [('circle', .7, .07, .12, .05)], 'c': 'orange', 'at': 0, 'dt': 5.0},
       {'fig': [('circle', .5, .48, .05, .07)], 'c': 'purple', 'at': 0, 'dt': 7.0})
B.spen(LESSON, S, 3, {'fig': [('underline', .1, .9, .97)], 'c': 'red', 'at': 0})
S = 'Functions: mapping'
B.spen(LESSON, S, 1, {'fig': [('box', .04, .04, .33, .97)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('box', .37, .04, .66, .97)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .69, .04, .98, .97)], 'c': 'green', 'at': 0})
S = 'Counting: how strong'
B.spen(LESSON, S, 1, {'fig': [('circle', .27, .68, .1, .04)], 'c': 'red', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .455, .54, .08, .04)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .64, .215, .12, .04)], 'c': 'green', 'at': 0}, {'fig': [('circle', .83, .13, .12, .04)], 'c': 'blue', 'at': 2})
S = 'Permutations and combinations'
B.spen(LESSON, S, 2, {'fig': [('arrow', .35, .75, .39, .83)], 'c': 'blue', 'at': 2, 'dt': 1.5}, {'fig': [('arrow', .45, .75, .41, .83)], 'c': 'blue', 'at': 2, 'dt': 2.0},
       {'fig': [('circle', .4, .86, .04, .07)], 'c': 'red', 'at': 3})
S = 'The pigeonhole'
B.spen(LESSON, S, 0, {'fig': [('circle', .8, .6, .1, .25)], 'c': 'red', 'at': 1}, {'fig': [('underline', .11, .89, .235)], 'c': 'blue', 'at': 1, 'dt': 1.5})
S = 'Number theory'
B.spen(LESSON, S, 3, *[{'fig': [('highlight', .06, y0, .94, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in ((1, .25, .44), (3, .45, .64), (4, .65, .85))],
       {'fig': [('circle', .68, .75, .06, .08)], 'c': 'green', 'at': 5})
S = 'Modular arithmetic'
B.spen(LESSON, S, 1, {'fig': [('circle', .455, .48, .03, .05)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .6, .92, .19)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .61, .9, .405)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .6, .91, .545)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('underline', .56, .96, .805)], 'c': 'purple', 'at': 1})
S = 'Putting it together: RSA'
B.spen(LESSON, S, 1, *[{'fig': [('highlight', .03, y0, .97, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((2, .135, .25), (3, .25, .365), (4, .37, .485), (5, .49, .6), (6, .605, .72))])
B.spen(LESSON, S, 2, *[{'fig': [('highlight', .03, y0, .97, y1)], 'c': 'green', 'at': a, 'solo': True} for a, y0, y1 in ((0, .72, .84), (2, .845, .96))],
       {'fig': [('circle', .78, .9, .05, .05)], 'c': 'green', 'at': 3})
S = 'Graphs: dots'
B.spen(LESSON, S, 1, {'fig': [('circle', .6, .31, .05, .09)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('underline', .7, .97, .93)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, *[{'fig': [('arrow',) + a], 'c': 'green', 'at': 1, 'dt': t} for a, t in
       (((.14, .29, .32, .53), 0), ((.345, .52, .36, .15), .6), ((.39, .12, .57, .28), 1.2), ((.63, .28, .81, .15), 1.8))])

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
