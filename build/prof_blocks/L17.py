# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Lab: AC-to-DC power supplies', {'t': 'wb', 'h': "Worked example: sizing a Zener regulator's resistor", 'steps': [
    {'say': "Let's work the Zener design problem, because it's always about the worst case. The unregulated input swings between nine and twelve volts. We want five point one volts out, for a load that draws up to twenty milliamps, and the Zener needs at least five milliamps to stay in regulation.",
     'w': [{'m': r'$V_{in} = 9 \ldots 12\ \mathrm{V}$,   $V_Z = 5.1\ \mathrm{V}$', 'at': 1},
           {'m': r'$I_{L,max} = 20\ \mathrm{mA}$,   $I_{Z,min} = 5\ \mathrm{mA}$', 'at': 3}]},
    {'say': "Worst case one, the hardest for regulation: lowest input and heaviest load. The resistor must still pass the load current plus the Zener's minimum: twenty five milliamps, from only nine minus five point one, three point nine volts. So R s can be at most three point nine over twenty five milliamps, about one hundred fifty six ohms. Choose one fifty.",
     'w': [{'m': 'worst case 1: lowest $V_{in}$, heaviest load', 'c': 'blue', 'at': 1},
           {'m': r'$R_s \leq \frac{9 - 5.1}{20 + 5\ \mathrm{mA}} = 156\ \Omega$  $\to$  use $150\ \Omega$', 'at': 3}]},
    {'say': "Worst case two, the hardest on the Zener: highest input and no load at all. Now every bit of the resistor's current goes through the Zener. That's twelve minus five point one, over one fifty: forty six milliamps.",
     'w': [{'m': 'worst case 2: highest $V_{in}$, no load', 'c': 'red', 'at': 0},
           {'m': r'$I_Z = \frac{12 - 5.1}{150} = 46\ \mathrm{mA}$', 'at': 2}]},
    {'say': "The Zener dissipates five point one volts times forty six milliamps, about a quarter of a watt. So a quarter watt Zener would be on the edge. Pick a half watt part. Two worst cases, one for each failure mode: that's how every regulator, and most real designs, are sized.",
     'w': [{'m': r'$P_Z = 5.1 \times 0.046 \approx 0.24\ \mathrm{W}$  $\to$  use a 0.5 W Zener', 'c': 'green', 'box': True, 'at': 2}]},
]})

G = "Worked example: sizing a Zener regulator's resistor"
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'use $150\ \Omega$', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'= 46\ \mathrm{mA}$', 'c': 'red', 'at': 2})
