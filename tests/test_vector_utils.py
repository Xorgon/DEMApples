from unittest import TestCase
import numpy as np
from dem_sim.util.vector_utils import *


class TestCollision(TestCase):
    def test_normalize(self):
        TestCase.assertAlmostEquals(self,
                                    np.linalg.norm(normalize([1, 1, 1]) - np.array([3 ** -0.5, 3 ** -0.5, 3 ** -0.5])),
                                    0)
