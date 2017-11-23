from dem_sim.generators.box import generate_open_cube_box
import numpy as np

from dem_sim.objects.collision import AAWallCollision, Collision
from dem_sim.objects.particle import Particle
from dem_sim.objects.walls import AAWall
from dem_sim.util.file_io import particles_to_paraview


def simple_open_box():
    particles = []
    walls = generate_open_cube_box(1, [0, 0, 0])

    y = 0.5
    for x in np.arange(-0.4, 0.41, 0.2):
        for z in np.arange(-0.4, 0.41, 0.2):
            pos = np.array([x, y, z])
            particles.append(Particle(len(particles), pos, -np.array([pos[0], 0, pos[2]]), diameter=0.1))
    y = 0.35
    for x in np.arange(-0.4, 0.41, 0.2):
        for z in np.arange(-0.4, 0.41, 0.2):
            pos = np.array([x, y, z])
            particles.append(Particle(len(particles), pos, np.array([pos[0], 0, pos[2]]), diameter=0.1))

    cols = []
    for p in particles:
        for wall in walls:
            cols.append(AAWallCollision(p, wall))

    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            cols.append(Collision(particles[i], particles[j]))

    timestep = 0.0005
    last_time = 0
    for time in np.arange(0, 15, timestep):
        delta_t = time - last_time
        for col in cols:
            col.calculate(delta_t)
        for p in particles:
            p.iterate(delta_t, implicit=True)
        last_time = time

    particles_to_paraview(particles, "simple_open_box", "../../run/simple_open_box/")


simple_open_box()
