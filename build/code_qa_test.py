"""Ask code-type questions; check code is shown (fenced) and none of it is spoken."""
import json, time, urllib.request, sys
B = 'http://127.0.0.1:' + (sys.argv[1] if len(sys.argv) > 1 else '8766')
def where(t):
    return json.loads(urllib.request.urlopen(f'{B}/api/where?v=main&t={t}').read())['label']
def find(code_kw, t0=0):
    # scan forward in 30 s steps for a slide label containing code_kw
    t = t0
    while t < 30000:
        if code_kw in where(t): return t
        t += 30
cases = [(12140.0, 'can you give me a worked example of a stack datatype implemented in c++'),
         (find('EGEE 203') + 300, 'Can you draw a voltage divider with 12 volts, a 1k and a 2k resistor, and show the output voltage?'),
         (find('EGCP 446') + 400, 'Show me a D flip-flop in Verilog and draw its timing diagram.')]
if len(sys.argv) > 2 and sys.argv[2] == 'mix':
    cases = [(12140.0, 'Why is it called last in, first out?'),
             (12140.0, 'How does inserting a node in the middle of a linked list work?'),
             (find('PHYS 225') + 200, 'Can you show me how to break a force at 30 degrees into components?')]
if len(sys.argv) > 2 and sys.argv[2] == 'old': cases = [(4150.0,'show me an example of a hello world program when declaring standard namespace at the top'),
         (find('EGCP 281') + 600, 'Can you show me a 4-bit counter with synchronous reset in VHDL?'),
         (find('EGCP 446') + 400, 'Show me a Verilog module for a 2-to-1 mux and a quick testbench for it.'),
         (find('EGCP 180') + 900, 'What does the truth table for a full adder look like?'),
         (find('EGEE 203') + 300, 'Why is current the same everywhere in a series circuit?')]
for _ in range(90):
    try: urllib.request.urlopen(B + '/api/videos', timeout=2); break
    except Exception: time.sleep(1)
answers = []
import os
sys.stdout.reconfigure(encoding='utf-8')
AOUT = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'out', 'answers.json')
for t, q in cases:
    j = json.loads(urllib.request.urlopen(urllib.request.Request(B + '/api/ask', data=json.dumps({'video': 'main', 't': t, 'question': q, 'history': []}).encode(),
                                                              headers={'Content-Type': 'application/json'})).read())
    while True:
        st = json.loads(urllib.request.urlopen(B + '/api/job/' + j['job']).read())
        if st['done']: break
        time.sleep(0.3)
    answers.append(st['text']); json.dump(answers, open(AOUT, 'w', encoding='utf-8'), ensure_ascii=False)
    spoken = ' | '.join(c['text'] for c in sorted(st['clips'], key=lambda c: c['i']))
    leak = [s for s in ('#include', 'cout <<', 'endmodule', 'end architecture', '```', '<=', 'begin', '<svg', 'viewBox', 'stroke') if s in spoken]
    print(f"[{st['where']}]  t={t:.0f}\n  Q: {q}\n  FULL ANSWER:\n{st['text']}\n  SPOKEN ({len(st['clips'])} clips): {spoken}\n"
          f"  code blocks={st['text'].count('```') // 2}  leaked-code-in-speech={leak}  timing={st['timing']} error={st['error']}\n" + '=' * 80)
