import fire
import numpy as np
import pandas as pd
import itertools


def increment_neighbours(board, x, y):
    shift_x = 0 if x - 1 < 0 else 1
    shift_y = 0 if y - 1 < 0 else 1
    neighbours_slice = np.s_[x - shift_x: x + 2, y - shift_y: y + 2]
    board[neighbours_slice][board[neighbours_slice] != 0] = board[neighbours_slice][board[neighbours_slice] != 0] + 1
    return board


def simulate_flashing(data, steps):
    flashes = 0
    for step in range(steps):
        flashes += increment_and_flash(data)
    return flashes


def increment_and_flash(data):
    data += 1
    to_flash = data > 9
    while to_flash.sum() > 0:
        flashed_indexes = np.where(to_flash)
        data[to_flash] = 0
        for x, y in zip(*flashed_indexes):
            data = increment_neighbours(data, x, y)
        to_flash = data > 9
    return (data == 0).sum()


def find_simultaneous_flash(data):
    steps = 0
    while not np.all(data == 0):
        increment_and_flash(data)
        steps += 1
    return steps


def main(input_file_path: str):
    data = pd.read_csv(input_file_path, dtype=str, header=None)
    data = data[0].apply(lambda x: pd.Series(list(x))).astype(int).values

    flashes = simulate_flashing(np.copy(data), 100)
    print(f"Answer 1: {flashes}")
    steps = find_simultaneous_flash(data)
    print(f"Answer 2: {steps}")


if __name__ == '__main__':
    fire.Fire(main)
