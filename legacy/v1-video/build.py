import os, sys, re, wave, subprocess, importlib.util, json
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfbase.ttfonts import TTFont

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.join(HERE, '..', 'voice', 'en_US-ryan-high.onnx')
OUT = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] == 'render' else None   # 'render' to skip audio
KVOICE = os.environ.get('KOKORO_VOICE')            # e.g. af_heart; unset = Piper ryan
KSPEED = float(os.environ.get('KOKORO_SPEED', '1.0'))
WORK = os.path.join(HERE, 'build' if not KVOICE else f'build_{KVOICE}'); os.makedirs(WORK, exist_ok=True)

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.LESSONS
LESSONS = load('lessons1') + load('lessons2') + load('lessons3')

W, H = 1920, 1080
FD = r'C:\Windows\Fonts\\'
def F(name, size, idx=0): return ImageFont.truetype(FD + name, size, index=idx)
def cm(name, idx=0):
    return set(TTFont('x' + name + str(idx), FD + name, subfontIndex=idx).face.charToGlyph.keys())
CM = {'segoeui.ttf': cm('segoeui.ttf'), 'segoeuib.ttf': cm('segoeuib.ttf'), 'consola.ttf': cm('consola.ttf'),
      'cambria.ttc': cm('cambria.ttc', 1), 'seguisym.ttf': cm('seguisym.ttf')}

BG = (247, 249, 252); INK = (27, 35, 51); ACC = (43, 92, 171); MUT = (93, 103, 120); CODEBG = (236, 240, 247); WHITE = (255, 255, 255)

def runs(text, fname):
    """split text into (segment, fontfile) using fallback fonts for missing glyphs"""
    out = []
    for ch in text:
        f = fname
        if ord(ch) >= 128 and ord(ch) not in CM[fname]:
            f = 'cambria.ttc' if ord(ch) in CM['cambria.ttc'] else 'seguisym.ttf'
        if out and out[-1][1] == f: out[-1][0] += ch
        else: out.append([ch, f])
    return out

def font_for(f, size): return F(f, size, 1 if f == 'cambria.ttc' else 0)

def text_len(text, fname, size):
    return sum(font_for(f, size).getlength(s) for s, f in runs(text, fname))

def draw_text(d, xy, text, fname, size, fill):
    x, y = xy
    for s, f in runs(text, fname):
        fo = font_for(f, size)
        d.text((x, y), s, font=fo, fill=fill)
        x += fo.getlength(s)

def wrap(text, fname, size, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_len(t, fname, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def chrome(d, code, sem, idx, total):
    d.rectangle([0, 0, W, 92], fill=ACC)
    draw_text(d, (70, 22), code, 'segoeuib.ttf', 38, WHITE)
    if sem:
        sw = text_len(sem, 'segoeui.ttf', 32); draw_text(d, (W - 70 - sw, 26), sem, 'segoeui.ttf', 32, (220, 230, 248))
    d.rectangle([0, H - 10, W, H], fill=(220, 227, 240))
    d.rectangle([0, H - 10, int(W * idx / total), H], fill=ACC)

def render(lesson, s, path, idx, total):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    if s['t'] == 'title':
        d.rectangle([0, 0, W, H], fill=ACC)
        draw_text(d, (140, 330), lesson['code'].upper() + ('  ·  ' + lesson['sem'] if lesson['sem'] else ''), 'segoeuib.ttf', 40, (200, 215, 245))
        y = 400
        for ln in wrap(s['h'], 'segoeuib.ttf', 96, W - 280):
            draw_text(d, (140, y), ln, 'segoeuib.ttf', 96, WHITE); y += 118
        d.rectangle([140, y + 30, 340, y + 38], fill=WHITE)
        draw_text(d, (140, y + 70), s.get('sub', ''), 'segoeui.ttf', 42, (220, 230, 248))
        d.rectangle([0, H - 10, int(W * idx / total), H], fill=WHITE)
    else:
        chrome(d, lesson['code'], lesson['sem'], idx, total)
        y = 150
        for ln in wrap(s['h'], 'segoeuib.ttf', 66, W - 200):
            draw_text(d, (100, y), ln, 'segoeuib.ttf', 66, INK); y += 82
        d.rectangle([100, y + 12, 220, y + 18], fill=ACC); y += 60
        if s['t'] == 'b':
            for p in s['pts']:
                d.ellipse([110, y + 24, 126, y + 40], fill=ACC)
                for j, ln in enumerate(wrap(p, 'segoeui.ttf', 46, W - 300)):
                    draw_text(d, (160, y), ln, 'segoeui.ttf', 46, INK); y += 62
                y += 30
        else:
            lines = s['code'].split('\n')
            size = 34
            while size > 22 and (max(text_len(l, 'consola.ttf', size) for l in lines) > W - 300 or len(lines) * size * 1.42 > H - y - 90):
                size -= 1
            lh = int(size * 1.42)
            d.rounded_rectangle([100, y, W - 100, y + lh * len(lines) + 60], radius=18, fill=CODEBG, outline=(201, 213, 234), width=2)
            yy = y + 30
            for l in lines:
                col = (110, 120, 140) if l.strip().startswith(('--', '//', '#')) else INK
                draw_text(d, (150, yy), l, 'consola.ttf', size, col); yy += lh
    im.save(path)

def wav_dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()

voice = None
def synth(text, path):
    global voice
    if KVOICE:
        import soundfile as sf
        if voice is None:
            from kokoro_onnx import Kokoro
            vd = os.path.join(HERE, '..', 'voice')
            voice = Kokoro(os.path.join(vd, 'kokoro-v1.0.onnx'), os.path.join(vd, 'voices-v1.0.bin'))
        audio, sr = voice.create(text, voice=KVOICE, speed=KSPEED, lang='en-gb' if KVOICE[0] == 'b' else 'en-us')
        sf.write(path, audio, sr, subtype='PCM_16'); return
    if voice is None:
        from piper import PiperVoice
        voice = PiperVoice.load(VOICE)
    with wave.open(path, 'wb') as wf:
        voice.synthesize_wav(text, wf)

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}'

flat = [(li, si) for li, L in enumerate(LESSONS) for si in range(len(L['slides']))]
total = len(flat)
segs, srt, chapters, t = [], [], [], 0.0
n = 1
for k, (li, si) in enumerate(flat):
    L = LESSONS[li]; s = L['slides'][si]
    base = os.path.join(WORK, f'{k:03d}')
    render(L, s, base + '.png', k + 1, total)
    if ONLY == 'render': continue
    if not os.path.exists(base + '.wav'):
        synth(s['say'], base + '.wav')
    dur = wav_dur(base + '.wav') + 0.9
    if si == 0:
        chapters.append((t, (L['code'] + (' – ' + L['slides'][0]['h'] if L['slides'][0]['t'] == 'title' and L['code'] not in ('Welcome',) else '')) if L['code'] != 'Welcome' else 'Welcome'))
    # subtitles: split into sentences, time by character share
    sents = [x.strip() for x in re.split(r'(?<=[.?!])\s+', s['say']) if x.strip()]
    chunks = []
    for x in sents:
        while len(x) > 110:
            cut = x.rfind(', ', 0, 100); cut = cut + 1 if cut > 30 else 100
            chunks.append(x[:cut].strip()); x = x[cut:].strip()
        chunks.append(x)
    speech = dur - 0.9; tot = sum(len(c) for c in chunks); tt = t
    for c in chunks:
        dd = speech * len(c) / tot
        srt.append(f'{n}\n{ts(tt)} --> {ts(tt + dd)}\n{c}\n'); n += 1; tt += dd
    seg = base + '.mp4'
    if not os.path.exists(seg):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', '24', '-i', base + '.png',
                        '-i', base + '.wav', '-af', ('volume=6dB,alimiter=limit=0.95,' if KVOICE else '') + 'apad=pad_dur=0.9', '-t', f'{dur:.3f}',
                        '-c:v', 'libx264', '-preset', 'medium', '-tune', 'stillimage', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '24',
                        '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '1', seg], check=True)
    segs.append(seg); t += dur
    print(f'[{k+1}/{total}] {L["code"]} – {s["h"][:40]}  ({dur:.1f}s, total {t/60:.1f} min)', flush=True)

if ONLY == 'render':
    print('rendered', total); sys.exit()

with open(os.path.join(WORK, 'list.txt'), 'w') as f:
    for s in segs: f.write(f"file '{s}'\n")
with open(os.path.join(WORK, 'subs.srt'), 'w', encoding='utf-8') as f: f.write('\n'.join(srt))
with open(os.path.join(WORK, 'meta.txt'), 'w', encoding='utf-8') as f:
    f.write(';FFMETADATA1\ntitle=Undergrad Recap – The Lectures\nartist=Computer Engineering, CSUF\n\n')
    for i, (st, name) in enumerate(chapters):
        en = chapters[i + 1][0] if i + 1 < len(chapters) else t
        f.write(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(st*1000)}\nEND={int(en*1000)}\ntitle={name}\n\n')
joined = os.path.join(WORK, 'joined.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(WORK, 'list.txt'), '-c', 'copy', joined], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', joined, '-i', os.path.join(WORK, 'subs.srt'), '-i', os.path.join(WORK, 'meta.txt'),
                '-map', '0', '-map', '1', '-map_metadata', '2', '-map_chapters', '2', '-c', 'copy', '-c:s', 'mov_text',
                '-metadata:s:s:0', 'language=eng', '-movflags', '+faststart', OUT], check=True)
print('DONE', OUT, f'{t/60:.1f} min')
