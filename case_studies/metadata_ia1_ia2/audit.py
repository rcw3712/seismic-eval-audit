"""Metadata-only audits using the unchanged archived wheel and a separate cross-check."""
from pathlib import Path
import sys
P=Path(__file__).parent
for x in [P/'.deps',P/'software/installed']:sys.path.insert(0,str(x))
import argparse,csv,json,gzip,hashlib,datetime,math,collections,platform
import pandas as pd
import numpy as np
from pyproj import Transformer,CRS
import seismic_eval_audit as sea

def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,allow_nan=False),encoding='utf-8')
def writecsv(path,rows,fields=None):
 rows=list(rows);fields=fields or list(rows[0])
 opener=gzip.open if path.suffix=='.gz' else open
 with opener(path,'wt',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def good(s):return isinstance(s,str) and bool(s.strip()) and s==s.strip() and s.lower() not in ['nan','none','null']
def load(ds):
 manifests=json.loads((P/'provenance/input_manifest.json').read_text())
 selected=[x for x in manifests if x['dataset']==ds]
 if ds=='isc_ehb':assert len(selected)==32,'Require all 32 ISC-EHB chunks'
 out=[];fields=set()
 for meta in sorted(selected,key=lambda x:x.get('filename',ds+'.csv')):
  fn=meta.get('filename',ds+'.csv');p=P/'inputs'/fn
  assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256'],fn
  with p.open(newline='',encoding='utf-8-sig') as f:
   reader=csv.DictReader(f);fields.update(reader.fieldnames)
   for i,r in enumerate(reader,2):
    out.append({'record_id':json.dumps([fn,r.get('trace_name','')],separators=(',',':')),'native_trace_name':r.get('trace_name',''),'input_file':fn,'input_line':i,
     'source_id':r.get('source_id',''),'split':r.get('split',''),'network':r.get('station_network_code',''),'station':r.get('station_code',''),
     'origin':r.get('source_origin_time',''),'latitude':r.get('source_latitude_deg',''),'longitude':r.get('source_longitude_deg','')})
 assert out
 assert len({r['record_id'] for r in out})==len(out),'Duplicate native trace within chunk'
 return out,fields
def verify_report(rows,report):
 # Independently aggregate the prepared memberships. No core functions used.
 df=pd.DataFrame(rows);gs=df.groupby('group_id')['split'].nunique();shared=set(gs[gs>1].index)
 assert report['records']==len(df) and report['sources']==df['group_id'].nunique()
 assert report['shared_sources']==len(shared) and report['affected_records']==int(df.group_id.isin(shared).sum())
 for split,block in df.groupby('split'):
  assert report['splits'][split]=={'records':len(block),'sources':block.group_id.nunique()}
 for pair in report['pairs']:
  a=df[df.split==pair['a']];b=df[df.split==pair['b']];over=set(a.group_id)&set(b.group_id)
  assert pair['shared_sources']==len(over)
  assert pair['a_records']==int(a.group_id.isin(over).sum()) and pair['b_records']==int(b.group_id.isin(over).sum())
 return True
def run_contract(dataset,name,raw,groups,dest,details):
 rows=[{'record_id':r['record_id'],'source_id':r['source_id'],'split':r['split'],'group_id':g} for r,g in zip(raw,groups)]
 report=sea.audit_split(rows,group='group_id');verify_report(rows,report)
 dest.mkdir(parents=True,exist_ok=False)
 writecsv(dest/'membership.csv.gz',rows)
 writecsv(dest/'violations.csv.gz',report.pop('violations'),['record_id','source_id','split'])
 report.update(dataset=dataset,contract=name,group_definition=details,independent_aggregation_check='PASS',violations_file='violations.csv.gz')
 dump(dest/'report.json',report)
 tr=[r for r in rows if r['split']=='train'];te=[r for r in rows if r['split']=='test'];tg={r['group_id'] for r in tr};testg={r['group_id'] for r in te};exp=[r for r in te if r['group_id'] in tg]
 testsrc={r['source_id'] for r in te if good(r['source_id'])};expsrc={r['source_id'] for r in exp if good(r['source_id'])}
 summary=dict(dataset=dataset,contract=name,status=report['status'],eligible_records=len(rows),groups=report['sources'],shared_groups_any=report['shared_sources'],affected_records_any=report['affected_records'],
  train_records=len(tr),test_records=len(te),train_test_shared_groups=len(tg&testg),test_groups=len(testg),test_records_on_train_groups=len(exp),test_record_fraction=len(exp)/len(te) if te else None,
  test_source_ids=len(testsrc) if testsrc else None,test_source_ids_on_train_groups=len(expsrc) if testsrc else None,test_source_fraction=len(expsrc)/len(testsrc) if testsrc else None)
 group_rows=[]
 df=pd.DataFrame(rows)
 for (grp,split),block in df.groupby(['group_id','split'],sort=True):
  group_rows.append({'group_id':grp,'split':split,'records':len(block),'source_ids':int(block.source_id[block.source_id.map(good)].nunique())})
 writecsv(dest/'group_counts.csv.gz',group_rows)
 return summary
def a1():
 O=P/'results/I_A1';O.mkdir(parents=True,exist_ok=False);summ=[];profiles=[]
 for ds in ['ethz','geofon','iquique','isc_ehb']:
  raw,cols=load(ds);prof={'dataset':ds,'input_records':len(raw),'split_counts':dict(collections.Counter(r['split'] for r in raw)),'has_source_id':'source_id' in cols,'contracts':{}}
  for contract in ['source_id','network_station']:
   valid=[];groups=[];bad=[]
   for r in raw:
    reasons=[]
    for k in ['native_trace_name','split']:
     if not good(r[k]):reasons.append('invalid_'+k)
    for k in (['source_id'] if contract=='source_id' else ['network','station']):
     if not good(r[k]):reasons.append('invalid_'+k)
    if reasons:bad.append({'record_id':r['record_id'],'reasons':'|'.join(reasons)})
    else:
     valid.append(r);groups.append(r['source_id'] if contract=='source_id' else json.dumps([r['network'],r['station']],separators=(',',':')))
   prof['contracts'][contract]={'eligible':len(valid),'excluded':len(bad),'reasons':dict(collections.Counter(r['reasons'] for r in bad))}
   writecsv(O/(ds+'_'+contract+'_excluded.csv.gz'),bad,['record_id','reasons'])
   if not valid:
    summ.append({'dataset':ds,'contract':contract,'status':'NOT_ASSESSABLE','eligible_records':0,'excluded_records':len(raw),'input_records':len(raw)});continue
   result=run_contract(ds,contract,valid,groups,O/(ds+'_'+contract),'Exact supplied source_id' if contract=='source_id' else 'JSON tuple of station_network_code and station_code; no location/epoch distinction')
   result.update(input_records=len(raw),excluded_records=len(bad),coverage=len(valid)/len(raw),scope='complete table' if not bad else 'eligible records only; full table has missing/invalid input')
   summ.append(result)
  profiles.append(prof);print(ds,prof['input_records'],prof['contracts'],flush=True)
 fields=list(dict.fromkeys(k for r in summ for k in r));writecsv(O/'summary.csv',summ,fields);dump(O/'summary.json',summ);dump(O/'input_quality.json',profiles)
def utc(s):
 d=datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
 if d.tzinfo is None:raise ValueError('Timezone not specified')
 return d.astimezone(datetime.timezone.utc)
def timekey(d,kind,width=None,offset=0):
 if kind=='month':return d.strftime('%Y-%m')
 if kind=='day':return d.strftime('%Y-%m-%d')
 if kind=='year':return str(d.year)
 return str(math.floor((d.timestamp()-offset*86400)/(width*86400)))
def gridkey(x,y,size,ox=0,oy=0):return f'{math.floor((x-ox)/size)},{math.floor((y-oy)/size)}'
def a2():
 O=P/'results/I_A2';O.mkdir(parents=True,exist_ok=False);raw,_=load('ethz');sources=collections.defaultdict(list)
 for r in raw:sources[r['source_id']].append(r)
 proj=Transformer.from_crs(4326,3035,always_xy=True);inverse=Transformer.from_crs(3035,4326,always_xy=True);crs=CRS.from_epsg(3035)
 events={};quality=[];tranges=[]
 for sid,rs in sorted(sources.items()):
  e={'source_id':sid,'record_count':len(rs),'splits':sorted({r['split'] for r in rs})};times=set();coords=set();errors=[]
  try:
   for r in rs:times.add(utc(r['origin']))
   if len(times)!=1:raise ValueError('conflicting origin times')
   e['time']=next(iter(times));e['time_valid']=True
  except (ValueError,TypeError):e['time_valid']=False;errors.append('missing_invalid_or_conflicting_time')
  try:
   for r in rs:
    lat,lon=float(r['latitude']),float(r['longitude'])
    if not math.isfinite(lat+lon) or not(-90<=lat<=90 and -180<=lon<=180):raise ValueError('invalid coordinates')
    coords.add((lat,lon))
   if len(coords)!=1:raise ValueError('conflicting coordinates')
   lat,lon=next(iter(coords));area=crs.area_of_use
   if not(area.west<=lon<=area.east and area.south<=lat<=area.north):raise ValueError('outside CRS extent')
   x,y=proj.transform(lon,lat,errcheck=True);lon2,lat2=inverse.transform(x,y,errcheck=True)
   assert abs(lon-lon2)<1e-7 and abs(lat-lat2)<1e-7
   e.update(latitude=lat,longitude=lon,x_m=x,y_m=y,space_valid=True)
  except (ValueError,TypeError):e['space_valid']=False;errors.append('missing_invalid_conflicting_or_out_of_domain_coordinates')
  quality.append({'source_id':sid,'records':len(rs),'time_valid':e['time_valid'],'space_valid':e['space_valid'],'reason':'|'.join(errors)})
  events[sid]=e
 # Guard transformation and bin edges with known projection origin and exact UTC boundaries.
 px,py=proj.transform(10,52);assert abs(px-4321000)<0.01 and abs(py-3210000)<0.01
 assert gridkey(0,0,10000)=='0,0' and gridkey(-.01,10000,10000)=='-1,1'
 assert timekey(utc('1970-01-08T00:00:00Z'),'fixed',7)=='1'
 assert timekey(utc('1970-01-07T23:59:59Z'),'fixed',7)=='0'
 assert timekey(utc('2020-02-01T00:30:00+01:00'),'month')=='2020-01'
 summaries=[]
 for kind,width,offset in [('month',None,0),('day',None,0),('year',None,0)]+[('fixed',d,o) for d in [7,30,90] for o in [0,d/2]]:
  name='calendar_'+kind if kind!='fixed' else f'window_{width}d_offset_{offset:g}d'
  valid=[r for r in raw if events[r['source_id']]['time_valid'] and good(r['split'])]
  groups=[timekey(events[r['source_id']]['time'],kind,width,offset) for r in valid]
  s=run_contract('ethz',name,valid,groups,O/name,{'type':'origin_time_UTC','kind':kind,'days':width,'offset_days':offset,'epoch':'1970-01-01T00:00:00Z','bins':'half-open'})
  s.update(domain='temporal',primary=kind=='month',excluded_records=len(raw)-len(valid));summaries.append(s)
 for km in [10,25,50]:
  size=km*1000
  for fx,fy in [(0,0),(.5,0),(0,.5),(.5,.5)]:
   name=f'grid_{km}km_offset_{fx:g}_{fy:g}'
   valid=[r for r in raw if events[r['source_id']]['space_valid'] and good(r['split'])]
   groups=[gridkey(events[r['source_id']]['x_m'],events[r['source_id']]['y_m'],size,fx*size,fy*size) for r in valid]
   s=run_contract('ethz',name,valid,groups,O/name,{'crs':'EPSG:3035','size_m':size,'offset_x_m':fx*size,'offset_y_m':fy*size,'index':'floor','input_order':'longitude,latitude'})
   s.update(domain='spatial',primary=km==25 and fx==fy==0,size_km=km,offset_x_fraction=fx,offset_y_fraction=fy,excluded_records=len(raw)-len(valid));summaries.append(s)
 for split in sorted({r['split'] for r in raw}):
  es=[e for e in events.values() if split in e['splits'] and e['time_valid']];ts=[e['time'] for e in es]
  tranges.append({'split':split,'source_ids':len(es),'origin_min_utc':min(ts).isoformat(),'origin_max_utc':max(ts).isoformat()})
 train=[e['time'] for e in events.values() if 'train' in e['splits'] and e['time_valid']];test=[e['time'] for e in events.values() if 'test' in e['splits'] and e['time_valid']]
 chronology={'all_train_precedes_all_test':max(train)<min(test),'min_test_minus_max_train_days':(min(test)-max(train)).total_seconds()/86400,'time_ranges':tranges}
 fields=list(dict.fromkeys(k for s in summaries for k in s));writecsv(O/'summary.csv',summaries,fields);dump(O/'summary.json',summaries);writecsv(O/'source_property_quality.csv',quality);dump(O/'chronology.json',chronology)
 dump(O/'geometry.json',{'crs_wkt':crs.to_wkt(),'area_of_use':str(crs.area_of_use),'origin_test':'PASS','roundtrip_tolerance_deg':1e-7,'source_count':len(events),'valid_time_sources':sum(e['time_valid'] for e in events.values()),'valid_space_sources':sum(e['space_valid'] for e in events.values())})
 writecsv(O/'source_locations_times.csv',[{'source_id':sid,'split':'|'.join(e['splits']),'records':e['record_count'],'time_utc':e['time'].isoformat() if e['time_valid'] else '', 'latitude':e.get('latitude',''),'longitude':e.get('longitude',''),'x_m':e.get('x_m',''),'y_m':e.get('y_m','')} for sid,e in events.items()])
 print(json.dumps({'primary':[s for s in summaries if s['primary']],'chronology':chronology},indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--section',choices=['a1','a2'],required=True);a=p.parse_args()
 assert Path(sea.__file__).resolve().is_relative_to((P/'software/installed').resolve())
 assert sea.__version__=='0.1.3'
 (a1 if a.section=='a1' else a2)()
 dump(P/'provenance'/('environment_'+a.section+'.json'),{'python':platform.python_version(),'platform':platform.platform(),'pandas':pd.__version__,'numpy':np.__version__,'package':sea.__version__,'import_path':str(Path(sea.__file__).resolve()),'training':False,'inference':False})
