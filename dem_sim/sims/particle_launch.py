from dem_sim.objects.particle import Particle


def particle_launch():
    p = Particle([0, 0, 0], [0, 10, 0], gravity=[0, -9.81, 0])

    last_time = 0
    for t in range(100):
        time = t / 50
        p.iterate(time - last_time)
        last_time = time
    return [p]
