import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [list(line) for line in lines]
    part1_result = part1(lines)
    print(part1_result)


def part1(grid):
    """
    0: north
    1: east
    2: south
    3: west
    """

    def get_starting_position(grid):
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char == "S":
                    return (x, y)

    def get_ending_position(grid):
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char == "E":
                    return (x, y)

    def draw_grid(grid, seen):
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if (x, y) in seen:
                    print("O", end="")
                else:
                    print(char, end="")
            print()

    starting_position = get_starting_position(grid)
    ending_position = get_ending_position(grid)
    # queue = []
    # queue.append((starting_position, 0, 0))  # current, direction, score
    # print(starting_position)

    def walk(grid, ending_position, position):
        seen = set()
        stack = []
        stack.append((position, 1, 0))

        nodes = dict()

        while len(stack) != 0:
            current = stack.pop(0)
            pos, direction, score = current

            key = pos
            if (
                key in nodes and nodes[key] <= score
            ):  # Already been to this node with a better score
                continue

            nodes[key] = score

            x, y = pos

            if direction == 0:  # NORTH
                if grid[y][x - 1] != "#":  # WEST
                    stack.append(((x - 1, y), 3, score + 1001))
                if grid[y][x + 1] != "#":  # EAST
                    stack.append(((x + 1, y), 1, score + 1001))

                if grid[y - 1][x] != "#":
                    stack.append(((x, y - 1), 0, score + 1))
            if direction == 1:  # EAST
                if grid[y - 1][x] != "#":  # NORTH
                    stack.append(((x, y - 1), 0, score + 1001))
                if grid[y + 1][x] != "#":  # SOUTH
                    stack.append(((x, y + 1), 2, score + 1001))

                if grid[y][x + 1] != "#":
                    stack.append(((x + 1, y), 1, score + 1))
            if direction == 2:  # SOUTH
                if grid[y][x + 1] != "#":  # EAST
                    stack.append(((x + 1, y), 1, score + 1001))
                if grid[y][x - 1] != "#":  # WEST
                    stack.append(((x - 1, y), 3, score + 1001))

                if grid[y + 1][x] != "#":
                    stack.append(((x, y + 1), 2, score + 1))
            if direction == 3:  # WEST
                if grid[y + 1][x] != "#":  # SOUTH
                    stack.append(((x, y + 1), 2, score + 1001))
                if grid[y - 1][x] != "#":  # NORTH
                    stack.append(((x, y - 1), 0, score + 1001))

                if grid[y][x - 1] != "#":
                    stack.append(((x - 1, y), 3, score + 1))

        return nodes[ending_position]

    return walk(grid, ending_position, starting_position)


def part2(lines):
    pass
