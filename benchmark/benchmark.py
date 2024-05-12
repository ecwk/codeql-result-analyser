from typing import Annotated, List, Optional

import typer
import ollama


def stream_model_response(model: str, message: str, handler: callable):
    stream = ollama.chat(model="codellama", message="Hello, how are you?", stream=True)

    for chunk in stream:
        message = chunk["message"]["content"]
        handler(message)
        # print(chunk["message"]["content"], end="", flush=True)


def get_model_response(model: str, message: str):
    response = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
    return response["message"]["content"]


def main(
    models: Annotated[List[str], typer.Option("-m", "--model")],
    # `test_paths` file will be a standard codeql csv response with a `label` column (1 - filtered, 0 - not filtered)
    test: Annotated[str, typer.Option("-t", "--test")],
    output_file: Annotated[str, typer.Option("-o", "--output-file")] = None,
):
    for model in models:
        try:
            ollama.show(model)
        except ollama.ResponseError:
            print(f"Model {model} not found. Pulling...")
            ollama.pull(model)

        print(get_model_response(model, "What is the Python dictionary .keys() method for?"))


def run_tests_on_model(model: str, tests_path: str):
    pass


if __name__ == "__main__":
    typer.run(main)
