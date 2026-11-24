"""Contact sheets of the pen-marked ordinary slides of a lesson (frames from a --frames run): the last beat of each slide that has marks,
plus any beat whose marks are not kept. -> review/spen_<lesson>_<k>.png   python spensheet.py L03_cpsc120 [--all]"""
import os, sys, glob, importlib.util
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(sys.argv[0])); sys.path.insert(0, HERE)
n = sys.argv[1]; allb = '--all' in sys.argv
f = glob.glob(os.path.join(HERE, 'lessons', n + '.py'))[0]
sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
import fixes; fixes.apply(n, m.LESSON)
picks = []
for si, s in enumerate(m.LESSON['slides']):
    if s['t'] == 'wb' or not s.get('pen'): continue
    nb = len(s['say']) if isinstance(s.get('say'), list) else 1
    bs = sorted({p['b'] for p in s['pen']})
    want = bs if allb else sorted({bs[-1]} | {p['b'] for p in s['pen'] if not p.get('keep', True)} | ({b for b in bs} if s.get('reveal', True) and s.get('pts') and nb > 1 and False else set()))
    picks += [(si, b) for b in want]
fo = ImageFont.truetype('C:\\Windows\\Fonts\\consolab.ttf', 22)
tw, th, cols = 960, 540, 2
for page in range(0, len(picks), 4):
    grp = picks[page:page + 4]
    sheet = Image.new('RGB', (tw * cols, th * ((len(grp) + 1) // 2)), 'white')
    for k, (si, b) in enumerate(grp):
        im = Image.open(os.path.join(HERE, 'frames', f'{n}_{si:02d}_{b}.png')).convert('RGB').resize((tw, th))
        ImageDraw.Draw(im).text((8, th - 30), f's{si} b{b}', font=fo, fill=(220, 0, 120))
        sheet.paste(im, ((k % cols) * tw, (k // cols) * th))
    p = os.path.join(HERE, 'review', f'spen_{n}_{page // 4}.png'); sheet.save(p); print(p)
