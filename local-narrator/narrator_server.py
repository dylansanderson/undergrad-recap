"""Ask the Narrator: watch the lecture series and pause to ask the narrator a question.

Runs a small local web app (http://127.0.0.1:8765):
  * plays the combined lecture video (or any single course lecture) with subtitles
  * when you ask a question, it works out exactly what is on screen and what the narrator just said
    (from timeline.json, written by the build), sends that plus your question to Claude through the
    Claude Code CLI (`claude -p`, uses your existing Claude login, no API key needed, no tools enabled),
  * streams the answer back sentence by sentence, speaking each sentence in the narrator's voice
    (Kokoro af_heart, same mastering as the lectures) while the rest is still being written.

Start:  python narrator_server.py [--open] [--port 8765] [--model sonnet]
"""
import os, sys, re, json, time, uuid, shutil, bisect, argparse, threading, subprocess, webbrowser, traceback
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

APP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(APP)                       # the Coursework folder
sys.path.insert(0, APP)
MAIN_VIDEO = 'Undergrad_Recap_Lectures.mp4'
CLIPS = os.path.join(APP, '_clips'); os.makedirs(CLIPS, exist_ok=True)
LOG = os.path.join(APP, 'qa_log.jsonl')

ap = argparse.ArgumentParser()
ap.add_argument('--port', type=int, default=8765)
ap.add_argument('--open', action='store_true', help='open the player in the default browser')
ap.add_argument('--model', default='sonnet', help='Claude model alias or id passed to `claude --model`')
ap.add_argument('--claude', default=None, help='path to the claude executable (default: found on PATH)')
ARGS = ap.parse_args()

TL = json.load(open(os.path.join(APP, 'timeline.json'), encoding='utf-8'))
LES = TL['lessons']; BEATS = TL['beats']; BSTART = [b[0] for b in BEATS]
ORDER = sorted(LES, key=lambda n: LES[n]['start'])
VERSION = time.strftime('%Y%m%d-%H%M%S', time.localtime(max(os.path.getmtime(os.path.join(APP, f)) for f in
                                                            ('narrator_server.py', 'player.html', 'tts.py', 'timeline.json'))))

# ---------------------------------------------------------------- videos
def videos():
    out = [{'id': 'main', 'label': 'Full series: all lectures', 'file': MAIN_VIDEO}]
    for n in ORDER:
        L = LES[n]
        if L.get('file'): out.append({'id': n, 'label': f"{L['code']}: {L['title']}", 'file': L['file']})
    return [v for v in out if os.path.exists(os.path.join(ROOT, v['file']))]
VIDS = {v['id']: v for v in videos()}

_SCALE = {}
def scale(vid):
    """encoded videos run a few ms longer per joined segment than the narration timeline (~6 s over 6 h):
    map player time onto timeline time proportionally, using the real file duration from ffprobe"""
    if vid not in _SCALE:
        if vid == 'main': exp = TL['duration']
        else:
            k = ORDER.index(vid); exp = (LES[ORDER[k + 1]]['start'] if k + 1 < len(ORDER) else max(b[1] for b in BEATS if b[2] == vid)) - LES[vid]['start']
        try:
            r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, VIDS[vid]['file'])],
                               capture_output=True, text=True, timeout=20, creationflags=0x08000000 if os.name == 'nt' else 0)
            act = float(r.stdout.strip()); _SCALE[vid] = exp / act if 0.97 < exp / act < 1.03 else 1.0
        except Exception:
            _SCALE[vid] = 1.0
    return _SCALE[vid]

def series_time(vid, t):
    t = t * scale(vid)
    return t if vid == 'main' else t + LES[vid]['start']

# ---------------------------------------------------------------- context
def locate(T):
    i = max(0, bisect.bisect_right(BSTART, T) - 1)
    t0, t1, n, si, bi = BEATS[i]
    if T > TL['duration'] - 0.5 and T > t1: return None          # in the image-credit pages
    return n, si, bi

def slide_text(s, upto=None):
    say = s['say'] if upto is None else s['say'][:upto + 1]
    return ' '.join(x for x in say if x)

def context(vid, t):
    T = series_time(vid, t); loc = locate(T)
    if loc is None:
        return {'label': 'Image credits', 'prompt': 'The viewer is on the image-credit pages at the very end of the series.'}
    n, si, bi = loc; L = LES[n]; S = L['slides']; s = S[si]
    k = ORDER.index(n)
    outline = '\n'.join(f"  {'>>' if j == si else ('  ' if j > si else 'ok')} {x['h']}" for j, x in enumerate(S))
    parts = [f"SERIES: 'Computer Engineering, Re-Taught': {len(ORDER)} lectures re-teaching a computer engineering B.S. course by course.",
             f"CURRENT LECTURE: {L['code']}: {L['title']}" + (f" ({L['tag']})" if L.get('tag') else ''),
             'ALL LECTURES IN THE SERIES, in viewing order. Already watched (earlier): ' + '; '.join(f"{LES[x]['code']} {LES[x]['title']}" for x in ORDER[:k]) +
             '. Not yet watched (later): ' + '; '.join(f"{LES[x]['code']} {LES[x]['title']}" for x in ORDER[k + 1:]) + '.',
             f"SLIDES IN THIS LECTURE (ok = already covered, >> = on screen now):\n{outline}",
             f"ON SCREEN NOW: the slide titled '{s['h']}'"]
    if s['pts']: parts.append('Bullet points on this slide: ' + ' | '.join(s['pts']))
    if s.get('big'): parts.append('Statement on the slide: ' + s['big'])
    if s.get('code'): parts.append('Code on the slide:\n' + s['code'])
    if si > 0: parts.append(f"WHAT THE NARRATOR SAID ON THE PREVIOUS SLIDE ('{S[si-1]['h']}'):\n{slide_text(S[si-1])}")
    parts.append(f"WHAT THE NARRATOR HAS SAID SO FAR ON THIS SLIDE:\n{slide_text(s, bi)}")
    if si + 1 < len(S): parts.append(f"Coming up next in this lecture: {S[si+1]['h']}")
    return {'label': f"{L['code']} · slide {si + 1}: {s['h']}", 'lesson': n, 'slide': si, 'beat': bi,
            'prompt': '\n\n'.join(p for p in parts if p)}

SYSTEM = """You are the narrator and lecturer of the video series "Computer Engineering, Re-Taught". A viewer has just paused the lecture to ask you a question out loud. You are given exactly what is on screen and what you (the narrator) have just said.

How to answer:
- Speak as the same warm, clear lecturer: conversational, precise, encouraging. Address the viewer as "you".
- Ground the answer in the current slide and lecture when relevant ("on this slide...", "remember from the previous slide..."). If the question is about something coming later or from another course in the series, answer it and mention where it is covered.
- Refer to other material by name, never by number: "later in this lecture", "in the slide on processes", "in the Computer Design lecture". Do not cite slide numbers or lecture numbers.
- Start directly with the answer. Do not open with praise such as "Great question" or "Good question".
- Be concise: usually 3 to 5 sentences, about 50 to 100 words, which is 20 to 40 seconds when spoken. Go longer (up to about 220 words) only if the viewer asks for detail, a derivation or a worked example. When a small worked example with real numbers would make it click, use one.
- Short follow-ups such as "explain that more simply" or "another example?" refer to your most recent answer. Just answer them; don't ask what they meant.
- You answer through THREE channels and choose, for every question, whichever combination teaches it best: VOICE (always: your spoken explanation), CODE (typed on screen, never spoken) and WHITEBOARD (a drawing on screen, never spoken). Decide from the question and the slide: a "why" or concept question is often voice alone; "show me", "example of", "write", "implement" or "what does the code look like" needs code; anything with a shape (a circuit, a data structure, a diagram, a waveform, a graph, a geometry or physics setup) benefits from the whiteboard; many questions deserve two or all three. Never describe in words what would be clearer typed or drawn.
- Channel details. Your answer has two kinds of text. (1) SPOKEN TEXT: everything outside code blocks is converted to speech. Write it as plain spoken sentences only: no markdown, no bullet lists, no headings, no emojis, no LaTeX, no inline code or backticks. Say math in words ("x squared", "one over R C") and name code in words ("the cout line", "the always block", "the include line", "the std prefix", "the rising edge check"), never symbol by symbol (never say "colon colon", "less than less than", "semicolon"). (2) SHOWN CODE: anything inside a fenced code block (three backticks plus a language tag, e.g. ```cpp ... ```) is displayed on screen as typed code and is NOT read aloud.
- Whenever the question asks for, or would clearly be answered best by, actual code (a program, a function, a snippet, HDL such as Verilog or VHDL, assembly, SQL, shell commands, a testbench), SHOW it in a fenced code block instead of describing it in words. Never read code out loud. Use the language tag that fits: cpp, c, python, java, verilog, vhdl, asm, sql, bash, text. For truth tables, state tables, timing tables, pin connections or a register layout, use a ```text block with neatly aligned columns. Code must be complete, correct and compile/synthesize as shown, short (usually under 30 lines), with brief comments on the important lines. Match the style of the course on screen (e.g. C++ with iostream in the C++ courses, Verilog in the Verilog course, VHDL in the VHDL course).
- You can also DRAW on the whiteboard. When a picture would make the idea clearer (a circuit schematic, a stack, queue or linked list with its contents, a tree or graph, a memory or register layout, a state diagram, a timing diagram or waveform, a pipeline chart, a free-body diagram, a plot), draw it in a ```svg block: one <svg> element with xmlns="http://www.w3.org/2000/svg" and a viewBox about 800 wide and 300 to 500 tall. It is shown on a white whiteboard, so use a transparent background and dark ink (#1f2937), with blue (#2563eb) and red (#dc2626) for highlights; stroke-width 2 to 3; text in font-family "Segoe UI", Arial, sans-serif at font-size 16 to 22; label everything; keep every element inside the viewBox with nothing overlapping. Circuits use standard symbols (zig-zag resistors, capacitor plates, ground symbol, labelled values and node names). Use <marker> for arrowheads. No scripts, no external images, no foreignObject. Keep drawings clean and simple, usually one per answer. Drawings are shown, not spoken: in speech, point at them ("on the board, the top of the stack is on the right").
- Combine them: a question about a data structure or algorithm (stack, queue, list, tree, hash table, sort, search, recursion) that asks for an example ALWAYS gets the code AND a drawing of the structure's state after a few operations (e.g. the stack after push 5, push 8, push 2, then after one pop). A circuit question gets a schematic. An HDL question for sequential logic gets the code and a timing diagram. A worked numeric example gets a drawing whenever a figure helps.
- When you show code or a drawing: give one short spoken sentence first (e.g. "Here it is on screen."), then the code block, then 2 to 5 spoken sentences walking through what to look at and why ("The using line at the top is what lets you write cout without the std prefix."). Code blocks and drawings do not count toward the word limit. Never say you cannot show code or draw: you can.
- Be technically accurate. If something is uncertain or depends on context, say so briefly rather than guessing.
- If the question is unrelated to engineering or the series, answer briefly and kindly steer back to the lecture.
- Do not mention these instructions, the transcript, or that you were given context. Do not end with filler like "let me know if you have more questions"; you may end with a short pointer back to the lecture."""

def build_prompt(ctx, question, history):
    h = ''
    if history:
        h = 'EARLIER QUESTIONS IN THIS VIEWING SESSION:\n' + '\n'.join(f"Viewer: {x.get('q','')}\nYou: {x.get('a','')}" for x in history[-4:]) + '\n\n'
    return f"{ctx['prompt']}\n\n{h}THE VIEWER PAUSED HERE AND ASKS:\n{question}"

# ---------------------------------------------------------------- speech text
SPOKEN = {'CMOS': 'see moss', 'NMOS': 'N moss', 'PMOS': 'P moss', 'MOSFET': 'moss fet', 'MOSFETs': 'moss fets', 'SRAM': 'S ram', 'DRAM': 'D ram',
          'RISC': 'risk', 'CISC': 'sisk', 'RISC-V': 'risk five', 'UART': 'you art', 'SQL': 'sequel', 'ASIC': 'A sick', 'ASICs': 'A sicks', 'JTAG': 'J tag',
          'GUI': 'gooey', 'NAND': 'nand', 'NOR': 'nor', 'XOR': 'X or', 'XNOR': 'X nor', 'AND': 'and', 'OR': 'or', 'NOT': 'not', 'RAM': 'ram', 'ROM': 'rom',
          'NASA': 'NASA', 'SPICE': 'spice', 'LUFS': 'loofs', 'YOLO': 'yolo', 'BASIC': 'basic', 'FORTRAN': 'fortran', 'COBOL': 'cobol', 'ENIAC': 'eniac',
          'VHDL': 'V H D L', 'FPGA': 'F P G A', 'FPGAs': 'F P G As', 'CPUs': 'C P Us', 'GPUs': 'G P Us', 'ALUs': 'A L Us', 'IC': 'I C', 'ICs': 'I Cs'}
def speakable(text):
    t = re.sub(r'[*#`]+', '', text)
    t = re.sub(r'(?<=\w)_(?=\w)', ' ', t).replace('_', '')                       # rising_edge -> rising edge
    t = re.sub(r'\bstd::', 'standard ', t).replace('::', ' ')
    for a, b in [('—', ', '), ('–', ' to '), ('≈', ' about '), ('%', ' percent'), ('&', ' and '), ('→', ' to '), ('×', ' times '), ('=', ' equals '),
                 ('Ω', ' ohms'), ('µ', 'micro'), ('°', ' degrees'), ('≤', ' less than or equal to '), ('≥', ' greater than or equal to ')]:
        t = t.replace(a, b)
    def acr(m):
        w = m.group(0)
        if w in SPOKEN: return SPOKEN[w]
        core, s = (w[:-1], 's') if w.endswith('s') and w[:-1].isupper() else (w, '')
        if core in SPOKEN: return SPOKEN[core] + s
        return ' '.join(core) + s
    return re.sub(r'\b(?:RISC-V|[A-Z]{2,6}s?)\b', acr, t)

# ---------------------------------------------------------------- TTS (one Kokoro instance, serialized)
TTS_LOCK = threading.Lock(); _tts = None
def tts_mod():
    global _tts
    if _tts is None:
        import tts as m; _tts = m
    return _tts

def synth(sentence, path):
    import soundfile as sf
    m = tts_mod()
    with TTS_LOCK:
        a, _ = m.speak(speakable(sentence))
    raw = path + '.raw.wav'; sf.write(raw, a, m.SR, subtype='FLOAT')
    m.master(raw, path); os.remove(raw)

def warm():
    try:
        p = os.path.join(CLIPS, 'warm.wav'); synth('Ready.', p); os.remove(p); print('[tts] voice ready', flush=True)
    except Exception as e:
        print('[tts] warm-up failed:', e, flush=True)

# ---------------------------------------------------------------- jobs
JOBS = {}
class Job:
    def __init__(self, vid, t, q, history):
        self.id = uuid.uuid4().hex[:12]; self.vid, self.t, self.q, self.history = vid, t, q, history
        self.ctx = context(vid, t); self.text = ''; self.clips = []; self.done = False; self.error = None
        self.created = time.time(); self.timing = {}; self.proc = None; self.cancelled = False
        self.dir = os.path.join(CLIPS, self.id); os.makedirs(self.dir, exist_ok=True)

def claude_exe():
    return ARGS.claude or shutil.which('claude') or shutil.which('claude.exe')

SENT_END = re.compile(r'(?<=[.!?])["”)]?\s+(?=["“(]?[A-Z0-9])')
ABBR = ('e.g.', 'i.e.', 'vs.', 'etc.', 'Dr.', 'Mr.', 'Ms.', 'approx.', 'Fig.')

class SpeechFilter:
    """Splits a streamed answer into spoken text and fenced code blocks (```lang ... ```).
    feed() yields ('text', s) for speakable text and ('code', '') when a code block begins.
    A trailing run of backticks is held back until we know whether it is a fence."""
    def __init__(self): self.rest = ''; self.code = False
    def feed(self, d, end=False):
        self.rest += d; out = []
        while True:
            i = self.rest.find('```')
            if i < 0:
                if self.code:
                    self.rest = '' if end else self.rest[-2:]
                else:
                    keep = 0 if end else len(self.rest) - len(self.rest.rstrip('`'))
                    s = self.rest[:len(self.rest) - keep]
                    if s: out.append(('text', s))
                    self.rest = self.rest[len(self.rest) - keep:]
                return out
            if self.code: self.code = False; self.rest = self.rest[i + 3:]
            else:
                if i: out.append(('text', self.rest[:i]))
                out.append(('code', '')); self.code = True; self.rest = self.rest[i + 3:]

def run_job(job):
    tq, tq_lock, tq_ev = [], threading.Lock(), threading.Event()
    def speaker():                                   # turns finished sentences into clips, in order
        i = 0
        while True:
            tq_ev.wait(0.2)
            with tq_lock:
                items = tq[i:]; tq_ev.clear()
            for s in items:
                if job.cancelled: return
                if s is None: return
                p = os.path.join(job.dir, f'{i:03d}.wav')
                try:
                    synth(s, p)
                    job.clips.append({'i': i, 'url': f'/clip/{job.id}/{i:03d}.wav', 'text': s})
                    job.timing.setdefault('first_audio', round(time.time() - job.created, 2))
                except Exception as e:
                    print('[tts] error', e, flush=True)
                i += 1
    def push(s):
        with tq_lock: tq.append(s)
        tq_ev.set()
    sp = threading.Thread(target=speaker, daemon=True); sp.start()
    try:
        exe = claude_exe()
        if not exe: raise RuntimeError('The Claude Code CLI ("claude") was not found on PATH. Install Claude Code and sign in, then restart.')
        cmd = [exe, '-p', '--output-format', 'stream-json', '--verbose', '--include-partial-messages', '--model', ARGS.model,
               '--tools', '', '--no-session-persistence', '--setting-sources', '', '--strict-mcp-config', '--disable-slash-commands',
               '--system-prompt', SYSTEM]
        flags = 0x08000000 if os.name == 'nt' else 0      # CREATE_NO_WINDOW
        job.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=APP, creationflags=flags)
        job.proc.stdin.write(build_prompt(job.ctx, job.q, job.history).encode('utf-8')); job.proc.stdin.close()
        buf = ''; final = None
        sp_in = SpeechFilter()
        def cut_sentences():
            nonlocal buf
            while True:                               # cut complete sentences off the front of the buffer
                cut = None
                for m in SENT_END.finditer(buf):
                    head = buf[:m.start()].rstrip()
                    if len(head) >= 20 and not head.endswith(ABBR): cut = m; break
                if not cut: break
                push(buf[:cut.start()].strip()); buf = buf[cut.end():]
        def feed(d, end=False):
            nonlocal buf
            for kind, x in sp_in.feed(d, end):        # code blocks are shown, never spoken
                if kind == 'text': buf += x; cut_sentences()
                elif buf.strip(): push(buf.strip()); buf = ''   # a code block starts: speak what came before it
        for line in job.proc.stdout:
            if job.cancelled: break
            try: ev = json.loads(line)
            except Exception: continue
            if ev.get('type') == 'stream_event':
                e = ev['event']
                if e.get('type') == 'content_block_delta' and e['delta'].get('type') == 'text_delta':
                    d = e['delta']['text']; job.text += d
                    job.timing.setdefault('first_text', round(time.time() - job.created, 2))
                    feed(d)
            elif ev.get('type') == 'result':
                final = ev
                if ev.get('is_error') or ev.get('subtype') != 'success':
                    raise RuntimeError('Claude returned an error: ' + str(ev.get('result') or ev.get('subtype')))
        rc = job.proc.wait()
        if final is None and not job.cancelled:
            err = job.proc.stderr.read().decode('utf-8', 'replace').strip()
            raise RuntimeError(f'claude exited with code {rc}. {err[:400]}' if err else f'claude exited with code {rc} without an answer (are you signed in? run `claude` once).')
        if not job.text and final: job.text = final.get('result', ''); feed(job.text)
        feed('', end=True)
        if buf.strip(): push(buf.strip())
        job.timing['text_done'] = round(time.time() - job.created, 2)
    except Exception as e:
        job.error = str(e); print('[ask] error:', e, flush=True)
    push(None); sp.join()
    job.timing['all_audio'] = round(time.time() - job.created, 2)
    job.done = True
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'when': time.strftime('%Y-%m-%d %H:%M:%S'), 'video': job.vid, 't': round(job.t, 1), 'where': job.ctx['label'],
                                'question': job.q, 'answer': job.text, 'error': job.error, 'timing': job.timing}, ensure_ascii=False) + '\n')
    except Exception: pass

def cleanup_clips(max_age=6 * 3600):
    now = time.time()
    for d in os.listdir(CLIPS):
        p = os.path.join(CLIPS, d)
        if os.path.isdir(p) and now - os.path.getmtime(p) > max_age: shutil.rmtree(p, ignore_errors=True)

# ---------------------------------------------------------------- subtitles
def srt_to_vtt(path):
    s = open(path, encoding='utf-8-sig').read().replace('\r\n', '\n')
    s = re.sub(r'(\d\d:\d\d:\d\d),(\d\d\d)', r'\1.\2', s)
    s = re.sub(r'(?m)^\d+\n(?=\d\d:\d\d:\d\d\.)', '', s)
    return 'WEBVTT\n\n' + s

# ---------------------------------------------------------------- HTTP
class H(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *a): pass

    def send(self, code, body=b'', ctype='application/json', extra=None):
        if isinstance(body, (dict, list)): body = json.dumps(body, ensure_ascii=False).encode('utf-8')
        elif isinstance(body, str): body = body.encode('utf-8')
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(body)

    def file(self, path, ctype):
        size = os.path.getsize(path); rng = self.headers.get('Range'); start, end = 0, size - 1; code = 200
        m = re.match(r'bytes=(\d*)-(\d*)', rng or '')
        if m:
            if m.group(1): start = int(m.group(1)); end = int(m.group(2)) if m.group(2) else size - 1
            else: start = size - int(m.group(2))
            end = min(end, size - 1); code = 206
        if start > end or start >= size:
            self.send_response(416); self.send_header('Content-Range', f'bytes */{size}'); self.send_header('Content-Length', '0'); self.end_headers(); return
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Length', str(end - start + 1))
        if code == 206: self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        try:
            with open(path, 'rb') as f:
                f.seek(start); left = end - start + 1
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk: break
                    self.wfile.write(chunk); left -= len(chunk)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError): pass

    def do_GET(self):
        u = urlparse(self.path); p = unquote(u.path); q = parse_qs(u.query)
        try:
            if p in ('/', '/index.html'):
                return self.send(200, open(os.path.join(APP, 'player.html'), encoding='utf-8').read(), 'text/html; charset=utf-8')
            if p == '/api/videos':
                return self.send(200, {'videos': [{'id': v['id'], 'label': v['label']} for v in VIDS.values()],
                                       'chapters': TL['chapters'], 'lessons': {n: {'code': LES[n]['code'], 'title': LES[n]['title'], 'start': LES[n]['start']} for n in ORDER},
                                       'duration': TL['duration']})
            if p == '/api/marks':                         # chapter markers in this video's own clock: lectures + slides
                vid = q.get('v', ['main'])[0]
                if vid not in VIDS: return self.send(404, {'error': 'no such video'})
                sc = scale(vid); off = 0.0 if vid == 'main' else LES[vid]['start']
                pt = lambda T: round((T - off) / sc, 2)
                lec = [[pt(LES[n]['start']), f"{LES[n]['code']}: {LES[n]['title']}" if LES[n]['title'] else LES[n]['code'], n]
                       for n in ORDER if vid == 'main' or n == vid]
                sl, seen = [], set()
                for t0, t1, n, si, bi in BEATS:
                    if (n, si) in seen or (vid != 'main' and n != vid): continue
                    seen.add((n, si)); sl.append([pt(t0), LES[n]['slides'][si]['h'], n])
                return self.send(200, {'lectures': lec, 'slides': sl})
            if p == '/api/version':
                return self.send(200, {'version': VERSION})
            if p == '/api/where':
                vid = q.get('v', ['main'])[0]; t = float(q.get('t', ['0'])[0])
                c = context(vid, t); return self.send(200, {'label': c['label']})
            if p == '/api/context':                       # debugging aid: the exact text Claude receives
                vid = q.get('v', ['main'])[0]; t = float(q.get('t', ['0'])[0])
                return self.send(200, build_prompt(context(vid, t), q.get('q', ['(question)'])[0], []), 'text/plain; charset=utf-8')
            if p == '/api/selftest-cases':
                return self.send(200, open(os.path.join(APP, 'selftest_cases.json'), encoding='utf-8').read())
            if p.startswith('/media/'):
                v = VIDS.get(p[7:]);
                if not v: return self.send(404, {'error': 'no such video'})
                return self.file(os.path.join(ROOT, v['file']), 'video/mp4')
            if p.startswith('/subs/'):
                v = VIDS.get(p[6:].replace('.vtt', ''))
                srt = os.path.splitext(os.path.join(ROOT, v['file']))[0] + '.srt' if v else ''
                if not v or not os.path.exists(srt): return self.send(404, 'WEBVTT\n\n', 'text/vtt')
                return self.send(200, srt_to_vtt(srt), 'text/vtt; charset=utf-8')
            if p.startswith('/api/job/'):
                j = JOBS.get(p[9:])
                if not j: return self.send(404, {'error': 'no such job'})
                return self.send(200, {'text': j.text, 'clips': j.clips, 'done': j.done, 'error': j.error, 'where': j.ctx['label'], 'timing': j.timing})
            if p.startswith('/clip/'):
                jid, name = p[6:].split('/', 1)
                path = os.path.join(CLIPS, re.sub(r'[^0-9a-f]', '', jid), re.sub(r'[^0-9.a-z]', '', name))
                if not os.path.exists(path): return self.send(404, {'error': 'no clip'})
                return self.file(path, 'audio/wav')
            return self.send(404, {'error': 'not found'})
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as e:
            traceback.print_exc(); self.send(500, {'error': str(e)})

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            n = int(self.headers.get('Content-Length') or 0); body = json.loads(self.rfile.read(n) or b'{}')
            if p == '/api/ask':
                q = (body.get('question') or '').strip()[:1500]
                vid = body.get('video', 'main'); t = float(body.get('t', 0))
                if not q: return self.send(400, {'error': 'empty question'})
                if vid not in VIDS: return self.send(400, {'error': 'unknown video'})
                hist = [x for x in body.get('history', []) if isinstance(x, dict)][-4:]
                j = Job(vid, t, q, hist); JOBS[j.id] = j
                threading.Thread(target=run_job, args=(j,), daemon=True).start()
                print(f"[ask] {j.ctx['label']} | {q}", flush=True)
                return self.send(200, {'job': j.id, 'where': j.ctx['label']})
            if p.startswith('/api/cancel/'):
                j = JOBS.get(p[12:])
                if j:
                    j.cancelled = True
                    if j.proc and j.proc.poll() is None: j.proc.kill()
                return self.send(200, {'ok': True})
            if p == '/api/shutdown':                       # a newer copy of the app is taking over this port
                if self.headers.get('X-Narrator') != 'takeover': return self.send(403, {'error': 'forbidden'})
                self.send(200, {'ok': True}); print('[server] a newer version is taking over; stopping', flush=True)
                threading.Thread(target=lambda: (time.sleep(0.3), SRV and SRV.shutdown()), daemon=True).start(); return
            if p == '/api/selftest-report':
                with open(os.path.join(APP, 'selftest_report.json'), 'w', encoding='utf-8') as f: json.dump(body, f, indent=1, ensure_ascii=False)
                print('[selftest] report saved', flush=True); return self.send(200, {'ok': True})
            return self.send(404, {'error': 'not found'})
        except Exception as e:
            traceback.print_exc(); self.send(500, {'error': str(e)})

class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False          # on Windows SO_REUSEADDR lets a 2nd copy bind the same port while the old one keeps answering
    def server_bind(self):
        import socket
        if os.name == 'nt' and hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()
    def handle_error(self, request, client_address):
        if isinstance(sys.exc_info()[1], (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, TimeoutError)): return  # browser dropped a video connection while seeking
        super().handle_error(request, client_address)

SRV = None
def take_over(port):
    """Port busy: if it is an older (or same) copy of this app, ask it to stop so the files on disk now are what runs."""
    import urllib.request
    base = f'http://127.0.0.1:{port}'
    try: other = json.loads(urllib.request.urlopen(base + '/api/version', timeout=3).read()).get('version')
    except Exception: other = None                           # very old copy (no version endpoint) or another program
    try:
        urllib.request.urlopen(urllib.request.Request(base + '/api/shutdown', data=b'{}', method='POST',
                                                      headers={'Content-Type': 'application/json', 'X-Narrator': 'takeover'}), timeout=3)
    except Exception:
        return False
    print(f'Stopped the copy that was already running (version {other}); starting version {VERSION}.', flush=True)
    for _ in range(30):
        time.sleep(0.25)
        try: return Server(('127.0.0.1', port), H)
        except OSError: pass
    return False

def main():
    global SRV
    try: sys.stdout.reconfigure(errors='replace')
    except Exception: pass
    cleanup_clips()
    threading.Thread(target=warm, daemon=True).start()
    try: srv = Server(('127.0.0.1', ARGS.port), H)
    except OSError:
        srv = take_over(ARGS.port)
        if not srv:
            print(f'Port {ARGS.port} is busy and the program using it could not be stopped. If an old Ask the Narrator is still running, '
                  f'close it (or restart the computer) and run this again.', flush=True)
            return 1
    SRV = srv
    url = f'http://127.0.0.1:{ARGS.port}/'
    print(f'Ask the Narrator is running at {url}  (videos: {len(VIDS)}; Claude via {claude_exe() or "NOT FOUND"}, model {ARGS.model})', flush=True)
    print('Close this window (or press Ctrl+C) to stop.', flush=True)
    if ARGS.open: threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: pass

if __name__ == '__main__': sys.exit(main())
