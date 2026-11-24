# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Worked example: 200 in binary and hex, by hand', {'t': 'wb', 'h': "Negative numbers: two's complement", 'fs': 48, 'cfs': 44, 'steps': [
    {'say': "Hardware has no minus sign, so how does a computer store negative five? Almost every computer uses two's complement. The trick: in eight bits, the top bit's place value isn't plus one twenty eight. It's minus one twenty eight. Everything else stays positive.",
     'w': [{'k': 'weights:  -128  64  32  16   8   4   2   1', 'lang': 'plain', 'at': 3}]},
    {'say': "To negate a number, invert every bit, then add one. Five is zero zero zero zero zero one zero one. Invert: one one one one one zero one zero. Add one: one one one one one zero one one. That's negative five.",
     'w': [{'k': ' 5      =  0000 0101', 'lang': 'plain', 'at': 1}, {'k': 'invert  =  1111 1010', 'lang': 'plain', 'at': 2},
           {'k': '+1      =  1111 1011   = -5', 'lang': 'plain', 'at': 3}]},
    {'say': "Check it with the weights: minus one twenty eight, plus sixty four, thirty two, sixteen, eight, two and one. That's minus five. And here's the beautiful part. Add five and negative five with an ordinary binary adder. Every column carries, and the final carry falls off the end of the eight bits, leaving zero.",
     'w': [{'m': r'$-128 + 64 + 32 + 16 + 8 + 2 + 1 = -5$', 'c': 'green', 'at': 1},
           {'k': '   0000 0101   (5)', 'lang': 'plain', 'at': 3, 'gap': 14}, {'k': ' + 1111 1011  (-5)', 'lang': 'plain', 'at': 3},
           {'k': ' 1 0000 0000   -> drop carry -> 0', 'lang': 'plain', 'at': 4}]},
    {'say': "So the same adder circuit does subtraction: a minus b is just a plus negative b. That's why everyone uses this format. Eight bits hold minus one twenty eight up to plus one twenty seven. Add one to one twenty seven, and you get one zero zero zero zero zero zero zero, which is minus one twenty eight. That's the integer overflow from the programming course: the wheel wraps around.",
     'w': [{'m': 'subtract = add the negative', 'c': 'blue', 'at': 0, 'gap': 10}, {'m': 'range (8 bits):  −128 … +127', 'at': 2},
           {'k': '0111 1111 + 1 = 1000 0000   127 + 1 = -128 !', 'lang': 'plain', 'at': 3}]},
]})

G = "Negative numbers: two's complement"
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'weights:', 'cols': (10, 14), 'at': 3})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'invert  =', 'c': 'blue', 'at': 2}, {'p': ('box',), 'on': '+1      =', 'c': 'red', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': ' 1 0000 0000', 'cols': (1, 2), 'at': 4})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '0111 1111 + 1', 'cols': (28, 43), 'c': 'red', 'at': 3})
