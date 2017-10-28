from unittest import TestCase

import numpy as np

from dem_sim.objects.particle import Particle


class TestParticle(TestCase):
    def test_terminal_velocity(self):
        """ Tests simulated terminal velocity against a calculated value. """
        p = Particle([0, 0, 0], [0, 0, 0])
        times = []
        speeds = []
        last_time = 0
        terminal_velocity_time = None
        for t in range(5000):
            time = t / 100
            p.iterate(time - last_time)
            times.append(time)
            speeds.append(np.linalg.norm(p.vel))
            last_time = time
            if np.abs(np.linalg.norm(p.vel) / 56.442091968912 - 1) < 0.001 and terminal_velocity_time is None:
                terminal_velocity_time = time

        # Uncomment these lines to view speed over time.
        # plot.plot(times, speeds)
        # plot.show()

        # Test if terminal velocity is within 0.1% of a calculated value.
        self.assertLess(np.abs(np.linalg.norm(p.vel) / 56.442091968912 - 1), 0.001)
        # Test if time taken to achieve terminal velocity is greater than the time if only gravity was acting.
        self.assertGreater(terminal_velocity_time, 5.75)
