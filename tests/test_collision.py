from unittest import TestCase
from dem_sim.objects.collision import Collision
from dem_sim.objects.particle import Particle
from dem_sim.util.file_io import particles_to_paraview
import numpy as np


class TestCollision(TestCase):
    def test_get_collision_normal(self):
        p1 = Particle([0, 0, 0], [0, 0, 0])
        p2 = Particle([1, 1, 1], [0, 0, 0])
        col = Collision(p1, p2)
        TestCase.assertAlmostEquals(self,
                                    np.linalg.norm(
                                        col.get_collision_normal() - (np.array([1, 1, 1]) / np.linalg.norm([1, 1, 1]))),
                                    0)

    def test_simple_collision(self):
        p1 = Particle([0, 0, 0], [0.1, 0, 0], 0.1, gravity=[0, 0, 0])
        p2 = Particle([1, 0, 0], [-0.1, 0, 0], 0.1, gravity=[0, 0, 0])
        col = Collision(p1, p2, 1e4, restitution=0.8)
        timestep = 0.001

        last_time = 0
        for time in np.arange(0, 10, timestep):
            col.calculate()
            p1.iterate(time - last_time)
            p2.iterate(time - last_time)
            last_time = time

        particles_to_paraview([p1, p2], "simple_col", "simple_collision/")

    def test_bouncing_collision(self):
        p1 = Particle([0, 0.5, 0], [0, 0, 0], 0.1)
        p2 = Particle([0, 0, 0], [0, 0, 0], 0.1, density=1e10, gravity=[0, 0, 0])
        col = Collision(p1, p2, 1e5, restitution=0.8)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            col.calculate()
            p1.iterate(time - last_time)
            p2.iterate(time - last_time)
            last_time = time

        TestCase.assertLess(self, p1.get_speed(), 1e-4)
        particles_to_paraview([p1, p2], "bounce_col", "bounce_collision/")

    def test_offset_bouncing_collision(self):
        ps = []
        coeff = 1
        for y in np.arange(0, 5, 0.5):
            ps.append(Particle([coeff * 0.025, y + 0.5, 0], [0, 0, 0], 0.1))
            coeff *= -1
        p_fixed = Particle([0, 0, 0], [0, 0, 0], 0.1, density=1e10, gravity=[0, 0, 0])
        cols = []
        for p in ps:
            cols.append(Collision(p, p_fixed, 1e5, restitution=0.8))
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            for col in cols:
                col.calculate()
            for p in ps:
                p.iterate(time - last_time)
            p_fixed.iterate(time - last_time)
            last_time = time

        ps.append(p_fixed)
        particles_to_paraview(ps, "offset_bounce_col", "offset_bounce_collision/")
