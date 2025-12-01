import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    result = part1(lines)
    print(result)

    result = part2(lines)
    print(result)


def part1(lines):
    max_number_of_dials = 100
    current_dial = 50

    counter = 0

    for line in lines:
        rotation, times = line[0], int(line[1:])
        if rotation == "L":
            current_dial = (current_dial - times) % max_number_of_dials
        else:
            current_dial = (current_dial + times) % max_number_of_dials

        if current_dial == 0:
            counter += 1

    return counter


def part2(lines):
    max_number_of_dials = 100
    current_dial = 50

    counter = 0

    for line in lines:
        rotation, times = line[0], int(line[1:])

        counter += times // max_number_of_dials

        times = times % max_number_of_dials

        if rotation == "L":
            if current_dial - times <= 0 and current_dial != 0:
                counter += 1
            current_dial = (current_dial - times) % max_number_of_dials
        else:
            if current_dial + times >= max_number_of_dials:
                counter += 1
            current_dial = (current_dial + times) % max_number_of_dials

    return counter
