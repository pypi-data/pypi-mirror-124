import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class FHcolors:
	def __init__(self):
		self.green1=np.array([23,156,125,255])/255
		self.green2=np.array([177,200,0,255])/255
		self.orange1=np.array([235,106,10,255])/255
		self.orange2=np.array([254,239,214,255])/255
		self.blue1=np.array([0,110,146,255])/255
		self.blue2=np.array([37,186,226,255])/255
		self.grey1=np.array([225,227,227,255])/255
		self.grey2=np.array([168,175,175,255])/255
		self.red1=np.array([226,0,26,255])/255

class FHcmap:
	def __init__(self):
		self.BlackToGreen = self.create_cmap([[0,0,0,1],colors.green1])
		self.WhiteToGreen = self.create_cmap([[1,1,1,1],colors.green1])
		self.GreenToWhite = self.create_cmap([colors.green1,[1,1,1,1]])
		self.OrangeToGreen = self.create_cmap([colors.orange1,colors.green1])
		self.GreenToOrange = self.create_cmap([colors.green1,colors.orange1])
		self.BlackToGreenToOrangeToWhite = self.create_cmap([[0,0,0,1],colors.green1,colors.orange1,[1,1,1,1]])
		self.BlackToGreenToWhite = self.create_cmap([[0,0,0,1],colors.green1,[1,1,1,1]],[0,100,255])
		self.BlackToGreenToWhite_short = self.create_cmap([self.BlackToGreenToWhite(50),colors.green1,self.BlackToGreenToWhite(200)],[0,85,255])
		self.colors=ListedColormap(np.vstack([colors.green1,colors.orange1,colors.blue1,colors.red1,colors.green2]),N=5)

	def startstoparray(self,start,stop,length=256):
		r=np.interp(np.linspace(0,1,length),[0,1],[start[0],stop[0]])
		g=np.interp(np.linspace(0,1,length),[0,1],[start[1],stop[1]])
		b=np.interp(np.linspace(0,1,length),[0,1],[start[2],stop[2]])
		a=np.interp(np.linspace(0,1,length),[0,1],[1,1])
		rgba=np.vstack((r,g,b,a)).T
		return rgba
        
	def create_cmap(self,tup,poss=False):
		if not poss:
			poss=np.linspace(0,255,len(tup))
		a=np.empty((0,4))
		for i in range(len(tup)-1):
			start=tup[i]
			stop =tup[i+1]
			b=self.startstoparray(start,stop,int(poss[i+1]-poss[i]))
			a=np.vstack((a,b))
		return ListedColormap(a)
        

colors=FHcolors()
maps=FHcmap()

if __name__ == "__main__":
	maps=[maps.BlackToGreen,maps.GreenToWhite,maps.GreenToOrange,maps.BlackToGreenToOrangeToWhite,maps.BlackToGreenToWhite,maps.BlackToGreenToWhite_short,maps.colors]
	mapnames=['maps.BlackToGreen','maps.GreenToWhite','maps.GreenToOrange','maps.BlackToGreenToOrangeToWhite','maps.BlackToGreenToWhite','maps.BlackToGreenToWhite_short','maps.colors']
	fig,axes=plt.subplots(nrows=len(maps), ncols=1)
	fig.set_figheight(20)
	fig.patch.set_facecolor(colors.grey1)
	for ii,m in enumerate(maps):
		for i in np.arange(0,256,1):
			light=np.sum(m(i)[:3])/3
			axes[ii].plot([i],[light], 'o', markersize=30, color=m(i))
		axes[ii].set_xlabel('Colorvalue')
		axes[ii].set_ylabel('Brightness')
		axes[ii].title.set_text(mapnames[ii])
		axes[ii].patch.set_facecolor(colors.grey1)
	plt.tight_layout(pad=3)
	plt.savefig('maps.png',facecolor=fig.get_facecolor(), edgecolor='none')
	plt.show()
'''

import sys 
sys.path.append('O:/200/270_PSM/MitarbeiterInnen/Jan Paschen/PythonJan')
import Fraunhofer_Colors as fhc


sns.boxplot(data=df,x='Group',y='Eta_corr',palette=sns.color_palette([fhc.colors.green1,fhc.colors.orange1]))
fig=plt.gcf()
ax=plt.gca()
fig.patch.set_facecolor(fhc.colors.grey1)
ax.patch.set_facecolor(fhc.colors.grey1)
plt.tight_layout()
plt.savefig('Boxplot_Eta_corr.png',facecolor=fig.get_facecolor(), edgecolor='none')
'''