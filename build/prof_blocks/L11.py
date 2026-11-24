# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Worked example: the Doppler shift of a siren', {'t': 'wb', 'h': 'Decibels by hand: the 10 vs 20 rule', 'steps': [
    {'say': "Decibels will follow you into every electronics course, so let's get them exactly right. A decibel compares two powers: ten times the log of the power ratio. A power ratio of one hundred is ten log one hundred, twenty decibels. A ratio of two is about three decibels.",
     'w': [{'m': r'power:  $dB = 10\log_{10}\frac{P_2}{P_1}$', 'c': 'blue', 'at': 1},
           {'m': r'$\times 100 \to 20\ dB$     $\times 2 \to 3\ dB$     $\times\frac{1}{2} \to -3\ dB$', 'at': 3}]},
    {'say': "Here's the trap. Engineers often measure voltages, not powers. But power goes as voltage squared. The square comes out of the log as a factor of two, so for voltages, it's twenty log of the ratio.",
     'w': [{'m': r'$P \propto V^2$:   $10\log\frac{V_2^2}{V_1^2} = 20\log_{10}\frac{V_2}{V_1}$', 'c': 'green', 'at': 2}]},
    {'say': "So an amplifier that multiplies voltage by ten has a gain of twenty decibels, not ten. And it multiplies power by one hundred, which is also twenty decibels. Same answer, as it must be. Use ten for power ratios, twenty for voltage or current ratios.",
     'w': [{'m': r'voltage $\times 10$:  $20\log 10 = 20\ dB$  = power $\times 100$', 'at': 1, 'box': True}]},
    {'say': "The most important number: minus three decibels. It's half the power, and one over root two, point seven oh seven, of the voltage. When you meet a filter's cutoff frequency in circuits and signals, it's defined exactly there: the frequency where the output drops three decibels.",
     'w': [{'m': r'$-3\ dB$:  power $\times\frac{1}{2}$,  voltage $\times 0.707$', 'c': 'red', 'box': True, 'at': 1, 'gap': 16},
           {'m': 'a filter cutoff = the −3 dB point', 'c': 'purple', 'at': 2}]},
]})

G = 'Decibels by hand: the 10 vs 20 rule'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'= 20\log_{10}', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'a filter cutoff', 'c': 'purple', 'at': 2})
