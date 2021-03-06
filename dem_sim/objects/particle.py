import numpy as np
import math
import dem_sim.util.vector_utils as vect


class Particle:
    pid = None
    pos = None
    next_pos = None
    vel = None
    next_vel = None
    diameter = None
    fluid_viscosity = None
    density = None

    time = None
    times = None
    pos_history = None
    vel_history = None

    dem_forces = None

    def __init__(self, pid, position, velocity, diameter=0.1, density=2000, fluid_viscosity=1.93e-5, get_vel_fluid=None,
                 get_gravity=None):
        self.pos = np.array(position)
        self.vel = np.array(velocity)
        self.diameter = diameter
        self.density = density
        self.fluid_viscosity = fluid_viscosity

        self.pid = pid

        self.time = 0
        self.times = []
        self.pos_history = []
        self.vel_history = []

        self.dem_forces = []

        if callable(get_vel_fluid) and len(get_vel_fluid(self)) == 3:
            self.get_vel_fluid = get_vel_fluid
        elif get_vel_fluid is not None:
            print("get_vel_fluid is not a valid function.")
        else:
            self.get_vel_fluid = lambda dummy: [0, 0, 0]

        if callable(get_gravity) and len(get_gravity(self)) == 3:
            self.get_gravity = get_gravity
        elif get_gravity is not None:
            print("get_gravity is not a valid function.")
        else:
            self.get_gravity = lambda delta_t: [0, -9.81, 0]

    def iterate(self, delta_t, implicit=True):
        self.time += delta_t

        self.iterate_velocity(delta_t, implicit)
        self.iterate_position(delta_t)

        self.vel = self.next_vel
        self.pos = self.next_pos

        self.record_state()
        self.dem_forces.clear()

    def iterate_velocity(self, delta_t, implicit):
        self.next_vel = self.vel + delta_t * self.get_accel(delta_t, implicit)

    def iterate_position(self, delta_t):
        self.next_pos = self.pos + delta_t * (self.next_vel + self.vel) / 2

    def get_accel(self, delta_t, implicit):
        if not implicit:
            return np.array(self.get_drag_accel() + self.get_dem_accel() + self.get_gravity(self))
        else:
            return self.get_accel_implicit_drag(delta_t)

    def get_accel_implicit_drag(self, delta_t):
        non_drag_a = self.get_dem_accel() + self.get_gravity(self)
        v = self.get_vel_fluid(self)
        return (v - self.vel + self.get_tau() * non_drag_a) / (self.get_tau() + delta_t)

    def get_drag_accel(self):
        return -(self.vel - np.array(self.get_vel_fluid(self))) / self.get_tau()

    def get_dem_accel(self):
        total_dem_force = np.sum(self.dem_forces, 0)
        return total_dem_force / self.get_mass()

    # Useful values.

    def get_tau(self):
        return self.density * self.diameter ** 2 / (18 * self.fluid_viscosity)

    def get_speed(self):
        return vect.mag(self.vel)

    def get_speed_at_time(self, time):
        try:
            index = self.times.index(time)
            return vect.mag(self.vel_history[index])
        except ValueError:
            return 0

    def get_speed_at_index(self, index):
        return vect.mag(self.vel_history[index])

    def get_mass(self):
        return self.density * math.pi * self.diameter ** 3 / 6

    def get_kinetic_energy(self):
        return 0.5 * self.get_mass() + self.get_speed() ** 2

    def record_state(self):
        """ Records current position, velocity, and time. """
        self.vel_history.append(self.vel.copy())
        self.pos_history.append(self.pos.copy())
        self.times.append(self.time)

    def __str__(self):
        return "{0:.5f},{1:.5f},{2:.5f},{3:.5f}\n".format(self.pos[0], self.pos[1], self.pos[2], self.get_speed())


class LowMemParticle(Particle):
    """ Same as Particle but without full history tracking. """

    def __init__(self, pid, position, velocity, diameter=0.1, density=2000, fluid_viscosity=1.93e-5, get_vel_fluid=None,
                 get_gravity=None):
        super().__init__(pid, position, velocity, diameter, density, fluid_viscosity, get_vel_fluid, get_gravity)
        self.times = None
        self.pos_history = None
        self.vel_history = None

    def iterate(self, delta_t, implicit=False):
        self.time += delta_t

        self.iterate_velocity(delta_t, implicit)
        self.iterate_position(delta_t)

        self.vel = self.next_vel
        self.pos = self.next_pos

        self.dem_forces.clear()
