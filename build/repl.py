"""Exact-text replacements in a lesson file: python repl.py <file> <pairs.py>  (pairs.py: P = [(old, new), ...]; each old must occur exactly once)"""
import sys, io
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
f, pf = sys.argv[1], sys.argv[2]
ns = {}; exec(io.open(pf, encoding='utf-8-sig').read(), ns)
t = io.open(f, encoding='utf-8').read(); bad = 0
for old, new in ns['P']:
    if new in t: print(f'already applied: {old[:60]}'); continue      # idempotent re-runs
    k = t.count(old)
    if k != 1: print(f'SKIP ({k}x): {old}'); bad += 1; continue
    t = t.replace(old, new)
io.open(f, 'w', encoding='utf-8', newline='').write(t)
print(f'{len(ns["P"]) - bad} applied, {bad} skipped')
