import os
from lib.helpers import read_file
from typing import List


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    print(part1(lines))
    print(part2(lines))


def part1(lines: List[str]) -> int:
    distance = 0

    left_side = []
    right_side = []

    for line in lines:
        test = line.split(" ")
        left, right = int(test[0]), int(test[-1])

        left_side.append(left)
        right_side.append(right)

    left_side.sort()
    right_side.sort()

    for i in range(len(left_side)):
        distance += abs(int(right_side[i]) - int(left_side[i]))

    return distance


def part2(lines: List[str]):
    def get_occurences(values: List[int]) -> dict:
        occurences = dict()
        for value in values:
            if value in occurences:
                occurences[value] += 1
            else:
                occurences[value] = 1

        return occurences

    left_side = []
    right_side = []

    for line in lines:
        test = line.split(" ")
        left, right = int(test[0]), int(test[-1])

        left_side.append(left)
        right_side.append(right)

    right_occurences = get_occurences(right_side)

    score = 0
    for left in left_side:
        if left in right_occurences:
            score += left * right_occurences[left]

    return score
