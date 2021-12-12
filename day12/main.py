from typing import List

import fire
import numpy as np


def add_to_dict(dictionary, start, end):
    if start not in dictionary.keys():
        dictionary[start] = [end]
    else:
        dictionary[start].append(end)
    return dictionary


def parse_input(input_file_path: str):
    connections = {}
    with open(input_file_path) as f:
        for line in f:
            start, end = line.split('-')
            add_to_dict(connections, start.replace('\n', ''),
                        end.replace('\n', ''))
    return connections


def get_possible_destinations(connections, start_position):
    destinations = []
    if start_position in connections.keys():
        destinations.extend(connections[start_position])
    for key, value in connections.items():
        if start_position in value:
            destinations.append(key)
    return destinations


def unique_small_caves(current_path: List[str], destination: str):
    """
    Part 1 condition for small caves
    """
    if destination.islower() and destination in current_path:
        return True
    return False


def double_small_cave_exists(path: List[str]):
    caves = {}
    for cave in path:
        if cave.islower() and cave != 'start':
            if cave not in caves.keys():
                caves[cave] = 1
            else:
                caves[cave] += 1
    small_caves_more_than_two = [True if x >= 2 else False for x in
                                 caves.values()]
    return sum(small_caves_more_than_two) == 1


def at_most_one_double_small_cave(current_path: List[str], destination: str):
    """
    Part Two condition for small caves
    """
    if destination == 'start':
        return True

    if double_small_cave_exists(
            current_path) and destination in current_path \
            and destination.islower():
        return True
    return False


def find_paths(connections: dict, current_position: str,
               current_path: list, paths: list, small_caves_condition):
    destinations = get_possible_destinations(connections, current_position)
    if len(current_path) == 0:
        current_path = [current_position]
    for destination in destinations:

        if small_caves_condition(current_path, destination):
            continue

        if destination == 'end':
            paths.append(current_path + ['end'])
            continue

        current_path.append(destination)

        find_paths(connections, destination, current_path, paths,
                   small_caves_condition)
    current_path.pop()
    return


def part_one(connections):
    paths = []
    find_paths(connections, 'start', [], paths, unique_small_caves)
    print(f"Answer 1: {len(paths)}")


def part_two(connections):
    paths = []
    find_paths(connections, 'start', [], paths, at_most_one_double_small_cave)
    print(f"Answer 2: {len(paths)}")


def main(input_file_path: str):
    connections = parse_input(input_file_path)
    part_one(connections)
    part_two(connections)


if __name__ == '__main__':
    fire.Fire(main)
