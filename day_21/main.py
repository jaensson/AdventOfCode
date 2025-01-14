import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


"""
    Code:
        1. 029A

    First numeric keypad: (How to write the code on the numeric keypad)
        1. <A^A>^^AvvvA
        2. <A^A^>^AvvvA
        3. <A^A^^>AvvvA

    First directional keypad: (How to write the movement from the first numeric keypad)
        1. v<<A>>^A<A>AvA<^AA>A<vAAA>^A (<A^A>^^AvvvA)
        2. v<<A>>^A<A>A<Av>A<^A>Av>AAA>^A (<A^A^>^AvvvA)

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
                if char == "":
                    continue
                for i in range(12):
                    target = numeric_keypad[i // 3][i % 3]
                    if target == "":
                        continue

                    seen = set()
                    seen.add((0, 3))
                    shortest[(char, target)] = dfs(
                        x, y, (i % 3, i // 3), "", seen
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
                if char == "":
                    continue
                for i in range(6):
                    target = directional_keypad[i // 3][i % 3]
                    if target == "":
                        continue
                    seen = set()
                    seen.add((0, 0))
                    shortest[(char, target)] = dfs(
                        x, y, (i % 3, i // 3), "", seen
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

        new_result = set()
        shortest = min(result, key=lambda x: len(x))

        for res in result:
            if len(res) == len(shortest):
                new_result.add(res)

        return list(new_result)

    def build_directional_keypad(numeric_keypad, directional_keypad):
        test = dict()

        for number in numeric_keypad:
            result = []
            for movement in numeric_keypad[number]:
                movement = "A" + movement
                curr = [""]
                for i in range(1, len(movement)):
                    copy = curr[::]
                    curr = []
                    for r in copy:
                        for move in directional_keypad[
                            (movement[i - 1], movement[i])
                        ]:
                            curr.append(r + move + "A")
                copy = curr[::]
                curr = []
                for r in copy:
                    for fallback in directional_keypad[(movement[-1], "A")]:
                        curr.append(f"{r}{fallback}A")

                result.extend(curr)

            new_result = set()
            if len(result) == 0:
                test[number] = 0
                continue

            shortest = min(result, key=lambda x: len(x))
            for r in result:
                if len(r) == len(shortest):
                    new_result.add(r)

            test[number] = list(new_result)

        # for t in test:
        #     print(t, test[t])

        return test

    def build_my_directional(numeric_keypad, directional_keypad):
        test = dict()

        for number in numeric_keypad:
            result = []
            for movement in numeric_keypad[number]:
                movement = "A" + movement
                curr = [""]
                for i in range(1, len(movement)):
                    copy = curr[::]
                    curr = []
                    for r in copy:
                        for move in directional_keypad[
                            (movement[i - 1], movement[i])
                        ]:
                            curr.append(r + move + "A")
                copy = curr[::]
                curr = []
                for r in copy:
                    for fallback in directional_keypad[(movement[-1], "A")]:
                        curr.append(f"{r}{fallback}")

                result.extend(curr)

            new_result = set()
            shortest = min(result, key=lambda x: len(x))
            for r in result:
                if len(r) == len(shortest):
                    new_result.add(r)

            test[number] = list(new_result)

        return test

    numeric_keypad = get_numeric_keypad()
    directional_keypad = get_directional_keypad()
    test = build_directional_keypad(numeric_keypad, directional_keypad)
    test1 = build_my_directional(test, directional_keypad)

    print(test["7", "A"])
    print(test1["7", "A"])

    result = 0
    for code in codes:
        code = "A" + code
        length = 0
        for i in range(1, len(code)):
            length += len(test1[code[i - 1], code[i]][0])

        number = int("".join([c for c in code if c.isdigit()]))
        result += length * number

    return result


def part2(codes):
    def get_numeric_keypad():
        def bfs(start, target, seen):
            x, y = start
            queue = [(x, y, "")]
            while len(queue) != 0:
                current = queue.pop(0)
                x, y, path = current

                if (x, y) == target:
                    return "".join(sorted(list(path)))

                seen.add((x, y))
                if y - 1 >= 0 and (x, y - 1) not in seen:
                    queue.append((x, y - 1, path + "^"))

                if x + 1 < 3 and (x + 1, y) not in seen:
                    queue.append((x + 1, y, path + ">"))

                if y + 1 <= 3 and (x, y + 1) not in seen:
                    queue.append((x, y + 1, path + "v"))

                if x - 1 >= 0 and (x - 1, y) not in seen:
                    queue.append((x - 1, y, path + "<"))

        numeric_keypad = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["", "0", "A"],
        ]
        shortest = dict()

        for y, row in enumerate(numeric_keypad):
            for x, char in enumerate(row):
                if char == "":
                    continue
                for i in range(12):
                    target = numeric_keypad[i // 3][i % 3]
                    if target == "":
                        continue

                    seen = set()
                    seen.add((0, 3))
                    shortest[(char, target)] = bfs(
                        (x, y), (i % 3, i // 3), seen
                    )

        return shortest

    def get_directional_keypad():
        def dfs(start, target, seen):
            x, y = start
            queue = [(x, y, "")]
            while len(queue) != 0:
                current = queue.pop(0)
                x, y, path = current

                if (x, y) == target:
                    return "".join(sorted(list(path)))

                seen.add((x, y))
                if y - 1 >= 0 and (x, y - 1) not in seen:
                    queue.append((x, y - 1, path + "^"))

                if x + 1 < 3 and (x + 1, y) not in seen:
                    queue.append((x + 1, y, path + ">"))

                if y + 1 <= 3 and (x, y + 1) not in seen:
                    queue.append((x, y + 1, path + "v"))

                if x - 1 >= 0 and (x - 1, y) not in seen:
                    queue.append((x - 1, y, path + "<"))

        directional_keypad = [
            ["", "^", "A"],
            ["<", "v", ">"],
        ]
        shortest = dict()

        for y, row in enumerate(directional_keypad):
            for x, char in enumerate(row):
                if char == "":
                    continue
                for i in range(6):
                    target = directional_keypad[i // 3][i % 3]
                    if target == "":
                        continue
                    seen = set()
                    seen.add((0, 0))
                    shortest[(char, target)] = dfs(
                        (x, y), (i % 3, i // 3), seen
                    )

        return shortest

        test = dict()

        for number in numeric_keypad:
            result = []
            for movement in numeric_keypad[number]:
                movement = "A" + movement
                curr = [""]
                for i in range(1, len(movement)):
                    copy = curr[::]
                    curr = []
                    for r in copy:
                        for move in directional_keypad[
                            (movement[i - 1], movement[i])
                        ]:
                            curr.append(r + move + "A")
                copy = curr[::]
                curr = []
                for r in copy:
                    for fallback in directional_keypad[(movement[-1], "A")]:
                        curr.append(f"{r}{fallback}")

                result.extend(curr)

            new_result = set()
            shortest = min(result, key=lambda x: len(x))
            for r in result:
                if len(r) == len(shortest):
                    new_result.add(r)

            test[number] = list(new_result)

        return test

    def build_directional_keypad(numeric_keypad, directional_keypad):
        def build_comb(movement, position, current, result):
            if position >= len(movement) - 1:
                if len(current) not in result:
                    result[len(current)] = set()
                result[len(current)].add(current)
                return result

            for move in directional_keypad[
                (movement[position], movement[position + 1])
            ]:
                build_comb(movement, position + 1, f"{current}{move}A", result)

            return result

        test = dict()

        result = dict()
        for movement in numeric_keypad[("7", "A")]:
            movement = f"A{movement}A"
            build_comb(movement, 0, "", result)
        movement = result[min(result.keys())]

        for i in range(2):
            result = dict()
            for move in movement:
                move = f"A{move}"
                build_comb(move, 0, "", result)

            movement = result[min(result.keys())]

        # print(movement)

        return test

    numeric_keypad = get_numeric_keypad()
    directional_keypad = get_directional_keypad()
    movement = build_directional_keypad(numeric_keypad, directional_keypad)

    result = 0

    return result
