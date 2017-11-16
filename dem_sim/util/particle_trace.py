import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import math


def trace_animation(particles, trail_length=None, speed=1, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None,
                    zmax=None):
    """
    Animates the given set of particles using their histories.
    :param particles: an array of Particle objects.
    :param trail_length: the number of steps to include in the particle trail.
    :param speed: a mutliplier to determine the speed of motion.
    """
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    ax = p3.Axes3D(fig)

    if xmin is not None and xmax is not None:
        ax.set_xlim(xmin, xmax)
    # y and z axis switched so that particle y coordinates are on the vertical axis.
    if ymin is not None and ymax is not None:
        ax.set_zlim(ymin, ymax)
    if zmin is not None and zmax is not None:
        ax.set_ylim(zmin, zmax)

    for p in particles:
        p.pos_history = np.array(p.pos_history)

    # y and z axis switched so that particle y coordinates are on the vertical axis.
    lines = [ax.plot(p.pos_history[0:1, 0], p.pos_history[0:1, 2], p.pos_history[0:1, 1])[0] for p in particles]

    def update_lines(num, particles, lines):
        num *= speed
        for line, p in zip(lines, particles):
            p_hist_trans = p.pos_history.transpose()

            i = 0
            if trail_length is not None:
                i = num - trail_length
                if i < 0:
                    i = 0
            # y and z axis switched so that particle y coordinates are on the vertical axis.
            line.set_data(p_hist_trans[(0, 2), i:num])
            line.set_3d_properties(p_hist_trans[1, i:num])

    line_ani = animation.FuncAnimation(fig, update_lines, math.ceil(len(particles[0].pos_history) / speed),
                                       fargs=(particles, lines), interval=1, blit=False)
    plt.show()


def trace_plot(particles):
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    ax = fig.gca(projection='3d')

    for particle in particles:
        particle.pos_history = np.array(particle.pos_history)
        # y and z axis switched so that particle y coordinates are on the vertical axis.
        ax.plot(particle.pos_history[:, 0], particle.pos_history[:, 2], particle.pos_history[:, 1], color="r")
    plt.show()
