import flask
import simplejson
from urllib.request import urlopen
from flask import Flask, flash, jsonify, render_template, request, session
from flask_googlemaps import GoogleMaps, Map
from geopy.distance import vincenty
from models import *
import trip_log

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def registration():
    if not session.get('logged_in'):
        return render_template('register.html')
    else:
        return profile()

@app.route('/register', methods=['POST'])
def register():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    if POST_PASSWORD != str(request.form['cpassword']):
        return
    POST_FIRSTNAME = str(request.form['firstname'])

    print (POST_USERNAME, POST_PASSWORD, POST_FIRSTNAME)

    Session = sessionmaker(bind=engine)
    s = Session()
    record = User(POST_USERNAME, POST_PASSWORD, POST_FIRSTNAME)
    s.add(record)
    s.commit()

@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        POST_USERNAME = str(request.form['username'])
        user_data = [POST_USERNAME]
        return flask.render_template('profile.html', userData = user_data)
#        return profile(POST_USERNAME)
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
    
    POST_USERNAME = str(request.form['username'])
    user_data = [POST_USERNAME]

    return flask.render_template('profile.html', userData = user_data)


@app.route('/logtrip/')
def log_trip():
    past_trips = trip_log.get_past_trips()
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

@app.route('/game/')
def game():
    return "Coming soon!"

@app.route('/settings/')
def settings():
    return "Coming soon!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
    #app.run(host='localhost', port=5000, debug=True, use_reloader=True)
