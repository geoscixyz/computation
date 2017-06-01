# Script to make "simple" geothermal models to show effects of shallow structures.
import numpy as np, sys, os, time, gzip, cPickle as pickle, scipy, gc
from glob import glob
import SimPEG as simpeg
import SimPEG
from SimPEG import NSEM

# Load the solver
#sys.path.append('/tera_raid/gudni')
from pymatsolver import MumpsSolver
# Open files
freqList = np.load('MTfrequencies.npy')
locs = np.load('MTlocations.npy')

# Load the model
mesh, modDict = simpeg.Mesh.TensorMesh.readVTK('nsmesh_CoarseHKPK1_NoExtension.vtr')
sigma = modDict['S/m']
bgsigma = np.ones_like(sigma)*1e-8
bgsigma[sigma > 9.999e-7] = 0.01


# for loc in locs:
#     # NOTE: loc has to be a (1,3) np.ndarray otherwise errors accure
#     for rxType in ['zxxr','zxxi','zxyr','zxyi','zyxr','zyxi','zyyr','zyyi']:
#         rxList.append(simpegNSEM.SurveyNSEM.RxMT(simpeg.mkvc(loc,2).T,rxType))
# Make a receiver list
rxList = []
for rxType in ['zxxr','zxxi','zxyr','zxyi','zyxr','zyxi','zyyr','zyyi','tzxr','tzxi','tzyr','tzyi']:
    rxList.append(NSEM.Rx(locs,rxType))
# Source list
srcList =[]
for freq in freqList:
    srcList.append(NSEM.SrcNSEM.polxy_1Dprimary(rxList,freq))
# Survey MT
survey = NSEM.Survey(srcList)
# Background 1D model
sigma1d = mesh.r(bgsigma,'CC','CC','M')[0,0,:]
## Setup the problem object
problem = NSEM.Problem3D_ePrimSec(mesh,sigmaPrimary = sigma1d)
problem.verbose = True

problem.Solver = MumpsSolver
problem.pair(survey)

## Calculate the fields
stTime = time.time()
print 'Starting calculating field solution at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
sys.stdout.flush()
FmtSer = problem.fields(sigma)
print 'Ended calculation field at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print 'Ran for {:f}'.format(time.time()-stTime)

## Project data
stTime = time.time()
print 'Starting projecting fields to data at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
sys.stdout.flush()
mtData = NSEM.Data(survey,survey.eval(FmtSer))
print 'Ended projection of fields at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print 'Ran for {:f}'.format(time.time()-stTime)
mtStArr = mtData.toRecArray('Complex')
SimPEG.np.save('MTdataStArr_nsmesh_HKPK1Coarse_noExtension',mtStArr)
