import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    registers = []
    instructions = []

    for i, line in enumerate(lines):
        if line == "":
            registers, instructions = parse(lines[:i], lines[i + 1 :])
            break

    part1_result = part1(registers, instructions)
    print(part1_result)


def parse(registers, instructions):
    register = dict()
    instruction = []

    for reg in registers:
        reg = reg.split(": ")
        value = True if int(reg[1]) == 1 else False
        register[reg[0]] = value

    for inst in instructions:
        inst = inst.split(" -> ")
        gates = inst[0].split(" ")
        inst_dict = dict()
        inst_dict["left"] = gates[0]
        inst_dict["operand"] = gates[1]
        inst_dict["right"] = gates[2]
        inst_dict["result"] = inst[1]

        instruction.append(inst_dict)

    return register, instruction


def part1(registers, instructions):
    # print(registers)
    # print(instructions)

    def and_gate(first, second):
        return first and second

    def or_gate(first, second):
        return first or second

    def xor_gate(first, second):
        return first ^ second

    test = {
        "AND": and_gate,
        "OR": or_gate,
        "XOR": xor_gate,
    }

    current = 0

    while len(instructions) != 0 and current < len(instructions):
        instruction = instructions[current % len(instructions)]
        if (
            instruction["left"] in registers
            and instruction["right"] in registers
        ):
            left = registers[instruction["left"]]
            right = registers[instruction["right"]]
            result = test[instruction["operand"]](left, right)

            registers[instruction["result"]] = result
            del instructions[current]
            current = 0
        else:
            current += 1

    start = 0
    number = ""
    while f"z{start:02}" in registers:
        number = str(int(registers[f"z{start:02}"])) + number
        start += 1

    result = int(number, 2)
    return result


def part2(lines):
    pass
