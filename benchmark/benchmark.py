from typing import Annotated, List, Optional

import typer
import ollama
import pandas as pd


def stream_model_response(model: str, message: str) -> str:
    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": message}],
        options={"temperature": 0.0},
        stream=True,
    )
    return stream


def get_model_response(model: str, message: str) -> str:
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": message}],
        options={"temperature": 0.0},
    )
    return response["message"]["content"]


def get_prompt(codeql_query: str, snippet: str, source_file: str, filter_str: str):

    return f"""# CONTEXT
You will be given a CodeQL query, CPP snippet, the source file containing the snippet, and a filter.

The CPP snippet was retrieved using the CodeQL query, a language used for static analysis. You don't have to understand the syntax of the language, but you should be able to understand the structure of the code.

Each line in the CPP snippet and source file will be prepended with the line number "L<i>: " where i is the line number. The line number in the snippet will correspond to the line number in the source file.

# INSTRUCTION
Given the filter, determine if the source file matches the filter (1) or not (0).

Strictly follow the following output format when giving your answer.

# OUTPUT FORMAT
Return a JSON of the following format.
{{
    "explanation": <str>,
    "is_filtered": <1 or 0>
}}

ONLY RETURN JSON. DO NOT PRINT ANYTHING ELSE.

# INPUT

## CodeQL Query
{codeql_query}

## CPP Snippet
```cpp
{snippet}
```

## Source File
```cpp
{source_file}
```

## Filter
{filter_str}"""


def main(
    models: Annotated[List[str], typer.Option("-m", "--model")],
    # `test_paths` file will be a standard codeql csv response with a `label` column (1 - filtered, 0 - not filtered)
    codeql_query_file: Annotated[str, typer.Option("-q", "--codeql-query")],
    test_file: Annotated[str, typer.Option("-t", "--test")],
    source_dir: Annotated[Optional[str], typer.Option("-d", "--source-dir")] = "./",
    output_file: Annotated[Optional[str], typer.Option("-o", "--output-file")] = None,
):
    for model in models:
        try:
            ollama.show(model)
        except ollama.ResponseError:
            print(f"Model {model} not found. Pulling...")
            ollama.pull(model)

        print(f"Running tests on {model}...")
        test_df = pd.read_csv(test_file)
        codeql_query = open(codeql_query_file, "r").read()

        if output_file:
            with open(output_file, "a") as f:
                f.write(f"---{model.upper()}---\n")

        for index, row in test_df.iterrows():
            source_file_path = source_dir + "/" + row["file_path"]

            label = row["label"]
            source_file: str = open(source_file_path, "r").read()
            start_row, end_row = (
                row["start_line"],
                row["end_line"],
            )
            source_file_split = source_file.split("\n")
            source_file_with_number = [
                f"L{i + 1}: {line}" for i, line in enumerate(source_file_split)
            ]
            source_file = "\n".join(source_file_with_number)

            snippet = "\n".join(
                source_file_with_number[start_row:end_row]
                if start_row != end_row
                else source_file_with_number[start_row - 1 : start_row]
            )

            prompt = get_prompt(codeql_query, snippet, source_file, row["filter"])

            if output_file:
                with open(output_file, "a") as f:
                    f.write(
                        f"File: {row['file_path']}\nLabel: {label}\nPrompt:\n{prompt}\n"
                    )

            print(f"\n\nGetting response for {row['file_path']} from {model}...")

            response = ""
            stream = stream_model_response(model, prompt)
            print("Received stream. Printing stream now...")
            for chunk in stream:
                message = chunk["message"]["content"]

                print(message, end="", flush=True)
                response += message

            if output_file:
                with open(output_file, "a") as f:
                    f.write(f"Response:\n{response}\n\n")


if __name__ == "__main__":
    typer.run(main)
