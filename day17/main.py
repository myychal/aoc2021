import fire
import numpy as np
import re

X = 0
Y = 1
LEFT_BOUND = 0
RIGHT_BOUND = 1
LOWER_BOUND = 0
UPPER_BOUND = 1


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        line = f.readline()
    coords = re.findall("-?\d+", line)
    return (int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3]))


def is_on_target(target_x, target_y, position):
    if target_x[LEFT_BOUND] <= position[X] <= target_x[RIGHT_BOUND] and \
            target_y[
                LOWER_BOUND] <= position[Y] <= target_y[UPPER_BOUND]:
        return True
    return False


def shoot(target_x, target_y, velocity, steps):
    highest_point = 0
    position = [0, 0]
    for step in range(steps):
        position[X] += velocity[X]
        position[Y] += velocity[Y]
        highest_point = position[Y] if position[
                                           Y] > highest_point else highest_point
        if is_on_target(target_x, target_y, position):
            return True, highest_point

        if position[Y] < target_y[LOWER_BOUND] or position[X] > target_x[
            RIGHT_BOUND]:
            return False, np.nan

        velocity[X] -= 1 if velocity[X] != 0 else velocity[X]
        velocity[Y] -= 1
    return False, np.nan


def find_highest_point(target_x, target_y, search_range: tuple = (250, 250)):
    """
    A lot of room for improvement:
    1: Somehow find an optimal boundaries for velocities
    2: Find optimal number of steps, or terminate aim simulation in a smarter way
    3: Do not brute force - maybe find a function?
    """
    highest_points = []
    for velocity_x, velocity_y in np.ndindex(search_range):
        hit, highest_point = shoot(target_x, target_y, [velocity_x, velocity_y],
                                   300)
        if hit:
            highest_points.append(highest_point)
    return np.max(highest_points)


def find_all_hits(target_x, target_y, search_range: tuple = (250, 250)):
    """
    A lot of room for improvement:
    1: Somehow find an optimal boundaries for velocities
    2: Find optimal number of steps, or terminate aim simulation in a smarter way
    3: Do not brute force - maybe find a function?
    """
    hit_velocities = []
    for velocity_x, velocity_y in np.ndindex(search_range):
        hit, highest_point = shoot(target_x, target_y, [velocity_x, velocity_y],
                                   300)
        if hit:
            hit_velocities.append((velocity_x, velocity_y))
    for velocity_x, velocity_y in np.ndindex(search_range):
        velocity_y = - velocity_y
        hit, highest_point = shoot(target_x, target_y, [velocity_x, velocity_y],
                                   300)
        if hit:
            hit_velocities.append((velocity_x, velocity_y))
    return set(hit_velocities)


def part_one(target_x, target_y):
    search_range = (target_x[RIGHT_BOUND] + 1, np.abs(target_y[LOWER_BOUND]))
    highest_point = find_highest_point(target_x, target_y,
                                       search_range=search_range)
    print(f"Answer 1: {highest_point}")


def part_two(target_x, target_y):
    search_range = (
    target_x[RIGHT_BOUND] + 1, np.abs(target_y[LOWER_BOUND]) + 10)
    hits = find_all_hits(target_x, target_y, search_range=search_range)
    print(f"Answer 2: {len(hits)}")


def main(input_file_path: str):
    target_x, target_y = parse_input_file(input_file_path)
    part_one(target_x, target_y)
    part_two(target_x, target_y)


if __name__ == '__main__':
    fire.Fire(main)
