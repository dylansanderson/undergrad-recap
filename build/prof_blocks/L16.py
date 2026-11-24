# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'The MOSFET: a voltage-controlled switch', {'t': 'wb', 'h': 'Which region? The MOSFET checklist', 'steps': [
    {'say': "On every electronics exam, the first question about a MOSFET is: which region is it in? Here's the checklist, in order. First compare the gate source voltage with the threshold. If V G S is below V t, there's no channel: cutoff, and no current.",
     'w': [{'m': r'1.  $V_{GS} < V_t$  $\to$  cutoff:  $I_D = 0$', 'at': 3}]},
    {'say': "If it's above threshold, compute the overdrive, V G S minus V t. Then compare V D S with it. If V D S is smaller, the channel is fully formed along its length, and it acts like a resistor: triode. If V D S is at least the overdrive, the channel pinches off at the drain end: saturation.",
     'w': [{'m': r'2.  overdrive  $V_{ov} = V_{GS} - V_t$', 'at': 1},
           {'m': r'$V_{DS} < V_{ov}$  $\to$  triode (a resistor)', 'c': 'blue', 'at': 3},
           {'m': r'$V_{DS} \geq V_{ov}$  $\to$  saturation:  $I_D = \frac{1}{2}k\,V_{ov}^2$', 'c': 'green', 'at': 4}]},
    {'say': "Numbers. Threshold one volt, k equals two milliamps per volt squared. With V G S equals three volts, the overdrive is two volts. If V D S is five volts, that's more than two, so it's saturated, and the current is one half times two times two squared: four milliamps. Drop V D S to one volt, and it's in triode instead.",
     'w': [{'m': r'$V_t = 1$, $k = 2\ \mathrm{mA/V^2}$, $V_{GS} = 3$:  $V_{ov} = 2\ \mathrm{V}$', 'at': 0, 'gap': 14},
           {'m': r'$V_{DS} = 5 \geq 2$:  saturation,  $I_D = \frac{1}{2}(2)(2^2) = 4\ \mathrm{mA}$', 'at': 2},
           {'m': r'$V_{DS} = 1 < 2$:  triode', 'at': 3}]},
    {'say': "And beware a famous naming trap. For a MOSFET, saturation is the amplifier region, where the current saturates at a steady value. For a B J T, saturation means the opposite: the transistor is jammed fully on, like a closed switch. Same word, different meaning. Always ask which device.",
     'w': [{'m': 'MOSFET "saturation" = amplifier', 'c': 'red', 'at': 1, 'gap': 14}, {'m': 'BJT "saturation" = fully-on switch', 'c': 'red', 'at': 2}]},
]})

G = 'Which region? The MOSFET checklist'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'overdrive  $V_{ov}', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'= 4\ \mathrm{mA}$', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': 'MOSFET "saturation"', 'c': 'red', 'at': 1}, {'p': ('box',), 'on': 'BJT "saturation"', 'c': 'red', 'at': 2})
