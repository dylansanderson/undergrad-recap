"""check that every whiteboard item's 'at' points at a real sentence of its step's narration"""
import sys, os, importlib, glob
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, 'lessons')]
import tts, board
bad = 0
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    mod = importlib.import_module(os.path.basename(f)[:-3])
    for s in mod.LESSON['slides']:
        if s.get('t') != 'wb': continue
        for k, st in enumerate(s['steps']):
            ns = len(tts.sentences(st['say']))
            for i, it in enumerate(st['w']):
                it = board.norm(it); at = it.get('at', i)
                if at >= ns:
                    bad += 1; print(f"{os.path.basename(f)[:3]} | {s['h'][:40]} | step {k} item {i} at={at} but only {ns} sentences")
print('problems:', bad)
