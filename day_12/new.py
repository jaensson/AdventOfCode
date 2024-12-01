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
    # print(part1_result)
    # part2_result = part2(lines)
    # print(part2_result)


# ?#?#?#?#?#?#?#?
# .#.###.#?#?#?#?


def part1(lines):
    def find(spring, setup):
        queue = [(spring, 0, 0)]

        final = []

        # print("original:", spring)
        while len(queue) != 0:
            curr_spring, curr_group, curr_ix = queue.pop(0)

            groups = [group for group in curr_spring.split(".") if group != ""]
            if len(groups) == len(setup):
                # print("last:", curr_spring)
                final.append(curr_spring)
                continue

            for i in range(curr_ix, len(curr_spring) - 1):
                start = i
                end = start + setup[curr_group] - 1
                if end + 1 >= len(curr_spring):
                    break
                slice = curr_spring[start : end + 1]

                if curr_spring[i] == ".":
                    continue

                if curr_spring[end + 1] == "#":
                    new_spring = curr_spring[:i] + "." + curr_spring[i + 1 :]
                    queue.append((new_spring, curr_group, i))
                    # print(new_spring)
                    break

                if (
                    curr_spring[i] == "#"
                    and "." not in slice
                    and spring[end + 1] != "#"
                ):
                    new_spring = (
                        curr_spring[:i]
                        + setup[curr_group] * "#"
                        + "."
                        + curr_spring[i + 1 + setup[curr_group] :]
                    )
                    # print(new_spring)
                    queue.append(
                        (new_spring, curr_group + 1, i + setup[curr_group])
                    )
                    break

                if (
                    curr_spring[i] == "?"
                    and "." not in slice
                    and spring[end + 1] != "#"
                ):
                    new_spring = (
                        curr_spring[:i]
                        + setup[curr_group] * "#"
                        + "."
                        + curr_spring[i + 1 + setup[curr_group] :]
                    )
                    # print(new_spring)
                    queue.append(
                        (new_spring, curr_group + 1, i + setup[curr_group])
                    )
                    # break

        # print("last:", final)

        return final

    for spring, setup in lines:
        test = find(spring, setup)
        print(test, setup)


def part1_old(lines):
    def check(curr_spring, groups, setup):
        for ix, group in enumerate(groups):
            if len(group) < setup[ix] or group.count("#") > setup[ix]:
                return

        print(curr_spring, groups, setup)

    def test(spring, setup):
        queue = [
            (spring, 0, 0)
        ]  # Each entry is a set of (current spring, current group, current index)

        while len(queue) != 0:
            curr_spring, curr_group, curr_ix = queue.pop(0)
            print(curr_spring)

            groups = [group for group in curr_spring.split(".") if group != ""]

            if len(groups) == len(setup):
                # check(curr_spring, groups, setup)
                # print(curr_spring, groups, setup)
                continue

            if "?" not in curr_spring:
                continue

            while curr_ix < len(curr_spring) and curr_spring[curr_ix] != "?":
                curr_ix += 1

            if curr_ix == len(curr_spring) or curr_spring[curr_ix] != "?":
                continue

            test = curr_spring[curr_ix : curr_ix + setup[curr_group] + 1]
            print(test)

            if "." in test or len(test) > setup[curr_group]:
                new_spring = (
                    curr_spring[:curr_ix] + "." + curr_spring[curr_ix + 1 :]
                )
                print(new_spring, curr_ix)
                queue.append((new_spring, curr_group + 1, curr_ix + 1))
                continue

            skip_spring = (
                curr_spring[:curr_ix] + "." + curr_spring[curr_ix + 1 :]
            )

            place_spring = (
                curr_spring[:curr_ix]
                + setup[curr_group] * "#"
                + "."
                + curr_spring[curr_ix + 2 :]
            )

            print(skip_spring)
            print(place_spring)

            # queue.append((skip_spring, curr_group, curr_ix))
            # queue.append((place_spring, curr_group + 1, curr_ix))

    for spring, setup in lines[0:3]:
        test(spring, setup)

    return 0


def part2(lines):
    pass


if __name__ == "__main__":
    main()
