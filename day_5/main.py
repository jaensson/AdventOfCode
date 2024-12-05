import os
from lib.helpers import read_file


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)
    lines = " ".join(lines)
    lines = lines.split("  ")

    pages = dict()
    for page in lines[0].split(" "):
        page = page.split("|")
        first, second = int(page[0]), int(page[1])

        if first in pages:
            pages[first].add(second)
        else:
            pages[first] = set()
            pages[first].add(second)

    orders = lines[1].split(" ")
    orders = [cast_to_integer_list(order.split(",")) for order in orders]

    part1_result = part1(pages, orders)
    print(part1_result)
    part2_result = part2(pages, orders)
    print(part2_result)


def cast_to_integer_list(lst):
    return [int(e) for e in lst]


def part1(pages, orders):
    def evaluate(order):
        seen = set()
        for e in order:
            if e in pages:
                for test in pages[e]:
                    if test in seen:
                        return 0

            seen.add(e)

        return order[len(order) // 2]

    total = 0
    for order in orders:
        total += evaluate(order)

    return total


def part2(pages, orders):
    def evaluate(order):
        seen = set()
        for e in order:
            if e in pages:
                for test in pages[e]:
                    if test in seen:
                        result = topological_order(order)
                        return result

            seen.add(e)
        return 0

    def topological_order(order):
        seen = set()
        post = []

        for elem in order:
            if elem not in seen and elem in order:
                topoplogial_helper(seen, post, order, elem)

        return post[len(post) // 2]

    def topoplogial_helper(seen, post, order, current):
        seen.add(current)
        if current in pages:
            for elem in pages[current]:
                if elem not in seen and elem in order:
                    topoplogial_helper(seen, post, order, elem)
        post.append(current)

    total = 0
    for order in orders:
        total += evaluate(order)
    return total


if __name__ == "__main__":
    main()
