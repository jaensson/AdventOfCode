import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    computer = parse_computer(lines)

    part1_result = part1(computer)
    print(part1_result)
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

    def create_computer_copy(computer):
        return {
            "A": computer["A"],
            "B": computer["B"],
            "C": computer["C"],
            "instructions": computer["instructions"],
        }

    def get_output(computer):
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
                val = combo_operand % 8
                output.append(val)
                # print(output)
            elif current_instruction == 6:
                computer["B"] = computer["A"] // (2**combo_operand)
            elif current_instruction == 7:
                computer["C"] = computer["A"] // (2**combo_operand)

            instruction_pointer += 2

        return output

    instructions = computer["instructions"]

    valids = [(3, 0)]
    max_depth = len(instructions) - 1
    result = set()
    while len(valids) != 0:
        current = valids.pop(0)
        value, depth = current

        if depth == max_depth:
            result.add(value)
            continue

        new_value = value * 8
        for i in range(8):
            computer_copy = create_computer_copy(computer)
            computer_copy["A"] = new_value + i
            output = get_output(computer_copy)

            if output == instructions[-len(output) :]:
                valids.append((new_value + i, depth + 1))

    return min(result)
