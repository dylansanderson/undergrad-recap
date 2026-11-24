# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Side-channel attacks: power and timing', {'t': 'wb', 'h': 'Worked example: correlation power analysis on a toy chip', 'cfs': 36, 'steps': [
    {'say': "Correlation power analysis sounds like magic, so let's do it by hand on a toy four bit chip. The chip computes p X O R k, a plaintext with a secret key. Driving more ones onto the wires costs more power, so the power is roughly the Hamming weight, the number of ones, of that result.",
     'w': [{'m': r'chip computes  $v = p \oplus k$', 'at': 1}, {'m': 'power ≈ Hamming weight of v  (number of 1s)', 'c': 'blue', 'at': 2}]},
    {'say': "We send four known plaintexts and measure the power each time. The numbers are noisy: one point one, two point nine, one point oh, one point two.",
     'w': [{'k': 'p:          0000  1111  0011  0101', 'lang': 'plain', 'at': 0, 'gap': 14}, {'k': 'measured:    1.1   2.9   1.0   1.2', 'lang': 'plain', 'at': 1}]},
    {'say': "Now guess the key. If k were zero zero zero zero, v would equal p, with weights zero, four, two, two. That doesn't track the measurements at all. Try k equals zero zero zero one: v becomes zero zero zero one, one one one zero, zero zero one zero, zero one zero zero, with weights one, three, one, one. That rises and falls exactly with the measured power.",
     'w': [{'k': 'guess 0000:  0     4     2     2', 'lang': 'plain', 'at': 1}, {'k': 'guess 0001:  1     3     1     1', 'lang': 'plain', 'at': 3}]},
    {'say': "The guess with the highest correlation is the key: zero zero zero one. We never broke the math. A real attack does this for each byte of an A E S key, with two hundred fifty six guesses per byte and thousands of traces to beat the noise. That's why masking, which randomizes v so its weight no longer depends on the key, is the standard defense.",
     'w': [{'m': 'best correlation  →  k = 0001', 'c': 'green', 'box': True, 'at': 0}, {'m': 'AES: 16 bytes × 256 guesses each, not 2^128', 'c': 'red', 'at': 2}]},
]})

G = 'Worked example: correlation power analysis on a toy chip'
B.pen(LESSON, G, 2, {'p': ('cross',), 'on': 'guess 0000:', 'at': 1}, {'p': ('check',), 'on': 'guess 0001:', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'AES: 16 bytes', 'c': 'red', 'at': 2})
