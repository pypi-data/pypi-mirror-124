================
Sub-package math
================

.. py:module:: pvlab.math

Provide tools for mathematical or statistical operations.

It contains the following modules:

Module hypot
^^^^^^^^^^^^

.. py:module:: pvlab.math.hypot

Contain the trigonometric function hypot, almost equal to math.hypot.

It supports n-dimensional coordinates. It is intended for using when
working with versions of python older than 3.8.


.. note::
   In python v3.8, it was added support for n-dimensional points.
   Then, in python 3.10, accuracy was improved.
   `Here`_ for further information.


.. py:function:: pvlab.math.hypot(*coordinates: Sequence[float]) -> float:

   Calculate the module of a vector, given its coordinates.



**Example 1**: correct use of function ``pvlab.math.hypot``.

.. code-block:: python

   coordinates = [5, 8, 3, 6]
   round(hypot(*coordinates), 3)
   11.576



**Example 2**: ``coordinates`` must be ``float`` or ``int`` types.

.. code-block:: python

   coordinates = [5, 3, 8, '6']
   hypot(*coordinates)
   Traceback (most recent call last):
   TypeError: coordinates items must be int or float types.



.. _Here: https://docs.python.org/3/library/math.html#trigonometric-functions
