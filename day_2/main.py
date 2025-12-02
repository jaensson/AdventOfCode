import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)[0].split(",")

    result = part1(lines)
    print(result)

    result = part2(lines)
    print(result)


def part1(lines):
    result = 0
    for line in lines:
        start, stop = [int(val) for val in line.split("-")]

        for i in range(start, stop + 1):
            current = str(i)
            mid = len(current) // 2
            if current[:mid] == current[mid:]:
                result += i

    return result


def part2(lines):
    result = 0
    for line in lines:
        start, stop = [int(val) for val in line.split("-")]

        for i in range(start, stop + 1):
            current = str(i)

            for p in [2, 3, 5, 7, 11]:
                if helper(current, p):
                    result += i
                    break

    return result


def helper(number, parts=2):
    if len(number) / parts != len(number) // parts:
        return False

    size_of_partition = len(number) // parts

    partitions = [
        number[i * size_of_partition : (i + 1) * size_of_partition]
        for i in range(parts)
    ]

    first = partitions[0]
    for i in range(1, len(partitions)):
        if first != partitions[i]:
            return False
    return True
