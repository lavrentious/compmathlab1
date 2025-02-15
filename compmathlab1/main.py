import sys
import argparse
import os
from random import random
from io import TextIOWrapper
from typing import Any, List
from gauss_solver import GaussSolver
from solver import calculate_discrepancies
import numpy as np

if __name__ != "__main__":
    exit(0)


def log(msg: str):
    print(msg, file=sys.stdout)


def error(msg: str):
    print(f"[ERROR] {msg}", file=sys.stderr)


def generate_random_dataset(out_stream: TextIOWrapper | Any, n: int):
    out_stream.write(str(n) + "\n")
    for i in range(n):
        for j in range(n):
            out_stream.write(str(round(random() * 1000, 3)) + " ")
        out_stream.write("\n")

    for i in range(n):
        out_stream.write(str(round(random() * 1000, 3)) + " ")
    out_stream.write("\n")


#  ----- validations -----
def validate_n(n: str) -> int:
    if not n.isdigit():
        error("N must be an integer.")
        exit(1)

    if not 1 <= int(n) <= 20:
        error("N must be in range [1, 20]")
        exit(1)

    return int(n)


def validate_float(f: str) -> float:
    try:
        return float(f)
    except ValueError:
        error(f"{f} is not a float")
        exit(1)


def read_dataset(
    in_stream: TextIOWrapper | Any,
) -> tuple[List[List[float]], List[float]]:
    silent = in_stream != sys.stdin

    if not silent:
        print("enter N: ", end="")
    n = validate_n(in_stream.readline().strip())

    matrix: List[List[float]] = []
    if not silent:
        print(f"enter A matrix ({n}x{n}), whitespace separated on each line:")
    for i in range(n):
        row = list(map(validate_float, in_stream.readline().replace(",", ".").split()))
        if len(row) != n:
            error(f"Invalid A matrix row {i=} (expected {n} elements, got {len(row)})")
            exit(1)
        matrix.append(row)

    if not silent:
        print(f"enter B matrix ({n}x1), whitespace separated in 1 line:")
    bs = list(map(float, in_stream.readline().replace(",", ".").split()))
    if len(bs) != n:
        error(f"Invalid B matrix (expected {n} elements, got {len(bs)})")
        exit(1)
    return matrix, bs


def print_res(res: List[float], matrix: List[List[float]], bs: List[float]):
    print("result:", res)
    print("rounded result:", ", ".join(map(str, map(lambda x: f"{x:.4f}", res))))
    print("discrepancies:", calculate_discrepancies(matrix, bs, res))


def run() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="shows help")
    parser.add_argument(
        "-g", "--generate", help="generate a random dataset with given N"
    )
    parser.add_argument("filepath", nargs="?", help="file to read from")
    args = parser.parse_args()

    file_path: str | None = args.filepath

    in_stream: None | TextIOWrapper | Any = sys.stdin
    out_stream: None | TextIOWrapper | Any = sys.stdout
    if file_path:
        if args.generate is None:
            if not os.path.exists(file_path):
                error(f"File '{file_path}' does not exist.")
                return
            if not os.access(file_path, os.R_OK):
                error(f"File '{file_path}' cannot be read. Permission denied.")
                return
            in_stream = open(file_path, "r")
        else:
            if not os.access(file_path, os.W_OK):
                error(f"File '{file_path}' cannot be written. Permission denied.")
                return
            out_stream = open(file_path, "w")
    silent = file_path is not None

    if args.help:
        parser.print_help()
        return
    elif args.generate is not None:
        # generate mode
        validate_n(args.generate)
        n: int = int(args.generate)
        print(f"generating {n=}")
        generate_random_dataset(out_stream, n)
    else:
        # solve mode
        matrix, bs = read_dataset(in_stream)
        solver = GaussSolver(matrix, bs)

        res = solver.solve(not silent)
        print_res(res, matrix, bs)
        print("A's determinant:", solver.det())

        print("----- solving with numpy -----")
        np_res = [float(x) for x in np.linalg.solve(matrix, bs)]
        print_res(np_res, matrix, bs)
        print("A's determinant:", np.linalg.det(matrix))


run()
