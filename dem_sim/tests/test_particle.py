from unittest import TestCase

import numpy as np
import matplotlib.pyplot as plt
import math

from dem_sim.objects.particle import Particle
import dem_sim.util.vector_utils as vect


class TestParticle(TestCase):
    def test_terminal_velocity(self):
        """ Tests simulated terminal velocity against a calculated value. """
        data = []
        for timestep in [0.1, 1, 2, 3, 4, 5, 6]:
            p = Particle([0, 0, 0], [0, 0, 0])
            times = []
            speeds = []
            last_time = 0
            for time in np.arange(0, 40, timestep):
                p.iterate(time - last_time)
                times.append(time)
                speeds.append(vect.mag(p.vel))
                last_time = time
            data.append([times, speeds])

        fig = plt.figure()
        fig.patch.set_facecolor('white')
        ax = fig.gca()
        for d in data:
            ax.plot(d[0], d[1])
        plt.show()
        # TODO: Analytical solution and comparison.
        # Test if terminal velocity is within 0.1% of a calculated value.
        self.assertLess(np.abs(vect.mag(data[0][1][-1]) / 56.442091968912 - 1), 0.001)

    def test_terminal_velocity_implicit_explicit(self):
        """ Tests simulated terminal velocity against a calculated value using implicit and explicit integration. """
        data = []
        for timestep in [1]:
            p_implicit = Particle([0, 0, 0], [0, 0, 0])
            p_explicit = Particle([0, 0, 0], [0, 0, 0])
            times = []
            explicit = []
            implicit = []
            analytic = []
            last_time = 0
            for time in np.arange(0, 40, timestep):
                p_explicit.iterate(time - last_time, implicit=False)
                p_implicit.iterate(time - last_time, implicit=True)
                times.append(time)
                explicit.append(vect.mag(p_explicit.vel))
                implicit.append(vect.mag(p_implicit.vel))
                tau = p_explicit.get_tau()
                analytic.append(-9.81 * tau * math.exp(-time / tau) + 9.81 * tau)
                last_time = time
            data.append([times, explicit])
            data.append([times, implicit])
            data.append([times, analytic])

        fig = plt.figure()
        fig.patch.set_facecolor('white')
        ax = fig.gca()
        plots = []
        for d in data:
            plots.append(ax.plot(d[0], d[1])[0])
        ax.set_xlabel('Time ($s$)')
        ax.set_ylabel(r'Speed ($ms^{-1}$)')
        plt.legend(plots, ['Explicit', 'Implicit', 'Analytic'], loc=4)
        plt.show()
        print("Explicit terminal velocity = {0}".format(vect.mag(data[0][1][-1])))
        print("Implicit terminal velocity = {0}".format(vect.mag(data[1][1][-1])))
        # Test if terminal velocity is within 0.1% of a calculated value.

        explicit_diff_sum = 0
        implicit_diff_sum = 0
        length = len(data[0][0])
        for i in range(1, length):  # Start at 1 to avoid division by zero at the initial conditions.
            explicit_diff_sum += (data[0][1][i] - data[2][1][i]) / data[2][1][i]
            implicit_diff_sum += (data[1][1][i] - data[2][1][i]) / data[2][1][i]
        explicit_avg = 100 * np.abs(explicit_diff_sum / length)
        print("Explicit average percentage difference = {0}".format(explicit_avg))
        implicit_avg = 100 * np.abs(implicit_diff_sum / length)
        print("Implicit average percentage difference = {0}".format(implicit_avg))

        self.assertLess(np.abs(vect.mag(data[0][1][-1]) / 56.442091968912 - 1), 0.001)

    def test_drag_velocity_implicit_explicit(self):
        """ Tests simulated terminal velocity against a calculated value using implicit and explicit integration. """
        v = 5  # Fluid speed

        def get_vel_fluid(pos):
            return [v, 0, 0]

        timesteps = np.arange(0.01, 5, 0.01)
        explicit_avgs = []
        implicit_avgs = []

        for timestep in timesteps:
            p_implicit = Particle([0, 0, 0], [0, 0, 0], get_vel_fluid=get_vel_fluid, gravity=[0, 0, 0])
            p_explicit = Particle([0, 0, 0], [0, 0, 0], get_vel_fluid=get_vel_fluid, gravity=[0, 0, 0])
            times = []
            explicit = []
            implicit = []
            analytic = []
            last_time = 0
            data = []

            for time in np.arange(0, 40, timestep):
                p_explicit.iterate(time - last_time, implicit=False)
                p_implicit.iterate(time - last_time, implicit=True)
                times.append(time)
                explicit.append(vect.mag(p_explicit.vel))
                implicit.append(vect.mag(p_implicit.vel))
                tau = p_explicit.get_tau()
                analytic.append(v * (1 - math.exp(- time / tau)))
                last_time = time
            data.append([times, explicit])
            data.append([times, implicit])
            data.append([times, analytic])

            # fig = plt.figure()
            # ax = fig.gca()
            # plots = []
            # for d in data:
            #     plots.append(ax.plot(d[0], d[1])[0])
            # ax.set_xlabel('Time ($s$)')
            # ax.set_ylabel(r'Speed ($ms^{-1}$)')
            # plt.legend(plots, ['Explicit', 'Implicit', 'Analytic'], loc=4)
            # plt.show()

            explicit_diff_sum = 0
            implicit_diff_sum = 0
            length = len(data[0][0])
            for i in range(1, length):  # Start at 1 to avoid division by zero at the initial conditions.
                explicit_diff_sum += (data[0][1][i] - data[2][1][i]) / data[2][1][i]
                implicit_diff_sum += (data[1][1][i] - data[2][1][i]) / data[2][1][i]
            explicit_avg = 100 * np.abs(explicit_diff_sum / length)
            # print("Explicit average percentage difference = {0}".format(explicit_avg))
            implicit_avg = 100 * np.abs(implicit_diff_sum / length)
            # print("Implicit average percentage difference = {0}".format(implicit_avg))
            explicit_avgs.append(explicit_avg)
            implicit_avgs.append(implicit_avg)

        fig = plt.figure()
        fig.patch.set_facecolor('white')
        ax = fig.gca()
        explicit_avgs_plot, = ax.plot(timesteps, explicit_avgs)
        implicit_avgs_plot, = ax.plot(timesteps, implicit_avgs)
        ax.set_xlabel('Timestep ($s$)')
        ax.set_ylabel(r'Average percentage difference')
        plt.legend([explicit_avgs_plot, implicit_avgs_plot], ['Explicit', 'Implicit'], loc=4)
        plt.show()
