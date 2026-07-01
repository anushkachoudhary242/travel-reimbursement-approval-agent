import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def load_json(relative_path: str):
    """
    Loads any JSON file from the project directory.

    Example:
        load_json("data/limits.json")
    """

    file_path = BASE_DIR / relative_path

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)