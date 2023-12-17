import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n\n")
    lines = [line.split("\n") for line in lines]

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(lines):
    # print(lines)
    total = 0
    for line in lines:
        vertical_grid = []
        for x in range(len(line[0])):
            row = ""
            for y in range(len(line)):
                row += line[y][x]
            vertical_grid.append(row)

        checking_grids = [vertical_grid, line]

        values = [0, 0]
        for i, checking_grid in enumerate(checking_grids):
            for mirror in range(1, len(checking_grid[1:]) + 1):
                left = "".join(checking_grid[:mirror][::-1])
                right = "".join(checking_grid[mirror:])

                length = min(len(left), len(right))
                left = left[:length]
                right = right[:length]

                if left == right:
                    values[i] = mirror
                    break

        vertical = values[0]
        horizontal = values[1]

        total += vertical + (horizontal * 100)

    return total


def part2(lines):
    total = 0
    for line in lines:
        vertical_grid = []
        for x in range(len(line[0])):
            row = ""
            for y in range(len(line)):
                row += line[y][x]
            vertical_grid.append(row)

        checking_grids = [vertical_grid, line]

        values = [0, 0]
        for i, checking_grid in enumerate(checking_grids):
            for mirror in range(1, len(checking_grid[1:]) + 1):
                left = "".join(checking_grid[:mirror][::-1])
                right = "".join(checking_grid[mirror:])

                length = min(len(left), len(right))
                left = left[:length]
                right = right[:length]

                difference_counter = 0
                for j in range(len(left)):
                    if left[j] != right[j]:
                        difference_counter += 1

                if difference_counter == 1:
                    values[i] = mirror
                    break

        vertical = values[0]
        horizontal = values[1]

        total += vertical + (horizontal * 100)

    return total


if __name__ == "__main__":
    main()
