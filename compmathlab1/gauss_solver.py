import sys
from io import TextIOWrapper
from typing import Any, List

from solver import Solver


class GaussSolver(Solver):
    out_stream: TextIOWrapper | Any = sys.stdout

    def __init__(
        self,
        matrix: List[List[float]],
        bs: List[float],
        out_stream: TextIOWrapper | Any = None,
    ):
        self.out_stream = out_stream
        super().__init__([row.copy() for row in matrix], bs.copy())

    def print_matrix(self):
        n = len(self.matrix)
        for i in range(n):
            row = " ".join(f"{self.matrix[i][j]:>8.4f}" for j in range(n))
            print(f"[{row}] | {self.bs[i]:>8.4f}", file=self.out_stream)
        print("-" * (10 * n), file=self.out_stream)

    def to_upper_triangle(self, log=False) -> int:
        permutations = 0

        n = len(self.matrix)
        for i in range(0, n - 1):
            if self.matrix[i][i] == 0:
                # перестановка уравнений
                for j in range(i + 1, n):
                    if self.matrix[j][i] != 0:
                        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
                        self.bs[i], self.bs[j] = self.bs[j], self.bs[i]
                        permutations += 1
                        break

            for k in range(i + 1, n):
                try:
                    c = self.matrix[k][i] / self.matrix[i][i]
                except ZeroDivisionError:
                    raise Exception("the system is not solvable (rank(A) < n)")
                self.matrix[k][i] = 0
                for j in range(i + 1, n):
                    self.matrix[k][j] -= c * self.matrix[i][j]
                self.bs[k] -= c * self.bs[i]

            if log:
                print(f"step {i + 1}:", file=self.out_stream)
                self.print_matrix()

        return permutations

    def det(self):
        old_matrix = [row.copy() for row in self.matrix]
        old_bs = self.bs.copy()
        permutations = self.to_upper_triangle()
        ans = (-1) ** permutations
        for i in range(len(self.matrix)):
            if self.matrix[i][i] == 0:
                ans = 0
                break
            ans *= self.matrix[i][i]
        self.matrix = old_matrix
        self.bs = old_bs
        return ans

    def solve(self, log=False) -> List[float]:
        old_matrix = [row.copy() for row in self.matrix]
        old_bs = self.bs.copy()

        n = len(self.matrix)

        # 1. triangle
        self.to_upper_triangle(log)

        # 2. reverse
        res = [0.0] * n
        for i in range(n - 1, -1, -1):
            s = 0.0
            for j in range(i + 1, n):
                s += self.matrix[i][j] * res[j]
            res[i] = (self.bs[i] - s) / self.matrix[i][i]

        # restore initial values
        self.matrix = old_matrix
        self.bs = old_bs

        return res
