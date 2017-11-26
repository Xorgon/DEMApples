from dem_sim.objects.particle import Particle
from dem_sim.objects.walls import AAWall
import dem_sim.util.vector_utils as vect
import numpy as np
import math


# TODO: Add cohesion/adhesion.

class Collision:
    """ Collision object for particle-particle collisions. """
    p1 = None
    p2 = None
    stiffness = None
    damping_coefficient = None
    friction_coefficient = None
    friction_stiffness = None

    last_kinetic_energy = None

    def __init__(self, particle1, particle2, stiffness=1e5, damping_coefficient=None, restitution=0.8,
                 friction_coefficient=0.6, friction_stiffness=1e5):
        self.p1 = particle1
        self.p2 = particle2
        self.stiffness = stiffness

        if damping_coefficient is None:
            self.damping_coefficient = self.calculate_damping_coefficient(restitution)
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
        return vect.normalize(self.p2.pos - self.p1.pos)

    def get_relative_velocity(self):
        return self.p2.vel - self.p1.vel

    def get_normal_velocity(self):
        normal = self.get_collision_normal()
        return np.dot((self.get_relative_velocity()), normal) * normal

    def get_particle_centre_separation(self):
        return vect.mag(self.p2.pos - self.p1.pos)

    def get_collision_tangent(self):
        vel_relative = self.get_relative_velocity()
        return vect.normalize(vel_relative - self.get_normal_velocity())

    def get_tangential_displacement(self, delta_t):
        # TODO: Investigate more accurate methods of numerically integrating this.
        return vect.mag((self.get_relative_velocity() - self.get_normal_velocity()) * delta_t)

    def calculate_tangential_friction_force(self, normal_force, delta_t):
        f_dyn = - self.friction_coefficient * vect.mag(normal_force) * self.get_collision_tangent()
        f_static = - self.friction_stiffness * self.get_tangential_displacement(delta_t) * self.get_collision_tangent()
        if vect.mag_squared(f_dyn) < vect.mag_squared(f_static):
            return f_dyn
        else:
            return f_static

    def calculate_collision_normal_force(self):
        force = self.stiffness * self.get_particle_overlap() * self.get_collision_normal() \
                - self.damping_coefficient * self.get_normal_velocity()
        return force

    def get_particle_overlap(self):
        return self.p1.diameter / 2 + self.p2.diameter / 2 - self.get_particle_centre_separation()

    def calculate(self, delta_t):
        self.last_kinetic_energy = self.p1.get_kinetic_energy() + self.p2.get_kinetic_energy()
        if self.get_particle_overlap() > 0:
            force = self.calculate_collision_normal_force()
            self.p1.dem_forces.append(-force)
            self.p2.dem_forces.append(force)

            if self.friction_stiffness is not None and self.friction_coefficient is not None:
                friction = self.calculate_tangential_friction_force(force, delta_t)
                self.p1.dem_forces.append(-friction)
                self.p2.dem_forces.append(friction)

    def check_total_kinetic_energy(self):
        """ Checks the current kinetic energy of the collision against the last kinetic energy. """
        # TODO: May break for multi-particle collision situations or moving flows. Implement within calculate?
        correct = self.p1.get_kinetic_energy() + self.p2.get_kinetic_energy < self.last_kinetic_energy
        if not correct:
            print("Warning: Kinetic energy greater than last kinetic energy.")
        return correct


class AAWallCollision:
    """ Collision object for particle-axis-aligned wall collisions. """
    p = None
    wall = None
    stiffness = None
    damping_coefficient = None
    friction_coefficient = None
    friction_stiffness = None

    def __init__(self, particle, wall, stiffness=1e5, damping_coefficient=None, restitution=0.8,
                 friction_coefficient=0.6,
                 friction_stiffness=1e5):
        self.p = particle
        self.wall = wall
        self.stiffness = stiffness

        if damping_coefficient is None:
            self.damping_coefficient = self.calculate_damping_coefficient(restitution)
        else:
            self.damping_coefficient = damping_coefficient

        self.friction_coefficient = friction_coefficient
        self.friction_stiffness = friction_stiffness

    def calculate_damping_coefficient(self, restitution):
        ln_rest = math.log(restitution)
        return -2 * ln_rest * (self.p.get_mass() * self.stiffness / (math.pi ** 2 + ln_rest ** 2)) ** 0.5

    def get_collision_normal(self):
        return vect.normalize(np.dot(self.p.pos - self.wall.max, self.wall.normal) * self.wall.normal)

    def get_normal_velocity(self):
        normal = self.get_collision_normal()
        return np.dot(self.p.vel, normal) * normal

    def get_particle_centre_distance(self):
        return np.abs(np.dot(self.wall.max - self.p.pos, self.wall.normal))

    def get_collision_tangent(self):
        return vect.normalize(self.p.vel - self.get_normal_velocity())

    def get_tangential_displacement(self, vel, delta_t):
        # TODO: Investigate more accurate methods of numerically integrating this.
        return vect.mag(vel * delta_t)

    def calculate_tangential_friction_force(self, normal_force, vel, delta_t):
        f_dyn = - self.friction_coefficient * vect.mag(normal_force) * self.get_collision_tangent()
        f_static = - self.friction_stiffness * self.get_tangential_displacement(vel,
                                                                                delta_t) * self.get_collision_tangent()
        if vect.mag_squared(f_dyn) < vect.mag_squared(f_static):
            return f_dyn
        else:
            return f_static

    def calculate_collision_normal_force(self):
        force = self.stiffness * self.get_overlap() * self.get_collision_normal() \
                - self.damping_coefficient * self.get_normal_velocity()
        return force

    def get_overlap(self):
        return self.p.diameter / 2 - self.get_particle_centre_distance()

    def is_in_wall_bounds(self):
        dif_max = self.wall.max - self.p.pos
        dif_min = self.p.pos - self.wall.min

        # Differences tangential to the wall, ignoring component normal to the wall.
        normal = self.get_collision_normal()
        tang_dif_max = dif_max - np.dot(dif_max, normal) * normal
        tang_dif_min = dif_min - np.dot(dif_min, normal) * normal
        return all(tang_dif_max >= 0) and all(tang_dif_min >= 0)

    def calculate(self, delta_t):

        if self.get_overlap() > 0 and self.is_in_wall_bounds():
            force = self.calculate_collision_normal_force()
            self.p.dem_forces.append(force)

            if self.friction_stiffness is not None and self.friction_coefficient is not None:
                friction = self.calculate_tangential_friction_force(force, self.p.vel, delta_t)
                self.p.dem_forces.append(friction)
