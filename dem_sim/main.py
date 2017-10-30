import dem_sim
import dem_sim.sims.taylor_green_vortex as tgv


# dem_sim.util.flow_plot.flow_plot(taylor_green_vortex)
particles = tgv.taylor_green_vortex_sim(500)
dem_sim.util.animation.animate_particles(particles, speed=2)
