import functools
from typing import TextIO


def load(fp: TextIO):
    devs: dict[str, set[str]] = {}
    while line := fp.readline():
        i = line.index(':')
        devs[line[:i]] = set(line[i+1:].split())
    return devs


def part1and2(data: dict[str, set[str]]):
    # Initially I did a naive DFS for part 1, but that doesn't work for part 2
    # because the search space is too large. After some iterations, I ended up
    # with a nice generic solution with a cache and a frozenset to track the
    # required nodes.

    @functools.cache
    def out_paths(dev: str, has: frozenset[str] = frozenset()):
        if dev in has:
            has -= {dev}
        paths = 0
        for o in data[dev]:
            if o == 'out':
                # invalid path if we didn't pass by all the required nodes
                paths += 0 if has else 1
            else:
                paths += out_paths(o, has)
        return paths

    return out_paths('you'), out_paths('svr', frozenset({'dac', 'fft'}))
