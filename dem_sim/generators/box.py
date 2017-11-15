from dem_sim.objects.walls import AAWall


def generate_open_cube_box(length, center):
    c_x = center[0]
    c_y = center[1]
    c_z = center[2]

    walls = [AAWall([c_x - length / 2, c_y - length / 2, c_z - length / 2],
                    [c_x - length / 2, c_y + length / 2, c_z + length / 2]),
             AAWall([c_x - length / 2, c_y - length / 2, c_z - length / 2],
                    [c_x + length / 2, c_y - length / 2, c_z + length / 2]),
             AAWall([c_x - length / 2, c_y - length / 2, c_z - length / 2],
                    [c_x + length / 2, c_y + length / 2, c_z - length / 2]),
             AAWall([c_x + length / 2, c_y + length / 2, c_z + length / 2],
                    [c_x + length / 2, c_y - length / 2, c_z - length / 2]),
             # AAWall([c_x + length / 2, c_y + length / 2, c_z + length / 2],
             #        [c_x - length / 2, c_y + length / 2, c_z - length / 2]),  # REMOVING THE LID
             AAWall([c_x + length / 2, c_y + length / 2, c_z + length / 2],
                    [c_x - length / 2, c_y - length / 2, c_z + length / 2])]

    return walls


def generate_closed_cube_box(length, center):
    c_x = center[0]
    c_y = center[1]
    c_z = center[2]

    walls = [AAWall([c_x - length / 2, c_y - length / 2, c_z - length / 2],
                    [c_x - length / 2, c_y + length / 2, c_z + length / 2]),
             AAWall([c_x - length / 2, c_y - length / 2, c_z - length / 2],
                    [c_x + length / 2, c_y - length / 2, c_z + length / 2]),
             AAWall([c_x - length / 2, c_y - length / 2, c_z - length / 2],
                    [c_x + length / 2, c_y + length / 2, c_z - length / 2]),
             AAWall([c_x + length / 2, c_y + length / 2, c_z + length / 2],
                    [c_x + length / 2, c_y - length / 2, c_z - length / 2]),
             AAWall([c_x + length / 2, c_y + length / 2, c_z + length / 2],
                    [c_x - length / 2, c_y + length / 2, c_z - length / 2]),
             AAWall([c_x + length / 2, c_y + length / 2, c_z + length / 2],
                    [c_x - length / 2, c_y - length / 2, c_z + length / 2])]

    return walls
