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
    part2_result = part2(lines)
    print(part2_result)


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
    def evaluate(dp, spring, setup, curr_index, curr_group):
        # print("inne")
        key = (spring, curr_index, curr_group)
        if key in dp:
            return dp[key]

        hashtags_left = spring[curr_index:].count("#")
        question_marks_left = spring[curr_index:].count("?")

        if curr_group >= len(setup):
            dp[key] = 1
            return dp[key]

        if hashtags_left + question_marks_left < sum(
            setup[curr_group:]
        ):  # No characters left to fill
            dp[key] = 0
            return dp[key]

        if (
            curr_group >= len(setup)
            and curr_index <= len(spring)
            or curr_index >= len(spring)
            and curr_group <= len(setup)
        ):
            dp[key] = 0
            return dp[key]

        # if curr_group >= len(setup) and hashtags_left == 0:
        #     dp[key] = 1
        #     return dp[key]

        # if (
        #     curr_index >= len(spring)
        #     or curr_group >= len(setup)
        #     and hashtags_left != 0
        # ):
        #     dp[key] = 0
        #     return dp[key]

        # if hashtags_left + question_marks_left < sum(setup[curr_group:]):
        #     dp[key] = 0
        #     return dp[key]

        # print(curr_index, curr_group)

        start = curr_index
        end = start + setup[curr_group] - 1
        slice = spring[start : end + 1]

        if spring[start] == ".":
            dp[key] = evaluate(dp, spring, setup, curr_index + 1, curr_group)
            # print(curr_index + 1, curr_group)
            return dp[key]

        if spring[start] == "?":
            if "." in slice or (
                end + 1 < len(spring) and spring[end + 1] == "#"
            ):
                dp[key] = evaluate(
                    dp, spring, setup, curr_index + 1, curr_group
                )
                # print(curr_index + 1, curr_group)
                return dp[key]

            skip = evaluate(dp, spring, setup, curr_index + 1, curr_group)
            choose = evaluate(
                dp,
                spring,
                setup,
                curr_index + setup[curr_group] + 1,
                curr_group + 1,
            )
            dp[key] = skip + choose
            # print(curr_index + 1, curr_group)
            # print(curr_index + setup[curr_group] + 1, curr_group + 1)
            return dp[key]

        if spring[start] == "#":
            if (
                "." in slice
                or end + 1 < len(spring)
                and spring[end + 1] == "#"
            ):
                dp[key] = 0
                return dp[key]

            dp[key] = evaluate(
                dp,
                spring,
                setup,
                curr_index + setup[curr_group] + 1,
                curr_group + 1,
            )
            # print(curr_index + setup[curr_group] + 1, curr_group + 1)
            return dp[key]

    total = 0

    # print(evaluate(dict(), "?###????????", [3, 2, 1], 0, 0))

    # print(evaluate(dict(), "???.###", [1, 1, 3], 0, 0))

    for line in lines:
        spring, setup = line
        spring = "?".join([spring] * 5)
        setup = setup * 5

        # print(spring, setup)

        test = dict()
        val = evaluate(test, spring, setup, 0, 0)
        total += val
        # print(test)

    return total


if __name__ == "__main__":
    main()
