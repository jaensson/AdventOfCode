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


def tilt_up(rounded_stones, horizontal_cubed_stones):
    cubed_stones = dict()

    for i, rounded_stone in enumerate(rounded_stones):
        x, y = rounded_stone
        current_cubed_stone = len(horizontal_cubed_stones[x]) - 1
        while (
            current_cubed_stone >= 0
            and y <= horizontal_cubed_stones[x][current_cubed_stone][1]
        ):
            current_cubed_stone -= 1

        rest_stone = (
            (x, -1)
            if current_cubed_stone < 0
            else horizontal_cubed_stones[x][current_cubed_stone]
        )

        if rest_stone not in cubed_stones:
            cubed_stones[rest_stone] = 0

        cubed_stones[rest_stone] += 1
        rounded_stones[i] = (x, rest_stone[1] + cubed_stones[rest_stone])


def tilt_left(rounded_stones, vertical_cubed_stones):
    cubed_stones = dict()

    for i, rounded_stone in enumerate(rounded_stones):
        x, y = rounded_stone
        current_cubed_stone = len(vertical_cubed_stones[y]) - 1
        while (
            current_cubed_stone >= 0
            and x <= vertical_cubed_stones[y][current_cubed_stone][0]
        ):
            current_cubed_stone -= 1

        rest_stone = (
            (-1, y)
            if current_cubed_stone < 0
            else vertical_cubed_stones[y][current_cubed_stone]
        )

        if rest_stone not in cubed_stones:
            cubed_stones[rest_stone] = 0

        cubed_stones[rest_stone] += 1
        rounded_stones[i] = (rest_stone[0] + cubed_stones[rest_stone], y)


def tilt_down(rounded_stones, horizontal_cubed_stones, height):
    cubed_stones = dict()

    for i, rounded_stone in enumerate(rounded_stones):
        x, y = rounded_stone
        current_cubed_stone = len(horizontal_cubed_stones[x]) - 1
        while (
            current_cubed_stone >= 0
            and y
            >= horizontal_cubed_stones[x][
                len(horizontal_cubed_stones[x]) - 1 - current_cubed_stone
            ][1]
        ):
            current_cubed_stone -= 1

        rest_stone = (
            (x, height)
            if current_cubed_stone < 0
            else horizontal_cubed_stones[x][
                len(horizontal_cubed_stones[x]) - 1 - current_cubed_stone
            ]
        )

        if rest_stone not in cubed_stones:
            cubed_stones[rest_stone] = 0

        cubed_stones[rest_stone] += 1
        rounded_stones[i] = (x, rest_stone[1] - cubed_stones[rest_stone])


def tilt_right(rounded_stones, vertical_cubed_stones, width):
    cubed_stones = dict()

    for i, rounded_stone in enumerate(rounded_stones):
        x, y = rounded_stone
        current_cubed_stone = len(vertical_cubed_stones[y]) - 1
        while (
            current_cubed_stone >= 0
            and x
            >= vertical_cubed_stones[y][
                len(vertical_cubed_stones[y]) - 1 - current_cubed_stone
            ][0]
        ):
            current_cubed_stone -= 1

        rest_stone = (
            (width, y)
            if current_cubed_stone < 0
            else vertical_cubed_stones[y][
                len(vertical_cubed_stones[y]) - 1 - current_cubed_stone
            ]
        )

        if rest_stone not in cubed_stones:
            cubed_stones[rest_stone] = 0

        cubed_stones[rest_stone] += 1
        rounded_stones[i] = (rest_stone[0] - cubed_stones[rest_stone], y)


def part2(lines):
    seen_cycles = dict()
    CYCLES = 1000000000
    rounded_stones, cubed_stones = get_stones(lines)
    unique_cycle = 0

    repeats = set()

    horizontal_cubed_stones = [[] for _ in range(len(lines[0]))]
    vertical_cubed_stones = [[] for _ in range(len(lines))]

    for cubed_stone in cubed_stones:
        x, y = cubed_stone
        horizontal_cubed_stones[x].append(cubed_stone)
        horizontal_cubed_stones[x].sort()
        vertical_cubed_stones[y].append(cubed_stone)
        vertical_cubed_stones[y].sort()

    for cycle in range(CYCLES):
        rounded_stones.sort()
        before = str(rounded_stones)
        if before in seen_cycles:
            if seen_cycles[before][1] in repeats:
                break

            repeats.add(seen_cycles[before][1])
            rounded_stones = seen_cycles[before][0]
            continue

        tilt_up(rounded_stones, horizontal_cubed_stones)
        tilt_left(rounded_stones, vertical_cubed_stones)
        tilt_down(rounded_stones, horizontal_cubed_stones, len(lines))
        tilt_right(rounded_stones, vertical_cubed_stones, len(lines[0]))

        seen_cycles[before] = (rounded_stones[::], unique_cycle)
        unique_cycle += 1

    seen_cycles = list(seen_cycles.values())
    seen_cycles.sort(key=lambda cycles: cycles[1])

    new_seen_cycles = []
    for seen_cycle in seen_cycles:
        if seen_cycle[1] in repeats:
            new_seen_cycles.append(seen_cycle[0])

    loads = []
    for elem in new_seen_cycles:
        load = 0
        for x, y in elem:
            load += len(lines) - y
        loads.append(load)

    return loads[(CYCLES - 1 - min(repeats)) % len(new_seen_cycles)]


if __name__ == "__main__":
    main()
