# Notes / source material

- `corpus/` (**on disk only, not in git**): text extracted from each Coursework folder (assignments, notes, labs). The lessons and `recap.md` used it as "what this course actually covered". It is kept out of git because the raw text contains instructors' and classmates' names, emails and phone numbers. To regenerate it, run `python -P -E legacy/recap-pdf/extract.py "C:\Users\user\Desktop\school_notes_projects_etc\Coursework" notes/corpus` (needs `pip install pypdf python-docx python-pptx`).
- `research/`: CSUF catalog text (`bsms.txt` holds the B.S. requirements and course descriptions; `cpsc.txt` the CPSC course list). It was used to pick the courses and match lesson content to the catalog descriptions.
