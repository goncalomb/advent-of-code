#!/usr/bin/env python3

import os
import sys


def load_input():
    file = os.path.join(os.path.dirname(__file__), 'input.txt')
    if len(sys.argv) > 1:
        file = sys.argv[1]
    with open(file) as fp:
        while line := fp.readline():
            n = int(line[1:])
            yield -n if line[0] == 'L' else n


def part1():
    code = 0
    dial = 50
    for n in load_input():
        dial = (dial + n) % 100
        if dial == 0:
            code += 1
    print(code)


def part2():
    code = 0
    dial = 50
    for n in load_input():
        code += abs((dial + n) // 100)
        if dial == 0 and n < 0:
            code -= 1
        dial = (dial + n) % 100
        if dial == 0 and n < 0:
            code += 1
    print(code)


if __name__ == '__main__':
    part1()
    part2()
