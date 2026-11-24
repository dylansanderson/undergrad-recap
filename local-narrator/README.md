# Ask the Narrator

Watch the lecture series and pause at any moment to ask the narrator a question. The answer is written by Claude, knows exactly which lecture and slide you're on and what was just said, and is spoken back in the narrator's voice (Kokoro af_heart).

## Start
Double-click **`Watch with Ask-the-Narrator.bat`** in the Coursework folder. A console window opens (keep it open; closing it stops the app) and the player opens in your browser at http://127.0.0.1:8765/.

## Use
| Key / button | What it does |
|---|---|
| **Q** (or `/`) | pause the lecture and jump to the question box |
| **Enter** | send the question (Shift+Enter for a new line) |
| 🎤 **Speak** | ask out loud instead of typing (browser speech recognition, Chrome/Edge) |
| **Space** | play/pause; after an answer, resumes the lecture |
| **Esc** / Stop answer | stop the narrator mid-answer |
| auto-resume | continue the lecture automatically when the answer finishes |

* The top-left menu switches between the **full series** (`Undergrad_Recap_Lectures.mp4`) and any **single course lecture**; "Jump to…" lists the lectures inside the full series.
* Follow-ups work: "explain that more simply", "give me another example" (the last 4 questions are remembered until you reload the page).
* Every question and answer is saved to `qa_log.jsonl` in this folder.
* The player remembers where you stopped in each video.

## How it works
1. `timeline.json` (written by the lecture build) maps every moment of every video to its lecture, slide, bullet points, code and narration.
2. When you ask, `narrator_server.py` builds a prompt from that (the current slide, what the narrator said on it and the previous slide, the lecture outline) plus your question and recent Q&A.
3. It runs the Claude Code CLI headless: `claude -p --model sonnet --tools ""` with a narrator system prompt. This uses your normal Claude login (no API key) and has **no tools**, so it can only write text.
4. The answer streams back; each finished sentence is voiced immediately with Kokoro (`tts.py`, same leveling/mastering as the lectures) while the next one is still being written, so speech starts within a few seconds.

Options: `python narrator_server.py --open --port 8765 --model sonnet` (`--model opus` for deeper answers, slower).

## Requirements
Python 3 with `kokoro-onnx`, `soundfile`, `numpy`; `ffmpeg`/`ffprobe` on PATH; Claude Code installed and signed in (`claude` on PATH). The voice model lives in `voice/`.

## Self-test
With the app running, open http://127.0.0.1:8765/?selftest=1. The page drives itself through the sample questions in `selftest_cases.json` at different points of the series. For each question it seeks, plays, asks, plays every spoken clip, then resumes. It writes `selftest_report.json` and sets the tab title to "SELFTEST DONE".

## Notes
* An MP4 file can't contain interactive features, so this player wraps the final video. The video itself is unchanged and still plays anywhere (or on YouTube) without Q&A.
* If the timeline and video ever get out of sync (after a rebuild), copy the new `Undergrad_Recap_Lectures_timeline.json` from the build over `timeline.json`.
