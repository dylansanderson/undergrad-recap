"""print the reveal schedules fixes.py sets, next to the default schedule"""
import glob, importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import fixes
for name, pres in fixes.REVEAL.items():
    f = glob.glob(os.path.join(HERE, 'lessons', name + '.py'))[0]
    sp = importlib.util.spec_from_file_location(name, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    fixes.apply(name, m.LESSON)
    for pre in pres:
        s = next(x for x in m.LESSON['slides'] if x.get('h', '').startswith(pre)); nb = len(s['say']); off = nb - len(s['pts'])
        print(f"{name:14s} {pre[:34]:34s} default {[max(0, b - off + 1) for b in range(nb)]} -> {s['rv']}")
