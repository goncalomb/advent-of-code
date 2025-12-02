import math
from typing import TextIO


def load(fp: TextIO):
    return list(r.strip().split('-') for r in fp.read().strip().split(','))


def part1(data: list[list[str]]):
    value = 0
    for fst, lst in data:
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
    return value


def part2(data: list[list[str]]):
    # kind of a brute force approach but with some optimizations
    # using a set to exclude repeated values
    unique_ids = set()
    for fst, lst in data:
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
    return sum(unique_ids)
