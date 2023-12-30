import os
from typing import List
from enum import Enum
import time


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n")
    lines = [
        (line.split(" ")[0], list(map(int, line.split(" ")[1].split(","))))
        for line in lines
    ]

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    start = time.time()
    part2_result = part2(lines)
    print(part2_result)
    end = time.time()
    print(end - start)


def part1(lines):
    def get_combinations(
        original, length, arrangements, current_arrangement=0
    ):
        if current_arrangement >= len(arrangements):
            return []

        valids = []

        offset = sum(arrangements[current_arrangement + 1 :]) + len(
            arrangements[current_arrangement + 1 :]
        )
        for i in range(
            length - arrangements[current_arrangement] + 1 - offset
        ):
            valid = [*"." * length]
            for j in range(arrangements[current_arrangement]):
                valid[i + j] = "#"

            sub_length = length - (i + arrangements[current_arrangement] + 1)
            sub_valids = get_combinations(
                original, sub_length, arrangements, current_arrangement + 1
            )

            for sub_valid in sub_valids:
                new_valid = (
                    "".join(valid)[
                        0 : i + arrangements[current_arrangement] + 1
                    ]
                    + sub_valid
                )
                valids.append(new_valid)

            if len(sub_valids) == 0:
                valids.append("".join(valid))

        return valids

    total = 0
    combinations = []
    for line in lines:
        start, arrangements = line
        valids = get_combinations(start, len(start), arrangements)

        for valid in reversed(valids):
            for j, char in enumerate(valid):
                if (
                    char == "."
                    and start[j] == "#"
                    or char == "#"
                    and start[j] == "."
                ):
                    valids.remove(valid)
                    break

        total += len(valids)
        combinations.append(len(valids))

    return total


if __name__ == "__main__":
    main()
