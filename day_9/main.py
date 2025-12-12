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


def print_grid(tiles):
    min_x = min(tiles, key=lambda tile: tile[0])[0]
    max_x = max(tiles, key=lambda tile: tile[0])[0]
    min_y = min(tiles, key=lambda tile: tile[1])[1]
    max_y = max(tiles, key=lambda tile: tile[1])[1]

    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            if (x, y) in tiles:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1(tiles):
    max_area = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            first, second = tiles[i], tiles[j]
            area = (abs(first[0] - second[0]) + 1) * (
                abs(first[1] - second[1]) + 1
            )
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

    corners = []
    walls = []
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

        min_x, max_x = ascending(current[0], next[0])
        min_y, max_y = ascending(current[1], next[1])
        walls.append(((min_x, max_x), (min_y, max_y)))

    # print(len(corners))

    # has_wall_inside(walls, (7, 1), (9, 5))
    # has_wall_inside(walls, (11, 7), (7, 3))
    # has_wall_inside(walls, (11, 7), (2, 3))

    valid_corner = {
        Corner.TOP_LEFT: (
            lambda first, second: first[0] <= second[0]
            and first[1] <= second[1]
        ),
        Corner.TOP_RIGHT: (
            lambda first, second: first[0] >= second[0]
            and first[1] <= second[1]
        ),
        Corner.BOTTOM_RIGHT: (
            lambda first, second: first[0] >= second[0]
            and first[1] >= second[1]
        ),
        Corner.BOTTOM_LEFT: (
            lambda first, second: first[0] <= second[0]
            and first[1] >= second[1]
        ),
    }
    valid_rectangles = set()
    for corner in corners:
        position, type = corner

        for second_corner in corners:
            if (
                corner == second_corner
                or not valid_corner[type](position, second_corner[0])
                or has_tile_inside(tiles, position, second_corner[0])
                or has_wall_inside(walls, position, second_corner[0])
            ):
                continue

            if (position, second_corner[0]) in valid_rectangles or (
                second_corner[0],
                position,
            ) in valid_rectangles:
                continue
            valid_rectangles.add((position, second_corner[0]))

    max_area = 0
    for rectangle in valid_rectangles:
        first, second = rectangle

        min_x, max_x = ascending(first[0], second[0])
        min_y, max_y = ascending(first[1], second[1])

        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        max_area = max(max_area, area)

    return max_area
