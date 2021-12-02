import fire
import numpy as np


def first_part(data: np.ndarray):
    data_shifted = data[:-1]
    data = data[1:]
    measurement_differences = data - data_shifted
    increments = (measurement_differences > 0).sum()
    return increments


def second_part(data: np.ndarray):
    data_shifted_by_one = data[1:-1]
    data_shifted_by_two = data[2:]
    table = np.column_stack(
        [data[:-2], data_shifted_by_one, data_shifted_by_two])
    sums = np.sum(table, axis=1)
    increments = first_part(sums)
    return increments


def main(input_file_path: str):
    data = np.loadtxt(input_file_path)
    first_part_increments = first_part(data)
    print(f"Answer 1: {first_part_increments}")
    second_part_increments = second_part(data)
    print(f"Answer 2: {second_part_increments}")


if __name__ == '__main__':
    fire.Fire(main)
