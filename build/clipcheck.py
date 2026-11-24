"""Find generated figures whose content touches the image edge (text or drawing cut off).
python clipcheck.py  -> prints suspects (figs/*.png, newest version of each figure name)"""
import os, sys, glob, re
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
latest = {}
for p in glob.glob(os.path.join(HERE, 'figs', 'L*_*.png')):
    key = re.sub(r'_\d+x\d+\.png$', '', os.path.basename(p))
    if key not in latest or os.path.getmtime(p) > os.path.getmtime(latest[key]): latest[key] = p
for key, p in sorted(latest.items()):
    a = np.asarray(Image.open(p).convert('L'), dtype=np.int16)
    bg = int(np.median(np.r_[a[0], a[-1], a[:, 0], a[:, -1]]))
    ink = np.abs(a - bg) > 60
    edges = {'right': ink[:, -3:].sum(), 'left': ink[:, :3].sum(), 'top': ink[:3].sum(), 'bottom': ink[-3:].sum()}
    bad = {k: int(v) for k, v in edges.items() if v > 12}
    if bad: print(f'{key:40s} {bad}')
