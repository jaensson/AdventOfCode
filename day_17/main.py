import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    computer = parse_computer(lines)

    # part1_result = part1(computer)
    # print(part1_result)
    part2_result = part2(computer)
    print(part2_result)


def parse_computer(lines):
    def parse_registration(computer, registration):
        registration = registration.split(":")
        reg_name = registration[0].split(" ")[-1]
        val = int(registration[-1].strip())
        computer[reg_name] = val

    computer = dict()
    registration = ""
    instructions = ""
    for i in range(len(lines)):
        if lines[i] == "":
            registration = ",".join(lines[:i])
            instructions = "".join(lines[i + 1 :])
            break

    registrations = registration.split(",")
    for reg in registrations:
        parse_registration(computer, reg)

    computer["instructions"] = [
        int(val) for val in instructions.split(":")[-1].strip().split(",")
    ]
    return computer


def part1(computer):
    def find_combo_operand(computer, operand):
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return computer["A"]
        if operand == 5:
            return computer["B"]
        if operand == 6:
            return computer["C"]

        # print("error")

    instructions = computer["instructions"]

    instruction_pointer = 0
    output = []

    while instruction_pointer < len(instructions):
        current_instruction = instructions[instruction_pointer]
        operand = instructions[instruction_pointer + 1]
        literal_operand = operand
        combo_operand = find_combo_operand(computer, operand)

        if current_instruction == 0:
            computer["A"] = computer["A"] // (2**combo_operand)
        elif current_instruction == 1:
            computer["B"] = computer["B"] ^ literal_operand
        elif current_instruction == 2:
            computer["B"] = combo_operand % 8
        elif current_instruction == 3:
            if computer["A"] != 0:
                instruction_pointer = literal_operand
                continue
        elif current_instruction == 4:
            computer["B"] = computer["B"] ^ computer["C"]
        elif current_instruction == 5:
            output.append(str(combo_operand % 8))
        elif current_instruction == 6:
            computer["B"] = computer["A"] // (2**combo_operand)
        elif current_instruction == 7:
            computer["C"] = computer["A"] // (2**combo_operand)

        instruction_pointer += 2

    print(output, computer)

    return ",".join(output)


def part2(computer):
    def find_combo_operand(computer, operand):
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return computer["A"]
        if operand == 5:
            return computer["B"]
        if operand == 6:
            return computer["C"]

    instructions = computer["instructions"]

    print(computer)

    """
        out A (mod 8) -> A divided by combo (0, 1, 2, 3, A, B, C)

        11100101011000000

        1. 0
        x = x // 8
        (x + y1) % 8) = 0

        2. 3
        x = x // 8
        (x+y2) % = 0
    """

    # for i in range(120000):

    dp = set()
    for i in range(120000):
        computer_copy = {
            "A": computer["A"],
            "B": computer["B"],
            "C": computer["C"],
        }
        computer_copy["A"] = computer["A"] + i

        instruction_pointer = 0
        output = []
        same = True
        while instruction_pointer < len(instructions):
            key = (
                computer_copy["A"],
                computer_copy["B"],
                computer_copy["C"],
                instruction_pointer,
                "".join(output),
            )
            if key in dp:
                print("inne")
                break

            dp.add(key)

            current_instruction = instructions[instruction_pointer]
            operand = instructions[instruction_pointer + 1]
            literal_operand = operand
            combo_operand = find_combo_operand(computer_copy, operand)

            if current_instruction == 0:
                computer_copy["A"] = computer_copy["A"] // (2**combo_operand)
            elif current_instruction == 1:
                computer_copy["B"] = computer_copy["B"] ^ literal_operand
            elif current_instruction == 2:
                computer_copy["B"] = combo_operand % 8
            elif current_instruction == 3:
                if computer_copy["A"] != 0:
                    instruction_pointer = literal_operand
                    continue
            elif current_instruction == 4:
                computer_copy["B"] = computer_copy["B"] ^ computer_copy["C"]
            elif current_instruction == 5:
                val = combo_operand % 8
                if val != instructions[len(output)]:
                    same = False
                    break
                output.append(str(val))
            elif current_instruction == 6:
                computer_copy["B"] = computer_copy["A"] // (2**combo_operand)
            elif current_instruction == 7:
                computer_copy["C"] = computer_copy["A"] // (2**combo_operand)

            instruction_pointer += 2

        if same:
            print(computer["A"] + i, "same")
            break

    print(computer_copy, computer)

    return ",".join(output)
