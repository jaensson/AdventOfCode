import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    machines = parse_input(lines)

    result = part1(machines)
    print(result)

    result = part2(machines)
    print(result)


def parse_input(lines):
    def parse_integer_list(input):
        return [int(elem) for elem in input.split(",")]

    machines = []
    for line in lines:
        machine = dict()
        instructions = line.split(" ")
        machine["indicator"] = instructions[0].lstrip("[").rstrip("]")
        machine["buttons"] = [
            parse_integer_list(button.lstrip("(").rstrip(")"))
            for button in instructions[1:-1]
        ]
        machine["joltage"] = parse_integer_list(
            instructions[-1].lstrip("{").rstrip("}")
        )
        machines.append(machine)

    return machines


def part1(machines):
    number_of_presses = 0

    for machine in machines:
        indicator = machine["indicator"]

        goal = ""
        for i in range(len(indicator)):
            goal = ("1" if indicator[i] == "#" else "0") + goal
        goal = int("0b" + goal, base=2)

        queue = [(0b0, 0)]
        seen = set()
        while len(queue) != 0:
            current, clicks = queue.pop(0)

            if current == goal:
                number_of_presses += clicks
                break

            if current in seen:
                continue

            seen.add(current)

            for button in machine["buttons"]:
                copy = current
                for light in button:
                    copy ^= 1 << light
                queue.append((copy, clicks + 1))

    return number_of_presses

