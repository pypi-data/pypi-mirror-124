import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey,Boolean,Float
from sqlalchemy.ext.declarative import declarative_base
import uuid
import time

Base = declarative_base()
class HelperBase:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def to_json(self):
        return json.dumps(self.as_dict())
def gen_id():
    return uuid.uuid4().hex
class User(Base,HelperBase):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True,default=gen_id)
    username = Column(String(30), nullable=True)
    email = Column(String(30), nullable=True)
    mobile = Column(String(30), nullable=True)
    confirmed = Column(Boolean(), nullable=False,default=False)
    created=Column(Float(),nullable=False,default=time.time)
    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}

