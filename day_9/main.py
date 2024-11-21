import os
from typing import List
from enum import Enum
import math


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n")
    lines = [list_to_int(line.split(" ")) for line in lines]

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def list_to_int(list):
    return [int(element) for element in list]


def part1(lines):
    result = []

    for line in lines:
        sequence = [line]

        while len([element for element in sequence[-1] if element != 0]) != 0:
            difference = []

            for i in range(len(sequence[-1]) - 1):
                difference.append(sequence[-1][i + 1] - sequence[-1][i])

            sequence.append(difference)

        sequence[-1].append(0)
        sequence = sequence[::-1]

        for i, difference in enumerate(sequence[:-1]):
            next = sequence[i][-1] + sequence[i + 1][-1]
            sequence[i + 1].append(next)

        result.append(next)

    return sum(result)


def part2(lines):
    result = []

    for line in lines:
        sequence = [line]

        while len([element for element in sequence[-1] if element != 0]) != 0:
            difference = []

            for i in range(len(sequence[-1]) - 1):
                difference.append(sequence[-1][i + 1] - sequence[-1][i])

            sequence.append(difference)

        sequence[-1].append(0)
        sequence = sequence[::-1]

        for i, difference in enumerate(sequence[:-1]):
            prev = sequence[i + 1][0] - sequence[i][0]
            sequence[i + 1].insert(0, prev)

        result.append(prev)

    return sum(result)


if __name__ == "__main__":
    main()
