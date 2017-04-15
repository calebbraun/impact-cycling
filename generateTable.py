import time
from datetime import datetime, date
import calendar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from impact_cycling import db

engine = create_engine('sqlite:///tutorial.db')

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User(username="python", password="python", first_name="Dustin")
trip = Trips(lat=12.0, lon=140.34, distance=2, date=datetime.datetime.now(), user_id=1)
session.add(user)

timestamp1 = datetime(2017, 4, 12)
trip1 = Trips(lat=120, lon=140, date=timestamp1)
session.add(trip1)

# commit the record the database
session.commit()
