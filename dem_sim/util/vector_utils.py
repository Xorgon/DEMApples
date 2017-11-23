import numpy as np
import math


def normalize(vector):
    vector = np.array(vector)
    if mag_squared(vector) == 0:
        # print("Warning, encountered 0 length vector when attempting to normalize.")
        # TODO: Fix this!!
        return vector
    else:
        return vector / mag(vector)


def mag(vector):
    return math.sqrt(mag_squared(vector))


def mag_squared(vector):
    """ Returns the magnitude of the vector squared. Used to reduce unnecessary square-root operations. """
    return vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2]


def subtract(v1, v2):
    """ Subtracts v2 from v1. """
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]
