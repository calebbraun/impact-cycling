from sqlalchemy import Column, DateTime, String, Float, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    first_name = Column(String)

    def __init__(self, name=None, password=None, first_name=None):
        self.username = name
        self.password = password
        self.first_name = first_name

    def __repr__(self):
        return '<User %r>' % (self.username)
    # ---------------------------------------------------


class Trips(db.Model):
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
