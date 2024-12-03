import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(lines):
    result = 0

    for line in lines:
        ix = 0

        while ix < len(line):
            if line[ix : ix + 3] == "mul":
                current_mul = []

                current_mul.append("mul")
                ix += 3

                if line[ix] != "(":
                    ix += 1
                    continue

                current_mul.append("(")
                ix += 1

                for i in range(3, 0, -1):
                    if (line[ix : ix + i]).isdigit():
                        current_mul.append(line[ix : ix + i])
                        ix += i
                        break

                if line[ix] != ",":
                    ix += 1
                    continue

                current_mul.append(",")
                ix += 1

                for i in range(3, 0, -1):
                    if (line[ix : ix + i]).isdigit():
                        current_mul.append(line[ix : ix + i])
                        ix += i
                        break

                if line[ix] != ")":
                    ix += 1
                    continue

                current_mul.append(")")

                first = int(current_mul[2])
                second = int(current_mul[4])

                result += first * second

            ix += 1

    return result


def part2(lines):
    result = 0

    is_future_enabled = True

    for line in lines:
        ix = 0

        while ix < len(line):
            if line[ix : ix + 4] == "do()":
                is_future_enabled = True
                ix += 4
                continue
            if line[ix : ix + 7] == "don't()":
                is_future_enabled = False
                ix += 7
                continue

            if line[ix : ix + 3] == "mul":
                current_mul = []

                current_mul.append("mul")
                ix += 3

                if line[ix] != "(":
                    ix += 1
                    continue

                current_mul.append("(")
                ix += 1

                for i in range(3, 0, -1):
                    if (line[ix : ix + i]).isdigit():
                        current_mul.append(line[ix : ix + i])
                        ix += i
                        break

                if line[ix] != ",":
                    ix += 1
                    continue

                current_mul.append(",")
                ix += 1

                for i in range(3, 0, -1):
                    if (line[ix : ix + i]).isdigit():
                        current_mul.append(line[ix : ix + i])
                        ix += i
                        break

                if line[ix] != ")":
                    ix += 1
                    continue

                current_mul.append(")")

                if is_future_enabled:
                    first = int(current_mul[2])
                    second = int(current_mul[4])

                    result += first * second

            ix += 1

    return result
