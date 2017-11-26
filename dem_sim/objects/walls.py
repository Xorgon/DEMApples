import numpy as np
from dem_sim.util.vector_utils import normalize
from dem_sim.util.exceptions import ParameterException


class AAWall:
    """ An axis-aligned planar wall. """

    normal = None
    max = None
    min = None

    def __init__(self, pos1, pos2):
        pos1 = np.array(pos1)
        pos2 = np.array(pos2)
        if 0 in (pos1 - pos2):
            n = normalize(pos1 - pos2)
            self.normal = np.array([1, 1, 1]) - np.divide(n, n, where=n!= 0)

            self.max = np.maximum(pos1, pos2)
            self.min = np.minimum(pos1, pos2)
        else:
            raise ParameterException("Points not in the same axis-aligned plane.")

# TODO: Add non-axis-aligned wall.
# TODO: Add periodic wall.
