================
Sub-package math
================

.. py:module:: pvlab.math

Provide tools for mathematical or statistical operations.

It contains the following modules:

Module module
^^^^^^^^^^^^

.. py:module:: pvlab.math.module

Calculates the module of a vector (n-dimensions).

It supports n-dimensional components. It is intended for using when
working with versions of python older than 3.8.


.. note::
   In python v3.8, it was added support for n-dimensional points.
   Then, in python 3.10, accuracy was improved.
   `Here`_ for further information.


.. py:function:: pvlab.math.module(*components: Sequence[float]) -> float:

   Calculate the module of a vector, given its components.



**Example 1**: correct use of function ``pvlab.math.module``.

.. code-block:: python

   components = [5, 8, 3, 6]
   round(module(*components), 3)
   11.576



**Example 2**: ``components`` must be ``float`` or ``int`` types.

.. code-block:: python

   components = [5, 3, 8, '6']
   module(*components)
   Traceback (most recent call last):
   TypeError: components items must be int or float types.



.. _Here: https://docs.python.org/3/library/math.html#trigonometric-functions
