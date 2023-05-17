"""This is an attemp to implement Django ORM like libry atop Python sqlite3.
It is not design to be 100% like Django ORM.
It is meant for quick non critical scripting such as
custom social bots that makes little database interactions. ORAMI is developed by Musa Ibrahim <musaaj@gmail.com>

Usage: 
>>>from orami import Model
>>>from orami.fields import TextField, IntegerField
>>>from orami.fields import BoolField
>>>
>>>class User(Model):
>>>    first_name = TextField()
>>>    last_name = TextField()
>>>    email = TextField(unique=True)
>>>    is_active = BoolField()
>>>    is_pro = BoolField()
>>>
>>>
>>>#create table
>>>User.migrate()
>>>
>>>#create an isinstance
>>>user = User(
            first_name="Musa",
            last_name="Ibrahim",
            email="musaaj@gmail.com",
            is_active=False,
            is_pro=False)
>>>#save to the database
>>>user.save()
>>>
>>>#get a record from database
>>>user = User.get(email="musaaj@gmail.com")
>>>#update a record
>>>user.is_active = True
>>>#save to database
>>>user.save()
>>>
>>>#delete record from database
>>>user.delete()
"""


from ..engine.sqlite3 import engine, sqlite3
from .fields import BaseField, IntegerField, DatetimeField, TextField


class Model:
    __engine = engine
    pk = IntegerField(primary_key=True, auto_increment=True)
    created_at = DatetimeField(default="CURRENT_TIMESTAMP")


    def __init__(self, **extras):
        for key, value in extras.items():
            self.__setattr__(key, value)

    def save(self):
        """save an instance to database"""
        insert_query = f"""INSERT INTO {self.__class__.__name__.lower()} ({', '.join(self.__dict__.keys())})
        VALUES({', '.join(['?' for key in self.__dict__.keys()])})"""
        update_query = f"""UPDATE {self.__class__.__name__.lower()} SET {'=?, '.join(self.__dict__.keys())}=? WHERE pk = ?"""
        cursor = self.__engine.cursor()
        if self.__dict__.get("pk"):
            cursor.execute(update_query, tuple(self.__dict__.values()) + (self.pk,))
        else:
            cursor.execute(insert_query, tuple(self.__dict__.values()))
        self.__engine.commit()

    def delete(self):
        """delete an instance of this model"""
        cursor = self.__engine.cursor()
        try:
            cursor.execute(f"DELETE FROM {self.__class__.__name__.lower()} WHERE pk = ?", (self.pk,))
            self.__engine.commit()
        except sqlite3.OperationalError as e:
            raise sqlite3.OperationalError("record not exists")

    @classmethod
    def table_sql(cls):
        """Generate sql table defination"""
        fields = ", ".join([f"{key} {getattr(cls, key)}" for key in dir(cls) if not key.startswith("_") and isinstance(getattr(cls, key), BaseField)])
        return f"CREATE TABLE {cls.__name__.lower()}({fields})"

    @classmethod
    def migrate(cls):
        """Create or update sqlite3 table defination of this model
        """
        try:
            cls.__engine.execute(cls.table_sql())
        except sqlite3.OperationalError as e:
            print(e)
            cursor = cls.__engine.cursor()
            tmp_table = cls.table_sql().replace(cls.__name__.lower(), "temp")
            cursor.execute(f"SELECT * FROM {cls.__name__.lower()}")
            old_table_columns = [column[0] for column in cursor.description]
            new_table_columns = [key for key in dir(cls) if not key.startswith("_") and isinstance(getattr(cls, key), BaseField)]
            columns_to_select = [key for key in old_table_columns if key in new_table_columns]
            cursor.execute("DROP TABLE IF EXISTS temp")
            cursor.execute(tmp_table)
            cursor.execute(f"INSERT INTO temp({', '.join(columns_to_select)}) SELECT {', '.join(columns_to_select)} FROM {cls.__name__.lower()}")
            cursor.execute(f"DROP TABLE {cls.__name__.lower()}")
            cursor.execute(cls.table_sql())
            cursor.execute(f"INSERT INTO {cls.__name__.lower()} SELECT * FROM temp")
            cursor.execute("DROP TABLE temp")
            cls.__engine.commit()

    @classmethod
    def get(cls, **extras):
        """Get a single objects that satisfies a given condition

        """
        cursor = cls.__engine.cursor()
        cursor.execute(f"SELECT * FROM {cls.__name__.lower()} WHERE {'=? '.join(extras.keys())}=?", tuple(extras.values()))
        result = cursor.fetchone()
        if result is not None:
            return cls(**result)

    @classmethod
    def query(cls, **extras):
        cursor = cls.__engine.cursor()
        cursor.execute(f"SELECT * FROM {cls.__name__.lower()} WHERE {'=? '.join(extras.keys())}=?", tuple(extras.values()))
        result = cursor.fetchone()
        if result is not None:
            return tuple([cls(**obj) for obj in result])

    @classmethod
    def all(cls):
        """get all the objects in this model"""
        cursor = cls.__engine.cursor()
        cursor.execute(f"SELECT * FROM {cls.__name__.lower()}")
        return tuple([cls(**obj) for obj in cursor.fetchall()])
