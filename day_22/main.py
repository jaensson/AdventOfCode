import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [int(line) for line in lines]

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(secret_numbers):
    def mix(original, secret_number):
        return secret_number ^ original

    def prune(secret_number):
        return secret_number % 16777216

    result = 0
    for secret_number in secret_numbers:
        for i in range(2000):
            secret_number = prune(mix(secret_number, secret_number * 64))
            secret_number = prune(mix(secret_number, secret_number // 32))
            secret_number = prune(mix(secret_number, secret_number * 2048))

        result += secret_number

    return result


def part2(secret_numbers):
    def mix(original, secret_number):
        return secret_number ^ original

    def prune(secret_number):
        return secret_number % 16777216

    result = 0
    bananas = dict()
    for secret_number in secret_numbers:
        price_change = []
        sequence = []
        start = 0
        seen = set()
        for i in range(2000):
            banana = secret_number % 10
            if len(price_change) != 0:
                sequence.append(banana - price_change[-1])
            if len(sequence[start : start + 4]) == 4:
                test = tuple(sequence[start : start + 4])
                if test not in seen:
                    seen.add(test)
                    if test not in bananas:
                        bananas[test] = 0
                    bananas[test] += banana
                start += 1

            secret_number = prune(mix(secret_number, secret_number * 64))
            secret_number = prune(mix(secret_number, secret_number // 32))
            secret_number = prune(mix(secret_number, secret_number * 2048))
            price_change.append(banana)

        result += secret_number

    return max(bananas.values())
