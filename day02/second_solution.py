from typing import List

import numpy as np
import fire


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()
    contents = [x.strip('\n') for x in contents]
    return contents


class Instruction:
    def __init__(self, origin, command_name, operation):
        self.origin = origin
        self.command_name = command_name
        self.operation = operation

    def __call__(self, current_position: int, new_value: int):
        return self.operation(current_position, new_value)


INSTRUCTIONS = [Instruction("horizontal", "forward", np.add),
                Instruction("depth", "up", np.subtract),
                Instruction("depth", "down", np.add)]


def part_one(data: List[str]):
    horizontal_position = 0
    depth_position = 0
    for command in data:
        command_name, value = command.split(' ')
        value = int(value)
        for instruction in INSTRUCTIONS:
            if instruction.command_name == command_name:
                if instruction.origin == 'horizontal':
                    horizontal_position = instruction(horizontal_position, value)
                elif instruction.origin == 'depth':
                    depth_position = instruction(depth_position, value)
    return horizontal_position, depth_position


def part_two(data: List[str]):
    horizontal_position = 0
    depth_position = 0
    aim = 0
    for command in data:
        command_name, value = command.split(' ')
        value = int(value)
        for instruction in INSTRUCTIONS:
            if instruction.command_name == command_name:
                if instruction.origin == 'horizontal':
                    horizontal_position = instruction(horizontal_position, value)
                    depth_position += aim * value
                elif instruction.origin == 'depth':
                    aim = instruction(aim, value)
    return horizontal_position, depth_position


def main(input_file_path: str):
    data = parse_input_file(input_file_path)
    horizontal_position, depth_position = part_one(data)
    print(f"Answer 1: {horizontal_position * depth_position}")
    horizontal_position, depth_position = part_two(data)
    print(f"Answer 2: {horizontal_position * depth_position}")


if __name__ == '__main__':
    fire.Fire(main)
