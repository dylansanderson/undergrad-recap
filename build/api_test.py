import json, time, sys, urllib.request, os, subprocess, re
B = 'http://127.0.0.1:8765'
APP = r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Ask-the-Narrator'
def get(p, hdr=None):
    r = urllib.request.urlopen(urllib.request.Request(B + p, headers=hdr or {}), timeout=60); return r.status, dict(r.headers), r.read()
def post(p, body):
    r = urllib.request.urlopen(urllib.request.Request(B + p, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}), timeout=60)
    return json.loads(r.read())

cases = json.load(open(os.path.join(APP, 'selftest_cases.json'), encoding='utf-8'))
print('== slide lookup')
for c in cases:
    w = json.loads(get(f"/api/where?v={c['video']}&t={c['t']}")[2])['label']
    ok = w.split(': ', 1)[-1] in c['expect_slide'] or c['expect_slide'].split(' · ')[1] in w
    print(('OK  ' if ok else 'BAD '), c['video'], c['t'], '->', w)
print('== media range / subtitles')
s, h, b = get('/media/main', {'Range': 'bytes=1000-1999'}); print('range', s, h.get('Content-Range'), len(b))
s, h, b = get('/media/main', {'Range': 'bytes=8000000000-'}) if False else (None, None, None)
s, h, b = get('/subs/main.vtt'); print('vtt', s, b[:60].decode(), '...', b.count(b'-->'), 'cues')
s, h, b = get('/subs/L27_egcp450.vtt'); print('vtt L27', s, b.count(b'-->'), 'cues')
s, h, b = get('/'); print('page', s, len(b))
if '--ask' not in sys.argv: sys.exit()
print('== ask')
hist = []
for c in cases[:int(sys.argv[sys.argv.index('--ask') + 1])]:
    t0 = time.time(); j = post('/api/ask', {'video': c['video'], 't': c['t'], 'question': c['q'], 'history': hist})
    while True:
        st = json.loads(get('/api/job/' + j['job'])[2])
        if st['done']: break
        time.sleep(0.3)
    hist = (hist + [{'q': c['q'], 'a': st['text']}])[-4:]
    lu = []
    for cl in st['clips'][:2]:
        _, _, wav = get(cl['url']); p = os.path.join(os.environ['TEMP'], 'clip_t.wav'); open(p, 'wb').write(wav)
        e = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
        lu.append(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1])
    print(f"\n[{c['expect_slide']}]  Q: {c['q']}\n  where={st['where']}  timing={st['timing']}  clips={len(st['clips'])}  clip LUFS={lu}  error={st['error']}\n  A: {st['text']}")
