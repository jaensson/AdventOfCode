import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    result = part1(lines)
    print(result)

    result = part2(lines)
    print(result)


def part1(lines):
    result = 0
    for line in lines:
        current_largest = 0
        for i in range(1, len(line) - 1):
            if int(line[i]) > int(line[current_largest]):
                current_largest = i

        second_largest = current_largest + 1
        for i in range(current_largest + 1, len(line)):
            if int(line[i]) > int(line[second_largest]):
                second_largest = i

        result += int(f"{line[current_largest]}{line[second_largest]}")

    return result


def part2(lines):
    result = 0

    length_of_number = 12
    for line in lines:
        current_largest = ""
        next_index = 0
        while len(current_largest) != length_of_number:
            for i in range(
                next_index + 1,
                len(line) - length_of_number + len(current_largest) + 1,
            ):
                if (int(line[i])) > int(line[next_index]):
                    next_index = i

            current_largest += line[next_index]
            next_index += 1

        result += int(current_largest)

    return result
