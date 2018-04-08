from dem_sim.objects.collision import *
from dem_sim.objects.particle import Particle
from dem_sim.util.file_io import particles_to_file
import numpy as np
from math import *


def get_mass(density, diameter):
    return density * pi * diameter ** 3 / 6


def get_vel_fluid(self):
    return self.vel


def friction():
    u_0 = 1
    diameter = 0.1
    stiffness = 1e5
    restitution = 0.8
    density = 2000
    mass = get_mass(density, diameter)

    theoretical_overlap = get_mass(density, diameter) * 9.81 / stiffness

    col_duration = pi * sqrt(mass / stiffness)

    wall = AAWall([50, 0, 50], [-50, 0, -50])

    for interval in [8, 16, 32, 64]:
        fp = Particle(1, [0, diameter / 2 - theoretical_overlap, 0], [u_0, 0, 0], diameter)
        fcol = AAWallCollision(fp, wall, 1e5, restitution=0.8, friction_coefficient=0.6, friction_stiffness=1e8)

        timestep = col_duration / interval

        last_time = 0
        log_step = 0.01
        last_log = None

        for time in np.arange(0, 0.5 + timestep, timestep):
            delta_t = time - last_time
            fcol.calculate(delta_t)
            fp.iterate(delta_t)
            last_time = time
            if last_log is None or time - last_log >= log_step:
                particles_to_file([fp], "1_friction_" + str(interval), "data/", time)
                last_log = time


friction()
