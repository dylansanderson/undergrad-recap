"""compact outline of lessons: slide type, heading, #beats, and (for ex slides) whether there's code"""
import os, sys, glob, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    n = os.path.splitext(os.path.basename(f))[0]
    if not any(n.startswith(c) for c in sys.argv[1:]): continue
    sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    L = m.LESSON; print(f"== {n}  {L['code']} {L['title']}")
    for i, s in enumerate(L['slides']):
        nb = len(s['steps']) if s['t'] == 'wb' else (len(s['say']) if isinstance(s.get('say'), list) else 1)
        extra = ''
        if s['t'] == 'ex': extra = ' [code: ' + s['code'].split('\n')[0][:50] + ' ...]'
        if s.get('pts'): extra += ' | ' + ' / '.join(p[:45] for p in s['pts'][:4])
        print(f"  {i:2d} {s['t']:7s} {s.get('h', '')[:60]:60s} b{nb}{extra}")
