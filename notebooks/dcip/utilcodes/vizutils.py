from SimPEG import Mesh, Utils
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt

def gettopoCC(mesh, airind):
# def gettopoCC(mesh, airind):
    """
        Get topography from active indices of mesh.
    """
    mesh2D = Mesh.TensorMesh([mesh.hx, mesh.hy], mesh.x0[:2])
    zc = mesh.gridCC[:,2]
    AIRIND = airind.reshape((mesh.vnC[0]*mesh.vnC[1],mesh.vnC[2]), order='F')
    ZC = zc.reshape((mesh.vnC[0]*mesh.vnC[1], mesh.vnC[2]), order='F')
    topo = np.zeros(ZC.shape[0])
    topoCC = np.zeros(ZC.shape[0])
    for i in range(ZC.shape[0]):
        ind  = np.argmax(ZC[i,:][~AIRIND[i,:]])
        topo[i] = ZC[i,:][~AIRIND[i,:]].max() + mesh.hz[~AIRIND[i,:]][ind]*0.5
        topoCC[i] = ZC[i,:][~AIRIND[i,:]].max()
    XY = Utils.ndgrid(mesh.vectorCCx, mesh.vectorCCy)
    return mesh2D, topoCC

def viz(mesh, sigma, ind, airind, normal="Z", ax=None, label="Conductivity (S/m)", scale="log", clim=(-4, -1), xc=0, yc=0,zc=0., cb=True):
    if normal == "Z":
        if ax is None:
            fig = plt.figure(figsize=(5*1.2, 5))
            ax = plt.subplot(111)
    else:
        if ax is None:
            fig = plt.figure(figsize=(5*1.2, 2.5))
            ax = plt.subplot(111)

    temp = sigma.copy()

    if scale == "log":
        temp = np.log10(temp)

    temp[airind] = np.nan

    dat = mesh.plotSlice(temp, ind=ind, clim=clim, normal=normal, grid=False, pcolorOpts={"cmap":"viridis"}, ax=ax)
    if normal == "Z":
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Northing (m)")
        xmin, xmax = -500+xc, 500+xc
        ymin, ymax = -500+yc, 500.+yc
        ax.set_title(("Elevation at %.1f m")%(mesh.vectorCCz[ind]))
    elif normal == "Y":
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Elevation (m)")
        xmin, xmax = -500+xc, 500+xc
        ymin, ymax = -500+zc, 0.+zc
        ax.set_title(("Northing at %.1f m")%(mesh.vectorCCy[ind]))

    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.set_xticks(np.linspace(xmin, xmax, 3))
    ax.set_yticks(np.linspace(ymin, ymax, 3))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # plt.tight_layout()

    if scale == "log":
        cbformat = "$10^{%1.1f}$"
    elif scale == "linear":
        cbformat = "%.1e"

    if clim is None:
        vmin, vmax = dat[0].get_clim()
    else:
        vmin, vmax = clim[0], clim[1]

    if cb:
        cb = plt.colorbar(dat[0], format=cbformat, ticks=np.linspace(vmin, vmax, 3))
        cb.set_label(label)
    # plt.show()
    return ax, dat

def vizEJ(mesh, sigma, ind, f, src, airind, normal="Z", ftype="E", clim=None, xc=0, yc=0,zc=0., ax=None, cb=True):
    if normal == "Z":
        if ax is None:
            fig = plt.figure(figsize=(5*1.2, 5))
            ax = plt.subplot(111)
    else:
        if ax is None:
            fig = plt.figure(figsize=(5*1.2, 2.5))
            ax = plt.subplot(111)

    temp = sigma.copy()
    temp[airind] = np.nan

    if ftype == "E":
        dat=mesh.plotSlice(f[src,'e'], vType="F", view="vec", ind=ind, normal=normal, grid=False, streamOpts={'color':'w'}, pcolorOpts={"cmap":"viridis"}, ax=ax)
        cb_label = "Electric fields (V/m)"
    elif ftype == "phi":
        dat=mesh.plotSlice(f[src,'phi'], ind=ind, normal=normal, pcolorOpts={"cmap":"viridis"}, ax=ax)
        cb_label = "Potential (V)"
    elif ftype == "charg":
        dat=mesh.plotSlice(f[src,'charge'], ind=ind, normal=normal, pcolorOpts={"cmap":"viridis"}, ax=ax)
        cb_label = "Electric charges (C)"
    elif ftype == "J":
        dat=mesh.plotSlice(f[src,'j'], vType="F", view="vec", ind=ind, normal=normal, grid=False, streamOpts={'color':'w'}, pcolorOpts={"cmap":"viridis"}, ax=ax)
        cb_label = "Electric currents (V/m)"
    ax.set_xlabel("Easting (m)")

    cbformat = "%.1e"

    if clim is None:
        vmin, vmax = dat[0].get_clim()
    else:
        vmin, vmax = clim[0], clim[1]

    if cb:
        cb = plt.colorbar(dat[0], format=cbformat, ticks=np.linspace(vmin, vmax, 3))
        cb.set_label(cb_label)

    if normal == "Z":
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Northing (m)")
        xmin, xmax = -700+xc, 700+xc
        ymin, ymax = -700+yc, 700.+yc
        ax.set_title(("Elevation at %.1f m")%(mesh.vectorCCz[ind]))
    elif normal == "Y":
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Elevation (m)")
        xmin, xmax = -700+xc, 700+xc
        ymin, ymax = -700+zc, 0.+zc
        ax.set_title(("Northing at %.1f m")%(mesh.vectorCCy[ind]))


#     ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.set_xticks(np.linspace(xmin, xmax, 3))
#     ax.set_yticks(np.linspace(ymin, ymax, 3))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    return ax, dat
