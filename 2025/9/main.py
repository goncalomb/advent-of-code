from typing import TextIO


def load(fp: TextIO):
    def gen():
        while line := fp.readline():
            yield tuple(map(int, line.split(',')))
    return list(gen())


def ab_norm(a, b):
    (ax, ay), (bx, by) = a, b
    return (min(ax, bx), min(ay, by)), (max(ax, bx), max(ay, by))


def ab_area(a, b):
    return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)


def part1and2(data: list[tuple[int, int]]):
    # Part 1 was easy, just find the max area for all possible rectangles.
    # Part 2 took a while, but I ended up realizing that I just needed to test
    # if any of the segments intersect the rectangle. I consider the segments
    # as opposite points of another rectangle (not a really rectangle because
    # one of the sides is always 1) and test if the rectangles intersect.
    # Maybe there is some optimization to be done here.

    def seg_gen():
        l = len(data)
        for i in range(l):
            j = (i + 1) % l
            a, b = ab = ab_norm(data[i], data[j])
            # I don't think this approach would work with segments of size one,
            # because there could segments that intersect with the rectangle,
            # but still paint the entire rectangle (assert this case).
            dx = abs(b[0] - a[0])
            dy = abs(b[1] - a[1])
            assert dx == 0 and dy > 1 or dy == 0 and dx > 1
            yield ab

    # generate normalized list of segments (min, max)
    seg = list(seg_gen())

    def seg_test(a, b):
        (ax, ay), (bx, by) = a, b
        for (cx, cy), (dx, dy) in seg:
            # test rectangle intersection
            if ax < dx and bx > cx and ay < dy and by > cy:
                return False
        return True

    part1 = part2 = -1
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            a, b = ab_norm(data[i], data[j])
            area = ab_area(a, b)
            if area > part1:
                part1 = area
            if area > part2 and seg_test(a, b):
                part2 = area
    return part1, part2
