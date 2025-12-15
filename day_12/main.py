import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    input = parse_input(lines)

    result = part1(input)
    print(result)

    result = part2(input)
    print(result)


def parse_input(lines):
    def parse_presents(lines, number_of_presents, lines_per_present):
        presents = dict()
        for i in range(number_of_presents):
            presents[i] = lines[
                i * lines_per_present + 1 : (i + 1) * lines_per_present - 1
            ]
        return presents

    def parse_trees(lines):
        trees = []
        for line in lines:
            tree = dict()
            size, number_of_presents = line.split(": ")
            width, height = size.split("x")
            tree["width"] = int(width)
            tree["height"] = int(height)
            tree["presents"] = [
                int(number_of_present)
                for number_of_present in number_of_presents.split(" ")
            ]
            trees.append(tree)
        return trees

    number_of_presents = 6
    lines_per_present = 5
    transition = number_of_presents * lines_per_present

    input = dict()
    input["shapes"] = parse_presents(
        lines[:transition], number_of_presents, lines_per_present
    )
    input["trees"] = parse_trees(lines[transition:])
    return input


def part1(input):
    pass


def part2(input):
    pass
