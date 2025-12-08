import os
from lib.helpers import read_file


class UnionFind:
    def __init__(self, size):
        self.parent = [i for i in range(size)]

    def get_parent(self, a):
        return self.parent[a]

    def is_connected(self, a, b):
        return self.get_parent(a) == self.get_parent(b)

    def connect(self, a, b):
        if self.is_connected(a, b):
            return

        p_a, p_b = self.get_parent(a), self.get_parent(b)
        for i in range(len(self.parent)):
            if self.parent[i] == p_a:
                self.parent[i] = p_b

    def get_number_of_clusters(self):
        clusters = set()
        for i in range(len(self.parent)):
            clusters.add(self.get_parent(i))

        return len(clusters)

    def get_parents(self):
        return self.parent


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    boxes = parse_input(lines)
    pairs = get_pairs(boxes)

    result = part1(boxes, pairs, 1000)
    print(result)

    result = part2(boxes, pairs)
    print(result)


def parse_input(lines):
    boxes = []

    for line in lines:
        box = [int(coordinate) for coordinate in line.split(",")]
        boxes.append(box)

    return boxes


def get_pairs(boxes):
    pairs = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            distance = calculate_distance(boxes[i], boxes[j])
            pairs.append((i, j, distance))
    pairs.sort(key=lambda pair: pair[2])
    return pairs


def calculate_distance(box1, box2):
    return (
        (box1[0] - box2[0]) ** 2
        + (box1[1] - box2[1]) ** 2
        + (box1[2] - box2[2]) ** 2
    ) ** 0.5


def part1(boxes, pairs, number_of_connections):
    union_find = UnionFind(size=len(boxes))
    for i in range(number_of_connections):
        box1, box2, distance = pairs[i]
        union_find.connect(box1, box2)

    count = dict()
    for box in union_find.get_parents():
        count[box] = count.get(box, 0) + 1

    result = 1
    for number in sorted(count.values(), reverse=True)[:3]:
        result *= number
    return result


def part2(boxes, pairs):
    pairs = get_pairs(boxes)
    union_find = UnionFind(size=len(boxes))
    while union_find.get_number_of_clusters() != 1:
        box1, box2, distance = pairs.pop(0)
        union_find.connect(box1, box2)

    return boxes[box1][0] * boxes[box2][0]
