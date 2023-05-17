import uuid
import sqlite3
from datetime import datetime

def json_factory(cursor, row):
    keys = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(keys, row)}


def uuid_adapter(value):
    if value:
        return str(value)


def datetime_converter(value):
    if value.decode():
        return datetime.fromisoformat(value.decode())


def uuid_converter(value):
    if value.decode():
        return uuid.UUID(value.decode())


def bool_converter(value):
    return True if int(value.decode()) else False


sqlite3.register_adapter(uuid.UUID, uuid_adapter)

sqlite3.register_converter("datetime", datetime_converter)
sqlite3.register_converter("uuid", uuid_converter)
sqlite3.register_converter("bool", bool_converter)
