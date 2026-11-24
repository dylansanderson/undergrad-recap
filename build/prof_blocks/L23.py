# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Transactions and ACID', {'t': 'wb', 'h': 'Worked example: a transfer, a crash, and the log', 'lang': 'sql', 'cfs': 34, 'steps': [
    {'say': "Here's the bank transfer as real SQL. Begin a transaction, subtract a hundred from checking, add a hundred to savings, commit. Until the commit, none of it is permanent.",
     'w': [{'k': 'BEGIN;', 'at': 1}, {'k': 'UPDATE acct SET bal = bal - 100 WHERE id = 1;', 'at': 1},
           {'k': 'UPDATE acct SET bal = bal + 100 WHERE id = 2;', 'at': 1}, {'k': 'COMMIT;', 'at': 2}]},
    {'say': "Before touching any data page, the database writes each change to the log on disk: transaction seven, account one, old value five hundred, new value four hundred. Then account two, old two hundred, new three hundred. Then a commit record.",
     'w': [{'k': 'LOG: T7 acct1  old 500  new 400', 'lang': 'plain', 'at': 1, 'gap': 14}, {'k': 'LOG: T7 acct2  old 200  new 300', 'lang': 'plain', 'at': 2},
           {'k': 'LOG: T7 COMMIT', 'lang': 'plain', 'at': 3}]},
    {'say': "Now suppose the power fails after the first update, before the commit. On restart, the database reads the log. Transaction seven has no commit record, so it's undone using the old values: account one goes back to five hundred. Atomicity: no money vanished.",
     'w': [{'m': 'crash before COMMIT  →  UNDO with old values', 'c': 'red', 'at': 2}]},
    {'say': "If the crash comes after the commit record is on disk, but before the data pages were written, the database redoes the change from the new values. Durability: a committed transfer is never lost. That's the whole trick: log first, data later.",
     'w': [{'m': 'crash after COMMIT  →  REDO with new values', 'c': 'green', 'at': 0}, {'m': 'write-ahead: log first, data later', 'box': True, 'at': 2}]},
]})

G = 'Worked example: a transfer, a crash, and the log'
B.pen(LESSON, G, 0, {'p': ('box',), 'on': 'COMMIT;', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'LOG: T7 acct1', 'cols': (24, 27), 'c': 'red', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'LOG: T7 COMMIT', 'cols': (9, 15), 'c': 'green', 'at': 0})
