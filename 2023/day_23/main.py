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

    # solve_maze()

    part1_result = part1(lines)
    print(part1_result)
    # part2_result = part2(lines)
    # print(part2_result)


def draw_board(lines, seen):
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (x, y) in seen:
                print("O", end="")
            else:
                print(char, end="")
        print()


def solve_maze():
    maze = [
        [" ", "#", " ", " ", " ", " "],
        [" ", " ", " ", "#", "#", " "],
        [" ", "#", " ", "#", "#", " "],
        [" ", "#", " ", "#", " ", " "],
        [" ", "#", " ", "#", " ", "#"],
        [" ", "#", " ", " ", " ", " "],
        [" ", "#", "#", "#", "#", " "],
        [" ", " ", " ", " ", " ", " "],
    ]

    for line in maze:
        for char in line:
            print(char, end="")
        print()

    paths = []
    start_point = (0, 0)
    end_point = (5, 7)
    current_path = []
    current_path.append(start_point)

    def draw_board(path):
        for y, line in enumerate(maze):
            for x, char in enumerate(line):
                if (x, y) in path:
                    print("O", end="")
                else:
                    print(char, end="")
            print()

    def solve(current_node):
        x, y = current_node
        # print(current_node)
        if current_node == end_point:
            paths.append(list(current_path))
            print("hittat rätt")
            return

        up = (x, y - 1)
        right = (x + 1, y)
        down = (x, y + 1)
        left = (x - 1, y)

        adjacents = [up, right, down, left]
        for adjacent in adjacents:
            if (
                0 <= adjacent[1] < len(maze)
                and 0 <= adjacent[0] < len(maze[adjacent[1]])
                and adjacent not in current_path
                and maze[adjacent[1]][adjacent[0]] == " "
            ):
                current_path.append(adjacent)
                solve(adjacent)
                current_path.pop()

    solve(start_point)
    # print(paths)

    for path in paths:
        draw_board(path)


def part1(lines):
    start_point = (1, 0)
    end_point = (len(lines[0]) - 2, len(lines) - 1)

    paths = []
    current_path = [start_point]

    def solve(current_node):
        x, y = current_node
        if current_node == end_point:
            paths.append(list(current_path))
            # print("hittat rätt")
            return

        up = (x, y - 1)
        right = (x + 1, y)
        down = (x, y + 1)
        left = (x - 1, y)

        adjacents = [
            (up, [".", "^"]),
            (right, [".", ">"]),
            (down, [".", "v"]),
            (left, [".", "<"]),
        ]
        for adjacent, allowed_cells in adjacents:
            if (
                0 <= adjacent[1] < len(lines)
                and 0 <= adjacent[0] < len(lines[adjacent[1]])
                and adjacent not in current_path
                and lines[adjacent[1]][adjacent[0]] in allowed_cells
            ):
                current_path.append(adjacent)
                solve(adjacent)
                current_path.pop()

    solve(start_point)

    for path in paths:
        draw_board(lines, path)
        print()

    paths = [len(path) - 1 for path in paths]
    # print(paths)

    return max(paths)

    # for path in paths:
    # draw_board(lines, path)


def part2(lines):
    pass


if __name__ == "__main__":
    main()
