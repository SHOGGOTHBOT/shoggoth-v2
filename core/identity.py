import os

PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompt.txt")


def load_identity() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


IDENTITY = load_identity()
