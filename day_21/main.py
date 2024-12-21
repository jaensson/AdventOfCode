import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)


"""
    Code:
        1. 029A

    First numeric keypad: (How to write the code on the numeric keypad)
        1. <A^A>^^AvvvA
        2. <A^A^>^AvvvA
        3. <A^A^^>AvvvA

    First directional keypad: (How to write the movement from the first numeric keypad)
        1. v<<A>>^A<A>AvA<^AA>A<vAAA>^A (<A^A>^^AvvvA)
        2. v<<A>>^A<A>A<Av>A<^A>Av<AAA>^A (<A^A^>^AvvvA)

    Second direction keypad (me?): (How to write the movement from the first directional keypad)
        1. <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A 

"""


def part1(codes):
    def get_numeric_keypad():
        def dfs(x, y, target, move, seen):
            if (x, y) == target:
                return [move]

            seen.add((x, y))
            test = []
            if y - 1 >= 0 and (x, y - 1) not in seen:
                up = dfs(x, y - 1, target, move + "^", seen.copy())
                test.extend(up)

            if x + 1 < 3 and (x + 1, y) not in seen:
                right = dfs(x + 1, y, target, move + ">", seen.copy())
                test.extend(right)

            if y + 1 <= 3 and (x, y + 1) not in seen:
                down = dfs(x, y + 1, target, move + "v", seen.copy())
                test.extend(down)

            if x - 1 >= 0 and (x - 1, y) not in seen:
                left = dfs(x - 1, y, target, move + "<", seen.copy())
                test.extend(left)

            if len(test) != 0:
                result = []
                shortest = min(test, key=lambda x: len(x))

                for t in test:
                    if len(t) == len(shortest):
                        result.append(t)

                return result

            return []

        numeric_keypad = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["", "0", "A"],
        ]
        shortest = dict()

        for y, row in enumerate(numeric_keypad):
            for x, char in enumerate(row):
                for i in range(12):
                    target = numeric_keypad[i // 3][i % 3]
                    shortest[(char, target)] = dfs(
                        x, y, (i % 3, i // 3), "", set()
                    )

        # for t in shortest:
        #     print(t, shortest[t])

        # print(shortest)
        return shortest

    def get_directional_keypad():
        def dfs(x, y, target, move, seen):
            if (x, y) == target:
                return [move]

            seen.add((x, y))
            test = []
            if y - 1 >= 0 and (x, y - 1) not in seen:
                up = dfs(x, y - 1, target, move + "^", seen.copy())
                test.extend(up)

            if x + 1 < 3 and (x + 1, y) not in seen:
                right = dfs(x + 1, y, target, move + ">", seen.copy())
                test.extend(right)

            if y + 1 < 2 and (x, y + 1) not in seen:
                down = dfs(x, y + 1, target, move + "v", seen.copy())
                test.extend(down)

            if x - 1 >= 0 and (x - 1, y) not in seen:
                left = dfs(x - 1, y, target, move + "<", seen.copy())
                test.extend(left)

            if len(test) != 0:
                result = []
                shortest = min(test, key=lambda x: len(x))

                for t in test:
                    if len(t) == len(shortest):
                        result.append(t)

                return result

            return []

        directional_keypad = [
            ["", "^", "A"],
            ["<", "v", ">"],
        ]
        shortest = dict()

        for y, row in enumerate(directional_keypad):
            for x, char in enumerate(row):
                for i in range(6):
                    target = directional_keypad[i // 3][i % 3]
                    shortest[(char, target)] = dfs(
                        x, y, (i % 3, i // 3), "", set()
                    )

        return shortest

    def build_numeric_comb(numeric_keyboard, code):
        code = "A" + code
        result = [""]
        for i in range(1, len(code)):
            new_result = []
            for r in result:
                for move in numeric_keyboard[(code[i - 1], code[i])]:
                    new_result.append(r + move + "A")

            result = new_result

        return result

        new_result = set()
        shortest = min(result, key=lambda x: len(x))

        for res in result:
            if len(res) == len(shortest):
                new_result.add(res)

        return list(new_result)

    def build_directional_keypad(directional_keypad, movements):
        result = set()

        for movement in movements:
            movement = "A" + movement
            current = [""]
            for i in range(1, len(movement)):
                new_result = []
                for r in current:
                    for move in directional_keypad[
                        (movement[i - 1], movement[i])
                    ]:
                        new_result.append(r + move + "A")
                current = new_result

            result.update(current)

        return list(result)

        new_result = set()
        shortest = min(result, key=lambda x: len(x))

        for r in result:
            if len(r) == len(shortest):
                new_result.add(r)

        return list(new_result)

    numeric_keypad = get_numeric_keypad()
    directional_keypad = get_directional_keypad()

    result = 0
    for code in codes:
        numeric = build_numeric_comb(numeric_keypad, code)
        first_directional = build_directional_keypad(
            directional_keypad, numeric
        )
        second_directional = build_directional_keypad(
            directional_keypad, first_directional
        )

        shortest = min(second_directional, key=lambda x: len(x))

        number = int("".join([c for c in code if c.isdigit()]))

        print(len(shortest), number)
        result += len(shortest) * number

    return result


def part2(lines):
    pass
