import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import onset_check as o
import numpy as np, soundfile as sf
pre = sys.argv[1]
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'onset_tmp', pre + '_*_mas.wav'))):
    marks = json.load(open(f[:-4] + '.json'))
    a, sr = sf.read(f)
    for (s, t0, t1) in marks:
        x = o.excesses(f, [(s, t0, t1)])
        if x and x[0][0] - x[0][1] > 1.5:
            seg = a[int(t0 * sr):int(t1 * sr)]; w = int(0.12 * sr); hop = int(0.03 * sr)
            db = [20 * np.log10(np.sqrt(np.mean(seg[i:i + w] ** 2)) + 1e-9) for i in range(0, len(seg) - w, hop)]
            print(f'{x[0][0]-x[0][1]:+.2f}', os.path.basename(f), s[:60])
            print('   ', ' '.join(f'{d:.0f}' for d in db[:40]))
