import os
from typing import List
from enum import Enum


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

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def get_starting_point(lines):
    TILES = {
        "|": [Tiles.NORTH, Tiles.SOUTH],
        "-": [Tiles.EAST, Tiles.WEST],
        "L": [Tiles.NORTH, Tiles.EAST],
        "J": [Tiles.NORTH, Tiles.WEST],
        "7": [Tiles.SOUTH, Tiles.WEST],
        "F": [Tiles.SOUTH, Tiles.EAST],
        ".": [Tiles.GROUND],
        "S": [Tiles.START],
    }

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == Tiles.START.value:
                connecting_pipes = []
                north = TILES[lines[y - 1][x]] if y - 1 >= 0 else []
                south = TILES[lines[y + 1][x]] if y + 1 < len(lines) else []
                west = TILES[lines[y][x - 1]] if x - 1 >= 0 else []
                east = TILES[lines[y][x + 1]] if x + 1 < len(lines[0]) else []

                if Tiles.SOUTH in north:
                    connecting_pipes.append(Tiles.NORTH)
                if Tiles.WEST in east:
                    connecting_pipes.append(Tiles.EAST)
                if Tiles.EAST in west:
                    connecting_pipes.append(Tiles.WEST)
                if Tiles.NORTH in south:
                    connecting_pipes.append(Tiles.SOUTH)

                tiles = [
                    tile
                    for tile in TILES.items()
                    if tile[0] != "." and tile[0] != "S"
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


def get_connecting_pipes(lines, coordinates):
    TILES = {
        "|": [Tiles.NORTH, Tiles.SOUTH],
        "-": [Tiles.EAST, Tiles.WEST],
        "L": [Tiles.NORTH, Tiles.EAST],
        "J": [Tiles.NORTH, Tiles.WEST],
        "7": [Tiles.SOUTH, Tiles.WEST],
        "F": [Tiles.SOUTH, Tiles.EAST],
        ".": [Tiles.GROUND],
        "S": [Tiles.START],
    }
    x, y = coordinates
    current_connecting_pipes = TILES[lines[y][x]]
    # print("nu är den", lines[y][x], current_connecting_pipes)

    north = TILES[lines[y - 1][x]] if y - 1 >= 0 else []
    south = TILES[lines[y + 1][x]] if y + 1 < len(lines) else []
    west = TILES[lines[y][x - 1]] if x - 1 >= 0 else []
    east = TILES[lines[y][x + 1]] if x + 1 < len(lines[0]) else []

    connecting_pipes = []

    if Tiles.SOUTH in north and Tiles.NORTH in current_connecting_pipes:
        connecting_pipes.append(Tiles.NORTH)
    if Tiles.WEST in east and Tiles.EAST in current_connecting_pipes:
        connecting_pipes.append(Tiles.EAST)
    if Tiles.EAST in west and Tiles.WEST in current_connecting_pipes:
        connecting_pipes.append(Tiles.WEST)
    if Tiles.NORTH in south and Tiles.SOUTH in current_connecting_pipes:
        connecting_pipes.append(Tiles.SOUTH)

    return connecting_pipes


def part1(lines):
    start_point = get_starting_point(lines)
    path = [start_point]

    current_pipe = -1
    while len([tile for tile in path if tile == start_point]) != 2:
        current_pipe += 1
        x, y = path[-1]
        connecting_pipes = get_connecting_pipes(lines, (x, y))
        # print(current_pipe, connecting_pipes)
        connecting_pipes_coordinates = []
        for connecting_pipe in connecting_pipes:
            match connecting_pipe:
                case Tiles.NORTH:
                    connecting_pipes_coordinates.append((x, y - 1))
                case Tiles.EAST:
                    connecting_pipes_coordinates.append((x + 1, y))
                case Tiles.WEST:
                    connecting_pipes_coordinates.append((x - 1, y))
                case Tiles.SOUTH:
                    connecting_pipes_coordinates.append((x, y + 1))

        if len(path) == 1:
            path.append(connecting_pipes_coordinates[0])
            continue

        connecting_pipes_coordinates = [
            coordinate
            for coordinate in connecting_pipes_coordinates
            if coordinate != path[-2]
        ]
        if len(connecting_pipes_coordinates) == 0:
            path.append(start_point)
            continue
        path.append(connecting_pipes_coordinates[0])

    # print("gingo", path)

    return len(path) // 2


def part2(lines):
    pass


if __name__ == "__main__":
    main()
