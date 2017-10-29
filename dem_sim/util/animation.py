import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from dem_sim.objects.particle import Particle
import math


def animate_particles(particles, trail_length=None, speed=1):
    """
    Animates the given set of particles using their histories.
    :param particles: an array of Particle objects.
    :param trail_length: the number of steps to include in the particle trail.
    :param speed: a mutliplier to determine the speed of motion.
    """
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    lines = [ax.plot(p.pos_history[0:1, 0], p.pos_history[0:1, 1], p.pos_history[0:1, 2])[0] for p in particles]

    def update_lines(num, particles, lines):
        num *= speed
        for line, p in zip(lines, particles):
            p_hist_trans = p.pos_history.transpose()

            i = 0
            if trail_length is not None:
                i = num - trail_length
            line.set_data(p_hist_trans[0:2, i:num])
            line.set_3d_properties(p_hist_trans[2, i:num])

    line_ani = animation.FuncAnimation(fig, update_lines, math.ceil(len(particles[0].pos_history) / speed),
                                       fargs=(particles, lines), interval=1, blit=False)
    plt.show()
