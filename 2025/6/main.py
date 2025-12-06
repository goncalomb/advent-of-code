from typing import TextIO


def load(fp: TextIO):
    data = [l.rstrip('\n') for l in fp.readlines()]

    # find operations (+*) and digit offsets
    def find_ops():
        ops = data[-1]
        i, l = -1, len(ops)
        for j in range(l):
            if ops[j] in '+*':
                if i != -1:
                    yield ops[i], i, j - 1
                i = j
        if i != -1:
            yield ops[i], i, l

    # split all numbers
    return [(op, [n[i:l] for n in data[:-1]]) for op, i, l in find_ops()]


def part1(data: list[tuple[str, list]]):
    total = 0
    for op, num in data:
        if op == '+':
            total += sum(map(int, num))
        else:
            t = 1
            for n in num:
                t *= int(n)
            total += t
    return total


def part2(data: list[tuple[str, list]]):
    total = 0
    for op, num in data:
        if op == '+':
            for i in range(len(num[0])):
                total += int(''.join(n[i] for n in num))
        else:
            t = 1
            for i in range(len(num[0])):
                t *= int(''.join(n[i] for n in num))
            total += t
    return total
