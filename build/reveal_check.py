"""Bullets that the narrator talks about BEFORE they appear (reveal timing mismatch).
For each revealing bullet slide: a bullet is flagged if its distinctive words match an earlier beat's narration much
better than the beat where the bullet first shows.   python reveal_check.py"""
import os, sys, glob, re, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
STOP = set('this that with from they them then than when what which where your have will into their there these those about would could should'.split())
W = lambda t: set(w for w in re.findall(r"[a-z]+", t.lower()) if len(w) > 3 and w not in STOP)
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    n = os.path.splitext(os.path.basename(f))[0]
    sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    for si, s in enumerate(m.LESSON['slides']):
        pts = s.get('pts'); says = s.get('say')
        if s['t'] == 'wb' or not pts or not isinstance(says, list) or len(says) < 2 or not s.get('reveal', True): continue
        nb = len(says); off = nb - len(pts)
        for i, p in enumerate(pts):
            first = max(0, i + off)                      # beat where bullet i first shows: nshow = beat - off + 1 > i
            pw = W(p)
            if len(pw) < 2: continue
            sc = [len(pw & W(x)) / len(pw) for x in says]
            best = max(range(nb), key=lambda b: sc[b])
            if best < first and sc[best] >= 0.5 and sc[best] > sc[first] + 0.2:
                print(f"{n} s{si} '{s['h'][:40]}': bullet {i} '{p[:50]}' shows at beat {first} but is narrated in beat {best} ({sc[best]:.2f} vs {sc[first]:.2f})")
