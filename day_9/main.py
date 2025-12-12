import os
from lib.helpers import read_file
from enum import IntEnum
from typing import Self


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


class Direction(IntEnum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    UP = 4

    def direction(first, second) -> Self:
        if first[0] < second[0]:
            return Direction.RIGHT
        if first[0] > second[0]:
            return Direction.LEFT
        if first[1] < second[1]:
            return Direction.DOWN
        if first[1] > second[1]:
            return Direction.UP


class Corner(IntEnum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT = 4

    def corner(first: Direction, second: Direction) -> Self:
        corner_mapping = {
            (Direction.UP, Direction.RIGHT): Corner.TOP_LEFT,
            (Direction.LEFT, Direction.DOWN): Corner.TOP_LEFT,
            (Direction.UP, Direction.LEFT): Corner.TOP_RIGHT,
            (Direction.RIGHT, Direction.DOWN): Corner.TOP_RIGHT,
            (Direction.DOWN, Direction.LEFT): Corner.BOTTOM_RIGHT,
            (Direction.RIGHT, Direction.UP): Corner.BOTTOM_RIGHT,
            (Direction.DOWN, Direction.RIGHT): Corner.BOTTOM_LEFT,
            (Direction.LEFT, Direction.UP): Corner.BOTTOM_LEFT,
        }
        return corner_mapping[(first, second)]


def part2(tiles):
    number_of_tiles = len(tiles)

    corners = []
    for i in range(number_of_tiles):
        prev, current, next = (
            tiles[(i - 1) % number_of_tiles],
            tiles[i],
            tiles[(i + 1) % number_of_tiles],
        )

        prev_direction = Direction.direction(prev, current)
        next_direction = Direction.direction(current, next)
        corner = Corner.corner(prev_direction, next_direction)
        corners.append((current, corner))
        # print(
        #     prev, current, next, prev_direction.name, next_direction.name, corner.name
        # )

    # print(len(corners))

    valid_corner = {
        Corner.TOP_LEFT: (
            lambda first, second: first[0] <= second[0] and first[1] <= second[1]
        ),
        Corner.TOP_RIGHT: (
            lambda first, second: first[0] >= second[0] and first[1] <= second[1]
        ),
        Corner.BOTTOM_RIGHT: (
            lambda first, second: first[0] >= second[0] and first[1] >= second[1]
        ),
        Corner.BOTTOM_LEFT: (
            lambda first, second: first[0] <= second[0] and first[1] >= second[1]
        ),
    }
    for corner in corners:
        position, type = corner

        possible_rectangles = []
        for second_corner in corners:
            if corner == second_corner:
                continue
            if valid_corner[type](position, second_corner[0]):
                possible_rectangles.append(second_corner[0])
        print(position, type.name, possible_rectangles)
