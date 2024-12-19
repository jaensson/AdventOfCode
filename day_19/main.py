import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    towels = None
    onsens = None

    for i, line in enumerate(lines):
        if line == "":
            towels = lines[:i][0].split(", ")
            onsens = lines[i + 1 :]
            break

    part1_result = part1(towels, onsens)
    print(part1_result)
    part2_result = part2(towels, onsens)
    print(part2_result)


def part1(towels, onsens):
    def is_working_design(towels, design, index):
        if index >= len(design):
            return True

        for towel in towels:
            if design[
                index : index + len(towel)
            ] == towel and is_working_design(
                towels, design, index + len(towel)
            ):
                return True

        return False

    result = 0
    for onsen in onsens:
        test = is_working_design(towels, onsen, 0)
        if test:
            result += 1

    return result


def part2(towels, onsens):
    def is_working_design(dp, towels, design, index):
        key = design[index:]

        if key in dp:
            return dp[key]

        if index >= len(design):
            return 1

        result = 0
        for towel in towels:
            if design[index : index + len(towel)] == towel:
                result += is_working_design(
                    dp, towels, design, index + len(towel)
                )

        dp[key] = result

        return result

    dp = dict()
    result = 0
    for onsen in onsens:
        result += is_working_design(dp, towels, onsen, 0)

    return result
