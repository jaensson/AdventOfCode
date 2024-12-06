import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [list(line) for line in lines]

    starting_point = 0

    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "^":
                starting_point = (x, y, 0)
                break

    # print(starting_point)

    # part1_result = part1(lines, starting_point)
    # print(part1_result)
    part2_result = part2(lines, starting_point)
    print(part2_result)


def part1(grid, starting_point):
    stack = []
    seen = set()
    stack.append(starting_point)

    while len(stack) != 0:
        x, y, direction = stack.pop(0)

        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            print("stop")
            break

        seen.add((x, y))
        if direction % 4 == 0:
            if y - 1 < 0:
                print("stop")
                break

            if grid[y - 1][x] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("up")
                stack.append((x, y - 1, 0))
        elif direction % 4 == 1:
            if x + 1 >= len(grid[0]):
                print("stop")
                break

            if grid[y][x + 1] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("right")
                stack.append((x + 1, y, 1))
        elif direction % 4 == 2:
            if y + 1 >= len(grid):
                print("stop")
                break

            if grid[y + 1][x] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("down")
                stack.append((x, y + 1, 2))
        elif direction % 4 == 3:
            if x - 1 < 0:
                print("stop")
                break

            if grid[y][x - 1] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("left")
                stack.append((x - 1, y, 3))

        # print(x, y, direction)
    print(seen)

    return len(seen)


def part2(grid, starting_point):
    def is_loop(start_x, start_y, start_direction):
        # print(start_x, start_y, start_direction)
        start_direction = start_direction % 4

        seen = set()
        seen.add((start_x, start_y, start_direction))

        next_cell = None

        if start_direction == 0:
            # print("jag gick upp")
            next_cell = (start_x, start_y - 1)
        elif start_direction == 1:
            # print("jag gick höger")
            next_cell = (start_x + 1, start_y)
        elif start_direction == 2:
            # print("jag gick neråt")
            next_cell = (start_x, start_y + 1)
        elif start_direction == 3:
            # print("jag gick vänster")
            next_cell = (start_x - 1, start_y)

        if (
            next_cell[0] == -1
            or next_cell[0] == len(grid[0])
            or next_cell[1] == -1
            or next_cell[1] == len(grid)
        ):
            return False
        if grid[next_cell[1]][next_cell[0]] == "#":
            return False

        x, y, direction = start_x, start_y, start_direction

        while True:
            if y == 0 or x == 0 or y + 1 == len(grid) or x + 1 == len(grid[0]):
                return False

            direction = (direction + 1) % 4
            seen.add((x, y, direction))
            if direction == 0:
                while y > 0 and grid[y - 1][x] != "#":
                    y -= 1
                    if (x, y, direction) in seen:

                        return True
                    seen.add((x, y, direction))
            elif direction == 1:
                while x < len(grid[0]) - 1 and grid[y][x + 1] != "#":
                    x += 1
                    if (x, y, direction) in seen:
                        return True
                    seen.add((x, y, direction))
            elif direction == 2:
                while y < len(grid) - 1 and grid[y + 1][x] != "#":
                    y += 1
                    if (x, y, direction) in seen:
                        return True
                    seen.add((x, y, direction))
            elif direction == 3:
                while x > 0 and grid[y][x - 1] != "#":
                    x -= 1
                    if (x, y, direction) in seen:
                        return True
                    seen.add((x, y, direction))

        # print(seen)

        # print(x, y, direction)

    def walk(path, grid, starting_point):
        stack = []
        # seen = set()
        stack.append(starting_point)

        while len(stack) != 0:
            x, y, direction = stack.pop(0)

            if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                # print("inne")
                break

            # print(x, y, direction % 4)

            # print(x, y, direction % 4)
            if (x, y, direction % 4) in path:
                # print("inne som fan")
                return True

            path.add((x, y, direction % 4))
            if direction % 4 == 0:  # UP
                # print("up", x, y)
                if y - 1 >= 0 and grid[y - 1][x] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x, y - 1, 0))
            elif direction % 4 == 1:  # RIGHT
                # print("right", x, y)
                if x + 1 < len(grid[0]) and grid[y][x + 1] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x + 1, y, 1))
            elif direction % 4 == 2:  # DOWN
                # print("down", x, y)
                if y + 1 < len(grid) and grid[y + 1][x] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x, y + 1, 2))
            elif direction % 4 == 3:
                # print("left", x, y)
                if x - 1 >= 0 and grid[y][x - 1] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x - 1, y, 3))

            # print(x, y, direction)

        return False

    path = set()
    walk(path, grid, starting_point)

    path = list(path)

    # print(path)

    result = set()
    for x, y, direction in path:

        if direction == 0:
            next_cell = (x, y - 1)
        elif direction == 1:
            next_cell = (x + 1, y)
        elif direction == 2:
            next_cell = (x, y + 1)
        elif direction == 3:
            next_cell = (x - 1, y)

        if (
            next_cell[0] == -1
            or next_cell[0] == len(grid[0])
            or next_cell[1] == -1
            or next_cell[1] == len(grid)
        ):
            continue
        if grid[next_cell[1]][next_cell[0]] == "#":
            continue

        grid_copy = [line[::] for line in grid]
        grid_copy[next_cell[1]][next_cell[0]] = "#"

        if walk(set(), grid_copy, starting_point):
            result.add((next_cell[0], next_cell[1]))

    # print(result)

    return len(result)
