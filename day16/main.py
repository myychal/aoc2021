from typing import List

import fire
import numpy as np


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readline()
    return contents.replace("\n", '')


def hex_to_bin(hex_string):
    binary_strring = bin(int(hex_string, 16))[2:]
    leading_zeros = 4 - len(binary_strring) % 4 if len(
        binary_strring) % 4 != 0 else 0
    return binary_strring.zfill(len(binary_strring) + leading_zeros)


def decode_literal(transmission_line: str):
    result = ''
    numbers_found = 0
    for i in range(0, len(transmission_line), 5):
        first_bit = transmission_line[i]
        number = transmission_line[i + 1: i + 5]
        result += number
        numbers_found += 1
        if first_bit == '0':
            break
    return result, numbers_found


def count_versions(transmission_line: str, versions: List[int]):
    if len(transmission_line) <= 7:
        return ''
    packet_version = int(transmission_line[:3], 2)
    versions.append(packet_version)
    transmission_line = transmission_line[3:]

    packet_type_id = int(transmission_line[:3], 2)
    transmission_line = transmission_line[3:]

    if packet_type_id == 4:
        decoded_number, found_numbers = decode_literal(transmission_line)
        transmission_line = transmission_line[
                            len(decoded_number) + found_numbers:]
    else:
        length_type_id = transmission_line[0]
        transmission_line = transmission_line[1:]

        if length_type_id == '1':
            number_of_subpackets = int(transmission_line[:11], 2)
            transmission_line = transmission_line[11:]
            for subpacket in range(number_of_subpackets):
                transmission_line = count_versions(transmission_line, versions)
            a = 5
        else:
            subpackets_bits = int(transmission_line[:15], 2)
            transmission_line = transmission_line[15:]
            decoded_bits = 0
            while decoded_bits < subpackets_bits:
                current_transmision_bits = len(transmission_line)
                transmission_line = count_versions(transmission_line, versions)
                decoded_bits += current_transmision_bits - len(
                    transmission_line)

    return transmission_line


def part_one(transmission_line: str):
    transmission_line = hex_to_bin(transmission_line)
    result = []
    count_versions(transmission_line, result)
    print(f"Answer 1: {sum(result)}")


def decode_transmission(transmission_line: str, versions: List[int]):
    if len(transmission_line) <= 7:
        return '', np.nan
    packet_version = int(transmission_line[:3], 2)
    versions.append(packet_version)
    transmission_line = transmission_line[3:]

    packet_type_id = int(transmission_line[:3], 2)
    transmission_line = transmission_line[3:]

    if packet_type_id == 4:
        decoded_number, found_numbers = decode_literal(transmission_line)
        transmission_line = transmission_line[
                            len(decoded_number) + found_numbers:]
        packet_value = int(decoded_number, 2)
    else:
        length_type_id = transmission_line[0]
        transmission_line = transmission_line[1:]

        if length_type_id == '1':
            packet_numbers = []
            number_of_subpackets = int(transmission_line[:11], 2)
            transmission_line = transmission_line[11:]
            for subpacket in range(number_of_subpackets):
                transmission_line, value = decode_transmission(
                    transmission_line, versions)
                packet_numbers.append(value)
            packet_value = combine_packets(packet_numbers, packet_type_id)
        else:
            subpackets_bits = int(transmission_line[:15], 2)
            transmission_line = transmission_line[15:]
            decoded_bits = 0
            packet_numbers = []
            while decoded_bits < subpackets_bits:
                current_transmision_bits = len(transmission_line)
                transmission_line, value = decode_transmission(
                    transmission_line, versions)
                packet_numbers.append(value)
                decoded_bits += current_transmision_bits - len(
                    transmission_line)
            packet_value = combine_packets(packet_numbers, packet_type_id)

    return transmission_line, packet_value


def combine_packets(values: List[int], packet_id):
    if packet_id == 0:
        return sum(values)
    elif packet_id == 1:
        return np.product(values)
    elif packet_id == 2:
        return np.min(values)
    elif packet_id == 3:
        return np.max(values)
    elif packet_id == 5:
        return 1 if values[0] > values[1] else 0
    elif packet_id == 6:
        return 1 if values[0] < values[1] else 0
    elif packet_id == 7:
        return 1 if values[0] == values[1] else 0


def part_two(transmission_line: str):
    transmission_line = hex_to_bin(transmission_line)
    result = []
    res, value = decode_transmission(transmission_line, result)
    print(f"Answer 2: {value}")


def main(input_file_path: str):
    transmission_line = parse_input_file(input_file_path)
    part_one(transmission_line)
    part_two(transmission_line)


if __name__ == '__main__':
    fire.Fire(main)
