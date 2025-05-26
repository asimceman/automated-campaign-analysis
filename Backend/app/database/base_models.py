from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
import sqlalchemy as sa

class BaseRoot(DeclarativeBase):
    pass

class Base(BaseRoot):
    __abstract__ = True
    __name__: str