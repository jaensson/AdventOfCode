import os
from lib.helpers import read_file, read_file_without_strip


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    result = part1(lines)
    print(result)

    lines = read_file_without_strip(input_file)

    result = part2(lines)
    print(result)

def part1(lines):
    operations = [operation for operation in lines[-1].split(" ") if operation != ""]

    result = []
    for operation in operations:
        result.append(0 if operation == "+" else 1)

    for line in lines[:-1]:
        numbers = [number for number in line.split(" ") if number != ""]
        for ix, number in enumerate(numbers):
            if operations[ix] == "+":
                result[ix] += int(number)
            else:
                result[ix] *= int(number)


    return sum(result)


def part2(lines):
    operations = [operation for operation in lines[-1].split(" ") if operation != ""]

    result = []
    for operation in operations:
        result.append(0 if operation == "+" else 1)

    current_equation = 0
    for column in range(len(lines[0])):
        current = ""
        for row in range(len(lines[:-1])):
            current += lines[row][column]

        current = current.strip()

        if current == "":
            current_equation += 1
            continue


        if operations[current_equation] == "+":
            result[current_equation] += int(current)
        else:
            result[current_equation] *= int(current)
    
    return sum(result)
