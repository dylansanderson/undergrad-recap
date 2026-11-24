"""Compare encoded segment durations with planned beat durations (subtitle drift diagnosis)."""
import json, os, subprocess, glob, sys
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
TL = json.load(open(os.path.join(HERE, 'out', 'Undergrad_Recap_Lectures_timeline.json'), encoding='utf-8'))
B = TL['beats']
lists = sorted(glob.glob(os.path.join(HERE, 'out', 'list_*.txt')), key=lambda p: -os.path.getsize(p))
segs = [l.strip()[6:-1] for l in open(lists[0], encoding='utf-8') if l.startswith('file')]
print('segments in main list:', len(segs), 'beats:', len(B))
def dur(p, what='format=duration'):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', what, '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.split()[0])
tot = 0
for i in list(range(0, len(B), 160))[:10]:
    p = segs[i]; plan = B[i][1] - B[i][0]; real = dur(p)
    a = dur(p, 'stream=duration'); tot += real - plan
    print(f'{i:5d} plan {plan:7.3f} real {real:7.3f} diff {1000*(real-plan):6.1f} ms  {os.path.basename(p)[:12]}')
