"""
db schemas
"""

import os, sys

import config

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    topic = Column(String(500))

class Detail(Base):
    __tablename__ = 'detail'
    id = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    detail = Column(String(250))

engine = create_engine(config.DATABASE_PATH)

Base.metadata.create_all(engine)
