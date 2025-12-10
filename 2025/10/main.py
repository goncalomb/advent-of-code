from collections import deque
from typing import TextIO


def load(fp: TextIO):
    def gen():
        while line := fp.readline():
            a = line.index('[') + 1
            b = line.index(']', a)
            c = line.index('{', b + 1) + 1
            d = line.index('}', c)
            ind, btn, jol = line[a:b], line[b+2:c-2], line[c:d]
            ind = ind.replace('.', '0').replace('#', '1')
            btn = [set(map(int, v[1:-1].split(','))) for v in btn.split(' ')]
            jol = list(map(int, jol.split(',')))
            yield ind, btn, jol
    return list(gen())


def btn2int(v: set[int], l: int):
    l -= 1
    r = 0
    for i in v:
        r |= 1 << l - i
    return r


def part1(data: list[tuple[str, list[set[int]], list[int]]]):
    def count_presses(ind_i, btn_i):
        # breadth first search
        l = len(btn_i)
        deq = deque()
        deq.append((1, 0, 0))  # depth, indicator, next button
        while len(deq):
            d, i, b = deq.popleft()
            while b < l:
                j = i ^ btn_i[b]
                if j == ind_i:
                    return d
                b += 1
                deq.append((d + 1, j, b))
        raise RuntimeError('invalid buttons')

    total = 0
    for ind, btn, _ in data:
        ind_i = int(ind, 2)
        btn_i = [btn2int(b, len(ind)) for b in btn]
        total += count_presses(ind_i, btn_i)
    return total


def part2(data: list[tuple[str, list[set[int]], list[int]]]):
    # TODO: Failed! The search space is too large for a naive approach.
    # I'll come back with more knowledge...
    return -1
