import json, subprocess, os, urllib.request
G = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd')
T = subprocess.run([G,'auth','print-access-token'],capture_output=True,text=True,check=True).stdout.strip()
def get(u):
    r = urllib.request.Request('https://firebasehosting.googleapis.com/v1beta1/'+u, headers={'Authorization':'Bearer '+T,'x-goog-user-project':'undergrad-recap'})
    return json.load(urllib.request.urlopen(r))
rels = get('sites/undergrad-recap/releases?pageSize=5')['releases']
for r in rels: print(r['releaseTime'][:19], r['type'], r.get('version',{}).get('name','').split('/')[-1], r.get('version',{}).get('fileCount'), r.get('version',{}).get('versionBytes'))
v = rels[0]['version']['name']
fs = get(v+'/files?pageSize=1000').get('files',[])
print('\nLIVE VERSION', v, len(fs), 'files')
for f in sorted(fs, key=lambda f:f['path']): print(f['path'])
