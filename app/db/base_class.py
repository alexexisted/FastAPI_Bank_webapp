from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


"""
making a base class for sqlalchemy to define data models in db

This code uses the @as_declarative() decorator to tell SQLAlchemy, 
that the Base class should be used as the base class for all declared data models.

The @as_declarative() decorator makes a class declarative, 
making it easier to define mappings between classes and database tables.
"""