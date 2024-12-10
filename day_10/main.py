import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    grid = [
        [int(v) if v.isdigit() else v for v in list(line)] for line in lines
    ]

    part1_result = part1(grid)
    print(part1_result)
    part2_result = part2(grid)
    print(part2_result)


def part1(grid):
    def walk(x, y):
        queue = []
        queue.append((x, y))

        score = set()
        while len(queue) != 0:
            x, y = queue.pop(0)
            current_height = grid[y][x]

            if current_height == 9:
                score.add((x, y))
                continue

            if 0 <= y - 1 < len(grid) and grid[y - 1][x] == current_height + 1:
                queue.append((x, y - 1))
            if 0 <= y + 1 < len(grid) and grid[y + 1][x] == current_height + 1:
                queue.append((x, y + 1))
            if (
                0 <= x - 1 < len(grid[0])
                and grid[y][x - 1] == current_height + 1
            ):
                queue.append((x - 1, y))
            if (
                0 <= x + 1 < len(grid[0])
                and grid[y][x + 1] == current_height + 1
            ):
                queue.append((x + 1, y))

        return len(score)

    result = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 0:
                result += walk(x, y)

    return result


def part2(grid):
    def walk(x, y):
        current_height = grid[y][x]
        if current_height == 9:
            return 1

        score = 0
        if 0 <= y - 1 < len(grid) and grid[y - 1][x] == current_height + 1:
            score += walk(x, y - 1)
        if 0 <= y + 1 < len(grid) and grid[y + 1][x] == current_height + 1:
            score += walk(x, y + 1)
        if 0 <= x - 1 < len(grid[0]) and grid[y][x - 1] == current_height + 1:
            score += walk(x - 1, y)
        if 0 <= x + 1 < len(grid[0]) and grid[y][x + 1] == current_height + 1:
            score += walk(x + 1, y)

        return score

    result = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 0:
                result += walk(x, y)

    return result
