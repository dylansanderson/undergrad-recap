import numpy as np
print('sine', [int(round(7.5 + 7.5 * np.sin(2 * np.pi * k / 32))) for k in range(32)])
avg = 6 + 9.6 * 0.25 + 1; print('avg W', avg, 'batt W', avg / 0.85, 'hours', 60 * 0.8 / (avg / 0.85))
pk = 6 + 9.6 + 1; print('peak', pk, pk / 0.85, pk / 0.85 / 12)
W = [0.4, 0.3, 0.2, 0.1]; A = [4, 3, 5, 2]; Bc = [3, 5, 3, 4]
print('matrix', sum(w * a for w, a in zip(W, A)), sum(w * b for w, b in zip(W, Bc)))
