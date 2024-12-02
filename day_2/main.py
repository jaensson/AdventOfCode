import os
from lib.helpers import read_file
from typing import List


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(lines: List[str]):
    def is_safe(line):
        levels = line.split(" ")
        levels = [int(level) for level in levels]

        is_incrementing = levels[0] < levels[1]

        for i in range(len(levels) - 1):
            is_next_incremented = levels[i] < levels[i + 1]
            if (
                not (1 <= abs(levels[i] - levels[i + 1]) <= 3)
                or is_next_incremented != is_incrementing
            ):
                return False

        return True

    number_of_safes = 0
    for line in lines:
        if is_safe(line):
            number_of_safes += 1

    return number_of_safes


def part2(lines: List[str]):
    def is_safe(levels):

        is_incrementing = levels[0] < levels[1]

        for i in range(len(levels) - 1):
            is_next_incremented = levels[i] < levels[i + 1]
            if (
                not (1 <= abs(levels[i] - levels[i + 1]) <= 3)
                or is_next_incremented != is_incrementing
            ):
                return False

        return True

    number_of_safes = 0
    for line in lines:
        levels = line.split(" ")
        levels = [int(level) for level in levels]

        for i in range(len(levels)):
            copy = levels.copy()
            del copy[i]
            if is_safe(copy):
                number_of_safes += 1
                break

    return number_of_safes
