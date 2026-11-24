import os, sys, time, importlib.util
import soundfile as sf
from kokoro_onnx import Kokoro
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, '..', 'voice')
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)

spec = importlib.util.spec_from_file_location('l1', os.path.join(HERE, 'lessons1.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
text = m.LESSONS[1]['slides'][1]['say']   # first teaching slide of the first course
print(text[:200], '...')

k = Kokoro(os.path.join(V, 'kokoro-v1.0.onnx'), os.path.join(V, 'voices-v1.0.bin'))
voices = [('af_heart', 'en-us'), ('af_bella', 'en-us'), ('am_michael', 'en-us'), ('am_fenrir', 'en-us'),
          ('am_puck', 'en-us'), ('bm_george', 'en-gb'), ('bm_fable', 'en-gb')]
for i, (v, lang) in enumerate(voices, 1):
    t0 = time.time()
    audio, sr = k.create(text, voice=v, speed=1.0, lang=lang)
    sf.write(os.path.join(OUT, f'{i}_{v}.wav'), audio, sr)
    print(v, f'{len(audio)/sr:.1f}s audio in {time.time()-t0:.1f}s')
