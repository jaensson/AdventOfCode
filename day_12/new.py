import os
from typing import List
from enum import Enum
import time


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = [line for line in file.readlines()]
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
    # part2_result = part2(lines)
    # print(part2_result)


def part1(lines):
    def validate_comb(line, spring, setup):
        groups = [len(group) for group in spring.split(".") if group != ""]

        if groups != setup:
            return False

        for ix, char in enumerate(spring):
            if (
                char == "#"
                and line[ix] == "."
                or char == "."
                and line[ix] == "#"
            ):
                return False

        return True

    def test(line, setup):
        final = set()
        queue = [line]

        while len(queue) != 0:
            curr_spring = queue.pop(0)

            if curr_spring.count("?") == 0:
                if validate_comb(line, curr_spring, setup):
                    final.add(curr_spring)

                continue

            if curr_spring.count("?") + curr_spring.count("#") <= sum(setup):
                new_spring = curr_spring.replace("?", "#")
                if validate_comb(line, new_spring, setup):
                    final.add(new_spring)

                continue

            i = 0
            curr_group = 0
            while i < len(curr_spring):
                if curr_group == len(setup):
                    queue.append(curr_spring.replace("?", "."))
                    break

                start = i

                if curr_spring[start] == ".":
                    i += 1
                    continue

                end = start + setup[curr_group] - 1
                slice = curr_spring[start : end + 1]

                if curr_spring[start] == "?":
                    if "." in slice:
                        new_spring = (
                            curr_spring[:start]
                            + "."
                            + curr_spring[start + 1 :]
                        )
                        queue.append(new_spring)
                        break
                    if (
                        end + 1 < len(curr_spring)
                        and curr_spring[end + 1] == "#"
                    ):
                        new_spring = (
                            curr_spring[:start]
                            + "."
                            + curr_spring[start + 1 :]
                        )
                        queue.append(new_spring)
                        break

                    skip = curr_spring[:start] + "." + curr_spring[start + 1 :]
                    queue.append(skip)

                    # TODO: Fix such if end is the actual end to avoid adding a trailing "."
                    trailing = "." if end + 1 != len(curr_spring) else ""
                    pick = new_spring = (
                        curr_spring[:start]
                        + slice.replace("?", "#")
                        + trailing
                        + curr_spring[end + 2 :]
                    )
                    queue.append(pick)
                    break
                if curr_spring[start] == "#":
                    if "." in slice:
                        break
                    if "?" in slice:
                        trailing = "." if end + 1 != len(curr_spring) else ""
                        pick = new_spring = (
                            curr_spring[:start]
                            + slice.replace("?", "#")
                            + trailing
                            + curr_spring[end + 2 :]
                        )
                        queue.append(pick)
                        break
                    if (
                        end + 1 < len(curr_spring)
                        and curr_spring[end + 1] == "?"
                    ):
                        new_spring = (
                            curr_spring[: end + 1]
                            + "."
                            + curr_spring[end + 2 :]
                        )
                        queue.append(new_spring)
                        break
                    i += setup[curr_group]
                    curr_group += 1

        return len(final)

    total = 0
    for line, setup in lines:
        total += test(line, setup)

    return total


def part2(lines):
    pass


if __name__ == "__main__":
    main()
