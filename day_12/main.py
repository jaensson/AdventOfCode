import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [list(line) for line in lines]

    part1_result = part1(lines)
    print(part1_result)
    # part2_result = part2(lines)
    # print(part2_result)


def part1(grid):
    def find_area(seen, start_x, start_y):
        current_region = grid[start_y][start_x]

        queue = []
        queue.append((start_x, start_y))
        current = set()
        fence = 0

        while len(queue) != 0:
            x, y = queue.pop(0)

            if (x, y) in current:
                continue

            current.add((x, y))
            seen.add((x, y))
            if y - 1 >= 0 and grid[y - 1][x] == current_region:
                queue.append((x, y - 1))
            else:
                fence += 1
            if y + 1 < len(grid) and grid[y + 1][x] == current_region:
                queue.append((x, y + 1))
            else:
                fence += 1
            if x - 1 >= 0 and grid[y][x - 1] == current_region:
                queue.append((x - 1, y))
            else:
                fence += 1
            if x + 1 < len(grid[0]) and grid[y][x + 1] == current_region:
                queue.append((x + 1, y))
            else:
                fence += 1

        print(fence)
        return len(current) * fence

    seen = set()
    total = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if (x, y) in seen:
                continue
            total += find_area(seen, x, y)

    return total


def part2(grid):
    def find_area(seen, start_x, start_y):
        current_region = grid[start_y][start_x]

        queue = []
        queue.append((start_x, start_y))
        current = set()
        fence = 0

        while len(queue) != 0:
            x, y = queue.pop(0)

            if (x, y) in current:
                continue

            current.add((x, y))
            seen.add((x, y))
            if y + 1 < len(grid) and grid[y + 1][x] == current_region:
                queue.append((x, y + 1))
                if (
                    x - 1 >= 0
                    and grid[y + 1][x - 1] != current_region
                    and x + 1 < len(grid[0])
                    and grid[y + 1][x + 1] != current_region
                ):  # Go down where both left and right is not in region
                    fence += 2
            if x + 1 < len(grid[0]) and grid[y][x + 1] == current_region:
                queue.append((x + 1, y))
            if y - 1 >= 0 and grid[y - 1][x] == current_region:
                queue.append((x, y - 1))
            if x - 1 >= 0 and grid[y][x - 1] == current_region:
                queue.append((x - 1, y))

        # print(current)

        # fence = 4
        # test = list(current)
        # for ix, curr in enumerate(test):
        #     x, y = curr
        #     print(x, y)

        return len(current)

    seen = set()
    total = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if (x, y) in seen:
                continue
            total += find_area(seen, x, y)
            break
        break

    return total
