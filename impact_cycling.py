import flask
import simplejson
from urllib2 import urlopen
from flask import Flask, jsonify, render_template, request, session
from flask_googlemaps import GoogleMaps, Map
import os
from geopy.distance import vincenty
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tabledef import *
import trip_log

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'DYF~KPCVVjkdfFEQ93jJ]'
engine = create_engine('sqlite:///tutorial.db', echo=True)

@app.route('/')
def get_main_page():
    return flask.render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return profile()
        #return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    session['username'] = POST_USERNAME

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile/")
def profile():
    POST_USERNAME = str(request.form['username'])
    user_data = [POST_USERNAME]
    return flask.render_template('profile.html', userData = user_data)


@app.route('/logtrip/')
def log_trip():
    past_trips = trip_log.get_past_trips()

    user = User.query.filter_by(username=session['username']).first()
    past_trips = user.id
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
    start_coordinate = [start_info['results'][0].get("geometry").get("location").get("lat"), start_info['results'][0].get("geometry").get("location").get("lng")]

    urlstring2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + endpoint_url + "&key=" + api_key
    end_info = simplejson.load(urlopen(urlstring2))
    end_coordinate = [end_info['results'][0].get("geometry").get("location").get("lat"), end_info['results'][0].get("geometry").get("location").get("lng")]


    distance = vincenty(start_coordinate, end_coordinate).miles

    co2 = 411 * distance

    #avg mpg: 25.5
    #avg price per gallon: 2.42
    gallons_used = distance / 25.5
    money_saved = 2.42 * gallons_used

    print(distance)

    points = [startpoint, endpoint, distance, co2, money_saved]

    return flask.render_template('trip-data.html', points = points)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
    #app.run(host='localhost', port=5000, debug=True, use_reloader=True)
