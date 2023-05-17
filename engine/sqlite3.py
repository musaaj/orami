import os
from sqlite3 import sqlite_version
from ..driver.normalizer import(
        sqlite3,
        json_factory
    )
from ..settings import BASE_DIR, BACKENDS


engine = sqlite3.connect(os.path.join(BASE_DIR, BACKENDS["default"]["name"]), detect_types=sqlite3.PARSE_COLNAMES|sqlite3.PARSE_DECLTYPES)
engine.row_factory = json_factory
