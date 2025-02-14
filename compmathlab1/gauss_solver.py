from typing import List, Tuple
from solver import Solver


class GaussSolver(Solver):

    def __init__(self, matrix: List[List[float]], bs: List[float]):
        super().__init__(matrix, bs)

    def print_matrix(self):
        n = len(self.matrix)
        for i in range(n):
            row = " ".join(f"{self.matrix[i][j]:>8.4f}" for j in range(n))
            print(f"[{row}] | {self.bs[i]:>8.4f}")
        print("-" * (10 * n))

    def solve(self, log=False) -> Tuple[List[float], List[float]]:
        old_matrix = [row.copy() for row in self.matrix]
        old_bs = self.bs.copy()

        n = len(self.matrix)

        # 1. triangle
        for i in range(0, n - 1):
            if self.matrix[i][i] == 0:
                # перестановка уравнений
                for j in range(i + 1, n):
                    if self.matrix[j][i] != 0:
                        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
                        self.bs[i], self.bs[j] = self.bs[j], self.bs[i]
                        break

            for k in range(i + 1, n):
                c = self.matrix[k][i] / self.matrix[i][i]
                self.matrix[k][i] = 0
                for j in range(i + 1, n):
                    self.matrix[k][j] -= c * self.matrix[i][j]
                self.bs[k] -= c * self.bs[i]

            if log:
                print(f"step {i + 1}:")
                self.print_matrix()

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

        # 3. discrepancy
        discrepancies = [0.0] * n
        for i in range(n):
            discrepancies[i] = self.bs[i] - sum(
                [self.matrix[i][j] * res[j] for j in range(n)]
            )

        return res, discrepancies
