# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_phasorrc(ax, n, w, h):
    O = (w * 0.25, h * 0.55); s = 34
    P = lambda re, im: (O[0] + re * s, O[1] + im * s)
    if n >= 1:
        B.arr(ax, O[0] - 40, O[1], O[0] + 12 * s, O[1], 'gray', 2, 14); B.arr(ax, O[0], O[1] - 9 * s, O[0], O[1] + 6 * s, 'gray', 2, 14)
        B.lab(ax, O[0] + 12 * s, O[1] - 26, 'Re', 24, 'gray'); B.lab(ax, O[0] + 26, O[1] + 6 * s, 'Im', 24, 'gray', ha='left')
        B.arr(ax, *O, *P(10, 0), 'blue', 4, 22); B.lab(ax, *P(10.3, 0.8), r'$V_s = 10\angle 0°$', 26, 'blue', ha='left')
    if n >= 2:
        B.arr(ax, *O, *P(5, 5), 'green', 4, 22); B.lab(ax, *P(5.2, 5.6), r'$I$ leads by 45°', 26, 'green', ha='left')
    if n >= 3:
        B.arr(ax, *O, *P(5, -5), 'red', 4, 22); B.lab(ax, *P(5.2, -5.9), r'$V_C = 7.07\angle -45°$', 26, 'red', ha='left')

B.insert(LESSON, 'AC circuits with phasors', {'t': 'wb', 'h': 'Worked example: an RC circuit with phasors', 'draw': 'phasorrc', 'split': 0.58, 'steps': [
    {'say': "Let's actually do a phasor problem, because the complex arithmetic is where students get stuck. A ten volt, one kilohertz sine wave drives a one kilohm resistor in series with a capacitor. At this frequency, the capacitor's impedance works out to minus j one kilohm.",
     'w': [{'m': r'$v_s = 10\cos(2\pi\,1000\,t)$  $\to$  $V_s = 10\angle 0°$', 'at': 1}, {'d': 1, 'at': 1},
           {'m': r'$Z_C = \frac{1}{j\omega C} = -j\,1\ \mathrm{k\Omega}$', 'at': 2}]},
    {'say': "Series impedances add, like resistors, and adding is easiest in rectangular form: one k minus j one k. To divide, switch to polar form: the magnitude is the square root of one plus one, so one point four one four k, at an angle of minus forty five degrees.",
     'w': [{'m': r'$Z = 1k - j1k = 1.414k\,\angle -45°$', 'c': 'blue', 'at': 2},
           {'m': 'add in rectangular,  multiply/divide in polar', 'c': 'gray', 'at': 2}]},
    {'say': "Now Ohm's law with complex numbers. To divide in polar form, divide the magnitudes and subtract the angles. Ten over one point four one four k is seven point oh seven milliamps, at zero minus minus forty five: plus forty five degrees. The current leads the voltage, as it always does in a capacitive circuit.",
     'w': [{'m': r'$I = \frac{10\angle 0°}{1.414k\angle -45°} = 7.07\ \mathrm{mA}\,\angle 45°$', 'c': 'green', 'at': 2}, {'d': 2, 'at': 3}]},
    {'say': "The capacitor's voltage is I times Z C. Multiply in polar: multiply magnitudes and add angles. Seven point oh seven milliamps times one k is seven point oh seven volts, at forty five minus ninety, minus forty five degrees. Finally, convert back to time: seven point oh seven cosine of two pi one thousand t, minus forty five degrees. No differential equation needed.",
     'w': [{'m': r'$V_C = (7.07m\angle 45°)(1k\angle -90°) = 7.07\angle -45°$', 'at': 2}, {'d': 3, 'at': 2},
           {'m': r'$v_C(t) = 7.07\cos(2\pi\,1000\,t - 45°)$', 'c': 'red', 'box': True, 'at': 4}]},
]})

G = 'Worked example: an RC circuit with phasors'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'add in rectangular', 'c': 'gray', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'7.07\ \mathrm{mA}\,\angle 45°', 'c': 'green', 'at': 2})
