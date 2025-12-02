from typing import TextIO


def load(fp: TextIO):
    def gen():
        while line := fp.readline():
            n = int(line[1:])
            yield -n if line[0] == 'L' else n
    return list(gen())


def part1(data: list[int]):
    code = 0
    dial = 50
    for n in data:
        dial = (dial + n) % 100
        if dial == 0:
            code += 1
    return code


def part2(data: list[int]):
    code = 0
    dial = 50
    for n in data:
        code += abs((dial + n) // 100)
        if dial == 0 and n < 0:
            code -= 1
        dial = (dial + n) % 100
        if dial == 0 and n < 0:
            code += 1
    return code
