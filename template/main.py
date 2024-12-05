import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    for line in lines:
        print(line)


def part1(lines):
    pass


def part2(lines):
    pass
