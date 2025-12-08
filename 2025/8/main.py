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


def calculate_d2s(data: list[tuple[int, int, int]]):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            yield i, j, d2(data[i], data[j])


def part1and2(data: list[tuple[int, int, int]]):
    data_len = len(data)

    # use closest power of 10 for max links (to support example input)
    part1_max_links = 10**math.floor(math.log10(data_len))
    part1 = part2 = -1

    # calculate and sort distances
    d2s = list(calculate_d2s(data))
    d2s.sort(key=lambda v: v[2])

    # create circuits
    links_len = 0
    circuits = [i for i in range(data_len)]
    circuits_len = [1] * data_len
    for a, b, d2 in d2s:
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
            lst = list(circuits_len)
            lst.sort(reverse=True)
            part1 = lst[0] * lst[1] * lst[2]

    return part1, part2
