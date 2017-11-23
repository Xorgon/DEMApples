import os
import shutil
from dem_sim.util import num_utils


def particles_from_files(filename_root):
    particles = []
    return particles


def particles_to_binary(particles, filename_root, path="", ignore_warnings=False):
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
        file = open(path + filename_root + "_" + str(millis) + ".raw", 'w')
        for p in particles:
            # TODO: Make this actually do binary output and test with ParaView.
            file.write("{0}{1}{2}{3}".format(num_utils.float_to_bin(p.pos_history[i][0]),
                                             num_utils.float_to_bin(p.pos_history[i][1]),
                                             num_utils.float_to_bin(p.pos_history[i][2]),
                                             num_utils.float_to_bin(p.get_speed_at_index(i))))


def particles_to_paraview(particles, filename_root, path="", ignore_warnings=False, fps=60):
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
    log_step = 1 / fps
    last_log = None
    print("At {0} frames per second, logging every {1} seconds.".format(fps, round(log_step, 4)))
    for i in range(len(times)):
        log = False
        if last_log is None:
            last_log = times[i]
            log = True
        elif times[i] - last_log >= log_step:
            last_log = times[i]
            log = True

        if log:
            millis = int(times[i] * 1000)
            file = open(path + filename_root + "_" + str(millis) + ".txt", 'w')
            for p in particles:
                file.write("{0:.5f},{1:.5f},{2:.5f},{3:.5f}\n".format(p.pos_history[i][0], p.pos_history[i][1],
                                                                      p.pos_history[i][2],
                                                                      p.get_speed_at_index(i)))


class Logger:
    # TODO: Add full state logging to allow for simulation continuation in the case of a crash.

    particles = None
    filename_root = None
    path = ""
    ignore_warnings = None
    log_step = None
    last_log = None

    def __init__(self, particles, filename_root, path="", ignore_warnings=False, fps=60):
        self.particles = particles
        self.filename_root = filename_root
        self.path = path
        self.ignore_warnings = ignore_warnings

        self.log_step = 1 / fps

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
        print("At {0} frames per second, logging every {1} seconds.".format(fps, round(self.log_step, 4)))

    def log(self, time):
        log = False
        if self.last_log is None:
            self.last_log = time
            log = True
        elif time - self.last_log >= self.log_step:
            self.last_log = time
            log = True

        if log:
            millis = int(time * 1000)
            file = open(self.path + self.filename_root + "_" + str(millis) + ".txt", 'w')
            for p in self.particles:
                file.write(str(p) + "\n")
