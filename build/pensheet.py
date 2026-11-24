"""Every step (beat) of whiteboard slides, as the board looks at the END of that step (pen marks included).
python pensheet.py L12 "Worked example: binary search" [more heading prefixes...]   -> review/pen_L12_<k>.png
With only the lesson given, every wb slide that has pen items is rendered."""
import os, sys, glob, importlib.util
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(sys.argv[0])); sys.path.insert(0, HERE)
import board
f = glob.glob(os.path.join(HERE, 'lessons', sys.argv[1] + '_*.py'))[0]; n = os.path.splitext(os.path.basename(f))[0]
sys.path.insert(0, os.path.join(HERE, 'lessons'))
sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
want = sys.argv[2:]
BW, BH = 1768, 846
font = ImageFont.truetype('C:\\Windows\\Fonts\\segoeui.ttf', 22)
k = 0
for si, s in enumerate(m.LESSON['slides']):
    if s['t'] != 'wb': continue
    if want and not any(s['h'].startswith(w) for w in want): continue
    if not want and not any('p' in board.norm(it) for st in s['steps'] for it in st.get('w', [])): continue
    tiles = []
    for b in range(len(s['steps'])):
        im = board.render(s, m, b, board.n_through(s, b), BW, BH).resize((BW // 2, BH // 2))
        d = ImageDraw.Draw(im); d.rectangle([0, 0, BW // 2, 30], fill='#1d2f5e'); d.text((8, 2), f"{s['h'][:70]}  |  step {b}", fill='white', font=font)
        tiles.append(im)
    rows = (len(tiles) + 1) // 2
    sheet = Image.new('RGB', (BW, rows * BH // 2), 'white')
    for j, t in enumerate(tiles): sheet.paste(t, ((j % 2) * BW // 2, (j // 2) * BH // 2))
    p = os.path.join(HERE, 'review', f'pen_{sys.argv[1]}_{k}.png'); sheet.save(p); print(p); k += 1
