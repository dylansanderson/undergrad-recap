"""Deploy public/ to Firebase Hosting (site undergrad-recap) through the Hosting REST API, using the gcloud login.
/api/** is rewritten to the Cloud Run service 'narrator' (us-central1)."""
import os, sys, json, gzip, hashlib, subprocess, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(HERE, 'public')
SITE, PROJECT = 'undergrad-recap', 'undergrad-recap'
# usage: deploy_hosting.py            -> live site
#        deploy_hosting.py preview    -> preview channel https://undergrad-recap--preview-<hash>.web.app
#        deploy_hosting.py disable    -> take the live site offline (same as `firebase hosting:disable`)
CHANNEL = sys.argv[1] if len(sys.argv) > 1 else None
GCLOUD = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd')
TOKEN = subprocess.run([GCLOUD, 'auth', 'print-access-token'], capture_output=True, text=True, check=True).stdout.strip()
API = 'https://firebasehosting.googleapis.com/v1beta1/'

def call(method, url, body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url, data=data, method=method, headers={'Authorization': 'Bearer ' + TOKEN, 'x-goog-user-project': PROJECT, 'Content-Type': ctype})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: t = r.read(); return json.loads(t) if t else {}
    except urllib.error.HTTPError as e:
        sys.exit(f'{method} {url} -> {e.code}: {e.read().decode()[:800]}')

if CHANNEL == 'disable':   # take the live site offline (visitors get "Site Not Found"); redeploy to bring it back
    rel = call('POST', f'{API}sites/{SITE}/releases', {'type': 'SITE_DISABLE', 'message': 'site disabled'})
    sys.exit(f"site disabled ({rel.get('name')}). Re-enable: python -P -E deploy_hosting.py")

CONFIG = {
    'rewrites': [{'glob': '/api/**', 'run': {'serviceId': 'narrator', 'region': 'us-central1'}}],
    'headers': [
        {'glob': '**', 'headers': {'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'strict-origin-when-cross-origin',
                                   'Permissions-Policy': 'microphone=(self), camera=(), geolocation=()'}},
        {'glob': '/{index.html,player.js,meta.json}', 'headers': {'Cache-Control': 'no-cache'}},
        {'glob': '/slides/**', 'headers': {'Cache-Control': 'public, max-age=86400'}},
    ],
    'cleanUrls': True,
}

files = {}
for root, _, names in os.walk(PUB):
    for n in names:
        full = os.path.join(root, n); rel = '/' + os.path.relpath(full, PUB).replace(os.sep, '/')
        gz = gzip.compress(open(full, 'rb').read(), compresslevel=9, mtime=0)
        files[rel] = (hashlib.sha256(gz).hexdigest(), gz)
print(f'{len(files)} files, {sum(len(g) for _, g in files.values()) / 1e6:.1f} MB gzipped')

ver = call('POST', f'{API}sites/{SITE}/versions', {'config': CONFIG})['name']
pop = call('POST', f'{API}{ver}:populateFiles', {'files': {k: h for k, (h, _) in files.items()}})
need = set(pop.get('uploadRequiredHashes', [])); up = pop['uploadUrl']
byhash = {h: g for h, g in files.values()}
for i, h in enumerate(sorted(need), 1):
    call('POST', f'{up}/{h}', raw=byhash[h], ctype='application/octet-stream'); print(f'  uploaded {i}/{len(need)}', end='\r')
print(f'\nuploaded {len(need)} new files')
call('PATCH', f'{API}{ver}?update_mask=status', {'status': 'FINALIZED'})
if CHANNEL:   # preview channel: a separate URL that expires after 7 days; the live site is untouched
    chans = call('GET', f'{API}sites/{SITE}/channels').get('channels', [])
    ch = next((c for c in chans if c['name'].endswith('/channels/' + CHANNEL)), None) or \
         call('POST', f'{API}sites/{SITE}/channels?channelId={CHANNEL}', {'ttl': '604800s'})
    rel = call('POST', f'{API}sites/{SITE}/channels/{CHANNEL}/releases?versionName={ver}', {'message': 'preview'})
    print('preview released ->', ch.get('url'))
else:
    rel = call('POST', f'{API}sites/{SITE}/releases?versionName={ver}', {'message': 'deploy'})
    print('released', rel.get('name'), '-> https://undergrad-recap.web.app')
