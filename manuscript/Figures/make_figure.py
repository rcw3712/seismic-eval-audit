from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
p=Path(__file__).parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42})
fig,axs=plt.subplots(1,2,figsize=(9,4.5))
def branch(ax,source_y,station_y,label,is_test=False):
 ax.add_patch(FancyArrowPatch((1.45,source_y),(3.05,station_y),arrowstyle='->',mutation_scale=10,color='#777'))
 ax.scatter([3.4],[station_y],marker='^',s=65,color='#333')
 ax.text(3.85,station_y,label,va='center',fontsize=9)
 c='#B85C1C' if is_test else '#226D94'
 ax.add_patch(FancyArrowPatch((6.15,station_y),(7.05,station_y),arrowstyle='->',mutation_scale=10,color=c))
 ax.add_patch(Rectangle((7.2,station_y-.32),2.15,.64,facecolor=c,edgecolor=c))
 ax.text(8.275,station_y,'Test' if is_test else 'Train',ha='center',va='center',color='white',fontsize=9)
for j,ax in enumerate(axs):
 ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
 ax.text(0,9.65,('A  Split by record','B  Split by earthquake source')[j],weight='bold',fontsize=11)
 ax.scatter([1],[7.4],marker='*',s=230,color='#343434')
 ax.text(1,6.35,'Earthquake 1',ha='center',fontsize=9)
 for i,(lab,y) in enumerate(zip(['Station A','Station B','Station C'],[8.6,7.4,6.2])):
  branch(ax,7.4,y,lab,j==0 and i==2)
 if j==1:
  ax.scatter([1],[3.75],marker='*',s=230,color='#343434')
  ax.text(1,2.7,'Earthquake 2',ha='center',fontsize=9)
  branch(ax,3.75,4.3,'Station A',True);branch(ax,3.75,3.15,'Station D',True)
  ax.text(5,1.05,'Each earthquake stays in one subset.\nStations can still occur in both subsets.',ha='center',va='center',fontsize=10)
 else:
  ax.text(5,3.7,'Different files from the same earthquake\ncan cross training and test subsets.',ha='center',va='center',fontsize=10)
  ax.text(5,1.05,'Fails a source-disjoint\nevaluation requirement.',ha='center',va='center',fontsize=10)
fig.subplots_adjust(left=.035,right=.98,bottom=.035,top=.96,wspace=.15)
for ext,kwargs in [('png',{'dpi':600}),('pdf',{})]:fig.savefig(p/f'Figure1_source_separation.{ext}',facecolor='white',**kwargs)
fig.savefig(p/'Figure1_preview.png',dpi=150,facecolor='white')
