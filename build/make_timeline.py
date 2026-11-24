"""Rebuild the Ask-the-Narrator timeline.json from lesson files + cached narration durations (same math as build2.py).
usage: python make_timeline.py <cache-version e.g. v4|v5> <out.json> [--credits]"""
import os, sys, re, json, glob, hashlib, importlib.util, wave
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ver, outp = sys.argv[1], sys.argv[2]; credits = '--credits' in sys.argv
def h(*parts):
    m = hashlib.sha1()
    for p in parts: m.update(p if isinstance(p, bytes) else str(p).encode('utf-8'))
    return m.hexdigest()[:16]
def wav_dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
mods = []
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    n = os.path.splitext(os.path.basename(f))[0]; sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); mods.append((n, m))
beats, chapters, t = [], [], 0.0
for n, m in mods:
    L = m.LESSON; chapters.append([round(t, 3), L.get('chapter', L['code'] + (' – ' + L['title'] if L.get('title') else ''))])
    for si, s in enumerate(L['slides']):
        says = s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')]
        for bi, say in enumerate(says):
            if s.get('silent'): d = float(s['silent'])
            else: d = wav_dur(os.path.join(HERE, 'cache', h('af_heart', 1.0, ver, say) + '.wav'))
            d += 0.55 if bi == len(says) - 1 else 0.05
            beats.append([round(t, 3), round(t + d, 3), n, si, bi]); t += d
if credits: chapters.append([round(t, 3), 'Image credits']); t += 10.0 * 3
les = {}
for n, m in mods:
    L = m.LESSON; folder = L.get('folder')
    title = re.sub(r'[\\/:*?"<>|]', '-', f"{L['code']} {L.get('title', '')}" if folder else f"{n[1:3]} {L['code']} - {L.get('title', '')}").strip()
    les[n] = {'code': L['code'], 'title': L.get('title', ''), 'tag': L.get('tag', ''), 'file': (folder + '/' if folder else '') + f'Lecture - {title}.mp4',
              'start': next(b[0] for b in beats if b[2] == n),
              'slides': [{'h': s.get('h', '').replace('**', ''), 'pts': [p.replace('**', '') for p in s.get('pts', [])], 'big': s.get('big', '').replace('**', ''),
                          'code': s.get('code', '') if isinstance(s.get('code'), str) else '',
                          'say': s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')]} for s in L['slides']]}
json.dump({'video': 'Undergrad_Recap_Lectures.mp4', 'duration': round(t, 3), 'lessons': les, 'beats': beats, 'chapters': chapters},
          open(outp, 'w', encoding='utf-8'), ensure_ascii=False)
print('beats', len(beats), 'duration', round(t / 60, 1), 'min ->', outp)
