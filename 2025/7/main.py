from typing import TextIO


def load(fp: TextIO):
    def find_splitters(s: str):
        i = -1
        while (i := s.find('^', i + 1)) != -1:
            yield i
    data = [l.rstrip('\n') for l in fp.readlines()]
    splitters = [set(find_splitters(s)) for s in data[2::2]]
    return data[0].find('S'), len(data[0]), splitters


def part1and2(data: tuple[int, int, list[set[int]]]):
    s, l, splitters = data
    splits = 0
    beams = [0] * l
    beams[s] = 1
    for s in splitters:
        for b in s:
            if beams[b]:
                splits += 1
                beams[b - 1] += beams[b]
                beams[b + 1] += beams[b]
                beams[b] = 0
    return splits, sum(beams)
