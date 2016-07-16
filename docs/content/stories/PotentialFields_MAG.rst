.. _PotentialFields_MAG:

Potential Fields (Magnetics)
============================

.. topic:: Purpose

    In this tutorial we will create a simple magnetic problem from scratch
using the SimPEG framework.  The synthetic example used is based on the TKC
kimberlite deposit, Northwest Territories. We are attempting to use the
magnetic field to image the various rock units making up the diamond deposit.
The approach is general and can be applied to any geological situation
involving magnetic susceptible rocks.

The code for this story is available in the SimPEG examples
- github path to SimPEG Example:
- github path to notebook:


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

:math:`\mathbf{M} = \kappa \mathbf{H}`

Using a few vector identities, we can re-write the
secondary magnetic field due to magnetized material in terms of a potential:

:math:`\phi = \frac{1}{4\pi}  \int_{V}    \nabla \left(\frac{1}{r}\right) \cdot \mathbf{M}  \; dV`

where :math:`r` defines the relative position between an observer and the
magnetic source. Taking the divergence of this potential yields:

:math:`\mathbf{b} = \frac{\mu_0}{4\pi}  \int_{V}  \nabla \nabla \left(\frac{1}{r}\right) \cdot \mathbf{M} \; dV`

While :math:`\mathbf{M}` can be oriented in any specific direction due to
secondary local fields and/or permanent dipole moments (remanence), for
simplicity we will here assume a purely induced response due to the Earth's
field :math:`\mathbf{H}_0` such that:

:math:`\mathbf{b} = \frac{\mu_0}{4\pi}  \int_{V}    \nabla \nabla \left(\frac{1}{r}\right) \cdot \mathbf{H}_0 \kappa  \; dV`

Great, we have a general expression relating any secondary magnetic flux due to
magnetic material

Forward Problem
---------------

Assuming a purely induced response, we can solve the integral analytically. As
derived by Sharma 1966, the integral can be evaluated for rectangular prisms
such that:

:math:`\mathbf{b} =  \mathbf{T} \cdot \mathbf{H}_0 \; \kappa`

Where the tensor matrix :math:`\bf{T}` relates the three components of magnetization :math:`\mathbf{M}` to the components of the field :math:`\mathbf{b}`:

:math:`\mathbf{T} = \begin{pmatrix} T_{xx} & T_{xy} & T_{xz}    \\ T_{yx} &
:T_{yy} & T_{yz}    \\ T_{zx} & T_{zy} & T_{zz} \end{pmatrix}`

In general, we discretize the earth into a collection of cells, each contributing to the magnetic data such that:

:math:`\mathbf{b} = \sum_{j=1}^{nc} \mathbf{T}_j \cdot \mathbf{H}_0 \; \kappa_j`

giving rise to a large and dense linear system. In most geophysical surveys,
we are not collecting all three components, but rather the magnitude of the
field, or *Total Magnetic Intensity* (TMI) data. Because the inducing field
is really large, we will assume that the anomalous fields are parallel to
:math:`H_0`:

:math:`d^{TMI}  = \mathbf{\hat H}_0 \cdot \mathbf{b}`

We then end up with a much smaller system:

:math:`d^{TMI} = \mathbf{F\; \kappa}`

where :math:`\mathbf{F} \in \mathbb{R}^{nd \times nc}` is our *forward*
operator and :math:`\kappa` is the physical property describing the Earth.


Mesh
^^^^

How did you set up the mesh? If you would like to show code snippets, you can!


.. exec::

    import SimPEG
    mesh = SimPEG.Mesh.TensorMesh([10,10])
    print mesh.nC

and a reproducible plot

.. plot::

    import SimPEG
    mesh = SimPEG.Mesh.TensorMesh([10,10])
    mesh.plotGrid()
    plt.show()



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
