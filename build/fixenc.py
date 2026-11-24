"""undo UTF-8 -> cp1252 -> UTF-8 double encoding (PowerShell Get-Content/Set-Content damage)"""
import sys
rev = {}
for b in range(0x80, 0xA0):
    try: rev[bytes([b]).decode('cp1252')] = b
    except UnicodeDecodeError: rev[chr(b)] = b
for f in sys.argv[1:]:
    raw = open(f, 'rb').read()
    s = raw.decode('utf-8-sig')
    if not any(m in s for m in ('â€', 'Â·', 'â†', 'Ã')):
        print('clean', f); continue
    out = bytearray()
    for ch in s:
        o = ord(ch)
        if ch in rev: out.append(rev[ch])
        elif o < 256: out.append(o)
        else: out += ch.encode('utf-8')
    fixed = out.decode('utf-8')
    open(f, 'w', encoding='utf-8', newline='').write(fixed)
    print('fixed', f)
