import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    connections = parse(lines)

    part1_result = part1(connections)
    print(part1_result)
    part2_result = part2(connections)
    print(part2_result)


def parse(lines):
    connections = dict()

    for connection in lines:
        test = connection.split("-")

        first, second = test

        if first not in connections:
            connections[first] = set()
        if second not in connections:
            connections[second] = set()

        connections[first].add(second)
        connections[second].add(first)

    return connections


def part1(connections):
    result = set()
    for node in connections:
        adjacents = list(connections[node])

        for i in range(len(adjacents)):
            for j in range(i + 1, len(adjacents)):
                if adjacents[i] in connections[adjacents[j]]:
                    test = sorted([node, adjacents[i], adjacents[j]])
                    result.add(tuple(test))

    count = set()
    for res in result:
        first, second, third = res
        test = [first, second, third]

        for t in test:
            if t[0] == "t":
                count.add(res)
                break

    return len(count)


def part2(connections):
    result = set()
    for node in connections:
        adjacents = list(connections[node])

        for i in range(len(adjacents)):
            for j in range(i + 1, len(adjacents)):
                if adjacents[i] in connections[adjacents[j]]:
                    test = sorted([node, adjacents[i], adjacents[j]])
                    result.add(tuple(test))

    while True:
        new_result = set()
        for res in result:
            res = set(res)
            for node in connections:
                if set(res).intersection(connections[node]) == res:
                    res.add(node)
                    res = tuple(sorted(list(res)))
                    new_result.add(res)

        if len(new_result) == 0:
            break
        result = new_result

    test = list(list(result)[0])
    test.sort()
    return ",".join(test)
