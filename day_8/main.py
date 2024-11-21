import os
from typing import List
from enum import Enum
import math


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n\n")

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = decode_input(lines)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def decode_input(lines):
    network = dict({"instruction": [*lines[0]]})
    nodes = lines[1].split("\n")

    for node in nodes:
        labels = node.split(" = ")
        network[labels[0]] = (
            labels[1].replace("(", "").replace(")", "").split(", ")
        )

    return network


def part1(lines):
    instructions = lines["instruction"]
    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        directions = lines[current_node]
        left = directions[0]
        right = directions[1]
        if instructions[steps % len(instructions)] == "R":
            current_node = right
        else:
            current_node = left

        steps += 1

    return steps


def part2(lines):
    instructions = lines["instruction"]
    current_nodes = [
        node[0] for node in lines.items() if node[0].endswith("A")
    ]
    steps = []

    for node in current_nodes:
        current_node = node
        current_steps = 0
        while not current_node.endswith("Z"):
            directions = lines[current_node]
            left = directions[0]
            right = directions[1]

            if instructions[current_steps % len(instructions)] == "R":
                current_node = right
            else:
                current_node = left

            current_steps += 1

        steps.append(current_steps)

    lcm = 1
    for step in steps:
        lcm = lcm * step // math.gcd(lcm, step)

    return lcm


if __name__ == "__main__":
    main()
