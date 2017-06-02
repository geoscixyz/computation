from SimPEG import (
    Problem, Utils, Maps, Props, Mesh, Tests, Survey, Solver as SimpegSolver
    )
import numpy as np
import scipy.sparse as sp
import properties
from scipy.constants import mu_0


class MT1DSurvey(Survey.BaseSurvey):

    def __init__(self, srcList, **kwargs):
        self.srcList = srcList
        Survey.BaseSurvey.__init__(self, **kwargs)
        self.getUniqFrequency()

    @property
    def nFreq(self):
        if getattr(self, '_nFreq', None) is None:
            self._nFreq = len(self.frequency)
        return self._nFreq

        self.getUniqueTimes()

    def getUniqFrequency(self):
        frequency_rx = []

        rxcount = 0
        for src in self.srcList:
            for rx in src.rxList:
                frequency_rx.append(rx.frequency)
                rxcount += 1
        freqs_temp = np.hstack(frequency_rx)
        self.frequency = np.unique(freqs_temp)

        # TODO: Generalize this so that user can omit specific datum at
        # certain frequencies
        if (len(freqs_temp) != rxcount * self.nFreq):
            raise Exception("# of Frequency of each Rx should be same!")

    @property
    def P0(self):
        """
            Evaluation matrix at surface
        """
        if getattr(self, '_P0', None) is None:
            P0 = sp.coo_matrix(
                (
                    np.r_[1.], (np.r_[0], np.r_[2*self.mesh.nC])),
                shape=(1, 2 * self.mesh.nC + 1)
                )
            self._P0 = P0.tocsr()
        return self._P0

    def eval(self, f):
        """
        Project fields to receiver locations

        :param Fields f: fields object
        :rtype: numpy.ndarray
        :return: data
        """
        data = Survey.Data(self)
        for src in self.srcList:
            for rx in src.rxList:
                data[src, rx] = rx.eval(src, f, self.P0)
        return data

    def evalDeriv(self):
        raise Exception('Use Receivers to project fields deriv.')

    def setMesh(self, sigma=0.1, max_depth_core=3000., ncell_per_skind=10, n_skind=2):

        """
        Set 1D Mesh based using skin depths

        """
        rho = 1./sigma
        fmin, fmax = self.frequency.min(), self.frequency.max()

        print (
            (">> Smallest cell size = %d m") % (500*np.sqrt(rho/fmax) / ncell_per_skind)
            )
        print (
            (">> Padding distance = %d m") % (500*np.sqrt(rho/fmin) * n_skind)
            )
        cs = 500*np.sqrt(rho/fmax) / ncell_per_skind
        length_bc = 500*np.sqrt(100/fmin) * n_skind

        npad = 1
        blength = cs*1.3**(np.arange(npad)+1)
        while blength < length_bc:
            npad += 1
            blength = (cs*1.3**(np.arange(npad)+1)).sum()
        print (
            (">> # of padding cells %d") % (npad)
            )

        ncz = int(max_depth_core / cs)
        hz = [(cs, npad, -1.3), (cs, ncz)]
        mesh = Mesh.TensorMesh([hz], x0='N')

        return mesh


class MT1DSrc(Survey.BaseSrc):
    """
    Source class for MT1D
    We assume a boundary condition of Ex (z=0) = 1
    """
    loc = np.r_[0.]


class ZxyRx(Survey.BaseRx):

    def __init__(self, locs, component=None, frequency=None, rxType=None):
        self.component = component
        self.frequency = frequency
        Survey.BaseRx.__init__(self, locs, rxType=None)

    def eval(self, src, f, P0):
        Zxy = - 1./(P0*f)
        if self.component == "real":
            return Zxy.real
        elif self.component == "imag":
            return Zxy.imag

    @property
    def nD(self):
        return len(self.frequency)


class AppResRx(ZxyRx):

    def __init__(self, locs, component=None, frequency=None):
        super(AppResRx, self).__init__(locs, component, frequency)

    def eval(self, src, f, P0):
        Zxy = - 1./(P0*f)
        omega = 2*np.pi*self.frequency
        return abs(Zxy)**2 / (mu_0*omega)

    # def evalDeriv(self, mesh, f, v=None, adjoint=False):


class PhaseRx(ZxyRx):

    def __init__(self, locs, component=None, frequency=None):
        super(PhaseRx, self).__init__(locs, component, frequency)

    def eval(self, src, f, P0):
        Zxy = - 1./(P0*f)
        return np.rad2deg(np.arctan(Zxy.imag / Zxy.real))

    # def evalDeriv(self, mesh, f, v=None, adjoint=False):


class MT1DProblem(Problem.BaseProblem):
    """
    1D Magnetotelluric problem under quasi-static approximation

    """

    sigma, sigmaMap, sigmaDeriv = Props.Invertible(
        "Electrical conductivity (S/m)"
    )

    rho, rhoMap, rhoDeriv = Props.Invertible(
        "Electrical resistivity (Ohm-m)"
    )

    Props.Reciprocal(sigma, rho)

    mu = Props.PhysicalProperty(
        "Magnetic Permeability (H/m)",
        default=mu_0
    )

    surveyPair = Survey.BaseSurvey  #: The survey to pair with.
    dataPair = Survey.Data  #: The data to pair with.

    mapPair = Maps.IdentityMap  #: Type of mapping to pair with

    Solver = SimpegSolver  #: Type of solver to pair with
    solverOpts = {}  #: Solver options

    verbose = False
    Ainv = None
    ATinv = None
    f = None

    def __init__(self, mesh, **kwargs):
        Problem.BaseProblem.__init__(self, mesh, **kwargs)
        # Setup boundary conditions
        mesh.setCellGradBC([['dirichlet', 'dirichlet']])

    @property
    def deleteTheseOnModelUpdate(self):
        toDelete = []
        if self.sigmaMap is not None or self.rhoMap is not None:
            toDelete += ['_MccSigma']
        return toDelete

    @property
    def Exbc(self):
        """
            Boundary value for Ex
        """
        if getattr(self, '_Exbc', None) is None:
            self._Exbc = np.r_[0., 1.]
        return self._Exbc

    ####################################################
    # Mass Matrices
    ####################################################

    @property
    def MccSigma(self):
        """
        Diagonal matrix for \\(\\sigma\\).
        """
        if getattr(self, '_MccSigma', None) is None:
            self._MccSigma = Utils.sdiag(self.sigma)
        return self._MccSigma

    @property
    def MccEpsilon(self):
        """
        Diagonal matrix for \\(\\epsilon\\).
        """
        if getattr(self, '_MccEpsilon', None) is None:
            self._MccEpsilon = Utils.sdiag(self.epsilon)
        return self._MccEpsilon

    @property
    def MfMu(self):
        """
        Edge inner product matrix for \\(\\mu\\).
        """
        if getattr(self, '_MMfMu', None) is None:
            self._MMfMu = Utils.sdiag(
                self.mesh.aveF2CC.T * self.mu * np.ones(self.mesh.nC)
                )
        return self._MMfMu

    ####################################################
    # Physics?
    ####################################################

    def getA(self, freq):
        """
            .. math::

                \mathbf{A} =
                \begin{bmatrix}
                    \mathbf{Grad} & \imath \omega \mathbf{M}^{f2cc}_{\mu} \\[0.3em]
                   \mathbf{M}^{cc}_{\hat{\sigma}} & \mathbf{Div}           \\[0.3em]
                \end{bmatrix}

        """

        Div = self.mesh.faceDiv
        Grad = self.mesh.cellGrad
        omega = 2*np.pi*freq
        A = sp.vstack(
            (sp.hstack(
                (Grad, 1j*omega*self.MfMu)), sp.hstack((self.MccSigma, Div))
            )
        )
        return A

    # def getADeriv_sigma(self, freq, u, v, adjoint=False):
    #     return ADeriv_sigma

    def getRHS(self, freq):
        """
            .. math::

                \mathbf{rhs} =
                \begin{bmatrix}
                     - \mathbf{B}\mathbf{E}_x^{bc} \\ [0.3em]
                    \boldsymbol{0} \\[0.3em]
                \end{bmatrix}$

        """
        B = self.mesh.cellGradBC
        RHS = np.r_[-B*self.Exbc, np.zeros(self.mesh.nC)]
        return RHS

    def fields(self, m=None):
        self.Ainv = []
        f = np.zeros(
            (int(self.mesh.nC*2+1), self.survey.nFreq), dtype="complex"
            )
        for ifreq, freq in enumerate(self.survey.frequency):
            A = self.getA(freq)
            self.Ainv.append(self.Solver(A))
            f[:, ifreq] = self.Ainv[ifreq] * self.getRHS(freq)
        return f

    # def Jvec(self, m, v, f=None):
    #     return Jvec

    # def Jtvec(self, m, v, f=None):
    #     return Jtvec
