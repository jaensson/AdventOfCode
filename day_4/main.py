import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    result = part1(lines)
    print(result)

    result = part2(lines)
    print(result)


def part1(grid):
    result = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@" and len(count_paper_neighbours(grid, (x, y))) < 4:
                result += 1

    return result


def part2(grid):
    def get_rolls_to_remove(state, count):
        rolls = []
        for pos in state:
            if len(state[pos]) < count:
                rolls.append(pos)
        return rolls

    state = dict()
    result = 0

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                state[(x, y)] = count_paper_neighbours(grid, (x, y))

    rolls_to_remove = get_rolls_to_remove(state, 4)
    while len(rolls_to_remove) != 0:
        result += len(rolls_to_remove)
        for roll in rolls_to_remove:
            for neighbour in state[roll]:
                state[neighbour].remove(roll)
            del state[roll]
        rolls_to_remove = get_rolls_to_remove(state, 4)

    return result


def count_paper_neighbours(grid, position):
    neighbours = set()
    pos_x, pos_y = position
    for y in range(pos_y - 1, pos_y + 2):
        for x in range(pos_x - 1, pos_x + 2):
            if (x, y) == position:
                continue
            if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                continue

            if grid[y][x] == "@":
                neighbours.add((x, y))

    return neighbours
