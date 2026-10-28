from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent/".deps"))
import urllib.request,ssl,certifi,hashlib,json,datetime,csv,concurrent.futures,time
P=Path(__file__).parent
for name in ['inputs','provenance']:(P/name).mkdir(exist_ok=True)
tls=ssl.create_default_context();tls.load_verify_locations(certifi.where())
base='https://hifis-storage.desy.de/Helmholtz/HelmholtzAI/SeisBench/datasets/'
manifest=P/'provenance/input_manifest.json';records=json.loads(manifest.read_text()) if manifest.exists() else []
jobs=[(x,None,x+'/metadata.csv',x+'.csv') for x in ['ethz','geofon','iquique']]
jobs += [('isc_ehb',str(y),'isc_ehb_depthphases/metadata'+str(y)+'.csv','isc_ehb_'+str(y)+'.csv') for y in range(1987,2019)]
def request(url,start,end):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'seismic-metadata-audit','Range':f'bytes={start}-{end}'}),context=tls,timeout=25) as r:
    b=r.read();h=dict(r.headers)
    assert r.status==206 and h.get('Content-Range','').startswith(f'bytes {start}-{end}/'),(r.status,h)
    assert len(b)==end-start+1
    return b,h
  except Exception:
   if attempt==2:raise
   time.sleep(1)
for ds,chunk,rel,filename in jobs:
 url=base+rel;out=P/'inputs'/filename
 old=next((r for r in records if r.get('filename',r['dataset']+'.csv')==filename),None)
 if out.exists() and old and hashlib.sha256(out.read_bytes()).hexdigest()==old['sha256']:
  print('CACHED '+filename,flush=True);continue
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();_,headers=request(url,0,0);size=int(headers['Content-Range'].rsplit('/',1)[1]);step=2*1024*1024
 ranges=[(a,min(a+step,size)-1) for a in range(0,size,step)]
 with out.with_suffix('.partial').open('wb') as f:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
   for b,h in ex.map(lambda ab:request(url,*ab),ranges):
    assert h.get('ETag')==headers.get('ETag');f.write(b)
 h=hashlib.sha256(out.with_suffix('.partial').read_bytes()).hexdigest()
 if old:assert h==old['sha256'],'Remote metadata changed from frozen manifest: '+filename
 out.with_suffix('.partial').replace(out)
 if old:
  print('RESTORED VERIFIED '+filename,flush=True);continue
 with out.open(newline='',encoding='utf-8-sig') as f:cols=next(csv.reader(f))
 rec={'dataset':ds,'chunk':chunk,'filename':filename,'url':url,'retrieved_utc':start,'bytes':size,'sha256':h,'http_headers':headers,'columns':cols}
 if old:records.remove(old)
 records.append(rec);manifest.write_text(json.dumps(records,indent=2),encoding='utf-8')
 print(json.dumps({k:rec[k] for k in ['dataset','chunk','bytes','sha256']}),flush=True)
assert len(records)==35,len(records)
