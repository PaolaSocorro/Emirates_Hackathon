from model import AirportCode, connect_to_db, db, Experience
from flask import Flask, render_template, redirect, request, flash, session, jsonify

import requests
import json
import datetime
import pprint
import geojson

import os


# sabre_access_token = os.environ["SABRE_ACCESS_TOKEN"]


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ABCDEF")

@app.route("/")
def homepage():
	"""Displays homepage."""

	return render_template("index.html")


@app.route("/autocomplete")
def autocomplete():
	"""From airport codes database, provide autocomplete in user's arrival input using AJAX."""

	search_value = request.args.get('term')

	query = AirportCode.query.filter(db.or_(AirportCode.code.ilike("%%%s%%" % (search_value)), 
											AirportCode.location.ilike("%%%s%%" % (search_value)))).all()
	
	suggestion_list = []

	for item in query:
		code = item.code
		location = item.location
		suggestion_string = "(%s) %s" %(code, location)
		suggestion_list.append(suggestion_string)
	
	# print suggestion_list
	
	return jsonify(data=suggestion_list)
	

@app.route("/persona")
def get_personas():
# places format is as follows: international, city/country, score, lon, lat 
	results = {'voyager': [[1, 'Czech Republic', "PRG", 9.0, 14.2600002, 50.1007996, "img/voyager_czech.jpg"], 
							[1, 'Ireland', "DUB", 7.5, -6.249909800000069, 53.42644809999999, "img/voyager_ireland.jpg"], 
							[1, 'Prince Edward Island, Canada',"YYG", 9.9, -63.1211014, 46.2900009]], 
				'venturer': [[1, 'South Africa',"CPT", 9.5, 18.6016998, -33.9648018], 
							[1, 'Victoria, British Columbia, Canada', "YYJ", 8.5, -123.4302928, 48.6402067], 
							[1, 'Kenya', "NBO", 9.5, 36.927109, -1.333731]], 
				'traditional': [[1, 'Vancouver, British Columbia, Canada', "YVR", 8.0, -123.1775716, 49.1959446, "img/traditional_vanouver.jpg"], 
								[1, 'Australia',"CBR", 8.5, 149.1950073, -35.3069, "img/traditional_australia.jpg"], 
								[1, 'London, England', "LCY", 7.0, 0.055278, 51.505268, "img/traditional_london.jpg"]], 
				'pioneer': [[1, 'Peru', "LIM", 9.5, -77.114304, -12.021800], 
							[1, 'Ireland', "DUB", 7.5, -6.249909800000069, 53.42644809999999], 
							[1, 'British Columbia, Canada', "YYJ", 9.9, -123.1775716, 49.1959446]]}


	persona = request.args.get("persona")

	top_3_international_places = results[persona]

	top_3_dict = []

	for item in top_3_international_places:
		one_place = {
			"name": item[1],
			"aiportcode": item[2],
			"lon": item[4],
			"lat": item[5],
			"img_url": item[6]
		}
		top_3_dict.append(one_place)

	return jsonify(results=top_3_dict)


@app.route("/result")
def results_page():
	""" Displays the results from the quiz """

	result = {"pioneer":{"1": "results of 1","2":"results of 2","3":"results of 3"}}


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
	origin = request.args.get('origin')
	origin = origin[1:4]
	earliest_departure = "2016-01-12"
	latest_departure = "2016-01-31"
	length_of_stay = "3"
	max_budget = "1000"
	theme = request.args.get("persona")


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

		# some results don't have a city name
		if city == None:
			continue

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
			# one_result = FlightDestinMarker(lon, lat, airport_code, city, fares)
			one_result = {"city": city,
							"airportcode": airport_code,
							"lon": lon,
							"lat": lat,
							"fares": fares}
			fare_list.append(one_result)
	

	return jsonify(data=fare_list)

	# # THIS WILL RETURN THE PLAIN JSON THAT WORKS
	# return jsonify(results=response_text) 

@app.route('/experiencesearch.json')
def searchExperience():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    print lat, lon
    search_results = Experience.get_experience_by_lat_long(original_lat=float(lat), original_lng=float(lon))
    print search_results
    return_dict = {}
    if search_results:
        for experience in search_results:
            detail_info = experience.get_detailed_info()
            name = detail_info.get('name', None)
            excerpt = detail_info.get('excerpt', None)
            duration = detail_info.get('duration', None)
            price = detail_info.get('price', None)
            medias = detail_info.get('medias', None)
            photo_src = None
            if medias:
                photo_src = medias[0].get('src', None)
            return_dict[experience.id] = {
                'name': name,
                'excerpt': excerpt,
                'duration': duration,
                'price': price,
                'photo_src': photo_src,
            }
        print return_dict
        return jsonify(return_dict)
    else:
        return jsonify("null")


if __name__ == "__main__":

	connect_to_db(app)
	PORT = int(os.environ.get("PORT", 5000))
	# DebugToolbarExtension(app)

	# SQLALCHEMY_TRACK_MODIFICATIONS = True

    
	DEBUG = "NO_DEBUG" not in os.environ
	app.run(debug=DEBUG)

