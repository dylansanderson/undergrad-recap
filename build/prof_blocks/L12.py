# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Big-O: how does the cost grow?', {'t': 'wb', 'h': 'Reading big-O straight off the code', 'cfs': 34, 'steps': [
    {'say': "Knowing the definition isn't enough. On exams and at work you have to read the big O right off the code. Rule one: a single loop over n items is order n. The body runs n times.",
     'w': [{'k': 'for (int i = 0; i < n; i++)  sum += a[i];', 'at': 1}, {'m': r'$\to O(n)$', 'c': 'blue', 'at': 2}]},
    {'say': "Rule two: nested loops multiply. For each of the n values of i, the inner loop runs n times, so the body runs n times n. Comparing every pair of items is order n squared.",
     'w': [{'k': 'for (int i = 0; i < n; i++)', 'at': 1, 'gap': 14}, {'k': '  for (int j = 0; j < n; j++)  check(a[i], a[j]);', 'at': 1},
           {'m': r'$n \times n \to O(n^2)$', 'c': 'red', 'at': 2}]},
    {'say': "Rule three: a loop that halves its range each time is logarithmic. Starting from n, how many halvings until you reach one? Log base two of n. That's binary search.",
     'w': [{'k': 'for (int k = n; k > 1; k = k / 2)  step();', 'at': 0, 'gap': 14}, {'m': r'$n,\ \frac{n}{2},\ \frac{n}{4},\ \ldots,\ 1$:  $\log_2 n$ steps $\to O(\log n)$', 'c': 'green', 'at': 2}]},
    {'say': "Combine them. A loop over n items with a binary search inside is n times log n. Statements one after another add, and then you keep only the biggest term: order n plus order n squared is just order n squared.",
     'w': [{'k': 'for (x : items)  BinarySearch(sorted, x);', 'at': 0, 'gap': 14}, {'m': r'$n \times \log n \to O(n\log n)$', 'c': 'purple', 'at': 1},
           {'m': r'in sequence: add, keep the biggest:  $O(n) + O(n^2) = O(n^2)$', 'at': 2}]},
]})

G = 'Reading big-O straight off the code'
B.pen(LESSON, G, 1, {'p': ('box',), 'on': '  for (int j = 0', 'c': 'red', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'k = k / 2', 'cols': (22, 31), 'c': 'green', 'at': 1})
