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


def get_pos(time, relaxation_time, fluid_velocity):
    return fluid_velocity * relaxation_time * (pow(e, - time / relaxation_time) - 1) + fluid_velocity * time


def get_vel(time, relaxation_time, fluid_velocity):
    return fluid_velocity * (1 - pow(e, -time / relaxation_time))


def plot_pos_and_vel():
    density = 10
    diameter = 0.1
    fluid_viscosity = 0.00193
    fluid_velocity = 1
    tau = density * diameter ** 2 / (18 * fluid_viscosity)
    print(tau)

    # Generate Analytic Solution Data
    times = np.arange(0, 5 * tau, tau / 64)
    positions = []
    velocities = []

    for t in times:
        positions.append(get_pos(t, tau, fluid_velocity))
        velocities.append(get_vel(t, tau, fluid_velocity))

    # Get Simulation Data
    data = []
    increments = []
    data_dir = os.listdir("data")
    for filename in data_dir:
        name_match = re.match("1_drag_(\d+)_\d+.txt", filename)
        if name_match:
            i = int(name_match.group(1))
            if increments.count(i) == 0:
                increments.append(i)
    increments.sort()
    for i in increments:
        timestep_data = np.array([]).reshape((0, 3))  # Times, Positions, Velocities
        for filename in data_dir:
            name_match = re.match("1_drag_" + str(i) + "_(\d+).txt", filename)
            if name_match:
                time = int(name_match.group(1)) / 1e6
                file = open("data/" + filename, "r")
                line = file.readlines()[0]
                data_match = re.match("(\d+\.\d+),(\d+\.\d+),(\d+\.\d+),(-?\d+\.\d+),(\d+\.\d+),(\d+\.\d+)", line)
                if data_match:
                    timestep_data = np.append(timestep_data,
                                              [[time, float(data_match.group(1)), float(data_match.group(4))]], axis=0)
        timestep_data = timestep_data[timestep_data[:, 0].argsort()]  # Sort by time
        data.append(timestep_data)

    # Normalize Data
    for incr_data in data:
        for n in range(len(incr_data)):
            incr_data[n, 0] = incr_data[n, 0] / tau  # Normalize time with collision duration
            incr_data[n, 1] = incr_data[n, 1] / diameter  # Normalize position with particle diameter
            incr_data[n, 2] = incr_data[n, 2] / fluid_velocity  # Normalize velocity with initial velocity

    for n in range(len(positions)):
        times[n] = times[n] / tau
        positions[n] = positions[n] / diameter
        velocities[n] = velocities[n] / fluid_velocity

    # Plot Data
    fig = plt.figure(figsize=(8, 10))
    fig.patch.set_facecolor('white')
    ax1 = fig.add_subplot(211)
    ax1_lines = []
    analytic_line, = ax1.plot(times, positions, 'k', label="Analytic")
    ax1_lines.append(analytic_line)
    for i in range(len(data)):
        timestep_data = data[i]
        timestep_label = "$\\tau / " + str(increments[i]) + "$"
        line, = ax1.plot(timestep_data[:, 0], timestep_data[:, 1], '--', label=timestep_label)
        ax1_lines.append(line)
    ax1.set_xlabel('$t / \\tau$')
    ax1.set_ylabel('$x / d_p$')
    ax1.legend(handles=ax1_lines, loc=4)

    ax2 = fig.add_subplot(212)
    ax2_lines = []
    analytic_line, = ax2.plot(times, velocities, 'k', label="Analytic")
    ax2_lines.append(analytic_line)
    for i in range(len(data)):
        timestep_data = data[i]
        timestep_label = "$\\tau / " + str(increments[i]) + "$"
        line, = ax2.plot(timestep_data[:, 0], timestep_data[:, 2], '--', label=timestep_label)
        ax2_lines.append(line)
    ax2.set_ylabel('$u / v$')
    ax2.set_xlabel('$t / \\tau$')
    ax2.legend(handles=ax2_lines, loc=1)

    fig.tight_layout()
    plt.show()


plot_pos_and_vel()
