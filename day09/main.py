import fire
import numpy as np
import pandas as pd
from itertools import product

BOUNDS = (100, 100)
X = 0
Y = 1


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


def find_basin_points(starting_point, data, result):
    valid_neighbours = find_valid_neighbours(data, starting_point)
    for neighbour in valid_neighbours:
        result.add(neighbour)
        find_basin_points(neighbour, data, result)
    return result


def find_valid_neighbours(data, starting_point):
    valid_neighbours = []
    if starting_point[X] - 1 >= 0:
        if data[starting_point[X] - 1, starting_point[Y]] > data[
            starting_point[X], starting_point[Y]] and data[
            starting_point[X] - 1, starting_point[Y]] != 9:
            valid_neighbours.append((starting_point[X] - 1, starting_point[Y]))
    if starting_point[X] + 1 < BOUNDS[X]:
        if data[starting_point[X] + 1, starting_point[Y]] > data[
            starting_point[X], starting_point[Y]] and data[
            starting_point[X] + 1, starting_point[Y]] != 9:
            valid_neighbours.append((starting_point[X] + 1, starting_point[Y]))
    if starting_point[Y] - 1 >= 0:
        if data[starting_point[X], starting_point[Y] - 1] > data[
            starting_point[X], starting_point[Y]] and data[
            starting_point[X], starting_point[Y] - 1] != 9:
            valid_neighbours.append((starting_point[X], starting_point[Y] - 1))
    if starting_point[Y] + 1 < BOUNDS[Y]:
        if data[starting_point[X], starting_point[Y] + 1] > data[
            starting_point[X], starting_point[Y]] and data[
            starting_point[X], starting_point[Y] + 1] != 9:
            valid_neighbours.append((starting_point[X], starting_point[Y] + 1))
    return valid_neighbours


def part_two(data):
    low_points_positions = find_low_points(data)
    basin_points_lengths = []
    for low_point in low_points_positions:
        result = set()
        basin_points = find_basin_points(low_point, data, result)
        basin_points_lengths.append(len(basin_points) + 1)
    top_3 = sorted(basin_points_lengths, reverse=True)[:3]
    print(f"Answer 2: {np.prod(top_3)}")


def main(input_file_path: str):
    data = pd.read_csv(input_file_path, dtype=str, header=None)
    data = data[0].apply(lambda x: pd.Series(list(x))).astype(int).values
    part_one(data)
    part_two(data)


if __name__ == '__main__':
    fire.Fire(main)
