"""Cross-lesson fixes applied after each lesson module loads (build2.load_lessons).

REVEAL: bullet slides where the narrator talks about a bullet before the default one-bullet-per-beat schedule shows it
(found by reveal_check.py, then checked by hand; false positives left out). For these, each bullet is shown from the
first beat whose narration covers it (or its default beat, whichever is earlier), stored as s['rv'] = bullets per beat."""
import re
STOP = set('this that with from they them then than when what which where your have will into their there these those about would could should'.split())
_W = lambda t: set(w for w in re.findall(r"[a-z]+", t.lower()) if len(w) > 3 and w not in STOP)

REVEAL = {
    'L07_egcp180': ['The logic gates'],
    'L11_phys227': ['Damping, resonance', 'Light bends: refraction'],
    'L13_egcp280': ['What is a microcontroller', 'Timers and PWM'],
    'L14_egcp281': ['What is an FPGA?', 'Negative numbers'],
    'L17_egee303l': ['Every meter changes what it measures'],
    'L18_egee323': ['Independence', 'Sums of random variables'],
    'L20_egcp381': ['Measuring performance'],
    'L22_cpsc362': ['Process models'],
    'L23_cpsc332': ['Storage and indexing'],
    'L24_egee401': ['Cash-flow diagrams', 'Comparing alternatives'],
    'L25_egcp441': ['Transmission gates'],
    'L30_egcp471': ['Object detection with Haar cascades', 'Data is everything'],
}

def schedule(s):
    pts, says = s['pts'], s['say']; nb = len(says); off = nb - len(pts)
    first = []
    for i, p in enumerate(pts):
        d = max(0, i + off); pw = _W(p)
        sc = [len(pw & _W(x)) / max(1, len(pw)) for x in says]
        m = next((b for b in range(nb) if sc[b] >= 0.5), d)
        first.append(min(d, m))
    return [max([i + 1 for i, f in enumerate(first) if f <= b] + [0]) for b in range(nb)]

def _key_phrase(p):
    p = p.replace('**', '')
    if ':' in p and 3 <= p.index(':') <= 42: return p[:p.index(':')].strip()
    w = p.split(' '); out = ' '.join(w[:4])
    return out.rstrip('.,;—–-→ ')

def _sents(t):
    import tts
    return tts.sentences(t)

# AUTO: text-heavy lessons. On every bullet slide WITHOUT hand-placed marks, the pen underlines each bullet's key phrase
# (text before ':' or its first words) on the sentence where the narrator talks about it, so the eye follows the voice.
AUTO = {'L22_cpsc362', 'L23_cpsc332', 'L24_egee401', 'L29_egcp470', 'L31_bigpicture', 'L00_welcome', 'L30_egcp471',
        'L26_egcp446', 'L27_egcp450', 'L28_egcp447', 'L25_egcp441',
        'L01_math150a', 'L02_math150b', 'L05_phys225', 'L06_math170a', 'L08_math250a', 'L09_math250b', 'L10_phys226', 'L11_phys227'}
COLS = ['blue', 'green', 'orange', 'purple']

def auto_pen(s):
    pts, says = s.get('pts'), s.get('say')
    if not pts or s['t'] in ('wb', 'title', 'q', 'section', 'clip'): return
    says = says if isinstance(says, list) else [says]
    nb = len(says); off = nb - len(pts)
    if s.get('rv'): first = [next(b for b in range(nb) if s['rv'][b] > i) for i in range(len(pts))]
    elif not s.get('reveal', True) or nb == 1: first = [0] * len(pts)
    else: first = [max(0, i + off) for i in range(len(pts))]
    pens = []
    for i, p in enumerate(pts):
        pw = _W(p); best = (-1, first[i], 0)
        for b in range(first[i], nb):
            for j, x in enumerate(_sents(says[b])):
                sc = len(pw & _W(x)) / max(1, len(pw))
                if sc > best[0] + 0.05: best = (sc, b, j)
        if best[0] < 0.2: best = (0, first[i], 0)
        pens.append({'b': best[1], 'at': best[2], 'p': 'underline', 'on': _key_phrase(p), 'c': COLS[i % len(COLS)]})
    s['pen'] = pens

def apply(name, L):
    for pre in REVEAL.get(name, []):
        s = next(x for x in L['slides'] if x.get('h', '').startswith(pre))
        s['rv'] = schedule(s)
    if name in AUTO:
        for s in L['slides']:
            hand = s.get('pen') or []
            if not hand: auto_pen(s)
            elif all('fig' in p or not any(p.get('on', '') in x.replace('**', '') for x in s.get('pts', [])) for p in hand):
                # hand marks only on the figure / code, none on the bullets: keep the automatic bullet underlines too
                s.pop('pen'); auto_pen(s); s['pen'] = (s.get('pen') or []) + hand
