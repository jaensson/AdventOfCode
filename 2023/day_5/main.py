import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


class Map(Enum):
    SEED = 1
    SEED_TO_SOIL = 2
    SOIL_TO_FERTILIZER = 3
    FERTIIZER_TO_WATER = 4
    WATER_TO_LIGHT = 5
    LIGHT_TO_TEMPERATURE = 6
    TEMPERATURE_TO_HUMIDITY = 7
    HUMIDITY_TO_LOCATION = 8


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


def convert_to_map(lines):
    hash_map = dict()

    maps = lines.items()

    for map in maps:
        key = map[0]
        data = map[1]

        if key == "seeds":
            hash_map[key] = [int(data) for data in data]
            continue

        hash_map[key] = dict()

        for row in data:
            destination_range_start = int(row[0])
            source_range_start = int(row[1])
            range_length = int(row[2])

            for i in range(range_length):
                hash_map[key][source_range_start + i] = (
                    destination_range_start + i
                )

    return hash_map


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
    intervals_before_stage = []
    for line in lines:
        destination_range_sort = line[0]
        source_range_start = line[1]
        range_length = line[2]

        start = source_range_start
        end = source_range_start + range_length - 1

        print(start, end)

        intervals_length = len(intervals_before_stage)
        for i in range(intervals_length):
            interval_before_stage = intervals_before_stage[i]
            min_value = interval_before_stage[0]
            max_value = interval_before_stage[1]

            if min_value < start < max_value:
                max_value = max(max_value, end)
            if min_value < end < max_value:
                min_value = min(min_value, start)
            if max_value < start or end < min_value:
                intervals_before_stage.append([start, end])
                break

            interval_before_stage[0] = min_value
            interval_before_stage[1] = max_value
            intervals_before_stage[i] = interval_before_stage

        if len(intervals_before_stage) == 0:
            intervals_before_stage.append([start, end])

    print(intervals_before_stage)


def part2(lines):
    seeds = lines["seeds"]
    print(seeds)

    get_intervals(lines["seed-to-soil"])

    intervals = []
    for i in range(0, (len(seeds) - 1), 2):
        # first_seed = seeds[i]
        # second_seed = seeds[i + 1]
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

    operations = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    lowest = []
    for interval in intervals:
        operation = "seed-to-soil"

        current_value = interval[0]

        for operation in operations:
            for map in lines[operation]:
                destination_range_start = map[0]
                source_range_start = map[1]
                range_length = map[2]

                if (
                    source_range_start
                    <= current_value
                    <= source_range_start + range_length
                ):
                    current_value = destination_range_start

        lowest.append(current_value)

    print(lowest)

    return min(lowest)

    # lowest = []
    # for interval in intervals:
    #     # print(interval)
    #     start = interval[0]
    #     end = interval[1]

    #     current_value = start
    # print(current_value)

    # for operation in operations:
    #     for map in lines[operation]:
    #         destination_range_start = map[0]
    #         source_range_start = map[1]
    #         range_length = map[2]

    #         if (
    #             source_range_start
    #             <= current_value
    #             <= source_range_start + range_length - 1
    #         ):
    #             current_value = destination_range_start + (
    #                 current_value - source_range_start
    #             )
    #             break
    # lowest.append(current_value)

    # return min(lowest)

    # for seed in range(start, end):
    #     current_value = seed
    #     for operation in operations:
    #         for map in lines[operation]:
    #             destination_range_start = map[0]
    #             source_range_start = map[1]
    #             range_length = map[2]

    #             if (
    #                 source_range_start
    #                 <= current_value
    #                 <= source_range_start + range_length - 1
    #             ):
    #                 current_value = destination_range_start + (
    #                     current_value - source_range_start
    #                 )
    #                 break

    #     lowest.append(current_value)


if __name__ == "__main__":
    main()
