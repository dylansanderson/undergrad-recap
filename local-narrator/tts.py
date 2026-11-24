"""Clean Kokoro narration: per-sentence synthesis, trimming, de-click fades, controlled pauses,
gentle compression + loudness normalisation (ffmpeg), no hard limiting."""
import os, re, subprocess, tempfile
import numpy as np, soundfile as sf

_HERE = os.path.dirname(os.path.abspath(__file__))
VD = os.path.join(_HERE, 'voice') if os.path.isdir(os.path.join(_HERE, 'voice')) else os.path.join(_HERE, '..', 'voice')
_k = None
SR = 24000

def _kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(VD, 'kokoro-v1.0.onnx'), os.path.join(VD, 'voices-v1.0.bin'))
    return _k

ABBR = ['e.g.', 'i.e.', 'vs.', 'etc.', 'Dr.', 'Mr.', 'Ms.', 'Prof.', 'approx.']

# ---- pronunciation dictionary (US English IPA, Kokoro/espeak symbols). Only the voice uses it; subtitles keep the spelling.
LEX_I = {   # any capitalisation
    'phasor': 'fˈeɪzɚ', 'phasors': 'fˈeɪzɚz', 'phasor\'s': 'fˈeɪzɚz',
    'sinusoid': 'sˈaɪnəsˌɔɪd', 'sinusoids': 'sˈaɪnəsˌɔɪdz', 'sinusoidal': 'sˌaɪnəsˈɔɪdəl', 'sinusoidally': 'sˌaɪnəsˈɔɪdəli',
    'kinematics': 'kˌɪnəmˈæɾɪks', 'kinematic': 'kˌɪnəmˈæɾɪk',
    'debounce': 'dˌiːbˈaʊns', 'debounced': 'dˌiːbˈaʊnst', 'debouncer': 'dˌiːbˈaʊnsɚ', 'debouncing': 'dˌiːbˈaʊnsɪŋ',
    'dijkstra': 'dˈaɪkstɹə', 'dijkstra\'s': 'dˈaɪkstɹəz',
    'fourier': 'fˈʊɹieɪ', 'gaussian': 'ɡˈaʊsiən', 'gaussians': 'ɡˈaʊsiənz',
    'thevenin': 'tˈɛvənɪn', 'thevenin\'s': 'tˈɛvənɪnz', 'kirchhoff': 'kˈɪɹkɔf', 'kirchhoff\'s': 'kˈɪɹkɔfs',
    'laplace': 'ləplˈɑːs', 'laplacian': 'ləplˈɑːsiən', 'leibniz': 'lˈaɪbnɪts', 'leibniz\'s': 'lˈaɪbnɪtsᵻz',
    'lagrange': 'ləɡɹˈeɪndʒ', 'lagrange\'s': 'ləɡɹˈeɪndʒᵻz', 'lissajous': 'lˈiːsəʒuː', 'karnaugh': 'kˈɑːɹnoʊ',
    'poisson': 'pwɑːsˈoʊn', 'modulo': 'mˈɑːdʒəloʊ', 'mosfet': 'mˈɑːsfɛt', 'mosfets': 'mˈɑːsfɛts', 'mosfet\'s': 'mˈɑːsfɛts',
    'kilohm': 'kˈɪloʊm', 'kilohms': 'kˈɪloʊmz', 'inode': 'ˈaɪnoʊd', 'inodes': 'ˈaɪnoʊdz', 'broglie': 'bɹˈɔɪ',
    'covariance': 'koʊvˈɛɹiəns', 'zener': 'zˈiːnɚ', 'zener\'s': 'zˈiːnɚz', 'moore': 'mˈɔːɹ', 'moore\'s': 'mˈɔːɹz',
    'redis': 'ɹˈɛdɪs', 'cardioid': 'kˈɑːɹdiˌɔɪd', 'stroustrup': 'stɹˈoʊstɹʌp',
}
LEX_C = {   # exact spelling only (so "arm" the body part and "out" the word are untouched)
    'AAPCS': 'ˌeɪˌeɪpˌiːsˌiːˈɛs', 'AMAT': 'ˈeɪmæt', 'ARM': 'ˈɑːɹm', "ARM's": 'ˈɑːɹmz', 'BIT': 'bˈɪt', 'CAP': 'kˈæp',
    'GPIO': 'dʒˌiːpˌiːˌaɪˈoʊ', 'IoT': 'ˌaɪˌoʊtˈiː', 'MACRS': 'mˈeɪkɚz', 'OUT': 'ˈaʊt', 'SUB': 'sˈʌb', 'PINs': 'pˈɪnz',
    'RAII': 'ˌɑːɹˌeɪˌaɪˈaɪ', 'SIMD': 'sˈɪmd', 'SECDED': 'sˈɛkdɛd', 'XOR': 'ˈɛksˈɔːɹ', 'XNOR': 'ˈɛksnˈɔːɹ', 'SysTick': 'sˈɪstˌɪk',
}
_LEX_RE = re.compile(r"(?<![\w'])(" + '|'.join(sorted(map(re.escape, list(LEX_I) + list(LEX_C)), key=len, reverse=True)) + r")(?![\w'])", re.I)

def lex_spans(s):
    out = []
    for m in _LEX_RE.finditer(s):
        w = m.group(1); ipa = LEX_C.get(w) or LEX_I.get(w.lower())
        if ipa: out.append((m.start(1), m.end(1), w, ipa))
    return out

def lex_sig(text):
    """'' when no dictionary word occurs (so existing audio caches stay valid), else a signature of the entries used"""
    return '|'.join(sorted({f'{w}={ipa}' for _, _, w, ipa in lex_spans(text)}))

_STAND_IN = 'xylophone'
def to_phonemes(k, s, lang, spans):
    """phonemize the WHOLE sentence with a stand-in word where each dictionary word is (so the other words keep
    their context, e.g. the article 'a' is not read as the letter), then swap the stand-in's phonemes for the dictionary's"""
    sp = k.tokenizer.phonemize(_STAND_IN, lang)
    t, i = '', 0
    for a, b, _, _ in spans: t += s[i:a] + _STAND_IN; i = b
    ph = k.tokenizer.phonemize(t + s[i:], lang)
    if sp and ph.count(sp) == len(spans):
        for _, _, _, ipa in spans: ph = ph.replace(sp, ipa, 1)
        return ph
    parts, i = [], 0                         # fallback: phonemize the pieces separately
    for a, b, _, ipa in spans:
        if s[i:a].strip(): parts.append(k.tokenizer.phonemize(s[i:a], lang))
        parts.append(ipa); i = b
    if s[i:].strip(): parts.append(k.tokenizer.phonemize(s[i:], lang))
    return ' '.join(p for p in parts if p).replace(' ,', ',').replace(' .', '.').replace(' ?', '?').replace(' !', '!')

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

def _rms_db(a, w):
    """centred moving RMS (dB) at every sample, via cumulative sums"""
    c = np.concatenate([[0.0], np.cumsum(a.astype(np.float64) ** 2)])
    i = np.arange(len(a)); lo = np.clip(i - w // 2, 0, len(a)); hi = np.clip(i + w // 2, 0, len(a))
    return 10 * np.log10((c[hi] - c[lo]) / np.maximum(hi - lo, 1) + 1e-12)

def _level_onset(a, look=1.2, ref_from=0.8, head=2.0, tail=3.0):
    """Kokoro renders the first word of a sentence hot. Measure the sentence's own speaking level
    (median of voiced 120 ms windows after the opening), then pull any part of the opening that is
    more than `head` dB above it down to that level; elsewhere only tame words > `tail` dB hot.
    Gain is smoothed (60 ms hold + 80 ms average) so it never pumps or clicks."""
    if len(a) < int((ref_from + 0.6) * SR): return a
    db = _rms_db(a, int(0.12 * SR))
    body = db[int(ref_from * SR):]; body = body[body > body.max() - 25]
    if len(body) < SR // 4: return a
    ref = np.median(body)
    thr = np.full(len(a), ref + tail); n = int(look * SR)
    thr[:n] = ref + head + (tail - head) * np.clip((np.arange(n) - 0.6 * n) / (0.4 * n), 0, 1)  # ease back to tail
    hop = int(0.005 * SR); idx = np.arange(0, len(a), hop)
    g = np.minimum(0.0, thr[idx] - db[idx])                       # gain curve on a 5 ms grid
    k = 6; gp = np.pad(g, k, mode='edge')                          # 60 ms hold (min filter)
    g = np.min(np.stack([gp[i:i + len(g)] for i in range(2 * k + 1)]), axis=0)
    k = 8; gp = np.pad(g, k, mode='edge')                          # 80 ms smoothing
    g = np.convolve(gp, np.ones(2 * k + 1) / (2 * k + 1), mode='valid')
    g = np.interp(np.arange(len(a)), idx, g)
    return (a * 10 ** (g / 20)).astype(np.float32)

def speak(text, voice='af_heart', speed=1.0):
    """returns (float32 mono @24k, list of (sentence, start_s, end_s))"""
    k = _kokoro(); lang = 'en-gb' if voice[0] == 'b' else 'en-us'
    pieces, marks, t = [], [], 0.0
    sil = lambda s: np.zeros(int(s * SR), dtype=np.float32)
    pieces.append(sil(0.25)); t += 0.25
    for s in sentences(text):
        spans = lex_spans(s)
        if spans: a, sr = k.create(to_phonemes(k, s, lang, spans), voice=voice, speed=speed, lang=lang, is_phonemes=True)
        else: a, sr = k.create(s, voice=voice, speed=speed, lang=lang)
        assert sr == SR
        a = _fade(_level_onset(_declick(_trim(np.asarray(a, dtype=np.float32)))))
        pieces.append(a); marks.append((s, t, t + len(a) / SR)); t += len(a) / SR
        gap = 0.55 if s.endswith(('?', ':')) else 0.42
        pieces.append(sil(gap)); t += gap
    return np.concatenate(pieces), marks

PRE = 'highpass=f=70,treble=g=-2:f=7500'   # no compressor: it relaxes in every pause and re-boosts first words

def master(raw_wav, out_wav, target=-16.0, peak_ceiling=-1.0):
    """tone + gentle compression, then ONE fixed gain to reach -16 LUFS.
    (v4 used single-pass dynamic loudnorm, whose gain crept up during the pauses between sentences
    and made every first word ~2 dB hot; a static gain cannot pump.)"""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', raw_wav, '-af', PRE + ',ebur128=peak=sample', '-f', 'null', '-'],
                       capture_output=True, text=True, check=True).stderr
    summ = r[r.rfind('Summary:'):]
    I = float(re.search(r'I:\s+(-?[\d.]+) LUFS', summ).group(1))
    gain = target - I + 0.2   # +0.2 dB: the peak limiter removes about that much loudness
    # lookahead peak limiter: gain <= 1 always and auto-level OFF, so it can only shave plosive peaks,
    # never lift a word (unlike a compressor recovering in a pause)
    lim = f'alimiter=limit={10 ** (peak_ceiling / 20):.4f}:attack=4:release=40:level=0'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw_wav, '-af', f'{PRE},volume={gain:.2f}dB,{lim},aresample=44100',
                    '-ac', '1', '-c:a', 'pcm_s16le', out_wav], check=True)

def make(text, out_wav, voice='af_heart', speed=1.0):
    a, marks = speak(text, voice, speed)
    tmp = out_wav + '.raw.wav'
    sf.write(tmp, a, SR, subtype='FLOAT')
    master(tmp, out_wav); os.remove(tmp)
    return marks

