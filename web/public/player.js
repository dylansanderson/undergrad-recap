'use strict';
const $ = id => document.getElementById(id);
const LOG = $('log'), QB = $('qbox');
const store = { get(k, d) { try { const x = localStorage.getItem(k); return x === null ? d : JSON.parse(x); } catch (e) { return d; } },
                set(k, x) { try { localStorage.setItem(k, JSON.stringify(x)); } catch (e) {} } };
let META = null, V = null, SCALE = 1, job = null, history = [], audio = new Audio(), queue = [], played = 0, answering = false;
let stats = null;   // per-question measurements (used by the self-test)
const QS = new URLSearchParams(location.search);
// can this browser make an element full screen? (iPhone Safari can't; iPad Safari can, with the webkit prefix)
const NATIVE_FS = !!((document.fullscreenEnabled || document.webkitFullscreenEnabled) &&
                     (Element.prototype.requestFullscreen || Element.prototype.webkitRequestFullscreen)) && !QS.get('nofs');

function fmt(t) { t = Math.max(0, Math.floor(t || 0)); const h = Math.floor(t / 3600), m = Math.floor(t % 3600 / 60), s = t % 60;
  return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(s).padStart(2, '0'); }
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ---------------- the video: one interface over a YouTube embed or (local testing) an HTML5 <video>
class Emitter {
  constructor() { this.h = {}; }
  addEventListener(t, f, o) { (this.h[t] = this.h[t] || []).push({ f, once: o && o.once }); }
  removeEventListener(t, f) { this.h[t] = (this.h[t] || []).filter(x => x.f !== f); }
  emit(t) { for (const x of [...(this.h[t] || [])]) { if (x.once) this.removeEventListener(t, x.f); try { x.f({ type: t }); } catch (e) { console.error(e); } } }
}
class YTVideo extends Emitter {
  constructor(el, id, t0) {
    super(); this._paused = true; this._ready = false; this.el = el;
    const host = document.createElement('div'); el.replaceWith(host); host.id = 'screen';
    this.p = new YT.Player(host, { videoId: id, width: '100%', height: '100%',
      playerVars: { rel: 0, playsinline: 1, cc_load_policy: 1, fs: NATIVE_FS ? 0 : 1, /* where we can't do our own full screen, let YouTube's button work */ iv_load_policy: 3, start: Math.floor(t0 || 0), origin: location.origin },
      events: { onReady: () => { this._ready = true; this.frame = this.p.getIframe(); this.frame.classList.add('screen'); this.frame.id = 'screen';
                                 this.frame.setAttribute('allow', 'autoplay; encrypted-media; picture-in-picture');
                                 const wait = () => this.duration > 0 ? this.emit('loadedmetadata') : setTimeout(wait, 200); wait(); },
                onError: e => { this.error = e.data; if (!this._paused) { this._paused = true; this.emit('pause'); } this.emit('error'); },
                onStateChange: e => { const s = e.data;
                  if (s === 1 || s === 3) { if (this._paused) { this._paused = false; this.emit('play'); } }
                  else if (s === 2 || s === 0) { if (!this._paused) { this._paused = true; this.emit('pause'); } } } } });
    setInterval(() => { if (this._ready && !this._paused) this.emit('timeupdate'); }, 250);
  }
  get currentTime() { return this._ready ? this.p.getCurrentTime() : 0; }
  set currentTime(t) { if (!this._ready) return; this.p.seekTo(t, true); setTimeout(() => { this.emit('seeked'); this.emit('timeupdate'); }, 250); }
  get duration() { return this._ready ? this.p.getDuration() : NaN; }
  get paused() { return this._paused; }
  play() { if (!this._ready) return Promise.resolve(); this._paused = false; this.p.playVideo(); this.emit('play');
    return new Promise(res => { const t0 = performance.now(); const chk = () => (this.p.getPlayerState() === 1 || performance.now() - t0 > 4000) ? res() : setTimeout(chk, 100); chk(); }); }
  pause() { if (!this._ready) return; this.p.pauseVideo(); if (!this._paused) { this._paused = true; this.emit('pause'); } }
}
function loadYT() { return new Promise(res => { window.onYouTubeIframeAPIReady = res; const s = document.createElement('script'); s.src = 'https://www.youtube.com/iframe_api'; document.head.appendChild(s); }); }

async function init() {
  META = await (await fetch('meta.json', { cache: 'no-cache' })).json();
  fetch('/api/warm').catch(() => {});                 // wake the narrator server while the video loads
  $('autoRes').checked = store.get('autoResume', false);
  $('autoRes').onchange = () => store.set('autoResume', $('autoRes').checked);
  const ch = $('chap'); ch.innerHTML = '<option>Jump to a lecture…</option>';
  for (const [t, n] of META.chapters) { const o = document.createElement('option'); o.value = t; o.textContent = n; ch.appendChild(o); }
  ch.onchange = () => { const T = parseFloat(ch.value); if (!isNaN(T)) { V.currentTime = T / SCALE + 0.05; } ch.selectedIndex = 0; };
  for (const d of META.decks) {
    const li = document.createElement('li'), a = document.createElement('a'); a.href = d.file; a.target = '_blank'; a.rel = 'noopener';
    a.innerHTML = '<b></b><span></span><small></small>'; a.children[0].textContent = d.code; a.children[1].textContent = d.title; a.children[2].textContent = d.mb + ' MB';
    li.appendChild(a); $('decks').appendChild(li);
  }
  const qt = QS.get('t'); const t0 = qt ? qt.split(':').reduce((s, x) => s * 60 + parseFloat(x || 0), 0) : store.get('pos', 0);
  const scr = $('screen');
  if (QS.get('local')) {                                   // local testing with the mp4 on disk
    const v = document.createElement('video'); v.id = 'screen'; v.className = 'screen'; v.controls = true; v.preload = 'metadata';
    v.setAttribute('controlslist', 'nofullscreen'); v.src = '/local/video.mp4';
    const tr = document.createElement('track'); tr.kind = 'subtitles'; tr.label = 'English'; tr.srclang = 'en'; tr.src = '/local/subs.vtt'; tr.default = true; v.appendChild(tr);
    scr.replaceWith(v); V = v;
    v.addEventListener('dblclick', e => { e.preventDefault(); toggleFull(); });
  } else if (META.youtube) {
    await loadYT(); V = new YTVideo(scr, QS.get('yt') || META.youtube, t0);   // ?yt=<id> only for testing the player
    V.addEventListener('error', () => { $('hint').textContent = `The video couldn't be played (YouTube error ${V.error}). It may still be processing: please try again later. The slides are available under "Slides".`; });
  } else {
    scr.textContent = 'The lecture video is being uploaded. Check back soon: the slides are already available under "Slides".'; return;
  }
  V.addEventListener('loadedmetadata', () => {
    const D = V.duration; SCALE = (D > 0 && Math.abs(META.duration / D - 1) < 0.03) ? META.duration / D : 1;
    if (QS.get('local') && t0 > 0 && t0 < D - 5) V.currentTime = t0;
    buildMarks(); drawBars(); refreshWhere(true);
  }, { once: true });
  V.addEventListener('timeupdate', updateBars); V.addEventListener('seeked', updateBars);
  V.addEventListener('timeupdate', () => { refreshWhere(false); store.set('pos', V.currentTime); });
  V.addEventListener('seeked', () => refreshWhere(true));
  V.addEventListener('play', () => { $('playBtn').textContent = '❚❚ Pause'; }); V.addEventListener('pause', () => { $('playBtn').textContent = '▶ Play'; });
  if (!(window.SpeechRecognition || window.webkitSpeechRecognition)) { $('micBtn').style.display = 'none'; }
  if (QS.get('selftest')) selftest();
}

// ---------------- chapter bars (lectures across the series, slides within the current lecture) + skip buttons
let MARKS = null, lastLec, CODES = {};
function buildMarks() {
  const pt = T => T / SCALE;
  for (const [T, label, n] of META.lectures) CODES[n] = label.split(':')[0];
  MARKS = { lectures: META.lectures.map(([T, label, n]) => [pt(T), label, n]), slides: META.slides.map(([T, h, n, si]) => [pt(T), h, n, si]) };
}
function idxAt(arr, t) { let lo = 0, hi = arr.length - 1, i = -1; while (lo <= hi) { const m = (lo + hi) >> 1; if (arr[m][0] <= t + 0.05) { i = m; lo = m + 1; } else hi = m - 1; } return i; }
function jump(a) { V.currentTime = a + 0.05; refreshWhere(true); }
function seg(bar, a, b, lo, hi, title, i) {
  const d = document.createElement('div'); d.className = 'sg' + (i % 2 ? ' alt' : '');
  d.style.left = ((a - lo) / (hi - lo) * 100) + '%'; d.style.width = Math.max(0.2, (b - a) / (hi - lo) * 100) + '%';
  d.title = fmt(a) + '  ' + title; d.onclick = () => jump(a);
  bar.appendChild(d);
}
function chip(box, a, bold, rest, title) {
  const c = document.createElement('button'); c.type = 'button'; c.className = 'chip'; c.setAttribute('role', 'listitem'); c.title = fmt(a) + '  ' + title;
  const b = document.createElement('b'); b.textContent = bold; c.appendChild(b);
  if (rest) { const s = document.createElement('span'); s.textContent = rest; c.appendChild(s); }
  c.onclick = () => { chipTouched = 0; jump(a); }; box.appendChild(c);
}
// keep the current chip in view, unless the visitor is scrolling the row themselves
let chipTouched = -1e9;
for (const id of ['lecChips', 'slideChips']) for (const ev of ['pointerdown', 'wheel', 'touchstart'])
  $(id).addEventListener(ev, () => { chipTouched = performance.now(); }, { passive: true });
function showChip(box, i, smooth) {
  const c = box.children[i]; if (!c || performance.now() - chipTouched < 5000) return;
  const left = c.offsetLeft - (box.clientWidth - c.offsetWidth) / 2;  box.scrollTo({ left: Math.max(0, left), behavior: smooth ? 'smooth' : 'auto' });
}
// re-centre when a row changes size (first layout, rotating a phone, resizing the window)
if (window.ResizeObserver) { const ro = new ResizeObserver(es => { for (const e of es) if (e.target._on >= 0) showChip(e.target, e.target._on, false); });
  ro.observe($('lecChips')); ro.observe($('slideChips')); }
function setOn(box, i) {
  if (box._on === i) return false; const old = box.children[box._on]; old && old.classList.remove('on');
  box._prev = box._on; box._on = i; const c = box.children[i]; c && c.classList.add('on'); return true;
}
function drawBars() {
  const D = V && V.duration; $('lecBar').innerHTML = ''; $('slideBar').innerHTML = ''; $('lecChips').innerHTML = ''; lastLec = undefined; $('lecChips')._on = -2;
  if (!MARKS || !isFinite(D) || !D) return;
  const L = MARKS.lectures;
  L.forEach((x, i) => {
    seg($('lecBar'), x[0], i + 1 < L.length ? L[i + 1][0] : D, 0, D, x[1], i);
    const k = x[1].indexOf(':'); chip($('lecChips'), x[0], k > 0 ? x[1].slice(0, k).trim() : x[1], k > 0 ? x[1].slice(k + 1).trim() : '', x[1]);
  });
  updateBars();
}
function setHead(bar, f) {
  let h = bar.querySelector('.head'); if (!h) { h = document.createElement('i'); h.className = 'head'; bar.appendChild(h); }
  h.style.left = (Math.min(1, Math.max(0, f)) * 100) + '%';
}
function updateBars() {
  const t = V.currentTime, D = V.duration;
  $('clock').textContent = fmt(t) + ' / ' + (isFinite(D) ? fmt(D) : '–');
  if (!MARKS || !isFinite(D) || !D) return;
  const L = MARKS.lectures, li = idxAt(L, t), lb = $('lecBar'), sb = $('slideBar'), lc = $('lecChips'), sc = $('slideChips');
  lb.querySelectorAll('.sg').forEach((d, i) => d.classList.toggle('on', i === li));
  if (setOn(lc, li)) showChip(lc, li, li - lc._prev === 1);     // glide when playback moves on to the next one; jump straight there after a seek
  const lec = li >= 0 ? L[li][2] : null;
  if (lec !== lastLec) {
    lastLec = lec; sb.innerHTML = ''; sc.innerHTML = ''; sc._on = -2; sc.scrollLeft = 0;
    const lo = li >= 0 ? L[li][0] : 0, hi = li + 1 < L.length ? L[li + 1][0] : D, S = MARKS.slides.filter(s => s[2] === lec);
    S.forEach((s, i) => { seg(sb, s[0], i + 1 < S.length ? S[i + 1][0] : hi, lo, hi, s[1], i); chip(sc, s[0], String(s[3] + 1), s[1], s[1]); });
    sb._lo = lo; sb._hi = hi; sb._S = S;
  }
  const S = sb._S || [], si = idxAt(S, t);
  sb.querySelectorAll('.sg').forEach((d, i) => d.classList.toggle('on', i === si));
  if (setOn(sc, si)) showChip(sc, si, si - sc._prev === 1);
  setHead(lb, t / D); setHead(sb, (t - sb._lo) / ((sb._hi - sb._lo) || 1));
  const c = $('curch'); c.innerHTML = '';
  if (li >= 0) { const b = document.createElement('b'); b.textContent = L[li][1]; c.appendChild(b); }
  if (si >= 0) c.appendChild(document.createTextNode('  ›  ' + S[si][1]));
}
function skip(n) { if (!V || !isFinite(V.duration)) return; V.currentTime = Math.min(V.duration - 0.5, Math.max(0, V.currentTime + n)); }
document.querySelectorAll('[data-skip]').forEach(b => b.onclick = () => skip(+b.dataset.skip));
$('playBtn').onclick = () => { if (!V) return; if (V.paused) resume(); else V.pause(); };

// where we are (lecture · slide), worked out in the page from the slide marks
let lastWhereT = -99;
function whereLabel(t) {
  if (!MARKS) return ''; const i = idxAt(MARKS.slides, t); if (i < 0) return '';
  const [, h, n, si] = MARKS.slides[i]; return `${CODES[n] || ''} · slide ${si + 1}: ${h}`;
}
function refreshWhere(force) {
  if (!V || (!force && Math.abs(V.currentTime - lastWhereT) < 2)) return;
  lastWhereT = V.currentTime; $('where').textContent = whereLabel(V.currentTime);
}

function add(cls, text, meta) {
  $('empty') && $('empty').remove();
  const d = document.createElement('div'); d.className = 'msg ' + cls;
  if (meta) { const m = document.createElement('div'); m.className = 'meta'; m.textContent = meta; d.appendChild(m); }
  const b = document.createElement('div'); b.className = 'body'; b.textContent = text; d.appendChild(b);
  LOG.appendChild(d); toBottom();
  if (PHONE.matches) requestAnimationFrame(() => d.scrollIntoView({ block: 'nearest', behavior: 'smooth' }));   // phones: the page scrolls, not the log
  return d;
}
const PHONE = matchMedia('(max-width: 900px), (max-height: 520px) and (pointer: coarse)');
function toBottom() { requestAnimationFrame(() => { LOG.scrollTop = LOG.scrollHeight; }); }
window.addEventListener('resize', toBottom);

function openAsk() { V && V.pause(); if (isFull()) exitFull(); QB.focus(); }

async function ask(question) {
  question = (question || QB.value).trim(); if (!question || answering) return;
  if (!V) { add('err', 'The narrator answers questions about the lecture video, which is not available yet.'); return; }
  stopAnswer(true);
  V.pause();
  const t = V.currentTime; QB.value = '';
  add('q', question, 'You · at ' + fmt(t));
  boardDismissed = false; hideBoard(); BLOCKS.clear();
  const a = add('a', '', 'Narrator'); const body = a.querySelector('.body');
  const dots = document.createElement('div'); dots.className = 'thinking'; dots.innerHTML = '<i></i><i></i><i></i>'; a.appendChild(dots);
  answering = true; $('askBtn').disabled = true; $('stopBtn').disabled = false; $('resumeBtn').classList.add('show');
  queue = []; played = 0;
  stats = { t, question, t0: performance.now(), firstText: null, firstAudio: null, clipsPlayed: 0, secondsSpoken: 0, pausedThroughout: true, error: null };
  let r;
  try {
    const resp = await fetch('/api/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' },
                                           body: JSON.stringify({ t: t * SCALE, question, history }) });
    r = await resp.json();
  } catch (e) { r = { error: 'Could not reach the narrator. Please try again in a moment.' }; }
  if (r.error) { a.className = 'msg err'; body.textContent = r.error; dots.remove(); finish(null); stats.error = r.error; return; }
  a.querySelector('.meta').textContent = 'Narrator · ' + r.where; stats.where = r.where;
  job = { id: r.job, el: a, body, dots, done: false, text: '' };
  const myJob = job; let misses = 0, seenN = 0, seenC = 0;
  while (job === myJob) {
    let s;
    try { const resp = await fetch(`/api/job/${myJob.id}?n=${seenN}&c=${seenC}`, { cache: 'no-store' }); s = await resp.json(); if (resp.status === 404) throw new Error(s.error); misses = 0;
          seenN = (s.clips || []).length; seenC = (s.text || '').length; }
    catch (e) { if (++misses > 40) { s = { error: 'Lost contact with the narrator. Please ask again.', done: true, clips: [] }; } else { await sleep(500); continue; } }
    if (job !== myJob) break;
    if (s.text && s.text !== myJob.text) { renderAnswer(body, s.text); myJob.text = s.text; if (stats.firstText === null) stats.firstText = (performance.now() - stats.t0) / 1000; toBottom(); }
    for (const c of s.clips || []) if (!queue.some(x => x.i === c.i)) { queue.push(c); }
    queue.sort((x, y) => x.i - y.i); pump();
    if (s.error) { a.className = 'msg err'; body.textContent = (s.text ? s.text + '\n\n' : '') + s.error; stats.error = s.error; }
    if (s.done) { myJob.done = true; dots.remove(); break; }
    await sleep(150);                                 // the server holds each request until something changes (long poll)
  }
  if (job === myJob) { history.push({ q: question, a: myJob.text }); history = history.slice(-3); waitSpeechEnd(myJob); }
}

let busy = false;          // a clip is loading or playing
function pump() {
  if (!job || busy) return;
  const next = queue.find(c => c.i === played);
  if (!next) return;
  busy = true; audio.src = next.url;
  audio.play().then(() => {
    if (!/AI \(Claude\)/.test($('hint').textContent)) $('hint').textContent = 'Answers are written by an AI (Claude) and can contain mistakes.';
    job && job.el.classList.add('speaking');
    if (stats && stats.firstAudio === null) stats.firstAudio = (performance.now() - stats.t0) / 1000;
  }).catch(e => { busy = false; if (e.name === 'NotAllowedError') $('hint').textContent = 'Click anywhere on the page once to allow the narrator to speak.'; });
}
// iPhone Safari only lets a page play sound from an audio element that was first started by a tap.
// Answers arrive seconds after the tap, so on the first tap we play a short silent clip to unlock the element.
const SILENT = (() => { const n = 400, b = new ArrayBuffer(44 + n * 2), v = new DataView(b), w = (o, s) => [...s].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
  w(0, 'RIFF'); v.setUint32(4, 36 + n * 2, true); w(8, 'WAVE'); w(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, 8000, true); v.setUint32(28, 16000, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); w(36, 'data'); v.setUint32(40, n * 2, true);
  return URL.createObjectURL(new Blob([b], { type: 'audio/wav' })); })();
let audioUnlocked = false;
function unlockAudio() {
  if (audioUnlocked || job) return; audioUnlocked = true;
  try { audio.src = SILENT; promise(audio.play()).catch(() => { audioUnlocked = false; }); } catch (e) { audioUnlocked = false; }
}
for (const ev of ['touchend', 'click', 'keydown']) document.addEventListener(ev, unlockAudio, { capture: true, passive: true });
const isSilent = () => audio.src === SILENT;
audio.addEventListener('ended', () => {
  if (isSilent()) return;
  busy = false; played++;
  if (stats) { stats.clipsPlayed++; stats.secondsSpoken += audio.duration || 0; if (V && !V.paused) stats.pausedThroughout = false; }
  job && job.el.classList.remove('speaking'); pump();
});
audio.addEventListener('error', () => { if (isSilent()) return; busy = false; played++; pump(); });
let lastAT = -1, stuck = 0;
setInterval(() => {
  if (!job || !busy || audio.ended || !audio.src) { stuck = 0; return; }
  if (audio.paused || audio.currentTime === lastAT) stuck++; else stuck = 0;
  lastAT = audio.currentTime;
  if (stuck >= 3) { stuck = 0; audio.play().catch(() => {}); if (stats) stats.nudges = (stats.nudges || 0) + 1; }
}, 500);
document.addEventListener('click', () => { if (job && !busy) pump(); });

async function waitSpeechEnd(myJob) {
  while (job === myJob && played < queue.length) await sleep(200);
  if (job !== myJob) return;
  finish(myJob);
  if ($('autoRes').checked) { await sleep(700); if (job === myJob) resume(); }
}
function finish(j) { answering = false; $('askBtn').disabled = false; $('stopBtn').disabled = true; if (stats) stats.done = (performance.now() - stats.t0) / 1000; }
function stopAnswer(silent) {
  if (job && !job.done) fetch('/api/cancel/' + job.id, { method: 'POST' }).catch(() => {});
  if (job) { job.el.classList.remove('speaking'); job.dots && job.dots.remove(); }
  audio.pause(); audio.removeAttribute('src'); busy = false; queue = []; played = 0;
  if (!silent) { job = null; finish(null); }
}
function resume() { stopAnswer(false); $('resumeBtn').classList.remove('show'); hideBoard(); V && V.play(); }

// ---------------- answers: spoken prose + fenced code blocks (code is displayed, never spoken)
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const KW = {
  c: 'auto break case char const continue default do double else enum extern float for goto if inline int long register return short signed sizeof static struct switch typedef union unsigned void volatile while bool true false NULL uint8_t uint16_t uint32_t int8_t int16_t int32_t size_t',
  cpp: 'alignas auto bool break case catch char class const constexpr continue default delete do double else enum explicit false float for friend if inline int long namespace new nullptr operator private protected public return short signed sizeof static struct switch template this throw true try typedef typename union unsigned using virtual void volatile while override final std string vector cout cin endl',
  python: 'and as assert break class continue def del elif else except False finally for from global if import in is lambda None nonlocal not or pass raise return True try while with yield print self',
  java: 'abstract boolean break byte case catch char class continue default do double else extends final float for if implements import int interface long new null package private protected public return short static super switch this throw throws try void while true false String',
  verilog: 'module endmodule input output inout wire reg logic always always_ff always_comb assign begin end if else case casez endcase default posedge negedge parameter localparam integer initial forever for generate endgenerate genvar function endfunction task endtask or and not',
  vhdl: 'library use entity is port in out inout end architecture of signal begin process if then elsif else case when others std_logic std_logic_vector unsigned signed integer downto to rising_edge falling_edge component map variable constant type and or not xor nand nor all work ieee',
  sql: 'select from where join inner left right outer on group by order having insert into values update set delete create table primary key foreign references as and or not null distinct count sum avg min max limit asc desc',
  asm: 'mov movs ldr str add adds sub subs mul cmp b bl bx beq bne bgt blt bge ble push pop and orr eor lsl lsr nop lw sw addi beq bne j jal jr slt li la',
  bash: 'if then else fi for do done while case esac echo cd ls export sudo git make'
};
const ALIAS = { 'c++': 'cpp', cc: 'cpp', h: 'c', py: 'python', sv: 'verilog', systemverilog: 'verilog', v: 'verilog', vhd: 'vhdl', mysql: 'sql',
                arm: 'asm', mips: 'asm', assembly: 'asm', sh: 'bash', shell: 'bash', powershell: 'bash', js: 'java', javascript: 'java' };
function hl(code, lang) {
  lang = ALIAS[lang] || lang; const kws = KW[lang]; if (!kws) return esc(code);
  const ci = lang === 'vhdl' || lang === 'sql' || lang === 'asm';
  const set = new Set(kws.split(' ').map(w => ci ? w.toLowerCase() : w));
  const cm = { python: '#[^\\n]*', bash: '#[^\\n]*', vhdl: '--[^\\n]*', sql: '--[^\\n]*', asm: '(?:;|@|//)[^\\n]*' }[lang] || '//[^\\n]*|/\\*[\\s\\S]*?\\*/';
  const pp = (lang === 'c' || lang === 'cpp') ? '|^[ \\t]*#[^\\n]*' : '';
  const re = new RegExp(`(${cm})|("(?:\\\\.|[^"\\\\\\n])*"|'(?:\\\\.|[^'\\\\\\n])*')${pp ? '|(' + pp.slice(1) + ')' : '|(\\b\\B)'}|(\\b(?:0x[0-9a-fA-F_]+|\\d+'[bhdo][0-9a-fA-FxXzZ_]+|\\d+(?:\\.\\d+)?)\\b)|([A-Za-z_]\\w*)`, 'gm');
  let out = '', i = 0, m;
  while ((m = re.exec(code))) {
    if (m.index === re.lastIndex) { re.lastIndex++; continue; }
    out += esc(code.slice(i, m.index)); i = re.lastIndex; const s = esc(m[0]);
    if (m[1]) out += `<span class="tk-c">${s}</span>`;
    else if (m[2]) out += `<span class="tk-s">${s}</span>`;
    else if (m[3]) out += `<span class="tk-p">${s}</span>`;
    else if (m[4]) out += `<span class="tk-n">${s}</span>`;
    else if (m[5]) { const w = ci ? m[5].toLowerCase() : m[5];
      out += set.has(w) ? `<span class="tk-k">${s}</span>` : (code[i] === '(' ? `<span class="tk-f">${s}</span>` : s); }
    else out += s;
  }
  return out + esc(code.slice(i));
}
function parseAnswer(text) {
  const parts = []; const re = /```([\w+#.-]*)[^\n]*\n?([\s\S]*?)(```|$)/g; let i = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > i) parts.push({ kind: 'text', s: text.slice(i, m.index) });
    parts.push({ kind: 'code', lang: (m[1] || 'text').toLowerCase(), s: m[2].replace(/\n+$/, ''), open: m[3] !== '```' });
    i = re.lastIndex; if (m[0] === '') break;
  }
  if (i < text.length) parts.push({ kind: 'text', s: text.slice(i) });
  return parts;
}
function drawing(p) {           // an SVG drawn by the narrator, shown as an <img> (no scripts can run)
  const d = document.createElement('div'); d.className = 'wbd';
  d.innerHTML = `<div class="cbh"><b>Whiteboard</b>${p.open ? '<span>drawing…</span>' : '<button>Enlarge</button>'}</div>`;
  if (p.open) { d.insertAdjacentHTML('beforeend', '<div class="pend">The narrator is drawing…</div>'); return d; }
  let svg = p.s.trim(); if (!/xmlns=/.test(svg)) svg = svg.replace(/<svg\b/, '<svg xmlns="http://www.w3.org/2000/svg"');
  const img = document.createElement('img'); img.alt = 'Whiteboard drawing'; img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  img.onerror = () => { img.replaceWith(Object.assign(document.createElement('div'), { className: 'pend', textContent: 'This drawing could not be displayed.' })); };
  d.appendChild(img);
  const en = d.querySelector('button'); if (en) en.onclick = () => showBoard(lastBoardText, true);
  return d;
}
const BLOCKS = new Map();
function codeBlock(p, big) {
  const key = (big ? 'B' : 'S') + (p.open ? 'o' : 'c') + p.lang + '\u0000' + p.s;
  if (!p.open && BLOCKS.has(key)) return BLOCKS.get(key);
  const d = makeBlock(p, big); if (!p.open) BLOCKS.set(key, d); return d;
}
function makeBlock(p, big) {
  if (p.lang === 'svg' || p.lang === 'xml' && /^\s*<svg/.test(p.s)) { const d = drawing(p); if (big) { const b = d.querySelector('button'); b && b.remove(); } return d; }
  const d = document.createElement('div'); d.className = 'cb';
  const body = big ? hl(p.s, p.lang).split('\n').map((l, k) => `<span class="ln">${k + 1}</span>${l}`).join('\n') : hl(p.s, p.lang);
  d.innerHTML = `<div class="cbh"><b>${esc(p.lang)}</b>${p.open ? '<span>writing…</span>' : ''}<button>Copy</button>${big ? '' : '<button>Enlarge</button>'}</div><pre><code>${body}</code></pre>`;
  const [cp, en] = d.querySelectorAll('button');
  cp.onclick = () => { navigator.clipboard.writeText(p.s).then(() => { cp.textContent = 'Copied'; setTimeout(() => cp.textContent = 'Copy', 1200); }).catch(() => {}); };
  if (en) en.onclick = () => showBoard(lastBoardText, true);
  return d;
}
let lastBoardText = '', boardDismissed = false;
function renderAnswer(el, text) {
  const parts = parseAnswer(text); el.innerHTML = ''; el.style.whiteSpace = 'normal';
  for (const p of parts) {
    if (p.kind === 'code') { el.appendChild(codeBlock(p, false)); continue; }
    for (const para of p.s.split(/\n{2,}/)) {
      if (!para.trim()) continue;
      const q = document.createElement('p');
      q.innerHTML = esc(para.trim()).replace(/`([^`\n]+)`/g, '<code class="in">$1</code>').replace(/\n/g, '<br>');
      el.appendChild(q);
    }
  }
  if (parts.some(p => p.kind === 'code')) { lastBoardText = text; if (!boardDismissed) showBoard(text, false); }
}
function showBoard(text, force) {
  if (force) boardDismissed = false;
  const b = $('boardBody'); const sc = b.scrollTop; b.innerHTML = '';
  const blocks = parseAnswer(text).filter(p => p.kind === 'code');
  const isDraw = p => p.lang === 'svg' || (p.lang === 'xml' && /^\s*<svg/.test(p.s));
  const code = blocks.filter(p => !isDraw(p)), draw = blocks.filter(isDraw);
  if (code.length && draw.length) {
    b.className = 'bb two'; const L = document.createElement('div'), R = document.createElement('div'); L.className = R.className = 'col';
    code.forEach(p => L.appendChild(codeBlock(p, true))); draw.forEach(p => R.appendChild(codeBlock(p, true))); b.append(L, R);
  } else { b.className = 'bb'; blocks.forEach(p => b.appendChild(codeBlock(p, true))); }
  b.scrollTop = sc; $('board').classList.add('show');
}
function hideBoard() { $('board').classList.remove('show'); }
$('boardHide').onclick = () => { boardDismissed = true; hideBoard(); };

$('askBtn').onclick = () => ask();
$('stopBtn').onclick = () => stopAnswer(false);
$('resumeBtn').onclick = resume;
QB.addEventListener('focus', () => V && V.pause());
QB.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(); } if (e.key === 'Escape') { QB.blur(); stopAnswer(false); } });
window.addEventListener('keydown', e => {
  if (!V || e.target === QB || e.target.tagName === 'SELECT' || e.target.tagName === 'INPUT' || e.ctrlKey || e.altKey || e.metaKey) return;
  if (document.querySelector('dialog[open]')) return;
  let handled = true;
  if (e.key === 'q' || e.key === 'Q' || e.key === '/') openAsk();
  else if (e.key === ' ') { if (V.paused) resume(); else V.pause(); }
  else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') skip((e.key === 'ArrowLeft' ? -1 : 1) * (e.shiftKey ? 30 : 10));
  else if (e.key === 'f' || e.key === 'F') toggleFull();
  else if (e.key === 'Escape') { if (document.body.classList.contains('pseudofs')) setPseudo(false); else if (!fsEl()) stopAnswer(false); handled = false; }
  else handled = false;
  if (handled) { e.preventDefault(); e.stopPropagation(); }
}, true);

// full screen = the video AND the narrator's board over it.
// Browsers that can't make an element full screen (iPhone Safari) get "fill the window" instead.
const SW = document.querySelector('.stagewrap');
const fsEl = () => document.fullscreenElement || document.webkitFullscreenElement || null;
function promise(x) { return x && x.then ? x : Promise.resolve(); }
function setPseudo(on) {
  document.body.classList.toggle('pseudofs', on); fsLabel();
  if (on) { window.scrollTo(0, 0); try { screen.orientation && screen.orientation.lock && screen.orientation.lock('landscape').catch(() => {}); } catch (e) {} }
}
function isFull() { return !!fsEl() || document.body.classList.contains('pseudofs'); }
function exitFull() {
  if (document.body.classList.contains('pseudofs')) setPseudo(false);
  if (fsEl()) promise((document.exitFullscreen || document.webkitExitFullscreen).call(document)).catch(() => {});
}
function toggleFull() {
  if (isFull()) return exitFull();
  if (NATIVE_FS) {
    try { promise((SW.requestFullscreen || SW.webkitRequestFullscreen).call(SW)).catch(() => setPseudo(true)); } catch (e) { setPseudo(true); }
  } else setPseudo(true);
}
function fsLabel() { $('fsBtn').textContent = $('fsOver').textContent = isFull() ? '✕ Exit full screen' : '⛶ Full screen'; }
$('fsBtn').onclick = toggleFull; $('fsOver').onclick = toggleFull;
for (const ev of ['fullscreenchange', 'webkitfullscreenchange']) document.addEventListener(ev, () => {
  const el = fsEl();
  if (el && el !== SW) promise((document.exitFullscreen || document.webkitExitFullscreen).call(document)).then(() => (SW.requestFullscreen || SW.webkitRequestFullscreen).call(SW)).catch(() => {});
  fsLabel();
});
{ let tm;
  SW.addEventListener('mousemove', () => { SW.classList.add('mousey'); clearTimeout(tm); tm = setTimeout(() => SW.classList.remove('mousey'), 2500); }); }

// ---------------- dialogs
$('slidesBtn').onclick = () => { V && V.pause && !V.paused && V.pause(); $('slidesDlg').showModal(); };
$('aboutBtn').onclick = () => $('aboutDlg').showModal();
document.querySelectorAll('dialog').forEach(d => {
  d.querySelector('[data-close]').onclick = () => d.close();
  d.addEventListener('click', e => { if (e.target === d) d.close(); });
});

// ---------------- resizable layout (remembered)
const SIZES = { chatw: [400, 260, () => window.innerWidth - 420], vidh: [null, 160, () => window.innerHeight - 260] };
function applySize(k, v) {
  const [def, lo, hi] = SIZES[k];
  if (v === null || v === undefined) { document.documentElement.style.removeProperty('--' + k); return; }
  v = Math.round(Math.min(hi(), Math.max(lo, v))); document.documentElement.style.setProperty('--' + k, v + 'px'); return v;
}
for (const k in SIZES) { const v = store.get('size:' + k, null); if (v !== null) applySize(k, v); }
function dragSize(el, k, axis, sign, current) {
  el.addEventListener('pointerdown', e => {
    e.preventDefault(); el.setPointerCapture(e.pointerId); el.classList.add('drag'); document.body.classList.add('dragging');
    const p0 = axis === 'x' ? e.clientX : e.clientY, v0 = current();
    const mv = ev => { const v = applySize(k, v0 + sign * ((axis === 'x' ? ev.clientX : ev.clientY) - p0)); store.set('size:' + k, v); };
    const up = () => { el.removeEventListener('pointermove', mv); el.removeEventListener('pointerup', up); el.removeEventListener('pointercancel', up);
                       el.classList.remove('drag'); document.body.classList.remove('dragging'); drawBars(); };
    el.addEventListener('pointermove', mv); el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
  });
  el.addEventListener('dblclick', () => { applySize(k, SIZES[k][0]); store.set('size:' + k, null); drawBars(); });
}
dragSize($('chatSplit'), 'chatw', 'x', -1, () => document.querySelector('aside').getBoundingClientRect().width);
dragSize($('vidSplit'), 'vidh', 'y', 1, () => $('screen').getBoundingClientRect().height);

// speech input (browser speech recognition)
$('micBtn').onclick = () => {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition; if (!SR) return;
  V && V.pause(); const rec = new SR(); rec.lang = 'en-US'; rec.interimResults = true;
  $('micBtn').classList.add('rec'); $('micBtn').textContent = '● Listening…';
  rec.onresult = e => { let s = ''; for (const r of e.results) s += r[0].transcript; QB.value = s; if (e.results[e.results.length - 1].isFinal) { rec.stop(); ask(s); } };
  rec.onend = () => { $('micBtn').classList.remove('rec'); $('micBtn').textContent = '🎤 Speak'; };
  rec.onerror = e => { $('hint').textContent = 'Microphone: ' + e.error; };
  rec.start();
};

// ---------------- self-test: drives the real UI through sample questions across the series.
// Cases come from the local server, or (live site) from the URL fragment #cases=<base64 JSON>, which never reaches a server.
// Results go to the local server's report endpoint when there is one, and always to window.__selftest for a debugger to read.
async function selftest() {
  const hc = new URLSearchParams(location.hash.slice(1)).get('cases');
  const cases = hc ? JSON.parse(decodeURIComponent(escape(atob(hc)))) : await (await fetch('/local/selftest_cases.json')).json(); const results = [];
  window.__selftest = { started: new Date().toISOString(), results, done: false };
  while (!MARKS) await sleep(200);
  for (const c of cases) {
    const r = { ...c };
    try {
      const s0 = performance.now();
      V.currentTime = c.T / SCALE; await new Promise(res => V.addEventListener('seeked', res, { once: true }));
      r.seekSeconds = +((performance.now() - s0) / 1000).toFixed(2);
      await V.play(); await sleep(1500);
      r.playedBeforeAsk = !V.paused && V.currentTime > c.T / SCALE;
      r.whereShown = $('where').textContent;
      const before = V.currentTime;
      await ask(c.q);
      const t0 = performance.now(); while (answering && performance.now() - t0 < 180000) await sleep(250);
      r.videoStayedPaused = V.paused && Math.abs(V.currentTime - before) < 0.05;
      Object.assign(r, { where: stats.where, answer: job ? job.text : '', firstText: stats.firstText, firstAudio: stats.firstAudio, done: stats.done,
                         clips: queue.length, clipsPlayed: stats.clipsPlayed, secondsSpoken: +stats.secondsSpoken.toFixed(1), error: stats.error,
                         audioNudges: stats.nudges || 0 });
      const p0 = V.currentTime; resume(); await sleep(2000);
      r.resumedOk = !V.paused && V.currentTime > p0 + 1;
    } catch (e) { r.error = String(e); }
    results.push(r);
  }
  window.__selftest.done = true;
  if (!hc) await fetch('/api/selftest-report', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ when: new Date().toISOString(), results }) });
  document.title = 'SELFTEST DONE';
}

init();
