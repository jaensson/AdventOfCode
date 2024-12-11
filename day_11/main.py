import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    lines = [int(stone) for stone in lines[0].split(" ")]

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def part1(stones):
    for i in range(6):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                test = str(stone)
                new_stones.append(int(test[0 : len(test) // 2]))
                if test[-1] != "0":
                    new_stones.append(int(test[len(test) // 2 :]))
                else:
                    new_stones.append(int(test[len(test) // 2 : len(test)]))
            else:
                new_stones.append(stone * 2024)

        stones = new_stones

    return len(stones)


def part2(stones):
    def break_down(dp, stone, depth):
        key = (stone, depth)

        if key in dp:
            return dp[key]

        if depth == 0:
            return 1

        if stone == 0:
            res = break_down(dp, 1, depth - 1)
            dp[key] = res
            return dp[key]
        elif len(str(stone)) % 2 == 0:
            test = str(stone)

            left = int(test[0 : len(test) // 2])
            if test[-1] != "0":
                right = int(test[len(test) // 2 :])
            else:
                right = int(test[len(test) // 2 : len(test)])

            res = break_down(dp, left, depth - 1) + break_down(
                dp, right, depth - 1
            )

            dp[key] = res
            return dp[key]
        else:
            res = break_down(dp, stone * 2024, depth - 1)
            dp[key] = res
            return dp[key]

    dp = dict()
    result = 0
    for stone in stones:
        result += break_down(dp, stone, 75)

    return result
