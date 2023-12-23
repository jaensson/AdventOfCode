import os
from typing import List
from enum import Enum


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

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def decode_input(lines):
    rules_input = lines[0].split("\n")
    parts_input = lines[1].split("\n")

    rules = dict()
    parts = []

    for rule in rules_input:
        rule = rule.replace("}", "")
        name = rule.split("{")[0]
        workflows = rule.split("{")[1].split(",")

        workflows = [
            (
                workflow[0],
                workflow[1],
                int(workflow.split(":")[0][2:]),
                workflow.split(":")[1],
            )
            for workflow in workflows[:-1]
        ]
        workflows.append((rule.split("{")[1].split(",")[-1]))

        rules[name] = workflows

    for part in parts_input:
        part = part.replace("{", "").replace("}", "")
        values = part.split(",")
        values = {value[0]: int(value[2:]) for value in values}
        parts.append((values, "in"))

    return rules, parts


def part1(lines):
    rules, parts = decode_input(lines)

    for i, part in enumerate(parts):
        values, destination = part[0], part[1]
        while destination != "A" and destination != "R":
            for rule in rules[destination]:
                if type(rule) is not tuple:
                    destination = rule
                    break

                name, operation, value, dest = rule

                if operation == ">" and values[name] > value:
                    destination = dest
                    break

                if operation == "<" and values[name] < value:
                    destination = dest
                    break

        parts[i] = (values, destination)

    total = 0
    for part, destination in parts:
        if destination == "A":
            total += sum(part.values())

    return total


def part2(lines):
    pass


if __name__ == "__main__":
    main()
