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
    def is_optimal(matrix):
        for ix, elem in enumerate(matrix[len(matrix) - 1]):
            if elem < 0:
                return False
        return True

    def find_pivot(matrix):
        objective = matrix[len(matrix) - 1]
        current_smallest = 0
        for i in range(1, len(objective) - 1):
            if objective[i] < objective[current_smallest]:
                current_smallest = i
        x = current_smallest

        constraints = [i for i in range(len(matrix) - 1) if matrix[i][x] > 0]
        current_smallest = constraints[0]
        for i in range(1, len(constraints)):
            ratio = matrix[constraints[i]][-1] / matrix[constraints[i]][x]
            if (
                ratio
                < matrix[current_smallest][-1] / matrix[current_smallest][x]
            ):
                current_smallest = i
        y = current_smallest

        return x, y

    def times_row(multiplier, matrix, row):
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

    matrix = [
        [3, 5, 1, 0, 0, 29],
        [2, 1, 0, 1, 0, 10],
        [-2, -3, 0, 0, 1, 0],
    ]

    matrix = [
        [1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 1, 1, 0, 0, 0, 1],
        [-10, -11, -11, -5, -10, -5, 0],
    ]

    matrix = [
        [1, -1, 1, -1, 1, -1, 0, 0, 1, 0, 0, 0, 1],
        [1, -1, 0, 0, 1, -1, 0, 0, 0, 1, 0, 0, 1],
        [1, -1, 1, -1, 0, 0, 1, -1, 0, 0, 1, 0, 1],
        [0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [-10, 10, -11, 11, -5, 5, -5, 5, 0, 0, 0, 0, 0],
    ]

    # matrix = [
    #     [0, 0, 0, 1, 1],
    #     [0, 1, 0, 1, 1],
    #     [0, 0, 1, 0, 1],
    #     [0, 0, 1, 1, 1],
    #     [1, 0, 1, 0, 1],
    #     [1, 1, 0, 0, 1],
    #     [-3, -5, -4, -7, 0],
    # ]
    # while not is_optimal(matrix):
    #     x, y = find_pivot(matrix)
    #     print((x, y))
    #     multiplier = matrix[y][x] ** -1
    #     times_row(multiplier, matrix, y)
    #     for i in range(len(matrix)):
    #         if i != y:
    #             times = -(matrix[i][x]) / matrix[y][x]
    #             add_row(times, matrix, y, i)

    #     for row in matrix:
    #         print(row)

    # maximum_value = matrix[-1][-1]
    # print(maximum_value)

    for machine in machines[:1]:
        print(machine)
        goal = machine["joltage"]

        matrix = []
        for i in range(len(goal)):
            row = []
            for ix, button in enumerate(machine["buttons"]):
                if i in button:
                    row.append(1)
                else:
                    row.append(0)
            row.append(goal[i])
            opposite = [-elem for ix, elem in enumerate(row)]
            matrix.append(row)
            matrix.append(opposite)

        for row in matrix:
            print(row)

        # print(affected_by)

    """
    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

    a + b + c = 10
    a + c + d = 11
    a + c + d = 11
    a + b     = 5
    a + b + c = 10
    c         = 5

    5a + 3b + 3c + 2d = 52
    """

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
