"""Clean Kokoro narration: per-sentence synthesis, trimming, de-click fades, controlled pauses,
gentle compression + loudness normalisation (ffmpeg), no hard limiting."""
import os, re, subprocess, tempfile
import numpy as np, soundfile as sf

VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
_k = None
SR = 24000

def _kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(VD, 'kokoro-v1.0.onnx'), os.path.join(VD, 'voices-v1.0.bin'))
    return _k

ABBR = ['e.g.', 'i.e.', 'vs.', 'etc.', 'Dr.', 'Mr.', 'Ms.', 'Prof.', 'approx.']

def sentences(text):
    t = text
    for i, a in enumerate(ABBR): t = t.replace(a, f'\x00{i}\x00')
    parts = [p.strip() for p in re.split(r'(?<=[.?!])\s+', t) if p.strip()]
    out = []
    for p in parts:
        for i, a in enumerate(ABBR): p = p.replace(f'\x00{i}\x00', a)
        out.append(p)
    return out

def _trim(a, thr=0.012, pad=0.04):
    env = np.abs(a)
    idx = np.where(env > thr)[0]
    if len(idx) == 0: return a[:0]
    s = max(0, idx[0] - int(pad * SR)); e = min(len(a), idx[-1] + int(pad * SR))
    return a[s:e]

def _fade(a, fin=0.012, fout=0.03):
    a = a.copy(); ni, no = int(fin * SR), int(fout * SR)
    if len(a) > ni + no:
        a[:ni] *= np.linspace(0, 1, ni) ** 2
        a[-no:] *= np.linspace(1, 0, no) ** 2
    return a

def _declick(a):
    """soften isolated sample jumps (Kokoro occasionally emits a 1-sample discontinuity)"""
    d = np.abs(np.diff(a))
    bad = np.where(d > 0.35)[0]
    for i in bad:
        lo, hi = max(0, i - 24), min(len(a), i + 24)
        a[lo:hi] = np.convolve(a[lo:hi], np.ones(9) / 9, mode='same')
    return a

def speak(text, voice='af_heart', speed=1.0):
    """returns (float32 mono @24k, list of (sentence, start_s, end_s))"""
    k = _kokoro(); lang = 'en-gb' if voice[0] == 'b' else 'en-us'
    pieces, marks, t = [], [], 0.0
    sil = lambda s: np.zeros(int(s * SR), dtype=np.float32)
    pieces.append(sil(0.25)); t += 0.25
    for s in sentences(text):
        a, sr = k.create(s, voice=voice, speed=speed, lang=lang)
        assert sr == SR
        a = _fade(_declick(_trim(np.asarray(a, dtype=np.float32))))
        pieces.append(a); marks.append((s, t, t + len(a) / SR)); t += len(a) / SR
        gap = 0.55 if s.endswith(('?', ':')) else 0.42
        pieces.append(sil(gap)); t += gap
    return np.concatenate(pieces), marks

def master(raw_wav, out_wav):
    """gentle compression to tame first-word bursts, then EBU R128 loudness to -16 LUFS, peaks <= -2 dBTP"""
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw_wav, '-af',
                    'highpass=f=70,acompressor=threshold=-24dB:ratio=3:attack=4:release=180:knee=6:makeup=1,'
                    'loudnorm=I=-16:TP=-2:LRA=6,aresample=44100',
                    '-ac', '1', '-c:a', 'pcm_s16le', out_wav], check=True)

def make(text, out_wav, voice='af_heart', speed=1.0):
    a, marks = speak(text, voice, speed)
    tmp = out_wav + '.raw.wav'
    sf.write(tmp, a, SR, subtype='FLOAT')
    master(tmp, out_wav); os.remove(tmp)
    return marks
