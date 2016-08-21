.. _pixelsandtheirneighbors:

Pixels and Their Neighbors
==========================

.. note::

    This article was originally published in the `Leading Edge
    <http://library.seg.org/doi/abs/10.1190/tle35080703.1>`_:

    Rowan Cockett, Lindsey J. Heagy, and Douglas W. Oldenburg (2016). ”Pixels and their neighbors: Finite volume.” The Leading Edge, 35(8), 703–706.
    doi: 10.1190/tle35080703.1

    .. image:: https://i.creativecommons.org/l/by-sa/4.0/88x31.png
        :target: http://creativecommons.org/licenses/by-sa/4.0/
        :align: center

    This work is licensed under a
    `Creative Commons Attribution-ShareAlike 4.0 International License <http://creativecommons.org/licenses/by-sa/4.0/>`_.

    Associated notebooks are available on `github <https://github.com/seg/tutorials-2016/tree/master/1608_Finite_volume>`_ and can be run online with binders

    .. image:: http://mybinder.org/badge.svg
        :target: http://mybinder.org:/repo/simpeg/tle-finitevolume
        :align: center

We take you on the journey from continuous equations to their discrete matrix
representations using the finite volume method for the Direct Current (DC)
resistivity problem. These techniques are widely applicable across geophysical
simulation types and have their parallels in finite element and finite
difference. We show derivations visually, as you would on a whiteboard, and
have provided an accompanying notebook to explore the numerical results using
SimPEG :ref:`(Cockett et al. 2015) <references>`.


DC Resistivity
--------------

.. figure:: https://storage.googleapis.com/simpeg/tle-finitevolume/DCSurvey.png
    :align: center
    :name: dcsurvey

    Setup of a DC resistivity survey.

DC resistivity surveys obtain information about subsurface electrical
conductivity, :math:`\sigma`. This physical property is often diagnostic in mineral
exploration, geotechnical, environmental and hydrogeologic problems, where the
target of interest has a significant electrical conductivity contrast from the
background. In a DC resistivity survey, steady state currents are set up in
the subsurface by injecting current through a positive electrode and
completing the circuit with a return electrode (:numref:`dcsurvey`). The equations for
DC resistivity are derived in :numref:`dcequations`. Conservation of charge (which can be
derived by taking the divergence of Ampere’s law at steady state) connects the
divergence of the current density everywhere in space to the source term which
consists of two point sources, one positive and one negative. The flow of
current sets up electric fields according to Ohm’s law, which relates current
density to electric fields through the electrical conductivity. From Faraday’s
law for steady state fields, we can describe the electric field in terms of a
scalar potential, :math:`\phi`, which we sample at potential electrodes to obtain
data in the form of potential differences.

.. figure:: https://storage.googleapis.com/simpeg/tle-finitevolume/DCEquations.png
    :align: center
    :name: dcequations

    Derivation of the DC resistivity equations.

To set up a solvable system of equations, we need the same number of unknowns
as equations, in this case two unknowns (one scalar, :math:`\phi`, and one vector
:math:`\vec{j}`) and two first-order equations (one scalar, one vector).

In this tutorial, we walk through setting up these first order equations in
finite volume in three steps: (1) defining where the variables live on the
mesh; (2) looking at a single cell to define the discrete divergence and the
weak formulation; and (3) moving from a cell based view to  the entire mesh to
construct and solve the resulting matrix system. The notebooks included with
this tutorial leverage the SimPEG package (http://simpeg.xyz, :ref:`Cockett et al.
2015 <references>`), which extends the methods discussed here to various mesh types.

Where do things live?
---------------------

To bring our continuous equations into the computer, we need to discretize the
earth and represent it using a finite(!) set of numbers. In this tutorial we
will explain the discretization in 2D and generalize to 3D in the notebooks. A
2D (or 3D!) mesh is used to divide up space, and we can represent functions
(fields, parameters, etc.) on this mesh at a few discrete places: the nodes,
edges, faces, or cell centers. For consistency between 2D and 3D we refer to
faces having area and cells having volume, regardless of their dimensionality.
Nodes and cell centers naturally hold scalar quantities while edges and faces
have implied directionality and therefore naturally describe vectors. The
conductivity, :math:`\sigma`, changes as a function of space, and is likely to
have discontinuities (e.g. if we cross a geologic boundary). As such, we will
represent the conductivity as a constant over each cell, and discretize it at
the center of the cell. The electrical current density, :math:`\vec{j}`, will
be continuous across conductivity interfaces, and therefore, we will represent
it on the faces of each cell. Remember that :math:`\vec{j}` is a vector; the
direction of it is implied by the mesh definition (i.e. in :math:`x`,
:math:`y` or :math:`z`), so we can store the array :math:`\bf{j}` as
*scalars* that live on the face and inherit the face's normal. When
:math:`\vec{j}` is defined on the faces of a cell the potential,
:math:`\vec{\phi}`, will be put on the cell centers (since :math:`\vec{j}` is
related to :math:`\phi` through spatial derivatives, it allows us to
approximate centered derivatives leading to a staggered, second-order
discretization). Once we have the functions placed on our mesh, we look at a
single cell to discretize each first order equation. For simplicity in this
tutorial we will choose to have all of the faces of our mesh be aligned with
our spatial axes (:math:`x`, :math:`y`, and :math:`z`), the extension to
curvilinear meshes will be presented in the supporting notebooks.

.. figure:: https://storage.googleapis.com/simpeg/tle-finitevolume/FiniteVolume.png
    :align: center
    :name: finitevolume

    Anatomy of a finite volume cell.

One cell at a time
------------------

To discretize the first order differential equations we consider a single cell
in the mesh and we will work through the discrete description of equations (1)
and (2) over that cell.

(1) In and out
^^^^^^^^^^^^^^

Equation (a) relates the divergence of the current density to a source term. To
discretize using finite volume, we will look at the divergence geometrically.
The divergence is the integral of a flux through a closed surface as that
enclosed volume shrinks to a point. Since we have discretized and no longer
have continuous functions, we cannot fully take the limit to a point; instead,
we approximate it around some (finite!) volume: *a cell*. The flux out of the
surface (:math:`\vec{j} \cdot \vec{n}`) is actually how we discretized
:math:`\vec{j}` onto our mesh (i.e. :math:`\bf{j}`) except that the face
normal points out of the cell (rather than in the axes direction). After
fixing the direction of the face normal (multiplying by :math:`\pm 1`), we
only need to calculate the face areas and cell volume to create the discrete
divergence matrix.

.. figure:: https://storage.googleapis.com/simpeg/tle-finitevolume/Divergence.png
    :align: center
    :name: divergence

    Geometrical definition of the divergence and the discretization.

So we have half of the equation discretized — the left hand side. Now we need
to take care of the source: it contains two dirac delta functions — these are
infinite at their origins, :math:`r_{s^+}` and :math:`r_{s^-}`, (infinity is not exactly
something a computer does well with!). However, the volume integral of a delta
function *is* well defined: it is *unity* if the volume contains the
origin of the delta function otherwise it is *zero*. As such, we can
integrate both sides of the equation over the volume enclosed by the cell.
Since :math:`\mathbf{D}\mathbf{j}` is constant over the cell, the integral is simply
a multiplication by the volume of the cell :math:`\text{v} \mathbf{D} \mathbf{j}`.
The integral of the source is zero unless one of the source electrodes is
located inside the cell, in which case it is :math:`q = \pm I`. Now we have a
discrete description of equation 1 over a single cell:

.. math::
    \text{v} \mathbf{D}\mathbf{j} = q

(2) Scalar equations only, please
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Equation (b) is a vector equation, so really it is two or three equations
involving multiple components of :math:`\vec{j}`. We want to work with a
single scalar equation, allow for anisotropic physical properties, and
potentially work with non-axis-aligned meshes — how do we do this?! We can use
the **weak formulation** where we take the inner product (:math:`\int \vec{a}
\cdot \vec{b} dv`) of the equation with a generic face function,
:math:`\vec{f}`. This reduces requirements of differentiability on the
original equation and also allows us to consider tensor anisotropy or
curvilinear meshes :ref:`(Haber 2014) <references>`.

In :numref:`weak_formulation`, we visually walk through the discretization of equation (b). On
the left hand side, a dot product requires a *single* cartesian vector,
:math:`[\mathbf{j_x, j_y}]`. However, we have a :math:`j` defined on each face (2 :math:`j_x`
and 2 :math:`j_y` in 2D!). There are many different ways to evaluate this inner
product: we could approximate the integral using trapezoidal, midpoint or
higher order approximations. A simple method is to break the integral into
four sections (or 8 in 3D) and apply the midpoint rule for each section using
the closest :math:`\mathbf{j}` components to compose a cartesian vector. A
:math:`\mathbf{P}_i` matrix (size 2 × 4) is used to pick out the appropriate faces
and compose the corresponding vector (these matrices are shown with colors
corresponding to the appropriate face in the figure). On the right hand side,
we use a vector identity to integrate by parts. The second term will cancel
over the entire mesh (as the normals of adjacent cell faces point in opposite
directions) and :math:`\phi` on mesh boundary faces are zero by the Dirichlet
boundary condition \footnote{We are using Dirichlet for simplicity in this
example, in practice, Neumann conditions are often used. This is because
“infinity” needs to be further away if applying Dirichlet boundary conditions
since potential falls off as :math:`1/r^2` and current density as :math:`1/r^3`.}. This
leaves us with the  divergence, which we already know how to do!

.. figure:: https://storage.googleapis.com/simpeg/tle-finitevolume/WeakFormulation.png
    :align: center
    :name: weak_formulation

    Discretization using the weak formulation and inner products.

The final step is to recognize that, now discretized, we can cancel the
general face function :math:`\mathbf{f}` and transpose the result (for
convention's sake):

.. math::

    \frac{1}{4}\sum_{i=1}^{4} \mathbf{P}_i^\top \sqrt{v} \boldsymbol{\Sigma}^{-1} \sqrt{v} \mathbf{P}_i \mathbf{j} =
    \mathbf{D}^\top v \phi

All together now
----------------

We have now discretized the two first order equations over a single cell. What
is left is to assemble and solve the DC system over the entire mesh. To
implement the divergence on the full mesh, the stencil of :math:`\pm 1`'s must index
into :math:`\mathbf{j}` on the entire mesh (instead of four elements). Although this
can be done in a :code:`for-loop`, it is conceptually, and often
computationally, easier to create this stencil using nested kronecker products
(see notebook). The volume and area terms in the divergence get expanded to
diagonal matrices, and we multiply them together to get the discrete
divergence operator. The discretization of the *face* inner product can
be abstracted to a function, :math:`\mathbf{M}_f(\sigma^{-1})`, that completes the
inner product on the entire mesh at once. The main difference when
implementing this is the :math:`\mathbf{P}` matrices, which must index into the
entire mesh.

With the necessary operators defined for both equations on the entire mesh, we
are left with two discrete equations

.. math::

    \text{diag}(\mathbf{v}) \mathbf{D}\mathbf{j} =
    \mathbf{q}
    \\
    \mathbf{M}_f(\sigma^{-1}) \mathbf{j} =
    \mathbf{D}^\top \text{diag}(\mathbf{v}) \boldsymbol{\phi}.


Note that now all variables are defined over the entire mesh. We could solve
this coupled system or we could eliminate :math:`\mathbf{j}` and solve for :math:`\phi`
directly (a smaller, second-order system).

.. math::

    \text{diag}(\mathbf{v})
    \mathbf{D}
    \mathbf{M}_f(\sigma^{-1})^{-1}
    \mathbf{D}^\top
    \text{diag}(\mathbf{v})
    \boldsymbol{\phi} =
    \mathbf{q}.


By solving this system matrix, we obtain a solution for the electric potential
:math:`\phi` everywhere in the domain. Creating predicted data from this requires an
interpolation to the electrode locations and subtraction to obtain potential
differences!

.. figure:: https://storage.googleapis.com/simpeg/tle-finitevolume/NumericalSolve.png
    :align: center
    :name: numerical_solve

    Electric potential on (a) Tensor and (b) Curvilinear meshes.

Moving from continuous equations to their discrete analogues is fundamental in
geophysical simulations. In this tutorial, we have started from a continuous
description of the governing equations for the DC resistivity problem,
selected locations on the mesh to discretize the continuous functions,
constructed differential operators by considering one cell at a time,
assembled and solved the discrete DC equations. Composing the finite volume
system in this way allows us to move to different meshes and incorporate
various types of boundary conditions that are often necessary when solving
these equations in practice.

.. _references:

References
----------

- Cockett, Rowan, Seogi Kang, Lindsey J. Heagy, Adam Pidlisecky, and Douglas W.
  Oldenburg. “SimPEG: An Open Source Framework for Simulation and Gradient Based
  Parameter Estimation in Geophysical Applications.” Computers & Geosciences 85
  (2015): 142–54. doi:10.1016/j.cageo.2015.09.015.


- Haber, E. Computational Methods in Geophysical Electromagnetics: Mathematics
  in Industry. Society for Industrial and Applied Mathematics, 2014.
  https://books.google.ca/books?id=favjoQEACAAJ.



