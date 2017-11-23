from dem_sim.generators.box import generate_closed_cube_box
import numpy as np

from dem_sim.objects.collision import AAWallCollision, Collision
from dem_sim.objects.cv import CVManager
from dem_sim.objects.particle import Particle
from dem_sim.objects.walls import AAWall
from dem_sim.util.file_io import particles_to_paraview
from random import random as rand

import progressbar


def simple_closed_box():
    manager = CVManager(10, 0.5, -0.5)
    particles = []
    walls = generate_closed_cube_box(1, [0, 0, 0])

    for y in [-0.18, -0.07, 0.1, 0.21, 0.32, 0.43]:
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
    max_time = 15
    bar = progressbar.ProgressBar(redirect_stdout=True, max_value=max_time)
    for t in np.arange(0, max_time, timestep):
        bar.update(t)
        manager.add_particles(particles)
        p_cols = manager.get_collisions()
        delta_t = t - last_time
        for col in p_cols + wall_cols:
            col.calculate(delta_t)
        for p in particles:
            p.iterate(delta_t, implicit=True)
        last_time = t
        manager.reset()
    bar.finish()
    particles_to_paraview(particles, "simple_closed_box", "../../run/simple_closed_box/")


simple_closed_box()
