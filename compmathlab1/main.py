import sys
from gauss_solver import GaussSolver


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


if __name__ != "__main__":
    exit(0)

n, matrix, bs = read_input()

solver = GaussSolver(matrix, bs)
res, discrepancies = solver.solve(True)
print("result:", res)
print("rounded result:", ", ".join(map(str, map(lambda x: f"{x:.4f}", res))))
print("discrepancies:", discrepancies)
print("A's determinant:", solver.det())
