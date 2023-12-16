import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n")
    lines = [[*line] for line in lines]

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def get_stones(lines):
    rounded_stones = []
    cubed_stones = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "O":
                rounded_stones.append((x, y))
            if char == "#":
                cubed_stones.add((x, y))

    rounded_stones.sort(key=lambda coordinates: coordinates[1])

    return rounded_stones, cubed_stones


def draw_stones(lines, rounded_stones, cubed_stones):
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            stone = (x, y)
            if stone in rounded_stones:
                print("O", end="")
            elif stone in cubed_stones:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1(lines):
    rounded_stones, cubed_stones = get_stones(lines)
    for i, rounded_stone in enumerate(rounded_stones):
        x, y = rounded_stone
        while (
            y - 1 >= 0
            and (x, y - 1) not in rounded_stones
            and (x, y - 1) not in cubed_stones
        ):
            y -= 1

        rounded_stones[i] = (x, y)

    load = 0
    for x, y in rounded_stones:
        load += len(lines) - y

    return load


def part2(lines):
    CYCLES = 3
    rounded_stones, cubed_stones = get_stones(lines)

    directions = ["north", "west", "south", "east"]

    for cycle in range(CYCLES):
        if cycle % 1000000 == 0:
            print(cycle)
        for direction in directions:
            match direction:
                case "north":
                    rounded_stones.sort(key=lambda coordinates: coordinates[1])
                    for i, rounded_stone in enumerate(rounded_stones):
                        x, y = rounded_stone
                        while (
                            y - 1 >= 0
                            and (x, y - 1) not in rounded_stones
                            and (x, y - 1) not in cubed_stones
                        ):
                            y -= 1

                        rounded_stones[i] = (x, y)
                case "west":
                    rounded_stones.sort(key=lambda coordinates: coordinates[0])
                    for i, rounded_stone in enumerate(rounded_stones):
                        x, y = rounded_stone
                        while (
                            x - 1 >= 0
                            and (x - 1, y) not in rounded_stones
                            and (x - 1, y) not in cubed_stones
                        ):
                            x -= 1

                        rounded_stones[i] = (x, y)
                case "south":
                    rounded_stones.sort(
                        key=lambda coordinates: coordinates[1], reverse=True
                    )
                    for i, rounded_stone in enumerate(rounded_stones):
                        x, y = rounded_stone
                        while (
                            y + 1 < len(lines)
                            and (x, y + 1) not in rounded_stones
                            and (x, y + 1) not in cubed_stones
                        ):
                            y += 1

                        rounded_stones[i] = (x, y)
                case "east":
                    rounded_stones.sort(
                        key=lambda coordinates: coordinates[0], reverse=True
                    )
                    for i, rounded_stone in enumerate(rounded_stones):
                        x, y = rounded_stone
                        while (
                            x + 1 < len(lines[0])
                            and (x + 1, y) not in rounded_stones
                            and (x + 1, y) not in cubed_stones
                        ):
                            x += 1

                        rounded_stones[i] = (x, y)

    draw_stones(lines, rounded_stones, cubed_stones)


if __name__ == "__main__":
    main()
