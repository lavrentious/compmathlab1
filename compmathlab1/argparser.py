import sys
import argparse
from argparse import Namespace
import os
from random import random
from io import TextIOWrapper
from typing import Any
from logger import Logger


class ArgParser:
    parser: argparse.ArgumentParser
    in_stream: None | TextIOWrapper | Any = sys.stdin
    out_stream: None | TextIOWrapper | Any = sys.stdout
    args: Namespace

    # args
    standard_mode: bool = False  # solve SLAU mode
    generate_mode: bool = False  # generate random mode
    generate_n: int | None = None  # N value
    help_mode: bool = False  # help mode
    verbose: bool  # verbosity for human format

    def _register_args(self):
        self.parser.add_argument("-h", "--help", action="store_true", help="shows help")
        self.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="set verbose mode (for human format only)",
        )
        self.parser.add_argument(
            "-g", "--generate", help="generate a random dataset with given N", type=int
        )
        self.parser.add_argument(
            "-o",
            "--output-file",
            help="specify output file",
            type=argparse.FileType("w"),
        )
        self.parser.add_argument(
            "input_file",
            nargs="?",
            help="file to read from",
            type=argparse.FileType("r"),
        )

    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=False)
        self._register_args()

    def parse_and_validate_args(self, logger: Logger | None = None) -> int:
        self.args = self.parser.parse_args()

        if self.args.input_file is not None:
            self.in_stream = self.args.input_file
        if self.args.output_file is not None:
            self.out_stream = self.args.output_file

        self.verbose = self.args.verbose or False
        if self.args.help:
            self.help_mode = True
        elif self.args.generate is not None:
            self.generate_mode = True
            self.generate_n = int(self.args.generate)
        else:
            self.standard_mode = True

        return 0

    def print_help(self):
        self.parser.print_help()
