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

    lines = decode_input(lines)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def decode_input(lines):
    times = []
    distances = []
    for line in lines:
        values = line.split(":")
        data = values[1].split(" ")
        if values[0].startswith("Time"):
            times.extend(data)
        else:
            distances.extend(data)

    times = [time for time in times if time != ""]
    distances = [distance for distance in distances if distance != ""]

    races = []
    for i in range(len(times)):
        races.append([int(times[i]), int(distances[i])])

    return races


def part1(lines):
    combinations = []
    for race in lines:
        time = race[0]
        distance = race[1]

        distances = []

        for i in range(time + 1):
            travled_distance = i * (time - i)
            if travled_distance > distance:
                distances.append(travled_distance)
        combinations.append(len(distances))

    total_combinations = 1
    for combination in combinations:
        total_combinations *= combination

    return total_combinations


def part2(lines):
    time = int("".join([str(race[0]) for race in lines]))
    distance = int("".join([str(race[1]) for race in lines]))

    left = 0
    right = time
    low = time
    while left <= right:
        middle = left + (right - left) // 2

        travled_distance = middle * (time - middle)
        if travled_distance > distance:
            right = middle - 1
            low = min(low, middle)
        else:
            left = middle + 1

    return (time - low) - low + 1


if __name__ == "__main__":
    main()
