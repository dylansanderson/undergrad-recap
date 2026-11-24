import os, json, glob
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
for f in glob.glob(os.path.join(A, '﻿*')):
    nf = os.path.join(A, os.path.basename(f).lstrip('﻿')); os.replace(f, nf); print('renamed', nf)
cp = os.path.join(A, 'credits.json'); c = json.load(open(cp, encoding='utf-8'))
c2 = {k.lstrip('﻿'): v for k, v in c.items()}
for v in c2.values(): v['file'] = v['file'].lstrip('﻿')
json.dump(c2, open(cp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); print(len(c2), 'credits')
