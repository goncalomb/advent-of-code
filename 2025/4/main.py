from typing import TextIO


def load(fp: TextIO):
    return [[bool(c == '@') for c in l.strip()] for l in fp.readlines()]


def find_accessible_rolls(data: list[list[bool]], k=1, n=4):
    w = len(data[0])
    h = len(data)

    def test(x, y):
        c = 0
        rx = max(0, x - k), min(w, x + k + 1)
        ry = max(0, y - k), min(h, y + k + 1)
        for xx in range(*rx):
            for yy in range(*ry):
                if data[xx][yy] and (xx != x or yy != y):
                    c += 1
                    if c >= n:
                        return False
        return True

    for x in range(0, w):
        for y in range(0, h):
            if data[x][y] and test(x, y):
                yield x, y


def part1(data: list[list[bool]]):
    return sum(1 for _ in find_accessible_rolls(data))


def part2(data: list[list[bool]]):
    total = 0
    found = True
    while found:
        found = False
        for x, y in find_accessible_rolls(data):
            data[x][y] = False
            found = True
            total += 1
    return total
