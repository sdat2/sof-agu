"""Test plot utilities."""
import unittest
from src.plot_utils.ellipses import plot_ellipsoid_test


class TestCase(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_ellipses(self):
        plot_ellipsoid_test()


suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
