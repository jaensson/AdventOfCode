import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    result = part1(lines)
    print(result)

    result = part2(lines)
    print(result)


def get_positions_of_symbol(grid, symbol):
    positions = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == symbol:
                positions.append((x, y))

    return positions


def splitter_below(position, splitters):
    splitter_below = None
    for splitter in splitters:
        if splitter[0] == position[0] and splitter[1] >= position[1]:
            splitter_below = splitter
            break

    return splitter_below


def part1(grid):
    starting_position = get_positions_of_symbol(grid, "S")[0]
    splitters = get_positions_of_symbol(grid, "^")
    splitting_splitters = [splitter_below(starting_position, splitters)]

    seen = set()
    while len(splitting_splitters) != 0:
        splitter = splitting_splitters.pop()

        if not splitter or splitter in seen:
            continue
        seen.add(splitter)

        x, y = splitter
        splitting_splitters.append(splitter_below((x - 1, y), splitters))
        splitting_splitters.append(splitter_below((x + 1, y), splitters))

    return len(seen)


def part2(grid):
    def timelines(dp, position, splitters):
        if position in dp:
            return dp[position]

        x, y = position
        left = splitter_below((x - 1, y), splitters)
        right = splitter_below((x + 1, y), splitters)

        number_of_timelines = 1 if not left else timelines(dp, left, splitters)
        number_of_timelines += 1 if not right else timelines(dp, right, splitters)

        dp[position] = number_of_timelines
        return dp[position]

    starting_position = get_positions_of_symbol(grid, "S")[0]
    splitters = get_positions_of_symbol(grid, "^")

    dp = dict()
    return timelines(dp, splitter_below(starting_position, splitters), splitters)
