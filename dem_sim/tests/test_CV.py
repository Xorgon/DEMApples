from unittest import TestCase
from random import random as rand
from dem_sim.generators.box import generate_closed_cube_box
from dem_sim.objects.cv import *
from dem_sim.objects.particle import *
from dem_sim.objects.collision import *
import progressbar
import time
import matplotlib.pyplot as plt

from dem_sim.util.file_io import particles_to_paraview


class TestCV(TestCase):
    def test_cv_manager(self):
        manager = CVManager(10, 0.5, -0.5)
        particles = []
        walls = generate_closed_cube_box(1, [0, 0, 0])

        for y in [0.1]:
            for x in np.arange(-0.4, 0.41, 0.2):
                for z in np.arange(-0.4, 0.41, 0.2):
                    pos = np.array([x + 0.05 * (rand() - 0.5), y, z + 0.05 * (rand() - 0.5)])
                    particles.append(Particle(len(particles), pos, np.array([pos[0], 0, pos[2]]), diameter=0.1))

        wall_cols = []
        for p in particles:
            for wall in walls:
                wall_cols.append(
                    AAWallCollision(p, wall, restitution=0.8, friction_coefficient=0.4, friction_stiffness=5e4))

        timestep = 0.0005
        last_time = 0
        max_time = 5
        bar = progressbar.ProgressBar(redirect_stdout=True, max_value=max_time)
        for t in np.arange(0, max_time, timestep):
            manager.add_particles(particles)
            cols = manager.get_collisions()
            bar.update(t)
            delta_t = t - last_time
            for col in cols:
                col.calculate(delta_t)
            for col in wall_cols:
                col.calculate(delta_t)
            for p in particles:
                p.iterate(delta_t, implicit=True)
            last_time = t
            manager.reset()
        bar.finish()
        particles_to_paraview(particles, "cv_test", "../../run/cv_test/", ignore_warnings=True)

    def test_cv_speed(self):
        y_sets = [[0.43],
                  [0.32, 0.43],
                  [0.21, 0.32, 0.43],
                  [0.1, 0.21, 0.32, 0.43]]
        ns = []
        times = []
        for y_set in y_sets:
            start = time.time()
            manager = CVManager(12, 0.5, -0.5)
            particles = []
            walls = generate_closed_cube_box(1, [0, 0, 0])

            for y in y_set:
                for x in np.arange(-0.4, 0.41, 0.2):
                    for z in np.arange(-0.4, 0.41, 0.2):
                        pos = np.array([x + 0.05 * (rand() - 0.5), y, z + 0.05 * (rand() - 0.5)])
                        particles.append(Particle(len(particles), pos, np.array([pos[0], 0, pos[2]]), diameter=0.1))

            ns.append(len(particles))
            print(len(particles))

            wall_cols = []
            for p in particles:
                for wall in walls:
                    wall_cols.append(
                        AAWallCollision(p, wall, restitution=0.8, friction_coefficient=0.4, friction_stiffness=5e4))

            timestep = 0.0005
            last_time = 0
            max_time = 2
            for t in np.arange(0, max_time, timestep):
                manager.add_particles(particles)
                cols = manager.get_collisions()
                delta_t = t - last_time
                for col in cols:
                    col.calculate(delta_t)
                for col in wall_cols:
                    col.calculate(delta_t)
                for p in particles:
                    p.iterate(delta_t, implicit=True)
                last_time = t
                manager.reset()
            run_time = time.time() - start
            times.append(run_time)
            print(run_time)
        plt.plot(ns, times)
        plt.show()

    def test_all_speed(self):
        y_sets = [[0.43],
                  [0.32, 0.43],
                  [0.21, 0.32, 0.43],
                  [0.1, 0.21, 0.32, 0.43]]
        ns = []
        times = []
        for y_set in y_sets:
            start = time.time()
            particles = []
            walls = generate_closed_cube_box(1, [0, 0, 0])

            for y in y_set:
                for x in np.arange(-0.4, 0.41, 0.2):
                    for z in np.arange(-0.4, 0.41, 0.2):
                        pos = np.array([x + 0.05 * (rand() - 0.5), y, z + 0.05 * (rand() - 0.5)])
                        particles.append(Particle(len(particles), pos, np.array([pos[0], 0, pos[2]]), diameter=0.1))

            ns.append(len(particles))
            print(len(particles))

            wall_cols = []
            for p in particles:
                for wall in walls:
                    wall_cols.append(
                        AAWallCollision(p, wall, restitution=0.8, friction_coefficient=0.4, friction_stiffness=5e4))

            cols = []
            for i in range(len(particles)):
                for j in range(i + 1, len(particles)):
                    cols.append(Collision(particles[i], particles[j]))

            for i in range(len(particles)):
                for j in range(i + 1, len(particles)):
                    wall_cols.append(Collision(particles[i], particles[j]))

            timestep = 0.0005
            last_time = 0
            max_time = 2
            for t in np.arange(0, max_time, timestep):
                delta_t = t - last_time
                for col in cols:
                    col.calculate(delta_t)
                for col in wall_cols:
                    col.calculate(delta_t)
                for p in particles:
                    p.iterate(delta_t, implicit=True)
                last_time = t
            run_time = time.time() - start
            times.append(run_time)
            print(run_time)
        plt.plot(ns, times)
        plt.show()
