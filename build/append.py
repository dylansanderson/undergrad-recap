"""Append a pen block file to a lesson (replacing any earlier copy of the same block): python append.py <lesson.py> <block.py>"""
import sys, io
f, b = sys.argv[1], sys.argv[2]
blk = io.open(b, encoding='utf-8-sig').read().strip('\n')
t = io.open(f, encoding='utf-8').read()
head = blk.split('\n', 1)[0]
if head in t: t = t[:t.index(head)].rstrip('\n') + '\n'
io.open(f, 'w', encoding='utf-8', newline='').write(t.rstrip('\n') + '\n\n' + blk + '\n')
print('appended', len(blk.splitlines()), 'lines')
