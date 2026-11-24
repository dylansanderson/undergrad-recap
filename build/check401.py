import json, os
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'credits.json')
c = json.load(open(A, encoding='utf-8')); c['solar_farm']['artist'] = 'Kkiefuik'
json.dump(c, open(A, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('F compound', 10000 * 1.06 ** 10, 'F 40y', 10000 * 1.06 ** 40)
i = 0.005; n = 60; P = 25000; Am = P * i * (1 + i) ** n / ((1 + i) ** n - 1); print('car payment', Am, 'total', Am * n)
print('eff 12% monthly', (1 + 0.01) ** 12 - 1)
pa = lambda r, n: ((1 + r) ** n - 1) / (r * (1 + r) ** n)
pw = lambda r: -50000 + 15000 * pa(r, 5) + 5000 / (1 + r) ** 5
print('PW10', pw(0.10))
lo, hi = 0.01, 0.5
for _ in range(100):
    m = (lo + hi) / 2
    if pw(m) > 0: lo = m
    else: hi = m
print('IRR', m)
# annual worth comparison: pump A 12000 cost, 6 yr, 1500/yr op; pump B 20000, 12 yr, 900/yr; MARR 8%
ap = lambda r, n: r * (1 + r) ** n / ((1 + r) ** n - 1)
print('EUAC A', 12000 * ap(0.08, 6) + 1500, 'EUAC B', 20000 * ap(0.08, 12) + 900)
print('retire', 500 * 12 * ((1.07 ** 40 - 1) / 0.07))
