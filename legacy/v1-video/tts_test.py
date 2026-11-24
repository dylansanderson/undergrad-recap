import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tts
spec = importlib.util.spec_from_file_location('l1', os.path.join(HERE, 'lessons1.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
text = m.LESSONS[1]['slides'][1]['say']
marks = tts.make(text, os.path.join(HERE, 'test_clean.wav'))
for s, a, b in marks[:4]: print(f'{a:6.2f}-{b:6.2f} {s[:60]}')
