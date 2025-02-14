from typing import List
import sys
from gauss_solver import GaussSolver
import numpy as np
from solver import calculate_discrepancies

if __name__ != "__main__":
    exit(0)


def read_input():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as file:
            lines = file.readlines()
        n = int(lines[0].strip())
        matrix = [list(map(float, lines[i + 1].split())) for i in range(n)]
        bs = list(map(float, lines[n + 1].split()))
    else:
        n = int(input("enter N: "))
        print("enter A (NxN):")
        matrix = [list(map(float, input().split())) for _ in range(n)]
        print("enter B (Nx1):")
        bs = list(map(float, input().split()))
    return n, matrix, bs


def print_res(res: List[float]):
    print("result:", res)
    print("rounded result:", ", ".join(map(str, map(lambda x: f"{x:.4f}", res))))
    print("discrepancies:", calculate_discrepancies(matrix, bs, res))


n, matrix, bs = read_input()

solver = GaussSolver(matrix, bs)
res = solver.solve(True)
print_res(res)
print("A's determinant:", solver.det())


print("----- solving with numpy -----")
np_res = [float(x) for x in np.linalg.solve(matrix, bs)]
print_res(np_res)
print("A's determinant:", np.linalg.det(matrix))
