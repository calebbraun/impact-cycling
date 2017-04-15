import flask
import simplejson
from urllib.request import urlopen
from flask import Flask, jsonify, render_template, request, session
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
from geopy.distance import vincenty

app = flask.Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def get_main_page():
    return flask.render_template('test-index.html')

@app.route('/logtrip/')
def log_trip():
    
    return flask.render_template('log-trip.html')

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
    app.run(host='localhost', port=5000, debug=True, use_reloader=True)