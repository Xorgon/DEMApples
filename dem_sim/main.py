import dem_sim
import dem_sim.sims.taylor_green_vortex as tgv

# # Plots the flow field with arrows.
# dem_sim.util.flow_plot.flow_plot(tgv.taylor_green_vortex)
# # Runs the taylor green vortex simulation.
particles = tgv.taylor_green_vortex_sim(50)
# # Plots the full trace of the particles.
#dem_sim.util.particle_trace.trace_plot(particles)
# # Animates the full trace of the particles.
anim_1 = dem_sim.util.particle_trace.trace_animation(particles, speed=2)
# # Animates the particles with 15 steps of history at a time.
anim_2 = dem_sim.util.particle_trace.trace_animation(particles, trail_length=15)

# particles = dem_sim.sims.particle_launch.particle_launch()
#dem_sim.util.particle_trace.trace_animation(particles, trail_length=15, speed=0.5, ymin=-3, ymax=3)

#dem_sim.util.file_io.particles_to_paraview(particles, "test", "test_run/", True)
