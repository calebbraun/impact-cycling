from sqlalchemy import Column, DateTime, String, Float, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    first_name = Column(String)
    # ---------------------------------------------------


class Trips(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    '''
    # Use cascade='delete,all' to propagate the deletion of a user onto its trips
    user = relationship(
        user_id,
        backref=backref('trips',
                        uselist=True,
                        cascade='delete,all'))'''