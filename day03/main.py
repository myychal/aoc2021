import fire
import numpy as np
import pandas as pd


def binary_array_to_decimal(array: np.ndarray):
    return int(''.join([str(x) for x in array]), 2)


def part_one(data: np.ndarray):
    summed_columns = np.sum(data, axis=0)
    gamma = np.array([1 if x > len(data) // 2 else 0 for x in summed_columns])
    epsilon = 1 - gamma
    gamma_decimal = binary_array_to_decimal(gamma)
    epsilon_decimal = binary_array_to_decimal(epsilon)
    print(f"Answer 1: {gamma_decimal * epsilon_decimal}")


def part_two_oxygen(data: np.ndarray):
    for column_id in range(data.shape[1]):
        if len(data) == 1:
            break
        _, (zeros, ones) = np.unique(data[:, column_id], return_counts=True)
        if ones >= zeros:
            data = data[data[:, column_id] == 1]
        else:
            data = data[data[:, column_id] == 0]
    return data[0]


def part_two_co2(data: np.ndarray):
    for column_id in range(data.shape[1]):
        if len(data) == 1:
            break
        _, (zeros, ones) = np.unique(data[:, column_id], return_counts=True)
        if ones >= zeros:
            data = data[data[:, column_id] == 0]
        else:
            data = data[data[:, column_id] == 1]
    return data[0]


def main(input_file_path: str):
    data = pd.read_csv(input_file_path, dtype=str, header=None)
    data = data[0].apply(lambda x: pd.Series(list(x))).astype(int).values
    part_one(data)
    oxygen = part_two_oxygen(data)
    co2 = part_two_co2(data)
    print(
        f"Answer 2: {binary_array_to_decimal(oxygen) * binary_array_to_decimal(co2)}")


if __name__ == '__main__':
    fire.Fire(main)
