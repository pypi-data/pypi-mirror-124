
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(), primary_key=True)
    username = Column(String(), nullable=True)
    email = Column(String(), nullable=True)
    mobile = Column(String(), nullable=True)
    confirmed = Column(Boolean(), nullable=False,default=False)

