# Legacy (first generation)

Kept for reference; nothing here is needed to build or run the current series.

- `v1-video/`: the first lecture pipeline (`build.py`, `lessons1-3.py`, `tts.py`). It produced a 64-minute single video with bullet slides and no whiteboard. `build2.py` in `build/` replaced it.
- `recap-pdf/`: the written course-by-course recap (`Undergrad_Recap.pdf` in Coursework). `extract.py` pulls text from the coursework files (`docs.txt` is the file inventory), `sums.py`/`summaries.txt` hold per-course summaries, `recap.md` and `part1-3.md` are the text, and `render.py` lays out the PDF with reportlab.
