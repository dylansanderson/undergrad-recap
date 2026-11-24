"""Print a lesson as a viewer experiences it: per slide what's on screen, then each narration beat split into numbered sentences
(the numbers are the 'at' values pen marks use). Whiteboard slides list each step's written lines.
python watch.py L03 [--from N] [--to N]"""
import os, sys, glob, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tts import sentences          # the same split the narration timing ('at') uses
a = sys.argv[1:]; pre = a[0]
lo = int(a[a.index('--from') + 1]) if '--from' in a else 0; hi = int(a[a.index('--to') + 1]) if '--to' in a else 999
f = next(x for x in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))) if os.path.basename(x).startswith(pre))
n = os.path.splitext(os.path.basename(f))[0]
sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
L = m.LESSON; print(f"#### {n}: {L['code']} {L.get('title','')}")
for i, s in enumerate(L['slides']):
    if not lo <= i <= hi: continue
    t = s['t']
    if '--static' in a and t in ('wb', 'title', 'q', 'section'): continue
    print(f"\n[s{i}] {t.upper()}  {s.get('h','')}")
    if t == 'wb':
        for k, st in enumerate(s['steps']):
            ws = [(w if isinstance(w, str) else (w.get('m') or w.get('k') or w.get('o') or ('PEN ' + str(w.get('p'))[:40] + (' on ' + w['on'] if 'on' in w else '')) or ('DRAW' if 'd' in w else str(list(w))[:30]))) for w in st.get('w', [])]
            if st.get('d') or s.get('draw'): ws = ws + ['(drawing)'] if st.get('d') else ws
            print(f"  step{k} board+: " + ' || '.join(str(x)[:60] for x in ws))
            for j, x in enumerate(sentences(st['say'])): print(f"     {j}: {x}")
        continue
    if s.get('img'): print('  img:', s['img'] if isinstance(s['img'], str) else ' / '.join(s['img']))
    for p in s.get('pts', []): print('  •', p)
    if s.get('big'): print('  BIG:', s['big'])
    if s.get('code'): print('  CODE:\n    ' + s['code'].replace('\n', '\n    '))
    if s.get('cap'): print('  cap:', s['cap'])
    if s.get('pen'): print('  (pen marks:', len(s['pen']), ')')
    says = s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')]
    for k, sy in enumerate(says):
        print(f"  beat{k}:")
        for j, x in enumerate(sentences(sy)): print(f"     {j}: {x}")
