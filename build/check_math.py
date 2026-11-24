"""try to render every whiteboard line of the given lessons; report the ones mathtext can't parse"""
import os, sys, glob, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import board, matplotlib.pyplot as plt
for code in sys.argv[1:]:
    f = glob.glob(os.path.join(HERE, 'lessons', code + '_*.py'))[0]; n = os.path.splitext(os.path.basename(f))[0]
    sp = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    bad = 0
    with plt.rc_context(board.RC):
        for s in m.LESSON['slides']:
            if s['t'] != 'wb': continue
            for e in board.events(s):
                if 'm' not in e['it']: continue
                fig = plt.figure(); t = fig.text(0, 0, e['it']['m'])
                try: t.get_window_extent(fig.canvas.get_renderer())
                except Exception as ex: bad += 1; print(code, '|', s['h'][:40], '|', e['it']['m'], '\n   ', str(ex).strip().splitlines()[-1][:160])
                plt.close(fig)
    print(code, 'bad lines:', bad)
