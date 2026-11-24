# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Race conditions and critical sections', {'t': 'wb', 'h': 'Worked example: losing an update, then fixing it', 'lang': 'c', 'cfs': 32, 'steps': [
    {'say': "Let's trace the lost update one machine step at a time, because seeing it written out is what makes it click. Count starts at five. Each thread's count plus plus is really three steps: load, add, store.",
     'w': [{'k': 'count++;   =>   reg = count;  reg = reg + 1;  count = reg;', 'at': 2}]},
    {'say': "Thread one loads five into its register. Then the scheduler switches. Thread two loads count, still five. Thread two adds one and stores six. Back to thread one: it adds one to its own copy, five, and stores six too.",
     'w': [{'k': 'T1: reg1 = count      // 5', 'lang': 'plain', 'at': 1, 'gap': 12}, {'k': 'T2: reg2 = count      // 5   (switched in!)', 'lang': 'plain', 'at': 2},
           {'k': 'T2: count = reg2 + 1  // 6', 'lang': 'plain', 'at': 3}, {'k': 'T1: count = reg1 + 1  // 6   <- T2\'s update is lost', 'lang': 'plain', 'at': 4}]},
    {'say': "Two increments, and count went up by one. The fix: wrap the read, modify, write in a mutex. Lock, increment, unlock.",
     'w': [{'k': 'pthread_mutex_lock(&m);', 'at': 2, 'gap': 14}, {'k': 'count++;                 // critical section', 'at': 2}, {'k': 'pthread_mutex_unlock(&m);', 'at': 2}]},
    {'say': "Now if thread two tries to lock while thread one holds the mutex, thread two simply waits. Thread one finishes all three steps, unlocks, and only then does thread two load count, which is now six. The answer is seven, every time. Keep critical sections as short as possible, because every thread waiting on a lock is a thread not running in parallel.",
     'w': [{'m': 'T2 waits at lock → loads 6 → stores 7', 'c': 'green', 'at': 2}, {'m': 'keep critical sections SHORT', 'c': 'red', 'box': True, 'at': 4}]},
]})

G = 'Worked example: losing an update, then fixing it'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'T2: reg2 = count', 'cols': (22, 23), 'c': 'red', 'at': 2}, {'p': ('cross',), 'on': "T1: count = reg1 + 1", 'at': 4})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': 'pthread_mutex_lock', 'c': 'green', 'at': 2}, {'p': ('box',), 'on': 'pthread_mutex_unlock', 'c': 'green', 'at': 2, 'dt': 0.8})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': 'T2 waits at lock', 'at': 2})
