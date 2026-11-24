# Lecture series v2 — progress tracker (read this after any context compaction)

## User goals (2026-11-17)
- Detailed RE-TEACH of the whole CSUF Computer Engineering B.S. (finished 2021). No GE courses.
- One well-made narrated video + slide deck PER COURSE (saved in each course folder) + one combined video in Coursework root.
- Courses with no folder (user took notes on paper) → create folder "CODE-NUM Title" like existing ones.
- Teach like a professor: real-world context (who uses it, why), diagrams/images on every slide, worked examples, assume the learner retained nothing. "YouTube-worthy"; longer and more detailed than v1 (v1 = 64 min).
- Audio bug in v1: first word of sentences loud/crackly → fixed in v2/tts.py (per-sentence synth, trim, fades, compressor, loudnorm, no limiter). Voice: Kokoro af_heart (user choice).
- Narration addresses general learners (no personal info, no instructor names, no other students' work). Mention "in this course's labs, students build X" where the user's labs are known (recap.md "What you actually did").

## Tools
- v2/build2.py (engine), v2/figlib.py (diagram helpers), v2/tts.py, v2/commons.py (Wikimedia search/get with credits → assets/credits.json)
- Run python as: python -P -E script.py
- Lesson files: v2/lessons/LNN_code.py with LESSON dict + fig_* functions(path,w,h).
- Slide types: title | section | b (bullets, optional img) | v (visual; img + optional pts) | ex (code; optional img; cl=lines per beat) | q (big statement)
  - say: str or list of beats; pts reveal one per beat (extra beats at start show none); img may be list per beat
  - img refs: 'fig:name' (fig_name in module) or 'a:assetkey'
- Course facts: research/bsms.txt (catalog descriptions lines 450-600), recap.md (per-course what-you-did)

## Course order (curriculum order) and status
| # | file | folder | status |
|---|------|--------|--------|
| 00 | L00_welcome | (root) | todo |
| 01 | L01_math150a | MATH-150A Calculus I (new) | written+frames reviewed |
| 02 | L02_math150b | MATH-150B Calculus II (new) | written+frames reviewed |
| 03 | L03_cpsc120 | CPSC-120 Intro to Programming (new) | written+frames reviewed |
| 04 | L04_cpsc121 | CPSC-121 Object-Oriented Programming (new) | written+frames reviewed |
| 05 | L05_phys225 | PHYS-225 Mechanics (new) | written+frames reviewed |
| 06 | L06_math170a | MATH-170A Mathematical Structures (new) | written+frames reviewed |
| 07 | L07_egcp180 | EGCP-180 Digital Logic (new) | written+frames reviewed |
| 08 | L08_math250a | MATH-250A Calculus III (new) | written+frames reviewed |
| 09 | L09_math250b | MATH-250B Differential Equations & Linear Algebra | written+frames reviewed |
| 10 | L10_phys226 | PHYS-226 Electricity & Magnetism | written+frames reviewed |
| 11 | L11_phys227 | PHYS-227 Physics | written+frames reviewed |
| 12 | L12_cpsc131 | CPSC-131 Data Structures (new) | written+frames reviewed |
| 13 | L13_egcp280 | EGCP-280 Microcontrollers (new) | written+frames reviewed |
| 14 | L14_egcp281 | EGCP-281 Digital Logic Design (VHDL) | written+frames reviewed; pilot audio build out/pilot_L14.mp4 |
| 15 | L15_egee203 | EGEE-203 Electric Circuits | written+frames reviewed |
| 16 | L16_egee303 | EGEE-303 Electronics | written+frames reviewed |
| 17 | L17_egee303l | EGEE-303L Electronics Lab | written+frames reviewed |
| 18 | L18_egee323 | EGEE-323 Probability & Random Variables | written+frames reviewed |
| 19 | L19_egcp371 | EGCP-371 Signals & Systems | written+frames reviewed |
| 20 | L20_egcp381 | EGCP-381 Computer Architecture (VHDL Processor) | written+frames reviewed |
| 21 | L21_cpsc351 | CPSC-351 Operating Systems | written+frames reviewed |
| 22 | L22_cpsc362 | CPSC-362 Software Engineering | written+frames reviewed |
| 23 | L23_cpsc332 | CPSC-332 Database Systems | written+frames reviewed |
| 24 | L24_egee401 | EGEE-401 Engineering Economics | written+frames reviewed |
| 25 | L25_egcp441 | EGCP-441 Advanced Electronics (CMOS) | written+frames reviewed |
| 26 | L26_egcp446 | EGCP-446 Advanced Digital Design (Verilog) | written+frames reviewed |
| 27 | L27_egcp450 | EGCP-450 Embedded Systems (MSP432 ARM) | written+frames reviewed |
| 28 | L28_egcp447 | EGCP-447 Cyber-Physical Systems Security | written+frames reviewed |
| 29 | L29_egcp470 | EGCP-470 Senior Design I | written+frames reviewed |
| 30 | L30_egcp471 | EGCP-471 Senior Design II (Object Detection) | written+frames reviewed |
| 31 | L31_bigpicture | (root) | todo |

## Outputs (final)
- each course folder: "Lecture - <CODE> <Title>.mp4" + ".srt" + "Slides - <CODE> <Title>.pdf"
- root: Undergrad_Recap_Lectures.mp4 (all, chapters) + _chapters.txt (YouTube) + Image_Credits.txt
- Remove old v1 video? -> replace root video with v2 when done.

## Workflow per lesson
1. images: write img_<code>.txt (key | File:Title) → python commons.py getmany img_x.txt  (thumb host; standard sizes)
2. write lessons/LNN_x.py (figs + LESSON)  3. python build2.py --only LNN --frames ; python sheet.py LNN 6 → view review/*.png, fix
4. final full build at the end (audio cached by text hash).
- NEVER use PowerShell Get-Content/Set-Content on UTF-8 files (mojibake). Use Python or Edit tool. fixenc.py repairs.
- canvas(w,h,need=N,exact=True): fixed ref width 900 (side) / 1400 (full); mathtext: no \displaystyle, \left/\right brackets.
- 'a:k1+k2' = side-by-side photos; 'a:key|x0,y0,x1,y1' = crop fractions.

## Status 2026-11-18 (whiteboards): 41 'wb' worked-example slides added to L01 L02 L05 L06 L08 L09 L10 L11
- board.py: slide type 'wb' (steps = beats; items written/drawn when sentence 'at' starts; handwriting font Ink Free,
  mathtext with \dfrac, xkcd-style drawings via draw_<name>(ax, n, w, h); auto column flow). board.insert(LESSON, heading, slide).
- build2.py seg_wb: left-to-right wipe of each new item, timed from sentence marks. Tools: check_math.py, wbsheet.py, wipe_check.py.
- mathtext gotchas: no \lor/\land (use \vee/\wedge), no \pmod/\bmod, no matrices (use \genfrac{[}{]}{0}{0}{a\quad b}{c\quad d}), avoid ' inside r'...'.
- User may want the same for other courses later (offered: EGEE 323, EGEE 203, EGCP 371 ...).

## Status 2026-11-18 (later): audio v5 + Ask-the-Narrator DONE.
- Audio v5 (cache key 'v5'): envelope onset leveler + static-gain master (no compressor/dynamic loudnorm) + alimiter level=0. verify_v5.py --p90: first word >1 dB louder than rest: v4 38% -> v5 1%.
- Ask-the-Narrator app in Coursework\Ask-the-Narrator (narrator_server.py, player.html, tts.py, voice/, timeline.json from build). Launcher: Coursework\Watch with Ask-the-Narrator.bat.
- Build now writes out\Undergrad_Recap_Lectures_timeline.json; install_v5.ps1 copies everything (course files staged in out\courses).
- Tests: api_test.py (lookup/range/vtt/ask), run_selftest.ps1 (headless Edge drives the real UI, 10/10 pass), show_report.py.

## Status 2026-11-18: DONE. Final build installed (379 min, 32 lectures + 32 PDFs + srt, root combined video, chapters, Image_Credits.txt).
Rebuild: python build2.py --credits --out out\Undergrad_Recap_Lectures.mp4 --course-root <Coursework>

## Status 2026-11-17 (end of session)
- ALL lessons L00–L31 written + frames reviewed (L00/L31 last fixes applied; re-check review/L00_chk.png).
- Audio: batch1 done (out/batch1.mp4, L01-07+L14, 128 min). batch2 (L08-L27) running in background → out/batch2.log.
- TODO: narrate L28-L31 + L00; build2.py: slide-deck PDF export, Image_Credits.txt + credits slide,
  per-course outputs into course folders (create "(new)" folders), final combined video to root; final review.

## Status 2026-11-18 (late): whiteboard worked examples in ALL technical courses
- board.py: 'm' handwriting/math, 'k' code (syntax colour, 'plain' monospace), 'o' terminal output,
  drawings via draw_<name>; B.circuit (schemdraw, real-extent fit + label refit), B.mos (hand-drawn MOSFET),
  B.wave, B.table, B.node, B.selfloop. '$' in code is escaped automatically.
- wb slides added to L03 L04 L07 L12-L30 (math/physics ones from earlier). Numbers verified in wb_numbers*.py.
- Review: python wbsheet.py LNN -> review/wb_LNN_*.png
- Full rebuild log: out\build_wb3.log (killed by low memory at the very end) + out\build_wb4.log (cached finish, OK)
- INSTALLED 2026-11-18 ~8 PM: combined video 489 min; 32 lectures + pdf + srt; timeline.json.
  wb_qa_test.py 9/9 sensible answers; run_selftest.ps1 10/10 PASS (gen_cases.py <timeline> <out> needs 2 args).
- Ask-the-Narrator CODE ANSWERS (user request): answers may contain ```lang fenced blocks = SHOWN not spoken.
  narrator_server.py SpeechFilter strips fences from the TTS stream (test_filter.py); speakable() turns a_b -> "a b", std:: -> "standard".
  player.html renders highlighted code (cpp c python java verilog vhdl asm sql bash text) + big numbered "board" overlay over the video,
  Copy/Enlarge/Hide. code_qa_test.py <port>; gen_render_test.py -> review/render_test.html (screenshot w/ headless Edge).
  run_selftest.ps1 -Port N. Self-test 11/11 incl. CPSC 121 hello-world case.
- THREE CHANNELS (user): voice always + code (```lang) + whiteboard drawings (```svg, shown as <img> on a white panel);
  model chooses per question. Board overlay puts code left / drawing right. code_qa_test.py <port> [mix|old].
- Server: exclusive port bind (Windows SO_REUSEADDR let stale copies keep answering!), /api/version, POST /api/shutdown
  (header X-Narrator: takeover) -> a new launch replaces an old copy automatically. Stop test servers via that API, not kill.
- 2026-11-18 night: SUBTITLE DRIFT fixed: build2 times everything from REAL encoded segment lengths (real_dur, cache/segdur.json);
  verify_timing.py: timeline == video within 0.023 s everywhere (was ~5 s ahead by 4:26, ~10 s at end).
  PRONUNCIATION: tts.py LEX_I/LEX_C dictionary (IPA) -> whole-sentence phonemize with stand-in 'xylophone' then swap;
  audio cache key adds lex signature only for sentences using it. pron_scan.py / pron_caps.py list words + phonemes.
  PLAYER: ±10/30 s buttons + arrows, lecture bar + slide bar (/api/marks), ?v=&t= deep links. cdp_shot.ps1 = DevTools screenshot.
  board.circuit closes schemdraw's spare pyplot figures (memory leak; likely caused the low-memory kill).
- 2026-11-18/19 PEN (teacher's marker) on whiteboards: item {'p': marks, 'at', 'c', 'keep', 'solo', 'on': text, 'to', 'cols', 'line'}.
  Marks: circle box underline strike highlight arrow cross check, 'row' (table row), 'span' (box/column across lines 'on'->'to'),
  'link' (arrow between two lines), 'circle@k' (k-th schemdraw circuit's coords). Drawings name points with B.anchor; B.table
  names cells r<i>c<j>. B.pen(LESSON, heading, step, items...) inserts by sentence. Pen marks clear at the next step ('keep' to
  persist; 'solo' wipes earlier marks of the step first). build2.seg_wb animates pen strokes along the path.
  Review: python pensheet.py LNN [heading...] -> review/pen_LNN_k.png. Pen blocks added to L01 L03 L04 L07 L12-L23 L25-L28 L30.
  Math/physics besides L01 not yet penned.
- CLIP slide type {'t':'clip','clip': file in assets/clips,'crop':(w,h,x,y),'ss','still','pts','cap'}: real footage plays muted in a
  panel. L30 'The real detector, running live' uses the user's own recording (cropped to the detector window only).
  User has a 2nd video (unlisted YouTube, servo-failure backup demo): needs the file (YouTube Studio download); check for teammates.
- 'at' past sentence count is clamped to last sentence (build2 seg_wb); check_at.py lists them.

## Notes / decisions
- "Data side projects" chapter from v1 dropped (not a class).
- EGCP 451 RTOS is in the current catalog but user did not take it (no folder) → skip, mention.
