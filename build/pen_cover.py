"""Pen coverage after fixes: static (non-whiteboard, non-title/section) beats with at least one mark, total marks, figure marks."""
import os, sys, glob, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'lessons'))
import fixes
st = cov = marks = figm = 0
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    n = os.path.splitext(os.path.basename(f))[0]
    sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    fixes.apply(n, m.LESSON)
    for s in m.LESSON['slides']:
        if s['t'] in ('wb', 'title', 'section', 'clip'): continue
        nb = len(s['say']) if isinstance(s.get('say'), list) else 1
        bs = {p['b'] for p in s.get('pen', [])}
        st += nb; cov += len(bs); marks += len(s.get('pen', [])); figm += sum(1 for p in s.get('pen', []) if 'fig' in p)
print(f'static beats {st}  with marks {cov} ({100*cov/st:.0f}%)  marks {marks}  figure marks {figm}')
