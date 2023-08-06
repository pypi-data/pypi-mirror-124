#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing of module hypot.

Created on Mon May 31 07:00:52 2021.

@author: josepedro
"""
import unittest
from pvlab.tools.math.hypot import hypot


class HypotTest(unittest.TestCase):
    def test_result(self):
        """Check if the result of hypot() function is correct"""
        self.assertEqual(11.576, round(hypot(5, 8, 3, 6), 3))

    def test_exception(self):
        """Check if hypot generates an exception when\
 combining strings and integer or floats"""
        with self.assertRaises(TypeError):
            hypot(5, 8, 3, '6')


if __name__ == '__main__':
    unittest.main(verbosity=1)
