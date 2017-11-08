from dem_sim.objects.particle import Particle
from dem_sim.util.vector_utils import *
import numpy as np
import math


class Collision:
    p1 = None
    p2 = None
    stiffness = None
    damping_coefficient = None

    def __init__(self, particle1, particle2, stiffness=1, damping_coefficient=None, restitution=None):
        self.p1 = particle1
        self.p2 = particle2
        self.stiffness = stiffness
        if damping_coefficient is None and restitution is not None:
            self.damping_coefficient = self.calculate_damping_coefficient(restitution)
        elif damping_coefficient is None:
            self.damping_coefficient = 1
        else:
            self.damping_coefficient = damping_coefficient

    def calculate_damping_coefficient(self, restitution):
        ln_rest = math.log(restitution)
        return -2 * ln_rest * (self.get_reduced_particle_mass() * self.stiffness / (math.pi ** 2 + ln_rest ** 2)) ** 0.5

    def get_reduced_particle_mass(self):
        m1 = self.p1.get_mass()
        m2 = self.p2.get_mass()
        return m1 * m2 / (m1 + m2)

    def get_collision_normal(self):
        return normalize(self.p2.pos - self.p1.pos)

    def get_normal_velocity(self):
        normal = self.get_collision_normal()
        return np.dot((self.p2.vel - self.p1.vel), normal) * normal

    def get_particle_centre_separation(self):
        return np.linalg.norm(self.p2.pos - self.p1.pos)

    def get_particle_overlap(self):
        return self.p1.diameter / 2 + self.p2.diameter / 2 - self.get_particle_centre_separation()

    def calculate_collision_normal_force(self):
        force = self.stiffness * self.get_particle_overlap() * self.get_collision_normal() \
                - self.damping_coefficient * self.get_normal_velocity()
        self.p1.dem_forces.append(-force)
        self.p2.dem_forces.append(force)

    def calculate(self):
        if self.get_particle_overlap() > 0:
            self.calculate_collision_normal_force()
