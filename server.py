from model import AirportCode, connect_to_db, db, Experience
from flask import Flask, render_template, redirect, request, flash, session, jsonify

import requests
import json
import datetime
import pprint
import geojson

import os


sabre_access_token = os.environ["SABRE_ACCESS_TOKEN"]


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ABCDEF")

@app.route("/")
def homepage():
	"""Displays homepage."""

	return render_template("index.html")


@app.route("/result")
def results_page():
	""" Displays the results from the quiz """

	result = {"1": "results of 1","2":"results of 2","3":"results of 3"}


	return render_template("result.html",result=result)

@app.route("/airfaresearch.json")
def airfare_search():
	"""Using Sabre API request with Bridge, returning fares info."""

	# # getting the form values that the user has provided
	# origin = request.args.get('origin')
	# origin = origin[1:4]
	# earliest_departure = request.args.get('earliest-departure-date')
	# latest_departure = request.args.get('latest-departure-date')
	# length_of_stay = request.args.get('length-of-stay')
	# max_budget = request.args.get('max-budget')

	# TEST INPUT
	origin = "SFO"
	earliest_departure = "2016-01-12"
	latest_departure = "2016-01-31"
	length_of_stay = "3"
	max_budget = "1000"
	theme = "Outdoors"


	headers = {"Authorization": sabre_access_token}

	base_url = "http://bridge2.sabre.cometari.com/shop/flights/fares?"
	param_url = "origin=%s&earliestdeparturedate=%s&latestdeparturedate=%s&lengthofstay=%s&maxfare=%s&pointofsalecountry=US&ac2lonlat=1&theme=%s" % (
		origin, earliest_departure, latest_departure, length_of_stay, max_budget, theme)
	
	# USE BELOW URL FOR TESTING PURPOSES
	# param_url = "origin=SFO&earliestdeparturedate=2015-09-01&latestdeparturedate=2015-09-09&lengthofstay=3&maxfare=500&pointofsalecountry=US&ac2lonlat=1" 
	
	# putting together the url to request to Sabre's API
	final_url = base_url + param_url
	print final_url

	response = requests.get(final_url, headers=headers)

	response_text = response.json()

	# easier json read format
	pprint.pprint(response_text)

	fare_list = []

	for item in response_text:

		airport_code = item["id"]
		city = item["city"]

		# must double check if valid coords. API sometimes returns invalid destinations
		check_type = type(item["coords"]["latitude"])
		if check_type == type(u'-85.73'):
			lat = float(item["coords"]["latitude"])
		else: 
			continue

		check_type = type(item["coords"]["longitude"])
		if check_type == type(u'-85.73'):
			lon = float(item["coords"]["longitude"])
		else:
			continue

		fares = item["fares"]


		# must clean up invalid fares that are $0
		if fares[0]["lowestFare"] == 0:
			continue
		else:
			one_result = FlightDestinMarker(lon, lat, airport_code, city, fares)

			fare_list.append(one_result)
	

	marker_collection = geojson.FeatureCollection(fare_list)
	print marker_collection
	

	# import pdb; pdb.set_trace()
	# this returns geojson
	marker_geojson = geojson.dumps(marker_collection, sort_keys=True)

	return marker_geojson

	# # THIS WILL RETURN THE PLAIN JSON THAT WORKS
	# return jsonify(results=response_text) 


def get_experience(id):
    experience = Experience.get_experience_by_id(id)
    detail_info = experience.get_detailed_info()
    name = detail_info.get('name', None)
    excerpt = detail_info.get('excerpt', None)
    duration = detail_info.get('duration', None)
    price = detail_info.get('price', None)
    medias = detail_info.get('medias', None)
    photo_src = None
    if medias:
        photo_src = medias[0].get('src', None)


    print name, excerpt, duration, price, photo_src

    return 'hello'


if __name__ == "__main__":

	connect_to_db(app)
	PORT = int(os.environ.get("PORT", 5000))
	# DebugToolbarExtension(app)

	# SQLALCHEMY_TRACK_MODIFICATIONS = True



	DEBUG = "NO_DEBUG" not in os.environ

	app.run(debug=DEBUG)
