import math
from random import random

import matplotlib.pyplot as plt
import numpy as np

from dem_sim.objects.particle import Particle


def taylor_green_vortex(x, y, z):
    """ Calculates Taylor Green vortex flow velocities. """

    A = 0.14
    B = A
    C = -2 * A
    a = 1
    b = 1
    c = 1

    # Position translated to ensure boundary flow is tangential and continuous.
    x_p = x + (math.pi / (a * 2))
    y_p = y + (math.pi / (a * 2))
    z_p = z + (math.pi / (a * 2))

    u = A * math.cos(a * x_p) * math.sin(b * y_p) * math.sin(c * z_p)
    v = B * math.sin(a * x_p) * math.cos(b * y_p) * math.sin(c * z_p)
    w = C * math.sin(a * x_p) * math.sin(b * y_p) * math.cos(c * z_p)

    return np.array([u, v, w])


def taylor_green_vortex_sim(number_of_particles=50):
    def get_vel_fluid(self):
        x = self.pos[0]
        y = self.pos[1]
        z = self.pos[2]

        return taylor_green_vortex(x, y, z)

    particles = []
    for i in range(number_of_particles):
        # Generate random start points.
        x_start = (2 * random() - 1) * math.pi
        y_start = (2 * random() - 1) * math.pi
        z_start = (2 * random() - 1) * math.pi

        pos = [x_start, y_start, z_start]
        p = Particle(len(particles), 
                     pos, 
                     [0, 0, 0], 
                     diameter=0.001, 
                     get_vel_fluid=get_vel_fluid, 
                     get_gravity=lambda _: [0, 0, 0])

        particles.append(p)

    last_time = 0
    for t in range(500):
        time = t / 10
        [p.iterate(time - last_time) for p in particles]
        last_time = time

    return particles
