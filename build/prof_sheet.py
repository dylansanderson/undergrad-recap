"""Contact sheets of the slides added/changed in the professor pass: python prof_sheet.py L01
Finds the headings inserted by prof_blocks/LNN.py ('h': '...'), then shows for each whiteboard slide the last frame of every
page (a 'clear' step starts a new page) and for ordinary slides the last beat. Output review/prof_LNN_k.png"""
import os, sys, re, io, glob, importlib.util
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
pre = sys.argv[1]
f = glob.glob(os.path.join(HERE, 'lessons', pre + '_*.py'))[0]; n = os.path.splitext(os.path.basename(f))[0]
blk = io.open(os.path.join(HERE, 'prof_blocks', pre + '.py'), encoding='utf-8').read()
heads = re.findall(r"""'h':\s*(?:"([^"]+)"|'([^']+)')""", blk); heads = [a or b for a, b in heads] + sys.argv[2:]
sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
shots = []
for si, s in enumerate(m.LESSON['slides']):
    if s.get('h') not in heads: continue
    if s['t'] == 'wb':
        st = s['steps']; ends = [b - 1 for b in range(1, len(st)) if st[b].get('clear')] + [len(st) - 1]
        shots += [(si, b) for b in ends]
    else:
        nb = len(s['say']) if isinstance(s['say'], list) else 1; shots.append((si, nb - 1))
ims = []
for si, b in shots:
    p = os.path.join(HERE, 'frames', f'{n}_{si:02d}_{b}.png')
    im = Image.open(p).resize((960, 540)); ImageDraw.Draw(im).text((8, 520), f's{si} beat{b}', fill=(200, 0, 0)); ims.append(im)
for k in range(0, len(ims), 4):
    sheet = Image.new('RGB', (1920, 1080), 'white')
    for j, im in enumerate(ims[k:k + 4]): sheet.paste(im, ((j % 2) * 960, (j // 2) * 540))
    p = os.path.join(HERE, 'review', f'prof_{pre}_{k // 4}.png'); sheet.save(p); print(p)
print('slides:', len(set(s for s, _ in shots)), 'shots:', len(shots), 'missing headings:', [h for h in heads if h not in [x.get('h') for x in m.LESSON['slides']]])
