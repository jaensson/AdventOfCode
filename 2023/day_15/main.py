import os
from typing import List
from enum import Enum
import re


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split(",")

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
    hash_values = []
    for line in lines:
        current_value = 0
        for char in line:
            current_value += ord(char)
            current_value *= 17
            current_value %= 256
        hash_values.append(current_value)

    return sum(hash_values)


def part2(lines):
    boxes = dict()
    for line in lines:
        label, focal_length = re.split("=|-", line)

        current_hash = 0
        for char in label:
            current_hash += ord(char)
            current_hash *= 17
            current_hash %= 256

        if current_hash not in boxes:
            boxes[current_hash] = []

        if line.find("=") != -1:
            lense_exists = False
            for i, lense in enumerate(boxes[current_hash]):
                if lense.startswith(label):
                    lense_exists = True
                    break

            if lense_exists:
                boxes[current_hash][i] = f"{label} {focal_length}"
            else:
                boxes[current_hash].append(f"{label} {focal_length}")

        if line.find("-") != -1:
            for i, lense in enumerate(boxes[current_hash]):
                if lense.startswith(label):
                    del boxes[current_hash][i]

    lens_configuration = 0
    for lense, boxes in boxes.items():
        for slot, box in enumerate(boxes, start=1):
            label, focal = box.split(" ")
            value = (int(lense) + 1) * int(slot) * int(focal)
            lens_configuration += value

    return lens_configuration


if __name__ == "__main__":
    main()
