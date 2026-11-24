"""Builds public/meta.json (chapters, lectures, slide marks, slide-deck list), copies the slide PDFs,
and writes public/local/subs.vtt (local testing only; YouTube shows its own captions)."""
import os, re, json, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CW = r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework'
PUB = os.path.join(HERE, 'public')
cfg = json.load(open(os.path.join(HERE, 'site_config.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'site_config.json')) else {}

TL = json.load(open(os.path.join(HERE, 'server', 'timeline.json'), encoding='utf-8'))
LES = TL['lessons']
ORDER = sorted(LES, key=lambda n: float(LES[n]['start']))
lectures, slides, seen, decks = [], [], set(), []
for n in ORDER:
    L = LES[n]
    lectures.append([round(float(L['start']), 2), f"{L['code']}: {L['title']}" if L['title'] else L['code'], n])
for t0, t1, n, si, bi in TL['beats']:
    if (n, si) in seen: continue
    seen.add((n, si)); slides.append([round(t0, 2), LES[n]['slides'][si]['h'], n, si])

os.makedirs(os.path.join(PUB, 'slides'), exist_ok=True)
for n in ORDER:
    L = LES[n]
    if not L.get('file'): continue
    want = os.path.basename(L['file']).replace('Lecture - ', 'Slides - ', 1)[:-4] + '.pdf'
    src = None
    for root, dirs, files in os.walk(CW):
        if want in files: src = os.path.join(root, want); break
    if not src: print('no slides for', n, want); continue
    safe = re.sub(r'[^A-Za-z0-9]+', '-', f"{L['code']} {L['title']}").strip('-') + '.pdf'
    shutil.copyfile(src, os.path.join(PUB, 'slides', safe))
    decks.append({'code': L['code'], 'title': L['title'], 'file': 'slides/' + safe, 'mb': round(os.path.getsize(src) / 1e6, 1)})

meta = {'duration': TL['duration'], 'chapters': TL['chapters'], 'lectures': lectures, 'slides': slides, 'decks': decks,
        'youtube': cfg.get('youtube', '')}
json.dump(meta, open(os.path.join(PUB, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

srt = os.path.join(CW, 'Undergrad_Recap_Lectures.srt')
s = open(srt, encoding='utf-8-sig').read().replace('\r\n', '\n')
s = re.sub(r'(\d\d:\d\d:\d\d),(\d\d\d)', r'\1.\2', s); s = re.sub(r'(?m)^\d+\n(?=\d\d:\d\d:\d\d\.)', '', s)
os.makedirs(os.path.join(HERE, 'local'), exist_ok=True)
open(os.path.join(HERE, 'local', 'subs.vtt'), 'w', encoding='utf-8').write('WEBVTT\n\n' + s)
print(f"meta: {len(lectures)} lectures, {len(slides)} slides, {len(decks)} decks ({sum(d['mb'] for d in decks):.0f} MB), youtube={meta['youtube'] or '-'}")
