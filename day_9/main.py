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


def part2(tiles):
    def ascending(first, second):
        if second < first:
            return second, first
        return first, second

    def has_wall_inside(walls, first, second):
        min_x, max_x = ascending(first[0], second[0])
        min_y, max_y = ascending(first[1], second[1])

        for wall in walls:
            x, y = wall
            if (
                not x[1] <= min_x
                and not x[0] >= max_x
                and not y[1] <= min_y
                and not y[0] >= max_y
            ):
                return True
        return False

    def has_tile_inside(tiles, first, second):
        min_x, max_x = ascending(first[0], second[0])
        min_y, max_y = ascending(first[1], second[1])

        for x, y in tiles:
            if min_x < x < max_x and min_y < y < max_y:
                return True

        return False

    number_of_tiles = len(tiles)
    walls = []
    for i in range(number_of_tiles):
        current, next = tiles[i], tiles[(i + 1) % number_of_tiles]
        min_x, max_x = ascending(current[0], next[0])
        min_y, max_y = ascending(current[1], next[1])
        walls.append(((min_x, max_x), (min_y, max_y)))

    is_valid_corner = {
        Direction.UP: (lambda first, second: first[0] <= second[0]),
        Direction.RIGHT: (lambda first, second: first[1] >= second[1]),
        Direction.DOWN: (lambda first, second: first[0] <= second[0]),
        Direction.LEFT: (lambda first, second: first[1] >= second[1]),
    }

    max_area = 0
    for i in range(number_of_tiles):
        prev, current = tiles[(i - 1) % number_of_tiles], tiles[i]
        direction = Direction.direction(prev, current)

        for j in range(i + 1, number_of_tiles):
            tile = tiles[j]
            if (
                not is_valid_corner[direction](current, tile)
                or has_tile_inside(tiles, current, tile)
                or has_wall_inside(walls, current, tile)
            ):
                continue

            area = (abs(current[0] - tile[0]) + 1) * (abs(current[1] - tile[1]) + 1)
            max_area = max(max_area, area)

    return max_area
