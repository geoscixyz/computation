from SimPEG import Mesh, Utils, np, Maps, Survey
from SimPEG.EM.Static import DC, IP
import warnings
import sys
sys.path.append("./utilcodes/")
from vizutils import gettopoCC, viz, vizEJ

from SimPEG import (DataMisfit, Regularization, Optimization, Directives,
                    InvProblem, Inversion)
import pickle

try:
    from pymatsolver import MumpsSolver
    solver = MumpsSolver
except ImportError, e:
    from SimPEG import SolverLU
    warnings.warn('Mumps solver not installed. Using SolverLU... will be '
                  'slower. To install Mumps, see '
                  'https://github.com/rowanc1/pymatsolver')
    solver = SolverLU

# Setup tensor mesh

# Core cell sizes in x, y, and z
csx, csy, csz = 25., 25., 25.
# Number of core cells in each direction
ncx, ncy, ncz = 48, 48, 20
# Number of padding cells to add in each direction
npad = 7
# Vectors of cell lengthts in each direction
hx = [(csx,npad, -1.3),(csx,ncx),(csx,npad, 1.3)]
hy = [(csy,npad, -1.3),(csy,ncy),(csy,npad, 1.3)]
hz = [(csz,npad, -1.3),(csz,ncz), (csz/2.,6)]
# Create mesh
mesh = Mesh.TensorMesh([hx, hy, hz],x0="CCN")
# Map mesh coordinates from local to UTM coordiantes
xc = 300+5.57e5
yc = 600+7.133e6
zc = 425.
mesh._x0 = mesh.x0 + np.r_[xc, yc, zc]

# Load synthetic conductivity model matching the designated mesh
sigma = mesh.readModelUBC("VTKout_DC.dat")
# Identify air cells in the model
airind = sigma == 1e-8

# Obtain topographic surface from 3D conductivity model
mesh2D, topoCC = gettopoCC(mesh, airind)


# Setup gradient array survey

# Define the source electrode locations
# Here we use a single dipole source (A-B electrode) in the x-direction)
Aloc1_x = np.r_[-600., 0, 0.] + np.r_[xc, yc, zc]
Bloc1_x = np.r_[600., 0, 0.] + np.r_[xc, yc, zc]

# Rx locations (M-N electrodes, x-direction)
# Find x and y cell centres in the interior portion of the mesh
x = mesh.vectorCCx[np.logical_and(mesh.vectorCCx>-300.+ xc, mesh.vectorCCx<300.+ xc)]
y = mesh.vectorCCy[np.logical_and(mesh.vectorCCy>-300.+ yc, mesh.vectorCCy<300.+ yc)]
# Grid selected cell centres to get M and N Rx electrode locations
Mx = Utils.ndgrid(x[:-1], y, np.r_[-12.5/2.])
Nx = Utils.ndgrid(x[1:], y, np.r_[-12.5/2.])
# Get cell ind for electrode locations to extract electrode elevation from topoCC
inds_Mx = Utils.closestPoints(mesh2D, Mx[:,:2])
inds_Nx = Utils.closestPoints(mesh2D, Nx[:,:2])
# Draped M and N electrode x,y,z locations
Mx_dr = np.c_[Mx[:,0], Mx[:,1], topoCC[inds_Mx]]
Nx_dr = np.c_[Nx[:,0], Nx[:,1], topoCC[inds_Nx]]

# Create Src and Rx classes for DC problem
rx_x = DC.Rx.Dipole(Mx_dr, Nx_dr)
src1 = DC.Src.Dipole([rx_x], Aloc1_x, Bloc1_x)

# Setup mappings
# Inversion model is log conductivity in the subsurface. This can be realized as a following mapping:
expmap = Maps.ExpMap(mesh) # from log conductivity to conductivity
actmap = Maps.InjectActiveCells(mesh, ~airind, np.log(1e-8)) # from subsurface cells to full3D cells
mapping = expmap*actmap


# Create inital and reference model (1e-4 S/m)
m0 = np.ones_like(sigma)[~airind]*np.log(1e-4)

# Form survey object using Srcs and Rxs that we have generated
survey = DC.Survey([src1])
# Define problem and set solver
problem = DC.Problem3D_CC(mesh, mapping=mapping)
problem.Solver = solver
# Pair problem and survey
problem.pair(survey)

# Define true model based on mapping
mtrue = np.log(sigma)[~airind]

# Forward model fields due to the reference model and true model
f0 = problem.fields(m0)
f = problem.fields(mtrue)

# Get observed data
dobs = survey.dpred(mtrue, f=f)

# Compute secondary potential
phi_sec = f[src1, "phi"] - f0[src1, "phi"]


# Inversion

# Depth weighting
depth = 1./(abs(mesh.gridCC[:,2]-zc))**1.5
depth = depth/depth.max()

# Setup inversion object
regmap = Maps.IdentityMap(nP=m0.size)
# Assign uncertainties
std = 0.05
eps = 1e-3
survey.std = std
survey.eps = eps
survey.dobs = dobs
# Define datamisfit portion of objective function
dmisfit = DataMisfit.l2_DataMisfit(survey)
# Define regulatization (model objective function)
reg = Regularization.Simple(mesh, mapping=regmap, indActive=~airind)
reg.wght = depth[~airind]
opt = Optimization.InexactGaussNewton(maxIter = 20)
invProb = InvProblem.BaseInvProblem(dmisfit, reg, opt)
# Define inversion parameters
beta = Directives.BetaSchedule(coolingFactor=5, coolingRate=2)
betaest = Directives.BetaEstimate_ByEig(beta0_ratio=1e0)
save = Directives.SaveOutputEveryIteration()
savemodel = Directives.SaveModelEveryIteration()
target = Directives.TargetMisfit()
inv = Inversion.BaseInversion(invProb, directiveList=[beta,betaest, save, target, savemodel])
reg.alpha_s = 1e-1
reg.alpha_x = 1.
reg.alpha_y = 1.
reg.alpha_z = 1.
problem.counter = opt.counter = Utils.Counter()
opt.LSshorten = 0.5
opt.remember('xc')

# Run inversion
mopt = inv.run(m0)

# Apply mapping to model to get and save recovered conductivity
sigopt = mapping*mopt
# np.save("sigest_singlesrc_withdweights", sigopt)

# Calculate dpred
dpred = survey.dpred(np.log(sigopt[~airind]))

# Pickle results for easy access
Results = {"sigma_true":sigma, "sigma_inv":sigopt, "Obs":dobs, "Pred":dpred}
outputs = open("DCresults", 'wb')
pickle.dump(Results, outputs)
outputs.close()


