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
    def find_string(line):
        new_string = []
        current_id = 0

        for ix, char in enumerate(line):
            if ix % 2 == 0:
                new_string += int(char) * [current_id]
                current_id += 1
            else:
                new_string += int(char) * ["."]

        left = 0
        right = len(new_string) - 1

        while left < right:
            while left < right and new_string[left] != ".":
                left += 1
            while left < right and new_string[right] == ".":
                right -= 1

            new_string[left], new_string[right] = (
                new_string[right],
                new_string[left],
            )

        total = 0
        for ix, char in enumerate(new_string):
            if char != ".":
                total += ix * char

        return total

    return find_string(lines[0])


def part2(lines):
    def find_string(line):
        new_string = []
        current_id = 0

        for ix, char in enumerate(line):
            if ix % 2 == 0:
                new_string.append(int(char) * [current_id])
                current_id += 1
            else:
                new_string.append(int(char) * ["."])

        right = len(new_string) - 1
        while 0 < right:
            if len(new_string[right]) == 0 or new_string[right][0] == ".":
                right -= 1
                continue
            for i in range(0, right):
                if len(new_string[i]) == 0 or new_string[i][0] != ".":
                    continue
                if len(new_string[i]) >= len(new_string[right]):
                    right_before = new_string[right]
                    new_string[i] = new_string[i][len(new_string[right]) :]
                    new_string[right] = len(new_string[right]) * ["."]
                    new_string.insert(i, right_before)
                    break
            right -= 1

        test = []
        for v in new_string:
            test.extend(v)

        total = 0
        for ix, char in enumerate(test):
            if char != ".":
                total += ix * char

        return total

    return find_string(lines[0])
