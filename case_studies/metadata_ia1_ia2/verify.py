"""Recompute audit memberships from original CSVs without importing audit.py or audit core."""
from pathlib import Path
import sys,json,hashlib
P=Path(__file__).parent;sys.path.insert(0,str(P/'.deps'))
import pandas as pd
import numpy as np
import pyproj
from pyproj import Transformer
manifest=json.loads((P/'provenance/input_manifest.json').read_text());assert len(manifest)==35
for m in manifest:
 assert hashlib.sha256((P/'inputs'/m.get('filename',m['dataset']+'.csv')).read_bytes()).hexdigest()==m['sha256']
wheel=P/'software/seismic_eval_audit-0.1.3-py3-none-any.whl'
assert hashlib.sha256(wheel.read_bytes()).hexdigest()=='12948abcd2805d42fa7af17e3eca2cdd499fd416e55c96aa94f9ef2a30c4b864'
def original(ds):
 frames=[]
 for m in manifest:
  if m['dataset']!=ds:continue
  fn=m.get('filename',ds+'.csv')
  f=pd.read_csv(P/'inputs'/fn,dtype=str,keep_default_na=False,usecols=lambda c:c in ['trace_name','source_id','split','station_network_code','station_code','source_origin_time','source_latitude_deg','source_longitude_deg'])
  f['record_id']=[json.dumps([fn,n],separators=(',',':')) for n in f.trace_name]
  frames.append(f)
 return pd.concat(frames,ignore_index=True).set_index('record_id')
verified=[]
for ds in ['ethz','geofon','iquique','isc_ehb']:
 f=original(ds);assert f.index.is_unique
 for con in ['source_id','network_station']:
  d=P/'results/I_A1'/(ds+'_'+con)
  if con=='source_id' and 'source_id' not in f:
   assert ds=='iquique' and not d.exists();continue
  g=f.source_id if con=='source_id' else pd.Series([json.dumps([n,s],separators=(',',':')) for n,s in zip(f.station_network_code,f.station_code)],index=f.index)
  mem=pd.read_csv(d/'membership.csv.gz',dtype=str,keep_default_na=False).set_index('record_id')
  assert set(mem.index)==set(f.index) and (mem.group_id==g.loc[mem.index]).all() and (mem.split==f.split.loc[mem.index]).all()
  rep=json.loads((d/'report.json').read_text())
  by={s:set(g[f.split==s]) for s in sorted(f.split.unique())}
  shared={v for v in set(g) if sum(v in x for x in by.values())>1}
  assert rep['shared_sources']==len(shared) and rep['affected_records']==int(g.isin(shared).sum())
  verified.append(ds+'/'+con)
eth=original('ethz');times=pd.to_datetime(eth.source_origin_time,utc=True,format='ISO8601')
x,y=Transformer.from_crs(4326,3035,always_xy=True).transform(eth.source_longitude_deg.astype(float).to_numpy(),eth.source_latitude_deg.astype(float).to_numpy())
for d in sorted((P/'results/I_A2').iterdir()):
 if not d.is_dir():continue
 rep=json.loads((d/'report.json').read_text());gd=rep['group_definition'];mem=pd.read_csv(d/'membership.csv.gz',dtype=str,keep_default_na=False).set_index('record_id')
 if 'crs' in gd:
  a=np.floor((x-gd['offset_x_m'])/gd['size_m']).astype(int);b=np.floor((y-gd['offset_y_m'])/gd['size_m']).astype(int)
  vals=[f'{i},{j}' for i,j in zip(a,b)]
 elif gd['kind'] in ['day','month','year']:vals=times.dt.strftime({'day':'%Y-%m-%d','month':'%Y-%m','year':'%Y'}[gd['kind']]).tolist()
 else:
  secs=np.array([t.timestamp() for t in times]);vals=np.floor((secs-gd['offset_days']*86400)/(gd['days']*86400)).astype(int).astype(str)
 expected=pd.Series(vals,index=eth.index)
 assert set(mem.index)==set(eth.index) and (mem.group_id==expected.loc[mem.index]).all()
 assert (mem.source_id==eth.source_id.loc[mem.index]).all() and (mem.split==eth.split.loc[mem.index]).all()
 verified.append('ethz/'+d.name)
result={'status':'PASS','input_files_verified':len(manifest),'contracts_recomputed_from_raw':len(verified),'contracts':verified,'wheel_sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),'method':'Separate pandas/vectorized implementation, without importing audit.py or seismic_eval_audit','pyproj':pyproj.__version__,'proj':pyproj.proj_version_str,'independent_user_adoption':False}
(P/'provenance/verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
