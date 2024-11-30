import os
from typing import List
from enum import Enum
import time


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n")
    lines = [
        (line.split(" ")[0], list(map(int, line.split(" ")[1].split(","))))
        for line in lines
    ]

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    start = time.time()
    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    end = time.time()
    print(part2_result)
    print(end - start)


def part1(lines):
    def valid_combination(combination, arrangement):
        import re

        elems = re.split(r"[.]", combination)
        elems = "".join([str(len(elem)) for elem in elems if elem != ""])

        return elems == arrangement

    def get_valid_combinations(start: str, arrangements: List[int]):
        valid = 0
        queue = [("", 0)]

        arrangement = "".join(map(str, arrangements))

        while len(queue) != 0:
            current_string, current_arrangement = queue.pop(0)

            if len(current_string) == len(start) and valid_combination(
                current_string, arrangement
            ):
                valid += 1
                continue

            if (
                current_arrangement < len(arrangements)
                and "."
                not in start[
                    len(current_string) : len(current_string)
                    + arrangements[current_arrangement]
                ]
                and (
                    len(current_string) + arrangements[current_arrangement]
                    >= len(start)
                    or start[
                        len(current_string) + arrangements[current_arrangement]
                    ]
                    != "#"
                )
            ):
                left = current_string + "#" * arrangements[current_arrangement]
                if len(left) < len(start):
                    left += "."

                queue.append((left, current_arrangement + 1))

            offset = sum(arrangements[current_arrangement:])
            if len(arrangements[current_arrangement:]) > 1:
                offset += round(len(arrangements[current_arrangement:]) / 2)

            if (
                len(current_string) < len(start)
                and start[len(current_string)] != "#"
                and offset < len(start) - len(current_string)
            ):
                right = current_string + "."
                queue.append((right, current_arrangement))

        return valid

    total = 0
    for start, arrangement in lines:
        total += get_valid_combinations(start, arrangement)

    return total


def part2(lines):
    """
    Förbättra genom att inte forstätta om den redan inte fungerar.
    Prova beräkna antal olika kombinationer istället. (Pascals triangel)
    Komplementtet

    Träddiagram
    Varje position är eller inte. Går det sätt ut alla tillhörande samt en seperator.

    Höger är som vänster men en prick framför
    """

    def valid_combination(combination, arrangement):
        import re

        elems = re.split(r"[.]", combination)
        elems = "".join([str(len(elem)) for elem in elems if elem != ""])

        print(combination)

        return elems == "".join(map(str, arrangement))

    def get_valid_combinations(
        spring: str,
        arrangement: List[int],
        current_spring: str = "",
        current_arrangement: int = 0,
        dp: dict = dict(),
    ):
        if len(spring) == len(current_spring) and valid_combination(
            current_spring, arrangement
        ):
            dp["valid"] += 1

        # print(spring, arrangement, current_spring, current_arrangement)

        print(current_arrangement, len(current_spring))

        if (
            current_arrangement < len(arrangement)
            and "."
            not in spring[
                len(current_spring) : len(current_spring)
                + arrangement[current_arrangement]
            ]
            and (
                len(current_spring) + arrangement[current_arrangement]
                >= len(spring)
                or spring[
                    len(current_spring) + arrangement[current_arrangement]
                ]
                != "#"
            )
        ):
            # print("skulle kunna lägga till en rackare")
            # dp["ofan"] = "fungerar"

            left = current_spring + "#" * arrangement[current_arrangement]
            if len(left) < len(spring):
                left += "."
            # print(left)
            get_valid_combinations(
                spring, arrangement, left, current_arrangement + 1, dp
            )

        offset = sum(arrangement[current_arrangement:])
        if len(arrangement[current_arrangement:]) > 1:
            offset += round(len(arrangement[current_arrangement:]) / 2)

        if (
            len(current_spring) < len(spring)
            and spring[len(current_spring)] != "#"
            and offset < len(spring) - len(current_spring)
        ):
            right = current_spring + "."
            get_valid_combinations(
                spring, arrangement, right, current_arrangement, dp
            )
            # print("skulle kunna lägga till en prick")

    springs = "?#?.??."
    arrangement = [2, 1]
    test_dict = {"valid": 0}

    total = get_valid_combinations(springs, arrangement, dp=test_dict)
    print(total, test_dict)

    # for springs, arrangement in lines:
    # get_valid_combinations(springs, arrangement)

    pass


if __name__ == "__main__":
    main()


""" Testing

# 34144603979562 för lågt
# 56776584635449 för lågt

# 252446150283850 för hög

n * (n + 1) * (n + 2) / 6
n * (n + 1) / 2
    
?###???????? 3,2,1

###.##.#....
###.##..#...
###.##...#..
###.##....#.
###.##.....#
###..##.#...
###..##..#..
###..##...#.
###..##....#
###...##.#..
###...##..#.
###...##...#
###....##.#.
###....##..#
###.....##.#
(5 * 6) / 2 = 15

.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#
(4 * 5) / 2 = 10

..###.##.#..
..###.##..#.
..###.##...#
..###..##.#.
..###..##..#
..###...##.#
(3 * 4) / 2 = 6

...###.##.#.
...###.##..#
...###..##.#
(2 * 3) / 2 = 3

....###.##.#
(1 * 2) / 2 = 1


"""

""" skit fråån tidigare
for line in lines[:1]:
    springs = line.split(" ")
    group = springs[1]

    conditions = []
    current_group = ""
    for i in range(len(springs[0])):
        char = springs[0][i]
        next = springs[0][i + 1] if i + 1 < len(springs[0]) else ""

        current_group += char

        if char != next:
            conditions.append(
                current_group if current_group != "" else char
            )
            current_group = ""

    print(conditions, group)
"""
