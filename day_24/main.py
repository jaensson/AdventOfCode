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
    def get_specific_instruction(instructions, registers, operand):
        for instruction in instructions:
            used = set()
            used.add(instruction["left"])
            used.add(instruction["right"])

            if used == registers and instruction["operand"] == operand:
                return instruction

    def get_instruction(instructions, registers, operand):
        for instruction in instructions:
            used = set([instruction["left"], instruction["right"]])
            if (
                len(used.intersection(registers)) != 0
                and instruction["operand"] == operand
            ):
                return instruction

    def get_corresponding_instructions(number):
        if number == 0:
            valid = set()
            for instruction in instructions:
                used_registers = set()
                used_registers.add(instruction["left"])
                used_registers.add(instruction["right"])

                if (
                    f"x{number:02}" in used_registers
                    and f"y{number:02}" in used_registers
                ):
                    valid.add(tuple(instruction.items()))

            result = []
            for val in valid:
                result.append(dict(val))

            return result

    def get_wrong_outputs(instructions, registers, number, wrong, carry=None):
        if f"x{number:02}" not in registers:
            return

        if number == 0:
            input_and = get_specific_instruction(
                instructions, set([f"x{0:02}", f"y{0:02}"]), "AND"
            )
            input_xor = get_specific_instruction(
                instructions, set([f"x{0:02}", f"y{0:02}"]), "XOR"
            )

            return get_wrong_outputs(
                instructions, registers, number + 1, wrong, input_and["result"]
            )

        # print(number, carry)

        input_and = get_specific_instruction(
            instructions, set([f"x{number:02}", f"y{number:02}"]), "AND"
        )
        input_xor = get_specific_instruction(
            instructions, set([f"x{number:02}", f"y{number:02}"]), "XOR"
        )
        sum = get_specific_instruction(
            instructions, set([carry, input_xor["result"]]), "XOR"
        )
        tmp = get_specific_instruction(
            instructions, set([carry, input_xor["result"]]), "AND"
        )

        # print("input and:", input_and)
        # print("input xor:", input_xor)
        # print("sum:", sum)
        # print("tmp:", tmp)

        if sum is None and tmp is None:
            print("either the in carry is wrong or the value from input_xor")
            sum = get_instruction(
                instructions, set([carry, input_xor["result"]]), "XOR"
            )
            tmp = get_instruction(
                instructions, set([carry, input_xor["result"]]), "AND"
            )

            used_sum = set([sum["left"], sum["right"]])
            used_tmp = set([tmp["left"], tmp["right"]])
            if used_tmp != used_sum:
                print("this should not happen?")
                print(used_sum, used_tmp)

            used = used_sum

            if carry in used:
                used.remove(carry)
                expected = list(used)[0]
                print(
                    f"wrong input xor register should be {expected} but got",
                    input_xor["result"],
                )
                wrong.add(input_xor["result"])
                wrong.add(expected)

            if input_xor["result"] in used:
                used.remove(input_xor["result"])
                expected = list(used)[0]
                print(
                    f"wrong in carry register should be {expected} but got {carry}"
                )
                wrong.add(carry)
                wrong.add(expected)

            out_carry = get_instruction(
                instructions, set([input_and["result"], tmp["result"]]), "OR"
            )
            # print("out carry:", out_carry)

            return get_wrong_outputs(
                instructions, registers, number + 1, wrong, out_carry["result"]
            )

        if f"z{number:02}" != sum["result"]:
            print(
                f"wrong sum register should be z{number:02} but got",
                sum["result"],
            )
            wrong.add(sum["result"])
            wrong.add(f"z{number:02}")

            out_carry = get_instruction(
                instructions, set([input_and["result"], tmp["result"]]), "OR"
            )
            # print("out carry:", out_carry)

            return get_wrong_outputs(
                instructions, registers, number + 1, wrong, out_carry["result"]
            )
        out_carry = get_specific_instruction(
            instructions, set([input_and["result"], tmp["result"]]), "OR"
        )

        # print("out carry:", out_carry)

        get_wrong_outputs(
            instructions, registers, number + 1, wrong, out_carry["result"]
        )

    wrong = set()

    get_wrong_outputs(instructions, registers, 0, wrong)

    return ",".join(sorted(list(wrong)))
