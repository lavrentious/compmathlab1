from argparser import ArgParser
import sys
from validators import validate_n, validate_float
from random import random
from io import TextIOWrapper
from typing import Any, List
from gauss_solver import GaussSolver
from solver import calculate_discrepancies
from logger import Logger
from utils import ResWriter
from argparser import OutputFormat

if __name__ != "__main__":
    exit(0)

logger = Logger()


def generate_random_dataset(out_stream: TextIOWrapper | Any, n: int):
    out_stream.write(str(n) + "\n")
    for i in range(n):
        for j in range(n):
            out_stream.write(str(round(random() * 1000, 3)) + " ")
        out_stream.write("\n")

    for i in range(n):
        out_stream.write(str(round(random() * 1000, 3)) + " ")
    out_stream.write("\n")


def read_dataset(
    in_stream: TextIOWrapper | Any,
) -> tuple[List[List[float]], List[float]]:
    silent = in_stream != sys.stdin

    if not silent:
        print("enter N: ", end="")
    n = validate_n(in_stream.readline().strip(), logger)

    matrix: List[List[float]] = []
    if not silent:
        print(f"enter A matrix ({n}x{n}), whitespace separated on each line:")
    for i in range(n):
        row = list(
            map(
                lambda x: validate_float(x, logger),
                in_stream.readline().replace(",", ".").split(),
            )
        )
        if len(row) != n:
            logger.critical(
                f"Invalid A matrix row {i=} (expected {n} elements, got {len(row)})"
            )
            exit(1)
        matrix.append(row)

    if len(set(tuple(row) for row in matrix)) != len(matrix):
        logger.critical("A matrix must be unique")
        exit(1)

    if not silent:
        print(f"enter B matrix ({n}x1), whitespace separated in 1 line:")
    bs = list(map(float, in_stream.readline().replace(",", ".").split()))
    if len(bs) != n:
        logger.critical(f"Invalid B matrix (expected {n} elements, got {len(bs)})")
        exit(1)
    return matrix, bs


def print_res(
    res: List[float],
    matrix: List[List[float]],
    bs: List[float],
    out_stream: TextIOWrapper | Any = sys.stdout,
):
    print("result:", res, file=out_stream)
    print(
        "rounded result:",
        ", ".join(map(str, map(lambda x: f"{x:.4f}", res))),
        file=out_stream,
    )
    print("discrepancies:", calculate_discrepancies(matrix, bs, res), file=out_stream)


def run() -> None:
    parser = ArgParser()
    parser.parse_and_validate_args(logger)

    if parser.help_mode:
        parser.print_help()
        return
    elif parser.generate_mode and parser.generate_n is not None:
        # generate mode
        n = parser.generate_n
        logger.debug(f"generating {n=}")
        generate_random_dataset(parser.out_stream, n)
    elif parser.standard_mode:
        # solve mode
        matrix, bs = read_dataset(parser.in_stream)
        solver = GaussSolver(matrix, bs)

        res = solver.solve(
            parser.verbose and parser.output_format == OutputFormat.HUMAN
        )

        res_writer = ResWriter(parser.out_stream)
        res_writer.write(res, matrix, bs, solver.det(), parser.output_format)


run()
