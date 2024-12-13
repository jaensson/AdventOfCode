import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [parse_machine(lines[i : i + 3]) for i in range(0, len(lines), 4)]

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def parse_machine(machine):
    def parse_button(parsed_machine, button):
        button = button.split(",")

        X = int(button[0].strip().split(":")[-1].split("+")[-1])
        Y = int(button[-1].strip().split("+")[-1])

        name = button[0].strip().split(":")[0].split(" ")[-1]

        parsed_machine[name] = {"x": X, "y": Y}

    def parse_prize(parsed_machine, prize):
        prize = prize.split(",")

        Y = int(prize[-1].strip().split("=")[-1])
        X = int(prize[0].strip().split(":")[-1].strip().split("=")[-1])

        parsed_machine["prize"] = {"x": X, "y": Y}

    parsed_machine = dict()

    parse_button(parsed_machine, machine[0])
    parse_button(parsed_machine, machine[1])
    parse_prize(parsed_machine, machine[2])

    return parsed_machine


def part1(machines):
    def calculate(machine):
        A = machine["A"]["x"]
        B = machine["B"]["x"]
        C = machine["A"]["y"]
        D = machine["B"]["y"]

        x1 = machine["prize"]["x"]
        x2 = machine["prize"]["y"]

        c1 = (A * x2 - C * x1) / (A * D - C * B)
        c2 = (x2 - D * c1) / C

        if c1 // 1 != c1 or c2 // 1 != c2 or c1 > 100 or c2 > 100:
            return 0

        return int(c2 * 3 + c1 * 1)

    result = 0
    for machine in machines:
        result += calculate(machine)

    return result


def part2(machines):
    def calculate(machine):
        A = machine["A"]["x"]
        B = machine["B"]["x"]
        C = machine["A"]["y"]
        D = machine["B"]["y"]

        x1 = machine["prize"]["x"] + 10000000000000
        x2 = machine["prize"]["y"] + 10000000000000

        c1 = (A * x2 - C * x1) / (A * D - C * B)
        c2 = (x2 - D * c1) / C

        if c1 // 1 != c1 or c2 // 1 != c2 or c1 < 100 or c2 < 100:
            return 0

        return int(c2 * 3 + c1 * 1)

    result = 0
    for machine in machines:
        result += calculate(machine)

    return result
