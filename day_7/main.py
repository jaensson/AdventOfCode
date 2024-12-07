import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [line.split(": ") for line in lines]

    lines = [
        [int(line[0]), [int(val) for val in line[1].split(" ")]]
        for line in lines
    ]

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(lines):
    def calculate(res, current_result, numbers, current_number):
        if current_result == res and current_number == len(numbers):
            return True

        if current_number == len(numbers):
            return False

        return calculate(
            res,
            current_result + numbers[current_number],
            numbers,
            current_number + 1,
        ) or calculate(
            res,
            current_result * numbers[current_number],
            numbers,
            current_number + 1,
        )

    result = 0
    for line in lines:
        res = line[0]
        numbers = line[1]

        if calculate(res, numbers[0], numbers, 1):
            result += res

    return result


def part2(lines):
    def calculate(res, current_result, numbers, current_number):
        if current_result == res and current_number == len(numbers):
            return True

        if current_number == len(numbers):
            return False

        if current_number > res:
            return False

        return (
            calculate(
                res,
                current_result + numbers[current_number],
                numbers,
                current_number + 1,
            )
            or calculate(
                res,
                current_result * numbers[current_number],
                numbers,
                current_number + 1,
            )
            or calculate(
                res,
                int(str(current_result) + str(numbers[current_number])),
                numbers,
                current_number + 1,
            )
        )

    result = 0
    for line in lines:
        res = line[0]
        numbers = line[1]

        if calculate(res, numbers[0], numbers, 1):
            result += res

    return result
