import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)
    lines = [parse_coordinate(line) for line in lines]

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def parse_coordinate(line):
    line = line.split(",")
    return (int(line[0]), int(line[1]))


def part1(coordinates):
    def draw_memory(fallen):
        for y in range(size + 1):
            for x in range(size + 1):
                if (x, y) in fallen:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def walk(start, end, size, fallen):
        queue = []
        queue.append((start, 0))

        seen = set()
        while len(queue) != 0:
            current, steps = queue.pop(0)
            x, y = current

            if current in seen:
                continue
            seen.add(current)

            if current == end:
                return steps

            if x - 1 >= 0 and (x - 1, y) not in fallen:
                queue.append(((x - 1, y), steps + 1))

            if x + 1 <= size and (x + 1, y) not in fallen:
                queue.append(((x + 1, y), steps + 1))

            if y - 1 >= 0 and (x, y - 1) not in fallen:
                queue.append(((x, y - 1), steps + 1))

            if y + 1 <= size and (x, y + 1) not in fallen:
                queue.append(((x, y + 1), steps + 1))

    size = 70

    start = (0, 0)
    exit = (size, size)

    fallen = set()
    for coordinate in coordinates[0:1024]:
        fallen.add(coordinate)

    return walk(start, exit, size, fallen)


def part2(coordinates):
    def walk(start, end, size, fallen):
        queue = []
        queue.append((start, 0))

        seen = set()
        while len(queue) != 0:
            current, steps = queue.pop(0)
            x, y = current

            if current in seen:
                continue
            seen.add(current)

            if current == end:
                return steps

            if x - 1 >= 0 and (x - 1, y) not in fallen:
                queue.append(((x - 1, y), steps + 1))

            if x + 1 <= size and (x + 1, y) not in fallen:
                queue.append(((x + 1, y), steps + 1))

            if y - 1 >= 0 and (x, y - 1) not in fallen:
                queue.append(((x, y - 1), steps + 1))

            if y + 1 <= size and (x, y + 1) not in fallen:
                queue.append(((x, y + 1), steps + 1))

    size = 70

    start = (0, 0)
    exit = (size, size)

    left = 0
    right = len(coordinates)

    while left < right:
        middle = left + (right - left) // 2

        fallen = set()
        for coordinate in coordinates[0:middle]:
            fallen.add(coordinate)

        test = walk(start, exit, size, fallen)

        if test is None:
            right = middle - 1
        else:
            left = middle + 1

    return coordinates[left]
