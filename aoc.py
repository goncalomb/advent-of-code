#!/usr/bin/env python3

import argparse
import datetime
import importlib
import os
import sys
import time
from typing import TextIO

AOC_FIRST_YEAR = 2015
AOC_LAST_YEAR = datetime.datetime.now().year
AOC_DAYS = 25
CODE_TEMPLATE = """
from typing import TextIO


def load(fp: TextIO):
    return fp.read()


def part1and2(data: str):
    return len(data), len(data)


def part1(data: str):
    return len(data)


def part2(data: str):
    return len(data)
"""


class PuzzleModule:
    @classmethod
    def get_all(cls, year=0, day=0):
        for y in (year,) if year else range(AOC_FIRST_YEAR, AOC_LAST_YEAR + 1):
            for d in (day,) if day else range(1, AOC_DAYS + 1):
                try:
                    yield cls(y, d)
                except ModuleNotFoundError:
                    pass

    def __init__(self, year: int, day: int):
        self._module = importlib.import_module(f'{year}.{day}.main')
        self._path = self._module.__loader__.path
        self._input = os.path.join(os.path.dirname(self._path), 'input.txt')
        self.year = year
        self.day = day

    def run(self, input: TextIO | None = None):
        has_load = hasattr(self._module, 'load')
        p1, p2 = hasattr(self._module, 'part1'), hasattr(self._module, 'part2')
        p1a2 = hasattr(self._module, 'part1and2')
        if (p1 and p2) == p1a2 or p1 != p2:
            return -1, "invalid functions, choose 'part1and2' OR 'part1' + 'part2'"

        if not input:
            if os.path.isfile(self._input):
                input = open(self._input, 'r')
            else:
                return -1, "no input"

        m = self._module
        with input:
            t0 = time.time()
            data = m.load(input) if has_load else input
            result = m.part1and2(data) if p1a2 else (
                m.part1(data), m.part2(data),
            )
            t1 = time.time()
            if not isinstance(result, tuple) or len(result) != 2:
                return -1, "result must be tuple of size 2"
            return t1 - t0, result

    def run_print(self, input: TextIO | None = None):
        t, result = self.run(input)
        if t == -1:
            print('%d %2d' % (self.year, self.day), ' ERROR', result)
        else:
            print('%d %2d %.3fs' % (self.year, self.day, t), result)


class PuzzleSet:
    def __init__(self, year=0, day=0):
        self.year = year
        self.day = day

    def get(self):
        return PuzzleModule.get_all(self.year, self.day)

    def run_print(self, input: TextIO | None = None):
        for pm in self.get():
            pm.run_print(input)

    def run_print_csv(self, input: TextIO | None = None):
        print('year,day,part1,part2')
        for pm in self.get():
            t, result = pm.run(input)
            p1, p2 = (-1, -1) if t == -1 else result
            print('%d,%d,%d,%d' % (pm.year, pm.day, p1, p2))


def command_new(args):
    f = os.path.join(str(args.year), str(args.day), 'main.py')
    f_full = os.path.join(os.path.dirname(__file__), f)

    if os.path.isfile(f_full):
        print("'%s' exists" % f, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(f_full), exist_ok=True)
    with open(f_full, 'w') as fp:
        fp.write(CODE_TEMPLATE.lstrip())

    print("'%s' created" % f)


def command_run(args):
    if args.input and not (args.year and args.day):
        print("'year' and 'day' are required when 'input' is used", file=sys.stderr)
        return 1

    ps = PuzzleSet(args.year, args.day)
    input = args.input() if args.input else None
    fn = ps.run_print_csv if args.csv else ps.run_print
    fn(input)


if __name__ == '__main__':
    def parse_int(min: int, max: int):
        def parse(value: str):
            v = int(value)
            if min <= v <= max:
                return v
            raise argparse.ArgumentTypeError(
                'must be between %d and %d (inclusive)' % (min, max)
            )
        return parse

    def parse_input(value: str):
        if value == '-':
            return lambda: sys.stdin
        if not os.path.isfile(value):
            raise argparse.ArgumentTypeError('file not found')
        return lambda: open(value, 'r')

    parse_year = parse_int(AOC_FIRST_YEAR, AOC_LAST_YEAR)
    parse_day = parse_int(1, AOC_DAYS)

    def parser_add_date_arguments(p: argparse.ArgumentParser, *, input=False, required=False):
        p.register('type', 'input', parse_input)
        p.register('type', 'year', parse_year)
        p.register('type', 'day', parse_day)

        if input:
            p.add_argument('-i', '--input', type='input',
                           help="file or '-' for stdin")

        g = p.add_argument_group(title='date arguments')
        g.add_argument('year', type='year', nargs=None if required else '?',
                       help='between %d and %d (inclusive)' % (AOC_FIRST_YEAR, AOC_LAST_YEAR))
        g.add_argument('day', type='day', nargs=None if required else '?',
                       help='between %d and %d (inclusive)' % (1, AOC_DAYS))

    parser = argparse.ArgumentParser(
        description='Advent of Code solutions manager and runner.',
        epilog='https://github.com/goncalomb/advent-of-code')
    subparsers = parser.add_subparsers(title='commands', required=True)

    parser_new = subparsers.add_parser(
        'new', help='create solution file',
        description='Create a new empty solution file for the selected year and day.')
    parser_add_date_arguments(parser_new, required=True)
    parser_new.set_defaults(fn=command_new)

    parser_run = subparsers.add_parser(
        'run', help='run solutions',
        description='Run all the solutions or by year/day.')
    parser_run.add_argument('--csv', action='store_true', help='output CSV')
    parser_add_date_arguments(parser_run, input=True)
    parser_run.set_defaults(fn=command_run)

    args = parser.parse_args()
    sys.exit(args.fn(args))
