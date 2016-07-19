.. _PF_MAG:

Potential Fields (Magnetics)
============================




Setup
-----
Maxwell's equations for a static electric field and in the absence of free-currents can be written as:

:math:`\nabla \cdot \mathbf{B} = 0 \\ \nabla \times \mathbf{H} = 0`

where :math:`\mathbf{B}` and :math:`\mathbf{H}` correspond to the magnetic
flux density and magnetic field respectively. Both quantities are related by:

:math:`\mathbf{B} = \mu \mathbf{H} \\ \mu = \mu_0 ( 1 + \kappa )`

where :math:`\mu` is the magnetic permeability. In free-space, both
:math:`\mathbf{B}` and :math:`\mathbf{H}` are linearly related by the magnetic
permealitity of free-space :math:`\mu_0`. In matter however, the magnetic flux
can be increased proportionally on how easily magnetic material gets
polarized, quantified by the magnetic susceptibility :math:`\kappa`. In a
macroscopic point of view, the magnetic property of matter are generally
described in terms of magnetization per unit volume such that:

:math:`\mathbf{M} = \kappa \mathbf{H_s + H_0} + M_r`

While :math:`\mathbf{M}` can be oriented in any specific direction due to
secondary local fields (:math:`\mathbf{H_s}`) and/or due to permanent dipole
moments (:math:`\mathbf{M_r}`). For simplicity we will here assume a purely
induced response due to the Earth's :math:`\mathbf{H_0}`. Using a few vector
identities, we can re-write the magnetic field due to magnetized material in
terms of a scalar potential:

:math:`\phi = \frac{1}{4\pi}  \int_{V}    \nabla \left(\frac{1}{r}\right) \cdot \mathbf{H}_0 \kappa  \; dV`

where :math:`r` defines the relative position between an observer and the
magnetic source. Taking the divergence of this potential yields:

:math:`\mathbf{b} = \frac{\mu_0}{4\pi}  \int_{V}  \nabla \nabla \left(\frac{1}{r}\right) \cdot \mathbf{H}_0 \kappa \; dV`

Great, we have a general expression relating any secondary magnetic flux due to
magnetic material

Forward Problem
---------------

Assuming a purely induced response, we can solve the integral analytically. As
derived by Sharma (1966), the integral can be evaluated for rectangular prisms
such that:

:math:`\mathbf{b} =  \mathbf{T} \cdot \mathbf{H}_0 \; \kappa`

Where the tensor matrix :math:`\bf{T}` relates the vector magnetization
:math:`\mathbf{M}` inside a single cell to the components of the field
:math:`\mathbf{b}` observed at a given location:

:math:`\mathbf{T} = \begin{pmatrix} T_{xx} & T_{xy} & T_{xz}    \\ T_{yx} &
T_{yy} & T_{yz}    \\ T_{zx} & T_{zy} & T_{zz} \end{pmatrix}`

In general, we discretize the earth into a collection of cells, each
contributing to the magnetic data such that giving rise to a large and dense
linear system of the form:

:math:`\mathbf{b} = \sum_{j=1}^{nc} \mathbf{T}_j \cdot \mathbf{H}_0 \; \kappa_j`

In most geophysical surveys, we are not collecting all three components, but
rather the magnitude of the field, or *Total Magnetic Intensity* (TMI) data.
Because the inducing field is really large, we will assume that the anomalous
fields are parallel to :math:`H_0`:

:math:`d^{TMI}  = \mathbf{\hat H}_0 \cdot \mathbf{b}`

We then end up with a much smaller system:

:math:`d^{TMI} = \mathbf{F\; \kappa}`

where :math:`\mathbf{F} \in \mathbb{R}^{nd \times nc}` is our *forward*
operator and :math:`\kappa` is the physical property describing the Earth.


Getting started
^^^^^^^^^^^^^^^

In order to define a geophysical experiment we need set important spatial
parameters, such as mesh and data location, as well as inversion parameters.
While we could set all of those parameters manually, SimPEG.PF gives the
option to work with an input file capturing all the necessary information to
run the inversion workflow. In preparation for this synthetic example,
we prepared all necessary files and added them to a working directory.
The input file looks like this:



.. exec::

    import SimPEG
    import SimPEG.PF as PF
    import os
    import sys

    sys.path.insert(0, os.path.abspath('.'))

    print os.getcwd()
    #driver = PF.MagneticsDriver.MagneticsDriver_Inv("./stories/SimPEG_PF_Input.inp")
    #mesh = driver.mesh
    #survey = driver.survey

    #print mesh.nC

and a reproducible plot


Model and Mapping
^^^^^^^^^^^^^^^^^

What is your model?


Fields
^^^^^^



Data
^^^^


Inverse Problem
---------------

Data Misfit
^^^^^^^^^^^

Regularization
^^^^^^^^^^^^^^

Inverse Problem
^^^^^^^^^^^^^^^

Optimization
^^^^^^^^^^^^

Inversion
^^^^^^^^^
