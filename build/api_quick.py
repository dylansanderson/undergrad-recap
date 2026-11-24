import json, time, urllib.request, os
B = 'http://127.0.0.1:8765'
cases = json.load(open(r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Ask-the-Narrator\selftest_cases.json', encoding='utf-8'))
for _ in range(60):
    try: urllib.request.urlopen(B + '/api/videos', timeout=2); break
    except Exception: time.sleep(1)
hist = []
for c in [cases[2], cases[3], cases[9]]:
    req = urllib.request.Request(B + '/api/ask', data=json.dumps({'video': c['video'], 't': c['t'], 'question': c['q'], 'history': hist}).encode(), headers={'Content-Type': 'application/json'})
    j = json.loads(urllib.request.urlopen(req).read())
    while True:
        st = json.loads(urllib.request.urlopen(B + '/api/job/' + j['job']).read())
        if st['done']: break
        time.sleep(0.3)
    hist.append({'q': c['q'], 'a': st['text']})
    print(f"Q: {c['q']}\n  {len(st['text'].split())} words, timing {st['timing']}\n  A: {st['text']}\n")
