import json
import sys
from io import TextIOWrapper
from typing import Any, List

import numpy as np
from argparser import OutputFormat
from solver import calculate_discrepancies


class ResWriter:
    out_stream: TextIOWrapper | Any = sys.stdout

    def __init__(self, out_stream) -> None:
        self.out_stream = out_stream

    def write(
        self,
        res: List[float],
        matrix: List[List[float]],
        bs: List[float],
        det: float,
        format: OutputFormat = OutputFormat.HUMAN,
    ) -> None:
        if format == OutputFormat.HUMAN:
            self._write_human(res, matrix, bs, det)
        elif format == OutputFormat.JSON:
            self._write_json(res, matrix, bs, det)

    def _print_res(
        self,
        res: List[float],
        matrix: List[List[float]],
        bs: List[float],
    ):
        print("result:", res, file=self.out_stream)
        print(
            "rounded result:",
            ", ".join(map(str, map(lambda x: f"{x:.4f}", res))),
            file=self.out_stream,
        )
        print(
            "discrepancies:",
            calculate_discrepancies(matrix, bs, res),
            file=self.out_stream,
        )

    def _write_human(
        self, res: List[float], matrix: List[List[float]], bs: List[float], det: float
    ):
        self._print_res(res, matrix, bs)
        print("A's determinant:", det, file=self.out_stream)

        print("----- solving with numpy -----", file=self.out_stream)
        np_res = [float(x) for x in np.linalg.solve(matrix, bs)]
        self._print_res(
            np_res,
            matrix,
            bs,
        )
        print("A's determinant:", np.linalg.det(matrix), file=self.out_stream)

    def _write_json(
        self, res: List[float], matrix: List[List[float]], bs: List[float], det: float
    ):
        result_data = {
            "result": res,
            "rounded_result": [float(f"{x:.4f}") for x in res],
            "discrepancies": calculate_discrepancies(matrix, bs, res),
            "determinant": det,
        }

        np_res = [float(x) for x in np.linalg.solve(matrix, bs)]
        np_result_data = {
            "result": np_res,
            "rounded_result": [float(f"{x:.4f}") for x in np_res],
            "discrepancies": calculate_discrepancies(matrix, bs, np_res),
            "determinant": np.linalg.det(matrix),
        }

        output_data = {"solution": result_data, "numpy_solution": np_result_data}

        json.dump(output_data, self.out_stream, indent=4)
