#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contain the trigonometric function hypot, almost equal to math.hypot.

It supports n-dimensional coordinates,
for compatibility with python versions previous
than 3.8. In python v3.8, it was added support for n-dimensional points.
In python 3.10, accuracy was improved.

`Here`_ for further information.

.. _Here: https://docs.python.org/3/library/math.html#trigonometric-functions
"""
from math import sqrt
from typing import Sequence


def hypot(*coordinates: Sequence[float]) -> float:
    """Calculate the module of a vector, given its coordinates.

    **Example 1**: correct functioning.

    >>> coordinates = [5, 8, 3, 6]

    >>> round(hypot(*coordinates), 3)
    11.576

    **Example 2**: coordinates must be floats or ints.

    >>> coordinates = [5, 8, 3, '6']

    >>> hypot(*coordinates)  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: Coordinate items must be 'int' or 'float' type.
    """
    # Check if coordinates members are 'int' or 'float' types.
    for item in coordinates:
        if type(item) not in [int, float]:
            raise TypeError("Coordinate items must be 'int' or 'float' type.")

    hypotenuse = sqrt(sum(x**2 for x in coordinates))
    return hypotenuse


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
