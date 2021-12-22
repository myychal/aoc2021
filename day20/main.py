import fire
import numpy as np


def parse_input_file(input_file_path: str):
    with open(input_file_path) as f:
        contents = f.readlines()

    iea = [0 if x == "." else 1 for x in contents[0].replace("\n", "")]
    image = []
    for line in contents[2:]:
        line = [0 if x == "." else 1 for x in line.replace("\n", "")]
        image.append(line)
    return np.array(iea), np.array(image)


def find_valid_neighbours(image, x, y):
    return image[max(x - 1, 0):min(x + 2, image.shape[0]),
           max(y - 1, 0):min(y + 2, image.shape[1])].flatten()


def enhance_image(iea: np.ndarray, image: np.ndarray, steps: int = 2):
    image = np.pad(image, (2, 2))
    for step in range(steps):
        canvas = np.zeros_like(image)
        for x, y in np.ndindex(image.shape):
            neighbours = find_valid_neighbours(image, x, y)
            if len(neighbours) < 9:
                continue
            decoded_number = int(''.join([str(x) for x in neighbours]), 2)
            input_pixel = iea[decoded_number]
            canvas[x, y] = input_pixel

        image = np.copy(canvas)
        # The void is blinking, so transform all 0 background pixels to 1
        if step % 2 == 0:
            image[:, 0] = 1
            image[:, -1] = 1
            image[0, :] = 1
            image[-1, :] = 1
            image = np.pad(image, (1, 1), constant_values=1)
        else:
            image = np.pad(image, (1, 1))

    return image


def part_one(iea, image):
    image = enhance_image(iea, image, 2)
    print(f"Answer 1: {(image == 1).sum()}")


def part_two(iea, image):
    image = enhance_image(iea, image, 50)
    print(f"Answer 2: {(image == 1).sum()}")


def main(input_file_path: str):
    iea, image = parse_input_file(input_file_path)
    part_one(iea, image)
    part_two(iea, image)


if __name__ == '__main__':
    fire.Fire(main)
