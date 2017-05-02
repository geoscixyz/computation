.. _story_CaseStudy:

Case Study
==========

.. topic:: Purpose

    purpose of this examples

The code for this story is available in the SimPEG examples
- github path to SimPEG Example:
- github path to notebook:


Setup
-----

Governing Equations and a picture here. Please put pictures in the local
images folder.



Forward Problem
---------------

A couple statements on what we will accomplish here


Mesh
^^^^

How did you set up the mesh? If you would like to show code snippets, you can!


.. exec::

    import SimPEG
    mesh = SimPEG.Mesh.TensorMesh([10,10])
    print mesh.nC

To show some code and hide some doce, use :code:`#hide` inside the :code:`exec` environment

.. exec::

    import SimPEG #hide
    mesh = SimPEG.Mesh.TensorMesh([10,10]) #hide
    print mesh.nC



Making a reproducible plot

.. plot::

    import SimPEG
    mesh = SimPEG.Mesh.TensorMesh([10,10])
    mesh.plotGrid()

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
