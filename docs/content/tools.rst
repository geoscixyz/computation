.. _tools:

Toolbox
=======

- **Purpose:** To introduce and provide resources for the tools used to build and work with SimPEG_

.. _SimPEG: http://simpeg.xyz

SimPEG_ is implemented in Python_ 2.7, a high-level, `object oriented language <https://docs.python.org/2/tutorial/classes.html>`_
and has core dependencies on three packages standard to scientific
computing in Python_.

- NumPy_: n-dimensional array package
- SciPy_: scientific computing including: sparse matrices, numerical solvers, optimiztion routines, etc.
- Matplotlib_: 2D plotting library

.. _Python: https://www.python.org/
.. _NumPy: http://www.numpy.org/
.. _SciPy: https://www.scipy.org/
.. _Matplotlib: http://matplotlib.org/
.. _Jupyter Notebook: http://jupyter.org/


Jupyter Notebook
----------------

.. image:: http://blog.jupyter.org/content/images/2015/02/jupyter-sq-text.png
    :align: right
    :width: 80

A notebook_ containing the following examples is available for you to download
and follow along. In the directory where you downloaded the notebook, open up
a `Jupyter Notebook`_ from a terminal::

    jupyter notebook

and open :code:`tools.ipynb`. A few things to note

.. image:: ../images/notebookpointers.png
    :align: center
    :width: 100%

- To execute a cell is **Shift + Enter**
- To restart the kernel (clean your slate) is **Esc + 00**

Throughout this tutorial, we will show a few tips for working with the
notebook.

Python
------

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/220px-Python-logo-notext.svg.png
    :align: right
    :width: 80
    :target: https://www.python.org/

Python_ is a high-level interpreted computing language. Here we outline a few
of the basics and common trip-ups. For more information and tutorials, check
out the `Python Documentation <https://www.python.org/doc/>`_. Note that at
the moment, we are using Python 2.7, so those are the docs to follow. In
particular, up to chapter 5 at this stage of the tutorials.


Types
*****

Python_ makes a distinction on types: `int`, `float`, and `complex`::

    >>> type(1) == int
    True
    >>> type(1.) == float
    True
    >>> type(1j) == complex
    True

This is particularly important when doing division::

    >>> 1/2
    0

is integer division, while::

    >>> 1./2.
    0.5

is float division.


Counting and Lists
******************

Python_ uses zero-based indexing::

    >>> mylist = [6, 5, 4, 3]
    >>> len(mylist)
    4
    >>> mylist[0]
    6

There are a few handy indexing tricks::

    >>> mylist[:2]
    [6, 5]
    >>> mylist[2:]
    [4, 3]
    >>> mylist[-1]
    3


Loops and List Comprehension
****************************


.. image:: ../images/loopsandlists.png
    :align: center
    :width: 80%

NumPy
-----

.. image:: https://www.scipy.org/_static/images/numpylogo_med.png
    :align: right
    :width: 80
    :target: http://www.numpy.org/



.. code::

    import numpy as np

SciPy
-----

.. image:: https://docs.scipy.org/doc/scipy-0.9.0/reference/_static/scipyshiny_small.png
    :align: right
    :width: 80
    :target: http://www.scipy.org/



Thinking in sparse
******************

.. code::

    import scipy.sparse as sp

How do I solve you?
*******************

Matplotlib
----------

Object Oriented Programming in Python
-------------------------------------

Class, Inheritance, Properties, Wrappers, and Self

Pointers
--------

- `Software Carpentry <http://swcarpentry.github.io/python-novice-inflammation/>`_
- `Python Tutorial <https://docs.python.org/2/tutorial/index.html>`_

