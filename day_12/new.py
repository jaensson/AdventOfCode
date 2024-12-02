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


# ?#?#?#?#?#?#?#?
# .#.###.#?#?#?#?

"""
    ??.?????.? 3,1

    ['#.?.###'] [1, 1, 3] = 1*1*1 = 1
    ['.??..??...?##.'] [1, 1, 3] = 2*2*1 = 4
    ['.#.###.#.#?#?#?'] [1, 3, 1, 6] = 1*1*1*1 = 1
    ['????.#...#...'] [4, 1, 1] = 1*1*1 = 1
    ['????.######..#####.'] [1, 6, 5] = 4*1*1 = 4
    ['.###.##.????', '.###.?##.???', '.###.??##.??', '.###.???##.?'] [3, 2, 1] = (1*1*4) + (1*1*3) + (1*1*2) + (1*1*1) = 4 + 3 + 2 + 1 = 10

    1 + 4 + 1 + 1 + 4 + 10 = 4 + 4 + 3 + 10 = 21
"""


def part1(lines):
    def valid_combination(arrangement, setup):
        arrangement = arrangement.replace("?", ".")
        groups = [group for group in arrangement.split(".") if group != ""]
        if len(groups) != len(setup):
            return False

        for ix, group in enumerate(groups):
            if len(group) != setup[ix]:
                return False

        return True

    def find(spring, setup):
        # print(spring)
        queue = [(spring, 0, 0)]

        final = set()

        # print("original:", spring)
        while len(queue) != 0:
            curr_spring, curr_group, curr_ix = queue.pop(0)

            # groups = [group for group in curr_spring.split(".") if group != ""]
            # if len(groups) == len(setup):
            #     # print("last:", curr_spring)
            #     final.append(curr_spring)
            #     continue

            # print(curr_spring, curr_group, curr_ix)
            if valid_combination(curr_spring, setup):
                final.add(curr_spring.replace("?", "."))

            if curr_group == len(setup):
                continue

            for i in range(curr_ix, len(curr_spring)):
                start = i
                end = start + setup[curr_group] - 1
                slice = curr_spring[start : end + 1]

                if curr_spring[i] == ".":
                    continue

                if end + 1 == len(curr_spring):
                    new_spring = (
                        curr_spring[:i]
                        + "#" * len(slice)
                        + curr_spring[i + len(slice) + 1 :]
                    )
                    # print(new_spring)
                    queue.append((new_spring, curr_group + 1, i + len(slice)))
                    break

                if curr_spring[end + 1] == "#":
                    new_spring = curr_spring[:i] + "." + curr_spring[i + 1 :]
                    queue.append((new_spring, curr_group, i))
                    # print(new_spring)
                    break

                if (
                    curr_spring[i] == "?"
                    and "." in slice
                    and spring[end + 1] != "#"
                ):
                    new_spring = (
                        curr_spring[:i]
                        + len(slice) * "."
                        + curr_spring[i + len(slice) :]
                    )
                    # print(new_spring)
                    queue.append((new_spring, curr_group, i + len(slice)))
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
                    print(new_spring)
                    queue.append(
                        (new_spring, curr_group + 1, i + setup[curr_group])
                    )
                    break

                if (
                    curr_spring[i] == "?"
                    and "." not in slice
                    and spring[end + 1] != "#"
                ):
                    # new_spring = (
                    #     curr_spring[:i]
                    #     + setup[curr_group] * "#"
                    #     + "."
                    #     + curr_spring[i + 1 + setup[curr_group] :]
                    # )
                    new_spring = (
                        curr_spring[:curr_ix]
                        + "." * (i - curr_ix)
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

    def count_permutations(arrangements, setup):
        # print(arrangements, setup)
        total_perm = 0
        for arrangement in arrangements:
            groups = [group for group in arrangement.split(".") if group != ""]
            # print(groups)
            perm = 1
            for i in range(len(groups)):
                if len(groups[i]) == setup[i]:
                    continue
                if setup[i] == 1:
                    perm *= len(groups[i])
            total_perm += perm
        return total_perm

    perm = 0
    for spring, setup in lines[1:2]:
        test = find(spring, setup)
        print(test, setup)
        perm += len(test)
        # perm += count_permutations(test, setup)
        # print(perm)

    return perm


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
