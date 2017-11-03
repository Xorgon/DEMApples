import os
import shutil
from dem_sim.util import num_utils


def particles_from_files(filename_root):
    particles = []
    return particles


def particles_to_files(particles, filename_root):
    return


def particles_to_paraview(particles, filename_root, path="", ignore_warnings=False, binary=False):
    if os.path.exists(path) and not ignore_warnings:
        ans = input(path + " already exists. Remove and continue? [y/N]\n")
        cont = True
        while cont:
            if ans == "y" or ans == "Y":
                shutil.rmtree(path)
                try:
                    os.mkdir(path)
                except PermissionError:
                    print("PermissionError, path may be active somewhere.")
                    ans = input("Try again? [y/N]\n")
                    continue
                print("Continuing...")
                cont = False
            else:
                print("Ending...")
                return
    elif os.path.exists(path):
        shutil.rmtree(path)
        cont = True
        while cont:
            try:
                os.mkdir(path)
                cont = False
            except PermissionError:
                print("PermissionError, trying again.")
    else:
        os.mkdir(path)

    times = particles[0].times
    for i in range(len(times)):
        millis = int(times[i] * 1000)
        file = open(path + filename_root + "_" + str(millis) + ".txt", 'a')
        for p in particles:
            if binary:
                file.write("{0}{1}{2}{3}".format(num_utils.float_to_bin(p.pos_history[i][0]),
                                                 num_utils.float_to_bin(p.pos_history[i][1]),
                                                 num_utils.float_to_bin(p.pos_history[i][2]),
                                                 num_utils.float_to_bin(p.get_speed_at_index(i))))
            else:
                file.write("{0:.5f},{1:.5f},{2:.5f},{3:.5f}\n".format(p.pos_history[i][0], p.pos_history[i][1],
                                                                      p.pos_history[i][2],
                                                                      p.get_speed_at_index(i)))
