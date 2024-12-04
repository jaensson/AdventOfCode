import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    # part1_result = part1(lines)
    # print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(grid):
    # print(grid)

    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != "X":
                continue
            # print(x, y)

            horizontal = grid[y][x : x + 4]
            horizontal_backwards = grid[y][x - 3 : x + 1]

            vertical_up = (
                "".join([grid[y - i][x] for i in range(4)])
                if y - 3 >= 0
                else ""
            )
            vertical_down = (
                "".join([grid[y + i][x] for i in range(4)])
                if y + 3 < len(grid)
                else ""
            )

            diagonal_down_right = (
                "".join([grid[y + i][x + i] for i in range(4)])
                if y + 3 < len(grid) and x + 3 < len(grid[0])
                else ""
            )
            # print(diagonal_down_right)

            diagonal_down_left = (
                "".join([grid[y + i][x - i] for i in range(4)])
                if y + 3 < len(grid) and x - 3 >= 0
                else ""
            )

            diagnoal_up_left = (
                "".join([grid[y - i][x - i] for i in range(4)])
                if y - 3 >= 0 and x - 3 >= 0
                else ""
            )

            diagnoal_up_right = (
                "".join([grid[y - i][x + i] for i in range(4)])
                if y - 3 >= 0 and x + 3 < len(grid[0])
                else ""
            )

            result = [
                horizontal,
                horizontal_backwards,
                vertical_up,
                vertical_down,
                diagnoal_up_left,
                diagnoal_up_right,
                diagonal_down_left,
                diagonal_down_right,
            ]

            for res in result:
                # print(res)
                if res == "XMAS" or res == "SAMX":
                    total += 1

    return total


def part2(grid):
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != "A":
                continue

            left_diagonal = (
                grid[y - 1][x - 1] + grid[y][x] + grid[y + 1][x + 1]
                if y - 1 >= 0
                and y + 1 < len(grid)
                and x - 1 >= 0
                and x + 1 < len(grid[0])
                else ""
            )

            right_diagonal = (
                grid[y + 1][x - 1] + grid[y][x] + grid[y - 1][x + 1]
                if y - 1 >= 0
                and y + 1 < len(grid)
                and x - 1 >= 0
                and x + 1 < len(grid[0])
                else ""
            )

            if left_diagonal != "MAS" and left_diagonal != "SAM":
                continue

            # print(left_diagonal, right_diagonal)
            if (
                left_diagonal == right_diagonal
                or left_diagonal == right_diagonal[::-1]
                or left_diagonal[::-1] == right_diagonal
            ):
                total += 1

    return total
