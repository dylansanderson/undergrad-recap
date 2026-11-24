from math import comb, exp, sqrt, pi, log10, erfc
import numpy as np
p = print
p('bayes', 0.05 * 0.9, 0.05 * 0.9 + 0.95 * 0.1, 0.045 / 0.14)
p('binom', [round(comb(10, k) * 0.1 ** k * 0.9 ** (10 - k), 4) for k in range(5)], 0.9 ** 10 + 10 * 0.1 * 0.9 ** 9)
Q = lambda z: 0.5 * erfc(z / sqrt(2)); p('gauss tail z=2', Q(2), 'within 1 sigma', 1 - 2 * Q(1))
p('rel', exp(-8760 / 50000))
p('conv', np.convolve([1, 2, 1], [1, 1]))
fc = 1 / (2 * pi * 1e3 * 100e-9); H = lambda f: 1 / sqrt(1 + (f / fc) ** 2)
p('rc', fc, H(1e3), 20 * log10(H(1e3)), H(1e4), 20 * log10(H(1e4)))
p('alias', abs(7 - 10))
y = []; prev = 0
for n in range(5): x = 1 if n == 0 else 0; prev = x + 0.5 * prev; y.append(prev)
p('iir', y)
w = (0 << 26) | (17 << 21) | (18 << 16) | (8 << 11) | (0 << 6) | 32; p('mips', hex(w))
a = 0x1234ABCD; p('cache', a & 0x3F, (a >> 6) & 0xFF, hex((a >> 6) & 0xFF), a >> 14, hex(a >> 14))
p('amat', 1 + 0.05 * 100, 1 + 0.05 * (10 + 0.2 * 100))
p('rr waits', (6 + 4 + 7) / 3)
def sim(refs, nf, lru):
    fr, faults, hist = [], 0, []
    for t, r in enumerate(refs):
        if r in fr:
            if lru: fr.remove(r); fr.append(r)
            hist.append((r, 'hit', list(fr))); continue
        faults += 1
        if len(fr) == nf: fr.pop(0)
        fr.append(r); hist.append((r, 'fault', list(fr)))
    return faults, hist
refs = [7, 0, 1, 2, 0, 3, 0, 4]
p('LRU', sim(refs, 3, True)); p('FIFO', sim(refs, 3, False))
