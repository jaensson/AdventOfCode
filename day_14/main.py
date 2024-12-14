import os
from lib.helpers import read_file
import time as t


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [parse_robot(line) for line in lines]

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def parse_robot(line):
    robot = dict()

    test = line.split(" ")
    point = test[0].split("=")[-1]
    velocity = test[1].split("=")[-1]
    robot["point"] = {
        "x": int(point.split(",")[0]),
        "y": int(point.split(",")[1]),
    }
    robot["vel"] = {
        "x": int(velocity.split(",")[0]),
        "y": int(velocity.split(",")[1]),
    }

    return robot


def part1(robots):
    time = 100
    positions = []
    width = 101
    height = 103

    for robot in robots:
        x = ((robot["vel"]["x"] * time) + robot["point"]["x"]) % width
        y = ((robot["vel"]["y"] * time) + robot["point"]["y"]) % height
        positions.append((x, y))

    vertical = height // 2
    horizontal = width // 2
    quadrants = [0, 0, 0, 0]  # Top-Left, Top-Right, Bottom-Left, Bottom-Right
    for x, y in positions:
        if x == horizontal or y == vertical:
            continue

        if x < horizontal:
            if y < vertical:
                quadrants[0] += 1
            if y > vertical:
                quadrants[2] += 1
        if x > horizontal:
            if y < vertical:
                quadrants[1] += 1
            if y > vertical:
                quadrants[3] += 1

    factor = 1
    for quadrant in quadrants:
        factor *= quadrant

    print(quadrants)

    return factor


def part2(robots):
    time = 0
    width = 101
    height = 103

    while True:
        positions = set()
        for robot in robots:
            x = ((robot["vel"]["x"] * time) + robot["point"]["x"]) % width
            y = ((robot["vel"]["y"] * time) + robot["point"]["y"]) % height
            positions.add((x, y))

        valid = False

        for position in positions:
            x, y = position

            if (
                (x - 1, y + 1) in positions
                and (x, y + 1) in positions
                and (x + 1, y + 1) in positions
                and (x - 2, y + 2) in positions
                and (x - 1, y + 2) in positions
                and (x, y + 2) in positions
                and (x + 1, y + 2) in positions
                and (x + 2, y + 2) in positions
            ):
                valid = True
                break
        if valid:
            break
        time += 1

    return time
