from dem_sim.objects.particle import Particle
from dem_sim.objects.walls import AAWall
from dem_sim.util.vector_utils import *
import numpy as np
import math


class Collision:
    """ Collision object for particle-particle collisions. """
    p1 = None
    p2 = None
    stiffness = None
    damping_coefficient = None
    friction_coefficient = None
    friction_stiffness = None

    pos_history = []
    vel_history = []
    time_history = []

    def __init__(self, particle1, particle2, stiffness=1, damping_coefficient=None, restitution=None,
                 friction_coefficient=None, friction_stiffness=None):
        self.p1 = particle1
        self.p2 = particle2
        self.stiffness = stiffness

        if damping_coefficient is None and restitution is not None:
            self.damping_coefficient = self.calculate_damping_coefficient(restitution)
        elif damping_coefficient is None:
            self.damping_coefficient = 1
        else:
            self.damping_coefficient = damping_coefficient

        self.friction_coefficient = friction_coefficient
        self.friction_stiffness = friction_stiffness

    def calculate_damping_coefficient(self, restitution):
        ln_rest = math.log(restitution)
        return -2 * ln_rest * (self.get_reduced_particle_mass() * self.stiffness / (math.pi ** 2 + ln_rest ** 2)) ** 0.5

    def get_reduced_particle_mass(self):
        m1 = self.p1.get_mass()
        m2 = self.p2.get_mass()
        return m1 * m2 / (m1 + m2)

    def get_collision_normal(self):
        return normalize(self.p2.pos - self.p1.pos)

    def get_relative_velocity(self):
        return self.p2.vel - self.p1.vel

    def get_normal_velocity(self):
        normal = self.get_collision_normal()
        return np.dot((self.get_relative_velocity()), normal) * normal

    def get_particle_centre_separation(self):
        return np.linalg.norm(self.p2.pos - self.p1.pos)

    def get_particle_overlap(self):
        return self.p1.diameter / 2 + self.p2.diameter / 2 - self.get_particle_centre_separation()

    def get_collision_tangent(self):
        vel_relative = self.get_relative_velocity()
        return normalize(vel_relative - self.get_normal_velocity())

    def get_tangential_displacement(self):
        # TODO: Investigate more accurate methods of numerically integrating this.
        delta_t = self.time_history[-1] - self.time_history[-2]
        return np.linalg.norm(self.vel_history[-1] * delta_t)

    def calculate_tangential_friction_force(self, normal_force):
        f_dyn = - self.friction_coefficient * np.linalg.norm(normal_force) * self.get_collision_tangent()
        f_static = - self.friction_stiffness * self.get_tangential_displacement() * self.get_collision_tangent()
        if np.linalg.norm(f_dyn) < np.linalg.norm(f_static):
            return f_dyn
        else:
            return f_static

    def calculate_collision_normal_force(self):
        force = self.stiffness * self.get_particle_overlap() * self.get_collision_normal() \
                - self.damping_coefficient * self.get_normal_velocity()
        return force

    def calculate(self, time):
        self.time_history.append(time)
        self.vel_history.append(self.get_relative_velocity())
        self.pos_history.append(self.p2.pos - self.p1.pos)

        if self.get_particle_overlap() > 0:
            force = self.calculate_collision_normal_force()
            self.p1.dem_forces.append(-force)
            self.p2.dem_forces.append(force)

            if self.friction_stiffness is not None \
                    and self.friction_coefficient is not None \
                    and len(self.time_history) > 1 \
                    and np.linalg.norm(self.get_relative_velocity()) != 0:
                friction = self.calculate_tangential_friction_force(force)
                self.p1.dem_forces.append(-friction)
                self.p2.dem_forces.append(friction)


class AAWallCollision:
    """ Collision object for particle-axis-aligned wall collisions. """
    p = None
    wall = None
    stiffness = None
    damping_coefficient = None

    def __init__(self, particle, wall, stiffness=1, damping_coefficient=None, restitution=None):
        self.p = particle
        self.wall = wall
        self.stiffness = stiffness
        if damping_coefficient is None and restitution is not None:
            self.damping_coefficient = self.calculate_damping_coefficient(restitution)
        elif damping_coefficient is None:
            self.damping_coefficient = 1
        else:
            self.damping_coefficient = damping_coefficient

    def calculate_damping_coefficient(self, restitution):
        ln_rest = math.log(restitution)
        return -2 * ln_rest * (self.p.get_mass() * self.stiffness / (math.pi ** 2 + ln_rest ** 2)) ** 0.5

    def get_collision_normal(self):
        return normalize(np.dot(self.p.pos - self.wall.max, self.wall.normal) * self.wall.normal)

    def get_normal_velocity(self):
        normal = self.get_collision_normal()
        return np.dot(self.p.vel, normal) * normal

    def get_particle_centre_distance(self):
        return np.abs(np.dot(self.wall.max - self.p.pos, self.wall.normal))

    def get_overlap(self):
        return self.p.diameter / 2 - self.get_particle_centre_distance()

    def is_in_wall_bounds(self):
        dif_max = self.wall.max - self.p.pos
        dif_min = self.p.pos - self.wall.min

        # Differences tangential to the wall, ignoring component normal to the wall.
        tang_dif_max = dif_max - dif_max * self.wall.normal
        tang_dif_min = dif_min - dif_min * self.wall.normal
        return all(tang_dif_max >= 0) and all(tang_dif_min >= 0)

    # TODO: Add collision tangential force.

    def calculate_collision_normal_force(self):
        force = self.stiffness * self.get_overlap() * self.get_collision_normal() \
                - self.damping_coefficient * self.get_normal_velocity()
        self.p.dem_forces.append(force)

    def calculate(self):
        if self.get_overlap() > 0 and self.is_in_wall_bounds():
            self.calculate_collision_normal_force()
