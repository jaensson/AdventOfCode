import os
from lib.helpers import read_file
from enum import IntEnum


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    tiles = parse_input(lines)

    result = part1(tiles)
    print(result)

    result = part2(tiles)
    print(result)


def parse_input(lines):
    tiles = []
    for line in lines:
        x, y = [int(coordinate) for coordinate in line.split(",")]
        tiles.append((x, y))
    return tiles


def part1(tiles):
    max_area = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            first, second = tiles[i], tiles[j]
            area = (abs(first[0] - second[0]) + 1) * (abs(first[1] - second[1]) + 1)
            max_area = max(max_area, area)

    return max_area


def part2(tiles):
    class Direction(IntEnum):
        LEFT = 1
        RIGHT = 2
        DOWN = 3
        UP = 4

    def direction(first, second):
        if first[0] < second[0]:
            return Direction.RIGHT
        if first[0] > second[0]:
            return Direction.LEFT
        if first[1] < second[1]:
            return Direction.DOWN
        if first[1] > second[1]:
            return Direction.UP

    def ascending(first, second):
        return (first, second) if first < second else (second, first)

    def is_inside(rectangles, corner):
        for first, second in rectangles:
            min_x, max_x = ascending(first[0], second[0])
            min_y, max_y = ascending(first[1], second[1])

            if min_x <= corner[0] <= max_x and min_y <= corner[1] <= max_y:
                return True

        return False

    red_tiles = set(tiles)
    valid_rectangles = set()
    tiles.append(tiles[0])
    tiles.append(tiles[1])
    for i in range(len(tiles) - 2):
        first, middle, second = tiles[i], tiles[i + 1], tiles[i + 2]

        min_x, max_x = ascending(first[0], second[0])
        min_y, max_y = ascending(first[1], second[1])

        first_step = direction(first, middle)
        second_step = direction(middle, second)

        is_part_of_figure = (
            (first_step == Direction.UP and second_step == Direction.RIGHT)
            or (first_step == Direction.DOWN and second_step == Direction.LEFT)
            or (first_step == Direction.LEFT and second_step == Direction.UP)
            or (first_step == Direction.RIGHT and second_step == Direction.DOWN)
        )
        if not is_part_of_figure:
            continue

        is_rectangle = True
        for x, y in red_tiles:
            if min_x < x < max_x and min_y < y < max_y:
                is_rectangle = False

        if not is_rectangle:
            continue

        valid_rectangles.add((first, second))

    max_area = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            first, second = tiles[i], tiles[j]

            min_x, max_x = ascending(first[0], second[0])
            min_y, max_y = ascending(first[1], second[1])

            is_rectangle = True
            for x, y in red_tiles:
                if min_x < x < max_x and min_y < y < max_y:
                    is_rectangle = False
            if not is_rectangle:
                continue

            third, fourth = (first[0], second[1]), (second[0], first[1])
            if is_inside(valid_rectangles, third) and is_inside(
                valid_rectangles, fourth
            ):
                area = (abs(first[0] - second[0]) + 1) * (abs(first[1] - second[1]) + 1)
                max_area = max(max_area, area)

    return max_area
