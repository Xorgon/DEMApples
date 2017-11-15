import numpy as np


def normalize(vector):
    vector = np.array(vector)
    if np.linalg.norm(vector) == 0:
        print("Warning, encountered 0 length vector when attempting to normalize.")
        # TODO: Fix this!!
        return vector
    else:
        return vector / np.linalg.norm(vector)
