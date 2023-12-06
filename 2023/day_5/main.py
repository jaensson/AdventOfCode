import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n\n")

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


def list_to_int(list):
    return [int(element) for element in list]


def decode_input(lines):
    output = dict()

    for line in lines:
        key_value = line.split(":")
        key = key_value[0].replace(" map", "")
        data = key_value[1].strip()
        if line.startswith("seeds"):
            data = list_to_int(data.split(" "))
        else:
            data = data.split("\n")
            data = [list_to_int(data.split(" ")) for data in data]

        output[key] = data

    return output


def part1(lines):
    operations = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    seeds = lines["seeds"]
    lowest = []

    for seed in seeds:
        current_value = seed
        for operation in operations:
            for map in lines[operation]:
                destination_range_start = map[0]
                source_range_start = map[1]
                range_length = map[2]

                if (
                    source_range_start
                    <= current_value
                    <= source_range_start + range_length - 1
                ):
                    current_value = destination_range_start + (
                        current_value - source_range_start
                    )
                    break

        lowest.append(current_value)

    return min(lowest)


def get_intervals(lines):
    # [start, end, destination]
    intervals = [[line[1], line[1] + line[2] - 1, line[0]] for line in lines]
    intervals.sort(key=lambda interval: interval[0])

    return intervals


def seeds_interval(seeds):
    intervals = []
    for i in range(0, (len(seeds) - 1), 2):
        start = seeds[i]
        end = start + seeds[i + 1] - 1
        length = len(intervals)
        for i in range(length):
            interval = intervals[i]
            min_value = interval[0]
            max_value = interval[1]

            if min_value < start < max_value:
                max_value = max(max_value, end)
            if min_value < end < max_value:
                min_value = min(min_value, start)
            if max_value < start or end < min_value:
                intervals.append([start, end])
                break

            interval[0] = min_value
            interval[1] = max_value
            intervals[i] = interval

        if len(intervals) == 0:
            intervals.append([start, end])

    intervals.sort(key=lambda interval: interval[1])

    return intervals


def part2(lines):
    seed_interval = seeds_interval(lines["seeds"])

    interval_map = {
        key: get_intervals(lines[key])
        for key in lines.keys()
        if key != "seeds"
    }

    operations = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    current_intervals = seed_interval
    for operation in operations:
        operation_intervals = interval_map[operation]
        operation_interval_index = 0
        current_interval_index = 0

        new_intervals = []

        while current_interval_index < len(current_intervals):
            operation_interval = operation_intervals[operation_interval_index]
            current_interval = current_intervals[current_interval_index]

            # start = min(current_interval[0], operation_interval[0])
            # end = max(current_interval[1], operation_interval[1])

            # operation low | operation high | current low | current high
            if current_interval[0] > operation_interval[1]:
                if operation_interval_index < len(operation_intervals) - 1:
                    operation_interval_index += 1
                    continue
                else:
                    new_intervals.append(
                        [current_interval[0], current_interval[1]]
                    )
            # operation low | current low | current high | operation high
            elif (
                operation_interval[0] <= current_interval[0]
                and current_interval[1] <= operation_interval[1]
            ):
                start = (
                    current_interval[0]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                end = (
                    current_interval[1]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                new_intervals.append([start, end])
            # operation low | current low | operation high | current high
            elif (
                operation_interval[0] <= current_interval[0]
                and current_interval[0] <= operation_interval[1]
                and operation_interval[1] < current_interval[1]
            ):
                current_intervals.insert(
                    current_interval_index + 1,
                    [operation_interval[1] + 1, current_interval[1]],
                )
                start = (
                    current_interval[0]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                end = (
                    operation_interval[1]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                new_intervals.append([start, end])
            # current low | operation low | current high | operation high
            elif (
                current_interval[0] < operation_interval[0]
                and operation_interval[0] <= current_interval[1]
                and current_interval[1] <= operation_interval[1]
            ):
                start = (
                    operation_interval[0]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                end = (
                    current_interval[1]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                new_intervals.append([start, end])
            # current low | operation low | operation high | current high
            elif (
                current_interval[0] < operation_interval[0]
                and operation_interval[1] < current_interval[1]
            ):
                new_intervals.append(
                    [current_interval[0], operation_interval[0] - 1]
                )
                start = (
                    operation_interval[0]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                end = (
                    operation_interval[1]
                    - operation_interval[0]
                    + operation_interval[2]
                )
                new_intervals.append([start, end])
                current_intervals.insert(
                    current_interval_index + 1,
                    [operation_interval[1] + 1, current_interval[1]],
                )
            # current low | current high | operation low | operation high
            elif current_interval[1] < operation_interval[0]:
                new_intervals.append(
                    [current_interval[0], current_interval[1]]
                )
            current_interval_index += 1

        new_intervals.sort(key=lambda interval: interval[0])
        current_intervals = new_intervals

    lowest = [interval[0] for interval in new_intervals]

    return min(lowest)


if __name__ == "__main__":
    main()
