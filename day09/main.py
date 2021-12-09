import fire
import numpy as np
import pandas as pd
from itertools import product

BOUNDS = (100, 100)
X = 0
Y = 1


def main(input_file_path: str):
    data = pd.read_csv(input_file_path, dtype=str, header=None)
    data = data[0].apply(lambda x: pd.Series(list(x))).astype(int).values
    part_one(data)
    part_two(data)


def find_low_points(data):
    ii, jj = np.arange(len(data)), np.arange(data.shape[1])
    data = np.pad(data, (1, 1), constant_values=10)
    window_view = np.lib.stride_tricks.sliding_window_view(data, (3, 3))
    low_points_positions = []
    for i, j in product(ii, jj):
        window = window_view[i, j]
        middle_value = window[1, 1]
        neighbours = [window[1, 0], window[0, 1], window[1, 2], window[2, 1]]
        if all(middle_value < neighbours):
            low_points_positions.append([i, j])
    return np.array(low_points_positions)


def part_one(data):
    low_points_positions = find_low_points(data)
    low_points = data[low_points_positions[:, 0], low_points_positions[:, 1]]
    print(f"Answer 1: {np.sum(low_points + 1)}")


def find_basin_points(starting_point, data):
    valid_neighbours = set()
    if starting_point[X] - 1 >= 0:
        if data[starting_point[X] - 1, starting_point[Y]] > data[starting_point[X], starting_point[Y]]:
            valid_neighbours.add((starting_point[X] - 1, starting_point[Y]))
    if starting_point[X] + 1 < BOUNDS[X]:
        if data[starting_point[X] + 1, starting_point[Y]] > data[starting_point[X], starting_point[Y]]:
            valid_neighbours.add((starting_point[X] + 1, starting_point[Y]))
    if starting_point[Y] - 1 >= 0:
        if data[starting_point[X], starting_point[Y] - 1] > data[starting_point[X], starting_point[Y]]:
            valid_neighbours.add((starting_point[X], starting_point[Y] - 1))
    if starting_point[X] + 1 < BOUNDS[X]:
        if data[starting_point[X], starting_point[Y] + 1] > data[starting_point[X], starting_point[Y]]:
            valid_neighbours.add((starting_point[X], starting_point[Y] + 1))
    a=5


def part_two(data):
    low_points_positions = find_low_points(data)
    for low_point in low_points_positions:
        find_basin_points(low_point, data)
        a=5


if __name__ == '__main__':
    fire.Fire(main)
