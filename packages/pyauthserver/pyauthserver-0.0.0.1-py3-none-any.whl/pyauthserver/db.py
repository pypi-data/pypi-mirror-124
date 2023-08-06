# coding: utf-8
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


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


