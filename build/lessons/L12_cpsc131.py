import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_bigo(path, w, h):
    fig, ax = plot(w, h)
    n = np.logspace(0, 6, 200)
    for f, lab, c in ((np.log2(n), 'O(log n)', C['green']), (n, 'O(n)', C['blue']), (n * np.log2(n), 'O(n log n)', C['purple']), (n ** 2, 'O(n²)', C['orange']), (2.0 ** np.minimum(n, 60), 'O(2ⁿ)', C['red'])):
        ax.plot(n, f, color=c, label=lab, lw=3)
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_ylim(1, 1e13); ax.set_xlabel('input size n'); ax.set_ylabel('steps'); ax.legend(loc='lower right', ncol=2, fontsize=16)
    ax.set_title('n = 1,000,000 at 10⁹ steps/s:  n → 1 ms · n log n → 20 ms · n² → 17 min', fontsize=17)
    save(fig, path)

def fig_listarray(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    txt(ax, 4, 52, 'array / vector: one contiguous block', 20, C['blue'], ha='left', bold=True)
    for i, v in enumerate([12, 7, 31, 5, 18]):
        box(ax, 6 + i * 11, 36, 10, 10, str(v), fc=C['lblue'], fs=22, r=0.3); txt(ax, 11 + i * 11, 32, f'[{i}]', 16, C['mut'])
    txt(ax, 64, 41, 'a[3]: one step\ninsert at front:\nshift everything', 16, C['ink'], ha='left')
    txt(ax, 4, 25, 'linked list: nodes scattered, joined by pointers', 20, C['orange'], ha='left', bold=True)
    xs = [6, 30, 54, 78]
    for i, (x, v) in enumerate(zip(xs, [12, 7, 31, 5])):
        box(ax, x, 6, 10, 10, str(v), fc=C['lorange'], ec=C['orange'], fs=22, r=0.3); box(ax, x + 10, 6, 5, 10, '●', fc='white', ec=C['orange'], fs=14, r=0.3)
        if i < 3: arrow(ax, (x + 13, 11), (xs[i + 1], 11), color=C['orange'], lw=2.4)
    txt(ax, 94, 11, '∅', 22)
    save(fig, path)

def _stack(path, w, h, items, op):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    line(ax, [(30, 52), (30, 6), (70, 6), (70, 52)], C['ink'], 3)
    for i, v in enumerate(items):
        box(ax, 32, 8 + i * 9, 36, 8, v, fc=C['lorange'] if i == len(items) - 1 else C['lblue'], ec=C['orange'] if i == len(items) - 1 else C['blue'], fs=19)
    txt(ax, 50, 57, op, 20, C['ink'], bold=True)
    if items: txt(ax, 82, 8 + (len(items) - 1) * 9 + 4, '← top', 19, C['orange'], bold=True)
    save(fig, path)
def fig_stack1(p, w, h): _stack(p, w, h, ['typed "Hello"', 'bold "Hello"'], 'push, push')
def fig_stack2(p, w, h): _stack(p, w, h, ['typed "Hello"', 'bold "Hello"', 'deleted line 3'], 'push "deleted line 3"')
def fig_stack3(p, w, h): _stack(p, w, h, ['typed "Hello"', 'bold "Hello"'], 'Ctrl+Z → pop (undo the latest)')

def fig_queue(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    cx, cy, R = 28, 28, 20
    for k in range(8):
        a0 = 90 - k * 45
        ax.add_patch(matplotlib.patches.Wedge((cx, cy), R, a0 - 45, a0, width=8, fc=C['lblue'] if k in (2, 3, 4) else 'white', ec=C['blue'], lw=2))
        am = np.radians(a0 - 22.5); txt(ax, cx + (R - 4) * np.cos(am), cy + (R - 4) * np.sin(am), ['', '', 'A', 'B', 'C', '', '', ''][k], 20, bold=True)
    txt(ax, cx, cy, 'circular\nbuffer', 18, C['mut'])
    txt(ax, 76, 46, 'FIFO: first in, first out', 21, bold=True); txt(ax, 76, 34, 'enqueue at the tail,\ndequeue from the head', 18)
    txt(ax, 76, 16, 'keyboard & UART buffers,\nprint jobs, network packets', 17, C['mut'])
    save(fig, path)

def fig_fib(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    def node(x, y, n, depth):
        hl = n == 3 and depth >= 2
        box(ax, x - 4.5, y - 3, 9, 6, f'fib({n})', fc=C['lred'] if hl else C['lblue'], ec=C['red'] if hl else C['blue'], fs=14, r=0.6)
        if n >= 2 and depth < 3:
            dx = 24 / (2 ** depth)
            for k, m in ((-1, n - 1), (1, n - 2)):
                line(ax, [(x, y - 3), (x + k * dx, y - 10)], C['gray'], 1.5); node(x + k * dx, y - 13, m, depth + 1)
    node(50, 50, 5, 0)
    txt(ax, 50, 6, 'repeated work (red) → exponential time\nmemoize → linear time', 17, C['ink'])
    save(fig, path)

def _bsearch(path, w, h, step):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    arr = [3, 8, 12, 17, 23, 29, 37, 41, 48, 55, 62, 70, 77, 85, 91]
    lo, hi = 0, len(arr) - 1; hist = []
    while lo <= hi:
        mid = (lo + hi) // 2; hist.append((lo, hi, mid))
        if arr[mid] == 37: break
        if arr[mid] < 37: lo = mid + 1
        else: hi = mid - 1
    lo, hi, mid = hist[min(step, len(hist) - 1)]
    for i, v in enumerate(arr):
        inr = lo <= i <= hi
        fc = C['lorange'] if i == mid else (C['lblue'] if inr else '#F0F0F0')
        box(ax, 2 + i * 6.4, 18, 6, 9, str(v), fc=fc, ec=C['orange'] if i == mid else (C['blue'] if inr else '#D0D0D0'), fs=18, r=0.3, tc=C['ink'] if inr else '#B0B0B0')
    found = arr[mid] == 37
    txt(ax, 50, 38, f'step {min(step, len(hist) - 1) + 1}: check middle = {arr[mid]}' + ('  → found 37!' if found else ('  → 37 is bigger: keep right half' if arr[mid] < 37 else '  → 37 is smaller: keep left half')), 20, C['green'] if found else C['ink'], bold=True)
    txt(ax, 50, 8, 'each step halves the range: 1,000,000,000 items → about 30 steps', 18, C['mut'])
    save(fig, path)
for _k in range(4):
    globals()[f'fig_bsearch{_k}'] = (lambda kk: (lambda p, w, h: _bsearch(p, w, h, kk)))(_k)

def fig_merge(path, w, h):
    fig, ax, H = canvas(w, h, need=62, exact=True)
    levels = [[[38, 27, 43, 3, 9, 82, 10, 5]], [[38, 27, 43, 3], [9, 82, 10, 5]], [[38, 27], [43, 3], [9, 82], [10, 5]],
              [[27, 38], [3, 43], [9, 82], [5, 10]], [[3, 27, 38, 43], [5, 9, 10, 82]], [[3, 5, 9, 10, 27, 38, 43, 82]]]
    for li, groups in enumerate(levels):
        y = 56 - li * 10; n = sum(len(g) for g in groups); gap = 3; cw = 5.4
        total = n * cw + gap * (len(groups) - 1); x = 50 - total / 2
        for g in groups:
            for v in g:
                box(ax, x, y - 3.5, cw - 0.4, 7, str(v), fc=C['lblue'] if li < 3 else C['lgreen'], ec=C['blue'] if li < 3 else C['green'], fs=15, r=0.3); x += cw
            x += gap
    txt(ax, 6, 46, 'split', 18, C['blue'], bold=True); txt(ax, 6, 18, 'merge', 18, C['green'], bold=True)
    txt(ax, 50, 2.6, 'log₂n levels × n work per level = O(n log n)', 18, C['ink'], bold=True)
    save(fig, path)

def fig_hash(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    keys = [('"alice"', 3), ('"bob"', 1), ('"carol"', 3), ('"dave"', 6)]
    for i, (k, b) in enumerate(keys):
        y = 50 - i * 12
        box(ax, 2, y - 4, 16, 8, k, fc=C['lyellow'], ec=C['yellow'], fs=17)
        box(ax, 24, y - 4, 16, 8, 'hash % 8', fc=C['lpurple'], ec=C['purple'], fs=15); arrow(ax, (18, y), (24, y), lw=2)
        arrow(ax, (40, y), (58, 54 - b * 6.6 - 3), color=C['gray'], lw=1.6)
    for b in range(8):
        y = 54 - b * 6.6
        box(ax, 58, y - 6, 10, 6, str(b), fc=C['lblue'], fs=16, r=0.2)
    box(ax, 72, 54 - 1 * 6.6 - 6, 16, 6, 'bob', fc=C['lgreen'], ec=C['green'], fs=15, r=0.3)
    box(ax, 72, 54 - 3 * 6.6 - 6, 12, 6, 'alice', fc=C['lgreen'], ec=C['green'], fs=15, r=0.3); arrow(ax, (84, 54 - 3 * 6.6 - 3), (87, 54 - 3 * 6.6 - 3), lw=2)
    box(ax, 87, 54 - 3 * 6.6 - 6, 12, 6, 'carol', fc=C['lred'], ec=C['red'], fs=15, r=0.3)
    box(ax, 72, 54 - 6 * 6.6 - 6, 16, 6, 'dave', fc=C['lgreen'], ec=C['green'], fs=15, r=0.3)
    txt(ax, 86, 4, 'collision → chain', 16, C['red'])
    save(fig, path)

def fig_bst(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    pos = {50: (50, 48), 30: (28, 32), 70: (72, 32), 20: (16, 14), 40: (38, 14), 60: (62, 14), 80: (84, 14)}
    edges = [(50, 30), (50, 70), (30, 20), (30, 40), (70, 60), (70, 80)]
    path_ = [50, 30, 40]
    for a, b in edges: line(ax, [pos[a], pos[b]], C['orange'] if (a in path_ and b in path_) else C['gray'], 4 if (a in path_ and b in path_) else 2)
    for k, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 5, fc=C['lorange'] if k in path_ else C['lblue'], ec=C['orange'] if k in path_ else C['blue'], lw=2.5, zorder=4)); txt(ax, x, y, str(k), 20, bold=True)
    txt(ax, 50, 3, 'find 40: 50 → left → 30 → right → 40   (smaller left, larger right)', 18, C['ink'])
    save(fig, path)

def fig_heap(path, w, h):
    fig, ax, H = canvas(w, h, need=62, exact=True)          # room above the title (it touched the top edge)
    vals = [2, 5, 3, 9, 6, 8, 4]; pos = [(50, 52), (30, 38), (70, 38), (20, 22), (40, 22), (60, 22), (80, 22)]
    for i in range(1, 7): line(ax, [pos[(i - 1) // 2], pos[i]], C['gray'], 2)
    for i, (v, (x, y)) in enumerate(zip(vals, pos)):
        ax.add_patch(Circle((x, y), 5, fc=C['lorange'] if i == 0 else C['lblue'], ec=C['orange'] if i == 0 else C['blue'], lw=2.5, zorder=4)); txt(ax, x, y, str(v), 20, bold=True)
    for i, v in enumerate(vals):
        box(ax, 22 + i * 8, 4, 7.5, 7, str(v), fc=C['pale'], ec=C['gray'], fs=17, r=0.2); txt(ax, 25.75 + i * 8, 1, f'[{i}]', 13, C['mut'])
    txt(ax, 50, 14, 'stored as an array: children of i are 2i+1 and 2i+2', 16, C['mut'])
    txt(ax, 50, 59, 'min-heap: every parent ≤ its children → smallest at the top', 18, bold=True)
    save(fig, path)

def fig_dijkstra(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    pos = {'A': (8, 34), 'B': (32, 48), 'C': (30, 18), 'D': (56, 34), 'E': (78, 48), 'F': (88, 18)}
    edges = [('A', 'B', 4), ('A', 'C', 2), ('B', 'D', 5), ('C', 'D', 8), ('C', 'B', 1), ('D', 'E', 3), ('D', 'F', 6), ('E', 'F', 2)]
    best = {('A', 'C'), ('C', 'B'), ('B', 'D'), ('D', 'E'), ('E', 'F')}
    dist = {'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 11, 'F': 13}
    for a, b, wgt in edges:
        on = (a, b) in best; line(ax, [pos[a], pos[b]], C['orange'] if on else C['gray'], 4.5 if on else 2)
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2; txt(ax, mx, my + 2.2, str(wgt), 17, C['ink'], bold=True)
    for n, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 4.5, fc=C['lblue'], ec=C['blue'], lw=2.5, zorder=4)); txt(ax, x, y, n, 20, bold=True)
        txt(ax, x + (6 if n != 'F' else -7), y + 5.5, f'd={dist[n]}', 16, C['purple'], bold=True, bbox=dict(fc='white', ec='none', pad=0.5))
    txt(ax, 50, 58, 'Dijkstra from A: always settle the closest unsettled node next', 18, bold=True)
    txt(ax, 50, 3, 'shortest A→F = 13 via A → C → B → D → E → F (not the direct-looking route)', 16, C['orange'])
    save(fig, path)

def fig_choose(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    rows = [('fast access by position', 'array / vector', 'O(1)'), ('undo, recursion, parsing', 'stack', 'O(1) push/pop'), ('first-come first-served', 'queue', 'O(1)'),
            ('look up by key', 'hash table', 'O(1) average'), ('sorted order + search', 'balanced BST (std::map)', 'O(log n)'),
            ('always grab the min/max', 'heap (priority queue)', 'O(log n)'), ('connections, routes', 'graph', 'BFS / Dijkstra')]
    table(ax, 2, H - 2, ['you need …', 'use …', 'cost'], rows, [36, 36, 24], 7.6, 19)
    save(fig, path)

LESSON = {
 'code': 'CPSC 131', 'title': 'Data Structures', 'tag': 'Year 2 · Software', 'folder': 'CPSC-131 Data Structures',
 'slides': [
 {'t': 'title', 'h': 'Data Structures', 'sub': 'How to organize data so programs stay fast: lists, stacks, queues, hash tables, trees, heaps and graphs', 'img': 'a:card_catalog',
  'say': "Welcome to C P S C one thirty one, data structures. Before computers, libraries organized millions of cards in drawers like these, so you could find any book in minutes. A data structure is the same idea: a way of organizing data so that the operations you need are fast. In this lecture you'll learn how to measure speed with big O notation, and the core structures every programmer uses: arrays, linked lists, stacks, queues, hash tables, trees, heaps and graphs."},

 {'t': 'v', 'h': 'Big-O: how does the cost grow?', 'img': 'fig:bigo',
  'pts': ['Count steps as a function of input size n', 'Keep only the fastest-growing term', 'O(log n) ≪ O(n) ≪ O(n log n) ≪ O(n²) ≪ O(2ⁿ)', 'An algorithm choice can mean 1 ms vs 17 minutes'],
  'say': ["To compare data structures, we need a way to measure speed that doesn't depend on the computer. So we count steps as a function of the input size, n.",
          "And we only care about how that count grows for large n. If a loop takes three n plus five steps, we just say it's order n, written big O of n. Constants and smaller terms don't matter when n is a billion.",
          "Here are the common growth rates, on a log log chart. Logarithmic barely grows. Linear grows in step with n. n log n is a bit worse. n squared shoots up. And two to the n is hopeless beyond tiny inputs.",
          "The difference is dramatic. For a million items, on a computer doing a billion steps per second, a linear algorithm takes about a millisecond, n log n about twenty milliseconds, and n squared about seventeen minutes. Choosing the right algorithm often matters far more than buying a faster computer."]},

 {'t': 'v', 'h': 'Arrays vs. linked lists', 'img': 'fig:listarray',
  'pts': ['Array: contiguous → instant access a[i], cache-friendly', 'Inserting in the middle: shift everything → O(n)', 'Linked list: insert/remove anywhere in O(1) (given the node)', 'But reaching element i means walking → O(n)'],
  'say': ["The two most basic ways to store a sequence. An array, or vector, keeps elements side by side in one block of memory. To get element i, the computer just computes the address, start plus i times the element size. That's instant, order one. Arrays are also cache friendly, because the processor loads neighboring elements together, which makes them very fast in practice.",
          "But inserting at the front means shifting every other element over by one: order n.",
          "A linked list stores each element in its own node, scattered in memory, with a pointer to the next node. To insert, you just rewire two pointers. Order one.",
          "But to reach element i, you have to start at the head and follow i pointers. Order n. Every data structure is a set of tradeoffs like this. The skill is knowing which operations your program does most."]},

 {'t': 'v', 'h': 'Stacks: last in, first out', 'img': ['a:plates', 'fig:stack1', 'fig:stack2', 'fig:stack3'],
  'pts': ['push onto the top, pop from the top', 'Undo history, browser Back button', 'The call stack for function calls', 'Checking balanced brackets: ( [ { } ] )'],
  'say': ["A stack is like a stack of plates. You add to the top and take from the top. Last in, first out.",
          "Undo is a stack. Every action you take is pushed: you type hello, then make it bold.",
          "Then you delete a line. That's pushed on top.",
          "Press control Z, and the most recent action is popped off and undone first. The browser's back button works the same way. And the call stack you met in programming is literally a stack of function frames. Compilers also use stacks to check that brackets are balanced: push every opening bracket, and every closing bracket must match the one on top."]},

 {'t': 'v', 'h': 'Queues: first in, first out', 'img': 'fig:queue',
  'pts': ['enqueue at the back, dequeue from the front', 'Print jobs, network packets, task scheduling', 'Circular buffer: fixed array that wraps around', 'Used in every UART and keyboard driver'],
  'say': ["A queue is a line at a store: first in, first out. New items join at the back, and items leave from the front.",
          "Print jobs wait in a queue. Network routers queue packets. Operating systems queue processes that are ready to run.",
          "A neat way to build one is a circular buffer: a fixed size array where the head and tail indexes wrap around to the start when they reach the end, using the modulo operator from discrete math.",
          "This matters a lot in embedded systems. When bytes arrive on a serial port faster than your program can handle them, an interrupt routine drops them into a circular buffer, and the main program pulls them out later. You'll write exactly this in the embedded systems course."]},

 {'t': 'v', 'h': 'Recursion: functions that call themselves', 'img': 'fig:fib',
  'pts': ['Base case + a smaller version of the same problem', 'factorial(n) = n × factorial(n − 1), factorial(0) = 1', 'Naive Fibonacci recomputes subproblems → O(2ⁿ)', 'Memoization (cache answers) → O(n)'],
  'say': ["A recursive function solves a problem by calling itself on a smaller version of the same problem, until it reaches a base case it can answer directly.",
          "Factorial is the classic: n factorial is n times n minus one factorial, and zero factorial is one. Recursion is natural for anything that's defined in terms of smaller pieces of itself, like trees, file directories, and the merge sort we'll see shortly.",
          "But be careful. Fibonacci, where each number is the sum of the two before it, looks perfect for recursion. Yet the naive version recomputes the same values over and over. Look at the tree: fib of three, in red, gets computed again and again. The total work grows exponentially. Fibonacci of fifty would take hours.",
          "The fix is memoization: store each answer the first time you compute it, and look it up afterwards. Now each value is computed once, and the time drops to linear. That idea, solving subproblems once and reusing them, is called dynamic programming."]},

 {'t': 'v', 'h': 'Binary search: halve the problem every step', 'img': ['fig:bsearch0', 'fig:bsearch1', 'fig:bsearch2', 'fig:bsearch3'],
  'say': ["If the data is sorted, you can search it incredibly fast. Let's find thirty seven in this sorted array. Check the middle element: forty one. Thirty seven is smaller, so it must be in the left half. Throw away the right half entirely.",
          "Check the middle of what's left: seventeen. Thirty seven is bigger, so keep the right half.",
          "Middle again: twenty nine. Still smaller than thirty seven, keep the right part.",
          "Middle: thirty seven. Found it, in four steps out of fifteen elements. Each step halves the range, so a billion items take only about thirty steps, because two to the thirtieth is about a billion. That's logarithmic time, and it's why sorting data first often pays off."]},

 {'t': 'v', 'h': 'Sorting: from O(n²) to O(n log n)', 'img': 'fig:merge',
  'pts': ['Insertion sort: simple, O(n²) — fine for small n', 'Merge sort: split in half, sort each, merge', 'log n levels × n work each = O(n log n)', 'Quicksort / std::sort: O(n log n) in practice'],
  'say': ["Sorting is one of the most studied problems in computing. The simple approach, insertion sort, takes each item and slides it into place among the ones already sorted. It's easy and fine for small lists, but it's order n squared.",
          "Merge sort uses divide and conquer. Split the list in half, sort each half recursively, then merge the two sorted halves by repeatedly taking the smaller front element. Look at the picture: we split down to single elements, then merge back up.",
          "There are log n levels of splitting, and each level does order n work merging. So the total is n log n. For a million items, that's the difference between about twenty million steps and a trillion.",
          "In practice, you'll usually call the library's sort, like s t d sort in C plus plus, which uses a carefully tuned hybrid of quicksort and other methods, and runs in n log n time. But knowing why it's fast helps you recognize when your own code accidentally isn't."]},

 {'t': 'v', 'h': 'Hash tables: look things up in O(1)', 'img': 'fig:hash',
  'pts': ['Hash function turns a key into a bucket number', 'Lookup, insert, delete: O(1) on average', 'Collisions: two keys, same bucket → chain them', 'Python dicts, std::unordered_map, caches, databases'],
  'say': ["What if you want to find things by name, not by position? A hash table runs each key through a hash function that scrambles it into a number, then takes that number mod the table size to pick a bucket. Store the item in that bucket.",
          "To look it up later, hash the key again and go straight to the same bucket. No searching. On average, lookup, insert and delete are all order one, no matter how big the table is.",
          "By the pigeonhole principle, some keys must collide in the same bucket. Here, alice and carol both land in bucket three. The usual fix is chaining: each bucket holds a short list. As long as the table isn't too full, those lists stay tiny. If they don't, say a bad hash function sends every key to the same bucket, a lookup degrades into scanning one long list: order n. That's why the order one is always quoted as average case. Real hash tables grow and rehash automatically when they get too full to keep it that way.",
          "Hash tables are everywhere: Python dictionaries, C plus plus unordered maps, web caches, compilers' symbol tables, and the indexes inside databases. If you only remember one data structure from this course, make it this one."]},

 {'t': 'v', 'h': 'Binary search trees', 'img': 'fig:bst',
  'pts': ['Left subtree smaller, right subtree larger', 'Search, insert, delete: O(height)', 'Balanced → height ≈ log₂ n', 'std::map, databases (B-trees), file systems'],
  'say': ["A binary search tree keeps data sorted while still allowing fast inserts. Each node has up to two children. Everything in the left subtree is smaller, and everything in the right subtree is larger.",
          "To find forty, start at the root, fifty. Forty is smaller, go left to thirty. Forty is bigger, go right. Found it. The cost is the height of the tree.",
          "If the tree stays balanced, the height is about log base two of n, so a million items need only about twenty comparisons. But insert items in sorted order into a plain BST and it degenerates into a long chain, as slow as a linked list. Self balancing trees, like red black trees, rotate nodes to stay balanced automatically.",
          "The C plus plus s t d map is a red black tree. Databases and file systems use a wide, shallow cousin called a B tree, designed so that each node fills one disk block. You'll see B trees in the databases course."]},

 {'t': 'v', 'h': 'Heaps and priority queues', 'img': 'fig:heap',
  'pts': ['Always know the smallest (or largest) item', 'Insert and remove-min: O(log n)', 'Stored compactly in an array', 'OS schedulers, Dijkstra, event simulations'],
  'say': ["Sometimes you don't need everything sorted. You just need to repeatedly grab the most urgent item. That's a priority queue, usually built as a heap.",
          "In a min heap, every parent is smaller than its children, so the smallest item is always at the top. Inserting or removing the top takes order log n, by swapping an item up or down one level at a time.",
          "A heap is stored compactly in a plain array, with no pointers at all. The children of position i live at two i plus one and two i plus two.",
          "Operating systems use priority queues to decide which task runs next. Network routers use them to prioritize traffic. And the shortest path algorithm on the next slide uses one to always explore the closest location first."]},

 {'t': 'v', 'h': 'Graphs and shortest paths', 'img': 'fig:dijkstra',
  'pts': ['Store as adjacency lists (sparse) or a matrix (dense)', 'BFS explores level by level (queue)', 'DFS goes deep first (stack / recursion)', "Dijkstra: shortest weighted paths — how map apps route you"],
  'say': ["A graph is a set of nodes connected by edges, like the road map from discrete math. In code, we usually store it as adjacency lists: for each node, a list of its neighbors. For dense graphs, an adjacency matrix works too.",
          "Breadth first search explores a graph level by level using a queue: all neighbors first, then their neighbors. On an unweighted graph, it finds shortest paths in number of hops.",
          "Depth first search dives as deep as possible before backing up, using a stack or recursion. It's how you'd solve a maze, detect cycles, or order tasks that depend on each other.",
          "For weighted graphs, Dijkstra's algorithm finds shortest paths. Using a priority queue, it repeatedly settles the closest unsettled node and updates its neighbors' distances. Here, from A, the shortest path to F costs thirteen, going A, C, B, D, E, F, which is not the most direct looking route. Your phone's navigation app runs refined versions of this on a graph with millions of road segments."]},

 {'t': 'v', 'h': 'Choosing the right structure', 'img': 'fig:choose',
  'say': "Here's the summary table to keep. Need fast access by position? An array or vector. Undo, recursion or parsing? A stack. First come, first served? A queue. Look things up by a key? A hash table, with order one average time. Need things kept in sorted order with fast search? A balanced binary search tree, like s t d map. Always need the smallest or largest item next? A heap. Modeling connections, networks or routes? A graph, with breadth first search or Dijkstra. The standard libraries of every major language provide all of these, so in practice your job is mostly choosing well, and understanding the costs well enough to avoid accidentally writing an n squared program."},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Data structures trade costs. Measure with **Big-O**, then pick the structure whose **fast operations** match what your program does most.',
  'cap': 'Next: EGCP 280, Microcontrollers — programming the hardware directly in assembly.',
  'say': "To wrap up. Big O notation measures how cost grows with input size. Arrays give instant access, and linked lists give cheap insertion. Stacks and queues order work. Recursion and divide and conquer give us binary search and merge sort. Hash tables give constant time lookup. Trees keep data sorted, heaps keep the minimum handy, and graphs model connections, searched with B F S, D F S and Dijkstra. Next, we drop down to the hardware itself, programming microcontrollers in assembly language. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def _llnode(ax, x, y, v, fc='#dfe8f7'):
    B.rect(ax, x, y, 100, 80, fc=fc); B.rect(ax, x + 100, y, 50, 80, fc='white'); B.lab(ax, x + 50, y + 40, str(v), 34); B.dot(ax, x + 125, y + 40, s=8)

def draw_ll(ax, n, w, h):
    y = h * 0.62
    if n >= 1:
        for x, v in ((20, 10), (250, 20), (480, 30)): _llnode(ax, x, y, v)
        B.arr(ax, 145, y + 40, 245, y + 40, lw=3); B.lab(ax, 700, y + 40, 'null', 26, 'gray'); B.arr(ax, 605, y + 40, 665, y + 40, 'gray', 2.5, 22)
        B.lab(ax, 45, y + 110, 'head', 26, 'gray'); B.lab(ax, 300, y + 110, 'prev', 26, 'blue')
    old = 'gray' if n >= 4 else 'ink'
    if n >= 1: B.arr(ax, 375, y + 40, 475, y + 40, old, 3 if n < 4 else 2, 26 if n < 4 else 18, '-|>')
    if n >= 4: B.lab(ax, 425, y + 70, '✗', 34, 'red')
    if n >= 2: _llnode(ax, 300, y - 250, 25, '#f6d6c4'); B.lab(ax, 375, y - 290, 'new node n', 26, 'orange')
    if n >= 3: B.arr(ax, 425, y - 210, 530, y - 5, 'green', 3.5); B.lab(ax, 530, y - 120, '①', 34, 'green')
    if n >= 4: B.arr(ax, 375, y + 15, 345, y - 165, 'green', 3.5); B.lab(ax, 300, y - 80, '②', 34, 'green')

def draw_brackets(ax, n, w, h):
    rows = [('{', 'push', '{'), ('[', 'push', '{ ['), ('(', 'push', '{ [ ('), (')', 'pop (  ok', '{ ['), (']', 'pop [  ok', '{'), ('}', 'pop {  ok', '(empty)')]
    B.table(ax, 20, h - 30, ['char', 'action', 'stack'], rows, [110, 230, 260], 70, nrows=max(0, n - 1) if n < 7 else 6, fs=32, hl={(5, 2): 'green'})
    if n >= 7: B.lab(ax, w / 2, h - 30 - 70 * 7.6, 'empty at the end: balanced', 30, 'green')

def draw_fact(ax, n, w, h):
    ys = [h - 120, h - 270, h - 420, h - 570]
    for k in range(4):
        if n >= k + 1:
            B.node(ax, 40 + k * 95, ys[k], 260, 90, f'Fact({4 - k})', fc='#dfe8f7' if k < 3 else '#e3f2e8', fs=32)
            if k: B.arr(ax, 40 + (k - 1) * 95 + 60, ys[k - 1], 40 + k * 95 + 60, ys[k] + 90, 'blue', 2.5, 22)
    if n >= 4: B.lab(ax, 40 + 3 * 95 + 290, ys[3] + 45, 'base case: 1', 30, 'green', ha='left')
    rets = ['= 4 × 6 = 24', '= 3 × 2 = 6', '= 2 × 1 = 2']
    for k in (2, 1, 0):
        if n >= 5 + (2 - k):
            B.lab(ax, 40 + k * 95 + 290, ys[k] + 45, rets[k], 30, 'red', ha='left')

def draw_bsearch(ax, n, w, h):
    a = [3, 8, 15, 21, 27, 34, 42, 50, 63, 71, 88]; cw = 68; x0 = 20
    steps = [(0, 10, 5), (0, 4, 2), (3, 4, 3)]
    for r, (lo, hi, mid) in enumerate(steps):
        if n >= r + 1:
            y = h - 140 - r * 200
            for i, v in enumerate(a):
                fc = '#f6d6c4' if i == mid else ('#dfe8f7' if lo <= i <= hi else '#f0f0f0')
                B.node(ax, x0 + i * cw, y, cw, 70, str(v), fc=fc, fs=26, tc='ink' if lo <= i <= hi else 'gray', lw=1.8)
                B.anchor(ax, f'r{r}c{i}', x0 + i * cw + cw / 2, y + 35)          # cell centre, for the pen
            B.lab(ax, x0 + lo * cw + cw / 2, y - 25, 'lo', 22, 'blue'); B.lab(ax, x0 + hi * cw + cw / 2, y - 25, 'hi', 22, 'blue')
            B.lab(ax, x0 + mid * cw + cw / 2, y + 95, 'mid', 22, 'orange')
    if n >= 3: B.lab(ax, x0 + 3 * cw + cw / 2, h - 140 - 2 * 200 - 70, 'found 21!', 32, 'green')

def draw_bst(ax, n, w, h):
    P = {50: (w / 2, h - 90), 30: (w / 2 - 200, h - 250), 70: (w / 2 + 200, h - 250), 20: (w / 2 - 300, h - 410), 40: (w / 2 - 100, h - 410), 60: (w / 2 + 100, h - 410), 80: (w / 2 + 300, h - 410)}
    par = {30: 50, 70: 50, 20: 30, 40: 30, 60: 70, 80: 70}
    order = [50, 30, 70, 20, 40, 60, 80]
    path = {50, 70, 60} if n >= 8 else set()
    for k, v in enumerate(order):
        if n >= k + 1:
            if v in par: B.ln(ax, [P[par[v]][0], P[v][0]], [P[par[v]][1] - 38, P[v][1] + 38], c='green' if v in path and par[v] in path else 'ink', lw=4 if v in path else 2.5)
            t = np.linspace(0, 2 * np.pi, 60)
            B.poly(ax, list(zip(P[v][0] + 40 * np.cos(t), P[v][1] + 40 * np.sin(t))), fc='#e3f2e8' if v in path else '#dfe8f7', c='green' if v in path else 'ink')
            B.lab(ax, *P[v], str(v), 32)

def draw_hash(ax, n, w, h):
    y0 = h - 70; bh = 85
    for b in range(7):
        if n >= 1:
            B.node(ax, 30, y0 - (b + 1) * bh, 110, bh, str(b), fc='#efe0f7', fs=30, lw=2)
    items = [(14, 0, 0), (23, 2, 0), (9, 2, 1), (31, 3, 0), (6, 6, 0)]
    for k, (key, b, pos) in enumerate(items):
        if n >= k + 2:
            x = 190 + pos * 170; y = y0 - (b + 1) * bh + 10
            B.node(ax, x, y, 130, bh - 20, str(key), fc='#f6d6c4' if pos else '#dfe8f7', fs=30)
            B.arr(ax, x - 50 if pos == 0 else x - 40, y + (bh - 20) / 2, x - 2, y + (bh - 20) / 2, 'gray', 2.5, 20)
    if n >= 4: B.lab(ax, 540, y0 - 3 * bh + 42 + 50, 'collision: chain it', 26, 'red', ha='left')

B.insert(LESSON, 'Arrays vs. linked lists', {'t': 'wb', 'h': 'Worked example: inserting into a linked list', 'lang': 'cpp', 'draw': 'll', 'split': 0.44, 'steps': [
    {'say': "Let's insert the value twenty five into the middle of a linked list, between twenty and thirty. Each node holds a value and a pointer to the next node. We already have a pointer, prev, to the node holding twenty.",
     'w': [{'k': 'struct Node {', 'at': 1}, {'k': '  int value;', 'at': 1}, {'k': '  Node* next;', 'at': 1}, {'k': '};', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "Step one: create the new node on the heap, holding twenty five. Right now, it isn't connected to anything.",
     'w': [{'k': 'Node* n = new Node{25, nullptr};', 'gap': 14, 'at': 0}, {'d': 2, 'at': 0}]},
    {'say': "Step two: point the new node at whatever prev currently points to, which is thirty. Now both twenty and twenty five point to thirty.",
     'w': [{'k': 'n->next = prev->next;   // 25 -> 30', 'at': 0}, {'d': 3, 'at': 0}]},
    {'say': "Step three: point prev at the new node. The old link from twenty to thirty is replaced, and the list reads ten, twenty, twenty five, thirty. No element moved in memory. That's why insertion is constant time.",
     'w': [{'k': 'prev->next = n;         // 20 -> 25', 'at': 0}, {'d': 4, 'at': 0}, {'m': 'list: 10 → 20 → 25 → 30', 'c': 'green', 'gap': 12, 'at': 1}]},
    {'say': "The order of those two lines is critical. Swap them, and prev points to twenty five before twenty five knows about thirty. The rest of the list is lost forever. When you edit pointers, always connect the new node first.",
     'w': [{'m': 'Connect the new node first, then relink!', 'c': 'red', 'gap': 8, 'at': 1}]},
]})

B.insert(LESSON, 'Stacks: last in, first out', {'t': 'wb', 'h': 'Worked example: are the brackets balanced?', 'draw': 'brackets', 'split': 0.4, 'steps': [
    {'say': "Compilers check brackets with a stack. Let's trace the string curly, square, round, close round, close square, close curly. The rule: push every opening bracket. For every closing bracket, pop the top and check that it matches.",
     'w': [{'m': 'input:  { [ ( ) ] }', 'fs': 46, 'at': 1}, {'m': 'open: push', 'at': 2}, {'m': 'close: pop, must match', 'at': 3}, {'d': 1, 'at': 3}]},
    {'say': "Curly: push. Square: push. Round: push. The stack now holds three brackets, with the round one on top.",
     'w': [{'d': 2, 'at': 0}, {'d': 3, 'at': 1}, {'d': 4, 'at': 2}]},
    {'say': "Close round: pop, and the top was round. A match. Close square: pop square, match. Close curly: pop curly, match.",
     'w': [{'d': 5, 'at': 0}, {'d': 6, 'at': 2}, {'d': 7, 'at': 3}]},
    {'say': "The stack is empty at the end, so the brackets are balanced. Now try round, then close square. Push round. Then close square pops round, which doesn't match. Error. That's exactly the message your compiler gives you, and it works because the most recent opening bracket must be the first one closed. Last in, first out.",
     'w': [{'m': 'input  ( ]', 'gap': 14, 'at': 1}, {'m': 'pop "(" but saw "]":  NOT balanced', 'c': 'red', 'at': 3}]},
]})

B.insert(LESSON, 'Recursion: functions that call themselves', {'t': 'wb', 'h': 'Worked example: tracing a recursive function', 'lang': 'cpp', 'draw': 'fact', 'split': 0.48, 'steps': [
    {'say': "Here's factorial written recursively. Every recursive function needs two parts. A base case that stops: if n is at most one, return one. And a recursive case that makes the problem smaller: n times factorial of n minus one.",
     'w': [{'k': 'int Fact(int n) {', 'at': 1}, {'k': '  if (n <= 1) return 1;      // base case', 'at': 2}, {'k': '  return n * Fact(n - 1);    // smaller problem', 'at': 3}, {'k': '}', 'at': 3}]},
    {'say': "Call Fact of four. It can't answer yet, so it calls Fact of three, which calls Fact of two, which calls Fact of one. Each call waits on the stack.",
     'w': [{'d': 1, 'at': 0}, {'d': 2, 'at': 1}, {'d': 3, 'at': 1}, {'d': 4, 'at': 1}, {'m': 'calls go down, waiting...', 'at': 1, 'c': 'blue'}]},
    {'say': "Fact of one hits the base case and returns one. Now the answers come back up. Fact of two returns two times one, two. Fact of three returns three times two, six. And Fact of four returns four times six, twenty four.",
     'w': [{'d': 5, 'at': 2}, {'d': 6, 'at': 3}, {'d': 7, 'at': 4}, {'m': '...answers come back up', 'at': 4, 'c': 'red'}]},
    {'say': "Forget the base case, and the calls never stop, until the stack runs out of memory. That's a stack overflow, and it's the classic recursion bug.",
     'w': [{'m': 'no base case = stack overflow', 'c': 'red', 'box': True, 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Binary search', {'t': 'wb', 'h': 'Worked example: binary search for 21', 'draw': 'bsearch', 'split': 0.3, 'steps': [
    {'say': "Let's find twenty one in this sorted array of eleven numbers. Low starts at index zero, high at index ten. The middle is index five, which holds thirty four. Thirty four is bigger than twenty one, so twenty one must be in the left half.",
     'w': [{'m': 'find 21', 'fs': 46}, {'d': 1, 'at': 1},
           {'p': lambda A, w, h: [('circle', 'r0c0', 30, 42), ('circle', 'r0c10', 30, 42)], 'c': 'blue', 'at': 1},
           {'p': lambda A, w, h: [('circle', 'r0c5', 33, 39)], 'at': 2},
           {'m': 'mid = 5: 34 > 21', 'at': 3}, {'m': 'so hi = 4', 'c': 'blue', 'at': 3},
           {'p': lambda A, w, h: [('strike', A['r0c5'][0] - 30, A['r0c5'][1], A['r0c10'][0] + 30, A['r0c10'][1])], 'at': 3}]},
    {'say': "Now low is zero, high is four, and the middle is index two, holding fifteen. Fifteen is smaller than twenty one, so move low up to three.",
     'w': [{'d': 2, 'at': 0}, {'p': lambda A, w, h: [('circle', 'r1c2', 33, 39)], 'at': 0}, {'m': 'mid = 2: 15 < 21'},
           {'p': lambda A, w, h: [('strike', A['r1c0'][0] - 30, A['r1c0'][1], A['r1c2'][0] + 30, A['r1c2'][1])], 'at': 1},
           {'m': 'so lo = 3', 'c': 'blue', 'at': 1},
           {'p': lambda A, w, h: [('arrow', A['r1c0'][0], A['r1c0'][1] - 88, A['r1c3'][0] - 6, A['r1c3'][1] - 88)], 'c': 'blue', 'at': 1}]},
    {'say': "Low is three, high is four, and the middle is index three. It holds twenty one. Found it, in three comparisons.",
     'w': [{'d': 3, 'at': 0}, {'p': lambda A, w, h: [('circle', 'r2c3', 34, 40)], 'c': 'green', 'at': 1},
           {'m': 'mid = 3: found!', 'c': 'green', 'at': 2}, {'p': ('check',), 'on': 'found!', 'c': 'green', 'at': 2}]},
    {'say': "A linear scan could take up to eleven comparisons. Binary search halves the range every step, so even a billion sorted items need only about thirty comparisons. That's the power of log n. The catch: the data must be sorted first.",
     'w': [{'m': r'$\log_2(10^9) \approx 30$ steps', 'c': 'red', 'box': True, 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Binary search trees', {'t': 'wb', 'h': 'Worked example: building and searching a BST', 'draw': 'bst', 'split': 0.36, 'steps': [
    {'say': "Let's build a binary search tree by inserting fifty, thirty, seventy, twenty, forty, sixty, eighty, in that order. Fifty becomes the root. Thirty is smaller, so it goes left. Seventy is bigger, so it goes right.",
     'w': ['insert: 50 30 70 20 40 60 80', {'d': 1, 'at': 1}, {'d': 2, 'at': 2}, {'d': 3, 'at': 3}]},
    {'say': "Twenty: smaller than fifty, go left. Smaller than thirty, go left again. Forty: left of fifty, but bigger than thirty, so right. Sixty: right of fifty, left of seventy. Eighty: right, then right.",
     'w': [{'d': 4, 'at': 0}, {'d': 5, 'at': 2}, {'d': 6, 'at': 3}, {'d': 7, 'at': 4}]},
    {'say': "Now search for sixty. Compare with fifty: bigger, go right. Compare with seventy: smaller, go left. Sixty. Found in three comparisons. Each comparison throws away half of what's left, just like binary search.",
     'w': [{'m': 'search 60:', 'at': 0}, {'m': '60 > 50: right', 'at': 1}, {'m': '60 < 70: left', 'at': 2}, {'m': 'found!', 'c': 'green', 'at': 3}, {'d': 8, 'at': 3}]},
    {'say': "But watch out: insert the same numbers already sorted, ten, twenty, thirty, and every node goes right. The tree becomes a linked list, and search slows to order n. That's why real libraries use self balancing trees.",
     'w': [{'m': 'sorted input makes a "stick": O(n)', 'c': 'red', 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Hash tables', {'t': 'wb', 'h': 'Worked example: filling a hash table', 'draw': 'hash', 'split': 0.42, 'steps': [
    {'say': "Let's insert five keys into a hash table with seven buckets. The hash function is the key mod seven: the remainder after dividing by seven.",
     'w': [{'m': 'h(key) = key mod 7', 'fs': 46, 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Fourteen mod seven is zero, so fourteen goes in bucket zero. Twenty three mod seven is two: bucket two.",
     'w': [{'m': '14 mod 7 = 0'}, {'d': 2, 'at': 0}, {'m': '23 mod 7 = 2', 'at': 1}, {'d': 3, 'at': 1}]},
    {'say': "Nine mod seven is also two. A collision! Two keys want the same bucket. With chaining, we simply add nine to a small list hanging off bucket two.",
     'w': [{'m': '9 mod 7 = 2   collision!', 'c': 'red'}, {'d': 4, 'at': 2}]},
    {'say': "Thirty one mod seven is three, and six goes in bucket six. To look up a key later, we compute its hash and only search that one bucket. With a good hash function and enough buckets, the chains stay short, and lookups take constant time on average.",
     'w': [{'m': '31 mod 7 = 3,   6 mod 7 = 6'}, {'d': 5, 'at': 0}, {'d': 6, 'at': 0}, {'m': 'lookup: hash, then check one bucket: O(1)', 'c': 'green', 'gap': 10, 'at': 2}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: inserting into a linked list'
B.pen(LESSON, G, 0, {'p': lambda A, w, h: [('circle', 145, h * 0.62 + 40, 30, 50)], 'at': 1},
      {'p': lambda A, w, h: [('circle', 325, h * 0.62 + 40, 92, 56)], 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'new Node{25, nullptr}', 'c': 'orange', 'at': 0})
B.pen(LESSON, G, 2, {'p': ('highlight',), 'on': 'n->next = prev->next;', 'at': 0},
      {'p': lambda A, w, h: [('circle', 555, h * 0.62 + 40, 92, 56)], 'c': 'green', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('highlight',), 'on': 'prev->next = n;', 'at': 0}, {'p': ('check',), 'on': 'list: 10', 'c': 'green', 'at': 1})
B.pen(LESSON, G, 4, {'p': ('box',), 'on': 'n->next = prev->next;', 'c': 'green', 'at': 0}, {'p': ('box',), 'on': 'prev->next = n;', 'c': 'green', 'at': 0},
      {'p': ('underline',), 'on': 'Connect the new node first', 'at': 1})
G = 'Worked example: are the brackets balanced?'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'open: push', 'c': 'blue', 'at': 2}, {'p': ('underline',), 'on': 'close: pop', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 1, {'p': ('row', 0), 'c': 'blue', 'at': 0}, {'p': ('row', 1), 'c': 'blue', 'at': 1, 'solo': True}, {'p': ('row', 2), 'c': 'blue', 'at': 2, 'solo': True},
      {'p': lambda A, w, h: [('circle', 'r2c2', 70, 30)], 'at': 3})
B.pen(LESSON, G, 2, {'p': ('row', 3), 'c': 'green', 'at': 0}, {'p': ('row', 4), 'c': 'green', 'at': 2, 'solo': True}, {'p': ('row', 5), 'c': 'green', 'at': 3, 'solo': True})
B.pen(LESSON, G, 3, {'p': lambda A, w, h: [('circle', 'r5c2', 85, 30)], 'c': 'green', 'at': 0}, {'p': ('box',), 'on': 'pop "(" but saw "]"', 'at': 4})
G = 'Worked example: tracing a recursive function'
B.pen(LESSON, G, 0, {'p': ('highlight',), 'on': 'if (n <= 1) return 1;', 'at': 2}, {'p': ('highlight',), 'on': 'return n * Fact(n - 1);', 'at': 3})
B.pen(LESSON, G, 2, {'p': lambda A, w, h: [('circle', 40 + 3 * 95 + 130, h - 570 + 45, 150, 62)], 'c': 'green', 'at': 0},
      {'p': ('box',), 'on': 'return n * Fact(n - 1);', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('strike',), 'on': 'if (n <= 1) return 1;', 'at': 0})
G = 'Worked example: building and searching a BST'
B.pen(LESSON, G, 2, {'p': lambda A, w, h: [('circle', w / 2, h - 90, 54, 54)], 'at': 1},
      {'p': lambda A, w, h: [('circle', w / 2 + 200, h - 250, 54, 54)], 'at': 2},
      {'p': lambda A, w, h: [('circle', w / 2 + 100, h - 410, 56, 56)], 'c': 'green', 'at': 3})
G = 'Worked example: filling a hash table'
bucket = lambda b, h: (85, h - 70 - (b + 0.5) * 85)
B.pen(LESSON, G, 1, {'p': lambda A, w, h: [('circle', *bucket(0, h), 70, 46)], 'c': 'blue', 'at': 0},
      {'p': lambda A, w, h: [('circle', *bucket(2, h), 70, 46)], 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': lambda A, w, h: [('circle', *bucket(2, h), 70, 46)], 'at': 1}, {'p': ('underline',), 'on': 'collision!', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': 'lookup: hash', 'c': 'green', 'at': 2})

# ---------------- the pen on ordinary slides ----------------
S = 'Big-O: how does the cost grow?'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'Keep only the fastest-growing term', 'at': 1})
B.spen(LESSON, S, 2, *[{'fig': [('circle', x, y, rx, .03)], 'c': c, 'at': a} for x, y, rx, c, a in
       ((.53, .68, .09, 'green', 1), (.5, .735, .06, 'blue', 2), (.57, .79, .1, 'purple', 3), (.77, .68, .07, 'orange', 4), (.77, .735, .07, 'red', 5))])
B.spen(LESSON, S, 3, {'fig': [('underline', .03, .97, .085)], 'at': 1, 'dt': 3.0}, {'p': 'circle', 'on': '17 minutes', 'at': 1, 'dt': 8.0})
S = 'Arrays vs. linked lists'
B.spen(LESSON, S, 0, {'fig': [('circle', .43, .28, .06, .11)], 'c': 'blue', 'at': 2}, {'fig': [('box', .05, .15, .61, .38)], 'c': 'green', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('arrow', .08, .45, .58, .45)], 'at': 0, 'dt': 1.5})
B.spen(LESSON, S, 2, {'fig': [('circle', .185, .8, .035, .07)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .425, .8, .035, .07)], 'c': 'orange', 'at': 1, 'dt': 1.0})
B.spen(LESSON, S, 3, {'fig': [('arrow', .06, .62, .85, .62)], 'at': 0, 'dt': 1.5})
S = 'Stacks: last in, first out'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'push onto the top, pop from the top', 'at': 1})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'Undo history', 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'balanced brackets', 'at': 3})
S = 'Queues: first in, first out'
B.spen(LESSON, S, 0, {'fig': [('underline', .6, .91, .46)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .28, .5, .22, .4)], 'c': 'blue', 'at': 0, 'dt': 2.0}, {'p': 'underline', 'on': 'fixed array that wraps around', 'at': 0, 'dt': 4.0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'UART', 'c': 'green', 'at': 1})
S = 'Recursion: functions that call themselves'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'factorial(0) = 1', 'c': 'blue', 'at': 0, 'dt': 3.5})
B.spen(LESSON, S, 2, {'fig': [('circle', .14, .55, .08, .08)], 'at': 3}, {'fig': [('circle', .74, .32, .08, .08)], 'at': 3, 'dt': 1.2})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Memoization (cache answers)', 'c': 'green', 'at': 0}, {'p': 'circle', 'on': 'O(n)', 'c': 'green', 'at': 1})
S = 'Binary search: halve the problem every step'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .485, .04, .11)], 'c': 'orange', 'at': 2}, {'fig': [('cross', .76, .49, 46)], 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('circle', .24, .49, .04, .11)], 'c': 'orange', 'at': 0}, {'fig': [('box', .27, .4, .47, .59)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .37, .49, .04, .11)], 'c': 'orange', 'at': 0}, {'fig': [('box', .41, .4, .48, .59)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .43, .49, .045, .12)], 'c': 'green', 'at': 0}, {'fig': [('check', .5, .3, 22)], 'c': 'green', 'at': 1})
S = 'Sorting: from O(n²) to O(n log n)'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': 'O(n²)', 'n': 1, 'at': 2})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'split in half, sort each, merge', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'log n levels × n work each', 'c': 'green', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'std::sort', 'c': 'blue', 'at': 0})
S = 'Hash tables: look things up in O(1)'
B.spen(LESSON, S, 0, {'fig': [('circle', .1, .17, .09, .06)], 'c': 'blue', 'at': 1, 'dt': 0.8}, {'fig': [('circle', .32, .17, .1, .06)], 'c': 'purple', 'at': 1, 'dt': 2.5})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'O(1) on average', 'c': 'green', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .62, .49, .07, .06)], 'at': 1}, {'fig': [('circle', .92, .49, .08, .07)], 'at': 2})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Python dicts, std::unordered_map', 'c': 'blue', 'at': 0})
S = 'Binary search trees'
B.spen(LESSON, S, 1, {'fig': [('circle', .5, .14, .08, .11)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .28, .42, .08, .11)], 'c': 'blue', 'at': 1},
       {'fig': [('circle', .38, .74, .08, .11)], 'c': 'green', 'at': 3})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'height ≈ log₂ n', 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'B-trees', 'at': 1})
S = 'Heaps and priority queues'
B.spen(LESSON, S, 1, {'fig': [('circle', .5, .14, .08, .11)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .26, .9, .04, .07)], 'c': 'blue', 'at': 1, 'dt': 1.0}, {'fig': [('circle', .335, .9, .04, .07)], 'at': 1, 'dt': 2.8},
       {'fig': [('circle', .415, .9, .04, .07)], 'at': 1, 'dt': 3.6})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'OS schedulers', 'c': 'blue', 'at': 0})
S = 'Graphs and shortest paths'
B.spen(LESSON, S, 1, {'p': 'circle', 'on': 'BFS', 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'DFS', 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'Dijkstra', 'at': 0}, {'fig': [('circle', .08, .42, .07, .11)], 'c': 'green', 'at': 2, 'dt': 0.6},
       {'fig': [('circle', .88, .7, .07, .11)], 'c': 'green', 'at': 2, 'dt': 2.0}, {'fig': [('underline', .08, .92, .985)], 'c': 'orange', 'at': 2, 'dt': 3.5})
S = 'Choosing the right structure'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .01, y - .045, .97, y + .045)], 'at': a, 'solo': True} for y, a in
       ((.2, 1), (.33, 3), (.46, 5), (.59, 7), (.72, 9), (.85, 11), (.965, 13))])

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
