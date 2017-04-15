import time
from datetime import datetime, date
import calendar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///data')

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User(username="python", password="python", first_name="Dustin")
session.add(user)

timestamp1 = datetime(2017, 4, 12)
trip1 = Trips(lat=120, lon=140, date=timestamp1)
session.add(trip1)

# commit the record the database
session.commit()