import numpy as np
from math import *
p = print
p('--- L08')
a, b = np.array([3, 4, 0]), np.array([4, 0, 3]); p('angle', a @ b, degrees(acos(12 / 25)))
a, b = np.array([1, 0, 2]), np.array([0, 3, 1]); c = np.cross(a, b); p('cross', c, c @ a, c @ b, np.linalg.norm(c))
p('D test', 'f(1,0)=', 1 - 3, ' f(-1,0)=', -1 + 3)
p('polar', 8 * pi)
x, y = 2.0, 1.0
for k in range(3):
    f = x * x + 3 * y * y; g = (2 * x, 6 * y); p('gd', k, (round(x, 4), round(y, 4)), round(f, 4), g); x, y = x - 0.1 * g[0], y - 0.1 * g[1]
p('--- L09')
p('elim', np.linalg.solve(np.array([[1, 1, 1], [0, 2, 5], [2, 5, -1]]), [6, -4, 27]))
A = np.array([[4, 7], [2, 6]]); p('inv solve', np.linalg.solve(A, [1, 2]))
p('lsq', np.polyfit([0, 1, 2], [1, 3, 4], 1), 7 / 6)
A = np.array([[4, 1], [2, 3]]); p('eig', np.linalg.eigvals(A), A @ [1, 1], A @ [1, -2])
yf = lambda t: 3 * exp(-2 * t) - 2 * exp(-3 * t); p('ode', yf(0), (-6 + 6), yf(0.5), yf(1), yf(2))
p('--- L10')
k = 8.99e9; p('E mid', 2 * k * 2e-9 / 0.09)
C = 8.854e-12 * 0.01 / 1e-4; p('cap', C, C * 5, 0.5 * C * 25)
R = 1.68e-8 * 10 / (pi * 0.0005 ** 2); p('wire', R, 100 * R, 10 * R)
p('B', 4e-7 * pi * 10 / (2 * pi * 0.05))
p('emf', 100 * 0.01 * 0.5 / 0.1, 'I if 10 ohm', 0.5)
p('--- L11')
p('shm', sqrt(200 / 0.5), 20 / (2 * pi), 2 * pi / 20, 0.05 * 20)
p('string', 2 * 0.65 * 110, 2 * 0.65)
p('doppler', 700 * 343 / (343 - 30), 700 * 343 / (343 + 30))
p('snell water', degrees(asin(1.33 * sin(radians(40)))), degrees(asin(1 / 1.33)))
E = 6.626e-34 * 3e8 / 650e-9; p('photon', E, E / 1.602e-19, 5e-3 / E)
