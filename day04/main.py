import fire
import numpy as np


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()
    drawn_numbers = np.fromstring(contents[0], sep=',', dtype=int)
    del contents[0:2]
    boards = []
    current_board = []
    for line in contents:
        if line == '\n':
            boards.append(current_board)
            current_board = []
            continue
        line_as_array = np.fromstring(line, sep=' ', dtype=int)
        current_board.append(line_as_array)
    boards = np.array(boards)
    return drawn_numbers, boards


def check_for_winning_board(board_masks: np.ndarray):
    five_in_a_row = np.ones(5, dtype=bool)
    for board_index, board in enumerate(board_masks):
        for row in board:
            if np.all(row == five_in_a_row):
                return board_index
        for column in board.T:
            if np.all(column == five_in_a_row):
                return board_index
    return None


def calculate_score_for_board(board: np.ndarray,
                              board_mask: np.ndarray,
                              called_number: int):
    unmarked_sum = np.sum(board[~board_mask])
    return unmarked_sum * called_number


def part_one(drawn_numbers: np.ndarray, boards: np.ndarray):
    board_masks = np.zeros_like(boards, dtype=bool)
    for drawn_number in drawn_numbers:
        board_masks = np.logical_or(board_masks, boards == drawn_number)
        winning_board_idx = check_for_winning_board(board_masks)
        if winning_board_idx is not None:
            winning_board = boards[winning_board_idx]
            winning_board_mask = board_masks[winning_board_idx]
            break

    score = calculate_score_for_board(winning_board, winning_board_mask,
                                      drawn_number)
    print(f"Answer 1: {score}")


def check_for_winning_boards(board_masks: np.ndarray):
    five_in_a_row = np.ones(5, dtype=bool)
    winning_boards = []
    for board_index, board in enumerate(board_masks):
        for row in board:
            if np.all(row == five_in_a_row):
                winning_boards.append(board_index)
        for column in board.T:
            if np.all(column == five_in_a_row):
                winning_boards.append(board_index)
    return winning_boards


def part_two(drawn_numbers: np.ndarray, boards: np.ndarray):
    board_masks = np.zeros_like(boards, dtype=bool)
    last_called_number = None
    for drawn_number in drawn_numbers:
        board_masks = np.logical_or(board_masks, boards == drawn_number)
        winning_board_idx = check_for_winning_boards(board_masks)
        if len(winning_board_idx) > 0:
            winning_board = boards[winning_board_idx[0]]
            winning_board_mask = board_masks[winning_board_idx[0]]
            last_called_number = drawn_number
            boards = np.delete(boards, winning_board_idx, axis=0)
            board_masks = np.delete(board_masks, winning_board_idx, axis=0)

    score = calculate_score_for_board(winning_board,
                                      winning_board_mask,
                                      last_called_number)
    print(f"Answer 2: {score}")


def main(input_file_path: str):
    drawn_numbers, boards = parse_input_file(input_file_path)
    part_one(drawn_numbers, boards)
    part_two(drawn_numbers, boards)


if __name__ == '__main__':
    fire.Fire(main)
