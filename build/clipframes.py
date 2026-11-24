"""4 frames across one slide of a built video -> review/clipframes.png.  python clipframes.py <video> <timeline> "<heading prefix>" """
import json, os, sys, subprocess
from PIL import Image
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
video, tlp, pre = sys.argv[1:4]
TL = json.load(open(tlp, encoding='utf-8'))
for n, L in TL['lessons'].items():
    for si, s in enumerate(L['slides']):
        if s['h'].startswith(pre):
            bs = [b for b in TL['beats'] if b[2] == n and b[3] == si]
t0, t1 = bs[0][0], bs[-1][1]
ims = []
for k in range(4):
    t = t0 + (t1 - t0) * (k + 0.5) / 4; p = os.path.join(HERE, 'out', f'cf{k}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', video, '-frames:v', '1', p], check=True)
    ims.append(Image.open(p).resize((960, 540)))
sheet = Image.new('RGB', (1920, 1080)); [sheet.paste(im, ((k % 2) * 960, (k // 2) * 540)) for k, im in enumerate(ims)]
sheet.save(os.path.join(HERE, 'review', 'clipframes.png')); print('slide', round(t0, 1), '-', round(t1, 1))
