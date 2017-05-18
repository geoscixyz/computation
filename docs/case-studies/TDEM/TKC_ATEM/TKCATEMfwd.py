import numpy as np
import cPickle as pickle
from scipy.constants import mu_0
from pymatsolver import PardisoSolver as Solver
from SimPEG import EM, Mesh, Maps, Utils

download_dir = '.'  # name of the local directory to create and put the files in.

root_url = 'https://storage.googleapis.com/simpeg/tkc_synthetic/atem/'
files = ['TKCATEMexample.p']
urls = [root_url + f for f in files]

downloads = Utils.download(url=urls, folder=download_dir, overwrite=True)
downloads = dict(zip(['fwd_params'], downloads))  # create a dict

TKCATEMexample = pickle.load(open(downloads['fwd_params'], "rb"))

mesh = TKCATEMexample["mesh"]
sigma = TKCATEMexample["sigma"]
xyz = TKCATEMexample["xyz"]
ntx = xyz.shape[0]

# TDEM Survey
srcLists = []
times = np.logspace(-4, np.log10(2e-3), 10)
for itx in range(ntx):
    rx = EM.TDEM.Rx.Point_b(
        xyz[itx, :].reshape([1, -1]), times, orientation='z'
    )
    src = EM.TDEM.Src.CircularLoop(
        [rx], waveform=EM.TDEM.Src.StepOffWaveform(),
        loc=xyz[itx, :].reshape([1, -1]), radius=13.
    )
    srcLists.append(src)

# TDEM Problem
survey = EM.TDEM.Survey(srcLists)
problem = EM.TDEM.Problem3D_b(
    mesh, verbose=False, sigmaMap=Maps.IdentityMap(mesh)
)
timeSteps = [(1e-5, 5), (1e-4, 10), (5e-4, 10)]
problem.timeSteps = timeSteps
problem.pair(survey)
problem.Solver = Solver

# Simulate
dpred = survey.dpred(sigma)
TKCATEMexample = {
    "mesh": mesh, "sigma": sigma, "xyz": xyz, "ntx": tx,
    "times": times, "timeSteps": problem.timeSteps, "dpred": dpred
}
pickle.dump(
    TKCATEMexample, open(download_dir + "/TKCATEMfwd.p", "wb" )
)
