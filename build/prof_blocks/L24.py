# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Comparing alternatives: present worth and rate of return', {'t': 'wb', 'h': 'Worked example: present worth, factor by factor', 'steps': [
    {'say': "Students often see the plus nine thousand nine hundred sixty six and wonder where it came from. Let's compute it by hand. Cost fifty thousand now, savings of fifteen thousand a year for five years, salvage five thousand at year five, at a MARR of ten percent.",
     'w': [{'m': r'$-50{,}000$ now,  $+15{,}000$/yr for 5 yr,  $+5{,}000$ at yr 5,  $i = 10\%$', 'at': 1}]},
    {'say': "The uniform series uses the P over A factor: one plus i to the n, minus one, over i times one plus i to the n. One point one to the fifth is one point six one zero five. So the factor is point six one zero five over point one six one zero five: three point seven nine one. Fifteen thousand times that is fifty six thousand eight hundred sixty two.",
     'w': [{'m': r'$(P/A) = \frac{(1+i)^n - 1}{i(1+i)^n} = \frac{0.6105}{0.16105} = 3.791$', 'c': 'blue', 'at': 1},
           {'m': r'$15{,}000 \times 3.791 = 56{,}862$', 'at': 3}]},
    {'say': "The salvage is a single future amount, so use P over F: one over one point six one zero five, which is point six two zero nine. Five thousand times that is three thousand one hundred five.",
     'w': [{'m': r'$(P/F) = \frac{1}{(1+i)^n} = 0.6209$:   $5{,}000 \times 0.6209 = 3{,}105$', 'c': 'green', 'at': 1}]},
    {'say': "Add everything at time zero: minus fifty thousand, plus fifty six thousand eight hundred sixty two, plus three thousand one hundred five. Plus nine thousand nine hundred sixty seven, the same as the slide, give or take rounding. Positive, so buy the machine. And the sign convention matters: costs are negative, receipts positive, everything moved to the same moment before adding.",
     'w': [{'m': r'$PW = -50{,}000 + 56{,}862 + 3{,}105 \approx +\$9{,}967$', 'c': 'red', 'box': True, 'at': 1},
           {'m': 'only add money that sits at the SAME time', 'c': 'purple', 'at': 4}]},
]})

G = 'Worked example: present worth, factor by factor'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '= 3.791$', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': r'\approx +\$9{,}967$', 'at': 2})
