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

    part1_result = part1(registers, instructions[::])
    print(part1_result)
    part2_result = part2(registers, instructions[::])
    print(part2_result)


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

    result = int(number, base=2)
    return result


def part2(registers, instructions):
    def half_adder(instructions):
        valid = set()

        for instruction in instructions:
            if (
                f"{0:02}" in instruction["left"]
                and f"{0:02}" in instruction["left"]
            ):
                valid.add(tuple(instruction.items()))

        return valid

    def full_adder(instructions, number):
        def get_input_xor(number):
            for instruction in instructions:
                if (
                    f"{number:02}" in instruction["left"]
                    and f"{number:02}" in instruction["right"]
                    and instruction["operand"] == "XOR"
                ):
                    return instruction["result"]

            return ""

        def get_input_and(number):
            for instruction in instructions:
                if (
                    f"{number:02}" in instruction["left"]
                    and f"{number:02}" in instruction["right"]
                    and instruction["operand"] == "AND"
                ):
                    return instruction["result"]
            return ""

        def get_carry(number):
            if number == 0:
                return get_input_and(number)

            input_and = get_input_and(number)
            input_xor = get_input_xor(number)

            for instruction in instructions:
                keys = ["left", "right", "result"]
                for key in keys:
                    if (
                        f"{number:02}" in instruction[key]
                        or input_xor in instruction[key]
                        or input_and in instruction[key]
                    ) and instruction["operand"] == "OR":
                        return instruction["result"]
            return ""

        def get_temp(valid, carry, input_xor):
            for val in valid:
                val = dict(val)
                used_registers = set()
                used_registers.add(val["left"])
                used_registers.add(val["right"])
                if (
                    val["operand"] == "AND"
                    and val["left"] in used_registers
                    and val["right"] in used_registers
                ):
                    return val["result"]
            return ""

        valid = set()
        carry = get_carry(number - 1)
        input_xor = get_input_xor(number)
        input_and = get_input_and(number)

        for instruction in instructions:
            keys = ["left", "right", "result"]
            for key in keys:
                if (
                    f"{number:02}" in instruction[key]
                    or input_xor in instruction[key]
                    or input_and in instruction[key]
                ):
                    valid.add(tuple(instruction.items()))

        tmp = get_temp(valid, carry, input_xor)
        # print(carry, input_xor, input_and, tmp)

        for val in valid:
            val = dict(val)
            used_registers = set()
            used_registers.add(val["left"])
            used_registers.add(val["right"])

            carry_to_result = (
                val["operand"] == "XOR"
                and carry in used_registers
                and input_xor in used_registers
                and f"{number:02}" in val["result"]
            )

            carry_to_tmp = (
                val["operand"] == "AND"
                and carry in used_registers
                and input_xor in used_registers
            )

            out_carry = (
                input_and in used_registers
                and tmp in used_registers
                and val["operand"] == "OR"
                and f"{number:02}" not in val["result"]
            )

            if (
                not carry_to_result
                and not carry_to_tmp
                and not out_carry
                and not (
                    val["left"] in used_registers
                    and val["right"] in used_registers
                    and val["operand"] == "XOR"
                    and input_xor == val["result"]
                )
                and not (
                    val["left"] in used_registers
                    and val["right"] in used_registers
                    and val["operand"] == "AND"
                    and input_and == val["result"]
                )
            ):
                # print("ERROR")
                return val["result"]

            # print(val)
        return None

    start = 1
    while f"z{start:02}" in registers:
        result = full_adder(instructions, start)
        if result is not None:
            print("fel", result)
        start += 1
