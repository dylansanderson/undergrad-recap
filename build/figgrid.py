"""Figures of a lesson with a fraction grid (0..1, y down) so pen marks can be placed on them -> review/figgrid_<lesson>_<k>.png
python figgrid.py L03_cpsc120 4 6 10      (slide indexes; uses the last beat's frame from a --frames run)"""
import os, sys, json, glob
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
n = sys.argv[1]; sis = [(int(x.split(':')[0]), int(x.split(':')[1]) if ':' in x else None) for x in sys.argv[2:]]   # 'si' or 'si:beat'
fo = ImageFont.truetype('C:\\Windows\\Fonts\\consolab.ttf', 15)
tiles = []
for si, bt in sis:
    fs = sorted(glob.glob(os.path.join(HERE, 'frames', f'{n}_{si:02d}_{"*" if bt is None else bt}.fig.json')))
    if not fs: print('no figure for slide', si); continue
    r = json.load(open(fs[-1])); im = Image.open(fs[-1].replace('.fig.json', '.png')).convert('RGB').crop(tuple(int(v) for v in r))
    si = f'{si}:{bt}' if bt is not None else si
    sc = 760 / max(im.size); im = im.resize((int(im.width * sc), int(im.height * sc)))
    d = ImageDraw.Draw(im, 'RGBA')
    for k in range(1, 10):
        x = im.width * k / 10; y = im.height * k / 10
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 140, 120) if k != 5 else (255, 0, 140, 200), width=1)
        d.line([(0, y), (im.width, y)], fill=(0, 150, 255, 120) if k != 5 else (0, 150, 255, 200), width=1)
        d.text((x + 2, 2), f'.{k}', font=fo, fill=(200, 0, 110)); d.text((2, y + 1), f'.{k}', font=fo, fill=(0, 110, 220))
    d.text((im.width - 60, im.height - 20), f's{si}', font=fo, fill=(0, 0, 0))
    tiles.append(im)
cols = 2; rows = (len(tiles) + cols - 1) // cols
for page in range(0, len(tiles), 4):
    grp = tiles[page:page + 4]; tw = max(t.width for t in grp); th = max(t.height for t in grp)
    sheet = Image.new('RGB', (tw * min(2, len(grp)) + 10, th * ((len(grp) + 1) // 2) + 10), 'white')
    for k, t in enumerate(grp): sheet.paste(t, ((k % 2) * (tw + 10), (k // 2) * (th + 10)))
    p = os.path.join(HERE, 'review', f'figgrid_{n}_{page // 4}.png'); sheet.save(p); print(p)
