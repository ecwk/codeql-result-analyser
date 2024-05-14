import os
from typing import Annotated, Optional
from pathlib import Path

import typer
import pandas as pd

app = typer.Typer()


@app.command()
def main(
    query_file: Annotated[Path, typer.Option("-q", "--query-file")],
    results_file: Annotated[Path, typer.Option("-r", "--results-file")],
    filter: Annotated[
        str, typer.Option("-f", "--filter", help="Filter the CodeQL query results")
    ],
    source_dir: Annotated[Path, typer.Option("-d", "--source-dir")] = "./",
    context: Annotated[
        Optional[str],
        typer.Option("-c", "--context", help="Context to use for the analysis"),
    ] = "",
    model: Annotated[
        str, typer.Option("-m", "--model", help="Model to use for the analysis")
    ] = "codellama:70b",
    output_file: Annotated[Path, typer.Option("-o", "--output")] = "output.txt",
):
    query_file = query_file.read_text()
    results = read_query_file(results_file)

    for _, result in results.iterrows():
        source, snippet = parse_result(source_dir, result)
        prompt = create_filter_prompt(query_file, source, snippet, filter, context)
        response = infer_model(model, prompt)

        with open(output_file, "a") as f:
            f.write(f"====================\n---{model.upper()}---\n====================\n")
            f.write(f"::Result::\n{result}\n")
            f.write(f"\n::Response::\n{response}\n")


def read_query_file(query_file: str) -> pd.DataFrame:
    return pd.read_csv(
        query_file,
        header=None,
        names=[
            "query_name",
            "unknown",
            "problem_type",
            "problem",
            "file_path",
            "start_line",
            "start_col",
            "end_line",
            "end_col",
        ],
    )


def parse_result(dir: str, result: pd.Series) -> tuple[str, str]:
    source = Path(os.path.join(dir, result["file_path"].lstrip("/"))).read_text()

    start, end = result["start_line"], result["end_line"]
    snippet = (
        source.split("\n")[start:end]
        # if same line, return the line
        if start != end
        else source.split("\n")[start - 1 : start]
    )
    return source, snippet


def create_filter_prompt(
    query_file: str, source: str, snippet: str, filter: str, context: str = ""
) -> str:

    return """"""


def infer_model(model: str, prompt: str) -> str:
    return """"""
