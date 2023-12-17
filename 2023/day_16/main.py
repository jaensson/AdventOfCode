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


def walk(lines, node):
    x, y, direction = node
    stack = []
    seen = set()

    start = (x, y, direction)
    stack.append(start)

    while len(stack) != 0:
        current_node = stack.pop()
        x, y, direction = current_node

        if current_node in seen:
            continue

        seen.add(current_node)

        match direction:
            case "up":
                if y - 1 < 0:
                    continue
                next_cell = lines[y - 1][x]
                if next_cell == "|" or next_cell == ".":
                    stack.append((x, y - 1, "up"))
                if next_cell == "-":
                    stack.append((x, y - 1, "right"))
                    stack.append((x, y - 1, "left"))
                if next_cell == "/":
                    stack.append((x, y - 1, "right"))
                if next_cell == "\\":
                    stack.append((x, y - 1, "left"))
            case "right":
                if x + 1 >= len(lines[y]):
                    continue
                next_cell = lines[y][x + 1]
                if next_cell == "|":
                    stack.append((x + 1, y, "up"))
                    stack.append((x + 1, y, "down"))
                if next_cell == "-" or next_cell == ".":
                    stack.append((x + 1, y, "right"))
                if next_cell == "/":
                    stack.append((x + 1, y, "up"))
                if next_cell == "\\":
                    stack.append((x + 1, y, "down"))
            case "down":
                if y + 1 >= len(lines):
                    continue
                next_cell = lines[y + 1][x]
                if next_cell == "|" or next_cell == ".":
                    stack.append((x, y + 1, "down"))
                if next_cell == "-":
                    stack.append((x, y + 1, "right"))
                    stack.append((x, y + 1, "left"))
                if next_cell == "/":
                    stack.append((x, y + 1, "left"))
                if next_cell == "\\":
                    stack.append((x, y + 1, "right"))
            case "left":
                if x - 1 < 0:
                    continue
                next_cell = lines[y][x - 1]
                if next_cell == "|":
                    stack.append((x - 1, y, "up"))
                    stack.append((x - 1, y, "down"))
                if next_cell == "-" or next_cell == ".":
                    stack.append((x - 1, y, "left"))
                if next_cell == "/":
                    stack.append((x - 1, y, "down"))
                if next_cell == "\\":
                    stack.append((x - 1, y, "up"))

    path = set((x, y) for x, y, direction in list(seen))

    return path


def part1(lines):
    if lines[0][0] == "." or lines[0][0] == "-":
        direction = "right"
    elif lines[0][0] == "\\":
        direction = "down"

    path = walk(
        lines,
        (0, 0, direction),
    )

    return len(path)


def part2(lines):
    length = len(lines)
    width = len(lines[0])

    up = [(x, 0, "down") for x in range(width)]
    right = [(width - 1, y, "left") for y in range(length)]
    down = [(x, length - 1, "up") for x in range(width)]
    left = [(0, y, "right") for y in range(length)]

    starting_points = []
    starting_points.extend(up)
    starting_points.extend(right)
    starting_points.extend(down)
    starting_points.extend(left)

    path = []

    for node in starting_points:
        path.append(len(walk(lines, node)))

    return max(path)


if __name__ == "__main__":
    main()
