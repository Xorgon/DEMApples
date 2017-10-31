import dem_sim
import dem_sim.sims.taylor_green_vortex as tgv

# Plots the flow field with arrows.
# dem_sim.util.flow_plot.flow_plot(tgv.taylor_green_vortex)
# # Runs the taylor green vortex simulation.
# particles = tgv.taylor_green_vortex_sim()
# # Plots the full trace of the particles.
# dem_sim.util.particle_trace.trace_plot(particles)
# # Animates the full trace of the particles.
# dem_sim.util.particle_trace.trace_animation(particles, speed=2)
# # Animates the particles with 15 steps of history at a time.
# dem_sim.util.particle_trace.trace_animation(particles, trail_length=15)

particles = dem_sim.sims.particle_launch.particle_launch()
dem_sim.util.particle_trace.trace_animation(particles, trail_length=15, speed=0.5, ymin=-3, ymax=3)
