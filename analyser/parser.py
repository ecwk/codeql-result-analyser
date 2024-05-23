import re
from typing import TypedDict
from pathlib import Path

import pandas as pd


class CodeQLFunctionTraceResult(TypedDict):
    function_name_a: str
    function_name_b: str
    start_line_a: int
    start_line_b: int
    end_line_a: int
    end_line_b: int
    start_column_a: int
    start_column_b: int
    end_column_a: int
    end_column_b: int
    file_path_a: str
    file_path_b: str


def parse_codeql_function_trace_results(
    results_file: Path,
    source_dir: Path,
    col_idx: int = 3,
    include_source_dir: bool = False,
) -> pd.DataFrame:
    results = pd.read_csv(
        results_file,
        # header=None,
    )

    parsed = pd.DataFrame()

    for i, result in results.iterrows():
        data = result[col_idx]
        # function_name_a, file_path_a, function_name_b, file_path_b
        match = re.match('("")(.+?)("")', data)
        # print(result, data)
        print(i)
        print(results)
        break

    return parsed


result = parse_codeql_function_trace_results(
    Path("results.csv"),
    Path(
        "C:\\Users\\maxki\\Downloads\\Work\\chromium\\src\\third_party\\angle",
    ),
)

# print(result)
# print(type(result))