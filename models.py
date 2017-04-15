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

    def __init__(self, username=None, password=None, first_name=None):
        self.username = username
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
    distance = Column(Float)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, lat=None, lon=None, distance=None, date=None, user_id=None):
        self.lat = lat
        self.lon = lon
        self.distance = distance
        self.date = date
        self.user_id = user_id

    def __repr__(self):
        return '<User_id %d>' % (self.user_id)
    '''
    # Use cascade='delete,all' to propagate the deletion of a user onto its trips
    user = relationship(
        user_id,
        backref=backref('trips',
                        uselist=True,
                        cascade='delete,all'))'''
