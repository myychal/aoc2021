from typing import List

import fire
import numpy as np

from itertools import permutations


def parse_input_file(input_file_path: str):
    snails = []
    with open(input_file_path) as f:
        for line in f:
            snails.append([x for x in line if x != "'" and x != "\n"])
    return snails


def add_digit_from_explode(snail: List[str], digit: int, start_idx: int,
                           direction: str):
    if direction == 'right':
        for idx in range(start_idx + 1, len(snail)):
            if snail[idx].isdigit():
                snail[idx] = str(int(snail[idx]) + digit)
                return snail
    elif direction == 'left':
        for idx in range(start_idx - 2, 0, -1):
            if snail[idx].isdigit():
                snail[idx] = str(int(snail[idx]) + digit)
                return snail
    return snail


def explode_snail(snail: List[str]):
    open_brackets_count = 0
    for idx, character in enumerate(snail):
        if character == '[':
            open_brackets_count += 1
        elif character == ']':
            open_brackets_count -= 1
        elif character.isdigit() and open_brackets_count >= 5 and snail[
            idx + 2].isdigit():
            left_digit = int(character)
            right_digit = int(snail[idx + 2])
            snail = snail[:idx - 1] + ['0'] + snail[idx + 4:]
            snail = add_digit_from_explode(snail, left_digit, idx, "left")
            snail = add_digit_from_explode(snail, right_digit, idx, "right")
            return snail
    return snail


def split(snail: List[str]):
    for idx, character in enumerate(snail):
        if character.isdigit() and int(character) >= 10:
            digit = int(character)
            left_digit = digit // 2
            right_digit = int(np.ceil(digit / 2))
            snail = snail[:idx] + ['[', str(left_digit), ',', str(right_digit),
                                   ']'] + snail[idx + 1:]
            return snail
    return snail


def check_for_explosion(snail: List[str]):
    open_brackets_count = 0
    for idx, character in enumerate(snail):
        if character == '[':
            open_brackets_count += 1
        elif character == ']':
            open_brackets_count -= 1
        if open_brackets_count > 4:
            return True
    return False


def check_for_split(snail: List[str]):
    for idx, character in enumerate(snail):
        if character.isdigit() and int(character) >= 10:
            return True
    return False


def perform_reduction(snail: List[str]):
    if check_for_explosion(snail):
        return explode_snail(snail), True
    if check_for_split(snail):
        return split(snail), True
    return snail, False


def add_snails(snails: List[List[str]]):
    current_snail = snails[0]
    for snail_idx in range(1, len(snails)):
        current_snail = ['['] + current_snail + [','] + snails[snail_idx] + [
            ']']
        current_snail, reduction_performed = perform_reduction(current_snail)
        while reduction_performed:
            current_snail, reduction_performed = perform_reduction(
                current_snail)
    return current_snail


def check_magnitude(snail: List[str]):
    while 1:
        reduced_in_loop = False
        for idx, character in enumerate(snail[:-2]):
            if character.isdigit() and snail[idx + 2].isdigit():
                pair_magnitude = int(character) * 3 + int(snail[idx + 2]) * 2
                snail = snail[:idx - 1] + [str(pair_magnitude)] + snail[
                                                                  idx + 4:]
                reduced_in_loop = True
                break
        if not reduced_in_loop:
            break
    return snail


def part_one(snails):
    snail = add_snails(snails)
    magnitude = check_magnitude(snail)
    print(f"Answer 1: {magnitude}")


def compare_magnitudes(snails: List[str]):
    biggest_magnitude = 0
    for snails_pair in permutations(snails, 2):
        snail = add_snails(snails_pair)
        magnitude = check_magnitude(snail)
        if int(magnitude[0]) > biggest_magnitude:
            biggest_magnitude = int(magnitude[0])
    return biggest_magnitude


def part_two(snails: List[List[str]]):
    biggest_magnitude = compare_magnitudes(snails)
    print(f"Answer 2: {biggest_magnitude}")


def main(input_file_path: str):
    snails = parse_input_file(input_file_path)
    part_one(snails)
    part_two(snails)


if __name__ == '__main__':
    fire.Fire(main)
