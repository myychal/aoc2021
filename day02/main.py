from typing import List
import fire


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()
    contents = [x.strip('\n') for x in contents]
    return contents


HORIZONTAL_INSTRUCTIONS = ['forward', 'aim']
DEPTH_INSTRUCTIONS = ['down', 'up']


def part_one(data: List[str]):
    horizontal_position = 0
    depth_position = 0
    for command in data:
        instruction_name, value = command.split(' ')
        value = int(value)
        if instruction_name in HORIZONTAL_INSTRUCTIONS:
            horizontal_position += value
        elif instruction_name in DEPTH_INSTRUCTIONS:
            if instruction_name == 'up':
                depth_position -= value
            elif instruction_name == 'down':
                depth_position += value
    return horizontal_position, depth_position


def part_two(data: List[str]):
    horizontal_position = 0
    depth_position = 0
    aim =0
    for command in data:
        instruction_name, value = command.split(' ')
        value = int(value)
        if instruction_name in HORIZONTAL_INSTRUCTIONS:
            horizontal_position += value
            depth_position += value * aim
        elif instruction_name in DEPTH_INSTRUCTIONS:
            if instruction_name == 'up':
                aim -= value
            elif instruction_name == 'down':
                aim += value
    return horizontal_position, depth_position


def main(input_file_path: str):
    data = parse_input_file(input_file_path)
    horizontal_position, depth_position = part_one(data)
    print(f"Answer 1: {horizontal_position * depth_position}")
    horizontal_position, depth_position = part_two(data)
    print(f"Answer 2: {horizontal_position * depth_position}")


if __name__ == '__main__':
    fire.Fire(main)
