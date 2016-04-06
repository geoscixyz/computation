# SimPEG Tutorials

[![Build Status](https://travis-ci.org/simpeg/tutorials.svg?branch=master)](https://travis-ci.org/simpeg/tutorials) 
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/simpeg/tutorials/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/simpegtutorials/badge/?version=latest)](http://simpegtutorials.readthedocs.org/en/latest/?badge=latest)

Docs and a collection of notebooks and tutorials using SimPEG for Geophysical Inversions. 

Prerequisites: 
- python, jupyter and git. Checkout [software carpentry](http://software-carpentry.org/lessons/) for getting started

Topics:
- Overview of gradient based geophysical inversions: *How do we estimate models from data?* and motivation for SimPEG!: including - reproducible inversions 
- Installing SimPEG (from git and from pip), and how we operate on github 
- SimPEG framework: *How do we organize all of the moving pieces?*
- diving into the modules
    - Mesh: *where do we put things?*, and *how do we construct differential operators?*
    - Forward Simulation: *how do we simulate data?*
        - Problem: *how do we model the physics?*
        - Survey: *what are our sources and receivers?*
        - Sensitivities: *how does a change in our model affect our data?* 
        - Mappings: *what is your model?* 
    - Constructing an inverse problem: *how do we mathematically define an inverse problem?*
        - Data Misfit: *how do we measure the "fit" of our data?*
        - Regularization: *the problem is ill-posed, how do we choose a model among the infinite number of choices?*
        - Statement of the Inverse Problem: *how do we mathematically pose the inverse problem as an optimization?*
    - Solving the inverse problem: *how do we solve the stated inverse problem for a model?*
        - Inversion as optimization: *how do we march towards a solution?*
        - Inversion directives: *how do we provide instructions to the inversion?* 
    - Bringing it all together: solving an inverse problem
  
Throughout, we will use examples from DC resistivity and electromagnetics to guide our discussion
