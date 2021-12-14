import fire
import numpy as np

from itertools import product


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()
    template = contents[0].replace("\n", '')
    contents = contents[2:]
    pair_insertions = [line.replace("\n", "").split(" -> ") for line in
                       contents]
    return template, pair_insertions


def build_template_pairs(template: str):
    pairs = []
    for character_index in range(len(template) - 1):
        pairs.append(
            f"{template[character_index]}{template[character_index + 1]}")
    return pairs


def template_pairs_to_string(template_pairs):
    string = ''.join([x[:2] for x in template_pairs])
    return string + template_pairs[-1][-1]


def find_matching_pair(template_pairs, pair):
    try:
        return template_pairs.index(pair)
    except ValueError:
        return None


def insert_pair(pair_insertion, template_as_pairs):
    matching_pair_index = find_matching_pair(template_as_pairs,
                                             pair_insertion[0])
    if matching_pair_index is not None:
        template_as_pairs[matching_pair_index] = template_as_pairs[
                                                     matching_pair_index][
                                                 :1] + pair_insertion[
                                                     1] + \
                                                 template_as_pairs[
                                                     matching_pair_index][
                                                 1:]
    return template_as_pairs


def apply_insertions(template, pair_insertions, steps):
    """
    Slow as fuck, wont work for second part.
    """
    for step in range(steps):
        template_as_pairs = build_template_pairs(template)
        while not all([len(x) == 3 for x in template_as_pairs]):
            for pair_insertion in pair_insertions:
                template_as_pairs = insert_pair(pair_insertion,
                                                template_as_pairs)
        template = template_pairs_to_string(template_as_pairs)
    return template


def part_one(template, pair_insertions, steps=10):

    template = apply_insertions(template, pair_insertions, steps)
    unique_values, counts = np.unique(list(template), return_counts=True)
    print(unique_values, counts)
    print(f"Answer 1: {np.max(counts) - np.min(counts)}")


def initialize_tracking_dict(template, pair_insertions):
    pairs = dict.fromkeys(pair_insertions.keys(), 0)
    for char_index in range(len(template) - 1):
        pairs[template[char_index] + template[char_index + 1]] += 1
    return pairs


def track_insertions(template, pair_insertions, steps):
    """
    Speedy boi, use this one for greater number of steps and larger templates.
    """
    current_pairs_count = initialize_tracking_dict(template,
                                                         pair_insertions)
    for step in range(steps):
        future_pairs = dict.fromkeys(pair_insertions.keys(), 0)
        for pair_key, value in pair_insertions.items():
            if current_pairs_count[pair_key] < 1:
                continue

            future_pairs[pair_key] -= current_pairs_count[pair_key]

            # from AB -> C we create ACB and have two new pairs,
            # left AC and right BC
            left_new_pair = pair_key[0] + pair_insertions[pair_key]
            future_pairs[left_new_pair] += current_pairs_count[
                pair_key]

            right_new_pair = pair_insertions[pair_key] + pair_key[1]
            future_pairs[right_new_pair] += current_pairs_count[
                pair_key]

        for key in current_pairs_count.keys():
            current_pairs_count[key] += future_pairs[key]

    return current_pairs_count


def count_letters(combinations_count: dict):
    letters = [combination[0] for combination in combinations_count.keys()]
    letters = set(letters)
    letters_counter = {letter: 0 for letter in letters}
    for key, value in combinations_count.items():
        letters_counter[key[-1]] += value
    return letters_counter


def part_two(template, pair_insertions, steps):
    current_combinations_count = track_insertions(template, pair_insertions,
                                                  steps)
    letters_counter = count_letters(current_combinations_count)
    letters_counter[template[0]] += 1
    print(f"Answer 2: {np.max(list(letters_counter.values())) - np.min(list(letters_counter.values()))}")


def main(input_file_path: str):
    template, pair_insertions = parse_input_file(input_file_path)
    # part_one(template, pair_insertions, 10)
    pair_insertions = {x[0]: x[1] for x in pair_insertions}
    part_two(template, pair_insertions, 40)


if __name__ == '__main__':
    fire.Fire(main)
