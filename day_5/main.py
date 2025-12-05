import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    parsed_input = parse_input(lines)

    result = part1(parsed_input)
    print(result)

    result = part2(parsed_input)
    print(result)


def parse_input(lines):
    parsed = {"ranges": set(), "ingredients": list()}

    blank_line = [ix for ix, line in enumerate(lines) if line == ""][0]

    for range in lines[:blank_line]:
        start, end = range.split("-")
        parsed["ranges"].add((int(start), int(end)))

    for ingredient in lines[blank_line + 1 :]:
        parsed["ingredients"].append(int(ingredient))

    return parsed


def part1(input):
    result = 0
    for ingredient in input["ingredients"]:
        for start, end in input["ranges"]:
            if start <= ingredient <= end:
                result += 1
                break

    return result


def part2(input):
    def combine_ranges(ranges):
        sorted_ranges = sorted(ranges, key=lambda range: range[0])

        valid_ranges = []

        current = 0
        while current < len(sorted_ranges):
            start, end = sorted_ranges[current]

            next = current + 1
            while (
                next < len(sorted_ranges)
                and start <= sorted_ranges[next][0] <= end
            ):
                start = min(start, sorted_ranges[next][0])
                end = max(end, sorted_ranges[next][1])
                next += 1

            current = next
            valid_ranges.append((start, end))

        return valid_ranges

    result = 0

    for start, end in combine_ranges(input["ranges"]):
        result += end - start + 1

    return result
