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
    lines = [
        (
            line.split(" ")[0],
            int(line.split(" ")[1]),
            line.split(" ")[2]
            .replace("(", "")
            .replace(")", "")
            .replace("#", ""),
        )
        for line in lines
    ]

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def draw(path, seen):
    min_x = min([coordinate[0] for coordinate in path]) - 1
    min_y = min([coordinate[1] for coordinate in path]) - 1
    max_x = max([coordinate[0] for coordinate in path]) + 2
    max_y = max([coordinate[1] for coordinate in path]) + 2

    width = abs(max_x - min_x)
    height = abs(max_y - min_y)

    grid = []
    for y in range(min_y, max_y):
        row = []
        for x in range(min_x, max_x):
            if (x, y) in path:
                row.append("#")
            elif (x, y) in seen:
                row.append("O")
            else:
                row.append(".")
        grid.append(row)

    for row in grid:
        for cell in row:
            print(cell, end="")
        print()


def part1(lines):
    start = (0, 0)
    location = start
    path = set()
    for direction, steps, color in lines:
        if len(path) == 0:
            steps -= 1
            path.add(start)

        for step in range(steps):
            x, y = location
            match direction:
                case "U":
                    y -= 1
                case "R":
                    x += 1
                case "D":
                    y += 1
                case "L":
                    x -= 1

            location = (x, y)
            path.add(location)

    min_x = min([coordinate[0] for coordinate in path]) - 1
    min_y = min([coordinate[1] for coordinate in path]) - 1
    max_x = max([coordinate[0] for coordinate in path]) + 2
    max_y = max([coordinate[1] for coordinate in path]) + 2

    width = abs(max_x - min_x)
    height = abs(max_y - min_y)

    area = width * height

    stack = []
    seen = set()
    stack.append((min_x, min_y))
    while len(stack) != 0:
        node = stack.pop()
        x, y = node

        if node not in seen:
            seen.add(node)

        up = (x, y - 1)
        right = (x + 1, y)
        down = (x, y + 1)
        left = (x - 1, y)

        adjacents = [up, right, down, left]

        for adjacent in adjacents:
            if (
                min_y <= adjacent[1] < max_y
                and min_x <= adjacent[0] < max_x
                and adjacent not in seen
                and adjacent not in path
            ):
                stack.append(adjacent)

    area -= len(seen)

    # draw(path, seen)
    return area


def part2(lines):
    start = (0, 0)
    location = start
    path = set()
    for line in lines:
        direction = line[0]
        steps = line[1]
        color = line[2]

        if len(path) == 0:
            steps -= 1
            path.add(start)

        for step in range(steps):
            x, y = location
            match direction:
                case 3 | "U":
                    y -= 1
                case 0 | "R":
                    x += 1
                case 1 | "D":
                    y += 1
                case 2 | "L":
                    x -= 1

            location = (x, y)
            path.add(location)

    min_x = min([coordinate[0] for coordinate in path]) - 1
    min_y = min([coordinate[1] for coordinate in path]) - 1
    max_x = max([coordinate[0] for coordinate in path]) + 2
    max_y = max([coordinate[1] for coordinate in path]) + 2

    width = abs(max_x - min_x)
    height = abs(max_y - min_y)

    area = width * height

    # draw(path, path)

    grid = list(path)
    new_grid = dict()
    for coordinate in grid:
        x, y = coordinate
        if y not in new_grid:
            # new_grid[y] = {"min": x, "max": x}
            new_grid[y] = []
            # continue

        # new_grid[y]["min"] = min(new_grid[y]["min"], x)
        # new_grid[y]["max"] = max(new_grid[y]["max"], x)
        new_grid[y].append(x)

    area = 0
    new_grid = list(new_grid.items())
    new_grid.sort(key=lambda coordinates: coordinates[0])
    print(new_grid)
    area = 0
    for y, coordinate in new_grid:
        coordinate.sort()
        print(coordinate)
        area += abs(coordinate[-1] - coordinate[0]) + 1

    # for y, coordinate in new_grid:
    #     # min_x = coordinate["min"]
    #     # max_x = coordinate["max"]
    #     area = abs(max_x - min_x) + 1
    #     print(y, min_x, max_x, area)

    # print(new_grid)

    # grid.sort(key=lambda coordinates: coordinates[1])
    # print(grid)

    return area


if __name__ == "__main__":
    main()
