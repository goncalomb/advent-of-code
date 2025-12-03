from typing import TextIO


def load(fp: TextIO):
    def gen():
        while line := fp.readline():
            yield line.strip()
    return list(gen())


def find_max_batteries(data: list[str], num: int):
    total = 0
    for l in data:
        max_i = -1
        for n in range(num - 1, -1, -1):
            max_v = -1
            for i in range(max_i + 1, len(l) - n):
                v = int(l[i])
                if v > max_v:
                    max_i = i
                    max_v = v
            assert max_v != -1
            total += 10**n * max_v
    return total


def part1(data: list[str]):
    return find_max_batteries(data, 2)


def part2(data: list[str]):
    return find_max_batteries(data, 12)
