import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef_old import *

engine = create_engine('sqlite:///tutorial.db', echo=True)

# delete
User.__table__.drop(engine)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin", "password", "Dustin", 120)
session.add(user)

user = User("python", "python", "aeg", 12)
session.add(user)

# commit the record the database
session.commit()

session.commit()