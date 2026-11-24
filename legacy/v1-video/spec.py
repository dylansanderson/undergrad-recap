import sys, numpy as np, soundfile as sf, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
files = sys.argv[1:-1]; out = sys.argv[-1]
fig, ax = plt.subplots(len(files) * 2, 1, figsize=(16, 5 * len(files)))
for i, f in enumerate(files):
    a, sr = sf.read(f)
    a = a[: int(sr * 9)]
    t = np.arange(len(a)) / sr
    ax[2*i].plot(t, a, lw=0.3); ax[2*i].set_title(f.split('\\')[-1] + ' waveform'); ax[2*i].set_ylim(-1, 1); ax[2*i].set_xlim(0, 9)
    ax[2*i+1].specgram(a, NFFT=512, Fs=sr, noverlap=384, cmap='magma', vmin=-120)
    ax[2*i+1].set_xlim(0, 9)
plt.tight_layout(); plt.savefig(out, dpi=70)
