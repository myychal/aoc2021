from typing import List

import fire


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()
    contents = [x.replace('\n', '') for x in contents]
    return contents


def get_matching_closing_bracket(bracket: str):
    if bracket == '[':
        return ']'
    elif bracket == '{':
        return '}'
    elif bracket == '(':
        return ')'
    elif bracket == '<':
        return '>'


def is_opening_bracket(bracket: str):
    if bracket in ['[', '(', '{', '<']:
        return True
    return False


def find_illegal_characters(lines: List[str]):
    illegal_characters = []
    for line in lines:
        valid_closing_brackets = []
        for character in line:
            if is_opening_bracket(character):
                matching_closing_bracket = get_matching_closing_bracket(
                    character)
                valid_closing_brackets.append(matching_closing_bracket)
            elif character != valid_closing_brackets[-1]:
                illegal_characters.append(character)
                break
            else:
                valid_closing_brackets.pop()
    return illegal_characters


def part_one(data):
    illegal_characters = find_illegal_characters(data)
    score_table = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    score = 0
    for character in illegal_characters:
        score += score_table[character]
    print(f"Anaswer 1: {score}")


def find_missing_brackets(line: str):
    illegal_characters = []
    valid_closing_brackets = []
    for character in line:
        if is_opening_bracket(character):
            matching_closing_bracket = get_matching_closing_bracket(
                character)
            valid_closing_brackets.append(matching_closing_bracket)
        elif character != valid_closing_brackets[-1]:
            illegal_characters.append(character)
            return []
        else:
            valid_closing_brackets.pop()
    return valid_closing_brackets


SCORE_TABLE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def calculate_line_score(line_characters):
    score = 0
    for character in line_characters:
        score = score * 5 + SCORE_TABLE[character]
    return score


def part_two(data):
    scores = []
    for line in data:
        missing_brackets = find_missing_brackets(line)
        if len(missing_brackets) == 0:
            continue
        else:
            missing_brackets.reverse()
            scores.append(calculate_line_score(missing_brackets))
    scores = sorted(scores)
    import numpy as np
    print(f"Answer 2: {np.median(scores)}")


def main(input_file_path: str):
    data = parse_input_file(input_file_path)
    part_one(data)
    part_two(data)


if __name__ == '__main__':
    fire.Fire(main)
