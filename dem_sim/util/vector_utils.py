import numpy as np


def normalize(vector):
    vector = np.array(vector)
    return vector / np.linalg.norm(vector)
