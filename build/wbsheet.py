"""contact sheet of the final frame of every whiteboard slide in a lesson: python wbsheet.py L01 [beat=-1]"""
import os, sys, glob, importlib.util
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
f = glob.glob(os.path.join(HERE, 'lessons', sys.argv[1] + '_*.py'))[0]; n = os.path.splitext(os.path.basename(f))[0]
sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
ims = []
for si, s in enumerate(m.LESSON['slides']):
    if s['t'] != 'wb': continue
    ims.append(Image.open(os.path.join(HERE, 'frames', f'{n}_{si:02d}_{len(s["steps"]) - 1}.png')).resize((960, 540)))
for k in range(0, len(ims), 4):
    sheet = Image.new('RGB', (1920, 1080), 'white')
    for j, im in enumerate(ims[k:k + 4]): sheet.paste(im, ((j % 2) * 960, (j // 2) * 540))
    p = os.path.join(HERE, 'review', f'wb_{sys.argv[1]}_{k // 4}.png'); sheet.save(p); print(p)
