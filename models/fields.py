"""Sql data fields mapper classes"""

class BaseField:
     
    def __init__(self, **options) -> None:
        for key, value in options.items():
            setattr(self, key, value)
        if not options.get("primary_key"):
            self.primary_key = False
        if not options.get("auto_increment"):
            self.auto_increment = False
        if not options.get("unique"):
            self.unique = False
        if not options.get("default"):
            self.default = False
        if not options.get("null"):
            self.null = True

    def __str__(self):
        return f"{self.data_type.upper()} {'PRIMARY KEY' if self.primary_key else ''} "+\
                f"{'AUTOINCREMENT' if self.auto_increment else ''} "+\
                f"{'UNIQUE' if self.unique else ''}"+\
                f"{'DEFAULT ' + str(self.default) if self.default else ''} "+\
                f"{'' if self.null else 'NOT NULL'}"


class TextField(BaseField):
    
    def __init__(self, **options) -> str:
        super().__init__(**options)
        self.data_type = "text"


class IntegerField(BaseField):

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.default = 0
        self.data_type = "integer"


class BoolField(BaseField):
    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.data_type = "bool"
        self.default = False


class UUIDField(BaseField):

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.data_type = "uuid"


class DatetimeField(BaseField):

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.data_type = "datetime"
