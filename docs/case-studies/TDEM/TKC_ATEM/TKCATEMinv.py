import numpy as np
from pymatsolver import Pardiso as Solver

from SimPEG import EM, Mesh, Utils, Maps
from SimPEG import DataMisfit, Regularization, Optimization, Directives, InvProblem, Inversion
from scipy.constants import mu_0
import cPickle as pickle

TKCATEMexample = pickle.load( open( "./TKCATEMfwd.p", "rb" ) )

mesh = TKCATEMexample["mesh"]
sigma = TKCATEMexample["sigma"]
xyz = TKCATEMexample["xyz"]
times = TKCATEMexample["times"]
# timeSteps = TKCATEMexample["timeSteps_inv"]
ntx = TKCATEMexample["ntx_ds"]
dobs = TKCATEMexample["dobs_ds"]
perc, floor = TKCATEMexample["perc"], TKCATEMexample["floor"]

# TDEM Survey
srcLists = []
times = np.logspace(-4, np.log10(2e-3), 10)
for itx in range(ntx):
    rx = EM.TDEM.Rx.Point_b(xyz[itx,:].reshape([1,-1]), times, orientation='z')
    src = EM.TDEM.Src.CircularLoop([rx], waveform=EM.TDEM.Src.StepOffWaveform(), loc=xyz[itx,:].reshape([1,-1]), radius = 13.) # same src location as FDEM problem
    srcLists.append(src)

# TDEM Problem
survey = EM.TDEM.Survey(srcLists)
airind = sigma == 1e-8
expmap = Maps.ExpMap(mesh)
actmap = Maps.InjectActiveCells(mesh, ~airind, np.log(1e-8))
mapping = expmap*actmap
m0 = np.ones_like(sigma)[~airind]*np.log(1e-4)

problem = EM.TDEM.Problem_b(mesh, sigmaMap=mapping)
timeSteps = [(1e-5, 5), (1e-4, 10), (5e-4, 10)]
problem.timeSteps = timeSteps
problem.pair(survey)
problem.Solver = Solver

regmap = Maps.IdentityMap(nP=m0.size)
survey.std = perc
survey.eps = floor
survey.dobs = dobs
dmisfit = DataMisfit.l2_DataMisfit(survey)
reg = Regularization.Simple(mesh, mapping=regmap, indActive=~airind)
opt = Optimization.InexactGaussNewton(maxIter = 20)
invProb = InvProblem.BaseInvProblem(dmisfit, reg, opt)

# Create an inversion object
beta = Directives.BetaSchedule(coolingFactor=5, coolingRate=2)
betaest = Directives.BetaEstimate_ByEig(beta0_ratio=1e0)
save = Directives.SaveOutputEveryIteration()
save_model = Directives.SaveModelEveryIteration()
target = Directives.TargetMisfit()
inv = Inversion.BaseInversion(invProb, directiveList=[beta, betaest, save, save_model,  target])
reg.alpha_s = 1e-2
reg.alpha_x = 1.
reg.alpha_y = 1.
reg.alpha_z = 1.
problem.counter = opt.counter = Utils.Counter()
opt.LSshorten = 0.5

mopt = inv.run(m0)
sigopt = mapping*mopt

np.save("sigest", sigopt)
np.save("dpred", invProb.dpred)
