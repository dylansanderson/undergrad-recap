"""Same narration beats, old (v4) vs new (v5) audio: first-word excess over a mid-sentence control (dB)."""
import os, sys, glob, json, random, hashlib, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import onset_check as oc
def h(*parts):
    m = hashlib.sha1()
    for p in parts: m.update(p if isinstance(p, bytes) else str(p).encode('utf-8'))
    return m.hexdigest()[:16]
says = []
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    n = os.path.splitext(os.path.basename(f))[0]; sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    for s in m.LESSON['slides']:
        if s.get('silent'): continue
        says += s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')]
random.seed(3); pick = random.sample(says, 120)
pick = [t for t in pick if all(os.path.exists(os.path.join(HERE, 'cache', h('af_heart', 1.0, v, t) + '.wav')) for v in ('v4', 'v5'))]
res = {}
if '--p90' in sys.argv:
    import soundfile as sf
    for ver in ('v4', 'v5'):
        ds = []
        for t in pick:
            p = os.path.join(HERE, 'cache', h('af_heart', 1.0, ver, t) + '.wav'); marks = json.load(open(p[:-4] + '.json', encoding='utf-8'))
            a, sr = sf.read(p); w = int(0.12 * sr); hp = int(0.03 * sr); n0 = int(0.45 * sr / hp)
            for _, t0, t1 in marks:
                seg = a[int(t0 * sr):int(t1 * sr)]
                if len(seg) < int(1.6 * sr): continue
                db = np.array([20 * np.log10(np.sqrt(np.mean(seg[i:i + w] ** 2)) + 1e-9) for i in range(0, len(seg) - w, hp)])
                ds.append(db[:n0].max() - np.percentile(db[n0:], 90))
        d = np.array(ds)
        print(f'{ver}: {len(d)} sentences  first word vs loud parts of the rest (p90): median {np.median(d):+.2f} dB  p90 {np.percentile(d, 90):+.2f}  '
              f'louder than the rest by >1 dB: {np.mean(d > 1) * 100:.0f}%  by >2 dB: {np.mean(d > 2) * 100:.0f}%')
    sys.exit()
if '--outliers' in sys.argv:
    import soundfile as sf
    for t in pick:
        p = os.path.join(HERE, 'cache', h('af_heart', 1.0, 'v5', t) + '.wav'); marks = json.load(open(p[:-4] + '.json', encoding='utf-8'))
        a, sr = sf.read(p)
        for mk in marks:
            x = oc.excesses(p, [mk])
            if x and x[0][0] - x[0][1] > 2.5:
                seg = a[int(mk[1] * sr):int(mk[2] * sr)]; w = int(0.12 * sr); hp = int(0.06 * sr)
                db = [20 * np.log10(np.sqrt(np.mean(seg[i:i + w] ** 2)) + 1e-9) for i in range(0, len(seg) - w, hp)]
                print(f'{x[0][0]-x[0][1]:+.1f}  first0.45s max {max(db[:7]):.1f}  sentence median(voiced) {np.median([d for d in db if d > max(db) - 25]):.1f}  max {max(db):.1f} | {mk[0][:50]}')
    sys.exit()
for ver in ('v4', 'v5'):
    xs = []
    for t in pick:
        p = os.path.join(HERE, 'cache', h('af_heart', 1.0, ver, t) + '.wav')
        if os.path.exists(p): xs += oc.excesses(p, json.load(open(p[:-4] + '.json', encoding='utf-8')))
    x = np.array(xs); d = x[:, 0] - x[:, 1]; res[ver] = d
    print(f'{ver}: {len(d)} sentences  first-word minus mid-sentence: median {np.median(d):+.2f} dB  p90 {np.percentile(d, 90):+.2f}  '
          f'share > +2 dB: {np.mean(d > 2) * 100:.0f}%')
