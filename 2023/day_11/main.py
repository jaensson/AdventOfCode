import os
from typing import List
from enum import Enum
import time


class File(Enum):
    READ = "r"


class Tiles(Enum):
    NORTH = "north"
    EAST = "east"
    WEST = "west"
    SOUTH = "south"
    GROUND = "ground"
    START = "S"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n")

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
    positions_x = set()
    positions_y = set()

    galaxies = []
    galaxy_counter = 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                galaxy_counter += 1
                positions_x.add(x)
                positions_y.add(y)
                galaxies.append((x, y))

    positions_x = {
        elem for elem in range(len(lines[0])) if elem not in positions_x
    }
    positions_y = {
        elem for elem in range(len(lines)) if elem not in positions_y
    }

    steps = []

    for i in range(len(galaxies)):
        galaxy = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            pair = galaxies[j]
            step_counter = abs(galaxy[0] - pair[0]) + abs(galaxy[1] - pair[1])

            for position_x in positions_x:
                if (
                    galaxy[0] < position_x < pair[0]
                    or pair[0] < position_x < galaxy[0]
                ):
                    step_counter += 1

            for position_y in positions_y:
                if (
                    galaxy[1] < position_y < pair[1]
                    or pair[1] < position_y < galaxy[1]
                ):
                    step_counter += 1

            steps.append(step_counter)

    return sum(steps)


def part2(lines):
    positions_x = set()
    positions_y = set()

    galaxies = []
    galaxy_counter = 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                galaxy_counter += 1
                positions_x.add(x)
                positions_y.add(y)
                galaxies.append((x, y))

    positions_x = {
        elem for elem in range(len(lines[0])) if elem not in positions_x
    }
    positions_y = {
        elem for elem in range(len(lines)) if elem not in positions_y
    }

    steps = []

    STEP_BETWEEN = 1000000
    for i in range(len(galaxies)):
        galaxy = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            pair = galaxies[j]
            step_counter = abs(galaxy[0] - pair[0]) + abs(galaxy[1] - pair[1])

            for position_x in positions_x:
                if (
                    galaxy[0] < position_x < pair[0]
                    or pair[0] < position_x < galaxy[0]
                ):
                    step_counter += STEP_BETWEEN - 1

            for position_y in positions_y:
                if (
                    galaxy[1] < position_y < pair[1]
                    or pair[1] < position_y < galaxy[1]
                ):
                    step_counter += STEP_BETWEEN - 1

            steps.append(step_counter)

    return sum(steps)


if __name__ == "__main__":
    main()
