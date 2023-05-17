import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

BACKENDS = {
    "default": {
        "engine": "engine.sqlite3",
        "name": "db.sqlite3",
    }
}
