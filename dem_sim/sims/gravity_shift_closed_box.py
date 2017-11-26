import math
from random import random as rand

import numpy as np
import progressbar

from dem_sim.generators.box import generate_closed_cube_box
from dem_sim.objects.collision import AAWallCollision
from dem_sim.objects.cv import CVManager
from dem_sim.objects.particle import Particle, LowMemParticle
from dem_sim.util.file_io import particles_to_paraview, Logger


def gravity_shift_closed_box():
    manager = CVManager(10, 0.5, -0.5)
    particles = []
    walls = generate_closed_cube_box(1, [0, 0, 0])

    def get_gravity(self):
        time_fact = 0.25 * self.time * self.time
        return [9.81 * math.sin(time_fact), -9.81 * math.cos(time_fact), 0]

    for y in [-0.18, -0.07, 0.1, 0.21, 0.32, 0.43]:
        for x in np.arange(-0.4, 0.41, 0.2):
            for z in np.arange(-0.4, 0.41, 0.2):
                pos = np.array([x + 0.05 * (rand() - 0.5), y, z + 0.05 * (rand() - 0.5)])
                particles.append(
                    LowMemParticle(len(particles), pos, np.array([pos[0], 0, pos[2]]), diameter=0.1,
                                   get_gravity=get_gravity))

    wall_cols = []
    for p in particles:
        for wall in walls:
            wall_cols.append(
                AAWallCollision(p, wall, restitution=0.8, friction_coefficient=0.4, friction_stiffness=5e4))

    timestep = 0.0005
    last_time = 0
    max_time = 30
    logger = Logger(particles, "accel_gravity_shift_closed_box", "../../run/accel_gravity_shift_closed_box/",
                    ignore_warnings=True)
    logger.log(0)
    bar = progressbar.ProgressBar(redirect_stdout=True, max_value=max_time)
    for t in np.arange(0, max_time, timestep):
        bar.update(t)
        manager.add_particles(particles)  # Kernel to set CV particle lists. (Pass over all particles).
        p_cols = manager.get_collisions()  # Kernel to get collisions from CVs. (Pass over all CVs).
        delta_t = t - last_time
        for col in p_cols + wall_cols:
            col.calculate(delta_t)  # Kernel to calculate all collisions. (Pass over all collisions).
        for p in particles:
            p.iterate(delta_t, implicit=True)  # Kernel to iterate all particles. (Pass over all particles).
        last_time = t
        manager.reset()
        logger.log(t)
    bar.finish()


gravity_shift_closed_box()
