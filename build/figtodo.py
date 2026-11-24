"""List slides in the AUTO lessons that have a figure/code/table but no hand-placed pen marks (auto only marks bullets).
python figtodo.py [L01 ...]"""
import os, sys, glob, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fixes
want = sys.argv[1:]; tot = 0
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    n = os.path.splitext(os.path.basename(f))[0]
    if n not in fixes.AUTO or (want and not any(n.startswith(w) for w in want)): continue
    sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    rows = []
    for i, s in enumerate(m.LESSON['slides']):
        if s['t'] in ('wb', 'title', 'section', 'q', 'clip') or s.get('pen'): continue
        kind = 'code' if s.get('code') else 'img' if s.get('img') else 'tbl' if s.get('table') or s.get('rows') else ''
        if not kind: continue
        nb = len(s['say']) if isinstance(s.get('say'), list) else 1
        img = s.get('img'); img = img if isinstance(img, str) else (img[0] + f'..({len(img)})' if img else '')
        rows.append(f"   s{i:02d} {s['t']:5s} {kind:4s} b={nb} {s.get('h','')[:55]:55s} {img}")
    tot += len(rows); print(f"{n}: {len(rows)}"); print('\n'.join(rows))
print('TOTAL', tot)
