import fitz, sys
d = fitz.open(sys.argv[1])
for p in [int(x) for x in sys.argv[3].split(',')]:
    d[p-1].get_pixmap(dpi=80).save(f"{sys.argv[2]}\\pg{p}.png")
missing = set()
for pg in d:
    for ch in pg.get_text():
        pass
print('ok', len(d))
