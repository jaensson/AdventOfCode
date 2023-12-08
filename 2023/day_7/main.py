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


def get_card_value(card, part):
    card_options_part_one = {
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

    card_options_part_two = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 1,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    return (
        card_options_part_one[card]
        if part == "one"
        else card_options_part_two[card]
    )


def get_type_part_one(hand):
    types = [
        "five-of-a-kind",
        "four-of-a-kind",
        "full-house",
        "three-of-a-kind",
        "two-pair",
        "one-pair",
        "high-card",
    ]

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

    cards = cards_in_hand.items()
    cards = sorted(
        cards_in_hand.items(), key=lambda card: card[1], reverse=True
    )
    cards = [card for card in cards if card[1] > 0]

    if cards[0][1] == 5:
        return types[0]
    elif cards[0][1] == 4:
        return types[1]
    elif cards[0][1] == 3 and cards[1][1] == 2:
        return types[2]
    elif cards[0][1] == 3:
        return types[3]
    elif cards[0][1] == 2 and cards[1][1] == 2:
        return types[4]
    elif cards[0][1] == 2:
        return types[5]
    else:
        return types[6]


def part1(lines):
    cards = [card.split(" ") for card in lines]
    cards = [[card[0], int(card[1])] for card in cards]

    types = {
        "five-of-a-kind": [],
        "four-of-a-kind": [],
        "full-house": [],
        "three-of-a-kind": [],
        "two-pair": [],
        "one-pair": [],
        "high-card": [],
    }

    for card in cards:
        hand = card[0]
        multiplier = card[1]
        types_in_hand = get_type_part_one(hand)
        types[types_in_hand].append([hand, multiplier])

    result = 0
    rank = len(cards)
    for type in types:
        card_in_type = types[type]
        sorted_cards = sorted(
            card_in_type,
            key=lambda card: [
                get_card_value(card, "one") for card in [*card[0]]
            ],
            reverse=True,
        )
        for card in sorted_cards:
            result += rank * card[1]
            rank -= 1

    return result


def get_type_part_two(hand):
    types = [
        "five-of-a-kind",
        "four-of-a-kind",
        "full-house",
        "three-of-a-kind",
        "two-pair",
        "one-pair",
        "high-card",
    ]

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

    cards = cards_in_hand.items()
    cards = sorted(
        cards_in_hand.items(), key=lambda card: card[1], reverse=True
    )
    cards = [card for card in cards if card[1] > 0 and card[0] != "J"]

    if (
        cards_in_hand["J"] == 5
        or cards[0][1] + cards_in_hand["J"] == 5
        or cards[0][1] == 5
    ):
        return types[0]
    elif cards[0][1] + cards_in_hand["J"] == 4 or cards[0][1] == 4:
        return types[1]
    elif (
        cards[0][1] + cards[1][1] + cards_in_hand["J"] == 5
        or cards[0][1] == 3
        and cards[1][1] == 2
    ):
        return types[2]
    elif cards[0][1] + cards_in_hand["J"] == 3 or cards[0][1] == 3:
        return types[3]
    elif (
        cards[0][1] + cards[1][1] + cards_in_hand["J"] == 4
        or cards[0][1] == 2
        and cards[1][1] == 2
    ):
        return types[4]
    elif cards[0][1] + cards_in_hand["J"] == 2 or cards[0][1] == 2:
        return types[5]
    else:
        return types[6]


def part2(lines):
    cards = [card.split(" ") for card in lines]
    cards = [[card[0], int(card[1])] for card in cards]

    types = {
        "five-of-a-kind": [],
        "four-of-a-kind": [],
        "full-house": [],
        "three-of-a-kind": [],
        "two-pair": [],
        "one-pair": [],
        "high-card": [],
    }

    for card in cards:
        hand = card[0]
        multiplier = card[1]
        types_in_hand = get_type_part_two(hand)
        types[types_in_hand].append([hand, multiplier])

    result = 0
    rank = len(cards)
    for type in types:
        card_in_type = types[type]
        sorted_cards = sorted(
            card_in_type,
            key=lambda card: [
                get_card_value(card, "two") for card in [*card[0]]
            ],
            reverse=True,
        )
        for card in sorted_cards:
            result += rank * card[1]
            rank -= 1

    return result


if __name__ == "__main__":
    main()
