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

    part1_result = part1(lines)
    print(part1_result)
    start = time.time()
    # part2_result = part2(lines)
    # print(part2_result)
    end = time.time()
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
    """

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
            # print("börjar med", current_string)

            if len(current_string) == len(start) and valid_combination(
                current_string, arrangement
            ):
                # print(current_string)
                valid += 1
                # valid_combination(current_string, arrangement)
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
                # print(f"left: {left}", end=" ")

            offset = sum(arrangements[current_arrangement:])
            if len(arrangements[current_arrangement:]) > 1:
                offset += round(len(arrangements[current_arrangement:]) / 2)

            # print(
            #     offset,
            #     len(start)
            #     - len(current_string)
            #     - [*start[len(current_string) :]].count("."),
            # )

            if (
                len(current_string) < len(start)
                and start[len(current_string)] != "#"
                and offset < len(start) - len(current_string)
            ):
                right = current_string + "."
                queue.append((right, current_arrangement))
                # print(f"right: {right}", end=" ")

            # print()

        return valid

    # start = "??????"
    # arrangements = [1, 2]
    # start = "??????#?#?#??"
    # arrangements = [2, 2, 6]

    # result = get_valid_combinations(start, arrangements)
    # print(result)

    # print(lines)
    # combinations = []
    total = 0
    for start, arrangement in lines:
        # print(start, arrangement)
        # combinations.append(get_valid_combinations(start, arrangement))
        # start = "?".join([start for _ in range(5)])
        # arrangement *= 5
        # print(test, test2)

        first = get_valid_combinations(start, arrangement)
        second = get_valid_combinations(start + "?", arrangement)
        third = get_valid_combinations("?" + start, arrangement)
        fourth = get_valid_combinations("?" + start + "?", arrangement)

        # total = first * testing**4

        # print(testing, total)

        # print(first, testing, total)

        print(first, second, third, fourth)
        # print(first, test, total)

        # print(first, second)

        # total += get_valid_combinations(start, arrangement)
        # print(combinations)

    return total

    # 34144603979562 för lågt
    # 56776584635449 för lågt

    # 252446150283850 för hög

    # start = [*start]
    # for arrange_ix, arrangement in enumerate(arrangements):
    #     print(len(start) - arrangement + 1)
    #     left_offset = sum(arrangements[:arrange_ix]) + len(
    #         arrangements[:arrange_ix]
    #     )
    #     right_offset = sum(arrangements[arrange_ix + 1 :]) + len(
    #         arrangements[arrange_ix + 1 :]
    #     )
    #     for i in range(
    #         left_offset, len(start) - arrangement + 1 - right_offset
    #     ):
    #         if "." in start[i : i + arrangement]:
    #             continue
    #         test = start[::]
    #         print(i, i + arrangement - 1)
    #         for j in range(arrangement):
    #             test[i + j] = "#"
    #         test = "".join(test)
    #         print(test)


if __name__ == "__main__":
    main()


""" Testing

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
