"""Experiment: where does the hot first word come from (Kokoro vs mastering), and does the new leveler fix it?"""
import os, sys, json, glob, random
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts, onset_check
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'onset_tmp'); os.makedirs(OUT, exist_ok=True)

def report(name, files):
    xs = []
    for f in files: xs += onset_check.excesses(f, json.load(open(os.path.splitext(f)[0] + '.json')))
    x = np.array(xs); d = x[:, 0] - x[:, 1]
    print(f'{name:28s} n={len(x)}  first-minus-control median {np.median(d):+.2f}  p90 {np.percentile(d, 90):+.2f}  max {d.max():+.2f}', flush=True)

random.seed(7)
texts = [json.load(open(f, encoding='utf-8')) for f in random.sample([f for f in glob.glob(os.path.join(HERE, 'cache', '*.json'))], 10)]
texts = [' '.join(s for s, _, _ in m) for m in texts]
mode = sys.argv[1] if len(sys.argv) > 1 else 'old'
raw, mas = [], []
for i, t in enumerate(texts):
    a, marks = tts.speak(t)
    p = os.path.join(OUT, f'{mode}_{i}_raw.wav'); sf.write(p, a, tts.SR); json.dump(marks, open(p[:-4] + '.json', 'w'))
    q = os.path.join(OUT, f'{mode}_{i}_mas.wav'); tts.master(p, q); json.dump(marks, open(q[:-4] + '.json', 'w'))
    raw.append(p); mas.append(q)
report(mode + ' pre-master', raw); report(mode + ' mastered', mas)
