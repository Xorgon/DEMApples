from math import *
import numpy as np
import matplotlib.pyplot as plt
import os
import re


def calculate_damping_coefficient(stiffness, restitution, m1, m2):
    ln_rest = log(restitution)
    return -2 * ln_rest * (get_reduced_particle_mass(m1, m2) * stiffness / (pi ** 2 + ln_rest ** 2)) ** 0.5


def get_mass(density, diameter):
    return density * pi * diameter ** 3 / 6


def get_reduced_particle_mass(m1, m2):
    return m1 * m2 / (m1 + m2)


def get_pos(time, mass, friction_coeff, u_0, g):
    return - friction_coeff * g * time ** 2 / 2 + u_0 * time


def get_vel(time, mass, friction_coeff, u_0, g):
    return - friction_coeff * g * time + u_0


def plot_pos_and_vel():
    stiffness = 1e5
    density = 2000
    diameter = 0.1
    mass = get_mass(density, diameter)
    restitution = 0.8
    friction_coeff = 0.6
    g = 9.81
    u_0 = 1

    damping_coeff = calculate_damping_coefficient(stiffness, restitution, mass, mass)

    col_duration = pi * sqrt(mass / stiffness)

    # Generate Analytic Solution Data
    t_max = u_0 / (friction_coeff * g)  # From Velocity equation
    # print("t_max = " + str(t_max))
    times = np.arange(0, t_max, col_duration / 16)
    positions = []
    velocities = []

    for t in times:
        positions.append(get_pos(t, mass, friction_coeff, u_0, g))
        velocities.append(get_vel(t, mass, friction_coeff, u_0, g))
    times = np.append(times, 0.5)
    positions.append(positions[-1])
    velocities.append(0)

    # Get Simulation Data
    data = []
    increments = []
    data_dir = os.listdir("data")
    for filename in data_dir:
        name_match = re.match("1_friction_(\d+)_\d+.txt", filename)
        if name_match:
            i = int(name_match.group(1))
            if increments.count(i) == 0:
                increments.append(i)
    increments.sort()
    for i in increments:
        timestep_data = np.array([]).reshape((0, 3))  # Times, Positions, Velocities
        for filename in data_dir:
            name_match = re.match("1_friction_" + str(i) + "_(\d+).txt", filename)
            if name_match:
                time = int(name_match.group(1)) / 1e6
                file = open("data/" + filename, "r")
                line = file.readlines()[0]
                data_match = re.match("(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+)",
                                      line)
                if data_match:
                    timestep_data = np.append(timestep_data,
                                              [[time, float(data_match.group(1)), float(data_match.group(4))]], axis=0)
        timestep_data = timestep_data[timestep_data[:, 0].argsort()]  # Sort by time
        data.append(timestep_data)

    # Normalize Data
    # Normalize Data
    for incr_data in data:
        for n in range(len(incr_data)):
            incr_data[n, 0] = incr_data[n, 0] / col_duration  # Normalize time with collision duration
            incr_data[n, 1] = incr_data[n, 1] / diameter  # Normalize position with particle diameter
            incr_data[n, 2] = incr_data[n, 2] / u_0  # Normalize velocity with initial velocity

    for n in range(len(positions)):
        times[n] = times[n] / col_duration
        positions[n] = positions[n] / diameter
        velocities[n] = velocities[n] / u_0

    # Plot Data
    fig = plt.figure(figsize=(8, 10))
    fig.patch.set_facecolor('white')
    ax1 = fig.add_subplot(211)
    ax1_lines = []
    analytic_line, = ax1.plot(times, positions, 'k', label="Analytic")
    ax1_lines.append(analytic_line)
    for i in range(len(data)):
        timestep_data = data[i]
        timestep_label = "$t_{collision} / " + str(increments[i]) + "$"
        line, = ax1.plot(timestep_data[:, 0], timestep_data[:, 1], '--', label=timestep_label)
        ax1_lines.append(line)
    ax1.set_xlabel('$t / t_{collision}$')
    ax1.set_ylabel('$x / d_p$')
    ax1.legend(handles=ax1_lines, loc=4)

    ax2 = fig.add_subplot(212)
    ax2_lines = []
    analytic_line, = ax2.plot(times, velocities, 'k', label="Analytic")
    ax2_lines.append(analytic_line)
    for i in range(len(data)):
        timestep_data = data[i]
        timestep_label = "$t_{collision} / " + str(increments[i]) + "$"
        line, = ax2.plot(timestep_data[:, 0], timestep_data[:, 2], '--', label=timestep_label)
        ax2_lines.append(line)
    ax2.set_ylabel('$u / u_0$')
    ax2.set_xlabel('$t / t_{collision}$')
    ax2.legend(handles=ax2_lines, loc=1)

    fig.tight_layout()
    plt.show()


plot_pos_and_vel()
