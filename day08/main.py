import fire
import numpy as np


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()
    combinations = []
    outputs = []
    for line in contents:
        combination, output = line.split(" | ")
        combination = combination.split(" ")
        output = output.replace("\n", '').split(" ")
        combinations.append(combination)
        outputs.append(output)
    return combinations, outputs


def part_one(outputs: list):
    digits_counter = 0
    for output in outputs:
        for output_value in output:
            value_length = len(output_value)
            if value_length == 2 or value_length == 3 or value_length == 4 or value_length == 7:
                digits_counter += 1
    return digits_counter


def decode_unique_numbers(combination, digit_codes):
    """
    Unique numbers are 1, 4, 7, 8
    """
    for digit in combination:
        if len(digit) == 2:
            digit_codes[1] = digit
        elif len(digit) == 3:
            digit_codes[7] = digit
        elif len(digit) == 4:
            digit_codes[4] = digit
        elif len(digit) == 7:
            digit_codes[8] = digit
    combination.remove(digit_codes[1])
    combination.remove(digit_codes[7])
    combination.remove(digit_codes[4])
    combination.remove(digit_codes[8])
    return combination, digit_codes


def remove_chars_from_string(string: str, chars_to_remove: str):
    for char in chars_to_remove:
        string = string.replace(char, "")
    return string


def compare_strings(string1, string2):
    if len(string1) != len(string2):
        return False
    else:
        return all(char in string1 for char in string2)


def find_six(combination, digit_codes):
    """
    Template is digit 8 - digit 1, only matching number will be digit 6 - digit 1
    """
    template = remove_chars_from_string(digit_codes[8], digit_codes[1])
    for digit in combination:
        if digit == digit_codes[8]:
            continue
        to_match_template = remove_chars_from_string(digit, digit_codes[1])
        if compare_strings(template, to_match_template):
            digit_codes[6] = digit
            combination.remove(digit)
            return combination, digit_codes


def find_zero(combination, digit_codes):
    """
    Only digits left with six segments are 0 and 9, find what segment is missing
    in both of those and check if that segment is present in digit 4
    (the middle one), we have found digit 0.
    """
    for digit in combination:
        if len(digit) < 6:
            continue
        missing_segment = remove_chars_from_string(digit_codes[8], digit)
        if missing_segment in digit_codes[4]:
            digit_codes[0] = digit
            combination.remove(digit)
            return combination, digit_codes


def find_nine(combination, digit_codes):
    """
    The only leftover digit with 6 segments is digit 9.
    """
    for digit in combination:
        if len(digit) == 6:
            digit_codes[9] = digit
            combination.remove(digit)
            return combination, digit_codes


def find_five(combination, digit_codes):
    """
    We can now find upper right and lower left segments by subtracting
    digit 6 from digit 9. Upper left segment is the one present in the digit 1,
    lower left is the leftover one.
    """
    digit_six = set(digit_codes[6])
    digit_nine = set(digit_codes[9])
    six_and_nine_difference = digit_six.symmetric_difference(digit_nine)
    digit_five = remove_chars_from_string(digit_codes[8],
                                          ''.join(six_and_nine_difference))
    for digit in combination:
        if compare_strings(digit_five, digit):
            digit_codes[5] = digit
            combination.remove(digit)
            return combination, digit_codes


def find_three(combination, digit_codes):
    """
    Having only digit 2 and 3, we check if all segments from digit 1 are present
    in a given digit, if so, we found digit 3.
    """
    for digit in combination:
        if all(char in digit for char in digit_codes[1]):
            digit_codes[3] = digit
            combination.remove(digit)
            return combination, digit_codes


def decode_output(output, digit_codes):
    result = ''
    for digit in output:
        for digit_value, digit_code in digit_codes.items():
            if compare_strings(digit, digit_code):
                result += str(digit_value)
                break
    return result


def part_two(combinations: list, outputs: list):
    results = []
    for combination, output in zip(combinations, outputs):
        digit_codes = {digit: '' for digit in range(10)}
        combination, digit_codes = decode_unique_numbers(combination,
                                                         digit_codes)
        combination, digit_codes = find_six(combination, digit_codes)
        combination, digit_codes = find_zero(combination, digit_codes)
        combination, digit_codes = find_nine(combination, digit_codes)
        combination, digit_codes = find_five(combination, digit_codes)
        combination, digit_codes = find_three(combination, digit_codes)
        # Leftover digit is digit 2
        digit_codes[2] = combination[0]
        decoded_output = decode_output(output, digit_codes)
        results.append(int(decoded_output))
    print(f"Answer 2: {np.sum(results)}")


def main(input_file_path: str):
    combinations, outputs = parse_input_file(input_file_path)
    result1 = part_one(outputs)
    print(f"Answer 1: {result1}")
    part_two(combinations, outputs)


if __name__ == '__main__':
    fire.Fire(main)
