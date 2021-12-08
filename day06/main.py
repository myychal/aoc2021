import fire
import numpy as np


def part_one(data: np.ndarray, days):
    for day in range(days):
        data -= 1
        transforms_count = (data == -1).sum()
        data = np.concatenate([data, np.full(transforms_count, 8)], dtype=np.int8)
        data[data == -1] = 6
        print(day)
    return len(data)


def create_lookup_table(values: np.ndarray):
    table = {}
    for value in values:
        print(f"Calculating for {value}")
        table[value] = part_one(np.array([value], dtype=np.int8), 256)
    return table


def part_two(data: np.ndarray):
    """
    Because of the memory constraints, the solution is achieved by computing
    number of lanternfish after 256 days (using part one solution) for each
    possible value(1, 2, 3, 4, 5) in the sequence separately, and using such
    lookup table to calcuate final number for a given sequence.
    """
    # lookup = {
    #     1: 6206821033,
    #     2: 5617089148,
    #     3: 5217223242,
    #     4: 4726100874,
    #     5: 4368232009,
    # }
    unique_values, counts = np.unique(data, return_counts=True)
    lookup_table = create_lookup_table(unique_values)
    result = 0
    for unique_value, count in zip(unique_values, counts):
        result += lookup_table[unique_value] * count
    print(f"Answer 2: {result}")


def main(input_file_path: str):
    data = np.loadtxt(input_file_path, delimiter=',', dtype=np.int8)
    part_one_answer = part_one(data, 80)
    print(f"Answer 1: {part_one_answer}")
    data = np.loadtxt(input_file_path, delimiter=',', dtype=np.int8)
    part_two(data)


if __name__ == '__main__':
    fire.Fire(main)
