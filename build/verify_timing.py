"""Timeline vs real video: total length, and spot checks that each segment starts where the timeline says."""
import json, os, sys, subprocess, glob
HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
TL = json.load(open(os.path.join(HERE, 'out', 'Undergrad_Recap_Lectures_timeline.json'), encoding='utf-8'))
real = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                             os.path.join(HERE, 'out', 'Undergrad_Recap_Lectures.mp4')], capture_output=True, text=True).stdout)
print(f"timeline {TL['duration']:.3f} s   real video {real:.3f} s   difference {real - TL['duration']:+.3f} s")
# packet-level check: find the video keyframe nearest each sampled beat start (each segment starts with a keyframe)
B = TL['beats']
for i in [100, 500, 900, 1060, 1300, 1600]:
    t0 = B[i][0]
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-skip_frame', 'nokey', '-show_entries', 'frame=pts_time',
                        '-read_intervals', f'{t0 - 1.5}%{t0 + 1.5}', '-of', 'csv=p=0', os.path.join(HERE, 'out', 'Undergrad_Recap_Lectures.mp4')],
                       capture_output=True, text=True).stdout.split()
    ks = [float(x.strip(',')) for x in r if x.strip(',')]
    near = min(ks, key=lambda k: abs(k - t0)) if ks else None
    print(f'beat {i:5d} timeline start {t0:10.3f}  nearest keyframe {near}  off {None if near is None else round(near - t0, 3)}')
