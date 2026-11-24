# Building the lecture videos

All commands are run from `build/` with `python -P -E`. You need ffmpeg on PATH, the voice model in `../voice/` (see `voice/README.md`), and the Windows fonts Segoe UI, Cambria and Consolas.

## How a lesson is written

Each course is one file, `lessons/LNN_code.py`, holding a `LESSON` dict (code, title, Coursework `folder`, `slides`) plus `fig_*` functions that draw diagrams. The slide types are:

| Type | Meaning |
|---|---|
| `title` | Title slide |
| `section` | Section divider |
| `b` | Bullets, with an optional image |
| `v` | Visual: an image, optionally with points |
| `ex` | Code example |
| `q` | One big statement |
| `wb` | Whiteboard worked example: handwritten math, typed code with its output, drawings, written step by step |

How slides are narrated and illustrated:

- `say` is either a string or a list of **beats**. Each beat is narrated separately, and bullets or whiteboard steps reveal one beat at a time.
- An image ref is either `fig:name`, which calls `fig_name()` in the lesson, or `a:assetkey`, which is a photo in `assets/`.
- Photos come from Wikimedia Commons through `commons.py`, which records the title, artist, license and URL in `assets/credits.json`. The credits are rendered at the end of the combined video and written to `Image_Credits.txt`.

More detail: `PLAN.md` covers the goals, course order and conventions, and `REVIEW_LOG.md` lists the review passes and what they fixed.

Helper libraries:

| File | Role |
|---|---|
| `build2.py` | Renders frames, synthesizes narration, cuts segments and muxes the videos |
| `board.py` | Whiteboard renderer: handwriting-style math (`m`), code (`k`), output (`o`), pen strokes |
| `figlib.py` | Diagram helpers: axes, circuits through schemdraw, logic gates, graphs |
| `tts.py` | Kokoro `af_heart` with the mastering chain and a pronunciation lexicon (IPA overrides for words like GPIO and MACRS) |
| `commons.py` | Wikimedia search and download with license capture |

## Edit, then review frames (fast, no audio)

```powershell
python -P -E build2.py --only L14 --frames     # renders frames/L14_*.png
python -P -E sheet.py L14 6                    # contact sheets -> review/L14_k.png
```

Look at the contact sheets and fix the lesson, repeating until it's right. Other checks that are worth running:

- `check_math.py`: the math in whiteboard steps is consistent
- `pron_scan.py`: words the TTS may mispronounce
- `verify_timing.py`: the timing still lines up

## Full build

```powershell
python -P -E build2.py --credits --out out\Undergrad_Recap_Lectures.mp4 --course-root out\courses
```

This writes:

- **`out\Undergrad_Recap_Lectures.mp4`**: the combined video, with chapters and soft subtitles
- **`out\...srt`**, **`_chapters.txt`**, **`_Image_Credits.txt`** and **`_timeline.json`**
- **`out\courses\<course folder>\Lecture - *.mp4`** and **`Slides - *.pdf`**: one per course

Narration is cached in `cache/`, keyed by voice, speed, TTS version and text. Only sentences you changed are re-synthesized. With the ~5 GB cache on disk a full rebuild takes tens of minutes; from scratch it takes many hours.

## Install into Coursework and update everything that depends on the video

```powershell
.\install_v5.ps1
```

This copies the combined video, subtitles, chapters, credits and per-course files into the Coursework folder, and the timeline into `Coursework\Ask-the-Narrator\timeline.json`.

Then keep the narrators in sync. The video and every timeline must match, or the narrator will describe the wrong slide.

```powershell
Copy-Item out\Undergrad_Recap_Lectures_timeline.json ..\web\server\timeline.json
Copy-Item out\Undergrad_Recap_Lectures_timeline.json ..\local-narrator\timeline.json
```

Finally:

1. Upload the new video to YouTube and put the new id in `web/site_config.json`.
2. Follow DEPLOY.md: run `build_site.py`, then `deploy_hosting.py preview`, then `deploy_hosting.py`, then `deploy_narrator.ps1`.
3. Commit.
