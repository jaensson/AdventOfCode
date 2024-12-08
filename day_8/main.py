import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(lines):
    def add(result, antinode):
        x, y = antinode

        if 0 <= x < len(lines[0]) and 0 <= y < len(lines):
            result.add((x, y))

    antennas = dict()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char.isalnum():
                if char not in antennas:
                    antennas[char] = set()
                antennas[char].add((x, y))

    result = set()
    for antenna in antennas.keys():
        test = list(antennas[antenna])

        for i in range(len(test)):
            for j in range(i + 1, len(test)):
                first = test[i]
                second = test[j]

                diff = (first[0] - second[0], first[1] - second[1])

                first_new = (first[0] + diff[0], first[1] + diff[1])
                second_new = (second[0] - diff[0], second[1] - diff[1])

                add(result, first_new)
                add(result, second_new)

    return len(result)


def part2(lines):
    def add(result, antinode):
        x, y = antinode

        if 0 <= x < len(lines[0]) and 0 <= y < len(lines):
            result.add((x, y))

    antennas = dict()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char.isalnum():
                if char not in antennas:
                    antennas[char] = set()
                antennas[char].add((x, y))

    result = set()
    for antenna in antennas.keys():
        test = list(antennas[antenna])

        for i in range(len(test)):
            for j in range(i + 1, len(test)):
                first = test[i]
                second = test[j]

                diff = (first[0] - second[0], first[1] - second[1])

                add(result, first)
                add(result, second)

                while 0 <= first[0] < len(lines[0]) and 0 <= first[1] < len(
                    lines
                ):
                    first = (first[0] + diff[0], first[1] + diff[1])
                    add(result, first)

                while 0 <= second[0] < len(lines[0]) and 0 <= second[1] < len(
                    lines
                ):
                    second = (second[0] - diff[0], second[1] - diff[1])
                    add(result, second)

    return len(result)
