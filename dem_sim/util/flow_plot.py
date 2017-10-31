import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np


def flow_plot(flow_vel_func, b_min=-math.pi, b_max=math.pi, step=0.5, ):
    """
    Plots the flow for a given flow velocity function.

    :param flow_vel_func: A function that takes three numbers x,y,z and returns a numpy array of length 3.
    :param b_min: Minimum boundary. Default: -pi
    :param b_max: Maximum boundary. Default: pi
    :param step: Distance between points: 0.5.
    """

    if not callable(flow_vel_func):
        print("flow_vel_func is not a valid flow velocity function.")

    positions = []
    velocities = []
    for x in np.arange(b_min, b_max, step):
        for y in np.arange(b_min, b_max, step):
            for z in np.arange(b_min, b_max, step):
                positions.append(np.array([x, y, z]))
                velocities.append(flow_vel_func(x, y, z))

    positions = np.array(positions)
    velocities = np.array(velocities)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # y and z axis switched so that particle y coordinates are on the vertical axis.
    ax.quiver(positions[:, 0], positions[:, 2], positions[:, 1], velocities[:, 0], velocities[:, 2], velocities[:, 1]
              , length=0.25)
    plt.show()
