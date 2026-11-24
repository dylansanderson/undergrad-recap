"""Wikimedia Commons helper: search for freely licensed images and download them with attribution.
usage:
  python commons.py search "query words" [n]
  python commons.py get "File:Name.jpg" key        -> assets/key.<ext> + credits.json entry
"""
import sys, os, json, re, urllib.request, urllib.parse, html
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets'); os.makedirs(ASSETS, exist_ok=True)
CRED = os.path.join(ASSETS, 'credits.json')
UA = {'User-Agent': 'CourseLectureVideoBuilder/1.0 (educational slides; python-urllib)'}
API = 'https://commons.wikimedia.org/w/api.php'
OK = re.compile(r'^(public domain|pd|cc0|cc[- ]by(-sa)?([- ]\d\.\d)?|cc by(-sa)? \d\.\d.*)', re.I)

import time
def fetch(url, binary=False, tries=6):
    delay = 5
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read() if binary else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and k < tries - 1:
                ra = e.headers.get('Retry-After')
                wait = int(ra) if ra and ra.isdigit() else delay
                print(f'  rate limited, waiting {wait}s', flush=True); time.sleep(wait); delay *= 2
            else: raise

def api(params):
    params = dict(params, format='json', maxlag=5)
    return fetch(API + '?' + urllib.parse.urlencode(params))

def strip(s): return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()

def info(titles, width=1600):
    d = api({'action': 'query', 'titles': '|'.join(titles), 'prop': 'imageinfo',
             'iiprop': 'url|extmetadata|size|mime', 'iiurlwidth': width})
    out = []
    for p in d['query']['pages'].values():
        if 'imageinfo' not in p: continue
        ii = p['imageinfo'][0]; m = ii.get('extmetadata', {})
        g = lambda k: strip(m.get(k, {}).get('value', ''))
        out.append(dict(title=p['title'], url=ii.get('thumburl') or ii['url'], w=ii['width'], h=ii['height'], mime=ii['mime'],
                        license=g('LicenseShortName'), artist=g('Artist')[:120], desc=g('ImageDescription')[:160],
                        page=ii.get('descriptionurl')))
    return out

def search(q, n=10):
    d = api({'action': 'query', 'list': 'search', 'srsearch': q + ' filetype:bitmap', 'srnamespace': 6, 'srlimit': n})
    titles = [x['title'] for x in d['query']['search']]
    return info(titles) if titles else []

def get(title, key, width=1280, i=None):
    if glob_exists(key): print('have', key); return
    i = i or info([title], width)[0]
    if not OK.match(i['license']): print(f'SKIP {key}: license not allowed: {i["license"]}'); return
    url = i['url'].split('?')[0]
    if '/thumb/' not in url:   # originals are throttled; always ask for a thumbnail
        m = re.match(r'https://upload\.wikimedia\.org/wikipedia/commons/(\w/\w\w)/(.+)$', url)
        if m:
            tw = max([s for s in (250, 330, 500, 960, 1280) if s < i['w']] or [250])
            url = f'https://thumb.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{tw}px-{m.group(2)}'
    url = url.replace('upload.wikimedia.org/wikipedia/commons/thumb', 'thumb.wikimedia.org/wikipedia/commons/thumb')
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() or '.jpg'
    if url.lower().endswith('.svg'): url += '.png'; ext = '.png'
    path = os.path.join(ASSETS, key + ext)
    data = fetch(url, binary=True)
    open(path, 'wb').write(data); time.sleep(1.5)
    cred = json.load(open(CRED, encoding='utf-8')) if os.path.exists(CRED) else {}
    cred[key] = dict(file=os.path.basename(path), title=i['title'], artist=i['artist'], license=i['license'], page=i['page'])
    json.dump(cred, open(CRED, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('saved', path, '|', i['artist'], '|', i['license'])

def glob_exists(key):
    import glob as g
    return any(not f.endswith('.json') for f in g.glob(os.path.join(ASSETS, key + '.*')))

def getmany(listfile, width=1280):
    """listfile lines: key | File:Title.ext"""
    pairs = [tuple(x.strip() for x in l.split('|', 1)) for l in open(listfile, encoding='utf-8-sig') if '|' in l and not l.startswith('#')]
    pairs = [(k, t) for k, t in pairs if not glob_exists(k)]
    for j in range(0, len(pairs), 20):
        chunk = pairs[j:j + 20]
        infos = {x['title']: x for x in info([t for _, t in chunk], width)}
        for k, t in chunk:
            norm = t.replace('_', ' ')
            i = infos.get(norm) or next((v for kk, v in infos.items() if kk.lower() == norm.lower()), None)
            if not i: print('NOT FOUND', k, t); continue
            try: get(t, k, width, i)
            except Exception as e: print('FAIL', k, e)

if __name__ == '__main__':
    if sys.argv[1] == 'getmany':
        getmany(sys.argv[2]); raise SystemExit
    if sys.argv[1] == 'search':
        for r in search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 10):
            flag = 'OK ' if OK.match(r['license']) else 'NO '
            print(f"{flag}{r['title']} | {r['w']}x{r['h']} | {r['license']} | {r['artist'][:40]} | {r['desc'][:80]}")
    elif sys.argv[1] == 'get':
        get(sys.argv[2], sys.argv[3])
