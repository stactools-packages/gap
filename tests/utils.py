import math
from typing import List
from unittest import TestCase


class StactoolsTestCase(TestCase):
    def assertListsAreClose(self, actual: List[float], expected: List[float],
                            abs_tol: float):
        for a, e in zip(actual, expected):
            self.assertTrue(math.isclose(a, e, abs_tol=abs_tol),
                            (f"Lists are not close enough: {a} != {e} "
                             f"(comparing {actual} and {expected})"))
