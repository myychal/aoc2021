from typing import List
import re

import fire
import numpy as np


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()
    dots_coordinates = [np.fromstring(x, sep=',') for x in contents if ',' in x]
    instructions = [x.replace("\n", '') for x in contents if '=' in x]
    return np.array(dots_coordinates, dtype=int), instructions


def build_dots_matrix(dots_coordinates: np.ndarray):
    matrix = np.zeros(
        (
            np.max(dots_coordinates[:, 1]) + 1,
            np.max(dots_coordinates[:, 0]) + 1
        )
    )
    matrix[dots_coordinates[:, 1], dots_coordinates[:, 0]] = 1
    return matrix


def _fold_by_y(matrix: np.ndarray, fold_index: int):
    upper_part = matrix[:fold_index, :]
    bottom_part = matrix[fold_index + 1:, :]
    if len(bottom_part) != len(upper_part):
        bottom_part = np.vstack([bottom_part, np.zeros((bottom_part.shape[1]))])
    flipped_bottom = np.flip(bottom_part, axis=0)
    folded = np.logical_or(upper_part, flipped_bottom)
    return folded


def _fold_by_x(matrix: np.ndarray, fold_index: int):
    left_part = matrix[:, :fold_index]
    right_part = matrix[:, fold_index + 1:]
    right_part_flipped = np.flip(right_part, axis=1)
    return np.logical_or(left_part, right_part_flipped)


def fold_matrix(matrix: np.ndarray, instructions: List[str]):
    for instruction in instructions:
        fold_index = int(re.findall(r"\d+", instruction)[0])
        if 'y' in instruction:
            matrix = _fold_by_y(matrix, fold_index)
        elif 'x' in instruction:
            matrix = _fold_by_x(matrix, fold_index)
    return matrix


def part_one(matrix: np.ndarray, instructions):
    matrix = fold_matrix(matrix, instructions[:1])
    overlapping_dots = (matrix == 1).sum()
    print(f"Answer 1: {overlapping_dots}")


def part_two(matrix: np.ndarray, instructions):
    matrix = fold_matrix(matrix, instructions)
    letters = [matrix[:, x:x + 4] for x in range(0, matrix.shape[1], 5)]
    for letter in letters:
        print(letter.astype(int))


def main(input_file_path: str):
    dots_coordinates, instructions = parse_input_file(input_file_path)
    matrix = build_dots_matrix(dots_coordinates)
    part_one(np.copy(matrix), instructions)
    part_two(matrix, instructions)


if __name__ == '__main__':
    fire.Fire(main)
