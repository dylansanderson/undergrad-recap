"""Pick sample questions at specific slides across the series -> selftest_cases.json (times in each video's own clock)."""
import json, sys, os
tlp, outp = sys.argv[1], sys.argv[2]
TL = json.load(open(tlp, encoding='utf-8')); LES = TL['lessons']; B = TL['beats']
def at(lesson, kw, beat=0, into=4.0, video='main'):
    S = LES[lesson]['slides']
    si = next(i for i, s in enumerate(S) if kw.lower() in s['h'].lower())
    b = next(x for x in B if x[2] == lesson and x[3] == si and x[4] == min(beat, len(S[si]['say']) - 1))
    t = b[0] + (b[1] - b[0]) / 2
    t = t if video == 'main' else t - LES[lesson]['start']
    if video == 'main': t *= SCALE_MAIN          # player clock (encoded video runs slightly long)
    return round(t, 2), S[si]['h']
import subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(tlp)))
act = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, TL['video'])], capture_output=True, text=True).stdout)
SCALE_MAIN = act / TL['duration']
cases = []
def add(lesson, kw, q, beat=0, video='main', expect=''):
    t, h = at(lesson, kw, beat, video=video)
    cases.append({'video': video, 't': t, 'expect_slide': f"{LES[lesson]['code']} · {h}", 'q': q, 'expect': expect})
add('L01_math150a', 'derivative', 'Why is the derivative the slope of the tangent line? Can you give me a quick example with numbers?')
add('L04_cpsc121', 'Using objects', 'show me an example of a hello world program when declaring standard namespace at the top', expect='C++ code shown in a code block, not read aloud')
add('L07_egcp180', 'Karnaugh', "I don't get why the columns go 00, 01, 11, 10 instead of counting normally.", expect='Gray code ordering / adjacent cells differ by one bit')
add('L14_egcp281', 'Anatomy', "What's the difference between a signal and a variable in VHDL?", beat=2)
add('L14_egcp281', 'Anatomy', 'Can you explain that more simply?', beat=2, expect='follow-up uses the previous answer')
add('L16_egee303', 'amplifier', 'Where would I find a circuit like this in a real product?')
add('L20_egcp381', 'pipelin', 'Why does pipelining increase throughput but not make a single instruction faster?')
add('L21_cpsc351', 'race', 'What exactly goes wrong if two threads run this at the same time?')
add('L27_egcp450', 'interrupt', 'Why use interrupts here instead of just polling in a loop?', video='L27_egcp450')
add('L30_egcp471', 'Haar', 'Is this approach still used today, or has deep learning replaced it?')
add('L24_egee401', 'present worth', "What's the weather going to be like this weekend?", expect='brief, steers back to the lecture')
json.dump(cases, open(outp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
for c in cases: print(c['video'], c['t'], c['expect_slide'])
