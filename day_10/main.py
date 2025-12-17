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


def part2(machines):
    """
    linear programming:
        - simplex algorithm


    simplex algorithm ~
    """

    def times_row(multiplier, matrix, row):
        print(multiplier, matrix, row)

        for ix, elem in enumerate(matrix[row]):
            matrix[row][ix] = elem * multiplier

    def add_row(multiplier, matrix, row_from, row_to):
        for ix, elem in enumerate(matrix[row_to]):
            matrix[row_to][ix] = elem + matrix[row_from][ix] * multiplier

    matrix = [
        [1, 3, 2, 1, 0, 0, 10],
        [1, 5, 1, 0, 1, 0, 8],
        [-8, -10, -7, 0, 0, 1, 0],
    ]

    times_row(1 / 5, matrix, 1)
    add_row(-3, matrix, 1, 0)
    add_row(10, matrix, 1, 2)

    for row in matrix:
        print(row)

    # def get_permutations(limits, buttons, target_value, current_index=0):
    #     if current_index >= len(buttons):
    #         return []
    #     print(limits, buttons, target_value, current_index)

    #     permutations = []
    #     for i in range(limits[buttons[current_index]]):
    #         if i == target_value:
    #             permutations.append(i)
    #         for t in get_permutations(
    #             limits, buttons, target_value - i, current_index + 1
    #         ):
    #             print(t)

    #     return permutations

    # print("part 2 \n\n")
    # for machine in machines[:1]:
    #     goal = machine["joltage"]

    #     limits = []
    #     for button in machine["buttons"]:
    #         limit = min([goal[light] for light in button])
    #         limits.append(limit)

    #     affected_by = []
    #     for i in range(len(goal)):
    #         row = []
    #         for ix, button in enumerate(machine["buttons"]):
    #             if i in button:
    #                 row.append(ix)
    #         affected_by.append(row)

    #     # test = [-1 for i in range(len(goal))]
    #     # print(test)

    #     # for ix, row in enumerate(affected_by):
    #     print(
    #         f"permutations for row: {0}, {get_permutations(limits, affected_by[0], 10)}"
    #     )

    #     # print(affected_by)
    #     # print(limits)

    #     # print()
