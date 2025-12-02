#!/usr/bin/env python3

import argparse
import datetime
import importlib
import os
import sys
import tempfile
import time

AOC_FIRST_YEAR = 2015
AOC_DAYS = 25
CODE_TEMPLATE = """
from typing import TextIO


def load(fp: TextIO):
    return fp.read()


def part1(data: str):
    return len(data)


def part2(data: str):
    return len(data)
"""


def module_load(year=None, day=None):
    for y in (year,) if year else range(AOC_FIRST_YEAR, datetime.datetime.now().year + 1):
        for d in (day,) if day else range(1, AOC_DAYS + 1):
            try:
                yield y, d, importlib.import_module(f'{y}.{d}.main')
            except ModuleNotFoundError:
                pass


def module_run(m, input_fp):
    if not input_fp:
        f = os.path.join(os.path.dirname(m.__loader__.path), 'input.txt')
        if os.path.isfile(f):
            input_fp = open(f, 'r')
        else:  # fallback to empty temporary file
            input_fp = tempfile.TemporaryFile(mode='r')
    t = time.time()
    with input_fp:
        data = m.load(input_fp)
    result = (
        m.part1(data),
        m.part2(data),
    )
    return time.time() - t, result


def command_new(args):
    # TODO: proper date and path checks
    f = os.path.join(args.year, args.day, 'main.py')
    f_full = os.path.join(os.path.dirname(__file__), f)

    if os.path.isfile(f_full):
        print("'%s' exists" % f, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(f_full))
    with open(f_full, 'w') as fp:
        fp.write(CODE_TEMPLATE.lstrip())

    print("'%s' created" % f)


def command_run(args):
    # TODO: proper date checks
    if args.input and not (args.year and args.day):
        print("'year' and 'day' are required when 'input' is used", file=sys.stderr)
        return 1

    input_fp = None
    if args.input == '-':
        input_fp = sys.stdin
    elif args.input:
        input_fp = open(args.input)

    for y, d, m in module_load(args.year, args.day):
        t, result = module_run(m, input_fp)
        print(y, d, '%.3fs' % t, result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    parser_new = subparsers.add_parser('new')
    parser_new.add_argument('year')
    parser_new.add_argument('day')
    parser_new.set_defaults(fn=command_new)

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('-i', '--input')
    parser_run.add_argument('year', nargs='?')
    parser_run.add_argument('day', nargs='?')
    parser_run.set_defaults(fn=command_run)

    args = parser.parse_args()
    sys.exit(args.fn(args))
