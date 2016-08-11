.. _tools:

Tools
=====

- **Purpose:** To introduce and provide resources for the tools used to build and work with SimPEG_

.. _SimPEG: http://simpeg.xyz

SimPEG_ is implemented in Python_ 2.7, a high-level, `object oriented language <https://docs.python.org/2/tutorial/classes.html>`_
and has core dependencies on three packages standard to scientific
computing in Python_.

- NumPy_: n-dimensional array package
- SciPy_: scientific computing including: sparse matrices, numerical solvers, optimization routines, etc.
- Matplotlib_: 2D plotting library

.. _Python: https://www.python.org/
.. _NumPy: http://www.numpy.org/
.. _SciPy: https://www.scipy.org/
.. _Matplotlib: http://matplotlib.org/
.. _Jupyter Notebook: http://jupyter.org/
.. _notebook: https://github.com/simpeg/tutorials/blob/master/notebooks/tools.ipynb


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
    :width: 90%

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

.. note::

    If that scares you, you can always use division from the future! :code:`from __future__ import division` see PEP0238_

is integer division, while::

    >>> 1./2.
    0.5

is floating point division. This is only the case in Python 2, in Python 3,
division will return a floating point number.


Counting and Lists
******************

Python_ uses zero-based indexing::

    >>> mylist = [6, 5, 4, 3]
    >>> len(mylist)
    4
    >>> mylist[0]
    6

There are a few handy indexing tricks::

    >>> mylist[:2] # counting up
    [6, 5]
    >>> mylist[2:] # starting from
    [4, 3]
    >>> mylist[-1] # going backwards
    3


Loops and List Comprehension
****************************

A :code:`for` loop to append :code:`10` values to a list looks like::

    >>> n = 10
    >>> a = []
    >>> for i in range(n):
    ... a.append(i)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

or using list comprehension

    >>> n = 10
    >>> b = [i for i in range(n)]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Try running these in the notebook_ and compare the times. To get a better
picture, increase :code:`n`.

.. note::

    In the notebook, we use the cell magic :code:`%%time` to track the amount of
    time it takes to execute cell

A handy tool for looping over lists is :code:`enumerate`::

    >>> mylist = ['Monty', 'Python', 'Flying', 'Circus'] # python was named after the movie!
    >>> for i, val in enumerate(mylist):
    ... print i, val
    0 Monty
    1 Python
    2 Flying
    3 Circus

This is a flavor of some of the flow control for lists in Python_, for more
details, check out chapters `4 <https://docs.python.org/2/tutorial/controlflow.html>`_,
`5 <https://docs.python.org/2/tutorial/datastructures.html>`_ in the `Python Tutorial`_.

If, elif, else
**************

Conditionals in Python_ are implemented using :code:`if`, :code:`elif`, :code:`else`

    >>> # Pick a random number between 0 and 100
    >>> import numpy as np
    >>> number = (100.*np.random.rand(1)).round() # make it an integer
    >>> if number > 42:
    ...     print '%i is too high'%number
    ... elif number < 42:
    ...     print '%i is too low'%number
    ... else:
    ...     print 'you found the secret to life. %i'%number

Note that the indentation level matters in python. Logical operators,
:code:`or`, :code:`and` are also handy for constructing conditionals

Functions
*********



NumPy
-----

.. image:: https://www.scipy.org/_static/images/numpylogo_med.png
    :align: right
    :width: 80
    :target: http://www.numpy.org/


NumPy_ contains the n-dimensional array machinery for storing and working with
matrices and vectors. To use NumPy_, it must first be imported. It is standard
practice to import is as shorthand :code:`np`.

.. code::

    >>> import numpy as np

.. note::
    You can use tab completion to look at the attributes of an object

    .. image:: ../images/tabcompletion.png
        :scale: 30%
        :align: center

How many dimensions?
********************

NumPy makes a distinction between scalars, vectors and arrays

    >>> a = np.array(1) # scalar
    >>> print a.shape # has no dimensions
    ()
    >>> b = np.array([1]) # vector
    >>> print b.shape # has one dimension
    (1,)
    >>> c = np.array([[1]]) # array
    >>> print c.shape # has two (or more) dimensions
    (1, 1)

The :code:`shape` gives the length of each array dimension. (:code:`size`
gives you the number of elements)

.. note::
    In the notebook, you can query documentation using a :code:`?`

    .. image:: ../images/docsinnotebook.png
        :scale: 30%
        :align: center

This distinction is particularly important when performing linear algebra
operations. For instance, if we create a vector::

    >>> v = np.random.rand(10)
    >>> v.shape
    (10,)

and then want to take an inner product, which we expect to output a scalar,
one way you might think to do this (spoiler alert: it's wrong!)::

    >>> a = v.T * v
    >>> a.shape
    (10,)

turns out, the concept of a transpose doesn't matter for vectors, they only
have one dimension, so there is no way to exchange dimensions. What we just
did was a `Hadamard product
<https://en.wikipedia.org/wiki/Hadamard_product_(matrices)>`_ (element-wise
multiplication), so

    >>> v.T * v == v * v
    True

So how do we take an inner product? (:code:`dot`)

    >>> b = v.dot(v)
    >>> b.shape
    ()

Success! :code:`b` is a scalar.

What happens if we work with arrays instead?

    >>> w = np.random.rand(10,1)
    >>> w.shape
    (10,1)



SciPy
-----

.. image:: https://docs.scipy.org/doc/scipy-0.9.0/reference/_static/scipyshiny_small.png
    :align: right
    :width: 80
    :target: http://www.scipy.org/

.. note::

    .. raw:: html

       <div class="col-md-2" align="center">
          <a href="https://github.com/simpeg/tutorials/"><i class="fa fa-wrench fa-4x" aria-hidden="true"></i></a>
       </div>

    This page is under construction. If you have suggestions, please make some
    noise on `github! <https://github.com/simpeg/tutorials/>`_


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

Also need functions

Class, Inheritance, Properties, Wrappers, and Self

Pointers
--------

- `Software Carpentry <http://swcarpentry.github.io/python-novice-inflammation/>`_
- `Python Tutorial`_

.. _Python Tutorial: https://docs.python.org/2/tutorial/index.html
.. _PEP0238: https://www.python.org/dev/peps/pep-0238/

