from pathlib import Path
import sys,json,csv,hashlib,importlib.metadata
P=Path(__file__).parent;sys.path.insert(0,str(P/'.deps'))
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
A=json.loads((P/'results/I_A1/summary.json').read_text());B=json.loads((P/'results/I_A2/summary.json').read_text());C=json.loads((P/'results/I_A2/chronology.json').read_text())
manifest=json.loads((P/'provenance/input_manifest.json').read_text())
labels={'ethz':'ETHZ','geofon':'GEOFON','isc_ehb':'ISC-EHB Depth Phases','iquique':'Iquique'}
order=['ethz','geofon','isc_ehb','iquique']
def ar(ds,contract):return next(r for r in A if r['dataset']==ds and r['contract']==contract)
def pct(v):return f'{100*v:.2f}%'
table=['| Dataset | Metadata records | Supplied source IDs | Source train–test overlap | Station keys shared train–test | Test records on training station keys |','|---|---:|---:|---:|---:|---:|']
for ds in order:
 s=ar(ds,'source_id');t=ar(ds,'network_station')
 table.append(f"| {labels[ds]} | {t['input_records']:,} | "+(f"{s['groups']:,}" if 'groups' in s else 'Not supplied')+' | '+(str(s['train_test_shared_groups']) if 'train_test_shared_groups' in s else 'Not assessable')+f" | {t['train_test_shared_groups']:,} | {t['test_records_on_train_groups']:,}/{t['test_records']:,} ({pct(t['test_record_fraction'])}) |")
sp=[r for r in B if r['domain']=='spatial'];tem=[r for r in B if r['domain']=='temporal'];primary=next(r for r in sp if r['primary'])
sensitivity=['| Cell side | Test source IDs on training cells, range across four origins | Test records on training cells, range |','|---|---:|---:|']
for km in [10,25,50]:
 rs=[r for r in sp if r['size_km']==km]
 sensitivity.append(f"| {km} km | {min(r['test_source_ids_on_train_groups'] for r in rs)}/{rs[0]['test_source_ids']}–{max(r['test_source_ids_on_train_groups'] for r in rs)}/{rs[0]['test_source_ids']} ({pct(min(r['test_source_fraction'] for r in rs))}–{pct(max(r['test_source_fraction'] for r in rs))}) | {pct(min(r['test_record_fraction'] for r in rs))}–{pct(max(r['test_record_fraction'] for r in rs))} |")
temtable=['| Origin-time groups | Shared groups across any subsets | Shared train–test groups | Test source IDs on training groups |','|---|---:|---:|---:|']
for r in tem:temtable.append(f"| {r['contract']} | {r['shared_groups_any']} | {r['train_test_shared_groups']} | {r['test_source_ids_on_train_groups']}/{r['test_source_ids']} |")
text='''# Cross-dataset and ETHZ space–time metadata audits

## Main finding

The supplied source-ID contracts pass for ETHZ, GEOFON and ISC-EHB Depth Phases, while their station memberships overlap between training and testing. Iquique supports a station audit but does not supply source IDs. ETHZ reproduces the documented chronological partition as a positive control; the substantive contrast is that its source-disjoint, chronological split nevertheless shares many spatial grid cells. These findings distinguish evaluation targets rather than demonstrate an error in the datasets or a change in predictive accuracy.

## Scope and provenance

This author-run audit uses the unchanged seismic-eval-audit 0.1.3 wheel. PROTOCOL.md was written before calculating the new overlap outcomes; previously reported ETHZ source/station outcomes were already known. PROTOCOL_AMENDMENT_1.md records the schema-driven addition of ISC-EHB when Iquique lacked source_id. No model training, inference or waveform processing was performed. The completed manuscript and its DOI archives are unchanged.

All 35 metadata files were downloaded from the official SeisBench distribution on 28 October 2026. ISC-EHB includes every adapter-listed yearly chunk from 1987 through 2018. Native record identity is the pair (chunk filename, trace_name); catalog source IDs and split labels are preserved. Station keys are JSON-encoded (network,station) pairs, with no location-code or deployment-epoch distinction. Every assessed source/station contract covers its complete snapshot; Iquique source-ID auditing is explicitly not assessable. Its pinned adapter documents standard random sampling of records, which does not guarantee event separation. Missing source IDs prevent testing that requirement precisely where record-level allocation can be consequential; neither actual overlap nor a ranking as the highest-risk dataset is established. There is no invented origin-time proxy for source identity.

The snapshots comprise '''+f"{sum(ar(ds,'network_station')['input_records'] for ds in order):,}"+''' metadata rows. ISC-EHB contains 190,275 rows and 45,028 supplied source IDs in the downloaded files, whereas the current overview documentation lists 174,436 traces and 44,106 events. This discrepancy is disclosed rather than reconciled speculatively: results apply to the exact 32-file snapshot identified by hashes, not an assumed publication count. The retrieved metadata may differ from the snapshot described on that overview page. No duplicated (chunk,trace_name) keys were found.

Selection was purposive: public metadata, compatible fields and contrasting seismic settings, with manageable full-table sizes. It is not a representative survey of SeisBench. BohemiaSaxony lacks a public precompiled dataset because of restricted network data; CEED's approximately 2.1 GB full metadata was deferred. No outcome-based dataset substitution was performed.

## I-A1 supplied source and station memberships

'''+ '\n'.join(table)+'''

All three assessable source-ID audits have zero shared source IDs across all supplied subsets. ETHZ and GEOFON reproduce the chronological cutoffs in their pinned adapters (2019-01-08 / 2019-09-04 and 2012-11-01 / 2013-03-15, respectively), with zero label mismatches across 36,743 and 275,274 rows. These are positive controls against documented designs. The ISC-EHB adapter lists yearly chunks but does not define the split. The primary paper (Münchmeyer, Saul and Tilmann, 2024, Section 2.1; online 2023) describes random allocation of events to 70% training, 10% development and 20% testing, keeping all traces of each event together. Our source-ID result is consistent with that design; it does not reconstruct the original random assignment or establish byte identity with the smaller publication snapshot. All four station audits fail a separately stated unseen-station exclusion contract. This is not evidence that station exclusion was the dataset designers' intended target. In a global teleseismic dataset such as ISC-EHB, extensive reuse of the observing network is compatible with its purpose; unseen-station exclusion is only an optional additional target, not a quality criterion imposed on that dataset. Counts are within each dataset; no cross-catalog matching of physically identical events between datasets is claimed. The legacy report fields sources/shared_sources count the grouping unit identified by group_definition.

## I-A2 spatial membership in ETHZ

ETHZ contains 14 adapter-local source IDs beginning sb_id_, covering 376 records (train: 13 IDs/292 records; dev: 1 ID/84 records; test: 0). The adapter generates such an ID once per event when the catalog resource identifier ends in /1; within-event grouping is retained, but the field alone is not a resolvable catalog identifier. All 2,231 ETHZ source IDs have internally consistent, valid origin times and epicentre coordinates across their repeated records; all fall within the EPSG:3035 domain. All 36,743 records are retained. Coordinates are transformed from WGS84 longitude/latitude using always_xy=True to ETRS89-extended / LAEA Europe. Square cells use floor indexing, with a primary width of 25 km and origin (0,0). Widths 10,25,50 km and four origin offsets were specified before inspecting these results.

At the primary grid, '''+f"{primary['train_test_shared_groups']} cells are shared between training and testing. {primary['test_source_ids_on_train_groups']}/{primary['test_source_ids']} test source IDs ({pct(primary['test_source_fraction'])}) and {primary['test_records_on_train_groups']:,}/{primary['test_records']:,} test records ({pct(primary['test_record_fraction'])}) occupy training-represented cells."+'''

'''+ '\n'.join(sensitivity)+'''

The ranges describe sensitivity to four grid origins, not confidence intervals. All twelve spatial configurations contain shared train–test cells. A cell label is not an exact distance buffer: nearby sources can fall on opposite sides of a boundary, and within-cell distances vary. Neither a spatial FAIL nor a PASS establishes a causal effect on model performance or statistical independence.

## I-A2 temporal membership in ETHZ

As a positive control for the documented chronological design, every training origin time precedes every test origin time. The latest training source is 2019-01-07T13:21:19.080879Z and the earliest test source is 2019-09-04T13:43:22.273780Z, separated by '''+f"{C['min_test_minus_max_train_days']:.6f}"+''' days. This is the separation between training and testing, with the development interval between them; it is not an empty period with no observed events.

Calendar months have no training–test overlap. The adapter cutoffs fall within January (8 January) and September (4 September) 2019, explaining why those calendar months straddle adjacent subsets. The three-subset month audit reports FAIL because January 2019 is shared by train/dev and September 2019 by dev/test: two months and 935 affected records in total. Calendar days are disjoint across all three subsets. The broad year-2019 bin is shared between training and testing despite their chronological order. All predefined 7-,30-,90-day configurations have zero training–test overlap. These distinctions prevent an arbitrary time-bin FAIL from being described as temporal leakage.

'''+ '\n'.join(temtable)+'''

## Verification and limits

Twenty-eight assessable contract outputs were recomputed from the original CSVs by a separate pandas/vectorized implementation that does not import audit.py or the audit core. The follow-up context check also verifies every ETHZ/GEOFON split label against its documented time cutoffs and counts ETHZ adapter-local IDs (provenance/context_verification.json). The primary runner also checks report counts and pairwise overlaps against independent group-by aggregation. All 35 input hashes and the original wheel hash were verified. Projection-origin, forward/inverse transformation, negative-coordinate floor, UTC conversion and half-open time-boundary checks passed. See provenance/verification.json and the group-level reports.

This is author-run computational cross-checking, not independent-user adoption. Source IDs are supplied metadata, not independently verified physical earthquake associations. Iquique's missing source_id is a contract limitation, not evidence of zero overlap. No performance metric, causal leakage estimate or claim that all seismic datasets behave alike is supported. The additions strengthen demonstrated metadata portability and the distinction among evaluation units; they do not establish a new audit algorithm or guarantee editorial acceptance.

## Reusable results wording for a later manuscript decision

Across three complete metadata snapshots with supplied source identifiers (ETHZ, GEOFON and ISC-EHB Depth Phases), source memberships were disjoint, while 91.91%, 93.67% and 99.93% of test records, respectively, used station keys represented in training. Iquique shared all test station keys but did not provide the source-ID field required for the source contract. In ETHZ, all training sources preceded test sources, while 512/524 test source IDs occupied training-represented 25 km cells. Thus, source exclusion, station exclusion, temporal ordering and spatial-cell exclusion describe different evaluation requirements; the metadata audit does not equate an unmet additional requirement with an error in the supplied split.

## Sources

- SeisBench benchmark metadata descriptions and dataset references: https://seisbench.readthedocs.io/en/main/pages/data/benchmark_datasets.html
- Pinned adapter code and default chronological cutoffs: https://github.com/seisbench/seisbench/tree/e5616ad33c00aba75d5130b44222df46b41e4094/seisbench/data
- SeisBench software: Woollam et al. (2022), https://doi.org/10.1785/0220210324.
- Iquique: Woollam, J., Rietbrock, A., Bueno, A., and De Angelis, S. (2019). Convolutional Neural Network for Seismic Phase Classification, Performance Demonstration over a Local Seismic Network. Seismological Research Letters 90(2A), 491–502. https://doi.org/10.1785/0220180312.
- ISC-EHB Depth Phases: Münchmeyer, J., Saul, J., and Tilmann, F. (2024; online 2023). Learning the Deep and the Shallow: Deep-Learning-Based Depth Phase Picking and Earthquake Depth Estimation. Seismological Research Letters 95(3), 1543–1557. https://doi.org/10.1785/0220230187.
- GEOFON benchmark context: Münchmeyer et al. (2022), Which picker fits my data? A quantitative evaluation of deep learning based seismic pickers. Journal of Geophysical Research: Solid Earth 127, e2021JB023499. https://doi.org/10.1029/2021JB023499. This is a benchmark reference, not a verified dedicated DOI for the distributed GEOFON snapshot. Network GE attribution: GEOFON Data Centre (1993), https://doi.org/10.14470/TR560404; this network DOI does not identify the entire multi-network benchmark.
- CRS definition: EPSG:3035, retained as WKT in results/I_A2/geometry.json; PROJ/pyproj provenance in verification.json.
- ETHZ network attribution remains CH 10.12686/sed/networks/ch; C4 10.12686/sed/networks/c4; 8D 10.12686/sed/networks/8d; S 10.12686/sed/networks/s; XT 10.12686/alparray/xt_2014.

Original dataset and network attribution/licensing remains separate from the MIT software license. Raw metadata are retained locally for reproducibility. The public evidence bundle excludes raw metadata and record-level tables; it provides hashes, official-source acquisition, original analysis scripts and aggregate outputs. Dataset redistribution permission has not been established uniformly for these 35 files; no software license is extended to them. See LICENSE_REVIEW.md and ARCHIVE_STATUS.md. The old DOI does not identify this new evidence.
'''
(P/'AUDIT_REPORT.md').write_text(text,encoding='utf-8')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
F=P/'figures';F.mkdir(exist_ok=True)
def save(fig,name):
 fig.savefig(F/(name+'.png'),dpi=600,bbox_inches='tight');fig.savefig(F/(name+'.pdf'),bbox_inches='tight');fig.savefig(F/(name+'_preview.png'),dpi=130,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.4));pos=np.arange(4)
for i,ds in enumerate(order):
 s=ar(ds,'source_id');t=ar(ds,'network_station')
 if 'test_record_fraction' in s:ax.bar(i-.19,100*s['test_record_fraction'],width=.34,color='#23698c',label='Source ID' if i==0 else None);ax.text(i-.19,2,'0%',ha='center',fontsize=9)
 else:ax.text(i-.19,6,'N/A',ha='center',fontsize=9,color='#555')
 v=100*t['test_record_fraction'];ax.bar(i+.19,v,width=.34,color='#c46a26',label='Network + station' if i==0 else None);ax.text(i+.19,v+2,f'{v:.2f}%',ha='center',fontsize=9)
ax.set_xticks(pos,['ETHZ','GEOFON','ISC-EHB\nDepth Phases','Iquique']);ax.set_ylim(0,112);ax.set_ylabel('Test records on groups also present in training (%)');ax.legend(loc='lower center',bbox_to_anchor=(.5,1.01),ncol=2,frameon=False);ax.set_title('Supplied partitions answer different source and station questions',loc='left',pad=40)
fig.text(.13,-.015,'Iquique does not supply source_id. Station overlap is conditional on an unseen-station requirement.',fontsize=9)
fig.tight_layout();save(fig,'IA1_source_station')
events=pd.read_csv(P/'results/I_A2/source_locations_times.csv');fig,axs=plt.subplots(1,2,figsize=(11,4.6),gridspec_kw={'width_ratios':[1.15,1]})
for s,color in [('train','#23698c'),('dev','#db8c31'),('test','#8b416b')]:
 e=events[events.split==s];axs[0].scatter(e.x_m/1000,e.y_m/1000,s=7,alpha=.65,color=color,label=f'{s} (n={len(e)})')
axs[0].set_xlabel('EPSG:3035 easting (km)');axs[0].set_ylabel('EPSG:3035 northing (km)');axs[0].set_aspect('equal');axs[0].legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.15),ncol=3);axs[0].set_title('A  Source epicentres',loc='left')
for col,key,label in [('#23698c','test_source_fraction','Distinct test source IDs'),('#c46a26','test_record_fraction','Test records')]:
 for j,km in enumerate([10,25,50]):
  ys=[100*r[key] for r in sp if r['size_km']==km];xx=j+(-.08 if key=='test_source_fraction' else .08)
  axs[1].vlines(xx,min(ys),max(ys),color=col,lw=2);axs[1].scatter(np.full(4,xx),ys,color=col,s=25,label=label if j==0 else None)
axs[1].set_xticks([0,1,2],['10','25','50']);axs[1].set_ylim(75,101);axs[1].set_xlabel('Square-cell side length (km)');axs[1].set_ylabel('Test units in training-represented cells (%)');axs[1].legend(fontsize=8,loc='lower right');axs[1].set_title('B  Four grid origins at each size',loc='left')
fig.tight_layout();save(fig,'IA2_spatial_sensitivity')
fig,axs=plt.subplots(1,2,figsize=(11,4.6),gridspec_kw={'width_ratios':[1.1,1]})
for i,s in enumerate(['train','dev','test']):
 r=next(r for r in C['time_ranges'] if r['split']==s);lo,hi=pd.to_datetime(r['origin_min_utc']),pd.to_datetime(r['origin_max_utc']);axs[0].plot([lo,hi],[i,i],lw=12,solid_capstyle='butt',color=['#23698c','#db8c31','#8b416b'][i]);axs[0].text(hi,i+.16,str(r['source_ids'])+' sources',ha='right',fontsize=8)
axs[0].set_yticks([0,1,2],['train','dev','test']);axs[0].set_ylim(-.5,2.7);axs[0].xaxis.set_major_locator(mdates.YearLocator(2));axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'));axs[0].set_xlabel('Source origin time (UTC)');axs[0].set_title('A  Training precedes test by 240 days',loc='left')
y=np.arange(len(tem));axs[1].barh(y-.17,[r['shared_groups_any'] for r in tem],height=.32,label='Any subset pair',color='#7c8793');axs[1].barh(y+.17,[r['train_test_shared_groups'] for r in tem],height=.32,label='Train–test',color='#8b416b')
names=['Calendar month','Calendar day','Calendar year','7 d / offset 0','7 d / offset 3.5 d','30 d / offset 0','30 d / offset 15 d','90 d / offset 0','90 d / offset 45 d'];axs[1].set_yticks(y,names,fontsize=8);axs[1].invert_yaxis();axs[1].set_xticks([0,1,2]);axs[1].set_xlabel('Shared time bins');axs[1].legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.15),ncol=2);axs[1].set_title('B  Bin sharing depends on definition',loc='left')
fig.tight_layout();save(fig,'IA2_temporal_order')
(F/'CAPTIONS.md').write_text('''# Figure captions

IA1. Fraction of test records whose exact supplied source-ID or network–station key is represented in training. Source-ID exclusion passes in ETHZ, GEOFON and ISC-EHB. Iquique source-ID results are not assessable, not zero. Station overlap describes a separately stated evaluation target and does not invalidate the intended supplied split.

IA2 spatial. (A) Unique ETHZ source locations by supplied split in EPSG:3035; points represent sources, not stations, and overlap visually. (B) Test-source and test-record fractions occupying training-represented cells for 10,25,50 km square grids and four offsets. Vertical ranges show grid-origin sensitivity, not statistical confidence intervals. The primary 25 km origin is (0,0).

IA2 temporal. (A) Origin-time ranges per ETHZ subset. The 240-day train–test separation contains the development period and is not an event-free interval. (B) Shared bins across any subset pair versus train–test only for every prespecified temporal configuration. Chronological ordering is a positive control for the documented adapter design. Monthly sharing concerns the within-month 8 January and 4 September train/dev and dev/test boundaries; the broad year bin can be shared while chronological order holds.

PNG exports are 600 dpi; PDF exports use vector elements with embedded TrueType fonts. Preview PNGs are internal QA only.
''',encoding='utf-8')
versions={m:importlib.metadata.version(m) for m in ['pandas','numpy','matplotlib','pyproj']}
(P/'requirements.txt').write_text('\n'.join(k+'=='+v for k,v in versions.items())+'\n',encoding='utf-8')
print(json.dumps({'report':'AUDIT_REPORT.md','figures':3,'versions':versions}))
