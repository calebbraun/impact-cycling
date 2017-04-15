from models import *

def get_past_trips(username):
    user = User.query.filter_by(username=username).first()
    trips = Trips.query.filter_by(user_id=user.id).all()
    return trips
