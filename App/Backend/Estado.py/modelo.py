from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Estado(Base):
    __tablename__ = 'Estado'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)