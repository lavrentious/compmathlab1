from math import isnan
from typing import List


def sanitize(matrix: List[List[str]]) -> List[List[float]]:
    n = len(matrix)
    res: List[List[float]] = []
    for i in range(len(matrix)):
        res.append([])
        for j in range(len(matrix[i])):
            assert not isnan(float(matrix[i][j]))
            res[i].append(float(matrix[i][j]))
        assert len(res[i]) == n
    return res


def calculate_discrepancies(
    matrix: List[List[float]], bs: List[float], res: List[float]
) -> List[float]:
    n = len(matrix)
    discrepancies = [0.0] * n
    for i in range(n):
        discrepancies[i] = bs[i] - sum([matrix[i][j] * res[j] for j in range(n)])
    return discrepancies


class Solver:
    matrix: List[List[float]]
    bs: List[float]

    def __init__(self, matrix: List[List[float]], bs: List[float]):
        self.matrix = matrix
        self.bs = bs

    def det(self) -> float:
        def sub_det(matrix: List[List[float]]) -> float:
            if len(matrix) == 1:
                return matrix[0][0]
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

            res = 0.0
            for i in range(len(matrix[0])):
                sub_matrix: List[List[float]] = [
                    row[:i] + row[i + 1 :] for row in matrix[1:]
                ]
                res += ((-1) ** i) * matrix[0][i] * sub_det(sub_matrix)
            return res

        return sub_det(self.matrix)
