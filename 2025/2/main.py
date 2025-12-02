#!/usr/bin/env python3

import math
import os
import sys


def open_input():
    file = os.path.join(os.path.dirname(__file__), 'input.txt')
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if file == '-':
            return sys.stdin
    return open(file)


def load_input():
    with open_input() as fp:
        for r in fp.read().strip().replace('\n', '').split(','):
            yield r.split('-')


def part1():
    value = 0
    for fst, lst in load_input():
        fst_i = int(fst)
        lst_i = int(lst)
        l = len(fst)
        # optimized repetition chunk (based on fst)
        # this brings the start of the iteration closer to fst
        p = 10**(l//2) if l % 2 else int(fst[0:l//2])
        while True:
            n = int(f'{p}{p}')
            if n > lst_i:
                break
            if n >= fst_i:
                value += n
            p += 1
    print(value)


def part2():
    # kind of a brute force approach but with some optimizations
    # using a set to exclude repeated values
    unique_ids = set()
    for fst, lst in load_input():
        fst_i = int(fst)
        lst_i = int(lst)
        # max number digits, d, limited by half digits of lst
        for d in range(1, len(lst)//2+1):
            # min repetitions, r, to reach fst (optimized start)
            r = max(math.ceil(len(fst)/d), 2)
            while True:
                p = 10**(d-1)  # repetition chunk
                n = int(str(p)*r)  # first number
                if n > lst_i:
                    break
                while True:
                    if n > lst_i:
                        break
                    if n >= fst_i:
                        unique_ids.add(n)
                    p += 1
                    n = int(str(p)*r)  # next number
                r += 1
    print(sum(unique_ids))


if __name__ == '__main__':
    part1()
    part2()
