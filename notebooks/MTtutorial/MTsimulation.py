import numpy as np
import scipy.sparse as sp

def app_res_phase(Zxy):
    """
    compute apparent resistivity and phase given an impedance
    """
    app_res = abs(Zxy)**2 / (mu_0*omega)
    app_phase = np.rad2deg(np.arctan(Zxy.imag / Zxy.real))

    return app_res, app_phase

def MTsimulation(mesh, sigma, frequency, rtype="app_res"):
    """
       Compute apparent resistivity and phase at each frequency. 
       Return apparent resistivity and phase for rtype="app_res",
       or impedance for rtype="impedance" 
    """
    
    omega = 2*np.pi*frequency # Angular frequency (rad/s)
    
    # Grad 
    mesh.setCellGradBC([['dirichlet', 'dirichlet']]) # Setup boundary conditions
    Grad = mesh.cellGrad # Gradient matrix

    # MfMu
    Mmu = Utils.sdiag(mesh.aveCC2F * mu) 

    # Mccsigma
    Msighat = Utils.sdiag(sigmahat) 

    # Div
    Div = mesh.faceDiv # Divergence matrix

    # Right Hand Side
    B = mesh.cellGradBC  # a matrix for boundary conditions
    Exbc = np.r_[0., 1.] # boundary values for Ex
    
    # A-matrix
    A = sp.vstack([
        sp.hstack([Grad, 1j*omega*Mmu]), # Top row of A matrix
        sp.hstack((Msighat, Div)) # Bottom row of A matrix
    ])

    # Right-hand side
    rhs = np.r_[
        -B*Exbc, 
        np.zeros(mesh.nC)
    ] 
    
    Ainv = Solver(A) # Factorize A matrix
    sol = Ainv*rhs   # Solve A^-1 rhs = sol
    Ex = sol[:mesh.nC] # Extract Ex from solution vector u
    Hy = sol[mesh.nC:mesh.nC+mesh.nN] # Extract Hy from solution vector u

    Zxy = - 1./Hy[-1] # Impedance at the surface
    
    if rtype.lower() == "impedance":
        return Zxy

    elif rtype.lower() == "app_res":
        return app_res_phase(Zxy)
    
    else:
        raise Exception, "rtype must be 'impedance' or 'app_res', not {}".format(rtype.lower())