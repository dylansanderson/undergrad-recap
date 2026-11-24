"""Sample questions at specific slides across the series -> local/selftest_cases.json (T = series time)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'server', 'timeline.json'), encoding='utf-8')); LES = TL['lessons']; B = TL['beats']
cases = []
def add(lesson, kw, q, beat=0, expect=''):
    S = LES[lesson]['slides']
    si = next(i for i, s in enumerate(S) if kw.lower() in s['h'].lower())
    b = next(x for x in B if x[2] == lesson and x[3] == si and x[4] == min(beat, len(S[si]['say']) - 1))
    cases.append({'T': round(b[0] + (b[1] - b[0]) / 2, 2), 'expect_slide': f"{LES[lesson]['code']} · {S[si]['h']}", 'q': q, 'expect': expect})
add('L01_math150a', 'derivative', 'Why is the derivative the slope of the tangent line? Can you give me a quick example with numbers?')
add('L04_cpsc121', 'Using objects', 'show me an example of a hello world program when declaring standard namespace at the top', expect='C++ code shown in a code block, not read aloud')
add('L07_egcp180', 'Karnaugh', "I don't get why the columns go 00, 01, 11, 10 instead of counting normally.", expect='Gray code ordering')
add('L14_egcp281', 'Anatomy', "What's the difference between a signal and a variable in VHDL?", beat=2)
add('L14_egcp281', 'Anatomy', 'Can you explain that more simply?', beat=2, expect='follow-up uses the previous answer')
add('L16_egee303', 'amplifier', 'Where would I find a circuit like this in a real product?')
add('L20_egcp381', 'pipelin', 'Why does pipelining increase throughput but not make a single instruction faster?')
add('L21_cpsc351', 'race', 'What exactly goes wrong if two threads run this at the same time?')
add('L27_egcp450', 'interrupt', 'Why use interrupts here instead of just polling in a loop?')
add('L30_egcp471', 'Haar', 'Is this approach still used today, or has deep learning replaced it?')
add('L24_egee401', 'present worth', "What's the weather going to be like this weekend?", expect='brief, steers back to the lecture')
os.makedirs(os.path.join(HERE, 'local'), exist_ok=True)
json.dump(cases, open(os.path.join(HERE, 'local', 'selftest_cases.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
for c in cases: print(c['T'], c['expect_slide'])
