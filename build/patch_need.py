"""set canvas need= per figure function: python patch_need.py lessonfile name=need ..."""
import sys, re
f = sys.argv[1]; src = open(f, encoding='utf-8').read()
for kv in sys.argv[2:]:
    name, need = kv.split('=')
    pat = re.compile(r'(def (?:fig_)?' + re.escape(name) + r'\(path, w, h[^)]*\):\n    fig, ax, H = canvas\(w, h)(?:, need=\d+)?\)')
    src, n = pat.subn(r'\1, need=' + need + ')', src)
    print(name, 'patched' if n else 'NOT FOUND')
open(f, 'w', encoding='utf-8').write(src)
