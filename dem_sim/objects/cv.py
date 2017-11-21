import numpy as np


class CV:
    idx = None
    particles = None
    neighbors = None

    def __init__(self, idx):
        self.idx = idx
        self.particles = []
        self.neighbors = []
        return

    def set_neighbors(self, cvs):
        for cv in cvs:
            if self.neighbors.count(cv) == 0:
                idx_dif = np.subtract(self.idx, cv.idx)
                if CV.array_in_bounds(idx_dif, -1, 1) and (idx_dif[0] != 0 or idx_dif[1] != 0 or idx_dif[2] != 0):
                    print("1: " + str(self) + ", 2: " + str(cv) + ", dif: " + str(idx_dif))
                    self.neighbors.append(cv)
                    cv.neighbors.append(self)

    def __str__(self):
        return "{0}, {1}, {2}".format(self.idx[0], self.idx[1], self.idx[2])

    @staticmethod
    def get_cv_idx_from_pos(pos, cv_length):
        return [pos[0] % cv_length, pos[1] % cv_length, pos[2] % cv_length]

    @staticmethod
    def array_in_bounds(array, min_val, max_val):
        """ Checks whether all elements in an array are within the given bounds. """
        for element in array:
            if element > max_val or element < min_val:
                return False
        return True
