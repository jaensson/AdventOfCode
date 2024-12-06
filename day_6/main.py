import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    starting_point = 0

    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "^":
                starting_point = (x, y, 0)
                break

    # print(starting_point)

    # part1_result = part1(lines, starting_point)
    # print(part1_result)
    part2_result = part2(lines, starting_point)
    print(part2_result)


def part1(grid, starting_point):
    stack = []
    seen = set()
    stack.append(starting_point)

    while len(stack) != 0:
        x, y, direction = stack.pop(0)

        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            print("stop")
            break

        seen.add((x, y))
        if direction % 4 == 0:
            if y - 1 < 0:
                print("stop")
                break

            if grid[y - 1][x] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("up")
                stack.append((x, y - 1, 0))
        elif direction % 4 == 1:
            if x + 1 >= len(grid[0]):
                print("stop")
                break

            if grid[y][x + 1] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("right")
                stack.append((x + 1, y, 1))
        elif direction % 4 == 2:
            if y + 1 >= len(grid):
                print("stop")
                break

            if grid[y + 1][x] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("down")
                stack.append((x, y + 1, 2))
        elif direction % 4 == 3:
            if x - 1 < 0:
                print("stop")
                break

            if grid[y][x - 1] == "#":
                stack.append((x, y, direction + 1))
            else:
                print("left")
                stack.append((x - 1, y, 3))

        # print(x, y, direction)
    print(seen)

    return len(seen)


def part2(grid, starting_point):
    def test_if_loop(start_x, start_y, start_direction):
        def is_start(x, y, direction):
            return (
                x == start_x and y == start_y and direction == start_direction
            )

        x, y, direction = start_x, start_y, start_direction
        print("start", x, y, direction)
        dir = direction

        # for d in range(direction, direction + 4):
        while True:
            dir = (dir + 1) % 4

            found_wall = False
            if dir == 0:  # UP
                # print("up")
                for i in range(y, 0, -1):
                    if grid[i - 1][x] == "#":
                        found_wall = True
                        break
                    y -= 1
                    if is_start(x, y, dir):
                        return True
            if dir == 1:  # RIGHT
                # print("right")
                for i in range(x, len(grid[0]) - 1):
                    if grid[y][i + 1] == "#":
                        found_wall = True
                        break
                    x += 1
                    if is_start(x, y, dir):
                        return True
            if dir == 2:  # DOWN
                # print("down")
                for i in range(y, len(grid) - 1):
                    if grid[i + 1][x] == "#":
                        found_wall = True
                        break
                    y += 1
                    if is_start(x, y, dir):
                        return True
            if dir == 3:  # LEFT
                # print("left")
                for i in range(x, 0, -1):
                    if grid[y][i - 1] == "#":
                        found_wall = True
                        break
                    x -= 1
                    if is_start(x, y, dir):
                        return True

            # print(x, y, dir)
            if not found_wall:
                return False

        # while len(stack) != 0:
        #     pass

        # print(x, y, direction)

    def walk(grid, starting_point):
        stack = []
        seen = set()
        stack.append(starting_point)

        while len(stack) != 0:
            x, y, direction = stack.pop(0)

            if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                break

            seen.add((x, y, direction % 4))

            if direction % 4 == 0:
                if y - 1 < 0:
                    break

                if grid[y - 1][x] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x, y - 1, 0))
            elif direction % 4 == 1:
                if x + 1 >= len(grid[0]):
                    break

                if grid[y][x + 1] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x + 1, y, 1))
            elif direction % 4 == 2:
                if y + 1 >= len(grid):
                    break

                if grid[y + 1][x] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x, y + 1, 2))
            elif direction % 4 == 3:
                if x - 1 < 0:
                    break

                if grid[y][x - 1] == "#":
                    stack.append((x, y, direction + 1))
                else:
                    stack.append((x - 1, y, 3))

        return seen

    result = walk(grid, starting_point)

    # print(test_if_loop(4, 8, 3))

    test = set()
    for x, y, direction in result:
        is_loop = test_if_loop(x, y, direction)
        if not is_loop:
            continue
        if direction % 4 == 0 and y > 0 and grid[y - 1][x] != "#":  # UP
            test.add((x, y - 1))
        if (
            direction % 4 == 1
            and x < len(grid[0]) - 1
            and grid[y][x + 1] != "#"
        ):  # RIGHT
            test.add((x + 1, y))
        if (
            direction % 4 == 2 and y < len(grid) - 1 and grid[y + 1][x] != "#"
        ):  # UP
            test.add((x, y + 1))
        if direction % 4 == 3 and x > 0 and grid[y][x - 1] != "#":  # LEFT
            test.add((x - 1, y))

    return len(test)
