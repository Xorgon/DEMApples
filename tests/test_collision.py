from unittest import TestCase
from dem_sim.objects.collision import *
from dem_sim.objects.particle import Particle
from dem_sim.util.file_io import particles_to_paraview
import numpy as np
import matplotlib.pyplot as plt


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
            delta_t = time - last_time
            col.calculate(delta_t)
            p1.iterate(delta_t)
            p2.iterate(delta_t)
            last_time = time

        particles_to_paraview([p1, p2], "simple_col", "../run/simple_collision/")

    def test_bouncing_collision(self):
        p1 = Particle([0, 0.5, 0], [0, 0, 0], 0.1)
        p2 = Particle([0, 0, 0], [0, 0, 0], 0.1, density=1e99, gravity=[0, 0, 0])
        col = Collision(p1, p2, 1e5, restitution=0.8)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            delta_t = time - last_time
            col.calculate(delta_t)
            p1.iterate(delta_t)
            p2.iterate(delta_t)
            last_time = time

        predicted_overlap = p1.get_mass() * np.linalg.norm(p1.gravity) / col.stiffness
        print("Predicted overlap = {0}".format(predicted_overlap))
        print("Calculated overlap = {0}".format(col.get_particle_overlap()))
        print("Percentage difference = {0}".format(100 * predicted_overlap / col.get_particle_overlap() - 100))
        TestCase.assertAlmostEqual(self, predicted_overlap, col.get_particle_overlap())
        particles_to_paraview([p1, p2], "bounce_col", "../run/bounce_collision/")

    def test_bouncing_collision_timesteps(self):
        p1 = Particle([0, 0.5, 0], [0, 0, 0], 0.1)
        p2 = Particle([0, 0, 0], [0, 0, 0], 0.1, density=1e99, gravity=[0, 0, 0])
        col = Collision(p1, p2, 1e5, restitution=0.8)

        timesteps = np.arange(0.0005, 0.001, 0.00001)
        overlap_errors = []
        for timestep in timesteps:
            print(timestep)
            last_time = 0
            for time in np.arange(0, 10, timestep):
                delta_t = time - last_time
                col.calculate(delta_t)
                p1.iterate(delta_t)
                p2.iterate(delta_t)
                last_time = time

            predicted_overlap = p1.get_mass() * np.linalg.norm(p1.gravity) / col.stiffness
            percent_dif = 100 * np.abs(col.get_particle_overlap() / predicted_overlap) - 100
            overlap_errors.append(percent_dif)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Percentage error against timestep')
        ax.set_ylabel('Percentage error (%)')
        ax.set_xlabel('Timestep (seconds)')
        ax.plot(timesteps, overlap_errors)
        plt.show()

    def test_offset_bouncing_collision(self):
        ps = []
        coeff = 1
        for y in np.arange(0, 5, 0.5):
            ps.append(Particle([coeff * 0.025, y + 0.5, 0], [0, 0, 0], 0.1))
            coeff *= -1
        p_fixed = Particle([0, 0, 0], [0, 0, 0], 0.1, density=1e99, gravity=[0, 0, 0])
        cols = []
        for p in ps:
            cols.append(Collision(p, p_fixed, 1e5, restitution=0.8, friction_coefficient=0.6, friction_stiffness=1e5))
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                cols.append(
                    Collision(ps[i], ps[j], 1e5, restitution=0.8, friction_coefficient=0.6, friction_stiffness=1e5))
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 3, timestep):
            delta_t = time - last_time
            for col in cols:
                col.calculate(delta_t)
            for p in ps:
                p.iterate(delta_t)
            p_fixed.iterate(delta_t)
            last_time = time

        ps.append(p_fixed)
        particles_to_paraview(ps, "offset_bounce_col", "../run/offset_bounce_collision/")

    def test_wall_bouncing(self):
        p = Particle([0, 0.5, 0], [0, 0, 0], 0.1)
        w = AAWall([1, 0, 1], [-1, 0, -1])
        col = AAWallCollision(p, w)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            delta_t = time - last_time
            col.calculate(delta_t)
            p.iterate(delta_t, implicit=True)
            last_time = time
        print("Final offset = {0}".format(p.pos[1]))
        # TODO: Check offset against calculated value.
        particles_to_paraview([p], "wall_bounce_col", "../run/wall_bounce_collision/", fps=60)

    def test_friction_slide(self):
        p1 = Particle([0.001, 0.1, 0], [0, 0, 0], 0.1)
        p2 = Particle([0, 0, 0], [0, 0, 0], 0.1, density=1e99, gravity=[0, 0, 0])
        col = Collision(p1, p2, 1e5, restitution=0.8, friction_coefficient=0.6, friction_stiffness=1e5)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            delta_t = time - last_time
            col.calculate(delta_t)
            p1.iterate(delta_t)
            p2.iterate(delta_t)
            last_time = time

        particles_to_paraview([p1, p2], "friction_slide", "../run/friction_slide/")

    def test_no_friction_slide(self):
        p1 = Particle([0.001, 0.1, 0], [0, 0, 0], 0.1)
        p2 = Particle([0, 0, 0], [0, 0, 0], 0.1, density=1e99, gravity=[0, 0, 0])
        col = Collision(p1, p2, 1e5, restitution=0.8)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            delta_t = time - last_time
            col.calculate(delta_t)
            p1.iterate(delta_t)
            p2.iterate(delta_t)
            last_time = time

        particles_to_paraview([p1, p2], "no_friction_slide", "../run/no_friction_slide/")

    def test_friction_comparison(self):
        fp1 = Particle([0.001, 0.1, -0.25], [0, 0, 0], 0.1)
        fp2 = Particle([0, 0, -0.25], [0, 0, 0], 0.1, density=1e99, gravity=[0, 0, 0])
        fcol = Collision(fp1, fp2, 1e5, restitution=0.8, friction_coefficient=0.6, friction_stiffness=1e5)

        nfp1 = Particle([0.001, 0.1, 0.25], [0, 0, 0], 0.1)
        nfp2 = Particle([0, 0, 0.25], [0, 0, 0], 0.1, density=1e99, gravity=[0, 0, 0])
        nfcol = Collision(nfp1, nfp2, 1e5, restitution=0.8, friction_coefficient=None, friction_stiffness=None)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            delta_t = time - last_time
            fcol.calculate(delta_t)
            nfcol.calculate(delta_t)
            fp1.iterate(delta_t)
            fp2.iterate(delta_t)
            nfp1.iterate(delta_t)
            nfp2.iterate(delta_t)
            last_time = time

        particles_to_paraview([fp1, fp2, nfp1, nfp2], "friction_comp", "../run/friction_comparison/")

    def test_wall_friction_comparison(self):
        wall = AAWall([1, 0, 1], [-1, 0, -1])

        fp = Particle([0, 0.05, -0.25], [1, 0, 0], 0.1)
        fcol = AAWallCollision(fp, wall, 1e5, restitution=0.8, friction_coefficient=0.6, friction_stiffness=1e5)

        nfp = Particle([0.001, 0.05, 0.25], [1, 0, 0], 0.1)
        nfcol = AAWallCollision(nfp, wall, 1e5, restitution=0.8, friction_coefficient=None, friction_stiffness=None)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            fcol.calculate(time)
            delta_t = time - last_time
            nfcol.calculate(delta_t)
            fp.iterate(delta_t)
            nfp.iterate(delta_t)
            last_time = time

        particles_to_paraview([fp, nfp], "wall_friction_comp", "../run/wall_friction_comparison/")

    def test_side_wall_collision(self):
        p = Particle([1, 0, 0], [-1, 0, 0], 0.1, gravity=[0, 0, 0])
        w = AAWall([-0.5, -0.5, -0.5], [-0.5, 0.5, 0.5])
        col = AAWallCollision(p, w)
        timestep = 0.0005

        last_time = 0
        for time in np.arange(0, 10, timestep):
            delta_t = time - last_time
            col.calculate(delta_t)
            p.iterate(delta_t, implicit=True)
            last_time = time
        print("Final offset = {0}".format(p.pos[1]))
        # TODO: Check offset against calculated value.
        particles_to_paraview([p], "side_wall_col", "../run/side_wall_collision/")
