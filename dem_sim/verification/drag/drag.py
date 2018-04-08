from dem_sim.objects.collision import *
from dem_sim.objects.particle import Particle
from dem_sim.util.file_io import particles_to_file
import numpy as np
from math import *


def get_mass(density, diameter):
    return density * pi * diameter ** 3 / 6


def drag():
    u_0 = -2
    diameter = 0.1
    density = 10
    mass = get_mass(density, diameter)
    fluid_vel = 1
    fluid_viscosity = 0.00193

    tau = density * diameter ** 2 / (18 * fluid_viscosity)
    sim_length = 5 * tau

    for interval in [8, 16, 32, 64]:
        p1 = Particle(1, [0, 0, 0], [0, 0, 0], diameter, density=density, get_gravity=lambda dummy: [0, 0, 0],
                      get_vel_fluid=lambda dummy: [fluid_vel, 0, 0], fluid_viscosity=fluid_viscosity)

        timestep = tau / interval

        last_time = 0
        for time in np.arange(0, sim_length + timestep, timestep):
            delta_t = time - last_time
            p1.iterate(delta_t)
            last_time = time
            particles_to_file([p1], "1_drag_" + str(interval), "data/", time)


drag()
