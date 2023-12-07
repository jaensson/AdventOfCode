import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n")

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def get_card_value(card):
    card_options = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    return card_options[card]


def get_type(hand):
    types = [
        "five-of-a-kind",
        "four-of-a-kind",
        "full-house",
        "three-of-a-kind",
        "two-pair",
        "one-pair",
    ]

    print(hand)

    cards_in_hand = {
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "T": 0,
        "J": 0,
        "Q": 0,
        "K": 0,
        "A": 0,
    }
    for card in hand:
        cards_in_hand[card] += 1

    test = cards_in_hand.items()
    print(test)


def part1(lines):
    cards = [card.split(" ") for card in lines]
    cards = [
        [
            "".join(sorted([*card[0]], key=lambda card: get_card_value(card))),
            int(card[1]),
        ]
        for card in cards
    ]

    types = {
        "five-of-a-kind": 0,
        "four-of-a-kind": 0,
        "full-house": 0,
        "three-of-a-kind": 0,
        "two-pair": 0,
        "one-pair": 0,
    }

    for card in cards:
        print(card)
        hand = card[0]
        multiplier = card[1]
        get_type(hand)


def part2(lines):
    pass


if __name__ == "__main__":
    main()
