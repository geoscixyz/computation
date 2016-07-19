.. _stories:

DC resistivity
==============

.. topic:: Purpose

    Understand basic setup and physics of a direct current (DC) resistivity survey within the context of a kimberlite exploration. Run DC forward modelling and inversion using SimPEG-Static package.

.. image:: images/tkc/dc.png
    :width: 80%
    :align: center

Set-up
------

Physical behavior of DC resistivity survey is governed by steady-state maxwell's equation:

.. math::
    \vec{j} = \sigma \vec{e}

.. math::
    \vec{e} = -\nabla \phi

.. math::
    \nabla \cdot \vec{j} = -\vec{j}_s = I_0 (\delta(\vec{r}-\vec{r}_+)-\delta(\vec{r}-\vec{r}_-))

.. math::
    \vec{j} \cdot \hat{n} \ \Big|_{\partial \Omega} = 0


- :math:`\vec{j}`: Current density (A/m :math:`^2`)

- :math:`\vec{e}`: Electric field (V/m)

- :math:`I_0`: Current (A)

- :math:`\delta`: Volumetric delta function (m :math:`^{-3}`)


Consider a simple gradient array having a pair of A (+) and B (+) current electrodes (Tx) with multiple M (+) and N (-) potential electrodes (Rx). Using giant battery (?), we make significant potential difference allowing electrical currents flow A to B electrodes. If the earth includes conductors or resistors that will distorts current flows, and measured potential differences on the surface electrodes (MN) will be reflective on those distortions. Typically kimberlitic pipe (including diamonds) will be more conductive than the background rock (granitic) hence, measured potential difference will be low. That is, contrasts in electrical conductivity between different rocks induce anomalous voltages. From the observed voltages, we want to estimate conductivity distribution of the earth. We use a geophysical inversion technique to do this procedure.

We work through each step of geophysical inversion using SimPEG-Static package under SimPEG's frame work having two main items: a) Forward simulation and b) Inversion.

.. figure:: images/SimPEGFramework.png
    :width: 80%
    :align: center
    :name: SimPEGFramework

    SimPEG's framework


Forward simulation
------------------

A forward simulation of DC requires Survey and Problem classes. We need to pass current and potential electrode locations to a DC survey class. Physical behavior of DC is governed by static Maxwell's equations, and a DC problem class handles this by solving a corresponding partial different equation in a discrete space. For this, the earth earth needs to be discretized to solve corresponding partial differential equation. The Problem class computes fields in full discretized domain, and the Survey class evaluates data at potential electrodes using the fields. The Survey and Problem classes need to share information hence, we pair them.


Mesh
****

We use a 3D tensor mesh to discretize the earth having 25x25x25 m core cell size.
Smaller vertical size of the cell (dz) is used close to the topographic surface (12.5 m), and padding cells are used to satisfies the natural boundary condition imposed.

.. plot::

    from SimPEG import Mesh, np
    # Core cell sizes in x, y, and z
    csx, csy, csz = 25., 25., 25.
    # Number of core cells in each directiPon s
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
    mesh.plotSlice(np.ones(mesh.nC)*np.nan, grid=True)
    mesh.plotSlice(np.ones(mesh.nC)*np.nan, grid=True, normal="Y")
    plt.gca().set_aspect('equal')
    plt.show()


Survey
******

We use a simple gradient array having a pair of current electrodes (AB), and multiple potential electrodes (MN). Then length of AB and MN are 1200 and 25 m, respectively.


.. figure:: images/dc/GradientArray.png
    :align: center
    :width: 50%
    :name: GradientArray

    Gradient array



Inversion
---------

.. .. toctree::
..     :maxdepth: 2

..     template

.. _SimPEG: http://simpeg.xyz
