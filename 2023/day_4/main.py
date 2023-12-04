import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = [line.strip() for line in file.readlines()]
    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = decode_input(lines)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def decode_input(lines):
    cards = []

    for line in lines:
        line = line.split(":")
        card = {
            "card": int(line[0].split(" ")[-1]),
            "winning_numbers": [],
            "my_numbers": [],
        }
        numbers = line[1].split("|")

        for i, number in enumerate(numbers):
            lottery_numbers = number.split(" ")
            lottery_numbers = [
                int(num) for num in lottery_numbers if num != ""
            ]
            if i == 0:
                card["winning_numbers"] = lottery_numbers
            else:
                card["my_numbers"] = lottery_numbers

        cards.append(card)

    return cards


def part1(lines):
    total_score = 0
    for line in lines:
        score = 0
        for my_number in line["my_numbers"]:
            if my_number in line["winning_numbers"]:
                score = 1 if score == 0 else score * 2

        total_score += score

    return total_score


def part2(lines):
    copies = {line["card"]: 1 for line in lines}

    for line in lines:
        current_card = line["card"]

        won = 0
        for my_number in line["my_numbers"]:
            if my_number in line["winning_numbers"]:
                won += 1

        for j in range(1, won + 1):
            copies[current_card + j] += 1 * copies[current_card]

    return sum(copies.values())


if __name__ == "__main__":
    main()
