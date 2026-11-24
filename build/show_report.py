import json, sys
r = json.load(open(r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Ask-the-Narrator\selftest_report.json', encoding='utf-8'))
keys = ['playedBeforeAsk', 'videoStayedPaused', 'resumedOk']
ok = 0
for c in r['results']:
    where_ok = (c.get('where') or '').split(': ', 1)[-1] in c['expect_slide']
    passed = where_ok and all(c.get(k) for k in keys) and not c.get('error') and c.get('clipsPlayed') == c.get('clips') and c.get('clips', 0) > 0
    ok += passed
    print(f"{'PASS' if passed else 'FAIL'} {c['video']} t={c['t']}  where_ok={where_ok}  " + ' '.join(f'{k}={c.get(k)}' for k in keys) +
          f"  seek={c.get('seekSeconds')}s firstText={c.get('firstText') and round(c['firstText'],1)}s firstAudio={c.get('firstAudio') and round(c['firstAudio'],1)}s"
          f"  clips {c.get('clipsPlayed')}/{c.get('clips')} spoken={c.get('secondsSpoken')}s nudges={c.get('audioNudges')} err={c.get('error')}")
    if '--text' in sys.argv: print('   Q:', c['q'], '\n   A:', c.get('answer', '').replace('\n\n', ' / '), '\n')
print(f'{ok}/{len(r["results"])} passed')
