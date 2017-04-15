import flask
import datetime
import simplejson
import urllib2
#from urllib.request import urlopen
from flask import Flask, flash, jsonify, render_template, request, session
from flask_googlemaps import GoogleMaps, Map
from geopy.distance import vincenty
from models import *
import trip_log
from sqlalchemy.sql import and_

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'DYF~KPCVVjkdfFEQ93jJ]'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# create tables
with app.app_context():
    db.create_all()

@app.route('/')
def get_main_page():
    return flask.render_template('index.html')

@app.route('/about/')
def about():
    return flask.render_template('about.html')

@app.route('/meettheteam/')
def meet_the_team():
    return flask.render_template('comingsoon.html')

@app.route('/register')
def registration():
    if not session.get('logged_in'):
        return flask.render_template('register.html')
    else:
        return profile()

@app.route('/register', methods=['POST'])
def register():
    new_username = str(request.form['username'])
    new_password = str(request.form['password'])
    new_firstname = str(request.form['firstname'])

    if new_password != str(request.form['cpassword']):
        print("Error!")
        session['logged_in'] = False
    else:
        session['logged_in'] = True
        new_user = User(new_username, new_password, new_firstname)
        db.session.add(new_user)
        db.session.commit()

    return registration()

@app.route('/login')
def home():
    if not session.get('logged_in'):
        return flask.render_template('login.html')
    else:
#        return flask.render_template('profile.html', userData = user_data)
        return profile()
        #return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    session['username'] = POST_USERNAME

    admin = User.query.filter_by(username=POST_USERNAME).first()
    if not admin:
        flash('invalid username!')
    elif admin.password == POST_PASSWORD:
        session['logged_in'] = True
    else:
        flash('wrong password!')
        session['logged_in'] = False
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile/")
def profile():
    
    username = session['username']
    name = User.query.filter_by(username=username).first().first_name
    userid = User.query.filter_by(username=username).first().id
    
    
    qry = Trips.query.filter_by(user_id=userid).count()
    
    if qry == 0:
        print("NO TRIPS")
    distance = 0
    
    for i in range(1,qry+1):
        qry2 = Trips.query.filter(and_(Trips.user_id == userid, Trips.id == i)).first().distance
        print(qry2)
        distance += qry2
        
    gallons_used = distance / 25.5
    money_saved = 2.42 * gallons_used
    co2 = distance * 411
    
    distance = "{0:.2f}".format(distance)
    gallons_used = "{0:.2f}".format(gallons_used)
    money_saved = "{0:.2f}".format(money_saved)
    co2 = "{0:.2f}".format(co2)
    
    user_data = [name, distance, money_saved, co2]

    return flask.render_template('profile.html', userData = user_data)


@app.route('/logtrip/')
def log_trip():
    past_trips = trip_log.get_past_trips(session['username'])
    return flask.render_template('log-trip.html', trips=past_trips)

@app.route('/tripdata/', methods=['POST'])
def trip_data():

    api_key = 'AIzaSyCgL4EhbainFOaUs3OJDUasN_9X3Kv7CN0'

    startpoint = request.form['startpoint']
    endpoint = request.form['endpoint']

    startpoint_url = startpoint.replace(" ", "+")
    endpoint_url = endpoint.replace(" ", "+")

    urlstring1 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + startpoint_url + "&key=" +api_key
    start_info = simplejson.load(urlopen(urlstring1))
    start_lat = start_info['results'][0].get("geometry").get("location").get("lat")
    start_lon = start_info['results'][0].get("geometry").get("location").get("lng")
    start_coordinate = [start_lat, start_lon]

    urlstring2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + endpoint_url + "&key=" + api_key
    end_info = simplejson.load(urlopen(urlstring2))
    end_coordinate = [end_info['results'][0].get("geometry").get("location").get("lat"), end_info['results'][0].get("geometry").get("location").get("lng")]


    distance = vincenty(start_coordinate, end_coordinate).miles

    co2 = 411 * distance

    #avg mpg: 25.5
    #avg price per gallon: 2.42
    gallons_used = distance / 25.5
    money_saved = 2.42 * gallons_used

    user_id = User.query.filter_by(username=session['username']).first().id
    new_trip = Trips(start_lat, start_lon, distance, datetime.datetime.now(), user_id)
    db.session.add(new_trip)
    db.session.commit()
    print(distance)

    points = [startpoint, endpoint, distance, co2, money_saved]

    return flask.render_template('trip-data.html', points = points)

@app.route('/game/')
def game():
    return flask.render_template('comingsoon.html')

@app.route('/settings/')
def settings():
    return flask.render_template('comingsoon.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
    #app.run(host='localhost', port=5000, debug=True, use_reloader=True)
