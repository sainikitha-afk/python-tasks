import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# =======================
# FIELD DESCRIPTORS
# =======================

class Field:
    def __init__(self, column_type, nullable=False, unique=False):
        self.column_type = column_type
        self.nullable = nullable
        self.unique = unique
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)


class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)


class ForeignKey(Field):
    def __init__(self, model, related_name=None):
        super().__init__("INTEGER")
        self.model = model
        self.related_name = related_name


# =======================
# META CLASS
# =======================

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)

        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value

        attrs["_fields"] = fields
        attrs["_table"] = name.lower()

        return super().__new__(cls, name, bases, attrs)


# =======================
# BASE MODEL
# =======================

class Model(metaclass=ModelMeta):
    id = IntegerField()

    def __init__(self, **kwargs):
        for field in self._fields:
            setattr(self, field, kwargs.get(field))

    @classmethod
    def create_table(cls):
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for name, field in cls._fields.items():
            if isinstance(field, ForeignKey):
                col = f"{name}_id INTEGER"
            else:
                col = f"{name} {field.column_type}"

            if not field.nullable:
                col += " NOT NULL"
            if field.unique:
                col += " UNIQUE"

            columns.append(col)

        sql = f"CREATE TABLE IF NOT EXISTS {cls._table} ({', '.join(columns)});"

        print("SQL:", sql)

        conn = get_connection()
        conn.execute(sql)
        conn.commit()
        conn.close()

        print(f"Table '{cls._table}' created.\n")

    def save(self):
        fields = []
        values = []

        for name, field in self._fields.items():
            val = getattr(self, name)
            if isinstance(field, ForeignKey):
                name = f"{name}_id"

            fields.append(name)
            values.append(val)

        placeholders = ", ".join(["?"] * len(values))

        sql = f"INSERT INTO {self._table} ({', '.join(fields)}) VALUES ({placeholders});"

        print("SQL:", sql.replace("?", "{}").format(*values))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()

        self.id = cursor.lastrowid

        conn.close()

        print(f"Record saved: {self.__class__.__name__}(id={self.id})\n")

    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


# =======================
# QUERYSET
# =======================

class QuerySet:
    def __init__(self, model):
        self.model = model
        self.conditions = []
        self.order = ""

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            if "__" in key:
                field, op = key.split("__")
                if op == "gte":
                    self.conditions.append(f"{field} >= {value}")
                elif op == "lte":
                    self.conditions.append(f"{field} <= {value}")
            else:
                self.conditions.append(f"{key} = '{value}'")
        return self

    def order_by(self, field):
        direction = "ASC"
        if field.startswith("-"):
            field = field[1:]
            direction = "DESC"

        self.order = f"ORDER BY {field} {direction}"
        return self

    def all(self):
        where = ""
        if self.conditions:
            where = "WHERE " + " AND ".join(self.conditions)

        sql = f"SELECT * FROM {self.model._table} {where} {self.order};"

        print("SQL:", sql)

        conn = get_connection()
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        return rows