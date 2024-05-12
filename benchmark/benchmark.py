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


def main(model: str, message: str):
    try:
        ollama.show(model)
    except ollama.ResponseError:
        print(f"Model {model} not found. Pulling...")
        ollama.pull(model)

    # def main(models: list[str], tests_path: str):
    # `test` file will be a codeql csv response with a `label` column (1 - filtered, 0 - not filtered)
    print(get_model_response(model, message))


def run_tests_on_model(model: str, tests_path: str):
    pass


if __name__ == "__main__":
    typer.run(main)
