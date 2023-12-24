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

    part1_result = part1(lines, start_point)
    print(part1_result)
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
    while True:
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
        if coordinates == start_point:
            break

    return len(path) // 2


def part2(lines, start_point):
    def find_path(lines, start_point):
        # Found the path of the pipes
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
        while True:
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
            if coordinates == start_point:
                break

        return set(path)

    def remove_non_pipes(lines, path):
        # Replace everything not in the path with ground
        new_lines = lines[::]
        for y, new_line in enumerate(new_lines):
            for x, char in enumerate(new_line):
                if (x, y) not in path:
                    lines[y][x] = "."

        return new_lines

    def add_extra_ground(lines):
        # Add extra space between squeezable pipes
        pipes = lines[::]
        vertical = {"||", "J|", "|L", "7|", "|F", "JL", "7F", "7L", "JF"}
        horizontal = {"--", "L-", "J-", "-7", "-F", "L7", "JF", "LF", "J7"}

        x_axis = set()
        y_axis = set()

        for y in range(len(pipes)):
            for x in range(len(pipes[y]) - 1):
                char = pipes[y][x]
                next_char = pipes[y][x + 1]

                arrangement = "".join([char, next_char])

                if arrangement in vertical:
                    x_axis.add(x + 1)

        for y in range(len(pipes) - 1):
            for x, char in enumerate(pipes[y]):
                char = pipes[y][x]
                next_char = pipes[y + 1][x]

                arrangement = "".join([char, next_char])

                if arrangement in horizontal:
                    y_axis.add(y + 1)

        x_axis = list(x_axis)
        y_axis = list(y_axis)

        x_axis.sort(reverse=True)
        y_axis.sort(reverse=True)

        for horizontal_index in x_axis:
            for pipe in pipes:
                char = pipe[horizontal_index - 1]
                next_char = pipe[horizontal_index]
                arrangement = "".join([char, next_char])

                if arrangement in vertical or "." in arrangement:
                    pipe.insert(horizontal_index, ".")
                else:
                    pipe.insert(horizontal_index, "-")

        for vertical_index in y_axis:
            new_pipe = []
            for i in range(len(pipes[vertical_index])):
                char = pipes[vertical_index - 1][i]
                next_char = pipes[vertical_index][i]
                arrangement = "".join([char, next_char])

                if arrangement in horizontal or "." in arrangement:
                    new_pipe.append(".")
                else:
                    new_pipe.append("|")

            pipes.insert(vertical_index, new_pipe)

        return pipes, (sorted(x_axis), sorted(y_axis))

    def replace_outside(lines, axes):
        # Replace every ground connected to the outside with "O"
        pipes = lines[::]
        x_axis, y_axis = axes

        width = len(pipes[0])
        pipes.insert(0, ["."] * width)
        pipes.insert(len(pipes), ["."] * width)
        for line in pipes:
            line.insert(0, ".")
            line.insert(len(line), ".")

        stack = []
        seen = set()
        start_point = (0, 0)
        stack.append(start_point)

        while len(stack) != 0:
            current_node = stack.pop()
            x, y = current_node

            seen.add(current_node)

            up = (x, y - 1)
            right = (x + 1, y)
            down = (x, y + 1)
            left = (x - 1, y)

            adjacents = [up, right, down, left]

            for adjacent in adjacents:
                if (
                    0 <= adjacent[1] < len(pipes)
                    and 0 <= adjacent[0] < len(pipes[adjacent[1]])
                    and adjacent not in seen
                    and pipes[adjacent[1]][adjacent[0]] == "."
                ):
                    stack.append(adjacent)

        for y, pipe in enumerate(pipes):
            for x, char in enumerate(pipe):
                if (x, y) in seen:
                    pipes[y][x] = "O"

        for y_index in y_axis:
            del pipes[y_index + 1]

        for pipe in pipes:
            for x_index in x_axis:
                del pipe[x_index + 1]

        return pipes

    def count_enclosed(lines):
        # Count ground enclosed by the pipes
        ground = 0
        for pipe in lines:
            ground += len([cell for cell in pipe if cell == "."])
        return ground

    # print(lines, start_point)
    path = find_path(lines, start_point)
    lines = remove_non_pipes(lines, path)
    lines, axes = add_extra_ground(lines)
    lines = replace_outside(lines, axes)
    enclosed_cells = count_enclosed(lines)

    return enclosed_cells


if __name__ == "__main__":
    main()
