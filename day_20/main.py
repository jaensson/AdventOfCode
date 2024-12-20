import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [list(line) for line in lines]

    # part1_result = part1(lines)
    # print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def get_start_and_end(grid):
    starting_position = None
    ending_position = None

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "S":
                starting_position = (x, y)
            if char == "E":
                ending_position = (x, y)

    return starting_position, ending_position


def part1(grid):
    def regular_path(start, end):
        queue = []
        queue.append((end, 0))

        path = dict()

        while len(queue) != 0:
            current, steps = queue.pop(0)
            x, y = current

            if current in path:
                continue

            path[current] = steps

            if y - 1 >= 0 and grid[y - 1][x] != "#":
                queue.append(((x, y - 1), steps + 1))
            if x + 1 < len(grid[0]) and grid[y][x + 1] != "#":
                queue.append(((x + 1, y), steps + 1))
            if y + 1 < len(grid) and grid[y + 1][x] != "#":
                queue.append(((x, y + 1), steps + 1))
            if x - 1 >= 0 and grid[y][x - 1] != "#":
                queue.append(((x - 1, y), steps + 1))

        return path

    def cheat_path(start, end, regular_path):
        total_steps = regular_path[start]
        queue = []
        queue.append((start, 0))

        cheat_path = set()

        seen = set()

        while len(queue) != 0:
            current, steps = queue.pop(0)

            if current in seen:
                continue
            seen.add(current)

            x, y = current
            cheats = []
            if y - 1 >= 0:
                if grid[y - 1][x] != "#":
                    queue.append(((x, y - 1), steps + 1))
                if (
                    grid[y - 1][x] == "#"
                    and y - 2 >= 0
                    and grid[y - 2][x] != "#"
                ):
                    cheats.append((current, (x, y - 2)))

            if x + 1 < len(grid[0]):
                if grid[y][x + 1] != "#":
                    queue.append(((x + 1, y), steps + 1))
                if (
                    grid[y][x + 1] == "#"
                    and x + 2 < len(grid[0])
                    and grid[y][x + 2] != "#"
                ):
                    cheats.append((current, (x + 2, y)))

            if y + 1 < len(grid):
                if grid[y + 1][x] != "#":
                    queue.append(((x, y + 1), steps + 1))
                if (
                    grid[y + 1][x] == "#"
                    and y + 2 < len(grid)
                    and grid[y + 2][x] != "#"
                ):
                    cheats.append((current, (x, y + 2)))

            if x - 1 >= 0:
                if grid[y][x - 1] != "#":
                    queue.append(((x - 1, y), steps + 1))
                if (
                    grid[y][x - 1] == "#"
                    and x - 2 >= 0
                    and grid[y][x - 2] != "#"
                ):
                    cheats.append((current, (x - 2, y)))

            for cheat in cheats:
                cheat_start, cheat_end = cheat
                cheat_steps = steps + regular_path[cheat_end] + 2

                saved_steps = total_steps - (cheat_steps)

                if saved_steps >= 100:
                    cheat_path.add(cheat)

        return len(cheat_path)

    start, end = get_start_and_end(grid)
    path = regular_path(start, end)

    return cheat_path(start, end, path)


def part2(grid):
    def regular_path(start, end):
        queue = []
        queue.append((end, 0))

        path = dict()

        while len(queue) != 0:
            current, steps = queue.pop(0)
            x, y = current

            if current in path:
                continue

            path[current] = steps

            if y - 1 >= 0 and grid[y - 1][x] != "#":
                queue.append(((x, y - 1), steps + 1))
            if x + 1 < len(grid[0]) and grid[y][x + 1] != "#":
                queue.append(((x + 1, y), steps + 1))
            if y + 1 < len(grid) and grid[y + 1][x] != "#":
                queue.append(((x, y + 1), steps + 1))
            if x - 1 >= 0 and grid[y][x - 1] != "#":
                queue.append(((x - 1, y), steps + 1))

        return path

    def cheat_path(cheats, grid, regular_path, current, current_steps, start):
        total_steps = regular_path[start]
        cheating_steps_allowed = 20

        queue = []
        queue.append((current, 0))
        seen = set()

        while len(queue) != 0:
            curr, steps = queue.pop(0)
            x, y = curr

            is_outside = y < 0 or x < 0 or y >= len(grid) or x >= len(grid[0])
            is_done = steps == cheating_steps_allowed + 1

            if is_outside or is_done or curr in seen:
                continue

            seen.add(curr)

            key = (current, curr)
            if key in cheats:
                continue

            if grid[y][x] == "." or grid[y][x] == "E":
                cheat_steps = steps + current_steps + regular_path[curr]
                saved_steps = total_steps - (cheat_steps)
                cheats[key] = saved_steps

            queue.append(((x, y - 1), steps + 1))
            queue.append(((x + 1, y), steps + 1))
            queue.append(((x, y + 1), steps + 1))
            queue.append(((x - 1, y), steps + 1))

    def get_number_of_cheating_routes(start, end, regular_path):
        queue = []
        queue.append((start, 0))

        cheats = dict()
        seen = set()

        while len(queue) != 0:
            current, steps = queue.pop(0)

            if current in seen:
                continue
            seen.add(current)

            x, y = current
            cheat_path(
                cheats,
                grid,
                regular_path,
                current,
                steps,
                start,
            )
            if y - 1 >= 0 and grid[y - 1][x] != "#":
                queue.append(((x, y - 1), steps + 1))
            if x + 1 < len(grid[0]) and grid[y][x + 1] != "#":
                queue.append(((x + 1, y), steps + 1))
            if y + 1 < len(grid) and grid[y + 1][x] != "#":
                queue.append(((x, y + 1), steps + 1))
            if x - 1 >= 0 and grid[y][x - 1] != "#":
                queue.append(((x - 1, y), steps + 1))

        result = 0
        for cheat in cheats:
            if cheats[cheat] >= 50:
                result += 1

        return result

    start, end = get_start_and_end(grid)
    path = regular_path(start, end)

    return get_number_of_cheating_routes(start, end, path)
