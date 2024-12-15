import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    result = None
    for i in range(len(lines)):
        if lines[i] == "":
            result = (lines[:i], lines[i + 1 :])
            break

    grid, moves = result

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "@":
                starting_position = (x, y)
                break
    grid = [list(row) for row in grid]

    grid_copy_part1 = [row[::] for row in grid]
    grid_copy_part2 = [row[::] for row in grid]

    part1_result = part1(grid_copy_part1, moves, starting_position)
    print(part1_result)
    part2_result = part2(grid_copy_part2, moves)
    print(part2_result)


def part1(grid, moves, starting_position):
    def draw_grid():
        for row in grid:
            for char in row:
                print(char, end="")
            print()

    def try_move_right(position):
        x, y = position
        if grid[y][x - 1] == "#":
            return position

        if grid[y][x - 1] == "O":
            try_move_right((x - 1, y))

        if grid[y][x - 1] == ".":
            grid[y][x], grid[y][x - 1] = grid[y][x - 1], grid[y][x]
            return (x - 1, y)

        return position

    def try_move_left(position):
        x, y = position
        if grid[y][x + 1] == "#":
            return position

        if grid[y][x + 1] == "O":
            try_move_left((x + 1, y))

        if grid[y][x + 1] == ".":
            grid[y][x], grid[y][x + 1] = grid[y][x + 1], grid[y][x]
            return (x + 1, y)

        return position

    def try_move_up(position):
        x, y = position
        if grid[y - 1][x] == "#":
            return position

        if grid[y - 1][x] == "O":
            try_move_up((x, y - 1))

        if grid[y - 1][x] == ".":
            grid[y][x], grid[y - 1][x] = grid[y - 1][x], grid[y][x]
            return (x, y - 1)

        return position

    def try_move_down(position):
        x, y = position
        if grid[y + 1][x] == "#":
            return position

        if grid[y + 1][x] == "O":
            try_move_down((x, y + 1))

        if grid[y + 1][x] == ".":
            grid[y][x], grid[y + 1][x] = grid[y + 1][x], grid[y][x]
            return (x, y + 1)

        return position

    current_position = starting_position
    for move in "".join(moves):
        if move == "<":
            current_position = try_move_right(current_position)
        if move == ">":
            current_position = try_move_left(current_position)
        if move == "^":
            current_position = try_move_up(current_position)
        if move == "v":
            current_position = try_move_down(current_position)

    result = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "O":
                result += 100 * y + x

    return result


def part2(grid, moves):
    def draw_grid(grid):
        for row in grid:
            for char in row:
                print(char, end="")
            print()

    def try_move_left(grid, position):
        x, y = position
        if grid[y][x - 1] == "#":
            return position

        if grid[y][x - 1] == "[" or grid[y][x - 1] == "]":
            try_move_left(grid, (x - 1, y))

        if grid[y][x - 1] == ".":
            grid[y][x], grid[y][x - 1] = grid[y][x - 1], grid[y][x]
            return (x - 1, y)

        return position

    def try_move_right(grid, position):
        x, y = position
        if grid[y][x + 1] == "#":
            return position

        if grid[y][x + 1] == "[" or grid[y][x + 1] == "]":
            try_move_right(grid, (x + 1, y))

        if grid[y][x + 1] == ".":
            grid[y][x], grid[y][x + 1] = grid[y][x + 1], grid[y][x]
            return (x + 1, y)

        return position

    def try_move_up(grid, position):
        def can_move_stone_up(grid, position):
            x, y = position

            if grid[y][x] == "[" and grid[y - 1][x] == ".":
                return True

            if grid[y][x] == "]" and grid[y - 1][x] == ".":
                return True

            if grid[y - 1][x] == "[":
                left = can_move_stone_up(grid, (x, y - 1))
                right = can_move_stone_up(grid, (x + 1, y - 1))

                if left and right:
                    return True

            if grid[y - 1][x] == "]":
                left = can_move_stone_up(grid, (x - 1, y - 1))
                right = can_move_stone_up(grid, (x, y - 1))

                if left and right:
                    return True

            return False

        def move_up(grid, position):
            x, y = position

            if grid[y - 1][x] == "[":
                move_up(grid, (x, y - 1))
                move_up(grid, (x + 1, y - 1))
            if grid[y - 1][x] == "]":
                move_up(grid, (x, y - 1))
                move_up(grid, (x - 1, y - 1))

            if grid[y - 1][x] == ".":
                grid[y][x], grid[y - 1][x] = grid[y - 1][x], grid[y][x]
                return (x, y - 1)

            return position

        x, y = position
        if grid[y - 1][x] == "#":
            return position

        if grid[y - 1][x] == "]":
            left = can_move_stone_up(grid, (x - 1, y - 1))
            right = can_move_stone_up(grid, (x, y - 1))

            if left and right:
                move_up(grid, (x - 1, y - 1))
                move_up(grid, (x, y - 1))

        if grid[y - 1][x] == "[":
            left = can_move_stone_up(grid, (x, y - 1))
            right = can_move_stone_up(grid, (x + 1, y - 1))

            if left and right:
                move_up(grid, (x, y - 1))
                move_up(grid, (x + 1, y - 1))

        if grid[y - 1][x] == ".":
            grid[y][x], grid[y - 1][x] = grid[y - 1][x], grid[y][x]
            return (x, y - 1)

        return position

    def try_move_down(grid, position):
        def can_move_stone_down(grid, position):
            x, y = position

            if grid[y][x] == "[" and grid[y + 1][x] == ".":
                return True

            if grid[y][x] == "]" and grid[y + 1][x] == ".":
                return True

            if grid[y + 1][x] == "[":
                left = can_move_stone_down(grid, (x, y + 1))
                right = can_move_stone_down(grid, (x + 1, y + 1))

                if left and right:
                    return True

            if grid[y + 1][x] == "]":
                left = can_move_stone_down(grid, (x - 1, y + 1))
                right = can_move_stone_down(grid, (x, y + 1))

                if left and right:
                    return True

            return False

        def move_down(grid, position):
            x, y = position

            if grid[y + 1][x] == "[":
                move_down(grid, (x, y + 1))
                move_down(grid, (x + 1, y + 1))
            if grid[y + 1][x] == "]":
                move_down(grid, (x, y + 1))
                move_down(grid, (x - 1, y + 1))

            if grid[y + 1][x] == ".":
                grid[y][x], grid[y + 1][x] = grid[y + 1][x], grid[y][x]
                return (x, y - 1)

            return position

        x, y = position
        if grid[y + 1][x] == "#":
            return position

        if grid[y + 1][x] == "]":
            left = can_move_stone_down(grid, (x - 1, y + 1))
            right = can_move_stone_down(grid, (x, y + 1))

            if left and right:
                move_down(grid, (x - 1, y + 1))
                move_down(grid, (x, y + 1))

        if grid[y + 1][x] == "[":
            left = can_move_stone_down(grid, (x, y + 1))
            right = can_move_stone_down(grid, (x + 1, y + 1))

            if left and right:
                move_down(grid, (x, y + 1))
                move_down(grid, (x + 1, y + 1))

        if grid[y + 1][x] == ".":
            grid[y][x], grid[y + 1][x] = grid[y + 1][x], grid[y][x]
            return (x, y + 1)

        return position

    scaled_grid = []
    for row in grid:
        scaled_row = []
        for char in row:
            if char == ".":
                scaled_row.append(".")
                scaled_row.append(".")
            if char == "#":
                scaled_row.append("#")
                scaled_row.append("#")
            if char == "O":
                scaled_row.append("[")
                scaled_row.append("]")
            if char == "@":
                scaled_row.append("@")
                scaled_row.append(".")
        scaled_grid.append(scaled_row)

    current_position = None
    for y, row in enumerate(scaled_grid):
        for x, char in enumerate(row):
            if char == "@":
                current_position = (x, y)
                break

    for move in "".join(moves):
        if move == "<":
            current_position = try_move_left(scaled_grid, current_position)
        if move == ">":
            current_position = try_move_right(scaled_grid, current_position)
        if move == "^":
            current_position = try_move_up(scaled_grid, current_position)
        if move == "v":
            current_position = try_move_down(scaled_grid, current_position)

    result = 0
    for y, row in enumerate(scaled_grid):
        for x, char in enumerate(row):
            if char == "[":
                result += 100 * y + x

    return result
