import math
import numpy as np

from dem_sim.particle import Particle
import dem_sim
from random import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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


def taylor_green_vortex_sim():
    def get_vel_fluid(self):
        x = self.pos[0]
        y = self.pos[1]
        z = self.pos[2]

        return taylor_green_vortex(x, y, z)

    histories = []
    for i in range(50):
        # Generate random start points.
        x_start = (2 * random() - 1) * math.pi
        y_start = (2 * random() - 1) * math.pi
        z_start = (2 * random() - 1) * math.pi

        p = Particle([x_start, y_start, z_start], [0, 0, 0], gravity=[0, -0.001, 0], get_vel_fluid=get_vel_fluid)

        particle_pos = []

        last_time = 0

        for t in range(500):
            time = t / 10
            p.iterate(time - last_time)
            particle_pos.append(p.pos)
            last_time = time

        particle_pos = np.array(particle_pos)
        histories.append(particle_pos)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for particle_pos in histories:
        ax.plot(particle_pos[:, 0], particle_pos[:, 1], particle_pos[:, 2], color="r")
    plt.show()


dem_sim.util.flow_plot.flow_plot(taylor_green_vortex)
taylor_green_vortex_sim()
