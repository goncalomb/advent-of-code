from typing import TextIO


def load(fp: TextIO):
    ranges = []
    ids = []
    rr = True
    while line := fp.readline():
        line = line.strip()
        if not line:
            rr = not rr
        elif rr:
            ranges.append(tuple(int(v) for v in line.split('-')))
        else:
            ids.append(int(line))
    return ranges, ids


def part1(data: str):
    ranges, ids = data

    def test(id):
        for a, b in ranges:
            if a <= id <= b:
                return True
        return False

    return sum(test(id) for id in ids)


def part2(data: str):
    ranges, ids = data
    ranges_final = list(ranges)
    p = 0
    for i in range(len(ranges_final)):
        a, b = ranges_final[p] = ranges_final[i]
        p += 1
        for j in range(i + 1, len(ranges_final)):
            c, d = ranges_final[j]
            if a <= d and c <= b:  # merge?
                ranges_final[j] = (min(a, c), max(b, d))
                p -= 1  # discard
                break
    ranges_final = ranges_final[0:p]
    return sum(b - a + 1 for a, b in ranges_final)
