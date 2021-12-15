import fire
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def find_valid_neighbours(cave, x, y):
    valid_neighbours = []
    if x - 1 >= 0:
        valid_neighbours.append((x - 1, y))
    if x + 1 < cave.shape[0]:
        valid_neighbours.append((x + 1, y))
    if y - 1 >= 0:
        valid_neighbours.append((x, y - 1))
    if y + 1 < cave.shape[1]:
        valid_neighbours.append((x, y + 1))
    return valid_neighbours


def create_graph(cave: np.ndarray):
    G = nx.DiGraph()
    for x, y in np.ndindex(cave.shape):
        neighbours = find_valid_neighbours(cave, x, y)
        G.add_node((x, y))
        for neighbour in neighbours:
            G.add_edge((x, y), (neighbour[0], neighbour[1]),
                       weight=cave[neighbour[0], neighbour[1]])
    return G


def calculate_shortest_path_cost(G, cave_map):
    end_point = (cave_map.shape[0] - 1, cave_map.shape[1] - 1)
    path = np.array(nx.shortest_path(G, (0, 0), end_point, weight='weight'))
    path_matrix = np.zeros_like(cave_map, dtype=bool)
    path_matrix[path[1:, 0], path[1:, 1]] = True
    path_cost = cave_map[path_matrix].sum()
    return path_cost


def part_one(cave):
    G = create_graph(cave)
    path_cost = calculate_shortest_path_cost(G, cave)
    print(f"Answer 1: {path_cost}")


def enlarge_map(cave_map: np.ndarray, n: int):
    enlarged_map = []
    baseline_column_cave = np.copy(cave_map)
    for column_idx in range(n):
        if column_idx != 0:
            baseline_column_cave += 1
        if column_idx != 0:
            baseline_column_cave[baseline_column_cave > 9] = 1
        rows = [baseline_column_cave]
        for row_idx in range(1, n):
            new_row = np.copy(rows[-1]) + 1
            new_row[new_row > 9] = 1
            rows.append(new_row)
        rows = np.vstack(rows)
        enlarged_map.append(rows)
    return np.hstack(enlarged_map)


def part_two(cave):
    enlarged_map = enlarge_map(cave, 5)
    G = create_graph(enlarged_map)
    path_cost = calculate_shortest_path_cost(G, enlarged_map)
    print(f"Answer 2: {path_cost}")


def main(input_file_path: str):
    cave = pd.read_csv(input_file_path, dtype=str, header=None)
    cave = cave[0].apply(lambda x: pd.Series(list(x))).astype(int).values
    part_one(cave)
    part_two(cave)


if __name__ == '__main__':
    fire.Fire(main)
