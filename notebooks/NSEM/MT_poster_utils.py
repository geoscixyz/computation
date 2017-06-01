import numpy as np
from SimPEG.NSEM.Utils import plotDataTypes as pDt
import matplotlib.pyplot as plt

# Define the area of interest
bw, be = 557100, 557580
bs, bn = 7133340, 7133960
bb, bt = 0,480

#Visualisation of convergences curves
def convergeCurves(resList,ax1,ax2,color1,color2,fontsize):
    its  = np.array([res['iter'] for res in resList]).T
    ind = np.argsort(its)
    phid = np.array([res['phi_d'] for res in resList]).T
    try:
        phim = np.array([res['phi_m'] for res in resList]).T
    except:
        phim = np.array([res['phi_ms'] for res in resList]).T + np.array([res['phi_mx'] for res in resList]).T + np.array([res['phi_my'] for res in resList]).T + np.array([res['phi_mz'] for res in resList]).T     
    x = np.arange(len(its))

    ax1.set_title('Data misfit $\phi_d$ and regularization $\phi_m$',fontsize=fontsize)
    ax1.semilogy(x,phid[ind],'o--',color=color1)
    ax1.set_ylabel('$\phi_d$',fontsize=fontsize)
    ax1.hlines(len(resList[0]['dpred'])*.5,0,len(x),colors='black',linestyles='-.')
    #for tl in ax1.get_yticklabels():
    #    tl.set_color(color1)
         
    ax2.semilogy(x,phim[ind],'x--',color=color2)
    ax2.set_ylabel('$\phi_m$',fontsize=fontsize)
    #for tl in ax2.get_yticklabels():
    #    tl.set_color(color2)
    ax1.set_xlabel('iteration',fontsize=fontsize)
    
    ax1.tick_params(axis='x',labelsize=fontsize)
    ax1.tick_params(axis='y',labelsize=fontsize)
    ax2.tick_params(axis='y',labelsize=fontsize)
    
    return ax1,ax2

def pseudoSect_OffDiagTip_RealImag(dataArray,sectDict,colBarMode='single',cLevel=None):
    '''
    Function that plots psudo sections of difference of real, imaginary and abs of the MT impedance
    '''
    from mpl_toolkits.axes_grid1 import ImageGrid

    fig = plt.figure(1,(15., 9.))
    axes = ImageGrid(fig, (0.05,0.05,0.875,0.875),aspect=False,nrows_ncols = (2, 4),
                     axes_pad = 0.25,add_all=True,share_all=True,label_mode = "L",
                     cbar_mode=colBarMode,cbar_location='right',cbar_pad=0.005)

    [ax.set_yscale('log') for ax in axes]
    n,v = sectDict.items()[0]
    fig.text(0.5,0.96,'Data section at {:.1f} m Northing '.format(v),fontsize=18,ha='center')
    # Plot data
    comps = ['zxy','zxy','zyx','zyx','tzx','tzx','tzy','tzy']
    cTypes = ['real','imag','real','imag','real','imag','real','imag']
    colBs = [True]*8 #[False,False,False,True,False,False,False,True] #
    cLevels = [[1e-1,1e2],[1e-1,1e2],[1e-1,1e2],[1e-1,1e2],
               [1e-3,1e0],[1e-3,1e0],[1e-3,1e0],[1e-3,1e0]]
    csList = []
    for ax, comp, ctype, colB, cLevel in zip(axes,comps,cTypes,colBs,cLevels):
        csList.append(pDt.plotPsudoSectNSimpedance(ax,sectDict,dataArray,comp,ctype,cLevel=cLevel,colorbar=colB))

    [csList[i][1].remove() for i in [0,1,2,4,5,6]]
    ax1 = axes[4]
    ax1.set_xticklabels(np.round((np.array(ax1.get_xticks().tolist(),dtype=int)/100).tolist())/10.)
    # ax1.get_xticklabels().rotation=45 
    axes[0].set_ylabel('Frequency [Hz]')
    ax1.set_ylabel('Frequency [Hz]')
    
    return (fig, axes, csList)

def pseudoSect_FullImpTip_RealImag(dataArray,sectDict,colBarMode='single',cLevel=None):
    '''
    Function that plots psudo sections of difference of real, imaginary and abs of the MT impedance
    '''
    from mpl_toolkits.axes_grid1 import ImageGrid

    fig = plt.figure(1,(15., 13.5))
    axes = ImageGrid(fig, (0.05,0.05,0.875,0.875),aspect=False,nrows_ncols = (3, 4),
                     axes_pad = 0.25,add_all=True,share_all=True,label_mode = "L",
                     cbar_mode=colBarMode,cbar_location='right',cbar_pad=0.005)

    [ax.set_yscale('log') for ax in axes]
    n,v = sectDict.items()[0]
    fig.text(0.5,0.96,'Data section at {:.1f} m Northing '.format(v),fontsize=18,ha='center')
    # Plot data
    comps = ['zxx','zxx','zxy','zxy','zyx','zyx','zyy','zyy','tzx','tzx','tzy','tzy']
    cTypes = ['real','imag','real','imag','real','imag','real','imag','real','imag','real','imag']
    colBs = [True]*12 #[False,False,False,True,False,False,False,True] #
    cLevels = [[1e-1,1e2],[1e-1,1e2],[1e-1,1e2],[1e-1,1e2],
               [1e-1,1e2],[1e-1,1e2],[1e-1,1e2],[1e-1,1e2],
               [1e-3,1e0],[1e-3,1e0],[1e-3,1e0],[1e-3,1e0]]
    csList = []
    for ax, comp, ctype, colB, cLevel in zip(axes,comps,cTypes,colBs,cLevels):
        csList.append(pDt.plotPsudoSectNSimpedance(ax,sectDict,dataArray,comp,ctype,cLevel=cLevel,colorbar=colB))


    [csList[i][1].remove() for i in [0,1,2,4,5,6,8,9,10]]		
    ax1 = axes[4]
    ax1.set_xticklabels(np.round((np.array(ax1.get_xticks().tolist(),dtype=int)/100).tolist())/10.)
    ax1.get_xticklabels().rotation=45 
    axes[0].set_ylabel('Frequency [Hz]')
    axes[4].set_ylabel('Frequency [Hz]')
    axes[8].set_ylabel('Frequency [Hz]')
    
    return (fig, axes, csList)


def CompareInversion(mesh,sigma,siginvoff,siginvtip,slice_ver,slice_hor):
	
	vmin,vmax=-4,-1.3
	ticksize=14
	fontsize=14
	titlesize=16

	
	fig = plt.figure(figsize=(15,10))
	ax0=plt.subplot2grid((12,18), (0, 0),colspan=6,rowspan=6)
	#ax4=plt.subplot2grid((10,12),(0,11),colspan=1,rowspan=10)
	#ax0 = plt.subplot(221)
	model = sigma.reshape(mesh.vnC,order='F')
	mask0 = np.ma.masked_where(model==1e-8,model)
	
	a = ax0.pcolormesh(mesh.gridCC[:,0].reshape(mesh.vnC,order='F')[:,slice_ver,:],
	                   mesh.gridCC[:,2].reshape(mesh.vnC,order='F')[:,slice_ver,:],np.log10(mask0[:,slice_ver,:]),
	                   edgecolor='k',cmap='viridis')
	    
	
	ax0.set_xlim([bw,be])
	ax0.set_ylim([0,bt])
	ax0.set_aspect("equal")
	
	ax0.set_ylabel(("at %1.0f m Northing \n Elevation (m)")%(np.unique(mesh.gridCC[:,1].reshape(mesh.vnC,order='F')[:,slice_ver,:])[0]),fontsize=titlesize)
	ax0.set_title("True Model",fontsize=titlesize)
	
	ax0.set_xticklabels([])
	
	ax0.set_yticks([0,200,400])
	ax0.tick_params(axis='y', labelsize=ticksize)
	
	ax1=plt.subplot2grid((12,18), (0, 6),colspan=6,rowspan=6)
	
	sinv = siginvoff.reshape(mesh.vnC,order='F')
	mask1= np.ma.masked_where(sinv<=9.9e-7,sinv)
	
	b = ax1.pcolormesh(mesh.gridCC[:,0].reshape(mesh.vnC,order='F')[:,slice_ver,:],
	                   mesh.gridCC[:,2].reshape(mesh.vnC,order='F')[:,slice_ver,:],np.log10(mask1[:,slice_ver,:]),
	                   edgecolor='k',cmap='viridis',vmin=vmin,vmax=vmax)
	
	ax1.set_xlim([bw,be])
	ax1.set_ylim([0,bt])
	ax1.set_aspect("equal")
	ax1.set_yticklabels([])
	ax1.set_title(("Off-diagonal \n Recovered Model")%(np.unique(mesh.gridCC[:,1].reshape(mesh.vnC,order='F')[:,slice_ver,:])[0]),fontsize=titlesize)
	ax1.set_xticklabels([])
	
	ax2=plt.subplot2grid((12,18), (6, 0),colspan=6,rowspan=6)
	#ax2 = plt.subplot(223)
	
	
	#print np.unique(mesh.gridCC[:,2].reshape(mesh.vnC,order='F')[:,:,slice])
	
	c = ax2.pcolormesh(mesh.gridCC[:,0].reshape(mesh.vnC,order='F')[:,:,slice_hor],mesh.gridCC[:,1].reshape(mesh.vnC,order='F')[:,:,slice_hor],
	                   np.log10(model[:,:,slice_hor]),edgecolor='k',cmap='viridis',vmin=vmin,vmax=vmax)
	
	ax2.set_xlim([bw,be])
	ax2.set_ylim([bs,bn])
	ax2.set_aspect("equal")
	ax2.set_xticks([bw,(bw+be)/2,be-80])
	ax2.set_xticklabels([bw,(bw+be)/2,be-80])
	ax2.set_xticklabels(np.round((np.array(ax2.get_xticks().tolist(),dtype=float)/100).tolist())/10)
	ax2xlabels=ax2.get_xticklabels()
	for label in ax2xlabels:
	    label.set_rotation(45)
	    
	ax2.set_yticks([7133400,7133600,7133800])
	ax2.set_yticklabels([400,600,800])
	ax2.tick_params(axis='y', labelsize=ticksize)
	
	ax2.set_xlabel("Easting (km)",fontsize=fontsize)
	ax2.set_ylabel(("at %1.0f m Elevation \n Northing 7133km+(m)")%(np.unique(mesh.gridCC[:,2].reshape(mesh.vnC,order='F')[:,:,slice_hor])[0]),fontsize=titlesize)
	
	ax3=plt.subplot2grid((12,18), (6, 6),colspan=6,rowspan=6)
	
	d = ax3.pcolormesh(mesh.gridCC[:,0].reshape(mesh.vnC,order='F')[:,:,slice_hor],mesh.gridCC[:,1].reshape(mesh.vnC,order='F')[:,:,slice_hor],
	                   np.log10(sinv[:,:,slice_hor]),edgecolor='k',cmap='viridis',vmin=vmin,vmax=vmax)
	
	ax3.set_xlim([bw,be])
	ax3.set_ylim([bs,bn])
	ax3.set_aspect("equal")
	
	ax3.set_xticks([bw,(bw+be)/2,be-80])
	ax3.set_xticklabels([bw,(bw+be)/2,be-80])
	ax3.set_xticklabels(np.round((np.array(ax3.get_xticks().tolist(),dtype=float)/100).tolist())/10)
	
	ax3xlabels=ax3.get_xticklabels()
	for label in ax3xlabels:
	    label.set_rotation(45)
	    
	ax3.set_yticklabels([])
	ax3.set_xlabel("Easting (km)",fontsize=fontsize)
	
	fig.subplots_adjust(right=0.9)
	cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
	cbar = plt.colorbar(c, cax=cbar_ax)
	cbar.set_label("Conductivity (S/m)",fontsize=titlesize)
	cbar.set_ticks([-4,-3,-2,-1.3])
	cbar.set_ticklabels(['1e-4','1e-3','1e-2','5e-2'])
	
	sinvtip = siginvtip.reshape(mesh.vnC,order='F')
	mask2= np.ma.masked_where(sinvtip<=9.9e-7,sinvtip)
	
	ax4=plt.subplot2grid((12,18), (0, 12),colspan=6,rowspan=6)
	
	e = ax4.pcolormesh(mesh.gridCC[:,0].reshape(mesh.vnC,order='F')[:,slice_ver,:],
	                   mesh.gridCC[:,2].reshape(mesh.vnC,order='F')[:,slice_ver,:],np.log10(mask2[:,slice_ver,:]),
	                   edgecolor='k',cmap='viridis',vmin=vmin,vmax=vmax)
	
	ax4.set_xlim([bw,be])
	ax4.set_ylim([0,bt])
	ax4.set_aspect("equal")
	ax4.set_yticklabels([])
	ax4.set_title(("Tipper \n Recoverered Model")%(np.unique(mesh.gridCC[:,1].reshape(mesh.vnC,order='F')[:,slice_ver,:])[0]),fontsize=titlesize)
	ax4.set_xticklabels([])
	
	ax5=plt.subplot2grid((12,18), (6, 12),colspan=6,rowspan=6)
	
	
	f = ax5.pcolormesh(mesh.gridCC[:,0].reshape(mesh.vnC,order='F')[:,:,slice_hor],mesh.gridCC[:,1].reshape(mesh.vnC,order='F')[:,:,slice_hor],
	                   np.log10(mask2[:,:,slice_hor]),edgecolor='k',cmap='viridis',vmin=vmin,vmax=vmax)
	
	ax5.set_xlim([bw,be])
	ax5.set_ylim([bs,bn])
	ax5.set_aspect("equal")
	
	ax5.set_xticks([bw,(bw+be)/2,be])
	ax5.set_xticklabels([bw,(bw+be)/2,be])
	ax5.set_xticklabels(np.round((np.array(ax5.get_xticks().tolist(),dtype=float)/100).tolist())/10)
	
	ax5xlabels=ax5.get_xticklabels()
	for label in ax5xlabels:
	    label.set_rotation(45)
	
	ax5.set_yticklabels([])
	
	
	ax5.set_xlabel("Easting (km)",fontsize=fontsize)
	
	for ax in [ax0,ax1,ax2,ax3,ax4,ax5,cbar.ax]:
	    ax.tick_params(axis='y', labelsize=ticksize)
	    ax.tick_params(axis='x', labelsize=ticksize)
	
	
	plt.show()
	