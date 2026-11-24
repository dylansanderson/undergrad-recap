"""Acronyms / mixed-case words as written in the narration, with their phonemes."""
import os, sys, re, glob, importlib.util, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
c = collections.Counter()
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    spec = importlib.util.spec_from_file_location('m', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for s in m.LESSON['slides']:
        says = [st['say'] for st in s['steps']] if s['t'] == 'wb' else (s['say'] if isinstance(s.get('say'), list) else [s.get('say', '')])
        for say in says:
            for w in re.findall(r"\b[A-Za-z]*[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9']*\b|\b[A-Z]{2,}s?\b", say or ''): c[w] += 1
from kokoro_onnx.tokenizer import Tokenizer
T = Tokenizer()
print(len(c), 'acronym-like tokens')
for w, n in sorted(c.items()):
    print(f'{w:16s} {n:4d}  {T.phonemize("the " + w + " is")}')
