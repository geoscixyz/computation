.. _stories:

DC resistivity
==============

.. topic:: Purpose

	Understand basic setup and physics of a direct current (DC) resistivity survey within the context of a kimberlite exploration. Run DC forward modelling and inversion using SimPEG-Static package.

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


Consider a simple gradient array having a pair of A (+) and B (+) current electrodes (Tx) with multiple M (+) and N (-) potential electrodes (Rx). Using giant battery (?), we make significant potential difference allowing electrical currents flow A to B electrodes. If the earth includes conductors or resistors that will distorts current flows, and measured potential differences on the surface electrodes (MN) will be reflective on those distortions. Typically kimberlitic pipe (including diamonds) will be more conductive than the background rock (granitic) hence, measured potential difference will be low.

.. image:: images/SimPEGFramework.png
    :width: 80%

.. image:: images/SimPEGFramework.png
    :width: 80%


.. toctree::
    :maxdepth: 2

    template

.. _SimPEG: http://simpeg.xyz
