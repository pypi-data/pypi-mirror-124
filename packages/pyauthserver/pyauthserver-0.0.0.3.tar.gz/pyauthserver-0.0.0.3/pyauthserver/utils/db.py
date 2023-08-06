

# coding: utf-8
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import exists
from pyauthserver.models.user import User
from pyauthserver.config import mysql
def gen_condition_expr_list(model, **kwargs):
    parts = []
    for k, v in kwargs:
        parts.append(getattr(model, k) == v)
    return parts
def gen_mysql_uri(username,password,host,db_name):
    return 'mysql+pymysql://%s:%s@%s/%s'%(username,password,host,db_name)
def gen_engine(uri,echo=True,encoding='utf-8'):
    return create_engine(uri,echo=echo,encoding=encoding)
def get_session(engine):
    Session=sessionmaker(bind=engine)
    return Session()
def get_declarative_base():
    return declarative_base()

Base=get_declarative_base()


class DBHelper:
    def __init__(self,model,uri):
        self.model=model
        self.engine=gen_engine(uri)

    def get_session(self):
        return get_session(self.engine)
    def find_one(self,id=None,**kwargs):
        if id:
            kwargs.update(id=id)
        with self.get_session() as session:
            return session.query(self.model).filter(*gen_condition_expr_list(self.model,**kwargs)).first()
    def find_all(self,**kwargs):
        with self.get_session() as session:
            return session.query(self.model).filter(*gen_condition_expr_list(self.model, **kwargs))
    def exists(self,id=None,**kwargs):
        if id:
            kwargs.update(id=id)
        with self.get_session() as session:
            return session.query(exists().where(*gen_condition_expr_list(self.model,**kwargs))).scalar()
    def create_one(self,**kwargs):
        one=self.model(**kwargs)
        with self.get_session() as session:
            session.add(one)
            session.commit()



def get_db_helper(model)->DBHelper:
    return DBHelper(model,gen_mysql_uri(
        username=mysql.username,
        password=mysql.password,
        host=mysql.host,
        db_name=mysql.db_name
    ))