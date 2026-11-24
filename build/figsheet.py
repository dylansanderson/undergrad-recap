"""Contact sheet of the newest version of named figures -> review/figsheet_<k>.png   python figsheet.py L14_egcp281_wheel L18_egee323_bayes ..."""
import os, sys, glob, re
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
fo = ImageFont.truetype('C:\\Windows\\Fonts\\consolab.ttf', 18)
ims = []
for key in sys.argv[1:]:
    ps = [p for p in glob.glob(os.path.join(HERE, 'figs', key + '_*.png')) if re.search(r'_\d+x\d+\.png$', p)]
    if not ps: continue
    p = max(ps, key=os.path.getmtime); im = Image.open(p).convert('RGB')
    sc = min(940 / im.width, 520 / im.height); im = im.resize((int(im.width * sc), int(im.height * sc)))
    t = Image.new('RGB', (960, 560), (200, 200, 200)); t.paste(im, (10, 30)); d = ImageDraw.Draw(t)
    d.rectangle([9, 29, 10 + im.width, 30 + im.height], outline=(255, 0, 120)); d.text((10, 4), key, font=fo, fill=(0, 0, 0)); ims.append(t)
for k in range(0, len(ims), 4):
    g = ims[k:k + 4]; s = Image.new('RGB', (1920, 560 * ((len(g) + 1) // 2)), 'white')
    for i, t in enumerate(g): s.paste(t, ((i % 2) * 960, (i // 2) * 560))
    p = os.path.join(HERE, 'review', f'figsheet_{k // 4}.png'); s.save(p); print(p)
