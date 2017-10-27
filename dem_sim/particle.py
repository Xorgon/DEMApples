import numpy as np


class Particle:
    GRAVITY = np.array([0, -9.81, 0])
    pos = [0, 0, 0]
    next_pos = [0, 0, 0]
    vel = [0, 0, 0]
    next_vel = [0, 0, 0]
    diameter = 0
    fluid_viscosity = 0
    density = 0

    def __init__(self, position, velocity, diameter=0.001, density=2000, fluid_viscosity=1.93e-5, get_vel_fluid=None):
        self.pos = np.array(position)
        self.vel = velocity
        self.diameter = diameter
        self.density = density
        self.fluid_viscosity = fluid_viscosity

        if callable(get_vel_fluid) and len(get_vel_fluid(self.pos)) == 3:
            self.get_vel_fluid = get_vel_fluid
        elif get_vel_fluid is not None:
            print("get_vel_fluid is not a valid function.")

    def iterate(self, delta_t):
        self.get_accel()
        self.iterate_velocity(delta_t)
        self.iterate_position(delta_t)

        self.vel = self.next_vel
        self.pos = self.next_pos

    def iterate_velocity(self, delta_t):
        self.next_vel = self.vel + delta_t * self.get_accel()

    def iterate_position(self, delta_t):
        self.next_pos = self.pos + delta_t * (self.next_vel + self.vel) / 2

    def get_accel(self):
        return np.array(self.get_drag_accel() + self.get_DEM_accel() + self.GRAVITY)

    def get_drag_accel(self):
        return -(self.vel - np.array(self.get_vel_fluid())) / self.get_tau()

    def get_DEM_accel(self):
        return 0

    def get_tau(self):
        return self.density * self.diameter ** 2 / (18 * self.fluid_viscosity)

    def get_vel_fluid(self):
        return [0, 0, 0]
