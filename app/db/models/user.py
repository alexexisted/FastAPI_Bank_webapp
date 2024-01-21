from sqlalchemy import Column, Integer, String, Boolean
from db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    balance = Column(Integer, default=0)


"""
making a model of table of user in bank. i decided not to use relationship and i don't have other tables
id column will be primary key to identify user
email will be used for login instead using username 
password column will contain the hash
name and surname i'll use just for display profile
is_superuser column will be used for admin
balance will be zero by default after creating account
"""