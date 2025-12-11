import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    connections = parse_input(lines)

    result = part1(connections)
    print(result)

    result = part2(connections)
    print(result)


def parse_input(lines):
    connections = dict()
    for line in lines:
        device, outputs = line.split(":")

        connections[device] = [
            output.strip() for output in outputs.strip().split(" ")
        ]

    return connections


def part1(connections):
    def paths_out(connections, current):
        if current == "out":
            return 1

        if current not in connections:
            return 0

        paths = 0
        for connection in connections[current]:
            paths += paths_out(connections, connection)
        return paths

    return paths_out(connections, "you")


def part2(connections):
    def paths_out(dp, connections, current, visited_dac, visited_fft):
        key = (current, visited_dac, visited_fft)
        if key in dp:
            return dp[key]

        if current == "out":
            if visited_dac and visited_fft:
                return 1
            return 0

        if current == "fft":
            visited_fft = True
        if current == "dac":
            visited_dac = True

        if current not in connections:
            return 0

        paths = 0
        for connection in connections[current]:
            paths += paths_out(
                dp, connections, connection, visited_dac, visited_fft
            )

        dp[key] = paths
        return dp[key]

    return paths_out(dict(), connections, "svr", False, False)
