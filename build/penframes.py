"""Frames during the pen strokes of one whiteboard beat -> review/penframes.png
python penframes.py <video> <timeline.json> "<heading prefix>" <beat> [fps]"""
import json, os, sys, subprocess, glob
from PIL import Image, ImageChops
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
video, tlp, pre, beat = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]); fps = float(sys.argv[5]) if len(sys.argv) > 5 else 12
TL = json.load(open(tlp, encoding='utf-8'))
for n, L in TL['lessons'].items():
    for si, s in enumerate(L['slides']):
        if s['h'].startswith(pre):
            b = next(x for x in TL['beats'] if x[2] == n and x[3] == si and x[4] == beat)
out = os.path.join(HERE, 'out', 'pf'); os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, '*.png')): os.remove(f)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{b[0]:.3f}', '-i', video, '-t', f'{b[1] - b[0]:.3f}', '-vf', f'fps={fps}', os.path.join(out, 'f%04d.png')], check=True)
fs = sorted(glob.glob(os.path.join(out, '*.png')))
# keep frames that differ from the previous one (i.e. something is being drawn)
keep, prev = [], None
for p in fs:
    im = Image.open(p).convert('RGB')
    if prev is not None and ImageChops.difference(im, prev).convert('L').point(lambda v: 255 if v > 60 else 0).getbbox(): keep.append((p, im))
    prev = im
print(len(fs), 'frames,', len(keep), 'changing')
skip = int(sys.argv[6]) if len(sys.argv) > 6 else 0
keep = keep[skip:skip + 16]
sheet = Image.new('RGB', (4 * 480, ((len(keep) + 3) // 4) * 270), 'white')
for j, (p, im) in enumerate(keep): sheet.paste(im.resize((480, 270)), ((j % 4) * 480, (j // 4) * 270))
sheet.save(os.path.join(HERE, 'review', 'penframes.png')); print(os.path.join(HERE, 'review', 'penframes.png'))
