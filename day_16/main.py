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
            current = stack.pop()
            pos, direction, score = current
            # print(current)

            key = (pos, direction)
            if (
                key in nodes and nodes[key] < score
            ):  # Already been to this node with a better score
                continue

            nodes[key] = score

            x, y = pos

            # This is the problem => might just spin around and adding alot of possible outcomes but in reality there are just 3
            stack.append(((x, y), (direction + 1) % 4, score + 1000))
            stack.append(((x, y), (direction - 1) % 4, score + 1000))

            if direction == 0 and grid[y - 1][x] != "#":  # NORTH
                stack.append(((x, y - 1), direction, score + 1))
            if direction == 1 and grid[y][x + 1] != "#":  # EAST
                stack.append(((x + 1, y), direction, score + 1))
            if direction == 2 and grid[y + 1][x] != "#":  # SOUTH
                stack.append(((x, y + 1), direction, score + 1))
            if direction == 3 and grid[y][x - 1] != "#":  # WEST
                stack.append(((x - 1, y), direction, score + 1))

        return min(nodes[(ending_position, 0)], nodes[(ending_position, 1)])

    return walk(grid, ending_position, starting_position)


def part2(lines):
    pass
