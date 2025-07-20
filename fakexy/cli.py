#!/usr/bin/env python
# by Dominik Stanisław Suchora <hexderm@gmail.com>
# License: GNU GPLv3

import sys
import argparse
import json

import treerequests

from .fakexy import fakexy


def argparser():
    parser = argparse.ArgumentParser(
        description="Tool for getting results from fakexy.com",
        add_help=False,
    )

    parser.add_argument(
        "url",
        metavar="URL",
        type=str,
        help="url pointing to source",
    )
    parser.add_argument(
        "count",
        metavar="COUNT",
        type=int,
        help="count of results",
    )

    general = parser.add_argument_group("General")
    general.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit",
    )

    treerequests.args_section(parser)

    return parser


def cli(argv: list[str]):
    args = argparser().parse_args(argv)

    fxy = fakexy(logger=treerequests.simple_logger(sys.stderr))
    treerequests.args_session(fxy.ses, args)

    for i in fxy.guess(args.url, args.count):
        sys.stdout.write(json.dumps(i))
        sys.stdout.write("\n")
