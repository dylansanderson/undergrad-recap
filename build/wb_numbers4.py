from math import *
import numpy as np
p = print
p('btree levels', log(1e9) / log(200), ceil(log(1e9) / log(200)))
p('compound', 1000 * 1.005 ** 120, 1.005 ** 12 - 1)
p('SL dep', [(50000 - 9000 * k) for k in range(6)])
p('RC delay', 0.69 * 10e3 * 10e-15, 0.69 * 10e3 * 40e-15)
p('power', 0.1 * 1e-9 * 1.0 ** 2 * 2e9, 0.1 * 1e-9 * 0.8 ** 2 * 2e9, 1 - 0.64)
p('systick', 48e6 / 1000 - 1, 48e6 / (440 * 32), 48e6 / (440 * 32) - 1)
d = [1, 0, 1, 1]; p1 = (d[0] + d[1] + d[3]) % 2; p2 = (d[0] + d[2] + d[3]) % 2; p4 = (d[1] + d[2] + d[3]) % 2
cw = [p1, p2, d[0], p4, d[1], d[2], d[3]]; p('hamming', cw)
r = list(cw); r[5] ^= 1
s1 = (r[0] + r[2] + r[4] + r[6]) % 2; s2 = (r[1] + r[2] + r[5] + r[6]) % 2; s4 = (r[3] + r[4] + r[5] + r[6]) % 2; p('recv', r, 'syndrome', s4 * 4 + s2 * 2 + s1)
p('battery', 37 * 0.85 / (1.2 * 5 + 4 * 0.4 * 6), 1.2 * 5 + 4 * 0.4 * 6)
img = np.array([[1, 2, 1, 0], [0, 1, 3, 1], [2, 1, 0, 2], [1, 0, 1, 1]]); ii = img.cumsum(0).cumsum(1); p('ii', ii.tolist(), 'rect r1-2 c1-2', img[1:3, 1:3].sum(), ii[2, 2] - ii[0, 2] - ii[2, 0] + ii[0, 0])
L1 = L2 = 10; x, y = 12, 8; c2 = (x * x + y * y - L1 ** 2 - L2 ** 2) / (2 * L1 * L2); t2 = -acos(c2)
t1 = atan2(y, x) - atan2(L2 * sin(t2), L1 + L2 * cos(t2))
p('IK', degrees(t1), degrees(t2), 'fk', L1 * cos(t1) + L2 * cos(t1 + t2), L1 * sin(t1) + L2 * sin(t1 + t2), 'elbow', L1 * cos(t1), L1 * sin(t1))
p('servo', 1 + 45 / 180, (1 + 45 / 180) * 1000)
