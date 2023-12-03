import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = [line.strip() for line in file.readlines()]
    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(lines):
    res = 0
    for y, line in enumerate(lines):
        current_number = ""
        is_adjacent = False
        for x, char in enumerate(line):
            if char.isdigit():
                current_number += char

                for adjacent_x in range(x - 1, x + 2):
                    for adjacent_y in range(y - 1, y + 2):
                        if (
                            adjacent_y < 0
                            or adjacent_y > len(lines) - 1
                            or adjacent_x < 0
                            or adjacent_x > len(lines[0]) - 1
                        ):
                            continue

                        current_cell = lines[adjacent_y][adjacent_x]
                        if not current_cell.isdigit() and current_cell != ".":
                            is_adjacent = True

            else:
                if is_adjacent:
                    res += int(current_number)
                is_adjacent = False
                current_number = ""
        if is_adjacent:
            res += int(current_number)

    return res


def part2(lines):
    res = 0
    engines = dict()
    for y, line in enumerate(lines):
        current_number = ""
        is_engine_found = False
        engine_key = ""
        for x, char in enumerate(line):
            if char.isdigit():
                current_number += char

                for adjacent_x in range(x - 1, x + 2):
                    for adjacent_y in range(y - 1, y + 2):
                        if (
                            adjacent_y < 0
                            or adjacent_y > len(lines) - 1
                            or adjacent_x < 0
                            or adjacent_x > len(lines[0]) - 1
                        ):
                            continue

                        current_cell = lines[adjacent_y][adjacent_x]

                        if current_cell == "*":
                            engine_key = (adjacent_x, adjacent_y)
                            if engine_key not in engines:
                                engines[engine_key] = []
                            is_engine_found = True

            else:
                if is_engine_found:
                    engines[engine_key].append(int(current_number))
                is_engine_found = False
                current_number = ""
        if is_engine_found:
            engines[engine_key].append(int(current_number))

    for key in engines.keys():
        if len(engines[key]) == 2:
            res += engines[key][0] * engines[key][1]

    return res


if __name__ == "__main__":
    main()
