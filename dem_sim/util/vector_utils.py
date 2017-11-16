import numpy as np


def normalize(vector):
    vector = np.array(vector)
    if np.linalg.norm(vector) == 0:
        print("Warning, encountered 0 length vector when attempting to normalize.")
        # TODO: Fix this!!
        return vector
    else:
        return vector / np.linalg.norm(vector)


def mag_squared(vector):
    """ Returns the magnitude of the vector squared. Used to reduce unnecessary square-root operations. """
    return vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2]
