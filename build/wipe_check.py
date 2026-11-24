"""grab frames across one whiteboard beat of a built video to check the write-on animation + sync.
usage: python wipe_check.py video.mp4 timeline.json "heading prefix" beat [step_s]"""
import sys, json, subprocess, os
from PIL import Image
vid, tlp, pre, beat = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]); step = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
TL = json.load(open(tlp, encoding='utf-8'))
for n, L in TL['lessons'].items():
    for si, s in enumerate(L['slides']):
        if s['h'].startswith(pre):
            b = next(x for x in TL['beats'] if x[2] == n and x[3] == si and x[4] == beat); break
    else: continue
    break
t0, t1 = b[0], b[1]; print('beat', t0, t1)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review'); ims = []
ts = [t0 + k * step for k in range(int((t1 - t0) / step))][:24]
for k, t in enumerate(ts):
    p = os.path.join(out, f'_wc{k}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', vid, '-frames:v', '1', '-vf', 'scale=480:-1', p], check=True)
    ims.append(Image.open(p))
sheet = Image.new('RGB', (480 * 4, 270 * ((len(ims) + 3) // 4)), 'white')
for k, im in enumerate(ims): sheet.paste(im, ((k % 4) * 480, (k // 4) * 270))
sheet.save(os.path.join(out, 'wipe_check.png')); print([round(t - t0, 2) for t in ts])
