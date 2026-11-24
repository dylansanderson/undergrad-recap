"""Measure how hot the first word of each sentence is vs the rest of that sentence.
usage: python onset_check.py [wav ...]   (default: a sample of cached narration wavs)
Reports, per file, the median and 90th-percentile 'onset excess' in dB:
  excess = peak 120 ms RMS within the first 0.45 s  -  median 120 ms RMS (voiced windows) of the rest of the sentence."""
import sys, os, glob, json, random
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))

def excesses(wav, marks):
    a, sr = sf.read(wav, dtype='float32')
    if a.ndim > 1: a = a.mean(1)
    w = int(0.12 * sr); hop = int(0.03 * sr); out = []
    for _, t0, t1 in marks:
        s = a[int(t0 * sr):int(t1 * sr)]
        if len(s) < int(1.6 * sr): continue
        r = np.array([np.sqrt(np.mean(s[i:i + w] ** 2)) + 1e-9 for i in range(0, len(s) - w, hop)])
        db = 20 * np.log10(r)
        n0 = int(0.45 * sr / hop)
        rest = db[n0:]; rest = rest[rest > rest.max() - 25]
        if len(rest) < 5: continue
        m0 = len(db) // 2  # control: same statistic for a window in the middle of the sentence
        mid = np.concatenate([db[:m0], db[m0 + n0:]]); mid = mid[mid > mid.max() - 25]
        out.append((db[:n0].max() - np.median(rest), db[m0:m0 + n0].max() - np.median(mid)))
    return out

def main():
    files = sys.argv[1:]
    if not files:
        random.seed(1)
        files = random.sample([f for f in glob.glob(os.path.join(HERE, 'cache', '*.wav')) if not os.path.basename(f).startswith('sil')], 40)
    allx = []
    for f in files:
        mp = os.path.splitext(f)[0] + '.json'
        if not os.path.exists(mp): continue
        allx += excesses(f, json.load(open(mp, encoding='utf-8')))
    allx = np.array(allx)
    for k, nm in ((0, 'first word '), (1, 'mid control')):
        x = allx[:, k]
        print(f'{nm}: sentences {len(x)}  excess dB median {np.median(x):+.2f}  p75 {np.percentile(x,75):+.2f}  p90 {np.percentile(x,90):+.2f}  max {x.max():+.2f}')
    d = allx[:, 0] - allx[:, 1]
    print(f'first-word minus control: median {np.median(d):+.2f} dB  p90 {np.percentile(d,90):+.2f} dB')

if __name__ == '__main__': main()
