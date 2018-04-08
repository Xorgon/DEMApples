from dem_sim.objects.collision import *
from dem_sim.objects.particle import Particle
from dem_sim.util.file_io import particles_to_file
import numpy as np
from math import *


def get_mass(density, diameter):
    return density * pi * diameter ** 3 / 6


def normal_collision():
    u_0 = -2
    diameter = 0.1
    stiffness = 1e5
    restitution = 0.8
    density = 2000
    mass = get_mass(density, diameter)

    col_duration = col_duration = pi * sqrt(mass / stiffness)

    for interval in [8, 16, 32, 64]:
        p1 = Particle(1, [0, 0, 0], [0, 0, 0], diameter, density=1e99, get_gravity=lambda dummy: [0, 0, 0])
        p2 = Particle(2, [diameter, 0, 0], [u_0, 0, 0], diameter, density=density, get_gravity=lambda dummy: [0, 0, 0])
        col = Collision(p1, p2, stiffness, restitution=restitution)

        timestep = col_duration / interval

        last_time = 0
        for time in np.arange(0, col_duration + timestep, timestep):
            delta_t = time - last_time
            col.calculate(delta_t)
            p1.iterate(delta_t)
            p2.iterate(delta_t)
            last_time = time
            particles_to_file([p1, p2], "2_normal_force_" + str(interval), "data/", time)


normal_collision()
