import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    tiles = parse_input(lines)

    result = part1(tiles)
    print(result)

    result = part2(tiles)
    print(result)


def parse_input(lines):
    tiles = []
    for line in lines:
        x, y = [int(coordinate) for coordinate in line.split(",")]
        tiles.append((x, y))
    return tiles


def part1(tiles):
    max_area = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            first, second = tiles[i], tiles[j]

            area = abs(first[0] - second[0] + 1) * abs(
                first[1] - second[1] + 1
            )
            max_area = max(max_area, area)

    return max_area


def part2(tiles):
    min_x, _ = min(tiles, key=lambda tile: tile[0])
    _, min_y = min(tiles, key=lambda tile: tile[1])
    max_x, _ = max(tiles, key=lambda tile: tile[0])
    _, max_y = max(tiles, key=lambda tile: tile[1])

    red_tiles = set(tiles)

    tiles.append(tiles[0])
    for i in range(len(tiles) - 2):
        first, middle, second = tiles[i], tiles[i + 1], tiles[i + 2]

        is_right = first[0] < second[0]
        is_down = first[1] < second[1]

        """
            paints green as walking
            up/left = NO
            up/right = YES
            down/left = YES
            down/right = NO

            left/up = YES
            left/down = NO
            right/up = NO
            right/down = YES
        """

        is_part_of_figure = (not is_right and is_down) or (
            is_right and not is_down or ()
        )
        print(first, second, is_part_of_figure)

        # for j in range(i + 1, len(tiles), 2):
        #     first, second = tiles[i], tiles[j]

        #     is_part_of_figure = first[0]

    # red_green_tiles = red_tiles.union(green_tiles)
    # max_area = 0
    # for i in range(len(tiles)):
    #     for j in range(i + 1, len(tiles)):
    #         first, second = tiles[i], tiles[j]

    #         third, fourth = (first[0], second[1]), (second[0], first[1])

    #         if third not in red_green_tiles and fourth not in red_green_tiles:
    #             continue

    #         area = abs(first[0] - second[0] + 1) * abs(
    #             first[1] - second[1] + 1
    #         )
    #         if third in red_green_tiles and fourth in red_green_tiles:
    #             max_area = max(max_area, area)
    #         elif third in red_green_tiles:
    #             max_area = max(max_area, area)
    #         elif fourth in red_green_tiles:
    #             max_area = max(max_area, area)
    #         else:
    #             print("här ska vi inte vara")

    #         # print(first, second, third, fourth)

    #         # area = abs(first[0] - second[0] + 1) * abs(
    #         #     first[1] - second[1] + 1
    #         # )
    #         # max_area = max(max_area, area)
    #     # break

    return 0


"""

red_tiles = set(tiles)

max_area = 0
for i in range(len(tiles)):
    for j in range(i + 1, len(tiles)):
        first, second = tiles[i], tiles[j]

        min_x, max_x = sorted([first[0], second[0]])
        min_y, max_y = sorted([first[1], second[1]])

        is_rectangle = True
        for x, y in red_tiles:
            if min_x < x < max_x and min_y < y < max_y:
                is_rectangle = False

        if is_rectangle:
            area = abs(first[0] - second[0] + 1) * abs(
                first[1] - second[1] + 1
            )
            print(first, second)
            max_area = max(max_area, area)

        # print(first, second, (min_x, min_y), (max_x, max_y))

return max_area

"""
