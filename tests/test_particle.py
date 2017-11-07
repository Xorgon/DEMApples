from unittest import TestCase

import numpy as np
import matplotlib.pyplot as plt

from dem_sim.objects.particle import Particle


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
                speeds.append(np.linalg.norm(p.vel))
                last_time = time
            data.append([times, speeds])

        fig = plt.figure()
        ax = fig.gca()
        for d in data:
            ax.plot(d[0], d[1])
        plt.show()
        # TODO: Analytical solution and comparison.
        # Test if terminal velocity is within 0.1% of a calculated value.
        self.assertLess(np.abs(np.linalg.norm(data[0][1][-1]) / 56.442091968912 - 1), 0.001)
