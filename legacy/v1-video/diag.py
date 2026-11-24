import sys, numpy as np, soundfile as sf, subprocess, os
p = sys.argv[1]
a, sr = sf.read(p)
print('sr', sr, 'dur', len(a)/sr, 'peak', np.abs(a).max(), 'clipped samples', int((np.abs(a) > 0.999).sum()))
# envelope in 20 ms windows; report windows whose peak is much higher than the running speech level
w = int(sr*0.02); n = len(a)//w
pk = np.array([np.abs(a[i*w:(i+1)*w]).max() for i in range(n)])
rms = np.array([np.sqrt((a[i*w:(i+1)*w]**2).mean()) for i in range(n)])
speech = rms > 0.01
# onsets: speech window following >=150ms of silence
on = [i for i in range(8, n) if speech[i] and not speech[i-8:i].any()]
print('onsets', len(on))
for i in on[:12]:
    seg = slice(i, i+15)
    print(f't={i*0.02:6.2f}s onset-peak={pk[i:i+5].max():.3f} next-300ms-peak={pk[i+5:i+15].max():.3f} median-speech-peak={np.median(pk[speech]):.3f}')
# look for discontinuities (clicks): big sample-to-sample jumps
d = np.abs(np.diff(a))
idx = np.where(d > 0.5)[0]
print('big jumps', len(idx), (idx[:10]/sr).round(3))
