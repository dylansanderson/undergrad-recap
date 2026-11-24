# Student-panel engagement review (started 2026-11-19)

User request: watch every lecture as a few first-time students; find parts that could be clearer, need more examples,
and above all where the narrator should use the pen / whiteboard / on-screen code instead of only talking over a static slide.
Model to follow: the pen marks at 58:33 (pass by value vs reference: circle + check).

Panel: Maya (no programming/EE background), Jordan (some Python, transfer student), Priya (visual learner, reviews by rewatching).

## Tools (v2/)
- watch.py L03 -> slide-by-slide screen content + numbered narration sentences ('at' indexes)
- build2.py --only L03 --frames -> frames/*.png with finished pen marks; *.fig.json = figure rect
- figgrid.py L03_cpsc120 4 6 ... -> review/figgrid_*.png (fraction grid on figures; READ THE GRID LABELS, tiles are stacked)
- spensheet.py L03_cpsc120 [--all] -> review/spen_*.png contact sheets of pen-marked ordinary slides
- penframes.py <video> <timeline> "<heading>" <beat> [fps] -> animation frames
- engage_stats.py -> static vs whiteboard beats per lesson
- B.spen(LESSON, heading, beat, {'on': text | 'fig': [...], 'p': kind, 'at': sentence, 'dt': secs, 'c': colour, 'n': occurrence, 'keep', 'solo'})

## Baseline
1621 beats; 1130 static-slide beats (70%) had no pen at all; 449 whiteboard beats.

## Progress
- [x] engine: pen on ordinary slides (build2: REC recording, find_on, spen_strokes, draw_strokes, seg_spen, anim_encode shared w/ whiteboard)
- [x] L03 CPSC 120: ~60 marks on 14 static slides; vowel trace circles each vowel as spoken (line changed to 'k' so cols work)
- [x] L04 CPSC 121: code walk-throughs (BankAccount, files, Fraction), UML, stack/heap, polymorphism results, TDD cycle
- [x] L07 EGCP 180: place values, Gray 3->4, CMOS on/off, each gate named, boolean steps, minterm row, blocks, SR latch, counter waves, CPU parts
- [x] L12 CPSC 131: big-O legend, binary search middle per step, fib(3) repeats, hash collision, BST path, heap index, Dijkstra, table row-by-row (solo highlight)
- [x] L13 EGCP 280: MCU blocks, registers SP/LR/PC, memory map, sum_array line by line, stack frame, bit masks, ISR, PWM avg, ADC step, UART frame
- [x] L14 EGCP 281: all 9 code slides line-by-line; mindset shift boxes/gates; FA sum column; glitch; overflow; std_logic rows; timing path bars; FSM states
- FIGURE CLIPPING (student-visible defects) found with clipcheck.py + figsheet.py, fixed in source:
  L14 wheel (text cut), L14 fa_gates (cout), L18 bayes, L22 usecase, L11 tir, L20 pipeline, L12 heap/merge, L28 hamming, L23 normal, L30 cascade, L16 doping
  -> re-run clipcheck after a full --frames run to confirm
- [x] L15 EGEE 203: divider/KCL/KVL, nodal steps, Thevenin steps, op-amp rules, RC curve, impedance rows, power triangle, 3-phase sum, Lissajous
  + figure fixes: divider (R2 label sat on source), thev1 ('load?' over '12 kΩ'); 'Voltage, current, power' reveal:False
- [x] L16 EGEE 303: doping/depletion, diode regions, load line Q, ripple, MOSFET parts/channel/regions, MCU driver, CE bias/gain, gm tangent, Bode corners, GBW
  + fig fix: mos_iv 'saturation' label overlapped legend
- [x] L17 EGEE 303L: meter loading points, scope ground short, Zener/R_s, clipper/clamper, switch design, curves, mirror, beta bias bars, report
- [x] L18 EGEE 323: dice 7 bar, Bayes tree counts, reliability chains, binomial bars, PDF/CDF, 68-95-99.7, CLT panels, MTTF points, rho clouds, conv triangle, BER curves
- [x] L19 EGCP 371: signal blocks, LTI box/eqn, convolution overlap, Gibbs spikes, spectrum peaks, AM shift arrows, alias samples, s-plane poles, Bode corner, z-plane, FIR/IIR
- WORKFLOW per lesson (fast): watch.py Lxx --static ; build2.py --only Lxx --frames ; figgrid.py <name> <si[:beat]>... ; append B.spen block ;
  re-render ; spensheet.py <name> ; read sheets, fix misplaced coords (typical misses: y of underlines on figure text, peaks/poles off by ~.05)
- [x] L20 EGCP 381 (+ fig fixes isa top caption, hierarchy SSD row)  - [x] L21 CPSC 351
- AUTO pen (fixes.AUTO / auto_pen): every bullet slide without hand marks underlines each bullet's key phrase on its best-matching sentence.
  Applied to L00 L01 L02 L05 L06 L08-L11 L22-L31. All 1621 frames render clean (full --frames 2026-11-19).
  Result: 911 of 1130 static beats now have pen marks (was 0); 1479 marks total.
- NEXT (if wanted): hand-placed FIGURE marks for L01 L02 L05 L06 L08-L11 L22-L31 (auto only marks bullet text)
- AFTER ALL: full --frames run -> clipcheck.py (confirm clipping fixes) ; reveal_check.py ; full build ; install_v5.ps1 ; verify_timing.py ; selftest ; spot-check penframes
- REVEAL MISMATCH (bullet narrated before it appears): reveal_check.py flagged 26, ~19 real -> fixes.py REVEAL list sets s['rv']
  (build2.render honours s['rv']). L05 ramp slide left out on purpose: check its narration when doing L05 (answer would show early)
- engine fix: figure marks drop when the slide's image changes between beats (spen_plan)
- [x] 2026-11-20: full build (68.6 min) installed; verify_timing +0.023 s; selftest 11/11 pass (port 8778, shut down, cleaned);
  penframes spot-check OK (binary search circle+box, pass-by-value circles+check)
- [x] 2026-11-20 FIGURE MARKS for every AUTO lesson (L00 L01 L02 L05 L06 L08-L11 L22-L31): pen_blocks/Lxx.py appended via append.py
  (re-running append.py replaces the block). fixes.apply keeps auto bullet underlines when hand marks don't touch bullets.
  figtodo.py lists what's left (18 slides, nearly all photos). pen_cover.py: 954/1129 static beats, 2424 marks, 1356 figure marks.
  Figure fixes: L02 disk/harmonic, L05 vectors/projectile/collision/analog, L06 passwords, L08 double, L09 slope/basis,
  L10 lorentz/faraday, L11 levels/doppler, L22 waterfall/testpyramid/mvc, L24 cashflow, L27 led. Narration fix: L01 secant h=2 slope (was 10, is 8).
  Tools: repl.py <file> pairs.py (exact replace), append.py <lesson> <block>.
  Built (45.0 min), installed, timing +0.023 s, selftest 11/11 (port 8779, shut down, cleaned), penframes checked (SQL, sin/cos).
- watch out: bullets reveal per beat; a mark can only target text already shown (KeyError lists visible lines)

# ITERATION 3 (2026-11-21): emeritus-professor pass — confusion points, missing steps, more boards/pen
User request: watch every lecture in full as a seasoned professor; find every unclear slide / common student question
(external textbook-style FAQs), re-explain with whiteboards + pen; then verify and validate.
- Backup of all lessons BEFORE this pass: lessons_backup_iter3\  (restore a lesson from here if a block goes wrong)
- Transcripts: prof\LNN.txt (before) and prof\LNN_new.txt (after)   [watch.py]
- Per lesson: prof_blocks\LNN.py (new wb slides + pens; header '# ---------------- professor pass (iteration 3)...',
  appended via append.py, re-append replaces it) and prof_blocks\LNN_pairs.py (narration edits; repl.py is now IDEMPOTENT:
  skips a pair whose new text is already present — earlier it re-applied prefix pairs and duplicated narration!)
- One command: .\prof_apply.ps1 LNN  (pairs, append, --frames, prof_sheet.py -> review\prof_LNN_k.png, watch -> prof\LNN_new.txt)
- RULES learned: '→' inside a line that contains $math$ renders as ¤ -> use $\to$ there (plain lines are fine);
  no \left( \right); boxed line after code needs 'gap': 18; append narration at the END of a beat when the slide has pen
  'at' marks after that sentence (or shift the marks' 'at' in the pairs file, as done in L01 related rates).
- Inserting sentences changes TTS for that beat only (cache by sentence text).
Progress:
- [x] L00 (no change needed)  [x] L01 limits DNE, notation, product/quotient, +C; RR implicit, endpoints, f'=0≠extremum, Riemann right-edge
- [x] L02 technique checklist, sequences vs series + ratio test L=1 trap, Taylor formula & factorials; partial-fraction caveats
- [x] L03 '=' is not algebra (+=, ++, uninitialized), return vs print
- [x] L04 & and * two meanings + dot/arrow, forget virtual (+virtual dtor); '::' narration
- [x] L05 missing-variable trick + sign convention, 3rd-law pairs (FBD drawing), static/kinetic friction, elastic/inelastic
- [x] L06 perm vs comb decision + 3-formula table; induction 'circular?' worry; RSA phi & modular inverse; inverse vs converse
- [x] L07 TWO'S COMPLEMENT board (was promised by L03 but missing!); A+A'B=A+B why; K-map overlap + don't cares ('cfs' = code font size)
- [x] L08 nabla three ways (grad/div/curl computed, field drawings); line integral on two paths (conservative); non-rect limits
- [x] L09 integrating factor (RC charging), matrix multiplication row×column + AB≠BA, complex roots y''+2y'+26y (ringing graph)
- [x] L10 force/field/U/V look-alikes (+gravity analogy, V is a difference); Gauss's law worked (sphere drawing); RHR electron flip
- [x] L11 decibels 10 vs 20 rule, −3 dB = filter cutoff
- [x] L12 reading big-O off code (single/nested/halving/combined); hash worst case narration
- [x] L13 memory-mapped I/O C line decoded (cols are [a,b) char indexes)
- [x] L14 VHDL numbers: std_logic_vector vs unsigned vs signed, numeric_std, conversions, '1' vs "0101"
- [x] L15 RC circuit with phasors (rect/polar arithmetic + phasor diagram); capacitor series/parallel trap narration
- [x] L16 MOSFET region checklist + MOSFET/BJT "saturation" naming trap; gm·RC bypassed-gain narration
- [x] L17 Zener resistor sizing, two worst cases
- [x] L18 mean & variance by hand (die, uniform), pdf can exceed 1
- [x] L19 Laplace solve start to finish (RC step); omega vs f / 2π narration
- [x] L20 Amdahl formula spelled out (moved "1.56×" box mark to sentence 2); back-refs fixed: L02 'bell curve you'll meet in
      probability', L20 'Amdahl ... you'll meet again in OS', L26 'max frequency from the VHDL course' (forward refs were phrased as past)
- [x] L21 lost update traced step by step + mutex fix
- [x] L22 velocity, critical path (draw cpm), risk exposure
- [x] L23 transaction + write-ahead log, crash before/after COMMIT; COUNT(*) vs COUNT(col)/AVG with NULLs narration
- [x] L24 present worth factor by factor; real vs market rate narration
- [x] L25 AOI gate Y=!(AB+C), pull-down/pull-up duality (draw aoi)
- [x] L26 latch inference + default assignment; timing report / slack (draw slack). NOTE: '\n' inside a code item does NOT
      break lines — use one 'k' item per line
- [x] L27 UART frame & 115200 baud (draw uartframe), divisor error; "quantization from probability" wording fixed
- [x] L28 correlation power analysis on a toy 4-bit chip
- [x] L29 decision-matrix sensitivity check narration
- [x] L30 P-only steady-state error vs integral (code trace); servo example no longer contradicts IK angles
- [x] L31 (no change needed)
- [x] 2026-11-22 VALIDATION: full --frames 1780/1780 ok (only pre-existing L02 'from 1 to e' 8px warning); clipcheck flags
      only pre-existing figures (table edges = false positives); check_at: 19 new-board items at=ns (engine clamps to last
      sentence = intended); full build OK (video 540 min, was 489), installed; verify_timing +0.023 s everywhere;
      selftest 11/11 (port 8780; needs gen_cases.py <timeline> <app>\selftest_cases.json first!; server shut down, files cleaned);
      penframes checked L28 CPA cross, L16 saturation box. Full build takes ~2.5 h when most lessons change (progress bar).
- board helpers: B.ln(ax, xs_list, ys_list, c, lw); B.rect(ax, x, y, w, h, fc=, c=, lw=) — positional args differ from arr!
