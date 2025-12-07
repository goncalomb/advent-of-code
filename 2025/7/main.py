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
    beams = {s}
    paths = [0] * l
    paths[s] = 1
    for s in splitters:
        for b in set(beams):
            if b in s:
                splits += 1
                beams.remove(b)
                if b > 0:
                    paths[b - 1] += paths[b]
                    beams.add(b - 1)
                if b + 1 < l:
                    paths[b + 1] += paths[b]
                    beams.add(b + 1)
                paths[b] = 0
    return splits, sum(paths)
