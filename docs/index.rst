.. _index:

Computation
===========

The purpose of `computation.geosci.xyz <http://computation.geosci.xyz>`_ is to be a point of entry for geoscientists
into the numerics of simulation and inversion in geophysics. It contains
fundamental principles and examples to get geoscientists up and running with
numerical tools. Everything is open. Everything is reproducible.

**Goals**

- Provide resources on fundamental concepts and important aspects for running and developing numerical simulations. This includes discretizing a partial differential equation using finite volume and practicalities such as mesh design.
- Discuss and demonstrate inversion as an optimization problem. This includes stating an inverse problem that is composed of a data misfit and a regularization function, and examining the impact of choices such as trade-off parameters.
- Examples and tutorials are fully reproducible - nothing is hidden. Examples are a growing area, submissions and ideas are welcome and encouraged.


**Resources & Connections**

- SimPEG Paper: http://www.sciencedirect.com/science/article/pii/S009830041530056X
- Oldenburg and Li, 2005: https://www.researchgate.net/profile/Douglas_Oldenburg/publication/238708196_5_Inversion_for_Applied_Geophysics_A_Tutorial/links/004635282572529927000000.pdf
- SimPEG documentation: http://docs.simpeg.xyz/
- Phil’s directed studies tutorials: https://github.com/jokulhaup/directed_studies


**Development strategy**

- Use a google doc for a proposal to get examples started
- Case-studies use the jupyter notebook
- Tutorials contain a text portion written in rst and an associated notebook or series of notebooks


**Contents:**

.. toctree::
   :maxdepth: 1

   content/fundamentals/index
   content/tutorials/index
   content/case-studies/index

