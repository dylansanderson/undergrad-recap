"""Engagement survey: per lesson, how many beats are static (slide only) vs whiteboard vs pen-marked.
Also flags 'reading' beats: narration that mostly repeats the slide's own bullet words.
python engage_stats.py [L03 ...]  -> table; with --detail prints every static beat"""
import os, sys, glob, re, importlib.util, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import board
det = '--detail' in sys.argv; want = [a for a in sys.argv[1:] if not a.startswith('--')]
W = lambda t: set(w for w in re.findall(r"[a-z0-9]+", t.lower()) if len(w) > 3)
tot = dict(beats=0, static=0, wb=0, pen=0)
print(f"{'lesson':16s} {'beats':>5s} {'static':>6s} {'wb':>4s} {'wbpen':>5s} {'read%':>5s}  types")
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    n = os.path.splitext(os.path.basename(f))[0]
    if want and not any(n.startswith(w) for w in want): continue
    sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    S = m.LESSON['slides']; beats = static = wb = pen = 0; reads = []; types = {}
    for i, s in enumerate(S):
        types[s['t']] = types.get(s['t'], 0) + 1
        if s['t'] == 'wb':
            for k, st in enumerate(s['steps']):
                beats += 1; wb += 1
                if any('p' in board.norm(it) for it in st.get('add', []) if isinstance(it, (dict, str))): pen += 1
            continue
        says = s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')]
        slide_words = W(' '.join(s.get('pts', [])) + ' ' + s.get('big', '') + ' ' + s.get('h', ''))
        for k, sy in enumerate(says):
            beats += 1
            if s['t'] in ('title', 'section'): continue
            static += 1
            sw = W(sy); ov = len(sw & slide_words) / max(1, len(slide_words)) if slide_words else 0
            reads.append(ov)
            if det: print(f"   {n} s{i:02d} b{k} {s['t']:5s} {s.get('h','')[:52]:52s} ov={ov:.2f} code={'y' if s.get('code') else '-'} img={'y' if s.get('img') else '-'}")
    rp = 100 * sum(1 for r in reads if r > 0.5) / max(1, len(reads))
    print(f"{n:16s} {beats:5d} {static:6d} {wb:4d} {pen:5d} {rp:5.0f}  {types}")
    tot['beats'] += beats; tot['static'] += static; tot['wb'] += wb; tot['pen'] += pen
print('TOTAL', tot)
