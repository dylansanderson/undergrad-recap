# Undergrad Recap

A narrated re-teach of a CSUF Computer Engineering B.S. — 32 lectures (MATH, PHYS, CPSC, EGCP, EGEE), about 9 hours — plus **Ask the Narrator**, a player that lets you pause at any moment and ask a question about the slide you're on. Claude writes the answer, which is spoken in the lecture voice, with code and whiteboard drawings when they help.

- **Live site:** https://undergrad-recap.web.app
- **Video:** https://youtu.be/nkAxsz9Yh4Q (unlisted)

## Repository layout

| Folder | What it is | Docs |
|---|---|---|
| `build/` | The lecture generator: 32 lesson scripts (`lessons/LNN_*.py`), the renderer (`build2.py`), whiteboard/figure libraries, TTS (`tts.py`), and the image assets with their licenses | [docs/BUILD_VIDEOS.md](docs/BUILD_VIDEOS.md) |
| `web/` | The public website. `public/` holds the page, `server/` the Cloud Run narrator API, and the folder root holds the build/deploy/test scripts. | [docs/DEPLOY.md](docs/DEPLOY.md) |
| `local-narrator/` | The original offline version of Ask the Narrator. It plays the local MP4 and answers through the `claude` CLI, so it needs no API key or cloud. | [local-narrator/README.md](local-narrator/README.md) |
| `voice/` | Kokoro TTS model files. Not committed (340 MB); see [voice/README.md](voice/README.md). | |
| `notes/` | Source material: text extracted from the coursework (`corpus/`) and course catalog descriptions (`research/`) | |
| `legacy/` | The first-generation pipeline: the v1 64-minute video and the written PDF recap | |
| `docs/` | Architecture, deploy, build and operations guides | |

## Start here

- **How the pieces fit (GCP vs Firebase vs YouTube):** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Changing the website or narrator, previewing, going live, rolling back, taking the site down:** [docs/DEPLOY.md](docs/DEPLOY.md)
- **Editing a lecture and rebuilding the videos:** [docs/BUILD_VIDEOS.md](docs/BUILD_VIDEOS.md)
- **Costs, limits, budget kill switch, console links:** [docs/OPERATIONS.md](docs/OPERATIONS.md)

## What is not in git

Everything generated or large stays on disk only, as listed in `.gitignore`:

- **Rendered video**: `build/out`, `segs`, `frames`, `figs`.
- **The TTS audio cache** (`build/cache`, ~5 GB). With it a rebuild re-uses all narration; without it every sentence is re-synthesized, which takes hours.
- **The voice models.**
- **The slide PDFs copied into `web/public/slides/`.**

The finished deliverables (per-course `Lecture - *.mp4` and `Slides - *.pdf`, the combined video, its subtitles) live in the Coursework folder at `C:\Users\user\Desktop\school_notes_projects_etc\Coursework`. Several scripts take that path as a constant (`CW` / `$cw`).

## Requirements (Windows)

- Python 3.13. Run scripts as `python -P -E script.py`.
- ffmpeg on PATH: `winget install Gyan.FFmpeg`.
- `pip install --user pillow reportlab matplotlib schemdraw networkx kokoro-onnx soundfile numpy pymupdf`
- For deploying: the Google Cloud SDK (`gcloud`, installed at `%LOCALAPPDATA%\Google\Cloud SDK`) and a login with `gcloud auth login`. No Node or Firebase CLI is needed, because hosting deploys go through the REST API.
- For browser tests: Microsoft Edge (used headless).
