from typing import TextIO


def load(fp: TextIO):
    shapes: list[str] = []
    regions: list[tuple[int, int, list[int]]] = []
    while line := fp.readline():
        i = line.find('x')
        if i == -1:  # read shape
            shp: list[str] = []
            while (line := fp.readline()) and line != '\n':
                shp.append(line.rstrip())
            shapes.append(''.join(shp))
        else:  # read region
            j = line.index(':', i + 1)
            w, h = int(line[:i]), int(line[i+1:j])
            regions.append((w, h, list(map(int, line[j+2:].split()))))
    return shapes, regions


def part1and2(data: tuple[list[str], list[tuple[int, int, list[int]]]]):
    def shp_alts(shp: str):
        def remap(s: str, *idx):
            return ''.join(s[i] for i in idx)

        def rotations(s: str):
            yield s
            yield remap(s, 6, 3, 0, 7, 4, 1, 8, 5, 2)
            yield remap(s, 8, 7, 6, 5, 4, 3, 2, 1, 0)
            yield remap(s, 2, 5, 8, 1, 4, 7, 0, 3, 6)

        def flips(s: str):
            yield s
            yield remap(s, 6, 7, 8, 3, 4, 5, 0, 1, 2)
            yield remap(s, 2, 1, 0, 5, 4, 3, 8, 7, 6)

        assert len(shp) == 9
        for a in rotations(shp):
            for b in flips(a):
                yield b

    shapes, regions = data
    shapes_siz = [sum(s == '#' for s in shp) for shp in shapes]
    shapes_all = [set(shp_alts(shp)) for shp in shapes]

    valid = 0
    for w, h, nums in regions:
        area = w * h
        shp_area = sum(nums[i] * shapes_siz[i] for i in range(len(nums)))
        if area < shp_area:  # the shapes are larger than region, not valid
            continue
        # I was preparing to check the shapes, but apparently even if all the
        # shapes were 3x3 full (no gaps), they still all fit in the remaining
        # regions. So the remaining regions are all valid!
        # All that shape rotation/flip code was for nothing.
        assert sum(nums) * 9 <= area
        assert shapes_all  # unused, kept for posterity
        valid += 1

    return valid, 0  # no part 2 :(
