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
    result = 0

    for line in lines:
        left = 0
        right = len(line) - 1

        while not line[left].isdigit() or not line[right].isdigit():
            if not line[left].isdigit():
                left += 1
            if not line[right].isdigit():
                right -= 1

        result += int(line[left] + line[right])

    return result


def part2(lines):
    STRING_DIGITS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    KEYS = STRING_DIGITS.keys()

    result = 0

    for line in lines:
        line_numbers = []
        for i, char in enumerate(line):
            if char.isdigit():
                line_numbers.append(char)
            else:
                for key in KEYS:
                    key_length = i + len(key)
                    substring = line[i:key_length]
                    if substring == key:
                        line_numbers.append(STRING_DIGITS[key])
                        i += len(key)
                        break
        result += int(f"{line_numbers[0]}{line_numbers[-1]}")

    return result


if __name__ == "__main__":
    main()
