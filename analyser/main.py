from typing import Annotated
from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def main(
    path: Path,
    # file: Path,
    filter: Annotated[
        str, typer.Option("-f", "--filter", help="Filter the CodeQL query results")
    ],
):
    pass
