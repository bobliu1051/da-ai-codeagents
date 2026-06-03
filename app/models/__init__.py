"""
Base model class.

NOTE: This was meant to be the start of a custom ORM layer but the project
moved back to raw SQL. Some models still inherit from this but most code
bypasses it.
"""


class BaseModel:
    table_name = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(**dict(row))

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
