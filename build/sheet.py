"""contact sheets: python sheet.py L14 [per=4] [all]  -> review/L14_k.png  (last beat of each slide unless 'all')"""
import sys, os, glob, re
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
tag = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 4; allb = 'all' in sys.argv
fr = sorted(glob.glob(os.path.join(HERE, 'frames', tag + '*_*.png')))
groups = {}
for f in fr:
    m = re.search(r'_(\d\d)_(\d+)\.png$', f); groups.setdefault(m.group(1), []).append((int(m.group(2)), f))
pick = []
for k in sorted(groups):
    bs = sorted(groups[k])
    pick += [f for _, f in bs] if allb else [bs[-1][1]]
os.makedirs(os.path.join(HERE, 'review'), exist_ok=True)
cols = 2; tw, th = 960, 540
for i in range(0, len(pick), per):
    chunk = pick[i:i + per]; rows = (len(chunk) + cols - 1) // cols
    sh = Image.new('RGB', (cols * tw, rows * th), 'white'); d = ImageDraw.Draw(sh)
    for j, f in enumerate(chunk):
        im = Image.open(f).resize((tw, th), Image.LANCZOS); x, y = (j % cols) * tw, (j // cols) * th
        sh.paste(im, (x, y)); d.rectangle([x, y, x + tw - 1, y + th - 1], outline='red'); d.text((x + 6, y + th - 16), os.path.basename(f), fill='red')
    out = os.path.join(HERE, 'review', f'{tag}_{i // per:02d}.png'); sh.save(out); print(out)
