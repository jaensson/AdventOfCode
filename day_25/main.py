import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)
    keys, locks = parse(lines)

    part1_result = part1(keys, locks)
    print(part1_result)


def parse(lines):
    def key_or_lock(keys, locks, current):
        if current[0][0] == "#":
            locks.append(current)
        else:
            keys.append(current)

    keys = []
    locks = []

    current = []
    for i, line in enumerate(lines):
        if line == "":
            key_or_lock(keys, locks, current)
            current = []
        else:
            current.append(line)
    key_or_lock(keys, locks, current)

    key_height = []
    for key in keys:
        height = []
        for x in range(len(key[0])):
            for y in range(len(key)):
                if key[y][x] == "#":
                    height.append(len(key) - y - 1)
                    break
        key_height.append(height)

    lock_height = []
    for lock in locks:
        height = []
        for x in range(len(key[0])):
            for y in range(len(key)):
                if lock[y][x] == ".":
                    height.append(len(key) - (len(key) - y + 1))
                    break
        lock_height.append(height)

    return key_height, lock_height


def part1(keys, locks):
    def does_key_match_lock(lock, key):
        for i in range(len(lock)):
            if lock[i] + key[i] > 5:
                return False

        return True

    matches = 0
    for lock in locks:
        for key in keys:
            if does_key_match_lock(lock, key):
                matches += 1

    return matches


def part2(lines):
    pass
