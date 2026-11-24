"""Ask the narrator questions while paused on whiteboard worked examples (final installed video + timeline)."""
import json, time, urllib.request, subprocess, os
APP = r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Ask-the-Narrator'
B = 'http://127.0.0.1:8765'
TL = json.load(open(os.path.join(APP, 'timeline.json'), encoding='utf-8'))
act = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                            os.path.join(os.path.dirname(APP), TL['video'])], capture_output=True, text=True).stdout)
scale = act / TL['duration']
def t_of(pre, beat):
    for n, L in TL['lessons'].items():
        for si, s in enumerate(L['slides']):
            if s['h'].startswith(pre):
                b = next(x for x in TL['beats'] if x[2] == n and x[3] == si and x[4] == beat)
                return (b[0] + b[1]) / 2 * scale
cases = [('Worked example: the chain rule', 2, 'Why do we multiply the two rates instead of adding them?'),
         ('Worked example: two blocks and a pulley', 2, 'Why does the tension disappear when you add the two equations?'),
         ('Worked example: finding eigenvalues', 2, 'How did you get v1 = (1, 1) from that row?'),
         ('Worked example: light leaving water', 1, 'What would happen at 50 degrees instead of 40?'),
         ('Worked example: a MOSFET motor driver', 3, 'Which way does current flow through the flyback diode when the MOSFET turns off?'),
         ('Worked example: a join, row by row', 2, 'Why did order 2 disappear from the output?'),
         ('Worked example: an ISR, and why', 1, 'Would making ticks a local variable fix the hang instead?'),
         ('Worked example: a pipeline diagram with a load-use stall', 3, "Why can't forwarding remove this stall completely?"),
         ('Worked example: building an inverter from two transistors', 3, 'So when does a CMOS inverter actually use power?')]
for _ in range(60):
    try: urllib.request.urlopen(B + '/api/videos', timeout=2); break
    except Exception: time.sleep(1)
for pre, beat, q in cases:
    t = t_of(pre, beat)
    j = json.loads(urllib.request.urlopen(urllib.request.Request(B + '/api/ask', data=json.dumps({'video': 'main', 't': t, 'question': q, 'history': []}).encode(),
                                                                  headers={'Content-Type': 'application/json'})).read())
    while True:
        st = json.loads(urllib.request.urlopen(B + '/api/job/' + j['job']).read())
        if st['done']: break
        time.sleep(0.3)
    print(f"[{st['where']}]  t={t:.1f}\n  Q: {q}\n  A: {st['text']}\n  clips={len(st['clips'])} timing={st['timing']} error={st['error']}\n")
