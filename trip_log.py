from models import *

def get_past_trips():
    user = User.query.filter_by(username=session['username']).first()
    past_trips = user
    return past_trips
