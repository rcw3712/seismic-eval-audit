from pathlib import Path
import csv,json,collections
P=Path(__file__).parent;out=[]
for p in sorted((P/'inputs').glob('*.csv')):
 with p.open(newline='',encoding='utf-8-sig') as f:
  rd=csv.DictReader(f);fields=rd.fieldnames;counts=collections.Counter();missing=collections.Counter();ids=set();duplicates=0;times=[];lats=[];lons=[];sources=set()
  for row in rd:
   counts[row.get('split','<NO_COLUMN>')]+=1
   for k in ['trace_name','source_id','split','station_network_code','station_code','source_origin_time','source_latitude_deg','source_longitude_deg']:
    if not row.get(k,'').strip():missing[k]+=1
   rid=row.get('trace_name','');duplicates+=rid in ids;ids.add(rid);sources.add(row.get('source_id',''))
   if row.get('source_origin_time'):times.append(row['source_origin_time'])
   for k,a in [('source_latitude_deg',lats),('source_longitude_deg',lons)]:
    try:a.append(float(row[k]))
    except (ValueError,KeyError):pass
 out.append({'dataset':p.stem,'rows':sum(counts.values()),'split_counts':dict(counts),'source_ids':len(sources-{''}) if 'source_id' in fields else None,'columns':fields,'missing':dict(missing),'duplicate_trace_name_rows':duplicates,'time_range':[min(times),max(times)] if times else None,'latitude_range':[min(lats),max(lats)] if lats else None,'longitude_range':[min(lons),max(lons)] if lons else None})
(P/'provenance/schema_profiles.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in x.items() if k!='columns'} for x in out],indent=2))
