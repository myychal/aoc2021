from dataclasses import dataclass

import fire
import numpy as np


@dataclass
class Coords:
    x1 = 0
    y1 = 1
    x2 = 2
    y2 = 3


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        lines = f.readlines()
    data = []
    for line in lines:
        data.append(
            np.fromstring(line.replace(' -> ', ','), sep=',', dtype=int))
    return np.array(data)


def part_one(data: np.ndarray):
    max_value = np.max(data) + 1
    board = np.zeros((max_value, max_value))
    for line in data:
        if line[Coords.x1] == line[Coords.x2] or line[Coords.y1] == line[
            Coords.y2]:
            if line[Coords.x1] > line[Coords.x2]:
                temp = line[Coords.x1]
                line[Coords.x1] = line[Coords.x2]
                line[Coords.x2] = temp
            if line[Coords.y1] > line[Coords.y2]:
                temp = line[Coords.y1]
                line[Coords.y1] = line[Coords.y2]
                line[Coords.y2] = temp
            line_board = np.zeros((max_value, max_value))
            line_board[line[Coords.y1]: line[Coords.y2] + 1, line[Coords.x1]: line[Coords.x2] + 1] = 1
            board = board + line_board
    more_than_two_count = (board >= 2).sum()
    print(f"Answer 1: {more_than_two_count}")


def fill_diagonal(data: np.ndarray, x1, y1, x2, y2):
    x_step = 1 if x1 < x2 else -1
    y_step = 1 if y1 < y2 else -1
    for x_shift, y_shift in zip(range(x1, x2 + x_step, x_step), range(y1, y2 + y_step, y_step)):
        data[y_shift, x_shift] = 1
    return data


def part_two(data: np.ndarray):

    max_value = np.max(data) + 1
    board = np.zeros((max_value, max_value))
    for line in data:
        line_board = np.zeros((max_value, max_value))
        if line[Coords.x1] == line[Coords.x2] or line[Coords.y1] == line[Coords.y2]:
            if line[Coords.x1] > line[Coords.x2]:
                temp = line[Coords.x1]
                line[Coords.x1] = line[Coords.x2]
                line[Coords.x2] = temp
            if line[Coords.y1] > line[Coords.y2]:
                temp = line[Coords.y1]
                line[Coords.y1] = line[Coords.y2]
                line[Coords.y2] = temp
            line_board[line[Coords.y1]: line[Coords.y2] + 1, line[Coords.x1]: line[Coords.x2] + 1] = 1
            board = board + line_board
        else:
            line_board = fill_diagonal(line_board, line[Coords.x1], line[Coords.y1],
                                  line[Coords.x2], line[Coords.y2])
            board = board + line_board
    more_than_two_count = (board >= 2).sum()
    print(f"Answer 2: {more_than_two_count}")


def main(input_file_path: str):
    data = parse_input_file(input_file_path)
    part_one(data)
    part_two(data)


if __name__ == '__main__':
    fire.Fire(main)
