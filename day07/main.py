import fire
import numpy as np


def part_one(data: np.ndarray):
    median = np.median(data)
    fuel = np.sum(np.abs(data - median))
    print(f"Answer 1: {fuel}")


def part_two(data: np.ndarray):
    mean = int(np.mean(data))
    position_changes = np.abs(data - mean)
    fuel = np.sum((position_changes / 2) * (1 + position_changes))
    print(f"Answer 2: {fuel}")


def main(input_file_path: str):
    data = np.loadtxt(input_file_path, delimiter=',', dtype=int)
    part_one(data)
    part_two(data)


if __name__ == '__main__':
    fire.Fire(main)
