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
    lines = [[*line] for line in lines]

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    start_point = get_starting_point(lines)

    # part1_result = part1(lines, start_point)
    # print(part1_result)
    part2_result = part2(lines, start_point)
    print(part2_result)


def get_starting_point(lines):
    NORTH = "north"
    EAST = "east"
    WEST = "west"
    SOUTH = "south"
    GROUND = "."
    START = "S"

    TILES = {
        "|": [NORTH, SOUTH],
        "-": [EAST, WEST],
        "L": [NORTH, EAST],
        "J": [NORTH, WEST],
        "7": [SOUTH, WEST],
        "F": [SOUTH, EAST],
        ".": [],
    }

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == START:
                connecting_pipes = []
                north = TILES[lines[y - 1][x]] if y - 1 >= 0 else []
                south = TILES[lines[y + 1][x]] if y + 1 < len(lines) else []
                west = TILES[lines[y][x - 1]] if x - 1 >= 0 else []
                east = TILES[lines[y][x + 1]] if x + 1 < len(lines[0]) else []

                if SOUTH in north:
                    connecting_pipes.append(NORTH)
                if WEST in east:
                    connecting_pipes.append(EAST)
                if EAST in west:
                    connecting_pipes.append(WEST)
                if NORTH in south:
                    connecting_pipes.append(SOUTH)

                tiles = [
                    tile
                    for tile in TILES.items()
                    if tile[0] != GROUND and tile[0] != START
                ]

                for tile in tiles:
                    direction, pipes = tile
                    is_valid = True
                    for pipe in pipes:
                        if pipe not in connecting_pipes:
                            is_valid = False
                    if is_valid:
                        lines[y][x] = direction

                return (x, y)


def part1(lines, start_point):
    path = [start_point]

    NORTH = "north"
    EAST = "east"
    WEST = "west"
    SOUTH = "south"

    TILES = {
        "|": [NORTH, SOUTH],
        "-": [EAST, WEST],
        "L": [NORTH, EAST],
        "J": [NORTH, WEST],
        "7": [SOUTH, WEST],
        "F": [SOUTH, EAST],
    }

    previous_walk = None
    previous_coords = start_point
    while len([tile for tile in path if tile == start_point]) != 2:
        x, y = previous_coords
        directions = TILES[lines[y][x]][::]

        if previous_walk is not None:
            if previous_walk == NORTH and SOUTH in directions:
                directions.remove(SOUTH)
            elif previous_walk == EAST and WEST in directions:
                directions.remove(WEST)
            elif previous_walk == WEST and EAST in directions:
                directions.remove(EAST)
            elif previous_walk == SOUTH and NORTH in directions:
                directions.remove(NORTH)

        walk = directions[0]
        if walk == NORTH:
            coordinates = (x, y - 1)
        elif walk == EAST:
            coordinates = (x + 1, y)
        elif walk == WEST:
            coordinates = (x - 1, y)
        elif walk == SOUTH:
            coordinates = (x, y + 1)

        previous_coords = coordinates
        previous_walk = walk
        path.append(coordinates)

    return len(path) // 2


def part2(lines, start_point):
    path = [start_point]

    NORTH = "north"
    EAST = "east"
    WEST = "west"
    SOUTH = "south"

    TILES = {
        "|": [NORTH, SOUTH],
        "-": [EAST, WEST],
        "L": [NORTH, EAST],
        "J": [NORTH, WEST],
        "7": [SOUTH, WEST],
        "F": [SOUTH, EAST],
    }

    previous_walk = None
    previous_coords = start_point
    while len([tile for tile in path if tile == start_point]) != 2:
        x, y = previous_coords
        directions = TILES[lines[y][x]][::]

        if previous_walk is not None:
            if previous_walk == NORTH and SOUTH in directions:
                directions.remove(SOUTH)
            elif previous_walk == EAST and WEST in directions:
                directions.remove(WEST)
            elif previous_walk == WEST and EAST in directions:
                directions.remove(EAST)
            elif previous_walk == SOUTH and NORTH in directions:
                directions.remove(NORTH)

        walk = directions[0]
        if walk == NORTH:
            coordinates = (x, y - 1)
        elif walk == EAST:
            coordinates = (x + 1, y)
        elif walk == WEST:
            coordinates = (x - 1, y)
        elif walk == SOUTH:
            coordinates = (x, y + 1)

        previous_coords = coordinates
        previous_walk = walk
        path.append(coordinates)

    min_x = path[0][0]
    max_x = min_x
    min_y = path[0][1]
    max_y = min_y

    for coordinate in path:
        x, y = coordinate
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    counter = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) not in path:
                print("O", end="")
            else:
                print(lines[y][x], end="")
                counter += 1
        print()

    print(counter)

    return counter


if __name__ == "__main__":
    main()
