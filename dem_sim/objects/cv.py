import numpy as np

from dem_sim.objects.collision import Collision
import dem_sim.util.vector_utils as vect
from dem_sim.util.hashing_utils import commutative_cantor


# TODO: Add broad phase for wall collisions.

class CVManager:
    cvs = None
    cv_length = None
    min_bound = None
    max_bound = None
    cvs_per_edge = None

    def __init__(self, cvs_per_edge, max_bound=0.5, min_bound=-0.5):
        self.initialize_cvs(cvs_per_edge)
        self.cv_length = (max_bound - min_bound) / cvs_per_edge
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.cvs_per_edge = cvs_per_edge

    def initialize_cvs(self, cvs_per_edge):
        self.cvs = []
        for i in range(cvs_per_edge):
            self.cvs.append([])
            for j in range(cvs_per_edge):
                self.cvs[i].append([])
                for k in range(cvs_per_edge):
                    self.cvs[i][j].append([])

    def get_nearby_particles(self, idx):
        i, j, k = idx
        particles = []
        for l in range(i - 1, i + 2):
            for m in range(j - 1, j + 2):
                for n in range(k - 1, k + 2):
                    if self.array_in_bounds([l, m, n], 0, self.cvs_per_edge - 1):
                        particles += self.cvs[l][m][n]
        return particles

    def add_particles(self, particles):
        for p in particles:
            idx = CVManager.get_cv_idx_from_pos(p.pos, self.cv_length, -self.min_bound)
            try:
                self.cvs[idx[0]][idx[1]][idx[2]].append(p)
            except KeyError:
                print(p.pos)
                continue

    def get_collisions(self):
        collision_ids = []
        collisions = []
        for i in range(self.cvs_per_edge):
            for j in range(self.cvs_per_edge):
                for k in range(self.cvs_per_edge):
                    cv = self.cvs[i][j][k]
                    for p in cv:
                        col_ps = self.get_nearby_particles([i, j, k])
                        for p2 in col_ps:
                            collision_id = commutative_cantor(p.pid, p2.pid)
                            if collision_id not in collision_ids:
                                collisions.append(Collision(p, p2))
                                collision_ids.append(collision_id)
        return collisions

    def reset(self):
        for i in range(self.cvs_per_edge):
            for j in range(self.cvs_per_edge):
                for k in range(self.cvs_per_edge):
                    self.cvs[i][j][k] = []

    @staticmethod
    def array_in_bounds(array, min_val, max_val):
        """ Checks whether all elements in an array are within the given bounds. """
        for element in array:
            if element > max_val or element < min_val:
                return False
        return True

    @staticmethod
    def get_cv_idx_from_pos(pos, cv_length, offset):
        x = pos[0] + offset
        y = pos[1] + offset
        z = pos[2] + offset
        i = int((x - x % cv_length) / cv_length)
        j = int((y - y % cv_length) / cv_length)
        k = int((z - z % cv_length) / cv_length)
        return [i, j, k]
