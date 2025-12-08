import math
from typing import TextIO


def load(fp: TextIO):
    def gen():
        while line := fp.readline():
            yield tuple(map(int, line.split(',')))
    return list(gen())


def d2(a, b):
    dx, dy, dz = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return dx*dx + dy*dy + dz*dz


def sorted_links(data: list[tuple[int, int, int]]):
    def gen():
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                yield i, j, d2(data[i], data[j])
    return sorted(gen(), key=lambda v: v[2])


def part1and2(data: list[tuple[int, int, int]]):
    data_len = len(data)

    # use closest power of 10 for max links (to support example input)
    part1_max_links = 10**math.floor(math.log10(data_len))
    part1 = part2 = -1

    # create circuits starting with closest links
    links_len = 0
    circuits = [i for i in range(data_len)]
    circuits_len = [1] * data_len
    for a, b, d2 in sorted_links(data):
        ca = circuits[a]
        cb = circuits[b]
        if ca != cb:
            for k in range(data_len):
                if circuits[k] == cb:
                    circuits[k] = ca
            joined_len = circuits_len[ca] + circuits_len[cb]
            circuits_len[ca] = joined_len
            circuits_len[cb] = 0

            if joined_len == data_len:
                # part2
                part2 = data[a][0] * data[b][0]
                break

        links_len += 1
        if links_len == part1_max_links:
            # part1
            lst = sorted(circuits_len, reverse=True)
            part1 = lst[0] * lst[1] * lst[2]

    return part1, part2
