from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent/".deps"))
import urllib.request,ssl,certifi,json,hashlib,datetime
P=Path(__file__).parent;O=P/'provenance';O.mkdir(exist_ok=True)
c=ssl.create_default_context();c.load_verify_locations(certifi.where())
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'seismic-metadata-audit'}),context=c,timeout=45) as r:return r.read()
sha='e5616ad33c00aba75d5130b44222df46b41e4094'
entries=[]
for name in ['ethz','geofon','iquique','isc_ehb']:
 url=f'https://raw.githubusercontent.com/seisbench/seisbench/{sha}/seisbench/data/{name}.py';b=get(url)
 (O/('seisbench_'+name+'.py')).write_bytes(b)
 entries.append({'dataset':name,'source_url':url,'upstream_commit':sha,'sha256':hashlib.sha256(b).hexdigest()})
(O/'upstream_sources.json').write_text(json.dumps({'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':entries,'documentation':'https://seisbench.readthedocs.io/en/main/pages/data/benchmark_datasets.html','note':'Current adapter code provides context, not proof of which historical code generated the distributed CSV.'},indent=2),encoding='utf-8')
print(json.dumps({'upstream_commit':sha,'files':len(entries)}))
