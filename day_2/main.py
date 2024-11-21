import os
from typing import List
from enum import Enum
import re


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = [line.strip() for line in file.readlines()]
    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = decode_input(read_file(input_file))

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def decode_input(lines: List[str]):
    res = []

    for line in lines:
        line = line.replace(" ", "").split(":")
        game = {"id": int(line[0][4:])}
        subsets = line[1].split(";")

        subset_temp = dict()
        for i, subset in enumerate(subsets):
            colors = subset.split(",")

            color_temp = dict()
            for color in colors:
                test = [re.split(r"\D+", color)[0], re.split(r"\d+", color)[1]]

                color_temp[test[1]] = int(test[0])

            subset_temp[i] = color_temp

        game["subsets"] = subset_temp
        res.append(game)

    return res


def part1(lines):
    BAG = {"red": 12, "green": 13, "blue": 14}
    BAG["total"] = sum(BAG.values())

    res = 0
    for line in lines:
        is_valid = True

        for subset in line["subsets"]:
            subset = line["subsets"][subset]
            total = sum(subset.values())
            if (
                total > BAG["total"]
                or "red" in subset
                and subset["red"] > BAG["red"]
                or "green" in subset
                and subset["green"] > BAG["green"]
                or "blue" in subset
                and subset["blue"] > BAG["blue"]
            ):
                is_valid = False
                break

        if is_valid:
            res += line["id"]

    return res


def part2(lines):
    res = 0
    for line in lines:
        colors_max = {"red": 0, "green": 0, "blue": 0}
        for subset in line["subsets"]:
            subset = line["subsets"][subset]
            for color in subset:
                if subset[color] > colors_max[color]:
                    colors_max[color] = subset[color]

        total = 1
        for color_total in colors_max.values():
            total *= color_total
        res += total

    return res


if __name__ == "__main__":
    main()
